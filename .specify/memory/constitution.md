<!--
SYNC IMPACT REPORT
==================
Version change: TEMPLATE (non ratificata) → 1.0.0
Bump rationale: prima ratifica. Nessuna versione precedente da confrontare, quindi MAJOR
                secondo la policy di versioning (adozione iniziale dell'impianto di governance).

Principi definiti (tutti nuovi):
  - [PRINCIPLE_1_NAME] → I. Provenienza e Confidenza dei Dati (NON NEGOZIABILE)
  - [PRINCIPLE_2_NAME] → II. Riproducibilità Totale
  - [PRINCIPLE_3_NAME] → III. Incrementalità
  - [PRINCIPLE_4_NAME] → IV. Trasparenza sui Limiti
  - [PRINCIPLE_5_NAME] → V. Confine dell'Automazione
  - (aggiunto oltre il template a 5) → VI. Coerenza Narrativa

Sezioni aggiunte:
  - [SECTION_2_NAME] → Vincoli di Dominio e di Dato
  - [SECTION_3_NAME] → Workflow di Sviluppo e Quality Gate

Sezioni rimosse: nessuna.

Template dipendenti:
  ✅ .specify/templates/spec-template.md — aggiunte due sezioni obbligatorie
     ("Provenienza e Confidenza dei Dati", "Limiti Dichiarati") a supporto dei principi I e IV
  ✅ .specify/templates/plan-template.md — nessuna modifica necessaria: il blocco
     "Constitution Check" è un segnaposto popolato in fase di /speckit.plan a partire da questo file
  ✅ .specify/templates/tasks-template.md — nessuna modifica necessaria: le categorie di task
     sono agnostiche e il vincolo di 1 giornata (principio III) si applica in fase di scomposizione
  ✅ .claude/skills/speckit-*/SKILL.md e .github/prompts/speckit.*.prompt.md — nessun riferimento
     obsoleto o agent-specifico da correggere
  ✅ README.md — allineato (licenza MIT, stato fasi)

TODO differiti: nessuno. Lo stack tecnico non è vincolato di proposito (vedi sezione
"Vincoli di Dominio e di Dato"): la scelta è demandata alla fase /speckit.plan.
-->

# StreamWave BI Constitution

Case study di Business Intelligence a supporto di una decisione strategica: StreamWave,
piattaforma di streaming video, valuta l'ingresso nel verticale del music streaming.
Il criterio di accettazione di ogni artefatto prodotto è uno solo: **deve reggere la
presentazione a un board reale**. Chi legge può non fidarsi dell'analista, ma deve poter
verificare da dove viene ogni numero.

## Core Principles

### I. Provenienza e Confidenza dei Dati (NON NEGOZIABILE)

Ogni KPI, metrica o numero mostrato in dashboard, report o documentazione DEVE dichiarare
in modo leggibile dall'utente finale:

- **Fonte**: `Netflix (reale)`, `Spotify (reale)`, `Sintetico` o `Derivato` (calcolato da
  più fonti — in tal caso vanno elencate le fonti a monte).
- **Livello di confidenza**: `alto`, `medio` o `basso`, con il criterio di attribuzione
  documentato nella feature che introduce la metrica.

Un valore sintetico NON DEVE essere presentato con precisione superiore a quanto la
metodologia giustifica: se la generazione poggia su un'assunzione a una cifra significativa,
il risultato non può esserne mostrato con tre.

Dove la confidenza è `bassa`, il valore DEVE essere espresso come **range best/base/worst
case**, mai come numero singolo. Un numero singolo comunica una certezza che il dato non ha.

Le assunzioni dietro ogni dato sintetico DEVONO essere dichiarate per iscritto e versionate
insieme allo script che le implementa, non solo nel commento del codice.

*Rationale*: il progetto mescola dati reali di due domini diversi con dati simulati per un
mercato in cui StreamWave non è ancora entrata. Senza etichettatura esplicita, la dashboard
diventa indistinguibile da una previsione inventata — ed è esattamente l'obiezione che un
board solleverebbe per primo.

### II. Riproducibilità Totale

Ogni trasformazione sui dati — cleaning, join, feature engineering, aggregazione,
generazione sintetica — DEVE essere implementata come codice in **Python** o **Power Query M**
e versionata nel repository.

Sono VIETATE le modifiche manuali one-off su file Excel o CSV. Se un dato è sbagliato, si
corregge lo script che lo produce, non il file di output.

`data/raw/` è **immutabile e in sola lettura**: nessuno script scrive al suo interno. Il
contenuto DEVE essere ricostruibile da fonte pubblica tramite `scripts/download_data.sh`.

Chiunque cloni il repository DEVE poter rigenerare ogni dataset intermedio e finale partendo
solo dal codice versionato e dai dataset pubblici di origine.

*Rationale*: un'analisi che non si può rieseguire non si può nemmeno difendere. Una modifica
manuale non tracciata rende l'intera catena non verificabile a valle.

### III. Incrementalità

Ogni feature DEVE essere completabile in **una giornata lavorativa**. Se la stima supera
quel limite, la feature NON DEVE essere avviata: va prima scomposta in unità più piccole,
ciascuna con valore dimostrabile in autonomia.

Ogni feature DEVE lasciare il repository in uno stato coerente e presentabile: niente rami
di lavoro che restano aperti a metà tra due stati funzionanti.

*Rationale*: vincolo di ritmo, non di ambizione. Feature piccole significano feedback
frequente, history git leggibile e nessun blocco su lavori lunghi mai finiti — il modo
tipico in cui un progetto da portfolio muore a metà.

### IV. Trasparenza sui Limiti

Ogni feature analitica DEVE dichiarare esplicitamente **cosa NON risponde**, in una sezione
dedicata della propria spec e — dove il consumatore è l'utente finale — nella dashboard stessa.

La dichiarazione DEVE coprire almeno: domande fuori portata dei dati disponibili, conclusioni
che il lettore potrebbe erroneamente inferire, e vincoli temporali o di copertura del dato
(es. catalogo Netflix fermo al 2021).

Una correlazione NON DEVE mai essere presentata con lessico causale.

*Rationale*: l'omissione di un limite è di fatto un'affermazione implicita. Dichiarare il
perimetro protegge sia il lettore sia la credibilità dell'analisi.

### V. Confine dell'Automazione

L'automazione — script, agent, Claude Code — copre: data prep, ETL, misure DAX, generazione
di dati sintetici, documentazione e testing.

L'interazione con l'**interfaccia grafica di Power BI Desktop e Tableau Public** resta
**manuale** ed è fuori dallo scope automatizzabile. Nessun task può presupporre che un agent
pilota quelle GUI.

Ne consegue che i task di build della dashboard DEVONO essere formulati come istruzioni
eseguibili da una persona, e che tutto ciò che è esprimibile come artefatto testuale
versionabile (misure DAX, schema del modello dati, mapping dei campi) DEVE esserlo, invece
di vivere solo dentro il file binario del report.

*Rationale*: confine onesto tra ciò che l'automazione fa davvero e ciò che richiede una
persona davanti allo schermo. Massimizza al contempo la porzione di lavoro che resta
versionata e ispezionabile.

### VI. Coerenza Narrativa

Ogni feature DEVE essere riconducibile a una delle tre domande di business (BQ1, BQ2, BQ3
definite nella sezione seguente). La spec di ogni feature DEVE indicare a quale domanda
risponde e in che modo vi contribuisce.

Una feature che non è riconducibile a nessuna delle tre NON DEVE essere implementata: va
prima motivata come estensione dello scope, con aggiornamento esplicito di questo documento.

*Rationale*: un case study da portfolio si giudica sul filo del discorso, non sul numero di
grafici. Il vincolo di tracciabilità impedisce l'accumulo di analisi tecnicamente corrette
ma narrativamente inerti.

## Vincoli di Dominio e di Dato

**Le tre domande di business** che l'intero progetto deve servire:

- **BQ1 — Posizionamento**: qual è il posizionamento del contenuto musicale rispetto a
  quello video in termini di caratteristiche "vincenti" (durata, genere, mood)? Esiste
  overlap di audience potenziale?
- **BQ2 — Segmento di ingresso**: quale segmento musicale (genere/mood) rappresenterebbe
  l'opportunità di ingresso più coerente con il catalogo attuale di StreamWave?
- **BQ3 — Impatto stimato**: che impatto stimato — simulato, con assunzioni dichiarate —
  avrebbe l'aggiunta del verticale musicale su engagement e revenue?

**Fonti dati ammesse**:

- `data/raw/netflix_titles.csv` — catalogo Netflix, proxy del catalogo StreamWave. Copertura
  fino al 2021: ogni conclusione temporale DEVE tenerne conto (principio IV).
- `data/raw/spotify_tracks_dataset.csv` — tracce Spotify con audio feature, proxy del mercato
  musicale.
- Dati sintetici generati da script versionati, esclusivamente dove i dati reali non esistono
  (tipicamente BQ3: engagement e revenue di un verticale non ancora lanciato).

L'uso di Netflix come proxy di StreamWave e di Spotify come proxy del mercato musicale è una
**assunzione strutturale del case study** e DEVE essere dichiarata in ogni artefatto rivolto
all'utente finale, non solo nella documentazione tecnica.

**Stack tecnico**: deliberatamente non vincolato da questa constitution, salvo per quanto
imposto dai principi II (Python o Power Query M per le trasformazioni) e V (Power BI Desktop
e Tableau Public come strumenti di presentazione a interazione manuale). Ogni ulteriore
scelta tecnologica è demandata alla fase `/speckit.plan` e va motivata lì.

## Workflow di Sviluppo e Quality Gate

Il progetto segue il flusso spec-driven di Spec Kit:
`/speckit.constitution` → `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` →
`/speckit.implement`.

**Gate prima di iniziare l'implementazione di una feature**:

1. La spec dichiara a quale domanda di business risponde (principio VI).
2. La spec contiene la sezione "Limiti Dichiarati" compilata (principio IV).
3. La spec contiene la sezione "Provenienza e Confidenza dei Dati" per ogni metrica
   introdotta (principio I).
4. La stima è entro una giornata lavorativa, o la feature è già stata scomposta (principio III).

**Gate prima di considerare una feature conclusa**:

1. Ogni trasformazione è scriptata e versionata; nessun passaggio manuale non documentato
   (principio II).
2. La pipeline è rieseguibile da zero su una copia pulita del repository.
3. Ogni numero pubblicato è etichettato con fonte e confidenza; i valori a bassa confidenza
   sono espressi come range (principio I).
4. I task che richiedono la GUI di Power BI o Tableau sono scritti come istruzioni manuali
   verificabili da una persona (principio V).

**Convenzioni**: commit in italiano, imperativo, con prefisso convenzionale
(`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`). La history è parte dell'artefatto da
portfolio e va tenuta leggibile.

## Governance

Questa constitution **prevale su ogni altra pratica di progetto**. In caso di conflitto tra
una scelta di comodo e un principio qui dichiarato, prevale il principio; se il principio è
davvero inapplicabile, si emenda il documento — non lo si aggira in silenzio.

**Procedura di emendamento**:

1. La modifica proposta è motivata per iscritto (principio interessato, ragione, impatto sugli
   artefatti già prodotti).
2. Il documento viene aggiornato insieme al Sync Impact Report in testa al file.
3. I template dipendenti sotto `.specify/templates/` vengono riallineati nello stesso commit.
4. Gli artefatti già prodotti che violano il nuovo testo vengono corretti o esplicitamente
   marcati come debito con scadenza.

**Policy di versioning** (semantic versioning):

- **MAJOR**: rimozione o ridefinizione incompatibile di un principio o della governance.
- **MINOR**: aggiunta di un nuovo principio o di una sezione, o ampliamento sostanziale di
  una guida esistente.
- **PATCH**: chiarimenti, riformulazioni, correzioni non semantiche.

**Verifica di conformità**: la conformità va verificata a ogni gate di feature (vedi sezione
precedente) e durante `/speckit.analyze`. Ogni violazione consapevole DEVE essere registrata
nella tabella "Complexity Tracking" del piano della feature, con la giustificazione e
l'alternativa più semplice che è stata scartata.

**Version**: 1.0.0 | **Ratified**: 2026-08-06 | **Last Amended**: 2026-08-06
