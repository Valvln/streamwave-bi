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
- [x] La stima è entro una giornata lavorativa (principio III) — 6 ore, vedi SC-008
- [x] Le cinque condizioni sui benchmark sono tutte tradotte in requisiti: citazione puntuale (FR-003), valore congelato in file versionato (FR-002), nessuna rete a runtime (FR-008), assunzione di trasferimento dichiarata (FR-007), nessuna promozione di confidenza (FR-021)

## Note

### Osservazioni della validazione

**Nessun marcatore [NEEDS CLARIFICATION].** Le due decisioni con più di una lettura ragionevole — la forma della derivazione (D1) e il passaggio da un benchmark a tre scenari (D2) — sono state **prese e argomentate** anziché rinviate, come il prompt di consegna richiedeva esplicitamente. Sono riportate alla regia come decisioni da contestare: è la sede giusta, perché una decisione argomentata si contesta meglio di una domanda aperta.

**Un'assunzione della spec non è confermata.** «Esiste una fonte pubblica citabile per il tasso di conversione a un tier superiore» è dichiarata fra le Assumptions e **non è verificata**: una ricognizione preliminare non ha trovato la metrica esatta in forma direttamente citabile e gratuitamente recuperabile. FR-006 governa il caso in cui cada, e riserva a Valerio la decisione conseguente. La checklist la registra come rischio noto, non come difetto della spec.

**Il perimetro rende la feature più piccola del nome che porta.** La spec lo dichiara in apertura e nella sezione «Perimetro». Non è un'omissione: è il risultato della domanda che il prompt chiedeva di porre per prima.

- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`
