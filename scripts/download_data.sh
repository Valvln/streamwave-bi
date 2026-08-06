#!/usr/bin/env bash
# Scarica i dataset raw del progetto Streamwave BI.
#
# Prerequisiti:
#   1. pip install kaggle   (oppure: uv tool install kaggle)
#   2. Token API Kaggle in ~/.kaggle/kaggle.json
#      (Kaggle > Settings > API > "Create New Token"), poi chmod 600 ~/.kaggle/kaggle.json
#
# Uso:  ./scripts/download_data.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW_DIR="$REPO_ROOT/data/raw"

if ! command -v kaggle >/dev/null 2>&1; then
  echo "ERRORE: CLI 'kaggle' non trovata. Installala con:  uv tool install kaggle" >&2
  exit 1
fi

mkdir -p "$RAW_DIR"

download() {
  local slug="$1" expected_file="$2"
  if [[ -f "$RAW_DIR/$expected_file" ]]; then
    echo "SKIP  $expected_file (già presente)"
    return
  fi
  echo "GET   $slug -> data/raw/$expected_file"
  kaggle datasets download -d "$slug" -p "$RAW_DIR" --unzip
}

# Spotify Tracks Dataset — 114k tracce, 125 generi, audio features
# https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
# Licenza: ODbL 1.0 (database) / © autori originali (contenuti)
download "maharshipandya/-spotify-tracks-dataset" "spotify_tracks_dataset.csv"

# Netflix Movies and TV Shows — catalogo titoli al 2021
# https://www.kaggle.com/datasets/shivamb/netflix-shows
# Licenza: CC0 1.0 Public Domain
download "shivamb/netflix-shows" "netflix_titles.csv"

# Il file Spotify viene scaricato come dataset.csv: normalizziamo il nome.
if [[ -f "$RAW_DIR/dataset.csv" && ! -f "$RAW_DIR/spotify_tracks_dataset.csv" ]]; then
  mv "$RAW_DIR/dataset.csv" "$RAW_DIR/spotify_tracks_dataset.csv"
  echo "RENAME dataset.csv -> spotify_tracks_dataset.csv"
fi

echo
echo "Fatto. Contenuto di data/raw:"
ls -lh "$RAW_DIR"
