# Specification Quality Checklist: Dashboard — narrazione, limiti a schermo, rifiniture

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-27
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

## Note su tre voci che meritano una precisazione

**«No implementation details».** La spec nomina Power BI Desktop, le pagine-tooltip e i segnalibri. Non è una fuga di dettaglio implementativo: sono i tre modi in cui lo strumento permette di nascondere un limite dietro un'azione dell'utente, e il divieto (`N3`) è una decisione di perimetro sul deliverable, non una scelta tecnica. Il principio V colloca la GUI fuori dall'automazione: ciò che la GUI rende possibile è quindi materia di spec, perché nessun piano potrà vincolarlo dopo.

**«Success criteria are technology-agnostic».** `SC-006` conta pagine, misure, tabelle e relazioni. Sono grandezze del deliverable, non dello strumento: misurano che la struttura chiusa dalla `008a` sia rimasta invariata, che è il criterio di perimetro di questa feature.

**«Requirements are testable».** Tutti i requisiti sono verificabili, ma **undici prove su dodici** lo sono solo da una persona davanti allo schermo. È dichiarato nella sezione *Come si verifica* della spec ed è il principio V, non una debolezza dei requisiti — la stessa condizione in cui si è chiusa la `008a`.

## Notes

- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
- Nessuna voce risulta incompleta alla prima iterazione di validazione.
