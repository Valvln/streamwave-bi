# Implementation Plan: Business Case e Framework KPI

**Branch**: `001-business-case-kpi` | **Date**: 2026-08-07 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-business-case-kpi/spec.md`

## Summary

La feature produce un solo artefatto: `docs/business_case.md`, il documento che traduce le tre domande di business in un framework di 6-9 KPI definiti concettualmente, con una North Star metric di coerenza strategica e un perimetro esplicito. Non produce codice, non calcola numeri di risultato.

L'approccio emerso dalla ricerca di Fase 0: prima di definire i KPI si è verificato cosa i due dataset reali contengono davvero, perché quattro caratteristiche dei dati escludono altrettante misure che sarebbero sembrate ovvie sulla carta — il campione Spotify è bilanciato per costruzione, un quinto delle righe sono tracce ripetute, le durate dei due domini non sono confrontabili e i generi non si agganciano per nome. Il framework è costruito su ciò che resta misurabile, e ciò che non lo è finisce nella sezione dei limiti invece di sparire.

## Technical Context

Il template di questa sezione presuppone una feature software. Questa produce un documento: i campi non applicabili sono marcati come tali invece di essere riempiti con valori fittizi.

**Linguaggio/Versione**: N/A — nessun codice prodotto da questa feature (spec, Assumptions: "questa feature non produce codice")

**Dipendenze primarie**: N/A. La ricerca di Fase 0 ha letto i CSV in `data/raw/` con la sola libreria standard Python, in sola lettura, senza produrre artefatti persistenti

**Storage**: file Markdown versionato in `docs/`

**Testing**: verifica per lettura secondo [quickstart.md](./quickstart.md) — controlli strutturali eseguibili da riga di comando più una sessione di revisione in contesto pulito (FR-019)

**Piattaforma target**: qualunque lettore Markdown; il documento è letto su GitHub e in locale

**Tipo di progetto**: documentazione analitica (fase di definizione di un progetto di BI)

**Obiettivi di performance**: N/A

**Vincoli**: lettura completa in 15 minuti (SC-001); una giornata lavorativa di realizzazione (principio III); nessun numero di risultato nel documento (FR-016); nessuna sintassi DAX/SQL/Python nelle formule (FR-007)

**Scala/Ambito**: 3 domande di business, 6-9 KPI, 1 North Star, ≥5 voci fuori scope

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni KPI del framework dichiara fonte e confidenza; i livelli hanno criteri oggettivi | ✅ imposto da FR-009/FR-010 | ✅ criteri operativi fissati in [research.md](./research.md) D5 |
| **II. Riproducibilità** | nessuna trasformazione manuale sui dati; `data/raw/` intatto | ✅ nessuna trasformazione prevista | ✅ la ricerca ha solo letto i file; nessuna scrittura in `data/` |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ tre strati incrementali (US1/US2/US3) | ✅ la scomposizione regge: US1 è già consegnabile da solo |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde | ✅ sezione "Limiti Dichiarati" compilata | ✅ i ritrovamenti R1-R5 aggiungono limiti reali da riportare nel documento |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessuna GUI coinvolta | ✅ invariato |
| **VI. Coerenza Narrativa** | riconducibile alle domande di business | ✅ feature fondativa: serve tutte e tre | ✅ ogni decisione di Fase 0 è agganciata a BQ1, BQ2 o BQ3 |

**Esito**: nessuna violazione, prima e dopo il design. La tabella "Complexity Tracking" resta vuota.

Un punto di attenzione, non una violazione: la ricerca ha prodotto informazioni che rendono **più severo** un criterio di attribuzione già presente nella spec (vedi la nota di impatto in fondo a [research.md](./research.md)). La spec è approvata, quindi la modifica è proposta e non applicata.

## Project Structure

### Documentation (this feature)

```text
specs/001-business-case-kpi/
├── spec.md              # specifica approvata (con Clarifications)
├── plan.md              # questo file
├── research.md          # Fase 0: inventario dati, ritrovamenti R1-R5, decisioni D1-D6
├── data-model.md        # Fase 1: entità del framework e loro vincoli
├── quickstart.md        # Fase 1: come verificare che il documento sia conforme
├── checklists/
│   └── requirements.md  # checklist di qualità della spec (20/20)
├── review.md            # verbale di revisione (FR-019) — prodotto in fase di implementazione
└── tasks.md             # output di /speckit.tasks — non creato qui
```

Nessuna cartella `contracts/`: vedi decisione D6 in [research.md](./research.md).

### Artefatti nel repository

```text
docs/
└── business_case.md     # l'unico deliverable della feature
```

**Structure Decision**: nessuna struttura di codice sorgente. La feature aggiunge un solo file al repository, in `docs/`, già presente come cartella vuota. Le cartelle `src/` e `tests/` non vengono create: introdurle ora, vuote, anticiperebbe scelte di stack che la constitution demanda esplicitamente alle feature successive.

## Fase 0 — Outline & Research

**Completata**. Output: [research.md](./research.md).

Cinque ritrovamenti sui dati reali (R1-R5) e sei decisioni (D1-D6) che vincolano la scrittura del documento. In sintesi, cosa hanno cambiato:

- **D1**: l'overlap di BQ1 si costruisce su un profilo di mood con tabella di corrispondenza curata, perché i generi dei due domini non si agganciano per nome
- **D2**: il dimensionamento di BQ2 usa `popularity` e mai i conteggi di tracce, perché il campione è bilanciato per costruzione
- **D3**: il confronto di durata riguarda solo film e tracce; le serie TV escono e vengono trattate a parte
- **D4**: ogni KPI dichiara se opera su coppie traccia-genere o su tracce deduplicate
- **D5**: la scala di confidenza ha tre criteri operativi basati sugli strati interpretativi tra dato e numero
- **D6**: nessun artefatto `contracts/`, per non duplicare le definizioni delle schede KPI

## Fase 1 — Design & Contracts

**Completata**. Output: [data-model.md](./data-model.md), [quickstart.md](./quickstart.md).

`data-model.md` descrive le entità del framework — domanda di business, KPI, North Star, fonte, confidenza, assunzione — con i loro vincoli di integrità: univocità degli identificativi, cardinalità KPI-domanda, coerenza obbligatoria tra livello di confidenza e formato di presentazione.

`quickstart.md` è la guida di verifica: controlli strutturali eseguibili da riga di comando (conteggi, presenza delle sezioni, assenza di numeri di risultato) più la sessione di revisione in contesto pulito che FR-019 richiede.

## Complexity Tracking

Nessuna violazione della constitution da giustificare.
