# Feature Specification: Business Case e Framework KPI

**Feature Branch**: `001-business-case-kpi`

**Created**: 2026-08-06

**Status**: Draft

**Input**: User description: "Costruisci il business case e il framework KPI per un progetto di BI che valuta se StreamWave (piattaforma streaming intrattenimento fittizia) debba espandersi nel music streaming. Contesto: due dataset reali (catalogo Netflix ~8.800 righe, tracce Spotify ~114.000 righe) più dati sintetici da generare in una feature successiva. L'output è un documento (docs/business_case.md) che risponde a tre domande di business, definendo per ciascuna la domanda riformulata in modo misurabile, 2-3 KPI con formula concettuale, fonte dati e livello di confidenza. Include una North Star metric unica e una sezione out of scope. Nessuna implementazione tecnica: solo definizione concettuale."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Il board capisce cosa stiamo per misurare (Priority: P1)

Il decisore (board di StreamWave) apre `docs/business_case.md` senza contesto preliminare e in
pochi minuti capisce: quale decisione strategica è in gioco, come le tre domande di business sono
state riformulate in forma misurabile, qual è la singola metrica North Star che riassume il
successo dell'iniziativa, e cosa il progetto esplicitamente **non** proverà a dimostrare.

**Why this priority**: è l'inquadramento senza cui nessun KPI ha significato. Un documento che si
ferma qui è già un artefatto difendibile: dichiara la domanda, il criterio di successo e il
perimetro. Tutto il resto del progetto eredita queste definizioni, quindi ogni ambiguità lasciata
qui si propaga a valle moltiplicata.

**Independent Test**: si consegna il documento a un lettore che non ha partecipato al progetto e
gli si chiede di riformulare a voce la decisione in gioco, la North Star e due cose fuori scope.
Se ci riesce senza porre domande, la storia è superata.

**Acceptance Scenarios**:

1. **Given** un lettore che non conosce il progetto, **When** legge le prime due sezioni del
   documento, **Then** sa dire quale decisione di business il progetto deve supportare e chi ne è
   il destinatario.
2. **Given** il documento completo, **When** il lettore cerca la metrica di riferimento,
   **Then** trova **una sola** North Star metric, con la sua definizione e la ragione per cui è
   stata scelta al posto delle alternative considerate.
3. **Given** il documento completo, **When** il lettore cerca il perimetro, **Then** trova una
   sezione "Out of Scope" che elenca almeno cinque domande che il progetto non risponderà, ognuna
   con la motivazione.
4. **Given** le tre domande di business originali (BQ1, BQ2, BQ3), **When** si confrontano con le
   versioni riformulate nel documento, **Then** ogni riformulazione contiene un soggetto
   misurabile, un'unità di misura e una soglia o un criterio di confronto.

---

### User Story 2 - L'analista sa quali KPI costruire (Priority: P2)

L'analista che dovrà implementare le feature successive apre il documento e trova, per ciascuna
delle tre domande di business, 2-3 KPI definiti in modo non ambiguo: nome, cosa misura, formula
concettuale (in linguaggio naturale o pseudo-formula, non in codice), unità di misura e come si
legge il risultato (quale valore è "buono").

**Why this priority**: trasforma l'inquadramento in un piano di lavoro. Senza questo strato il
documento resta una dichiarazione d'intenti; con questo strato ogni feature successiva sa
esattamente cosa deve produrre. Dipende da US1 perché un KPI senza domanda riformulata non è
verificabile.

**Independent Test**: si prende ogni KPI del documento e si verifica che due persone diverse,
leggendo solo la formula concettuale, descrivano lo stesso calcolo e la stessa granularità.

**Acceptance Scenarios**:

1. **Given** il documento, **When** si contano i KPI, **Then** ce ne sono tra 2 e 3 per ciascuna
   delle tre domande di business, per un totale compreso tra 6 e 9.
2. **Given** un qualsiasi KPI del documento, **When** lo si esamina, **Then** riporta nome, cosa
   misura, formula concettuale, unità di misura, granularità e direzione di lettura (valore alto
   = meglio, oppure il contrario).
3. **Given** un qualsiasi KPI del documento, **When** si cerca a quale domanda risponde, **Then**
   è associato a **esattamente una** delle tre domande di business.
4. **Given** la formula concettuale di un KPI, **When** la si legge, **Then** non contiene
   sintassi DAX, SQL, Python o riferimenti a nomi di colonna fisici dei dataset.

---

### User Story 3 - Chi legge un numero sa quanto fidarsi (Priority: P3)

Qualsiasi lettore, davanti a un KPI del framework, capisce da dove verrà il numero (dato reale
Netflix, dato reale Spotify, dato sintetico, o derivato) e quanto è affidabile, con la regola
esplicita che i KPI a bassa confidenza saranno presentati come range best/base/worst e mai come
valore puntuale.

**Why this priority**: è il principio I della constitution reso operativo già in fase di
definizione, prima che un solo numero venga calcolato. Vale P3 perché è uno strato di qualità che
si applica a KPI già definiti (US2), ma è non negoziabile prima che il progetto passi alla fase di
implementazione.

**Independent Test**: si estrae la tabella provenienza/confidenza e si verifica che ogni KPI
definito in US2 compaia esattamente una volta, con fonte e confidenza compilate e con il formato
di presentazione coerente con il livello di confidenza dichiarato.

**Acceptance Scenarios**:

1. **Given** il documento, **When** si cerca la scala di confidenza, **Then** i tre livelli
   (alto / medio / basso) sono definiti con criteri di attribuzione espliciti e verificabili, non
   soggettivi.
2. **Given** ogni KPI del framework, **When** se ne verifica la classificazione, **Then** ha una
   fonte dichiarata tra `Netflix (reale)`, `Spotify (reale)`, `Sintetico`, `Derivato` (con le
   fonti a monte elencate) e un livello di confidenza dichiarato.
3. **Given** un KPI classificato a confidenza `bassa`, **When** se ne legge il formato di
   presentazione previsto, **Then** è dichiarato come range best/base/worst, mai come valore
   puntuale.
4. **Given** l'assunzione strutturale che Netflix è proxy del catalogo StreamWave e Spotify è
   proxy del mercato musicale, **When** si legge il documento, **Then** l'assunzione è dichiarata
   in modo visibile e non solo in nota tecnica.

---

### Edge Cases

- **Un KPI si rivela non calcolabile con i dati disponibili.** Il documento deve poter dichiarare
  un KPI come "desiderabile ma non calcolabile con i dati attuali" invece di ometterlo in
  silenzio: l'assenza di un dato è essa stessa un risultato per il board.
- **Una domanda di business richiede dati comportamentali che non esistono.** Nessuno dei due
  dataset contiene comportamento utente (visioni, ascolti, sessioni, abbonamenti). I KPI di
  engagement devono quindi poggiare su dati sintetici dichiarati, e il documento deve dirlo prima
  di proporre il KPI, non dopo.
- **Tutti i KPI di BQ3 finiscono a confidenza bassa.** È l'esito atteso, non un fallimento: il
  documento deve rendere leggibile il fatto che la terza domanda è strutturalmente più incerta
  delle prime due, invece di gonfiare artificialmente la confidenza per uniformità estetica.
- **Due KPI di domande diverse misurano la stessa cosa.** Serve una regola di disambiguazione: un
  KPI appartiene a una sola domanda; se è utile a due, va scelta la domanda primaria e citato come
  riferimento nell'altra.
- **Il proxy salta.** Se un attributo dei dataset reali non è un proxy credibile del fenomeno di
  business (es. `popularity` Spotify usato come proxy di ricavo), il documento deve dichiararlo
  come limite invece di trattarlo come misura diretta.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Il documento MUST essere prodotto come singolo file Markdown in
  `docs/business_case.md`, leggibile senza strumenti diversi da un lettore Markdown.
- **FR-002**: Il documento MUST aprirsi con l'inquadramento della decisione: chi è StreamWave,
  quale scelta strategica è in valutazione, chi è il destinatario del documento.
- **FR-003**: Il documento MUST riportare le tre domande di business nella loro formulazione
  originale e, per ciascuna, una riformulazione misurabile che espliciti soggetto, unità di misura
  e criterio di confronto o soglia.
- **FR-004**: Il documento MUST definire da 2 a 3 KPI per ciascuna domanda di business, per un
  totale compreso tra 6 e 9 KPI.
- **FR-005**: Ogni KPI MUST riportare: identificativo univoco, nome, cosa misura, formula
  concettuale, unità di misura, granularità e direzione di lettura.
- **FR-006**: Ogni KPI MUST essere associato a esattamente una delle tre domande di business.
- **FR-007**: Le formule dei KPI MUST essere espresse in forma concettuale; NON DEVONO contenere
  DAX, SQL, Python, né nomi fisici di colonna dei dataset di origine.
- **FR-008**: Il documento MUST definire **una sola** North Star metric, con la motivazione della
  scelta e almeno due alternative considerate e scartate, con il perché.
- **FR-009**: Il documento MUST definire la scala di confidenza (alto / medio / basso) con criteri
  di attribuzione espliciti, applicabili da un terzo senza interpretazione soggettiva.
- **FR-010**: Ogni KPI MUST dichiarare la propria fonte dati tra `Netflix (reale)`,
  `Spotify (reale)`, `Sintetico` e `Derivato`; per i KPI derivati MUST elencare le fonti a monte.
- **FR-011**: Ogni KPI classificato a confidenza `bassa` MUST dichiarare che sarà presentato come
  range best/base/worst; nessun KPI a bassa confidenza può prevedere un valore puntuale.
- **FR-012**: Il documento MUST contenere una sezione "Out of Scope" con almeno cinque domande o
  analisi escluse, ciascuna con la motivazione dell'esclusione.
- **FR-013**: Il documento MUST dichiarare in modo visibile l'assunzione strutturale che il
  catalogo Netflix è usato come proxy del catalogo StreamWave e il dataset Spotify come proxy del
  mercato musicale, con i limiti che ne derivano.
- **FR-014**: Il documento MUST elencare le assunzioni di business su cui poggeranno le stime
  della terza domanda (modello di ricavo, base utenti, orizzonte temporale), ciascuna marcata come
  assunzione e non come dato.
- **FR-015**: Il documento MUST dichiarare la copertura temporale dei dati reali e le conclusioni
  che tale copertura impedisce di trarre.
- **FR-016**: Il documento NON DEVE contenere numeri di risultato, stime calcolate o conclusioni
  analitiche: definisce cosa si misurerà e come si giudicherà, non l'esito della misura.
- **FR-017**: Il documento MUST dichiarare come assunzione il modello di ricavo a **due tier**:
  abbonamento base solo video, più un tier premium a prezzo superiore che include il verticale
  musicale. La dichiarazione MUST includere la struttura di prezzo ipotizzata, la ragione della
  scelta e il fatto che si tratta di un'assunzione di scenario, non di un dato.
- **FR-018**: I KPI di revenue della terza domanda MUST derivare dal modello a due tier, ossia
  misurare l'adozione del tier premium e l'effetto sul ricavo medio per utente; NON DEVONO
  presupporre ricavi pubblicitari né una riduzione di churn, entrambi fuori dal modello assunto.

### Key Entities

- **Domanda di business (BQ)**: unità di indagine del progetto. Attributi: identificativo (BQ1,
  BQ2, BQ3), formulazione originale, riformulazione misurabile, KPI associati. Sono tre e sono
  fissate dalla constitution.
- **KPI**: misura definita concettualmente. Attributi: identificativo, nome, descrizione, formula
  concettuale, unità, granularità, direzione di lettura, domanda di business di appartenenza,
  fonte, livello di confidenza, formato di presentazione. Relazione: molti KPI → una BQ.
- **North Star metric**: KPI singolo elevato a criterio sintetico di successo dell'iniziativa. È
  uno e uno solo, e può coincidere con uno dei KPI del framework o esserne una composizione.
- **Fonte dati**: origine di un valore. Valori ammessi: `Netflix (reale)`, `Spotify (reale)`,
  `Sintetico`, `Derivato`. Un valore derivato referenzia le fonti a monte.
- **Livello di confidenza**: `alto`, `medio`, `basso`. Determina il formato di presentazione
  obbligatorio del KPI (valore puntuale ammesso solo sopra la confidenza bassa).
- **Assunzione**: ipotesi dichiarata non verificabile con i dati disponibili. Attributi:
  enunciato, ambito di impatto, KPI che ne dipendono.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un lettore esterno al progetto, dopo una lettura di 15 minuti, sa riformulare la
  decisione in gioco, la North Star metric e almeno due esclusioni di perimetro senza consultare
  altre fonti.
- **SC-002**: Il 100% dei KPI definiti è riconducibile a esattamente una delle tre domande di
  business; nessun KPI risulta orfano o assegnato a due domande.
- **SC-003**: Il 100% dei KPI dichiara fonte e livello di confidenza.
- **SC-004**: Il 100% dei KPI classificati a confidenza bassa prevede una presentazione a range
  best/base/worst; zero KPI a bassa confidenza prevedono un valore puntuale.
- **SC-005**: Due lettori indipendenti, leggendo la stessa formula concettuale, descrivono lo
  stesso calcolo e la stessa granularità per almeno l'80% dei KPI; le divergenze residue sono
  registrate come punti da chiarire nella feature successiva.
- **SC-006**: Il documento contiene tra 6 e 9 KPI, una sola North Star metric e almeno cinque voci
  fuori scope motivate.
- **SC-007**: Zero risultati numerici o conclusioni analitiche compaiono nel documento: una
  rilettura mirata non trova stime, percentuali di esito o affermazioni sull'opportunità
  dell'espansione.
- **SC-008**: Ogni feature successiva del progetto può citare un identificativo di KPI di questo
  documento come proprio riferimento, senza doverne ridefinire la semantica.

## Assumptions

- **Destinatario**: il documento si rivolge a un board fittizio di StreamWave. Il registro è
  quello di una presentazione executive: nessuna competenza tecnica presupposta.
- **Proxy dei dati**: il catalogo Netflix rappresenta il catalogo attuale di StreamWave; il
  dataset Spotify rappresenta il mercato musicale accessibile. È l'assunzione strutturale del case
  study, dichiarata nella constitution.
- **Nessun dato comportamentale reale**: né visioni, né ascolti, né abbonamenti, né ricavi reali
  esistono. Ogni KPI di engagement o revenue poggerà su dati sintetici generati in una feature
  successiva.
- **Perimetro geografico**: globale, coerentemente con la copertura dei due dataset. Nessuna
  analisi per singolo mercato nazionale.
- **Modello di ricavo**: due tier — abbonamento base solo video e tier premium, a prezzo
  superiore, che include la musica. Scelto perché è il pattern prevalente quando una piattaforma
  video aggiunge un verticale adiacente, e perché rende l'impatto economico misurabile con due sole
  leve (tasso di adozione del premium e differenziale di prezzo) invece che con una catena di
  assunzioni comportamentali. Restano fuori dal modello i ricavi pubblicitari e gli effetti su
  churn: se emergessero come rilevanti, andrebbero trattati come estensione dichiarata, non
  assorbiti in silenzio nelle stime.
- **Orizzonte temporale delle stime**: 12 mesi dal lancio ipotetico del verticale musicale.
  Orizzonte scelto perché compatibile con la granularità delle assunzioni disponibili; oltre i 12
  mesi la confidenza degraderebbe al punto da rendere la stima non informativa.
- **Copertura del dato reale**: il catalogo Netflix si ferma al 2021 e il dataset Spotify al 2022.
  Il documento non può fondare conclusioni su trend successivi a tali date.
- **Definizione di engagement**: tempo di fruizione per utente attivo mensile, salvo diversa
  definizione introdotta dai KPI di BQ1. Assunzione adottata perché è la metrica di riferimento
  comune del settore streaming e permette il confronto tra verticale video e verticale musicale.
- **Questa feature non produce codice**: nessuno script, nessuna misura DAX, nessuna
  trasformazione dati. Il principio II della constitution (riproducibilità) si applica quindi alle
  feature successive; qui vale il principio VI (coerenza narrativa) come vincolo primario.

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: BQ1, BQ2 e BQ3 — tutte e tre.
- **Contributo**: questa è la feature fondativa del progetto. Non risponde a nessuna delle tre
  domande: le rende **rispondibili**, traducendo ciascuna in una forma misurabile e nel set di KPI
  che le feature successive dovranno calcolare. È l'unica feature del progetto autorizzata a
  toccare tutte e tre le domande insieme, perché il suo oggetto è il framework, non la risposta.

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

Questa feature **non produce alcun numero**: produce le definizioni con cui i numeri verranno
prodotti e classificati. Non esiste quindi una metrica da etichettare qui. La tabella sotto
dichiara invece la provenienza attesa che il documento dovrà assegnare a ciascuna famiglia di KPI,
e vincola le feature successive.

| Famiglia di KPI | Fonte attesa | Confidenza attesa | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| Caratteristiche del catalogo video (BQ1) | Netflix (reale) | alto | dato osservato direttamente nel dataset, nessuna inferenza | valore singolo |
| Caratteristiche del catalogo musicale (BQ1) | Spotify (reale) | alto | dato osservato direttamente nel dataset, nessuna inferenza | valore singolo |
| Confronto e overlap video/musica (BQ1) | Derivato (Netflix + Spotify) | medio | dato reale su entrambi i lati, ma il confronto richiede una mappatura interpretativa tra domini diversi | valore singolo con nota metodologica |
| Coerenza segmento musicale ↔ catalogo (BQ2) | Derivato (Netflix + Spotify) | medio | dato reale, ma la nozione di "coerenza" è una costruzione dell'analista | valore singolo con nota metodologica |
| Dimensionamento del segmento (BQ2) | Spotify (reale) | medio | il dataset è un campione del mercato, non il mercato | valore singolo con nota metodologica |
| Engagement stimato (BQ3) | Sintetico | basso | nessun dato comportamentale reale esiste; il valore dipende interamente da assunzioni | range best/base/worst |
| Revenue stimata (BQ3) | Sintetico | basso | nessun dato economico reale esiste; il valore dipende interamente da assunzioni | range best/base/worst |

**Assunzioni dietro i dati sintetici**: nessun dato sintetico viene generato in questa feature. Le
assunzioni che ne governeranno la generazione (modello di ricavo, base utenti, orizzonte a 12 mesi)
sono dichiarate nella sezione Assumptions e saranno vincolanti per la feature di generazione.

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: nessuna delle tre domande di business. Questa feature definisce come si
  risponderà, non risponde. Chi cerca qui una raccomandazione sull'espansione non la troverà, e
  questo è deliberato.
- **Non risponde a**: quanto costa costruire il verticale musicale. Nessun dato di costo, licenze
  musicali, infrastruttura o organico è disponibile, e senza il lato costi il documento non è un
  business case finanziario completo — è un business case di opportunità.
- **Non risponde a**: se il pubblico reale di StreamWave vorrebbe la musica. Nessun dato
  comportamentale, di survey o di churn esiste. L'overlap di audience che BQ1 esplora è un overlap
  **di caratteristiche di contenuto**, non di persone osservate.
- **Inferenza da evitare**: che i KPI qui definiti, una volta calcolati, dimostreranno la
  convenienza dell'espansione. Il framework è costruito per poter produrre anche una risposta
  negativa, ed è esplicitamente progettato per non impedirla.
- **Inferenza da evitare**: che la somiglianza tra un genere musicale e un genere video implichi
  trasferibilità di pubblico. È una correlazione tra attributi di catalogo, non una relazione
  causale sul comportamento delle persone.
- **Non risponde a**: quale sarebbe il prezzo ottimale del tier premium. Il modello a due tier è
  uno scenario assunto, non il risultato di un'analisi di pricing: senza dati di elasticità della
  domanda, ogni prezzo indicato è un'ipotesi di lavoro e va letto come tale.
- **Copertura del dato**: catalogo Netflix fermo al 2021, tracce Spotify ferme al 2022. Il
  documento non può fondare alcuna conclusione su dinamiche di mercato successive, incluse le
  evoluzioni del settore musicale degli ultimi anni.
- **Dove è esposto all'utente finale**: il documento contiene una sezione "Out of Scope" dedicata,
  e ogni KPI a confidenza bassa porta il limite nella propria riga di definizione. Il limite non
  vive solo in questa spec: viaggia con il documento.
