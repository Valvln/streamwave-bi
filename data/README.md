# Dati

I dataset raw **non sono versionati** (vedi [`.gitignore`](../.gitignore)): pesano ~22 MB e sono riproducibili da fonte pubblica. Per ricostruire `data/raw/`:

```bash
./scripts/download_data.sh
```

## Fonti

| File | Fonte | Righe | Licenza |
|---|---|---|---|
| `raw/spotify_tracks_dataset.csv` | [Kaggle · maharshipandya/-spotify-tracks-dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) (DOI `10.34740/kaggle/dsv/4372070`) | ~114k tracce, 125 generi | ODbL 1.0 (database), © autori originali (contenuti) |
| `raw/netflix_titles.csv` | [Kaggle · shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) | ~8.8k titoli (catalogo al 2021) | CC0 1.0 Public Domain |

Il file `raw/-spotify-tracks-dataset-metadata.json` (metadati Croissant, 12 KB) **è** versionato come traccia di provenienza.

## Layout

```
data/
├── raw/         # immutabile, sola lettura — output del download
├── interim/     # trasformazioni intermedie
├── processed/   # dataset analitici finali, pronti per il modello dati
└── benchmarks/  # valori esterni congelati — versionata, al contrario delle altre
```

Regola: nulla scrive mai dentro `raw/`.

## Perché `benchmarks/` è versionata e le altre no

Sembra un'incoerenza e non lo è, ma la ragione va scritta o il prossimo lettore la prende per una svista.

Le altre cartelle non sono versionate **perché sono riproducibili**: `scripts/download_data.sh` ricostruisce `raw/`, la pipeline ricostruisce `processed/`. Chi clona il repository può rifarle, quindi versionarle significherebbe portarsi dietro peso senza guadagnare verificabilità.

`benchmarks/` è versionata **perché non è riproducibile**. Contiene valori osservati e pubblicati da terzi, raccolti a mano da una persona con un browser: nessuno script li rigenera, nessuno rieseguirà quella ricerca, e un valore perso è perso. È precisamente la ragione per cui la constitution, che ammette i benchmark pubblici di settore come fonte, impone di congelarne l'esito in un artefatto del repository insieme alla sua citazione.

La regola di `data/` non viene quindi violata: viene applicata al proprio criterio — *versiona ciò che non sai rifare* — invece che alla propria lettera.

| File | Che cosa congela | Chi lo scrive |
|---|---|---|
| `benchmarks/bq3_tier_upgrade.json` | il tasso di adozione di un tier premium osservato su un operatore terzo, con citazione, scarto di misura e registro delle fonti respinte | una persona, a mano — **mai uno script** |

Il metodo con cui quel valore diventa tre scenari, e i suoi limiti, stanno in [`docs/bq3_scenarios.md`](../docs/bq3_scenarios.md).
