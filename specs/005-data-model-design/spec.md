# Feature Specification: Data Model Design

**Feature Branch**: `005-data-model-design`

**Created**: 2026-08-17

**Status**: Draft

**Input**: disegnare il modello dati su cui la `007` scriverà le misure DAX e la `008` costruirà la dashboard, a partire dai quattro dataset di `data/processed/`, chiudendo i debiti `R4`/divergenza 1 e `R7`/divergenza 7 della revisione della `001`.

---

## Che cosa questa feature produce, in una frase

Un **modello dati progettato e non materializzato**: un documento versionato che dichiara quali tabelle esistono, a quale grana, con quali chiavi, con quali relazioni e in quale direzione filtrano, e da quale campo di quale dataset ogni colonna proviene — abbastanza perché la `007` possa scrivere una misura senza riaprire il codice della pipeline, e la `008` possa costruire il report senza reinventare i nomi.

Non produce misure, non produce la tabella di corrispondenza dei mood, non produce alcun file `.pbix`.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — L'ossatura del modello: grane, chiavi, relazioni, direzioni di filtro (Priority: P1)

Chi scriverà le misure della `007` deve sapere, prima di scrivere una riga di DAX, su quale tabella un conteggio è corretto e su quale è gonfiato. Oggi quell'informazione esiste soltanto come **regola di lettura in prosa** dentro il contratto della `003` — «i due dataset musicali non sono intercambiabili» — e come **nota metodologica** in §5.2 del business case, che presenta due granularità dove ne servono tre. Questa storia trasforma quella prosa in una struttura: tabelle con una grana dichiarata, chiavi che la rendono verificabile, relazioni che rendono *impossibile* la giunzione sbagliata invece di limitarsi a sconsigliarla.

**Why this priority**: è l'unica parte del lavoro che ha valore dimostrabile da sola. Un modello con grane, chiavi e direzioni di filtro dichiarate è già sufficiente a scrivere e verificare la struttura di una misura; un modello con i soli nomi e mapping non lo è. È anche la parte che chiude i due debiti ereditati, che sono entrambi debiti di grana.

**Independent Test**: si prende ciascuno degli 8 KPI del business case e si verifica che il documento permetta di rispondere a tre domande senza consultare altro — su quale tabella la misura si calcola, a che cosa si riferisce il numero che produce, e quale giunzione produrrebbe invece un numero sbagliato. Se anche un solo KPI lascia una delle tre senza risposta, la storia non è completa.

**Acceptance Scenarios**:

1. **Given** il documento del modello e nessun altro artefatto, **When** un lettore cerca su quale tabella si calcola un totale del catalogo musicale, **Then** trova la tabella alla grana traccia e la dichiarazione esplicita che la tabella alla grana coppia restituirebbe un valore diverso e sbagliato per quello scopo.
2. **Given** il documento del modello, **When** un lettore cerca la grana di `BQ2-K2`, **Then** trova dichiarate separatamente la grana su cui la misura opera e la grana a cui il suo risultato si riferisce, e trova detto che le due non coincidono.
3. **Given** il documento del modello, **When** un lettore cerca che cosa sia un «segmento», **Then** trova una definizione operativa univoca che nomina il campo di provenienza, e non una barra fra due nozioni.
4. **Given** il modello, **When** si costruisce il denominatore di `BQ1-K1`, **Then** la struttura dichiarata rende il conteggio dei titoli distinti l'unico calcolo possibile su quella tabella, e il conteggio delle assegnazioni di categoria un calcolo che vive su una tabella diversa e porta un nome diverso.

---

### User Story 2 — Il mapping dei campi: da quale colonna di quale dataset viene ogni cosa (Priority: P2)

Chi costruirà il modello davanti allo schermo, e chi vorrà contestare un numero a valle, deve poter risalire da ogni colonna del modello al campo del dataset che la produce, e alle trasformazioni interposte. Alcune colonne sono lette e basta; altre sono derivate dentro il modello — e il confine fra le due è precisamente ciò che il principio I chiede di rendere leggibile.

**Why this priority**: senza l'ossatura della `US1` il mapping non ha su cosa atterrare, quindi viene dopo. Ma è la storia che contiene le due decisioni di sostanza che il modello non può rinviare: quale campo del catalogo musicale realizza ciascuno dei tre assi di mood di §5.3, e da quale tabella la misura di popolarità legge il proprio valore quando le due tabelle musicali non concordano.

**Independent Test**: per ogni colonna del modello, il documento dichiara dataset di origine, campo di origine e regola di derivazione dove ce n'è una. Si verifica per campionamento incrociando con il contratto della `003`: una colonna che il contratto non descrive, o che descrive con un altro nome, è un difetto.

**Acceptance Scenarios**:

1. **Given** il documento, **When** si cerca da dove viene l'asse «ritmo» di §5.3, **Then** si trova il campo nominato, la scala su cui vive, e la ragione per cui il campo alternativo è stato scartato.
2. **Given** il documento, **When** si cerca il valore di popolarità che alimenta `BQ2-K1`, **Then** si trova dichiarato da quale delle due tabelle musicali viene letto e che cosa cambierebbe leggendolo dall'altra.
3. **Given** una colonna derivata dentro il modello, **When** si cerca come è costruita, **Then** si trova la regola in forma riproducibile e la dichiarazione che non è un campo di origine.

---

### User Story 3 — I posti vuoti: che cosa la `006` riempirà e con quale contratto (Priority: P3)

Tre KPI su otto — `BQ1-K3`, `BQ2-K2`, `BQ2-K3` — non esistono senza il profilo di mood del lato video, che questa feature **non costruisce**. Il modello deve però dichiarare la forma esatta della tabella che lo ospiterà: chiave, colonne, scala, cardinalità attesa e direzione della relazione. La `006` la riempie; nessuno la ridisegna.

**Why this priority**: è la storia che protegge la dipendenza dichiarata in roadmap — `006` dipende da `005` — dal rovesciarsi durante l'esecuzione. Senza questo contratto, la `006` costruirebbe una tabella e la `005` scoprirebbe di doverla riprogettare.

**Independent Test**: si verifica che il documento dichiari la forma della tabella di corrispondenza senza dichiararne alcun contenuto, e che la decisione aperta `DA-1` della roadmap non risulti né risolta né toccata.

**Acceptance Scenarios**:

1. **Given** il documento, **When** si cerca la tabella del profilo di mood video, **Then** se ne trova la forma e la dichiarazione esplicita che le sue righe non esistono ancora e sono di competenza della `006`.
2. **Given** il documento, **When** si cerca un criterio con cui una categoria video verrebbe associata a un profilo, **Then** non lo si trova, e si trova detto che quel criterio appartiene alla `006`.

---

### Edge Cases

- **Una traccia appartiene a più segmenti.** Ogni conteggio deve dichiarare se la conta una volta o una per segmento. È l'errore che la regola di lettura del contratto della `003` esiste per prevenire, e il modello deve renderlo strutturalmente difficile invece di sconsigliarlo a parole.
- **Una traccia porta due valori di popolarità diversi nelle due tabelle musicali.** Accade sulle tracce marcate `has_conflicting_popularity`. Il modello deve dichiarare quale valore alimenta la misura, perché altrimenti il numero dipende dalla tabella che chi scrive la misura ha scelto per caso.
- **Un titolo video appartiene a più categorie.** Il denominatore di `BQ1-K1` è il conteggio dei titoli distinti, non delle assegnazioni: la struttura deve rendere le due cose due misure distinte con due nomi distinti.
- **Un segmento concentra una quota alta di popolarità nulla.** 7 segmenti superano la soglia della decisione `D4` della `003`. La marcatura deve arrivare fino alla misura, perché la divergenza 6 della revisione della `001` obbliga la `007` a pubblicare la quota di zeri accanto a `BQ2-K1`.
- **Una traccia ha durata degenere.** Il modello deve trasportare la marcatura `is_duration_zero` fino alla misura di `BQ1-K2`, senza decidere al posto della `007` se quelle righe entrino nella mediana.
- **Un campo esiste in due tabelle con lo stesso nome e valore diverso.** È il caso della popolarità. Il modello deve impedire che due misure leggano lo stesso nome intendendo due cose.

---

## Requirements *(mandatory)*

### Requisiti sul deliverable

- **FR-001**: la feature DEVE produrre `docs/data_model.md`, documento versionato che descrive il modello per intero. Il modello NON DEVE esistere solo dentro un file binario: è l'obbligo esplicito del principio V, che nomina lo schema del modello dati e il mapping dei campi fra le cose che DEVONO essere artefatto testuale.
- **FR-002**: il documento DEVE reggersi da solo. Un lettore che possieda `docs/data_model.md`, `docs/business_case.md` e il contratto degli output della `003` DEVE poter costruire il modello senza aprire alcuna cartella sotto `specs/` e senza leggere il codice della pipeline.
- **FR-003**: il documento DEVE dichiarare in apertura che il modello è **progettato e non materializzato**, e che nessuna sua affermazione è stata verificata eseguendola in uno strumento.
- **FR-004**: ogni numerale del documento DEVE portare l'ancora al valore che lo produce oppure il marcatore di non-misurato, secondo la grammatica di `docs/convenzioni-marcatura.md`. Il documento DEVE essere registrato in `scripts/check_audit_coherence.py` sotto **severità stretta**, come i due documenti nuovi che l'hanno preceduto.
- **FR-005**: la feature NON DEVE modificare `scripts/build_datasets.py`, i quattro dataset di output, né alcun artefatto sotto `reports/`. Se il modello richiede una trasformazione che la pipeline non produce, quella trasformazione è o una **derivazione interna al modello** — ammessa, e da dichiarare come tale — oppure un **ritrovamento** da registrare per la regia.

### Requisiti sulla struttura

- **FR-006**: il documento DEVE elencare ogni tabella del modello con: nome, ruolo (dimensione, fatto, ponte, tabella di appoggio), **grana dichiarata in una frase che dica che cosa è una riga**, chiave, cardinalità attesa e dataset di provenienza.
- **FR-007**: ogni relazione DEVE dichiarare le due tabelle, le colonne su cui poggia, la cardinalità, la **direzione di filtro** e la ragione della direzione scelta.
- **FR-008**: il modello DEVE distinguere **tre** nozioni di grana, e ogni KPI del framework DEVE dichiararle tutte e tre:
  1. **grana di appartenenza** — quale riga stabilisce che un elemento appartiene a un insieme;
  2. **grana di calcolo** — su quali righe l'aggregazione opera;
  3. **grana del risultato** — a che cosa si riferisce un numero pubblicato.
- **FR-009**: il documento DEVE contenere una tabella che, per ciascuno degli 8 KPI, dichiari le tre grane, le tabelle coinvolte e la giunzione che produrrebbe un valore sbagliato. La colonna sull'errore NON è ornamentale: è ciò che rende la regola di lettura della `003` verificabile invece che raccomandata.
- **FR-010**: il modello NON DEVE ammettere che uno stesso conteggio sia calcolabile su due tabelle diverse con due risultati diversi senza che i due risultati portino nomi diversi.

### Requisiti sulle decisioni ereditate

- **FR-011**: il documento DEVE dichiarare la **definizione operativa di «segmento»**, nominando il campo di provenienza, e DEVE dichiarare che cosa la definizione adottata rende impossibile misurare. Chiude `R4` e la divergenza 1 della revisione della `001`.
- **FR-012**: il documento DEVE dichiarare l'alternativa scartata nella definizione di «segmento» e la ragione del rigetto, incluse le conseguenze che la lettura scartata avrebbe avuto sulla confidenza dei KPI di BQ2.
- **FR-013**: la feature DEVE aggiungere una **nota in loco** a §5.2 di `docs/business_case.md` che riformuli l'insufficienza delle due granularità, secondo la prassi di correzione degli artefatti già mergiati: il testo originale resta, la nota sta accanto e dichiara data, feature, affermazione precedente, affermazione corretta, causa e fonte verificabile. Chiude `R7` e la divergenza 7.
- **FR-014**: la nota di `FR-013` DEVE coprire entrambi i casi che la revisione della `001` aveva sollevato: la granularità ibrida dichiarata da `BQ2-K1` e lo scarto fra grana dichiarata e grana del risultato in `BQ2-K2`.
- **FR-015**: la feature DEVE aggiungere una **nota in loco** a §4 (BQ2) di `docs/business_case.md` che dichiari come la barra «genere/mood» è stata sciolta e che il mood resta nel framework come **attributo con cui i segmenti si confrontano**, non come criterio con cui si formano.
- **FR-016**: il documento DEVE registrare la **divergenza 1 della revisione della `003`** — a quale precisione si confrontano profilo e rendiconto — come **vincolo ereditato dalla `007`**, senza deciderlo. Se il modello obbliga a fissare una precisione su una colonna, il documento DEVE dichiarare che quella scelta è di tipo di dato e non risolve la divergenza, che riguarda il criterio di confronto.
- **FR-017**: il documento NON DEVE risolvere né toccare la decisione aperta `DA-1` della roadmap.

### Requisiti sul mapping dei campi

- **FR-018**: ogni colonna del modello DEVE dichiarare dataset di origine, campo di origine, tipo e — dove non è una lettura diretta — la **regola di derivazione** in forma riproducibile.
- **FR-019**: il documento DEVE dichiarare quale campo del catalogo musicale realizza ciascuno dei **tre assi di mood** di §5.3 del business case, con la scala su cui il campo vive e la ragione per cui l'alternativa è stata scartata.
- **FR-020**: il documento DEVE dichiarare da quale delle due tabelle musicali la misura di popolarità legge il proprio valore, e che cosa cambierebbe leggendolo dall'altra, citando la marcatura che il contratto della `003` fornisce per riconoscere i casi discordi.
- **FR-021**: dove due unità di misura devono essere confrontate — è il caso di `BQ1-K2`, minuti contro millisecondi — il modello DEVE dichiarare dove avviene la conversione e con quale regola, e NON DEVE fissare arrotondamenti: l'arrotondamento è una decisione di presentazione e appartiene alla `007`.
- **FR-022**: le marcature prodotte dalla `003` che condizionano una misura — almeno `is_popularity_zero`, `is_high_zero_genre`, `is_duration_zero`, `has_conflicting_popularity`, `is_repaired_duration` — DEVONO essere collocate nel modello alla grana di cui sono proprietà, e il documento DEVE dichiarare quale misura ciascuna condiziona.
- **FR-023**: il modello DEVE rendere calcolabile la **quota di popolarità nulla per segmento**, perché la divergenza 6 della revisione della `001` obbliga la `007` a pubblicarla accanto a `BQ2-K1`. Il modello espone la struttura; la misura resta della `007`.

### Requisiti sul naming e sulla presentazione

- **FR-024**: il documento DEVE dichiarare la convenzione di naming di tabelle, colonne e misure. I nomi sono in **inglese**, per la convenzione di progetto; la prosa del documento è in **italiano**.
- **FR-025**: i nomi delle misure DEVONO essere i **nomi semantici** già pubblicati in §5.4 del business case. §5.1 dichiara che il nome semantico «è quello che diventerà il nome della misura nel modello dati»: è un impegno già preso, e il modello lo onora invece di inventare una convenzione nuova.
- **FR-026**: il documento DEVE dichiarare quali colonne sono **nascoste** al lettore del report e perché. Una colonna tecnica visibile in un elenco di campi è un invito a costruirci sopra una misura sbagliata.
- **FR-027**: il documento DEVE dichiarare se il modello prevede una **tabella calendario** e, in caso negativo, la ragione — che è essa stessa una decisione di modello e non un'omissione.

### Requisiti sui posti che questa feature non riempie

- **FR-028**: il documento DEVE dichiarare la forma della tabella che ospiterà il **profilo di mood del lato video**: chiave, colonne, scala, cardinalità attesa, direzione della relazione. NON DEVE dichiararne alcuna riga.
- **FR-029**: il documento DEVE dichiarare che i sei valori di scenario della `004` **non sono un fatto del modello** e che il modo in cui entrano nel report è una decisione della `007` o della `008`, non di questa feature.
- **FR-030**: il documento DEVE elencare i **vincoli che le feature a valle ereditano** da questo modello, ciascuno con la feature a cui è assegnato.

### Requisiti sul drift documentale

- **FR-031**: la feature DEVE chiudere il proprio drift sul [README](../../README.md): riga nella tabella di stato con il collegamento al proprio verbale di revisione, deliverable elencato, prosa dei deliverable estesa, sezioni `Setup` e `Struttura` allineate a ciò che la feature aggiunge.
- **FR-032**: la feature DEVE produrre `specs/005-data-model-design/review.md`, verbale di una revisione in contesto pulito, secondo i quattro obblighi di [`CLAUDE.md`](../../CLAUDE.md#la-revisione-in-contesto-pulito).

### Key Entities

Le entità sono le tabelle del modello. Nomi e composizione esatta sono l'esito della feature; questo elenco fissa che cosa il modello deve contenere, non ancora come.

- **Titolo video** — una riga per titolo del catalogo video. È la tabella su cui si contano i titoli e su cui si misura la durata dei film.
- **Assegnazione titolo-categoria** — una riga per ogni accoppiamento fra un titolo e una delle categorie che gli sono state assegnate. Non è una tabella di titoli e non va contata come tale.
- **Categoria video** — una riga per categoria. Non è uno dei quattro dataset: è derivata, e la derivazione va dichiarata.
- **Profilo di mood della categoria video** — una riga per categoria, con il profilo atteso sui tre assi. **Forma dichiarata qui, righe prodotte dalla `006`.**
- **Traccia musicale** — una riga per traccia, indipendentemente dai segmenti a cui appartiene. È la tabella su cui si calcolano i totali del catalogo musicale e le misure di mood alla grana traccia.
- **Appartenenza traccia-segmento** — una riga per ogni accoppiamento fra una traccia e un segmento. È la tabella su cui si calcola qualunque cosa *per segmento*.
- **Segmento** — una riga per segmento, con gli attributi che sono proprietà del segmento e non della coppia.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: per tutti e 8 i KPI del business case, il documento dichiara le tre grane, le tabelle coinvolte e la giunzione errata. Copertura richiesta: **8 su 8**. Un KPI scoperto è un KPI che la `007` dovrà progettare da sé.
- **SC-002**: ogni colonna del modello ha dataset di origine e campo di origine dichiarati, oppure una regola di derivazione. Copertura richiesta: **totale**. Una colonna senza provenienza è un numero senza fonte al momento in cui una misura la legge.
- **SC-003**: un lettore che non conosca il progetto, avendo in mano il solo `docs/data_model.md`, risponde correttamente a queste tre domande: che cosa è un segmento; su quale tabella si conta il catalogo musicale; perché la tabella alla grana coppia darebbe un valore diverso. È la prova che la revisione in contesto pulito esegue.
- **SC-004**: `scripts/check_audit_coherence.py` termina con esito positivo su `docs/data_model.md` sotto severità stretta, e continua a terminare con esito positivo su tutti i documenti già registrati.
- **SC-005**: i due debiti ereditati risultano chiusi in modo verificabile — una definizione operativa di «segmento» esiste e ne esiste una sola; §5.2 del business case porta una nota che distingue la grana dell'ingresso da quella del risultato.
- **SC-006**: nessun artefatto della feature contiene una misura DAX, una riga della tabella di corrispondenza dei mood, o un riferimento a un file `.pbix` prodotto.

---

## Assumptions

- **I quattro dataset di `data/processed/` sono descritti fedelmente dal contratto della `003`.** La feature progetta sul contratto e non sui file, che non sono versionati. È il modo di lavorare che quel contratto è stato scritto per abilitare, ed è anche il suo limite dichiarato: se contratto e pipeline divergessero, il modello erediterebbe la divergenza. Il contratto dichiara che in quel caso è il contratto a essere sbagliato.
- **Lo strumento di destinazione è Power BI Desktop.** Il modello è disegnato per un motore tabellare a schema a stella con relazioni dichiarate e direzioni di filtro. La scelta è già fissata dalla roadmap e dalla constitution, che nomina Power BI Desktop come strumento di presentazione a interazione manuale.
- **Il modello è progettato prima di essere materializzato.** Nessuna affermazione di questa feature è stata verificata eseguendola. È l'assunzione più esposta e ha una conseguenza che il punto di stop porta alla regia: se la `007` non può verificare una misura contro un modello che esiste solo come documento, la materializzazione è lavoro reale che oggi non appartiene ad alcuna feature.
- **L'assunzione strutturale A1 vale qui come ovunque.** Il catalogo Netflix è proxy del catalogo StreamWave, il catalogo Spotify è proxy del mercato musicale accessibile. Il modello descrive quindi due cataloghi proxy, e nessuna delle sue tabelle contiene un dato di StreamWave — che non esiste.
- **La tabella di corrispondenza dei mood è lato video.** §5.3 del business case dichiara che sul lato musicale i tre assi sono misurati direttamente e sul lato video sono assegnati tramite la tabella. La `006` costruisce quindi un artefatto sul lato video, e questa feature ne dichiara la forma senza dipendere dal suo contenuto.

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ1 — Posizionamento** e **BQ2 — Segmento di ingresso**.

- **Contributo**: il ponte va scritto e non dato per ovvio, perché un modello dati non risponde da sé a una domanda di business. Il contributo di questa feature è di **rendere le due domande calcolabili senza ambiguità residua sull'unità di analisi**, ed è di sostanza in tre punti precisi:

  **Su BQ2, il contributo è la domanda stessa.** BQ2 chiede quale *segmento* musicale rappresenti l'opportunità di ingresso più coerente. Finché «segmento» significa indifferentemente un genere della fonte o un raggruppamento per mood, la domanda non ha un soggetto: tre dei suoi KPI ordinano un insieme di oggetti di cui nessuno sa dire che cosa siano. Questa feature fissa l'unità di analisi, e con essa fissa che cosa BQ2 stia ordinando, quante voci abbia la graduatoria e a che cosa si riferisca ciascun numero. Senza questo passaggio la `007` produrrebbe numeri corretti su un insieme indefinito.

  **Su BQ1, il contributo è la commensurabilità.** BQ1 confronta due cataloghi che vivono in due dataset con unità diverse, grane diverse e tassonomie disgiunte. Il modello è il luogo in cui i due lati diventano confrontabili: dichiara su quale grana si misura ciascun lato, quale campo realizza ciascun asse comune, e dove avviene la conversione fra unità. Un confronto fra due grandezze non commensurate non è una misura debole, è una misura priva di significato.

  **Su entrambe, il contributo è la protezione del denominatore.** La struttura del modello è ciò che impedisce alle misure di BQ1 e BQ2 di contare più volte gli stessi oggetti. È il difetto che la `002` ha misurato sul dato di origine e che la `003` ha trasformato in due tabelle distinte; il modello è il terzo e ultimo punto in cui può essere reintrodotto, perché è dove qualcuno traccia una relazione fra le due.

  **Su BQ3 il contributo è nullo, e va detto.** I sei valori di scenario della `004` non sono un fatto di questo modello. Il modo in cui entrano nel report è una decisione a valle, dichiarata come vincolo ereditato e non risolta qui.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

Questa feature **non introduce alcuna metrica**: non calcola valori e non ne pubblica di nuovi. Introduce le **strutture** su cui i valori saranno calcolati, e la loro provenienza è dichiarata perché è ciò che determina la confidenza di ogni misura che vi poggerà.

| Struttura introdotta | Fonte | Confidenza della catena | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| Tabella dei titoli video | Netflix (reale) | **alta** | lettura diretta di `data/processed/netflix_titles.csv`, nessuna interpretazione interposta | struttura, non valore |
| Tabella delle assegnazioni titolo-categoria | Netflix (reale) | **alta** | normalizzazione di un campo multi-valore già eseguita e rendicontata dalla `003` | struttura, non valore |
| Tabella delle categorie video | Derivato (Netflix) | **alta** | elenco dei valori distinti di una colonna esistente; nessuna selezione né raggruppamento | struttura, non valore |
| Tabella delle tracce musicali | Spotify (reale) | **alta** | lettura diretta di `data/processed/spotify_tracks.csv` | struttura, non valore |
| Tabella delle appartenenze traccia-segmento | Spotify (reale) | **alta** | lettura diretta di `data/processed/spotify_track_genre.csv` | struttura, non valore |
| Tabella dei segmenti | Derivato (Spotify) | **alta** | elenco dei valori distinti del campo che definisce il segmento, più gli attributi che il contratto della `003` dichiara costanti entro il segmento | struttura, non valore |
| Colonne di conversione fra unità | Derivato (Spotify) | **alta** | conversione aritmetica esatta, senza arrotondamento e senza assunzione | struttura, non valore |
| Tabella del profilo di mood delle categorie video | Derivato (analista) | **media**, e non può salire | la tabella è costruita dall'analista, non osservata: è lo strato interpretativo che §5.3 del business case dichiara e che tiene `BQ1-K3`, `BQ2-K2` e `BQ2-K3` a confidenza media. **Questa feature ne dichiara la forma, non le righe** | struttura vuota, riempita dalla `006` |

**Perché il modello non innalza né abbassa alcuna confidenza.** La scala di §6 del business case misura quanti strati interpretativi separano il dato osservato dal numero mostrato. Una struttura non è uno strato: non trasforma un valore, dichiara dove vive. La sola eccezione è la tabella del profilo di mood video, che è essa stessa uno strato interpretativo — ed è la ragione per cui il modello la tiene in una tabella separata invece di aggiungerne le colonne alla dimensione osservata. **Fondere una dimensione osservata e una costruita in un'unica tabella nasconderebbe la giuntura**, che è precisamente ciò che il principio I chiede di rendere visibile.

**Effetto della decisione su «segmento» sulla confidenza già pubblicata**: la definizione adottata lascia `BQ2-K1` sulla riga `Spotify (reale)` e a confidenza media, come §5.4 del business case già dichiara. La lettura alternativa l'avrebbe portata a `Derivato` e avrebbe modificato la riga di fonte di un artefatto già mergiato. Non è la ragione principale del rigetto, ma va registrata perché è una conseguenza reale.

**Assunzioni dietro i dati sintetici**: nessun dato sintetico. Questa feature non ne genera e non ne consuma. I sei valori sintetici del progetto, prodotti dalla `004`, restano fuori dal modello — vedi `FR-029`.

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

Questa sezione dichiara **cosa il modello rende impossibile misurare**, non soltanto cosa abilita. È la parte che una feature di progettazione tende a saltare, perché ogni scelta di struttura è anche una porta chiusa, e le porte chiuse non si vedono guardando lo schema.

- **Non risponde a**: nessuna delle tre domande di business. Questa feature non produce alcun numero. Chi cercasse qui un valore di `BQ1-K1` o una graduatoria di segmenti non li troverà, ed è deliberato: le misure sono della `007`.

- **Non risponde a**: qualunque domanda su come i segmenti si raggrupperebbero in famiglie più larghe. La definizione operativa adottata fissa i segmenti sull'insieme dichiarato dalla fonte; qualunque macro-raggruppamento sarebbe un secondo strato interpretativo che questa feature non introduce e che nessuna feature possiede oggi.

- **Non risponde a**: qualunque domanda temporale. Il modello **non prevede una dimensione di calendario**, e questa è una decisione, non un'omissione. Nessuno degli 8 KPI del framework è definito su un asse temporale, e l'assunzione A2 del business case — copertura ferma al 2021 sul lato video e al 2022 sul lato musicale — insieme a §8 esclude esplicitamente ogni conclusione di tendenza. Una dimensione di calendario nel modello **abiliterebbe in dashboard esattamente le analisi che il business case vieta**, e le renderebbe costruibili con un trascinamento. L'assenza della tabella è la forma strutturale di un limite già dichiarato a parole.

- **Non risponde a**: la sovrapposizione fra i *pubblici* dei due cataloghi. Il modello mette in relazione due cataloghi attraverso attributi di contenuto. Non esiste in esso alcuna entità «persona», «visione» o «ascolto», perché nessuna delle due fonti la contiene. Nessuna relazione di questo modello, per quanto disegnata bene, potrà mai essere letta come una relazione fra spettatori e ascoltatori.

- **Inferenza da evitare**: che una relazione nel modello indichi una relazione nel mondo. Una relazione fra la tabella delle tracce e quella dei segmenti dichiara come i dati si giuntano, non che esista un legame causale o comportamentale fra le entità che rappresentano. Vale in particolare per la tabella che collegherà le categorie video ai profili di mood: è una corrispondenza costruita dall'analista fra due tassonomie disgiunte, non una somiglianza osservata.

- **Inferenza da evitare**: che un modello progettato sia un modello funzionante. Nessuna affermazione di questo documento è stata verificata eseguendola in Power BI. Una direzione di filtro dichiarata corretta potrebbe rivelarsi ambigua davanti allo schermo, e una grana dichiarata potrebbe non reggere una misura reale. È il limite più esposto della feature ed è la ragione della domanda che il punto di stop porta alla regia.

- **Inferenza da evitare**: che il modello garantisca la correttezza delle misure che vi poggeranno. Il modello rende **difficile** la giunzione sbagliata; non la rende impossibile. Una misura scritta contro la tabella giusta con la logica sbagliata produrrà un numero sbagliato, e nessuna struttura può accorgersene. Contro questo esistono la revisione in contesto pulito e la marcatura dei valori, non lo schema.

- **Copertura del dato**: catalogo video fermo al **2021**, catalogo musicale fermo al **2022**, per A2. Il modello descrive due fotografie e non ha alcun modo di rappresentare che siano di due momenti diversi — il che è coerente con l'assenza della dimensione di calendario, e va letto insieme ad essa.

- **Copertura del dato**: il catalogo musicale contiene lo stesso numero di tracce per ogni segmento **per costruzione del campione**. Ne discende un limite strutturale del modello: **qualunque misura costruita contando le righe di un segmento misura il campionamento, non il mercato.** Il modello non può impedirlo, perché contare righe è l'operazione più naturale che un motore tabellare offre. Il documento deve quindi dichiararlo, e la `007` deve tenerne conto.

- **Copertura del dato**: la marcatura `has_conflicting_popularity` della `003` segnala le tracce su cui le due tabelle musicali portano valori di popolarità diversi. La scelta della tabella da cui leggere, dichiarata da questa feature, determina il valore di quelle righe. Non esiste un valore «giusto»: la fonte ne portava due.

- **Copertura del dato**: gli assi di mood del lato musicale sono attributi **calcolati dalla fonte con un metodo che la fonte non pubblica in dettaglio**. «Misurati direttamente», come dice §5.3, significa che questo progetto li legge senza trasformarli — non che siano una misura fisica. È uno strato interpretativo che sta a monte del progetto e su cui il progetto non ha presa.

- **Dove è esposto all'utente finale**: nessuno di questi limiti è esposto in dashboard da questa feature, che non ne produce alcuna. Il modello li porta però alla `008` come vincoli ereditati, e in particolare l'assenza della dimensione di calendario e l'inutilizzabilità del conteggio di righe per dimensionare un segmento vanno esposte dove un lettore potrebbe costruirsi da sé la misura vietata.

---

## Decisioni

Le decisioni di merito che la feature prende. Sono elencate qui perché il primo punto di stop le porta alla regia prima che diventino un piano.

### D1 — Un «segmento» è un genere dichiarato dalla fonte musicale

Chiude `R4` e la divergenza 1 della revisione della `001`. Il segmento è il valore del campo `track_genre` del catalogo musicale; l'insieme dei segmenti è l'insieme dei suoi valori distinti. È la prima delle due letture che la barra «genere/mood» lasciava aperte.

Quattro ragioni, in ordine di forza:

1. **La lettura alternativa rende falsa una frase già pubblicata.** §5.2 del business case afferma che «il catalogo musicale assegna una traccia a più segmenti quando è pertinente a più d'uno». L'appartenenza multipla è una proprietà del campo dei generi — una traccia ne porta fino a nove — e non di un raggruppamento per mood: il profilo di mood di una traccia è unico, quindi un raggruppamento costruito su di esso assegnerebbe ogni traccia a un solo gruppo. La lettura per mood non è soltanto meno comoda: contraddice il testo che dovrebbe interpretare.
2. **Evita la circolarità che il rilievo segnala.** `BQ2-K2` misura la distanza di mood fra un segmento e il catalogo video. Se il segmento fosse definito raggruppando per mood, la misura calcolerebbe la distanza di mood di un insieme costruito per mood, e la sua variabilità fra segmenti sarebbe in parte un artefatto della definizione.
3. **La grana esiste già come tabella.** La `003` produce una tabella alla grana coppia traccia-genere, con le coppie deduplicate. La definizione adottata poggia su una struttura che esiste; l'alternativa richiederebbe un artefatto di raggruppamento che nessuna feature possiede — vedi il ritrovamento `F1`.
4. **Osservabilità.** Il campo è letto dalla fonte, non costruito. È la sola lettura compatibile con il fatto che §5.4 dichiari `BQ2-K1` di fonte `Spotify (reale)`.

**Che cosa la decisione costa**, e va dichiarato: la graduatoria di `BQ2-K3` avrà tante voci quanti sono i generi distinti della fonte, che è un numero alto per una lettura a colpo d'occhio. È un problema di presentazione della `008`, ma nasce qui e va consegnato lì come vincolo, non scoperto davanti allo schermo.

**Che cosa la decisione non fa**: non emenda la constitution, che formula BQ2 con la stessa parentesi «(genere/mood)». La parentesi è una glossa, non una definizione, e scioglierne l'ambiguità operativa è esattamente il lavoro che `R4` e la divergenza 1 assegnano a questa feature. Il mood resta nel framework a pieno titolo — come **attributo con cui i segmenti si confrontano**, che è ciò che `BQ2-K2` misura, non come criterio con cui i segmenti si formano.

### D2 — Il modello distingue tre grane, non due

Chiude `R7` e la divergenza 7 della revisione della `001`. §5.2 del business case presenta due granularità e afferma che «ogni scheda KPI dichiara in quale delle due opera». La formulazione non regge: la grana che una scheda dichiara è quella dell'**ingresso**, e nulla nel documento dichiara la grana del **risultato**. Sono due cose diverse, e la loro sovrapposizione è il difetto che il rilievo e la divergenza descrivono da due lati.

Il modello distingue **grana di appartenenza**, **grana di calcolo** e **grana del risultato**, e obbliga ogni KPI a dichiararle tutte e tre.

**Sulla granularità ibrida di `BQ2-K1`** — il rilievo `R7` propriamente detto. La scheda dichiara «coppia traccia-segmento per l'appartenenza, traccia deduplicata per il calcolo», e la revisione osserva che è una terza modalità che §5.2 non prevede. Sul dato trasformato **non è una terza modalità**: la pipeline della `003` ha deduplicato le coppie, quindi entro un segmento ogni traccia compare già una volta sola. Ciò che la scheda chiamava «traccia deduplicata per il calcolo» è una proprietà **garantita a monte** dalla tabella alla grana coppia, non un'operazione che la misura deve compiere. La grana ibrida sparisce: appartenenza e calcolo coincidono sulla coppia, il risultato è il segmento.

**Sulla grana di `BQ2-K2`** — la divergenza 7. La scheda dichiara la coppia traccia-segmento, che è corretta come grana di ingresso; la formula confronta due profili mediani, quindi il risultato è un valore per segmento. Con la distinzione a tre nozioni entrambe le affermazioni diventano vere e smettono di contraddirsi.

La correzione va portata in §5.2 del business case come nota in loco, secondo la prassi: il testo originale resta, la nota sta accanto.

### D3 — La popolarità è un attributo dell'appartenenza, non della traccia

Il contratto della `003` dichiara che sulla tabella alla grana traccia la popolarità è il **massimo osservato fra le repliche**, e che sulle tracce marcate `has_conflicting_popularity` quel valore non coincide con quello che la stessa traccia porta sulla tabella alla grana coppia. Il modello deve scegliere, perché altrimenti il valore di `BQ2-K1` dipende da quale tabella chi scrive la misura ha collegato.

**Decisione: la misura legge dalla tabella alla grana coppia**, cioè dal valore che la riga di quel segmento porta.

La ragione dirimente non è di gusto: è la **regola di lettura non negoziabile** del contratto della `003`, che assegna qualunque analisi per genere alla tabella alla grana coppia. `BQ2-K1` è una mediana per segmento, quindi è un'analisi per genere. La ragione di merito la conferma: prendere il massimo fra le repliche importerebbe dentro un segmento un valore osservato su una riga di un altro segmento.

**Conseguenza sul modello**: la popolarità è collocata sulla tabella alla grana coppia. Dove il campo esiste anche sulla tabella alla grana traccia, il modello lo **nasconde**, perché due colonne con lo stesso nome e valore diverso in due tabelle collegate sono un errore che aspetta di essere commesso.

### D4 — I tre assi di mood sono realizzati da tre campi su scala 0-1

§5.3 del business case dichiara tre assi comuni — energia, positività, ritmo — tutti su scala 0-1, e afferma che sul lato musicale sono «misurati direttamente». Il mapping ai campi reali della fonte è una decisione di modello e non è stato ancora preso da nessuno.

Energia e positività hanno un corrispondente diretto e su scala 0-1. **Il ritmo ha due candidati** e la scelta va motivata: il campo di tempo, espresso in battiti al minuto, e il campo di ballabilità, espresso su scala 0-1. Il modello adotta il secondo, per due ragioni:

1. §5.3 dichiara che i tre assi vivono su scala 0-1 e che sul lato musicale sono letti senza trasformazione. Il campo di tempo non è su quella scala: adottarlo obbligherebbe a normalizzarlo, cioè a interporre una trasformazione dove il documento dichiara che non ce n'è, e a scegliere il massimo su cui normalizzare — che è una delle decisioni indefinite che il rilievo `R6` della revisione della `001` ha già assegnato alla `007`. Il modello importerebbe un problema aperto invece di risolverne uno.
2. La glossa di §5.3 — «regolarità e propulsione ritmica» — descrive un indice composito di regolarità del battito, non una frequenza. È la definizione del campo di ballabilità, non di quello di tempo.

**Limite dichiarato**: il campo adottato è un indice calcolato dalla fonte con un metodo che la fonte non pubblica in dettaglio. «Misurato direttamente» significa che questo progetto lo legge senza trasformarlo, non che sia una misura fisica.

### D5 — Nessuna dimensione di calendario

Il modello non prevede una tabella calendario. Nessuno degli 8 KPI è definito su un asse temporale, e A2 insieme a §8 del business case vieta esplicitamente ogni conclusione di tendenza. Una dimensione di calendario renderebbe costruibile con un trascinamento proprio l'analisi che il documento dichiara fuori portata.

La decisione è dichiarata invece che taciuta perché **l'assenza di una tabella non si vede guardando uno schema**: senza questa riga, chi materializza il modello ne aggiungerebbe una per abitudine.

### D6 — Il profilo di mood video sta in una tabella separata

La corrispondenza fra categorie video e profilo di mood potrebbe tecnicamente vivere come tre colonne aggiuntive sulla dimensione delle categorie. Il modello la tiene separata perché la dimensione delle categorie è **osservata** e il profilo è **costruito dall'analista**: fonderle nasconderebbe la giuntura fra un dato letto e uno interpretato, che è la cosa che il principio I esiste per rendere visibile. È anche ciò che permette alla `006` di riempire una tabella senza toccare una tabella che questa feature ha già chiuso.

---

## Ritrovamenti

Registrati e non risolti, secondo il precedente `FR-032` della `002`.

- **F1 — Il rovesciamento di dipendenza temuto non si produce, e la ragione corregge come il debito era mappato.** Il timore era che definire il segmento per mood rendesse la tabella di corrispondenza della `006` un prerequisito della `005`, invertendo l'ordine della roadmap. La premessa va corretta: §5.3 del business case dichiara che la tabella di corrispondenza è **lato video** — associa le categorie del catalogo video a un profilo atteso — mentre sul lato musicale i tre assi sono letti direttamente. Anche adottando la lettura per mood, quindi, la `006` non avrebbe fornito nulla di ciò che serviva: sarebbe servito un artefatto **diverso e inesistente**, un raggruppamento delle tracce musicali per profilo di mood, che nessuna feature del piano possiede. L'ordine `005` → `006` regge, e regge per una ragione più solida di quella per cui era stato scritto.
- **F2 — La materializzazione del modello non appartiene ad alcuna feature.** La `005` progetta, la `007` scrive le misure, la `008` costruisce la dashboard. Il passaggio in cui qualcuno carica i quattro dataset in Power BI, traccia le relazioni e verifica che il modello regga non è assegnato. È la domanda che il primo punto di stop porta alla regia, ed è l'unica il cui esito può modificare la roadmap.
- **F3 — La graduatoria di `BQ2-K3` avrà tante voci quanti sono i generi della fonte.** Discende da `D1` ed è una conseguenza di presentazione, non di calcolo. Va consegnata alla `008` come vincolo dichiarato.

---

## Vincoli che le feature a valle ereditano

| Vincolo | Origine | Erede |
|---|---|---|
| la precisione a cui si confrontano profilo e rendiconto resta da decidere; il modello fissa tipi di dato, non il criterio di confronto | divergenza 1 della revisione della `003` | `007` |
| ogni misura sulla popolarità pubblica accanto al proprio valore la quota di zeri del segmento | divergenza 6 della revisione della `001` | `007` |
| l'inclusione delle righe a durata degenere nella mediana di `BQ1-K2` | marcatura `is_duration_zero` della `003` | `007` |
| l'arrotondamento e la precisione di presentazione di ogni misura | `FR-021` di questa spec, e `FR-015` della `004` per gli importi in euro | `007` |
| i sei valori di scenario della `004` non sono un fatto del modello: il modo in cui entrano nel report va deciso | `FR-029` di questa spec | `007` o `008` |
| la graduatoria dei segmenti ha un numero di voci alto per una lettura a colpo d'occhio | ritrovamento `F3` | `008` |
| l'assenza della dimensione di calendario va esposta dove un lettore potrebbe costruirsi da sé una misura temporale | decisione `D5` | `008` |
| il conteggio delle righe di un segmento misura il campionamento e non il mercato | nota di `BQ2-K1` in §5.5 del business case | `007` e `008` |

---

## Perimetro — cosa questa feature non fa

- **Nessuna misura DAX**, nemmeno in bozza, nemmeno come esempio illustrativo. Sono la `007`.
- **Nessuna riga della tabella di corrispondenza generi → mood.** È la `006`, e la sua decisione aperta `DA-1` non viene né risolta né toccata.
- **Nessun file `.pbix` e nessuna costruzione nell'interfaccia grafica.** È la `008`. Questa feature progetta, non materializza.
- **Nessuna modifica ai quattro dataset o alla pipeline della `003`.** Una trasformazione mancante è o una derivazione interna al modello, dichiarata come tale, o un ritrovamento.
- **Nessuna decisione sulla precisione del confronto fra profilo e rendiconto.** È la divergenza 1 della revisione della `003`, assegnata alla `007`.
