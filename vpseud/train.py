"""Fine-tune a cased multilingual DistilBERT to mark private people's names.

Labels are O, B-PER, I-PER on word pieces, made from the character spans of
generate.py. The thesis model (tux.ai pii_model_v4) was English and uncased;
case is the best clue for a name, so this one is cased.

    python -m vpseud.train --data data --out out/model
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np
import torch
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)

from .metrics import score

LABELS = ["O", "B-PER", "I-PER"]
BASE = "distilbert/distilbert-base-multilingual-cased"
MAX_LEN = 192


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


def encode(tok, rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        enc = tok(r["text"], truncation=True, max_length=MAX_LEN, return_offsets_mapping=True)
        labels = []
        prev_in = False
        for (s, e) in enc["offset_mapping"]:
            if s == e:
                labels.append(-100)
                prev_in = False
                continue
            inside = any(s < se and e > ss for ss, se in r["spans"])
            if not inside:
                labels.append(0)
                prev_in = False
                continue
            # B- when this piece starts a span, I- when it continues one.
            starts = any(ss >= s and ss < e for ss, _ in r["spans"]) or not prev_in
            labels.append(1 if starts else 2)
            prev_in = True
        enc.pop("offset_mapping")
        enc["labels"] = labels
        out.append(enc)
    return out


class Rows(torch.utils.data.Dataset):
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default="out/model")
    ap.add_argument("--epochs", type=float, default=3)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--lr", type=float, default=5e-5)
    a = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(BASE)
    model = AutoModelForTokenClassification.from_pretrained(
        BASE, num_labels=len(LABELS), id2label=dict(enumerate(LABELS)), label2id={l: i for i, l in enumerate(LABELS)}
    )
    train = Rows(encode(tok, load(os.path.join(a.data, "train.jsonl"))))
    dev_rows = load(os.path.join(a.data, "dev_heldout.jsonl"))
    dev = Rows(encode(tok, dev_rows))

    args = TrainingArguments(
        output_dir=a.out + "-ckpt",
        per_device_train_batch_size=a.batch,
        per_device_eval_batch_size=64,
        learning_rate=a.lr,
        num_train_epochs=a.epochs,
        warmup_ratio=0.06,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=100,
        fp16=torch.cuda.is_available(),
        report_to=[],
        seed=13,
    )
    trainer = Trainer(model=model, args=args, train_dataset=train, eval_dataset=dev,
                      data_collator=DataCollatorForTokenClassification(tok))
    trainer.train()
    os.makedirs(a.out, exist_ok=True)
    trainer.save_model(a.out)
    tok.save_pretrained(a.out)

    # Character-level scores on both dev sets, from the saved model.
    from .infer import TorchDetector

    det = TorchDetector(a.out)
    report = {}
    for name in ("dev_names", "dev_heldout"):
        rows = load(os.path.join(a.data, f"{name}.jsonl"))
        report[name] = score(rows, [det.spans(r["text"]) for r in rows])
    print(json.dumps(report, indent=2))
    with open(os.path.join(a.out, "dev_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    np.save(os.path.join(a.out, "labels.npy"), np.array(LABELS))


if __name__ == "__main__":
    main()
