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
├── benchmarks/  # valori esterni congelati — versionata, al contrario delle altre
└── curated/     # assegnazioni dell'analista congelate — versionata, per la stessa ragione
```

Regola: nulla scrive mai dentro `raw/`.

## Perché `benchmarks/` e `curated/` sono versionate e le altre no

Sembra un'incoerenza e non lo è, ma la ragione va scritta o il prossimo lettore la prende per una svista.

Le altre cartelle non sono versionate **perché sono riproducibili**: `scripts/download_data.sh` ricostruisce `raw/`, la pipeline ricostruisce `processed/`. Chi clona il repository può rifarle, quindi versionarle significherebbe portarsi dietro peso senza guadagnare verificabilità.

`benchmarks/` e `curated/` sono versionate **perché non sono riproducibili**. La prima contiene valori osservati e pubblicati da terzi, raccolti a mano da una persona con un browser; la seconda contiene valori che nessuna fonte osserva e nessuna formula calcola, assegnati da una persona con l'assistenza di un modello linguistico invocato manualmente. In entrambi i casi nessuno script li rigenera, nessuno rieseguirà quel passaggio, e un valore perso è perso. È la stessa ragione per cui la constitution impone di congelare l'esito in un artefatto del repository — la condizione 3 dei benchmark, la condizione 2 delle assegnazioni dell'analista (emendamento v1.2.0).

La regola di `data/` non viene quindi violata: viene applicata al proprio criterio — *versiona ciò che non sai rifare* — invece che alla propria lettera.

**Perché `curated/` e non `benchmarks/` stessa.** Le due cartelle congelano fonti di natura diversa, e la constitution le tiene distinte con due comma separati e cinque condizioni ciascuno: un benchmark è un dato osservato su un operatore terzo e trasferito a StreamWave, un'assegnazione dell'analista non lo è — non esiste alcun operatore terzo, esiste un giudizio deciso e approvato da una persona contro un criterio che quella stessa persona ha scritto. Condividere la cartella avrebbe fatto sembrare le due cose un caso solo, con un'unica etichetta di fonte a coprirle; l'etichetta resta `Sintetico` per entrambe, ma la provenienza che la sostiene è diversa, e la separazione fisica la rende visibile a chi sfoglia `data/` senza aprire un solo file.

| File | Che cosa congela | Chi lo scrive |
|---|---|---|
| `benchmarks/bq3_tier_upgrade.json` | il tasso di adozione di un tier premium osservato su un operatore terzo, con citazione, scarto di misura e registro delle fonti respinte | una persona, a mano — **mai uno script** |
| `curated/dim_category_mood.json` *(feature `006`, in corso)* | il profilo di mood a tre assi per ciascuna delle 42 categorie del catalogo video, con numero di versione e registro di verifica indipendente rispetto alla proposta di un LLM | una persona, a mano — **mai uno script**; il modello propone, non scrive il file |
| `curated/dim_category_mood_proposal.json` *(feature `006`, in corso)* | la prima stesura del profilo, con prompt, nome del modello e data dell'unica invocazione manuale — input alla verifica, mai pubblicata come tabella finale | l'LLM, invocato a mano una sola volta |

Il metodo con cui il benchmark diventa tre scenari, e i suoi limiti, stanno in [`docs/bq3_scenarios.md`](../docs/bq3_scenarios.md). Il metodo con cui il profilo di mood viene assegnato e verificato, e i suoi limiti, staranno in `docs/content_taxonomy_bridge.md`.
