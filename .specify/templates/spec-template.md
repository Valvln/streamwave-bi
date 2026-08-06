# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`

**Created**: [DATE]

**Status**: Draft

**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

## Assumptions

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right assumptions based on reasonable defaults
  chosen when the feature description did not specify certain details.
-->

- [Assumption about target users, e.g., "Users have stable internet connectivity"]
- [Assumption about scope boundaries, e.g., "Mobile support is out of scope for v1"]
- [Assumption about data/environment, e.g., "Existing authentication system will be reused"]
- [Dependency on existing system/service, e.g., "Requires access to the existing user profile API"]

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

<!--
  ACTION REQUIRED: indicare a quale delle tre domande di business risponde questa feature
  (BQ1 posizionamento / BQ2 segmento di ingresso / BQ3 impatto stimato) e come vi contribuisce.
  Una feature non riconducibile a nessuna delle tre non va implementata.
-->

- **Domanda servita**: [BQ1 | BQ2 | BQ3]
- **Contributo**: [in che modo questa feature avvicina la risposta alla domanda]

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

<!--
  ACTION REQUIRED: una riga per ogni metrica o numero introdotto dalla feature.
  Fonte: Netflix (reale) | Spotify (reale) | Sintetico | Derivato (elencare le fonti a monte).
  Confidenza bassa => il valore va espresso come range best/base/worst, mai come numero singolo.
-->

| Metrica | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| [nome metrica] | [fonte] | [alto/medio/basso] | [perché quel livello] | [valore singolo / range] |

**Assunzioni dietro i dati sintetici**: [dichiarare per iscritto, oppure "nessun dato sintetico"]

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

<!--
  ACTION REQUIRED: cosa questa feature NON risponde. Coprire almeno: domande fuori portata
  dei dati, conclusioni che il lettore potrebbe erroneamente inferire, vincoli di copertura
  temporale del dato. Nessun lessico causale su risultati correlazionali.
-->

- **Non risponde a**: [domanda fuori scope e perché i dati non la coprono]
- **Inferenza da evitare**: [conclusione che il lettore potrebbe trarre erroneamente]
- **Copertura del dato**: [vincoli temporali o di perimetro, es. catalogo Netflix fermo al 2021]
- **Dove è esposto all'utente finale**: [dove compare il limite in dashboard/report, se applicabile]
