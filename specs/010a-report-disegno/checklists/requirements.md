# Specification Quality Checklist: il report che porta l'argomento a schermo — disegno

**Purpose**: validare completezza e qualità della spec prima di passare al piano
**Created**: 2026-08-29
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

**Nota sulla prima voce.** La spec nomina Power BI, DAX e `.pbix`. Non è una violazione: lo strumento di presentazione è vincolato dalla constitution (principio V) e non è una scelta che questa feature prende. I nomi compaiono per delimitare il perimetro — che cosa la feature **non** fa — non per prescrivere un'implementazione.

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

**Sui criteri di successo e la loro misurabilità.** `SC-001` e `SC-004` sono verificabili per lettura, non per conteggio: sono gli unici due che chiedono un giudizio. È deliberato e dichiarato qui invece di essere mascherato da una soglia numerica arbitraria — «la sequenza si legge come un discorso» non ha una metrica, e inventarne una produrrebbe un numero senza fonte, che è ciò che il principio I vieta. Il presidio su entrambi è la revisione in contesto pulito, non il controllo automatico.

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Gate di feature *(Constitution, Workflow e Quality Gate)*

- [x] La spec dichiara a quale domanda di business risponde (principio VI) — tutte e tre, con la ragione
- [x] La spec contiene «Limiti Dichiarati» compilata (principio IV)
- [x] La spec contiene «Provenienza e Confidenza dei Dati» (principio I) — nessuna metrica nuova, elencato ciò che il disegno porta a schermo
- [x] La stima è entro una giornata lavorativa (principio III) — ~6 ore, revisione e chiusura dei rilievi incluse

## Notes

Nessun elemento incompleto. La spec è pronta per il primo punto di fermata.
