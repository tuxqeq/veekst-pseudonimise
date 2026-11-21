"""From a model's labels to character spans of names.

The same decoding runs in three places: here on the pod (PyTorch), on the
founder's Mac for the real test set (ONNX), and in veekst's classifier (ONNX).
The classifier's copy is `vekst_classifier/sprout/detect.py`; keep the two equal.

Decoding, in order:
  1. a word piece is a name when P(B-PER) + P(I-PER) >= threshold;
  2. a span grows to whole words: one piece of a word marked marks the word,
     because half a surname is still a surname;
  3. spans with only spaces between them join: "Иванов Иван" is one name.
Long texts are read in overlapping windows.
"""

from __future__ import annotations

import re

import numpy as np

MAX_LEN = 192
STRIDE = 48
THRESHOLD = 0.35
_WORD = re.compile(r"[^\s,;:()\"«»/|]+")


def decode(text: str, offsets: list[tuple[int, int]], probs: np.ndarray, threshold: float = THRESHOLD) -> list[list[int]]:
    marked = np.zeros(len(text), dtype=bool)
    for (s, e), p in zip(offsets, probs):
        if e > s and (p[1] + p[2]) >= threshold:
            marked[s:e] = True
    return _words(text, marked)


def _words(text: str, marked: np.ndarray) -> list[list[int]]:
    spans: list[list[int]] = []
    for m in _WORD.finditer(text):
        if marked[m.start():m.end()].any():
            s, e = m.start(), m.end()
            # A word's trailing comma or stop is not part of the name; an
            # initial's stop is.
            while e > s and text[e - 1] in ".-–" and not (e - s >= 2 and text[e - 2].isalpha() and (e - s == 2 or not text[e - 3].isalpha())):
                e -= 1
            if spans and text[spans[-1][1]:s].strip() == "":
                spans[-1][1] = e
            else:
                spans.append([s, e])
    return spans


def softmax(x: np.ndarray) -> np.ndarray:
    x = x - x.max(-1, keepdims=True)
    ex = np.exp(x)
    return ex / ex.sum(-1, keepdims=True)


def windows(tok, text: str):
    """(input_ids, attention_mask, offsets) per window of at most MAX_LEN pieces."""
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    ids, offs = enc["input_ids"], enc["offset_mapping"]
    cls, sep = tok.cls_token_id, tok.sep_token_id
    body = MAX_LEN - 2
    start = 0
    while True:
        chunk = ids[start:start + body]
        yield [cls] + chunk + [sep], [(0, 0)] + offs[start:start + body] + [(0, 0)]
        if start + body >= len(ids):
            break
        start += body - STRIDE


class TorchDetector:
    def __init__(self, path: str, threshold: float = THRESHOLD):
        import torch
        from transformers import AutoModelForTokenClassification, AutoTokenizer

        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForTokenClassification.from_pretrained(path).eval()
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        self.threshold = threshold

    def spans(self, text: str) -> list[list[int]]:
        torch = self.torch
        marked = np.zeros(len(text), dtype=bool)
        for ids, offs in windows(self.tok, text):
            with torch.no_grad():
                t = torch.tensor([ids], device=self.model.device)
                logits = self.model(input_ids=t).logits[0].float().cpu().numpy()
            probs = softmax(logits)
            for (s, e), p in zip(offs, probs):
                if e > s and (p[1] + p[2]) >= self.threshold:
                    marked[s:e] = True
        return _words(text, marked)


class OnnxDetector:
    def __init__(self, model_path: str, tokenizer_path: str, threshold: float = THRESHOLD):
        import onnxruntime as ort
        from tokenizers import Tokenizer

        self.sess = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.tk = Tokenizer.from_file(tokenizer_path)
        self.tk.no_padding()
        self.tk.no_truncation()
        self.cls = self.tk.token_to_id("[CLS]")
        self.sep = self.tk.token_to_id("[SEP]")
        self.threshold = threshold

    def spans(self, text: str) -> list[list[int]]:
        enc = self.tk.encode(text, add_special_tokens=False)
        ids, offs = enc.ids, enc.offsets
        marked = np.zeros(len(text), dtype=bool)
        body = MAX_LEN - 2
        start = 0
        while True:
            chunk = [self.cls] + ids[start:start + body] + [self.sep]
            o = [(0, 0)] + offs[start:start + body] + [(0, 0)]
            arr = np.array([chunk], dtype=np.int64)
            logits = self.sess.run(None, {"input_ids": arr, "attention_mask": np.ones_like(arr)})[0][0]
            probs = softmax(logits)
            for (s, e), p in zip(o, probs):
                if e > s and (p[1] + p[2]) >= self.threshold:
                    marked[s:e] = True
            if start + body >= len(ids):
                break
            start += body - STRIDE
        return _words(text, marked)
