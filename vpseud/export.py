"""Export the trained model to ONNX, quantize it to int8, and check it.

    python -m vpseud.export --model out/model --data data --out out/onnx

Writes detector.onnx (int8), tokenizer.json and manifest.json. The manifest
holds the sha256 of each file and the dev scores of the int8 model, so the
number the classifier is gated on is the number of the file it loads.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil

import torch
from transformers import AutoModelForTokenClassification

from .infer import OnnxDetector
from .metrics import score
from .train import load


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="out/model")
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default="out/onnx")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    model = AutoModelForTokenClassification.from_pretrained(a.model).eval().cpu()
    fp32 = os.path.join(a.out, "detector-fp32.onnx")
    ids = torch.ones((1, 16), dtype=torch.long)
    torch.onnx.export(
        model, (ids, torch.ones_like(ids)), fp32,
        input_names=["input_ids", "attention_mask"], output_names=["logits"],
        dynamic_axes={"input_ids": {0: "batch", 1: "seq"}, "attention_mask": {0: "batch", 1: "seq"}, "logits": {0: "batch", 1: "seq"}},
        opset_version=17, dynamo=False,
    )
    from onnxruntime.quantization import QuantType, quantize_dynamic

    int8 = os.path.join(a.out, "detector.onnx")
    quantize_dynamic(fp32, int8, weight_type=QuantType.QInt8, op_types_to_quantize=["MatMul", "Gather"])
    shutil.copy(os.path.join(a.model, "tokenizer.json"), os.path.join(a.out, "tokenizer.json"))

    report = {}
    for variant, path in (("fp32", fp32), ("int8", int8)):
        det = OnnxDetector(path, os.path.join(a.out, "tokenizer.json"))
        for name in ("dev_names", "dev_heldout"):
            # The first 1500 of each: ONNX on CPU is the slow part of a run.
            rows = load(os.path.join(a.data, f"{name}.jsonl"))[:1500]
            report[f"{variant}/{name}"] = score(rows, [det.spans(r["text"]) for r in rows])
    os.remove(fp32)
    manifest = {
        "base": "distilbert/distilbert-base-multilingual-cased",
        "labels": ["O", "B-PER", "I-PER"],
        "files": {f: {"sha256": sha256(os.path.join(a.out, f)), "bytes": os.path.getsize(os.path.join(a.out, f))}
                  for f in ("detector.onnx", "tokenizer.json")},
        "dev": report,
    }
    with open(os.path.join(a.out, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
