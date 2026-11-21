# veekst-pseudonimise

The name detector behind veekst's sprout: it finds private people's names in
payment purposes and in the questions a person types, so that core can send
each name to a model as a token (`[PER_…]`) and never as the name.

It follows the thesis project [tux.ai](https://github.com/tuxqeq/tux.ai): a
DistilBERT token classifier, held-out templates, and the same measures
(value recall, leaked characters). It differs in three ways:

| | tux.ai | here |
| --- | --- | --- |
| Base | `distilbert-base-uncased`, English | `distilbert-base-multilingual-cased` |
| Text | English documents, US formats | Russian, Belarusian, Kazakh and Polish payment purposes, and questions |
| Labels | 40 PII types | `PER` only: firms are tokens by their column, and digits never leave |

## What is in this repository

Code, hand-written name lists and hand-written templates. **No customer data.**
Every training text is generated (`vpseud/generate.py`). The real test set —
statements the founder agreed to use — stays on his machine and is never
committed here or sent to the training pod.

## Run

```sh
pip install -r requirements.txt
python -m vpseud.generate --out data
python -m vpseud.train --data data --out out/model
python -m vpseud.export --model out/model --data data --out out/onnx
```

`run_pod.sh` does all three on a Runpod GPU pod and, with `GITHUB_TOKEN`,
publishes `detector.onnx`, `tokenizer.json` and `manifest.json` as a release.

## Measures

- **value recall**: a name counts as caught only when every letter is covered.
- **leaked chars**: the share of name letters no span covers.
- **char precision**, **false spans per 100 texts**.

`dev_names` has seen templates and unseen names; `dev_heldout` has unseen
templates and unseen names. The number veekst is gated on (95 % value recall)
is measured on the real test set, not here.
