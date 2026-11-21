"""The thesis's measures, on character spans.

value recall    a gold name counts as caught only when every letter of it is
                covered: one letter left is a name that left.
leaked chars    the share of gold letters no prediction covers.
char precision  the share of predicted letters inside a gold name.
false spans     predicted spans that touch no gold name, per 100 texts.
"""

from __future__ import annotations


def _letters(text: str, s: int, e: int) -> set[int]:
    return {i for i in range(s, e) if text[i].isalpha()}


def score(rows: list[dict], preds: list[list[list[int]]]) -> dict:
    gold_n = caught = 0
    gold_chars = leaked = 0
    pred_chars = pred_inside = 0
    false_spans = 0
    for r, p in zip(rows, preds):
        text = r["text"]
        covered: set[int] = set()
        for s, e in p:
            covered |= _letters(text, s, e)
        gold_all: set[int] = set()
        for s, e in r["spans"]:
            g = _letters(text, s, e)
            if not g:
                continue
            gold_all |= g
            gold_n += 1
            caught += g <= covered
            gold_chars += len(g)
            leaked += len(g - covered)
        pred_chars += len(covered)
        pred_inside += len(covered & gold_all)
        for s, e in p:
            if not (_letters(text, s, e) & gold_all):
                false_spans += 1
    return {
        "names": gold_n,
        "value_recall": round(caught / gold_n, 4) if gold_n else None,
        "leaked_chars": round(leaked / gold_chars, 4) if gold_chars else None,
        "char_precision": round(pred_inside / pred_chars, 4) if pred_chars else None,
        "false_spans_per_100": round(100 * false_spans / max(1, len(rows)), 2),
        "texts": len(rows),
    }
