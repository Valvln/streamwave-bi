# Dati

I dataset raw **non sono versionati** (vedi [`.gitignore`](../.gitignore)): pesano ~22 MB e
sono riproducibili da fonte pubblica. Per ricostruire `data/raw/`:

```bash
./scripts/download_data.sh
```

## Fonti

| File | Fonte | Righe | Licenza |
|---|---|---|---|
| `raw/spotify_tracks_dataset.csv` | [Kaggle · maharshipandya/-spotify-tracks-dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) (DOI `10.34740/kaggle/dsv/4372070`) | ~114k tracce, 125 generi | ODbL 1.0 (database), © autori originali (contenuti) |
| `raw/netflix_titles.csv` | [Kaggle · shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) | ~8.8k titoli (catalogo al 2021) | CC0 1.0 Public Domain |

Il file `raw/-spotify-tracks-dataset-metadata.json` (metadati Croissant, 12 KB) **è** versionato
come traccia di provenienza.

## Layout

```
data/
├── raw/         # immutabile, sola lettura — output del download
├── interim/     # trasformazioni intermedie
└── processed/   # dataset analitici finali, pronti per il modello dati
```

Regola: nulla scrive mai dentro `raw/`.
