# Specification Quality Checklist: Dashboard — modello, pagine, misure a schermo

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-24
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

## Notes

**Sulla prima voce e sull'ultima, che vanno lette insieme.** La spec nomina Power BI Desktop, il formato `.pbix`, il DAX e i nomi delle misure. Non è una fuga di dettaglio implementativo: lo strumento di presentazione è **fissato dalla constitution** (principio V e sezione «Vincoli di Dominio e di Dato», che nomina Power BI Desktop e Tableau Public come strumenti a interazione manuale), e i nomi delle misure sono identificativi già pubblicati da cinque documenti del progetto. Una spec che li omettesse per conformità formale descriverebbe una feature diversa da quella che verrà costruita. È lo stesso trattamento adottato dalla spec della `007b`.

**Sulla terza voce.** La prosa è in italiano e ogni sigla usata (`BQ1-K3`, `is_high_zero_genre`, `C1`/`C2`/`C3`, `D7`, `E9`) rinvia al documento che la definisce. Resta vero che il lettore ideale di questa spec conosce il progetto: è una spec interna, non l'artefatto rivolto al lettore esterno — quello è la dashboard, ed è la `008b` a renderlo leggibile senza contesto. Il rilievo `R11` della revisione `007b` (issue `#16`, glossario) copre esattamente questa zona ed è aperto.

**Sui criteri di successo e la loro verificabilità.** `SC-001`, `SC-003`, `SC-004` e `SC-005` sono misurabili ma **non automatizzabili**: si verificano guardando lo schermo, perché il deliverable vive fuori dal confine dell'automazione. Non è un difetto della formulazione: è la forma che il principio V impone, ed è dichiarata in «Come si verifica».

Nessuna voce richiede aggiornamenti prima di `/speckit.plan`.
