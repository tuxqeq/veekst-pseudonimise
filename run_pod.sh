#!/usr/bin/env bash
# The whole run on a Runpod GPU pod: generate, train, export, publish.
#
#   GITHUB_TOKEN  a fine-grained token with Contents: read and write on this
#                 repository only. With it, the run publishes detector.onnx,
#                 tokenizer.json and manifest.json as a release. Without it,
#                 the files stay in /workspace/out/onnx.
set -euo pipefail
cd /workspace
if [ ! -d veekst-pseudonimise ]; then
  git clone --depth 1 https://github.com/tuxqeq/veekst-pseudonimise
fi
cd veekst-pseudonimise
git pull --ff-only || true
pip install -q -r requirements.txt

# A restart (to add the token) keeps /workspace: train only once.
if [ ! -f out/onnx/manifest.json ] || [ -n "${RETRAIN:-}" ]; then
  python -m vpseud.generate --out data --train "${TRAIN_ROWS:-120000}" --dev 4000
  python -m vpseud.train --data data --out out/model --epochs "${EPOCHS:-3}"
  python -m vpseud.export --model out/model --data data --out out/onnx
fi

if [ -n "${GITHUB_TOKEN:-}" ]; then
  TAG="${RELEASE_TAG:-detector-v1}"
  API=https://api.github.com/repos/tuxqeq/veekst-pseudonimise
  AUTH="Authorization: Bearer ${GITHUB_TOKEN}"
  id=$(curl -fsS -H "$AUTH" "$API/releases/tags/$TAG" 2>/dev/null | python -c 'import sys,json;print(json.load(sys.stdin)["id"])' || true)
  if [ -z "$id" ]; then
    id=$(curl -fsS -H "$AUTH" -X POST "$API/releases" \
      -d "{\"tag_name\":\"$TAG\",\"name\":\"$TAG\",\"body\":\"Name detector, trained on generated text only. See manifest.json.\"}" \
      | python -c 'import sys,json;print(json.load(sys.stdin)["id"])')
  fi
  for f in detector.onnx tokenizer.json manifest.json; do
    curl -fsS -H "$AUTH" -H "Content-Type: application/octet-stream" \
      --data-binary @"out/onnx/$f" \
      "https://uploads.github.com/repos/tuxqeq/veekst-pseudonimise/releases/$id/assets?name=$f" >/dev/null
    echo "published $f"
  done
fi
echo DONE
