# Implementation Plan: Data Model Design

**Branch**: `005-data-model-design` | **Date**: 2026-08-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/005-data-model-design/spec.md`

## Summary

La feature disegna il modello dati su cui la `007` scriverà le misure DAX e la `008` costruirà la dashboard, e lo consegna come **documento versionato** invece che come file binario, per l'obbligo esplicito del principio V.

L'approccio scelto è **due stelle disgiunte** — una per il catalogo video, una per il catalogo musicale — con un ponte per lato a risolvere le due appartenenze multiple, e nessuna relazione fra i due lati: le due tassonomie non hanno chiave comune e il confronto fra i cataloghi avviene fra misure, non fra righe. Il punto in cui i due lati diventano confrontabili è la tabella del profilo di mood delle categorie video, di cui questa feature **dichiara la forma e non scrive alcuna riga**, perché è della `006`.

Il valore della feature non sta nello schema, che è convenzionale, ma nelle **quattro ambiguità che chiude**: che cosa sia un segmento, quante nozioni di grana servano per descrivere un KPI, da quale tabella si legga la popolarità quando le due musicali discordano, e quale campo realizzi l'asse di mood che il business case chiama «ritmo».

## Technical Context

**Linguaggio della prosa**: italiano. **Identificativi**: inglese, `snake_case`. Convenzione di progetto, constitution §Convenzioni.

**Artefatti prodotti**: `docs/data_model.md` (pubblicato), `specs/005-data-model-design/contracts/model-contract.md` (di lavorazione). Vedi `T1` di [research.md](./research.md).

**Artefatti modificati**: `scripts/check_audit_coherence.py` (una riga in `DOCUMENTS`), `docs/business_case.md` (due note in loco), `README.md` (drift).

**Ingressi**: i quattro dataset di `data/processed/`, letti **attraverso** [`specs/003-data-cleaning-etl/contracts/output-datasets.md`](../003-data-cleaning-etl/contracts/output-datasets.md) e non attraverso i file, che non sono versionati.

**Fonti delle ancore**: `reports/data_profile.json`, `reports/cleaning_report.json`. Copertura verificata in fase di piano — vedi `T2`.

**Strumento di destinazione**: Power BI Desktop, motore tabellare a schema a stella con relazioni e direzioni di filtro dichiarate. Fissato dalla constitution (principio V) e dalla roadmap.

**Testing**: `python3 scripts/check_audit_coherence.py`, che non richiede `data/raw/` e non riesegue alcuna pipeline. Più le prove manuali del [quickstart](./quickstart.md), fra cui quella di lettura in contesto pulito che realizza `SC-003`.

**Scala**: 7 tabelle, 5 relazioni, 8 KPI da mappare sulle tre grane, ~40 colonne da tracciare.

**Nessuna dipendenza da installare**: la feature non aggiunge codice eseguibile oltre a una riga di registro in uno script esistente.

## Constitution Check

*GATE: da superare prima della Fase 0. Ricontrollato dopo la Fase 1.*

| Principio | Esito | Come è soddisfatto |
|---|---|---|
| **I — Provenienza e Confidenza** | ✅ | la feature non introduce metriche; introduce strutture, e la spec dichiara provenienza e confidenza della catena per ciascuna. Ogni colonna del modello dichiara dataset e campo di origine (`FR-018`). Ogni quantità del documento è ancorata (`FR-004`), con copertura verificata in `T2` |
| **II — Riproducibilità Totale** | ✅ | nessuno script scrive in `data/raw/`; nessun dataset viene modificato. Le due dimensioni derivate sono dichiarate come regola riproducibile (`T7`) e il principio ammette Power Query M. Il controllo di coerenza gira su una copia priva dei dati di origine |
| **III — Incrementalità** | ⚠️ **dentro il limite, sopra la stima** | ~6,25 ore contro le 5 di roadmap. Sta nelle 6-7 ore del principio, quindi la condizione di scomposizione non si verifica e il taglio `005a`/`005b` non si attiva. Lo scostamento va riportato al secondo punto di stop — vedi `T10` |
| **IV — Trasparenza sui Limiti** | ✅ | la spec dichiara cosa il modello rende **impossibile** misurare, non solo cosa abilita. L'assenza della dimensione di calendario (`D5`) è la forma strutturale di un limite già dichiarato a parole |
| **V — Confine dell'Automazione** | ✅ | è il principio che *impone* questa feature: schema e mapping DEVONO essere artefatto testuale. Nessun task presuppone che un agent piloti la GUI, e il documento è scritto per essere eseguito da una persona |
| **VI — Coerenza Narrativa** | ✅ | serve BQ1 e BQ2, con il ponte scritto per esteso nella spec: su BQ2 il contributo è l'unità di analisi, su BQ1 la commensurabilità, su entrambe la protezione del denominatore. Su BQ3 il contributo è dichiarato **nullo** invece di essere inventato |

**Gate prima di iniziare l'implementazione** — tutti e quattro superati: la spec dichiara la domanda di business, contiene «Limiti Dichiarati», contiene «Provenienza e Confidenza», e la stima è dentro la giornata lavorativa senza bisogno di scomposizione.

**Nessuna violazione da registrare in Complexity Tracking.**

### Ricontrollo dopo la Fase 1

Nessun principio cambia esito. Due cose emerse in Fase 1 vanno però registrate:

- **`T3` è una deviazione dal template, non dalla constitution.** La Fase 1 non produce `data-model.md` sotto `specs/`, perché per questa feature coinciderebbe con il deliverable e creerebbe due fonti. È dichiarata, motivata e riconducibile a una lezione già pagata dalla `003`.
- **`T11` è un ritrovamento che tocca una misura.** Dopo la trasformazione della `003` il campione musicale non è più bilanciato fra i segmenti. Non apre una nota in loco — l'affermazione del business case riguarda la fonte e resta vera — ma va dichiarato nel documento del modello.

## Project Structure

### Documentation (this feature)

```text
specs/005-data-model-design/
├── spec.md                       # approvata al primo punto di stop
├── plan.md                       # questo file
├── research.md                   # Fase 0: decisioni T1-T11
├── contracts/
│   └── model-contract.md         # Fase 1: l'interfaccia per 006, 007, 008
├── quickstart.md                 # Fase 1: le prove di validazione
├── checklists/
│   └── requirements.md
├── tasks.md                      # Fase 2, prodotto da /speckit.tasks
└── review.md                     # verbale della revisione in contesto pulito
```

**`data-model.md` non compare, deliberatamente.** Vedi `T3`.

### Artefatti del repository toccati dalla feature

```text
docs/
├── data_model.md                 # NUOVO — il deliverable
└── business_case.md              # MODIFICATO — due note in loco, §5.2 e §4 (BQ2)

scripts/
└── check_audit_coherence.py      # MODIFICATO — una riga in DOCUMENTS, severità stretta

README.md                         # MODIFICATO — chiusura del drift
```

**Structure Decision**: nessuna cartella nuova, nessuno script nuovo, nessun dataset nuovo. La feature produce un documento e un contratto, e tocca tre artefatti esistenti. È la forma più leggera compatibile con il principio V, e la sola giustificabile per una feature che **progetta e non materializza**.

## Fase 1 — Design & Contracts

### Il contratto

[`contracts/model-contract.md`](./contracts/model-contract.md) fissa l'interfaccia fra questa feature e le tre che la consumano, sul precedente diretto del contratto degli output della `003`. Contiene la forma normativa di: tabelle e grane, chiavi, relazioni e direzioni, mapping delle colonne, la matrice delle tre grane per gli 8 KPI, e la forma della tabella che la `006` riempirà.

Non contiene la **motivazione** delle scelte, che vive nel documento pubblicato e in `research.md`. Il contratto dice *che cosa*, il documento dice *perché*: è la separazione che il contratto della `003` ha adottato e che ha funzionato.

### Le prove

[`quickstart.md`](./quickstart.md) elenca le prove di validazione, alcune eseguibili e altre manuali. Due vincoli, entrambi nati da difetti reali:

- **nessuna prova può passare per assenza di output.** È il difetto della Prova 9 della `004`, dove `git diff main` su un clone falliva, non produceva righe, e la prova riportava esito positivo. Ogni prova di questo quickstart dichiara che cosa deve **comparire**, non solo che cosa non deve;
- **le prove si eseguono anche su un clone privo di `data/raw/`**, perché è la condizione in cui il lettore esterno verifica.

## Complexity Tracking

Nessuna violazione della constitution da giustificare.

Una sola annotazione di complessità, e non è una violazione: **la bidirezionalità del ponte titolo-categoria** (`T6`). È la sola scelta del modello che introduce un rischio di ambiguità di percorso, ed è ammessa perché la condizione che la rende sicura è strutturale e verificabile — la stella video ha un solo ponte, nessun ciclo, e le due stelle sono disgiunte. Il documento deve dichiarare la condizione insieme alla direzione, perché una direzione bidirezionale sicura oggi smette di esserlo il giorno in cui qualcuno aggiunge una seconda relazione.

## Nota di calendario

La sessione ha attraversato la mezzanotte: spec e `research.md` portano la data del 17 agosto, piano e artefatti di Fase 1 quella del 18. Le date non vengono uniformate perché sono esatte, e perché lo scostamento fra stime e timestamp git è materia della regia.

La roadmap collocava il **chore dell'ambiente Power BI prima** dell'apertura della `005`, con la motivazione che conviene aver visto lo strumento funzionare prima di decidere grane e relazioni. Il chore non risulta eseguito e la feature è stata aperta comunque. Non blocca il piano — il modello è progettato sul contratto della `003` e non sullo strumento — ma è la stessa radice del ritrovamento `F2`: nessuno ha ancora aperto Power BI, e il momento in cui qualcuno lo farà non è assegnato ad alcuna feature.
