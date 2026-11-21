"""Generated, labelled texts for the name detector.

Each record is {"text", "spans", "kind", "lang"}: `spans` are [start, end)
character offsets of a private person's name. Nothing here reads a customer's
data; every text is a hand-written template with invented values.

    python -m vpseud.generate --out data --train 60000 --dev 4000
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re

from . import names, templates as T

SLOT = re.compile(r"\{([A-Z]+)(?::([a-z]+))?\}")


def _number(rnd: random.Random) -> str:
    shapes = [
        lambda: str(rnd.randint(1, 999)),
        lambda: str(rnd.randint(1000, 99999999)),
        lambda: f"{rnd.randint(1, 99)}/{rnd.randint(1, 999)}",
        lambda: f"{rnd.randint(10, 99)}-{rnd.choice(['А', 'Б', 'USD', 'CL'])}{rnd.randint(1, 99)}",
        lambda: f"TR{rnd.randint(100000000, 999999999)}",
    ]
    return rnd.choice(shapes)()


def _date(rnd: random.Random) -> str:
    d, m, y = rnd.randint(1, 28), rnd.randint(1, 12), rnd.choice([2022, 2023, 2024, 2025, 2026])
    return rnd.choice([f"{d:02d}.{m:02d}.{y}", f"{d:02d}.{m:02d}.{y % 100:02d}", f"{y}-{m:02d}-{d:02d}", f"{d:02d}/{m:02d}/{y}"])


def _amount(rnd: random.Random) -> str:
    whole = rnd.randint(1, 9_999_999)
    cents = rnd.randint(0, 99)
    return rnd.choice([f"{whole},{cents:02d}", f"{whole}.{cents:02d}", f"{whole:,}".replace(",", " ") + f"-{cents:02d}", str(whole)])


class Filler:
    def __init__(self, rnd: random.Random, pools: names.Pools):
        self.rnd, self.pools = rnd, pools

    def fill(self, style: str, lang: str, template: str) -> tuple[str, list[list[int]]]:
        rnd = self.rnd
        upper_text = style == "up"
        out: list[str] = []
        spans: list[list[int]] = []
        pos = 0
        last = 0
        for m in SLOT.finditer(template):
            lit = template[last:m.start()]
            out.append(lit)
            pos += len(lit)
            last = m.end()
            kind, case = m.group(1), m.group(2) or "nom"
            value, is_person = self._value(kind, case, style)
            if upper_text and not is_person:
                value = value.upper()
            out.append(value)
            if is_person:
                spans.append([pos, pos + len(value)])
            pos += len(value)
        out.append(template[last:])
        text = "".join(out)
        if upper_text:
            # Names are already in the case render() chose; the rest is upper.
            text = _upper_except(text, spans)
        return text, spans

    def _value(self, kind: str, case: str, style: str) -> tuple[str, bool]:
        rnd, pools = self.rnd, self.pools
        if kind == "P":
            p = names.person(rnd, pools, "ru")
            if rnd.random() < 0.08:
                return names.render_latin(p, rnd), True
            upper = True if style == "up" else (rnd.random() < 0.2)
            text = names.render(p, case, rnd, upper=upper)
            if style == "q" and rnd.random() < 0.35:
                text = text.lower()
            return text, True
        if kind == "PL":
            p = names.person(rnd, pools, "pl")
            upper = True if style == "up" else (rnd.random() < 0.15)
            text = names.render(p, case, rnd, upper=upper)
            if style == "q" and rnd.random() < 0.3:
                text = text.lower()
            return text, True
        if kind == "PLAT":
            p = names.person(rnd, pools, "ru")
            text = names.render_latin(p, rnd)
            if style == "up":
                text = text.upper()
            elif style == "q" and rnd.random() < 0.3:
                text = text.lower()
            return text, True
        if kind == "PSUR":
            p = names.person(rnd, pools, "ru")
            text = names.translit(p.surname_in("nom"))
            return (text.upper() if rnd.random() < 0.5 else text), True
        table = {
            "ORG": lambda: rnd.choice(T.ORGS).strip(),
            "BANK": lambda: rnd.choice(T.BANKS),
            "N": lambda: _number(rnd),
            "D": lambda: _date(rnd),
            "AMT": lambda: _amount(rnd),
            "Y": lambda: str(rnd.choice([2022, 2023, 2024, 2025, 2026])),
            "MON": lambda: rnd.choice(T.MONTHS),
            "MONG": lambda: rnd.choice(T.MONTHS_GEN),
            "MONP": lambda: rnd.choice(T.MONTHS_PRE),
            "MEN": lambda: rnd.choice(T.MONTHS_EN),
            "MPL": lambda: rnd.choice(T.MONTHS_PL),
            "SERV": lambda: rnd.choice(T.SERVICES),
            "CITY": lambda: rnd.choice(T.CITIES),
            "STREET": lambda: rnd.choice(T.STREETS).replace("{N}", str(rnd.randint(1, 120))),
            "CUR": lambda: rnd.choice(T.CURRENCIES),
            "WORDS": lambda: " ".join(rnd.sample(T.WORDS, rnd.randint(2, 7))),
            "EWORDS": lambda: " ".join(rnd.sample(T.EWORDS, rnd.randint(2, 7))),
        }
        return table[kind](), False


def _upper_except(text: str, spans: list[list[int]]) -> str:
    out, last = [], 0
    for s, e in spans:
        out.append(text[last:s].upper())
        out.append(text[s:e])
        last = e
    out.append(text[last:].upper())
    return "".join(out)


def _noise(rnd: random.Random, text: str, spans: list[list[int]]) -> tuple[str, list[list[int]]]:
    """What a bank's export does to a text: cuts it, joins words to numbers."""
    if rnd.random() < 0.15 and len(text) > 60:
        cut = rnd.randint(40, len(text))
        text = text[:cut]
        spans = [[s, min(e, cut)] for s, e in spans if s < cut]
        spans = [sp for sp in spans if sp[1] - sp[0] >= 2]
    if rnd.random() < 0.1:
        text = text.replace("ДО ", "ДО", 1)
    return text, spans


def _shift(spans: list[list[int]], by: int) -> list[list[int]]:
    return [[s + by, e + by] for s, e in spans]


def records(n: int, seed: int, pools: names.Pools, groups: dict[str, list]) -> list[dict]:
    rnd = random.Random(seed)
    f = Filler(rnd, pools)
    out = []
    for _ in range(n):
        r = rnd.random()
        if r < 0.42:
            style, lang, t = rnd.choice(groups["pos"])
            kind = "purpose"
        elif r < 0.80:
            style, lang, t = rnd.choice(groups["neg"])
            kind = "purpose"
        elif r < 0.92:
            style, lang, t = rnd.choice(groups["q"])
            kind = "question"
        else:
            style, lang, t = rnd.choice(groups["qneg"])
            kind = "question"
        text, spans = f.fill(style, lang, t)
        if kind == "purpose" and rnd.random() < 0.25:
            # A second sentence, the way a bank appends its own note.
            s2, l2, t2 = rnd.choice(groups["neg"])
            extra, _ = f.fill(style if style != "q" else "mix", l2, t2)
            sep = rnd.choice([". ", " ", ".."])
            if rnd.random() < 0.5:
                text = text + sep + extra
            else:
                lead = extra + sep
                text, spans = lead + text, _shift(spans, len(lead))
        if kind == "purpose":
            text, spans = _noise(rnd, text, spans)
        out.append({"text": text, "spans": spans, "kind": kind, "lang": lang})
    return out


def split_templates(seed: int = 11, held_out: float = 0.2) -> tuple[dict, dict]:
    rnd = random.Random(seed)

    def cut(xs):
        xs = list(xs)
        rnd.shuffle(xs)
        k = max(1, int(len(xs) * held_out))
        return xs[k:], xs[:k]

    parts = {k: cut(v) for k, v in (("pos", T.PURPOSES), ("neg", T.NEGATIVES), ("q", T.QUESTIONS), ("qneg", T.QUESTION_NEGATIVES))}
    return {k: v[0] for k, v in parts.items()}, {k: v[1] for k, v in parts.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data")
    ap.add_argument("--train", type=int, default=60000)
    ap.add_argument("--dev", type=int, default=4000)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    train_pools, held_pools = names.split()
    train_t, held_t = split_templates()
    sets = {
        "train": records(a.train, 1, train_pools, train_t),
        # Seen templates, unseen names: does it learn names, not a list?
        "dev_names": records(a.dev, 2, held_pools, train_t),
        # Unseen templates and unseen names: the honest number.
        "dev_heldout": records(a.dev, 3, held_pools, held_t),
    }
    for name, rows in sets.items():
        with open(os.path.join(a.out, f"{name}.jsonl"), "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(name, len(rows), sum(bool(r["spans"]) for r in rows), "with a name")


if __name__ == "__main__":
    main()
