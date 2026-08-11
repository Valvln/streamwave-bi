# Streamwave BI

> 🚧 **Work in progress** — progetto di Business Intelligence sviluppato con approccio *spec-driven* ([GitHub Spec Kit](https://github.com/github/spec-kit)).

**StreamWave**, piattaforma di streaming video, valuta l'ingresso nel verticale del **music streaming**. Questo repository contiene l'analisi e la dashboard a supporto della decisione.

Tre domande di business guidano l'intero progetto:

- **BQ1 — Posizionamento**: come si posiziona il contenuto musicale rispetto a quello video per caratteristiche "vincenti" (durata, genere, mood)? C'è overlap di audience potenziale?
- **BQ2 — Segmento di ingresso**: quale segmento musicale è più coerente con il catalogo attuale?
- **BQ3 — Impatto stimato**: quale impatto su engagement e revenue, simulato con assunzioni dichiarate?

I principi non negoziabili del progetto — etichettatura di fonte e confidenza su ogni numero, riproducibilità totale, trasparenza sui limiti — sono in [`.specify/memory/constitution.md`](.specify/memory/constitution.md). Il metodo di lavoro che ne discende, incluso il modo in cui il lavoro è diviso fra sessioni di agent, è in [`CLAUDE.md`](CLAUDE.md); il piano e il suo scostamento in [`docs/roadmap.md`](docs/roadmap.md).

## Cosa questo progetto non è

È un **case study**: un esercizio di analisi costruito per essere verificabile, non un prodotto pronto a supportare una decisione di mercato reale. Nello specifico:

- **StreamWave non esiste.** È un'azienda inventata. Nessun dato reale di StreamWave è stato usato, perché non ce n'è.
- **Netflix e Spotify sono proxy, non StreamWave.** Il catalogo Netflix rappresenta il catalogo ipotetico di StreamWave, il dataset Spotify rappresenta il mercato musicale accessibile. È l'assunzione strutturale del case study: regge il ragionamento, non la realtà di un'azienda.
- **Le metriche di business sono sintetiche.** Nessun dato di visione, ascolto, abbonamento o ricavo reale esiste in questi dataset. Tutto ciò che riguarda engagement e revenue è generato da script con assunzioni dichiarate, ed è etichettato come tale in ogni artefatto.
- **Manca il lato costi.** Licenze musicali, infrastruttura, organico: nessuno di questi dati è disponibile. Quello che segue è un business case *di opportunità*, non un business case finanziario. Chi cercasse qui un ROI non lo troverà, ed è deliberato.
- **I dati reali si fermano al 2021-2022.** Il catalogo Netflix è aggiornato al 2021, le tracce Spotify al 2022. Nessuna conclusione di questo progetto può dire alcunché sulle dinamiche di mercato successive.

I limiti analitici specifici di ogni singola analisi — cosa quel particolare KPI non risponde, quali inferenze evitare — vivono nella sezione *Limiti Dichiarati* della spec di ciascuna feature sotto [`specs/`](specs/), come richiesto dal principio IV della constitution. Questa sezione inquadra il progetto; quelle inquadrano i singoli risultati.

## Stato

Governance: [`constitution`](.specify/memory/constitution.md) v1.0.2 · [metodo di lavoro](CLAUDE.md) · [roadmap e stime](docs/roadmap.md)

| Feature | Deliverable | Stato |
|---|---|---|
| `001` Business Case & KPI Framework | [`docs/business_case.md`](docs/business_case.md) | ✅ conclusa, [revisionata](specs/001-business-case-kpi/review.md) |
| `002` Data Audit & Profiling | [`docs/data_audit.md`](docs/data_audit.md) · [`reports/data_profile.json`](reports/data_profile.json) | ✅ conclusa, [revisionata](specs/002-data-audit-profiling/review.md) |
| `003` Data Cleaning & ETL | `scripts/build_datasets.py` · `reports/cleaning_report.json` | 🔄 in corso |

Le feature successive, le stime e il debito aperto sono in [`docs/roadmap.md`](docs/roadmap.md).

## Il business case

Il primo deliverable è **[`docs/business_case.md`](docs/business_case.md)**: il framework con cui il progetto risponderà alle tre domande. Definisce 8 KPI con formula concettuale, fonte e livello di confidenza, una North Star metric e il perimetro di ciò che l'analisi non proverà a dimostrare. Non contiene risultati: quelli arriveranno dalle feature successive, ciascuno con l'etichetta di affidabilità definita qui.

Il secondo è **[`docs/data_audit.md`](docs/data_audit.md)**: il profilo dei due dataset reali, con ciò che la loro forma vincola per le feature successive. Ogni numero che contiene è rigenerato da uno script e vive in [`reports/data_profile.json`](reports/data_profile.json), versionato perché sia verificabile anche da chi non ha i dati di origine.

## Setup

```bash
# 1. Dati raw (non versionati — vedi data/README.md)
./scripts/download_data.sh

# 2. Profilo dei dataset (richiede i dati raw del passo 1)
python3 scripts/profile_data.py

# 3. Coerenza fra il documento di audit e il profilo (NON richiede i dati raw)
python3 scripts/check_audit_coherence.py
```

Nessuna dipendenza da installare: gli script usano la sola libreria standard di Python 3. Il passo 3 funziona su una copia del repository priva di `data/raw/`, perché confronta due artefatti entrambi versionati.

## Struttura

```
.specify/       # Spec Kit: constitution, template, script
.claude/        # comandi /speckit.* per Claude Code
.github/        # prompt /speckit.* per GitHub Copilot
data/           # raw / interim / processed (gitignored)
reports/        # artefatti generati e versionati (profilo dei dati)
scripts/        # utility riproducibili
specs/          # una cartella per feature: spec.md, plan.md, tasks.md
```

## Dati

Due dataset pubblici Kaggle (Spotify tracks + catalogo Netflix). Provenienza e licenze: [`data/README.md`](data/README.md).

## Licenza

[MIT](LICENSE) — codice e documentazione. I dataset raw restano soggetti alle rispettive licenze d'origine (vedi [`data/README.md`](data/README.md)).
