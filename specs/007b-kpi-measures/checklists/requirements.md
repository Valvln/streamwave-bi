# Specification Quality Checklist: Misure DAX e documento dei KPI

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-22
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — eccezione dichiarata: il linguaggio dello script (Python) e la libreria di precisione (`decimal.Decimal`) sono citati perché sono essi stessi una decisione di processo (E1) resa necessaria dal vincolo del principio V, non un dettaglio implementativo lasciato alla fase di piano — lo stesso trattamento che la `004` ha riservato a `decimal.Decimal` nella propria spec.
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

- Le otto misure e i sei debiti ereditati sono lo stesso identico elenco del prompt di consegna: nessuna interpretazione libera è stata necessaria oltre a E7/E8, entrambi dichiarati come verifica e non come nuova decisione.
- **Revisione di regia, 2026-08-22**: applicate tre correzioni. (1) aggiunta la decisione E9 — verifica manuale contro il motore reale da parte di Valerio, prima del merge, spostata dentro il perimetro della feature invece che rinviata alla `008a`; il principio V esclude l'automazione della GUI, non l'uso manuale del progetto. (2) corretto il conteggio in due punti (User Story 5, Key Entities): `docs/kpi_measures.md` è il settimo documento verificato e il sesto in severità stretta, non il settimo in severità stretta — stessa classe di errore dell'issue `#8`. (3) corretto il test indipendente di User Story 1: la riproducibilità che conta attraversa `build_datasets.py` (che rigenera `data/processed/`, non versionato) e poi `build_kpi_measures.py`, non lo script nuovo da solo.
- Prossimo passo: questa spec torna in revisione (primo punto di stop del flusso, `CLAUDE.md`) prima di `/speckit.plan`.
- **Revisione di regia sul piano e sui task, 2026-08-22**: un rilievo bloccante. L'esito di E9 non aveva alcuna ancora: `reports/kpi_measures.json` è generato dallo script ed è deterministico per FR-003, quindi non può contenere una lettura umana, e sotto severità stretta il controllo avrebbe fermato proprio il ramo in cui E9 trova una divergenza — l'unico caso in cui questo passo produce qualcosa di nuovo da dire. Anche l'esito «coincide» è un'affermazione derivata (regola D5) e voleva un'ancora propria. Rimedio: `reports/kpi_engine_check.json`, artefatto versionato curato a mano — mai scritto da uno script, sul precedente di `data/benchmarks/bq3_tier_upgrade.json` — che congela le otto letture del motore, la data e l'esito del confronto; nuovo FR-029a in spec.md, sesto membro di `ARTIFACTS`, nuovo task T026a in tasks.md fra il dispatch di E9 (T026) e la sua incorporazione nel documento (T027). Una seconda correzione non bloccante: nessun task riseguiva `check_audit_coherence.py` dopo le correzioni della revisione in contesto pulito (T040); aggiunto T040a. Applicate anche a plan.md e data-model.md (nuova Entità 1bis).
