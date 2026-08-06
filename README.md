# Streamwave BI

> 🚧 **Work in progress** — progetto di Business Intelligence sviluppato con approccio
> *spec-driven* ([GitHub Spec Kit](https://github.com/github/spec-kit)).

**StreamWave**, piattaforma di streaming video, valuta l'ingresso nel verticale del **music
streaming**. Questo repository contiene l'analisi e la dashboard a supporto della decisione.

Tre domande di business guidano l'intero progetto:

- **BQ1 — Posizionamento**: come si posiziona il contenuto musicale rispetto a quello video per
  caratteristiche "vincenti" (durata, genere, mood)? C'è overlap di audience potenziale?
- **BQ2 — Segmento di ingresso**: quale segmento musicale è più coerente con il catalogo attuale?
- **BQ3 — Impatto stimato**: quale impatto su engagement e revenue, simulato con assunzioni dichiarate?

I principi non negoziabili del progetto — etichettatura di fonte e confidenza su ogni numero,
riproducibilità totale, trasparenza sui limiti — sono in
[`.specify/memory/constitution.md`](.specify/memory/constitution.md).

## Cosa questo progetto non è

È un **case study**: un esercizio di analisi costruito per essere verificabile, non un prodotto
pronto a supportare una decisione di mercato reale. Nello specifico:

- **StreamWave non esiste.** È un'azienda inventata. Nessun dato reale di StreamWave è stato usato,
  perché non ce n'è.
- **Netflix e Spotify sono proxy, non StreamWave.** Il catalogo Netflix rappresenta il catalogo
  ipotetico di StreamWave, il dataset Spotify rappresenta il mercato musicale accessibile. È
  l'assunzione strutturale del case study: regge il ragionamento, non la realtà di un'azienda.
- **Le metriche di business sono sintetiche.** Nessun dato di visione, ascolto, abbonamento o
  ricavo reale esiste in questi dataset. Tutto ciò che riguarda engagement e revenue è generato da
  script con assunzioni dichiarate, ed è etichettato come tale in ogni artefatto.
- **Manca il lato costi.** Licenze musicali, infrastruttura, organico: nessuno di questi dati è
  disponibile. Quello che segue è un business case *di opportunità*, non un business case
  finanziario. Chi cercasse qui un ROI non lo troverà, ed è deliberato.
- **I dati reali si fermano al 2021-2022.** Il catalogo Netflix è aggiornato al 2021, le tracce
  Spotify al 2022. Nessuna conclusione di questo progetto può dire alcunché sulle dinamiche di
  mercato successive.

I limiti analitici specifici di ogni singola analisi — cosa quel particolare KPI non risponde,
quali inferenze evitare — vivono nella sezione *Limiti Dichiarati* della spec di ciascuna feature
sotto [`specs/`](specs/), come richiesto dal principio IV della constitution. Questa sezione
inquadra il progetto; quelle inquadrano i singoli risultati.

## Stato

| Fase | Artefatto | Stato |
|---|---|---|
| Constitution | [`.specify/memory/constitution.md`](.specify/memory/constitution.md) | ✅ v1.0.1 |
| Specification | [`specs/001-business-case-kpi/`](specs/001-business-case-kpi/) | ✅ feature 001 |
| Plan | `specs/*/plan.md` | — |
| Tasks | `specs/*/tasks.md` | — |
| Implementation | — | — |

## Setup

```bash
# 1. Dati raw (non versionati — vedi data/README.md)
./scripts/download_data.sh
```

## Struttura

```
.specify/       # Spec Kit: constitution, template, script
.claude/        # comandi /speckit.* per Claude Code
.github/        # prompt /speckit.* per GitHub Copilot
data/           # raw / interim / processed (gitignored)
scripts/        # utility riproducibili
specs/          # una cartella per feature: spec.md, plan.md, tasks.md
```

## Dati

Due dataset pubblici Kaggle (Spotify tracks + catalogo Netflix). Provenienza e licenze:
[`data/README.md`](data/README.md).

## Licenza

[MIT](LICENSE) — codice e documentazione. I dataset raw restano soggetti alle rispettive
licenze d'origine (vedi [`data/README.md`](data/README.md)).
