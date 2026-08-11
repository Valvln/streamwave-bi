# Feature Specification: Data Cleaning & ETL

**Feature Branch**: `003-data-cleaning-etl`

**Created**: 2026-08-11

**Status**: Draft

**Input**: User description: "Data Cleaning & ETL — dataset puliti e trasformazioni versionate. La feature porta i due dataset reali da `data/raw/` a uno stato utilizzabile dal modello dati, con trasformazioni in Python versionate e deterministiche, e produce un documento che dichiara ogni decisione di trattamento con la ragione, l'effetto quantificato e il riferimento al profilo che la motiva. Gli output non sono versionati: lo è la pipeline che li produce. La feature chiude cinque decisioni ereditate dalle revisioni della 001 e della 002. Trasforma, non definisce e non calcola."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

## Rapporto con le feature 001 e 002

Tre precisazioni servono a chi legge le tre spec in sequenza.

**Questa feature non riasserisce numeri.** La 002 ha prodotto `reports/data_profile.json`, dove ogni valore osservato ha un identificativo stabile — `NF.card.rating`, `SP.id.duplicate_share`, `SP.pop.zero.pct`. Ogni decisione presa qui deve poter citare l'identificativo che la motiva invece di ripetere la cifra. Un numero che questa feature scrive senza poterlo agganciare a un identificativo è, per costruzione, un numero che questa feature ha inventato.

**Questa feature cambia i denominatori.** Il profilo descrive `data/raw/`. Dopo la trasformazione alcuni di quei valori non valgono più: film con durata valorizzata, righe del catalogo musicale, completezza della classificazione per età. Non è un difetto della 002 né di questa feature: è ciò che una trasformazione fa. Il rischio è che a valle qualcuno citi l'uno credendo di citare l'altro, ed è il rischio contro cui questa spec scrive FR-030 e FR-031.

**Questa feature trasforma, non calcola.** Il confine con la 005 (modello dati), la 006 (tassonomia) e la 007 (misure) è dichiarato in «Perimetro» e ripreso in «Limiti Dichiarati». Dove una trasformazione sfiora una decisione di modellazione — la normalizzazione di un campo multi-valore, la scelta della grana di output — questa spec dichiara che cosa la scelta *non* stabilisce.

## Le decisioni ereditate e come questa spec le chiude

Sono cinque, tutte con riferimento puntuale a un verbale di revisione. Nessuna può essere rinviata: stanno tutte a monte di calcoli che le feature successive faranno. Ciascuna è riportata qui con le opzioni sul tavolo, la decisione, la sua ragione e dove va dichiarata; i requisiti che la rendono verificabile stanno più sotto.

Questa sezione è il punto di massima leva della spec. Se la revisione deve contestare qualcosa, è qui.

---

### D1 — Tracce a popolarità zero *(divergenza 6 della revisione 001)*

**Le opzioni**: incluse, escluse, o riportate come misura di fragilità accanto alla mediana.

**La decisione**: **incluse e marcate**. La pipeline non elimina alcuna riga per via del valore di popolarità. Aggiunge un indicatore esplicito che distingue le righe a popolarità zero, e pubblica la quota di zeri per genere insieme al dataset, così che qualunque misura costruita sulla popolarità possa riportare la propria fragilità accanto al proprio risultato.

**La ragione**: zero è un valore ammissibile di un indice definito su 0-100, non un valore mancante. Nulla nei dati distingue una traccia genuinamente non popolare da una traccia non misurata, e non esiste alcun criterio osservabile per farlo: escluderle significherebbe scegliere per conto di una misura che questa feature non possiede. La forma «riportate come misura di fragilità» è la sola che non pregiudica le altre due, perché l'indicatore consente a valle sia di includere sia di escludere, mentre l'eliminazione in pipeline è irreversibile.

**L'effetto**: nessuna riga rimossa. Le righe interessate sono quelle contate da `SP.pop.zero.count` e `SP.pop.zero.pct`.

**L'obbligo che ne discende**: la decisione chiude la divergenza sul piano del dato e ne apre uno vincolo sul piano della misura. Qualunque misura del framework calcolata sulla popolarità **deve pubblicare accanto al proprio valore la quota di zeri del segmento su cui è calcolata**. Vale in particolare per `BQ2-K1`. La feature 007 eredita l'obbligo, non la scelta: non può riaprire la questione dell'esclusione senza emendare questa decisione in modo esplicito.

---

### D2 — Titoli privi di durata *(divergenza 8 della revisione 001, parte dati)*

**Le opzioni**: eliminare le righe, imputare la durata, lasciarle prive di durata.

**Il fatto nuovo che questa feature porta**: il profilo registra tre titoli privi di durata (`NF.duration.missing`) e tre titoli con classificazione per età fuori dominio (`NF.rating.out_of_domain.rows`), i cui valori letterali sono in `catalogs.netflix_rating_out_of_domain` e hanno tutti la forma di una durata in minuti. Una verifica sui dati di origine mostra che si tratta **degli stessi tre titoli**: le righe prive di durata sono esattamente quelle il cui campo di classificazione contiene un valore che è sintatticamente una durata. La corrispondenza è totale in entrambe le direzioni. È uno scivolamento di colonna nella fonte, e la 002 lo aveva già osservato come fatto senza poterne trarre conseguenze operative.

**La decisione**: **riparazione dichiarata e circoscritta, mai imputazione, mai eliminazione**. In tre movimenti:

1. il valore che si trova nel campo di classificazione e che soddisfa la forma di una durata, su una riga il cui campo durata è vuoto, viene **spostato** nel campo durata;
2. il campo di classificazione di quelle righe viene posto a **mancante**, perché il valore corretto è andato perso nella fonte e inventarlo sarebbe l'unica cosa peggiore che perderlo;
3. le righe restano nel dataset e portano un indicatore che dichiara di essere state riparate.

**La ragione**: le due mosse sono di natura diversa e vanno distinte, perché è su questa distinzione che il resto della feature poggia. Porre a mancante un valore fuori da un dominio **già dichiarato e versionato** (`conventions.rating_domain`) è un controllo di dominio: meccanico, verificabile, ripetibile da chiunque. Spostare il valore nel campo durata è ammissibile solo perché la regola che lo autorizza è altrettanto meccanica — forma sintattica riconosciuta sul campo di partenza, campo di destinazione vuoto — e perché la sua area di applicazione è verificabile a priori. Non è una congettura sull'intenzione della fonte: è l'unica lettura che rende conto simultaneamente di due anomalie che coincidono riga per riga.

**Il vincolo che rende la riparazione difendibile**: la regola dichiara in anticipo quante righe si aspetta di toccare, e la pipeline **si ferma con errore** se ne tocca un numero diverso. Una regola di riparazione senza un limite dichiarato al proprio raggio d'azione è una regola che, su una versione diversa della fonte, riscrive dati senza che nessuno se ne accorga.

**L'effetto**: tre righe. Cambia il numero di film con durata valorizzata rispetto a `NF.num.movie_duration_min.count`, e cambia la completezza del campo di classificazione rispetto a `NF.miss.rating.*`. Entrambi ricadono sotto FR-030.

**La regola generale che resta in piedi**: al di fuori di questo caso, **nessuna durata mancante viene imputata e nessuna riga viene eliminata perché priva di durata**. Un titolo senza durata resta un titolo del catalogo: eliminarlo cambierebbe il denominatore della North Star `BQ1-K1`. L'esclusione dai calcoli spetta alla misura, che deve dichiarare il proprio denominatore.

**Cosa resta fuori**: il segno della differenza di `BQ1-K2` è della feature 007 e questa spec non lo tocca.

---

### D3 — Quale lettura di «sovrastima di circa un quinto» *(divergenza 6 della revisione 002)*

**Le opzioni**, entrambe aritmeticamente corrette e già registrate nella nota di correzione in §5.2 di `docs/business_case.md`: **21,28%** (`SP.id.duplicate_share`), quota di righe che ripetono una traccia già presente; **27,03%** (`SP.id.inflation`), eccesso del totale non deduplicato su quello corretto.

**La decisione**: si adotta **`SP.id.inflation`**, la seconda lettura, come misura dell'errore che si commette calcolando un totale di catalogo senza deduplicare.

**La ragione**: le due quote rispondono a domande diverse e solo una delle due è una sovrastima. `SP.id.duplicate_share` è una proprietà del file — quanta parte delle sue righe è ridondante — e ha per denominatore le righe, cioè la grandezza sbagliata. Una sovrastima si misura invece rispetto al valore giusto: quanto il totale errato eccede quello corretto. Il denominatore è il totale sulle tracce distinte, ed è la seconda lettura. Che sia anche quella che la parola *sovrastima* suggerisce più naturalmente lo aveva già osservato la nota di §5.2.

**La conseguenza sul testo**: «circa un quinto» descrive correttamente la prima lettura e non la seconda. La scelta va dichiarata **dove il documento la usa**, con una nota in loco che segue la prassi di `CLAUDE.md`: valore originale mai cancellato, data e feature dichiarate, fonte verificabile. Vedi FR-034.

**L'obbligo che ne discende**: ogni totale di catalogo musicale si calcola sulla grana **traccia deduplicata**. Le due grane restano entrambe disponibili come output (FR-013), ma la loro intercambiabilità è chiusa: nessuna misura può scegliere in silenzio.

---

### D4 — Criterio dei generi «a forte concentrazione di zeri» *(divergenza 8 della revisione 002)*

**Il problema**: nessuna soglia è fissata. Il profilo conta i generi oltre il 60% (`SP.pop.zero.genres_over_60`) ma quella soglia è un'etichetta di un conteggio, non un criterio adottato, e `country` — al 58,70% secondo `SP.pop.zero.by_genre.country` — cade dentro o fuori a seconda di dove la si mette.

**La decisione**: il criterio è **quota di righe a popolarità zero superiore al 50%**, e non il 60%.

**La ragione**: il 60% è un numero tondo, cioè nessuna ragione. Il 50% è invece la soglia oltre la quale un genere smette di essere descrivibile dalla propria mediana di popolarità: se più della metà delle righe di un genere vale zero, il valore centrale di quel genere è zero, qualunque cosa facciano le altre. Non è una proprietà stimata, è una proprietà della definizione di mediana. La soglia non nasce quindi da un giudizio sull'ampiezza accettabile di una massa di zeri, ma dalla misura che a valle la consumerà: è il punto in cui una misura di posizione perde la capacità di distinguere un genere dall'altro.

**Perché non pubblicare direttamente le mediane**: sarebbe il criterio più diretto, ed è escluso di proposito. Una mediana di popolarità per genere è a un passo da `BQ2-K1`, e «segmento» non è ancora definito (feature 005). La quota di zeri è l'osservazione equivalente che resta dentro il perimetro di questa feature.

**Che cosa il criterio produce**: un insieme di generi marcato nell'output e quantificato nel documento. `country` cade **dentro**, e con esso i generi fra il 50% e il 60% che la tabella di §3.5 di `docs/data_audit.md` lasciava fuori.

**L'avvertenza obbligatoria**: la soglia va dichiarata insieme al fatto che **due generi le stanno vicini entro pochi decimi di punto**. Un criterio che riclassifica un genere per un decimo di punto è un criterio di cui va detta la sensibilità, altrimenti la lista che ne esce si legge come una classifica naturale invece che come l'esito di un taglio.

**La granularità su cui si applica**: la quota va ricalcolata sulla grana coppia traccia-genere del dataset trasformato, non ripresa dal profilo. Le quote del profilo sono calcolate sulle righe di `data/raw/`; se la trasformazione tocca quelle righe, le quote cambiano e ricadono sotto FR-030.

---

### D5 — Statuto delle affermazioni derivate e perimetro del vincolo di tracciabilità *(divergenze 1 e 2 della revisione 002)*

**Il problema**: la revisione della 002 ha trovato tre affermazioni errate, e tutte e tre erano confronti o rapporti costruiti sui valori del profilo — «il secondo campo più incompleto», «tre delle sei corrispondenze», «un dominio quattro volte più ricco» — cioè affermazioni che nessun valore del profilo conteneva e che nessun controllo verificava. È la categoria in cui gli errori si sono concentrati, e il progetto non ha una regola per essa.

**La decisione — la regola.** Questa feature la adotta per i propri artefatti nella forma che segue, e la propone come regola generale del progetto:

> **Un confronto, una graduatoria, un rapporto o una differenza costruiti su valori misurati sono essi stessi valori misurati.** O esistono nell'artefatto con un identificativo proprio e vengono ancorati come qualunque altro numero, o non si scrivono. Non esiste la categoria intermedia dell'affermazione che «si ricava dai numeri già pubblicati e quindi non ha bisogno di fonte».
>
> Tre corollari operativi:
> **(a)** superlativi, ordinali e moltiplicatori riferiti a fatti misurati sono ammessi solo se ancorati a un valore che li sostiene;
> **(b)** i numerali scritti in lettere sono vietati per qualunque fatto misurato;
> **(c)** il controllo di coerenza **fallisce** — non avvisa — su un numerale non ancorato in posizione di fatto misurato.

**La ragione**: fra le tre strade che la revisione della 002 indicava — vietare in prosa, calcolare nel profilo, restringere l'enunciato — le prime due non sono alternative ma le due facce della stessa regola, e la terza da sola non impedisce il ripetersi dell'errore. Un divieto senza il canale del calcolo obbligherebbe a scrivere documenti che non possono dire nulla di comparativo; il calcolo senza divieto lascerebbe aperta la scorciatoia. Insieme funzionano perché spostano il costo dove serve: chi vuole scrivere «il campo più incompleto» deve prima farlo calcolare, e il costo di quel passaggio è esattamente ciò che nella 002 non è stato pagato.

**Il perimetro del vincolo di tracciabilità** (divergenza 1) ne discende. Il vincolo copre: i valori numerici; i valori letterali degli elenchi e delle convenzioni versionate; le affermazioni derivate come sopra definite. **Non copre** le affermazioni qualitative prive di contenuto numerico, che restano responsabilità di chi scrive e della revisione in contesto pulito.

**Il confine va dichiarato nel documento, non solo qui**, perché estendere la copertura sposta il confine, non lo elimina — ed è la lezione che la 002 ha già pagato una volta.

**Cosa la regia deve fare con questa decisione**: la spec la applica ai propri artefatti e ne riporta il testo. Portarla in `CLAUDE.md` perché valga per ogni documento successivo è atto di governance e spetta alla regia, non a questa feature.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chiunque abbia i dati di origine ottiene gli stessi dataset (Priority: P1)

Una persona che clona il repository, ricostruisce `data/raw/` e lancia un solo comando ottiene i dataset trasformati. Chi ripete l'operazione su un'altra macchina ottiene file identici ai primi. Nessun passaggio manuale, nessun file corretto a mano, nessuna differenza fra la prima esecuzione e la millesima.

**Why this priority**: è il principio II e il cuore della feature. Gli output non sono versionati: se la pipeline non è deterministica, non esiste nel progetto alcun modo di stabilire quali dati abbiano prodotto un numero. Una feature che si fermasse qui avrebbe già consegnato l'unico artefatto insostituibile — le altre storie lo rendono leggibile e verificabile, ma senza di esso non c'è nulla da leggere.

**Independent Test**: si esegue la pipeline due volte di seguito sullo stesso `data/raw/` e si confrontano gli output byte per byte; si verifica poi che `data/raw/` sia immutato. La storia è superata se le due esecuzioni coincidono e la cartella di origine non è stata toccata.

**Acceptance Scenarios**:

1. **Given** una copia del repository con `data/raw/` ricostruito, **When** si esegue la pipeline, **Then** vengono prodotti i dataset trasformati sotto le cartelle escluse da git e `data/raw/` risulta immutato — nessun file aggiunto, modificato o rimosso.
2. **Given** lo stesso `data/raw/`, **When** la pipeline viene eseguita due volte, **Then** ciascun file di output è identico byte per byte fra le due esecuzioni.
3. **Given** gli output prodotti, **When** si confronta l'impronta di ciascuno con quella registrata nell'artefatto versionato di rendicontazione, **Then** coincidono.
4. **Given** `data/raw/` incompleto, o una colonna attesa assente, o una regola di riparazione che tocca un numero di righe diverso da quello dichiarato, **When** si esegue la pipeline, **Then** si ferma con un errore che nomina la causa e **non** produce output parziali.
5. **Given** una copia pulita del repository, **When** si guarda sotto controllo di versione, **Then** nessun dataset di output è tracciato, mentre lo sono la pipeline, l'artefatto di rendicontazione e il documento.

---

### User Story 2 - Chi legge sa cosa è stato fatto ai dati e quanto pesa (Priority: P2)

Un lettore apre il documento delle trasformazioni e trova, per ogni decisione di trattamento, tre cose insieme: che cosa è stato fatto, perché, e quante righe o quanti valori tocca. Il perché rimanda a un identificativo del profilo, l'effetto a un valore versionato che chiunque può leggere senza possedere i dati. Le cinque decisioni ereditate stanno lì, chiuse, ciascuna con la propria ragione.

**Why this priority**: gli output non sono versionati, quindi non sono ispezionabili da chi non può rigenerarli. La verifica passa interamente dalla pipeline e da questo documento: è l'unico artefatto attraverso cui una decisione di trattamento diventa contestabile. Dipende da US1 perché ogni effetto quantificato deve provenire da un'esecuzione reale.

**Independent Test**: si consegna il solo documento a un lettore che non ha i dati e gli si chiede di dire, per tre decisioni a scelta, quante righe toccano e su quale osservazione del profilo poggiano. Se ci riesce senza eseguire nulla, la storia è superata.

**Acceptance Scenarios**:

1. **Given** il documento, **When** si cerca una qualunque decisione di trattamento, **Then** si trovano la ragione, l'effetto quantificato e il riferimento all'identificativo del profilo che la motiva.
2. **Given** il documento, **When** si cercano le cinque decisioni ereditate D1-D5, **Then** ciascuna è dichiarata chiusa con la propria decisione, e nessuna è rinviata a una feature successiva.
3. **Given** il documento, **When** si cerca un valore che dopo la trasformazione differisce dal corrispondente valore del profilo, **Then** lo si trova dichiarato accanto al valore del profilo da cui differisce, con la ragione della differenza.
4. **Given** il documento, **When** vi si cerca un valore di KPI o una risposta anche parziale a BQ1, BQ2 o BQ3, **Then** non se ne trova alcuno.
5. **Given** il documento, **When** si cercano i limiti, **Then** vi si trovano dichiarati almeno quelli elencati nella sezione «Limiti Dichiarati» di questa spec, incluso il fatto che gli output non sono ispezionabili da chi non può rigenerarli.

---

### User Story 3 - Prosa, pipeline e profilo non possono divergere in silenzio (Priority: P3)

Chi modifica il documento — oggi o fra quattro feature — non può lasciarvi un numero che gli artefatti non confermano più. Un comando eseguibile risolve ogni valore ancorato del documento sul profilo o sull'artefatto di rendicontazione e fallisce se trova una divergenza, un riferimento inesistente o un numerale non ancorato in posizione di fatto misurato.

**Why this priority**: è la regola D5 resa eseguibile. Vale P3 perché protegge artefatti già prodotti dalle altre due storie, ma senza di essa la regola resta un proposito — ed è esattamente ciò che nella 002 ha lasciato passare tre affermazioni errate mentre il controllo stampava esito positivo.

**Independent Test**: si altera un singolo valore ancorato nel documento e si esegue il comando; si aggiunge poi una frase con un numerale scritto in lettere riferito a un fatto misurato e lo si esegue di nuovo. La storia è superata se il comando fallisce in entrambi i casi e dice quale valore o quale frase non va.

**Acceptance Scenarios**:

1. **Given** documento e artefatti coerenti, **When** si esegue il comando, **Then** termina con esito positivo.
2. **Given** un valore ancorato alterato nel documento, **When** si esegue il comando, **Then** termina con esito negativo e nomina il valore, quello atteso e quello trovato.
3. **Given** un valore ancorato che rimanda a un identificativo inesistente, **When** si esegue il comando, **Then** termina con esito negativo e nomina il riferimento non risolvibile.
4. **Given** un numerale scritto in lettere riferito a un fatto misurato, **When** si esegue il comando, **Then** termina con esito negativo.
5. **Given** una copia del repository **senza** `data/raw/`, **When** si esegue il comando, **Then** funziona ugualmente, perché confronta artefatti tutti versionati.

---

### Edge Cases

- **Le repliche di una stessa traccia non concordano su tutti gli attributi.** La deduplicazione presuppone che le righe che condividono un identificativo siano la stessa traccia con etichette di genere diverse. Dove un attributo diverge fra le repliche, la deduplicazione **non è priva di perdita** e richiede una regola di scelta dichiarata, deterministica, e che conservi un valore effettivamente osservato invece di produrne uno nuovo. L'entità del fenomeno e la dispersione dei valori in conflitto vanno quantificate nel documento, non solo la regola. Vedi FR-016 e FR-017.
- **Una regola di riparazione tocca un numero di righe diverso da quello atteso.** La pipeline si ferma. È il vincolo che rende D2 difendibile: una riparazione senza limite dichiarato al proprio raggio d'azione riscrive dati in silenzio su una versione diversa della fonte.
- **Un valore fuori dominio non ha la forma che la regola di riparazione riconosce.** Viene posto a mancante e contato, mai indovinato. Il controllo di dominio e la riparazione sono due operazioni distinte e la seconda non è la conseguenza automatica della prima.
- **Una quota calcolata sul dataset trasformato differisce da quella del profilo.** È il caso normale, non l'eccezione: la trasformazione cambia i denominatori. Va dichiarata sotto FR-030, mai riconciliata forzando l'uno sull'altro.
- **Un genere cade appena sotto la soglia di D4.** La soglia va dichiarata insieme alla propria sensibilità: quali generi le stanno vicini e di quanto. Una lista prodotta da un taglio non va presentata come se fosse una proprietà naturale dei dati.
- **Il campo durata del catalogo video contiene due unità non convertibili** — minuti per i film, stagioni per le serie. Separarle è una trasformazione sintattica obbligata; **renderle confrontabili non lo è**, e non accade qui. Il fatto che il lato serie resti fuori da `BQ1-K2` è la decisione D3 della 001 e questa feature la cita, non la riformula.
- **`data/raw/` non è ricostruibile** perché manca il token Kaggle. La pipeline si ferma con un messaggio che rimanda a `scripts/download_data.sh`. Il documento e il comando di coerenza restano leggibili ed eseguibili, perché poggiano su artefatti versionati.

## Requirements *(mandatory)*

### La pipeline

- **FR-001**: La feature MUST produrre una pipeline di trasformazione in Python, versionata nel repository, eseguibile con un solo comando e senza alcun input manuale, interattivo o dipendente dall'ambiente di chi la lancia.
- **FR-002**: La pipeline MUST leggere esclusivamente da `data/raw/` e MUST NOT scrivervi. Al termine dell'esecuzione il contenuto di `data/raw/` MUST risultare immutato.
- **FR-003**: La pipeline MUST essere deterministica: due esecuzioni sugli stessi file di origine producono output identici byte per byte. Sono quindi vietati timestamp di esecuzione dentro gli output, ordinamenti non stabili, campionamenti casuali e qualunque dipendenza dall'ordine di iterazione non dichiarato.
- **FR-004**: La pipeline MUST fermarsi con un errore che nomina la causa, e MUST NOT produrre output parziali, quando: un file di origine manca; una colonna attesa è assente o ha cambiato nome; una regola di riparazione tocca un numero di righe diverso da quello dichiarato; un'invariante dichiarata sull'output non è soddisfatta.
- **FR-005**: La pipeline MUST verificare, prima di trasformare, che i file di origine corrispondano a quelli descritti dal profilo, confrontando l'impronta registrata in `sources` di `reports/data_profile.json`. Se non corrispondono MUST segnalarlo in modo esplicito: gli identificativi del profilo che il documento cita descriverebbero altri dati.
- **FR-006**: La pipeline MUST NOT modificare a mano alcun file di output. Se un valore è sbagliato si corregge la pipeline (principio II).

### Gli output di dati

- **FR-007**: Gli output di dati MUST essere collocati sotto le cartelle escluse da git e MUST NOT essere versionati. È la pipeline a essere versionata, non il suo prodotto.
- **FR-008**: Ogni file di output MUST avere un'impronta del contenuto registrata nell'artefatto di rendicontazione (FR-020), così che chi rigenera i dati possa stabilire di aver ottenuto esattamente gli stessi file senza che nessuno debba versionarli.
- **FR-009**: Ogni campo di ogni output MUST avere un tipo dichiarato e stabile. I campi booleani rappresentati come testo nella fonte MUST essere tipizzati; i campi numerici rappresentati come testo MUST esserlo.
- **FR-010**: Nessun campo dei due dataset di origine può essere eliminato in silenzio. I campi non presenti negli output MUST essere elencati nel documento con la ragione dell'esclusione.
- **FR-011**: Ogni output MUST dichiarare la propria **grana** — che cosa rappresenta una riga — e la grana MUST essere verificata dalla pipeline come invariante, non solo dichiarata.
- **FR-012**: Il catalogo video MUST produrre un output alla grana **titolo** e un output alla grana **titolo-categoria**, perché il campo delle categorie è multi-valore e i conteggi per categoria non sono sommabili sul totale del catalogo. La normalizzazione è una trasformazione sintattica del campo multi-valore e **non** costituisce disegno del modello dati, che è della feature 005.
- **FR-013**: Il catalogo musicale MUST produrre un output alla grana **coppia traccia-genere** e un output alla grana **traccia deduplicata**. Le due grane non sono intercambiabili e ciascun output MUST dichiarare la propria. Quale delle due una misura usi è decisione delle feature 005 e 007, con il vincolo posto da D3 sui totali di catalogo.
- **FR-014**: Il campo di durata del catalogo video MUST essere separato in due campi tipizzati e distinti — minuti per i film, stagioni per le serie — che la pipeline MUST NOT rendere confrontabili fra loro né aggregare in un'unica misura.

### Il trattamento — catalogo video

- **FR-015**: Il valore del campo di classificazione per età che ricade fuori dal dominio dichiarato in `conventions.rating_domain` MUST essere posto a mancante e contato. Il valore originale MUST essere riportato nel documento, non solo il conteggio.
- **FR-016**: La regola di riparazione dello scivolamento di colonna descritta in D2 MUST essere applicata con il proprio raggio d'azione dichiarato in anticipo, e la pipeline MUST fermarsi se lo eccede o non lo raggiunge (FR-004). Le righe riparate MUST portare un indicatore che le distingue.
- **FR-017**: Nessuna riga del catalogo video MUST essere eliminata, per alcuna ragione. Nessun valore mancante MUST essere imputato.

### Il trattamento — catalogo musicale

- **FR-018**: L'output alla grana traccia deduplicata MUST essere prodotto con una regola di deduplicazione **deterministica e dichiarata**. Dove le repliche di una stessa traccia divergono su un attributo, la regola MUST conservare un valore effettivamente osservato e MUST NOT produrne uno nuovo per aggregazione.
- **FR-019**: Il documento MUST quantificare la **perdita** della deduplicazione: quante tracce hanno repliche in disaccordo, su quali attributi, e con quale dispersione dei valori in conflitto. Dichiarare la regola senza dichiarare quanto pesa non è dichiararla.
- **FR-020**: Le righe a popolarità zero MUST essere conservate e marcate con un indicatore esplicito (D1). La quota di zeri per genere MUST essere ricalcolata sul dataset trasformato e resa disponibile insieme ai dati.
- **FR-021**: I generi che soddisfano il criterio di D4 — quota di righe a popolarità zero superiore al 50%, sulla grana coppia traccia-genere del dataset trasformato — MUST essere marcati nell'output ed elencati nel documento, insieme alla dichiarazione della sensibilità della soglia richiesta da D4.
- **FR-022**: Nessuna riga del catalogo musicale MUST essere eliminata sulla base del valore di popolarità. La sola riduzione di righe ammessa è la deduplicazione di FR-018, che produce un output distinto e non sostituisce quello alla grana coppia.
- **FR-023**: I valori degeneri diversi dalla popolarità — durate dichiarate pari a zero e simili — MUST essere contati e marcati, non eliminati e non corretti. Contarli è una constatazione; deciderne il trattamento in una misura non è di questa feature.

### L'artefatto di rendicontazione

- **FR-024**: La feature MUST produrre un artefatto di **soli numeri**, in formato strutturato leggibile da macchina, **versionato in git**, che registra per ogni decisione di trattamento il suo effetto quantificato e per ogni output la sua impronta e le sue dimensioni.
- **FR-025**: L'artefatto MUST essere collocato in una posizione effettivamente tracciata e MUST NOT essere intercettato da `.gitignore`. La verifica è meccanica: `git check-ignore` sul suo percorso non deve restituirlo.
- **FR-026**: Ogni valore dell'artefatto MUST avere un identificativo stabile e univoco, citabile dal documento e dalle feature successive, sullo stesso modello di `reports/data_profile.json`. Stabile significa che l'identificativo non cambia quando cambia il valore.
- **FR-027**: L'artefatto MUST NOT contenere prosa interpretativa, commento o giudizio. L'interpretazione vive nel documento.
- **FR-028**: L'artefatto esiste perché gli output di dati non sono versionati. È esso, insieme al documento, ciò che rende una decisione di trattamento verificabile da chi non possiede i dati di origine. Ogni numero che il documento pubblica sulle trasformazioni MUST risolversi su questo artefatto o su `reports/data_profile.json`.

### Il documento delle trasformazioni

- **FR-029**: La feature MUST produrre un documento in italiano, come singolo file Markdown, che dichiara **ogni** decisione di trattamento con: che cosa fa, la ragione, l'effetto quantificato, e il riferimento all'identificativo del profilo che la motiva. Una decisione senza effetto quantificato non è dichiarata.
- **FR-030**: Il documento MUST contenere una sezione dedicata ai **valori che cambiano**: ogni valore che dopo la trasformazione differisce dal corrispondente valore del profilo va riportato accanto all'identificativo del profilo da cui differisce, con la ragione della differenza. È il requisito che protegge dal citare l'uno credendo di citare l'altro.
- **FR-031**: Il documento MUST dichiarare le cinque decisioni ereditate D1-D5 come chiuse, ciascuna con la propria decisione e la propria ragione, e MUST NOT rinviarne alcuna a una feature successiva.
- **FR-032**: Il documento MUST applicare la regola D5 a se stesso: ogni valore misurato e ogni affermazione derivata sono ancorati a un identificativo; nessun numerale scritto in lettere compare in posizione di fatto misurato.
- **FR-033**: Il documento MUST dichiarare esplicitamente **che cosa il controllo di coerenza copre e che cosa no**, perché estendere la copertura sposta il confine invece di eliminarlo.
- **FR-034**: Il documento MUST contenere le sezioni obbligatorie richieste dai principi I e IV — provenienza e confidenza di ciò che riporta, limiti dichiarati. I limiti viaggiano con il documento, non solo con questa spec.

### Correzioni sugli artefatti già mergiati

- **FR-035**: La scelta di D3 MUST essere dichiarata **in loco** in §5.2 di `docs/business_case.md`, accanto alla nota di correzione del 2026-08-09 che registra l'ambiguità, secondo la prassi di `CLAUDE.md`: data, feature, letture possibili, lettura adottata, ragione, fonte verificabile. La nota precedente e il testo originale NON DEVONO essere cancellati né riscritti.
- **FR-036**: Dove il criterio di D4 riclassifica l'insieme dei generi rispetto a quanto §3.5 di `docs/data_audit.md` presentava, la divergenza MUST essere dichiarata con una nota in loco nello stesso documento, con la stessa prassi.
- **FR-037**: La feature MUST NOT correggere il disallineamento descrittivo di §3 di `docs/business_case.md` — le quattro tipologie di contenuto contro l'unica etichetta che la misura legge. È debito testuale assegnato altrove dalla roadmap: se lo incontra, lo registra come ritrovamento e si ferma lì. È il precedente FR-032 della 002.

### Il controllo di coerenza

- **FR-038**: La feature MUST produrre un **comando eseguibile** che risolve ogni valore ancorato del documento sul profilo o sull'artefatto di rendicontazione e segnala le divergenze. Se il controllo già esistente della 002 può essere esteso invece che duplicato, la scelta è del piano; il requisito è l'esistenza del comando, non la sua forma.
- **FR-039**: Il comando MUST terminare con stato di errore quando trova almeno una divergenza, e MUST nominare il valore divergente, quello atteso e quello trovato. Un controllo che segnala senza fallire è un controllo che verrà ignorato.
- **FR-040**: Il comando MUST segnalare come errore un riferimento non risolvibile e, per la regola D5 corollario (c), un numerale non ancorato in posizione di fatto misurato.
- **FR-041**: Il comando MUST poter essere eseguito **senza** `data/raw/` e **senza** rieseguire la pipeline, perché confronta artefatti tutti versionati.

### Perimetro — cosa la feature non fa

- **FR-042**: La feature MUST NOT definire «segmento» (rilievo R4 e divergenza 1 della 001): è della feature 005.
- **FR-043**: La feature MUST NOT costruire alcuna corrispondenza fra generi musicali e profili di mood: è della feature 006.
- **FR-044**: La feature MUST NOT calcolare alcun KPI del framework 001, né produrre risposte anche parziali a BQ1, BQ2 o BQ3. In particolare MUST NOT stabilire il segno della differenza di `BQ1-K2`, che è della feature 007, e MUST NOT pubblicare misure di posizione della popolarità per genere (vedi D4).
- **FR-045**: La feature MUST NOT generare dati sintetici: è della feature 004.
- **FR-046**: La feature MUST NOT disegnare il modello dati — tabelle dei fatti, dimensioni, relazioni, chiavi surrogate. La normalizzazione dei campi multi-valore di FR-012 è trasformazione, non modellazione, e il documento MUST dichiarare la distinzione.

### Key Entities

- **Sorgente**: un file di `data/raw/`. Attributi: nome, dimensione, impronta. Serve a stabilire se la pipeline sta trasformando i dati che il profilo descrive.
- **Decisione di trattamento**: una scelta applicata ai dati. Attributi: enunciato, ragione, identificativo del profilo che la motiva, effetto quantificato, righe o valori toccati, indicatore che ne marca l'esito nell'output. È l'unità che il documento dichiara e che l'artefatto di rendicontazione quantifica.
- **Output di dati**: un dataset trasformato. Attributi: grana dichiarata, campi con tipo, numero di righe, impronta. Non versionato, ma la sua impronta sì.
- **Valore di rendicontazione**: un numero prodotto dalla trasformazione. Attributi: identificativo stabile, valore, unità, decisione a cui si riferisce. È ciò che il documento cita e che il controllo verifica.
- **Denominatore cambiato**: un valore che dopo la trasformazione differisce dal corrispondente del profilo. Attributi: identificativo del profilo, valore precedente, valore nuovo, ragione della differenza.
- **Affermazione derivata**: un confronto, una graduatoria, un rapporto o una differenza costruiti su valori misurati. Per la regola D5 è essa stessa un valore: o ha identificativo, o non si scrive.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Due esecuzioni consecutive della pipeline sullo stesso `data/raw/` producono output identici byte per byte, per il 100% dei file prodotti.
- **SC-002**: Dopo l'esecuzione della pipeline, `data/raw/` è immutato: zero file aggiunti, modificati o rimossi.
- **SC-003**: Il 100% dei file di output ha un'impronta registrata nell'artefatto di rendicontazione, e le impronte registrate coincidono con quelle dei file rigenerati.
- **SC-004**: Zero dataset di output risultano tracciati da git; l'artefatto di rendicontazione non è intercettato da `.gitignore`, verificato meccanicamente sul percorso.
- **SC-005**: Il 100% delle decisioni di trattamento applicate dalla pipeline compare nel documento con ragione, effetto quantificato e riferimento a un identificativo del profilo; zero decisioni applicate e non dichiarate.
- **SC-006**: Tutte e cinque le decisioni ereditate D1-D5 sono dichiarate chiuse nel documento; zero decisioni rinviate.
- **SC-007**: Il 100% dei valori che dopo la trasformazione differiscono dal corrispondente valore del profilo è dichiarato nella sezione dei valori che cambiano, con l'identificativo del profilo accanto.
- **SC-008**: Il 100% dei campi di entrambi i dataset di origine è presente negli output oppure elencato fra le esclusioni con la ragione; zero campi omessi in silenzio.
- **SC-009**: Ogni output dichiara la propria grana e la pipeline la verifica come invariante: un output alla grana traccia deduplicata contiene un numero di righe pari agli identificativi distinti, e la verifica fallisce se non è così.
- **SC-010**: Zero righe eliminate dal catalogo video e zero righe eliminate dal catalogo musicale sulla grana coppia traccia-genere; l'unica riduzione presente è la deduplicazione, che vive in un output distinto.
- **SC-011**: Il 100% dei valori misurati e delle affermazioni derivate del documento è ancorato e risolvibile su un identificativo esistente; zero numerali scritti in lettere in posizione di fatto misurato.
- **SC-012**: Il comando di coerenza, eseguito su una copia pulita del repository **priva** di `data/raw/`, termina con esito positivo. Alterando un singolo valore ancorato termina con esito negativo e nomina quel valore; introducendo un numerale non ancorato in posizione di fatto misurato termina con esito negativo.
- **SC-013**: Chi clona il repository senza token Kaggle può risalire da qualunque numero del documento a un valore versionato, senza eseguire nulla e senza possedere i dati.
- **SC-014**: Zero valori di KPI e zero risposte anche parziali a BQ1, BQ2 o BQ3 compaiono negli artefatti prodotti; in particolare zero misure di posizione della popolarità per genere.
- **SC-015**: Le note in loco richieste da FR-035 e FR-036 esistono nei documenti interessati, e in nessuno dei due il testo o la nota preesistenti risultano cancellati o riscritti.

## Assumptions

Le assunzioni che seguono sono default ragionevoli adottati dove il prompt di consegna non vincolava. Sono decisioni di collocazione e di perimetro, non di implementazione: il come resta a `/speckit.plan`.

- **Collocazione della pipeline**: sotto `scripts/`, accanto a `scripts/profile_data.py` e `scripts/download_data.sh`.
- **Collocazione degli output di dati**: sotto `data/processed/`, già escluso da git. `data/interim/` resta disponibile per stadi intermedi se il piano ne trova la necessità, ma la feature non ne presuppone l'uso: uno stadio intermedio che nessuno legge è un file orfano.
- **Formato degli output di dati**: demandato al piano, con il vincolo che sia leggibile dallo strumento di destinazione e che il determinismo byte per byte di FR-003 sia verificabile. Il blanket di `.gitignore` intercetta comunque i formati tabellari usuali.
- **Collocazione dell'artefatto di rendicontazione**: sotto `reports/`, accanto a `reports/data_profile.json`, con lo stesso schema di identificativi stabili. Il piano decide se sia un file distinto o una sezione di un artefatto esistente; questa spec assume file distinto, perché il profilo descrive `data/raw/` e mescolarvi valori post-trasformazione riaprirebbe proprio la confusione che FR-030 esiste per chiudere.
- **Collocazione del documento**: `docs/`, accanto a `docs/data_audit.md` e `docs/business_case.md`, perché è un artefatto di lettura e non un artefatto di feature.
- **Il meccanismo di ancoraggio è quello della 002**, non uno nuovo. Il documento riusa la forma di marcatura già in uso in `docs/data_audit.md` e il controllo estende `scripts/check_audit_coherence.py` invece di duplicarlo, salvo che il piano dimostri che l'estensione costa più della duplicazione.
- **Nessuna figura, nessun grafico.** La feature produce dati e prosa. Le figure sono escluse da git sotto `reports/figures/` e non aggiungerebbero nulla di verificabile.
- **Dimensione dei dati**: circa 8.800 righe da un lato e 114.000 dall'altro. Nessun vincolo di memoria o di prestazioni entra nel perimetro; qualunque strumento ordinario è adeguato.
- **I due dataset sono quelli dichiarati dalla constitution** e non ne vengono aggiunti altri.
- **La revisione in contesto pulito è dentro la stima.** La roadmap la include da questa feature in avanti, per circa un'ora. L'artefatto da sottoporre a revisione è il documento delle trasformazioni.
- **Rischio di stima dichiarato**: la stima è di **7 ore, revisione inclusa**, ed è al limite del principio III. Il pezzo più esposto a crescere è il controllo di coerenza esteso al corollario (c) di D5 — riconoscere un numerale «in posizione di fatto misurato» è più difficile che risolvere un'ancora. Il ripiego dichiarato, se in fase di piano dovesse gonfiarsi, è la forma più conservativa che soddisfa FR-040: elenco esplicito delle forme ammesse fuori ancoraggio (date, riferimenti a sezioni, sigle, numeri di feature) e fallimento su tutto il resto. Non l'abbandono del requisito, che è la sola parte di D5 che impedisce all'errore della 002 di ripetersi.
- **La linea di scomposizione, se servisse**, è dichiarata dal prompt di consegna e passa fra la pipeline (US1) e il documento con il suo controllo (US2 e US3). Non è la scomposizione preferita — un documento che dichiara decisioni prese in un'altra sessione le eredita senza contesto — ma è l'unico taglio che lascia il repository coerente.

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: BQ1 e BQ2. **Non** BQ3.
- **Contributo**: feature **strumentale**. Non risponde ad alcuna domanda e non calcola alcun KPI: produce i dataset su cui le misure di BQ1 e BQ2 saranno calcolate, e chiude le decisioni di trattamento che stanno a monte di quei calcoli. Contribuisce a **BQ1** consegnando un catalogo video la cui grana per categoria è esplicita — condizione perché `BQ1-K1` non confonda titoli e assegnazioni — e le due durate separate e tipizzate su cui `BQ1-K2` sarà definito. Contribuisce a **BQ2** consegnando il catalogo musicale nelle due grane non intercambiabili che l'audit ha stabilito, con la massa di zeri marcata invece che silenziosamente inclusa o esclusa: è la condizione perché `BQ2-K1` possa dichiarare la propria fragilità invece di ereditarla senza saperlo. **Non** contribuisce a **BQ3**, che poggia interamente su dati sintetici perché nessun campo comportamentale o economico esiste nei dati reali, ed è della feature 004.

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

Questa feature **non introduce numeri nuovi sul mondo**: ogni valore che produce è o un valore osservato sui dati reali, o la misura dell'effetto di una propria trasformazione. Cambia però i denominatori, ed è la ragione per cui la tabella distingue le due nature.

| Famiglia di valori | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| Conteggi e quote ricalcolati sui dataset trasformati | Netflix (reale), Spotify (reale) | alta | conteggio diretto sull'output di una trasformazione dichiarata e rieseguibile | valore puntuale, con l'identificativo del profilo da cui differisce |
| Effetto quantificato di una decisione di trattamento | Derivato (dati reali + regola dichiarata) | alta | la regola è meccanica, versionata e il suo raggio d'azione è verificato dalla pipeline | valore puntuale |
| Perdita della deduplicazione (attributi in disaccordo fra repliche) | Spotify (reale) | alta | confronto diretto fra le repliche di uno stesso identificativo | valore puntuale, con la dispersione dei valori in conflitto |
| Insieme dei generi a forte concentrazione di zeri (D4) | Derivato (Spotify + soglia dichiarata) | **media** | il valore osservato è la quota di zeri, a confidenza alta; l'**appartenenza all'insieme** dipende da una soglia scelta da questa feature, e due generi le stanno vicini entro pochi decimi di punto | elenco, con la soglia e la sua sensibilità dichiarate accanto |
| Durate recuperate dalla riparazione dello scivolamento di colonna (D2) | Derivato (Netflix + regola dichiarata) | **media** | il valore è osservato nella fonte, ma la sua **attribuzione al campo durata** è un'inferenza — meccanica, verificabile e circoscritta a un raggio d'azione dichiarato, ma pur sempre un'inferenza sulla fonte | valore puntuale, righe marcate come riparate |

**Assunzioni dietro i dati sintetici**: nessun dato sintetico viene generato in questa feature.

**Perché due righe a confidenza media.** Il resto della feature osserva o conta. D2 e D4 no: in entrambi i casi fra il dato e il valore pubblicato si interpone una regola scelta da questa feature — una soglia, un'attribuzione di campo. Sono scelte dichiarate, motivate e verificabili, e restano scelte. Marcarle come alte le renderebbe indistinguibili dai conteggi diretti, che è esattamente la confusione che il principio I esiste per impedire. Nessuna delle due è a confidenza bassa: entrambe poggiano su valori osservati e su regole meccaniche, e il formato a range non aggiungerebbe informazione.

**Cosa questa scala non misura.** Vale per intero la distinzione di `docs/business_case.md` §6 e ripresa dalla 002: la confidenza qualifica la solidità di un numero **rispetto al dataset da cui è calcolato**, non la sua trasferibilità a StreamWave. Fra le due si interpone l'assunzione A1, che resta fuori scala per costruzione. Un dataset trasformato correttamente resta un dataset pubblico di terzi.

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Pulizia non è correttezza semantica.** La pipeline verifica forme, domini e coerenze dichiarate. Non ha modo di sapere se una durata dichiarata sia quella reale, se un genere sia attribuito correttamente, se un regista sia quello giusto. Il caso esemplare è già noto ed è dentro questa feature: tre durate finite nel campo della classificazione per età, in un campo che nessuna misura di completezza segnalava come problematico perché i valori erano **presenti**. Che quel caso sia stato trovato non autorizza a concludere che casi analoghi non esistano: autorizza a concludere il contrario.
- **Copertura del dato**: catalogo video fermo al **2021**, catalogo musicale fermo al **2022**. La trasformazione non estende la copertura di un giorno. Nessuna osservazione sui dataset trasformati dice qualcosa su dinamiche successive.
- **Gli output non sono ispezionabili da chi non può rigenerarli.** Non essendo versionati, non esistono per chi clona il repository senza token Kaggle. La verifica passa interamente dalla pipeline, dall'artefatto di rendicontazione e dal documento — che sono i tre artefatti versionati e sono il motivo per cui l'artefatto di rendicontazione esiste. Chi ha i dati può confrontare le impronte; chi non li ha si affida a tre artefatti leggibili invece che a un file che non può aprire. È il compromesso di FR-007 e va dichiarato, non attenuato.
- **Non risponde a**: nessuna delle tre domande di business. Non contiene KPI, stime né raccomandazioni.
- **Non risponde a**: quale sia il modello dati. La normalizzazione dei campi multi-valore è trasformazione sintattica, non disegno di tabelle dei fatti e di dimensioni. Chi leggesse gli output come uno schema li leggerebbe male: è la feature 005.
- **Non risponde a**: quale delle due grane del catalogo musicale una misura debba usare, salvo il vincolo posto da D3 sui totali di catalogo. La scelta appartiene a chi definisce la misura.
- **Non risponde a**: che cosa sia un «segmento». La marcatura dei generi di D4 è una marcatura di generi, non di segmenti: che il segmento coincida con il genere è una decisione della feature 005 che questa feature non anticipa.
- **Inferenza da evitare — un dataset pulito non è un dataset rappresentativo.** La pipeline rimuove ambiguità di forma, non distorsioni di campionamento. Il catalogo musicale resta bilanciato per costruzione a mille righe per genere, e contare righe per dimensionare un segmento resta sbagliato prima di essere calcolato, esattamente come lo era prima della trasformazione.
- **Inferenza da evitare — la deduplicazione non è priva di perdita.** Dove le repliche di una traccia divergono su un attributo, la grana deduplicata contiene un valore scelto da una regola. Il valore è osservato, la scelta no. Chi cita un totale sulla grana deduplicata cita anche quella regola, che il documento quantifica.
- **Inferenza da evitare — la marcatura di uno zero non è un giudizio sulla traccia.** L'indicatore di D1 dice che l'indice di popolarità di quella riga vale zero, non che la traccia sia irrilevante. Nulla nei dati distingue una traccia non popolare da una non misurata.
- **Inferenza da evitare — l'insieme dei generi di D4 è l'esito di un taglio, non una proprietà naturale.** La soglia è scelta e motivata, e due generi le stanno vicini entro pochi decimi di punto. Una lista prodotta da un criterio va letta come tale.
- **Dove è esposto all'utente finale**: il documento delle trasformazioni porta con sé la propria sezione di limiti. Non vivono solo in questa spec: viaggiano con l'artefatto che si legge.
