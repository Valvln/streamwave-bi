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

## Stato

| Fase | Artefatto | Stato |
|---|---|---|
| Constitution | [`.specify/memory/constitution.md`](.specify/memory/constitution.md) | ✅ v1.0.0 |
| Specification | `specs/` | prossimo passo |
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
