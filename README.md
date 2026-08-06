# Streamwave BI

> 🚧 **Work in progress** — progetto di Business Intelligence sviluppato con approccio
> *spec-driven* ([GitHub Spec Kit](https://github.com/github/spec-kit)).
> Contesto di business, obiettivi e KPI vengono definiti in `.specify/memory/constitution.md`
> e nelle spec sotto `specs/`.

## Stato

| Fase | Artefatto | Stato |
|---|---|---|
| Constitution | `.specify/memory/constitution.md` | da definire |
| Specification | `specs/` | da definire |
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

Da definire.
