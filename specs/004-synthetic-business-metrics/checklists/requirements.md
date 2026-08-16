# Specification Quality Checklist: Synthetic Business Metrics

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-16
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Gate della constitution — prima di implementare

- [x] La spec dichiara a quale domanda di business risponde (principio VI) — BQ3, sezione «Domanda di Business»
- [x] La spec contiene «Limiti Dichiarati» compilata (principio IV)
- [x] La spec contiene «Provenienza e Confidenza dei Dati» per ogni numero introdotto (principio I), con l'etichetta `Benchmark (esterno)` dove pertinente
- [x] La stima è entro una giornata lavorativa (principio III) — 6 ore, revisione inclusa. È un vincolo di processo e **non** un criterio di successo: sta nella nota in coda ai Measurable Outcomes, non fra essi
- [x] Le cinque condizioni sui benchmark sono tutte tradotte in requisiti: citazione puntuale (FR-003), valore congelato in file versionato (FR-002), nessuna rete a runtime (FR-008), assunzione di trasferimento dichiarata (FR-007), nessuna promozione di confidenza (FR-021)

## Note

### Revisione della regia — 2026-08-16, sei rilievi, tutti incorporati

La spec è stata rivista dalla sessione di regia al punto di stop 1. Nessun rilievo è caduto.

| Rilievo | Contenuto | Come è stato chiuso |
|---|---|---|
| **R1** | i fattori della banda vanno fissati **prima** di conoscere il benchmark: FR-011 ne imponeva l'ancoraggio e la dichiarazione, non il momento | **FR-011a** nuovo, più il paragrafo di D2 che ne dà la ragione e il precedente di §3 del business case |
| **R2** | nessun requisito imponeva che l'artefatto dei sei valori fosse **versionato**: FR-020 e SC-004 lo presupponevano soltanto | **FR-018a** nuovo, con il precedente di `reports/cleaning_report.json` |
| **R3** | `A6` e le note datate non devono contenere il **valore del benchmark**: il business case non è sotto controllo di coerenza, e un numero nella sua prosa riaprirebbe R8 della 001 | **FR-025a** e **FR-027a** nuovi |
| **R4** | il rapporto al punto di stop serve **anche quando la fonte viene adottata**: il rischio non è il fallimento rumoroso ma l'adozione silenziosa di una fonte «abbastanza vicina» | **FR-006a** nuovo |
| **R5** | «non dipende dalla 002 né dalla 003» è vero per i **dati** e falso per gli **strumenti**: FR-019 e FR-020 toccano artefatti di quelle feature | riscritta la sezione «Rapporto con le feature vicine», che ora distingue le due indipendenze |
| **R6** | SC-008 era un vincolo di **processo** fra criteri verificabili sul prodotto | rimosso dai Measurable Outcomes; la stima è ora una nota in coda alla sezione, che dichiara la differenza |

I quattro requisiti nuovi usano la forma con suffisso — `FR-006a`, `FR-011a`, `FR-018a`, `FR-025a`, `FR-027a` — sul precedente di `FR-017a` della 001, per collocarli accanto al requisito che estendono senza rinumerare i 32 esistenti.

**Un tratto comune ai sei rilievi vale più dei singoli**: quattro su sei — R1, R2, R3, R4 — sono casi della stessa regola di `CLAUDE.md`, *se una cosa non è scritta non accade*. In tutti e quattro la spec descriveva correttamente lo stato desiderato e ometteva il requisito che lo impone, lasciandolo a un automatismo, a un'ovvietà o al buon senso di chi esegue.

### Osservazioni della validazione

**Nessun marcatore [NEEDS CLARIFICATION].** Le due decisioni con più di una lettura ragionevole — la forma della derivazione (D1) e il passaggio da un benchmark a tre scenari (D2) — sono state **prese e argomentate** anziché rinviate, come il prompt di consegna richiedeva esplicitamente. Sono riportate alla regia come decisioni da contestare: è la sede giusta, perché una decisione argomentata si contesta meglio di una domanda aperta.

**Un'assunzione della spec non è confermata.** «Esiste una fonte pubblica citabile per il tasso di conversione a un tier superiore» è dichiarata fra le Assumptions e **non è verificata**: una ricognizione preliminare non ha trovato la metrica esatta in forma direttamente citabile e gratuitamente recuperabile. FR-006 governa il caso in cui cada, e riserva a Valerio la decisione conseguente. La checklist la registra come rischio noto, non come difetto della spec.

**Il perimetro rende la feature più piccola del nome che porta.** La spec lo dichiara in apertura e nella sezione «Perimetro». Non è un'omissione: è il risultato della domanda che il prompt chiedeva di porre per prima.

- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`
