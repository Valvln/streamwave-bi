# Data Model — Feature 001: Business Case e Framework KPI

**Data**: 2026-08-07 | **Fase**: 1 (Design) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)

Il modello qui descritto non è un modello dati di database: è la struttura logica del framework che il documento deve esprimere. Le entità sono concetti del business case, i vincoli sono le regole che rendono il documento verificabile.

## Entità

### Domanda di business (BQ)

Unità di indagine del progetto. Fissate dalla constitution, non estendibili da questa feature.

| Attributo | Tipo | Vincoli |
|---|---|---|
| `id` | stringa | `BQ1`, `BQ2`, `BQ3` — chiusi, esattamente tre |
| `formulazione_originale` | testo | invariata rispetto alla constitution |
| `formulazione_misurabile` | testo | deve contenere soggetto, unità di misura e criterio di confronto o soglia (FR-003) |
| `kpi` | relazione | da 2 a 3 KPI (FR-004) |

### KPI

Misura definita concettualmente. È l'entità centrale: tutto il resto la qualifica.

| Attributo | Tipo | Vincoli |
|---|---|---|
| `sigla` | stringa | forma `BQn-Km`; `n` è la domanda, `m` la progressione al suo interno (FR-005a) |
| `nome_semantico` | stringa | inglese `snake_case`, **univoco su tutto il progetto**, non solo dentro la domanda (FR-005a) |
| `nome` | testo | denominazione leggibile, in italiano |
| `cosa_misura` | testo | una frase |
| `formula_concettuale` | testo | linguaggio naturale o pseudo-formula; vietati DAX, SQL, Python e nomi fisici di colonna (FR-007) |
| `unita` | stringa | |
| `granularita` | enum | `coppia traccia-genere` \| `traccia deduplicata` \| `titolo` \| `film` — decisione D4 |
| `direzione_lettura` | enum | `alto = meglio` \| `basso = meglio` \| `nessuna direzione` |
| `bq` | relazione | esattamente una (FR-006) |
| `fonte` | enum | `Netflix (reale)` \| `Spotify (reale)` \| `Sintetico` \| `Derivato` |
| `fonti_a_monte` | lista | obbligatoria se `fonte = Derivato` (FR-010) |
| `confidenza` | enum | `alto` \| `medio` \| `basso` |
| `formato_presentazione` | enum | `valore puntuale` \| `range best/base/worst` |

### North Star metric

| Attributo | Tipo | Vincoli |
|---|---|---|
| `definizione` | testo | di natura **coerenza strategica** (FR-008) |
| `composizione` | relazione | uno o più KPI, **tutti a confidenza alta** |
| `alternative_scartate` | lista | almeno due, ciascuna con motivazione (FR-008) |

Esiste in esemplare unico. Non può includere KPI a confidenza media o bassa, né fondersi con la metrica di impatto economico (FR-020).

### Titolo secondario di impatto economico

| Attributo | Tipo | Vincoli |
|---|---|---|
| `definizione` | testo | metrica di impatto su revenue |
| `formato_presentazione` | costante | sempre `range best/base/worst` (FR-020) |
| `distinzione_visiva` | testo | deve essere esplicitamente distinto dalla North Star nel documento |

### Assunzione

| Attributo | Tipo | Vincoli |
|---|---|---|
| `enunciato` | testo | marcato visivamente come assunzione, mai come dato (FR-014, FR-016) |
| `ambito_impatto` | testo | quali KPI o conclusioni ne dipendono |
| `valore` | numero o testo | ammesso anche numerico se è un input di scenario (FR-016) |

Assunzioni obbligatorie nel documento: modello di ricavo a due tier con prezzi puntuali (FR-017), orizzonte a 12 mesi, base utenti, proxy strutturale Netflix/Spotify (FR-013), copertura temporale dei dati (FR-015).

### Voce fuori scope

| Attributo | Tipo | Vincoli |
|---|---|---|
| `domanda_esclusa` | testo | |
| `motivazione` | testo | obbligatoria |

Almeno cinque voci (FR-012).

## Vincoli di integrità

Sono le regole che rendono il framework verificabile meccanicamente. La guida di verifica ([quickstart.md](./quickstart.md)) le controlla una per una.

1. **Cardinalità**: ogni BQ ha 2-3 KPI; il totale è compreso tra 6 e 9.
2. **Appartenenza esclusiva**: ogni KPI appartiene a esattamente una BQ. Se un KPI è utile a due domande, si sceglie la primaria e nell'altra lo si cita come riferimento, senza duplicarne la definizione.
3. **Univocità**: nessun `nome_semantico` ripetuto in tutto il progetto; nessuna `sigla` ripetuta.
4. **Coerenza confidenza-formato**: `confidenza = basso` implica `formato_presentazione = range best/base/worst`. La violazione di questa regola è la sola che invalida il documento sul piano della constitution (principio I).
5. **Tracciabilità della fonte**: `fonte = Derivato` implica `fonti_a_monte` non vuoto.
6. **Composizione della North Star**: tutti i KPI che la compongono hanno `confidenza = alto`.
7. **Non duplicazione**: la `formula_concettuale` compare unicamente nella scheda del KPI, mai nella tabella riepilogativa (FR-005b).
8. **Granularità dichiarata**: ogni KPI che opera su dati Spotify dichiara se lavora su coppie traccia-genere o su tracce deduplicate (D4). L'omissione rende il KPI ambiguo del 21%.

## Struttura del documento

L'ordine delle sezioni di `docs/business_case.md` discende dalle user story della spec: US1 fornisce l'inquadramento, US2 il catalogo, US3 la qualificazione.

1. **Inquadramento** — chi è StreamWave, la decisione in valutazione, il destinatario (FR-002)
2. **Assunzioni strutturali** — proxy Netflix/Spotify, copertura temporale, modello di ricavo con prezzi (FR-013, FR-014, FR-015, FR-017)
3. **North Star metric** — definizione, motivazione, alternative scartate (FR-008)
4. **Le tre domande** — formulazione originale e riformulazione misurabile (FR-003)
5. **Framework KPI** — tabella riepilogativa come indice, poi una scheda per KPI (FR-005b)
6. **Scala di confidenza** — i tre criteri operativi di D5 (FR-009)
7. **Impatto economico** — il titolo secondario a range (FR-020)
8. **Out of scope** — almeno cinque voci motivate (FR-012)

Le note metodologiche che discendono dai ritrovamenti di Fase 0 — le due granularità (R2), l'esclusione delle serie TV dal confronto di durata (R3), l'inutilizzabilità dei conteggi (R1), la fragilità di `popularity` (R5) — vivono nella sezione 8 o nelle schede dei KPI che ne dipendono, mai in entrambe.
