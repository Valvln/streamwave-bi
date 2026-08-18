# Modello dati — StreamWave BI

## 1. Che cosa è questo documento

Descrive il modello dati su cui le feature successive calcoleranno gli otto<!--#--> KPI del [business case](business_case.md): quali tabelle esistono, che cosa è una riga di ciascuna, come sono collegate, e da quale campo di quale dataset proviene ogni colonna.

Esiste come documento e non come file di Power BI per un obbligo esplicito della [constitution](../.specify/memory/constitution.md), principio V: tutto ciò che è esprimibile come artefatto testuale versionabile — e lo schema del modello dati e il mapping dei campi lo sono — **deve** esserlo, invece di vivere solo dentro un file binario che nessuno può ispezionare né confrontare.

### Il modello è progettato, non materializzato

**Nessuna affermazione di questo documento è stata verificata eseguendola.** Al momento in cui è scritto, il modello non è mai stato caricato in Power BI: non esiste alcun file di report, nessuna relazione è mai stata tracciata, e nessuna cardinalità è mai stata messa alla prova da un motore.

Va letto con la conseguenza che ne discende, invece di scoprirla davanti allo schermo: una direzione di filtro qui dichiarata sicura potrebbe rivelarsi ambigua, e una grana dichiarata potrebbe non reggere una misura reale. **Chi costruirà questo modello è il primo a provarlo**, ed è tenuto a riportare ogni divergenza invece di aggiustarla in silenzio — perché una divergenza aggiustata e non detta rende falso questo documento senza che nessuno se ne accorga.

### Su che cosa poggia

I dati sono i quattro<!--#--> insiemi prodotti dalla pipeline di trasformazione, descritti in [`docs/data_cleaning.md`](data_cleaning.md). Non sono versionati, per il principio II: lo è la pipeline che li rigenera. Questo documento li descrive attraverso il loro contratto e non attraverso i file.

Vale qui, come in ogni artefatto del progetto, l'**assunzione strutturale A1** del business case: il catalogo Netflix rappresenta il catalogo di StreamWave, il catalogo Spotify rappresenta il mercato musicale accessibile. Non è un dettaglio di provenienza da cercare altrove — cambia che cosa questo modello descrive. **Nessuna tabella qui contiene un dato di StreamWave**, che non esiste: le tabelle descrivono due<!--#--> cataloghi proxy, e ogni misura che vi poggerà erediterà quella distanza.

### Come si leggono i numeri di questo documento

Ogni quantità è legata all'artefatto versionato che la produce, con la grammatica definita in [`docs/convenzioni-marcatura.md`](convenzioni-marcatura.md). Il legame è invisibile alla lettura e verificabile da uno script: nessun numero di questo documento è stato scritto a mano.

## 2. Che cosa è un segmento

La seconda domanda di business chiede quale **segmento** musicale rappresenti l'opportunità di ingresso più coerente, e tre<!--#--> KPI su otto<!--#--> ordinano i segmenti. Fino a questo documento, però, nessuno aveva detto che cosa un segmento sia: il business case lo scrive come «segmento musicale (genere/mood)», con una barra fra due<!--#--> nozioni che non coincidono.

> **Un segmento è un genere dichiarato dalla fonte musicale**: il valore del campo `track_genre`. L'insieme dei segmenti è l'insieme dei suoi valori distinti, e ne conta 114<!--@SP.genre.count-->.

La definizione chiude il rilievo `R4` e la divergenza 1 della revisione del business case, che l'avevano segnalata come l'unità di analisi mai definita di un'intera domanda di business.

### L'alternativa, e perché è stata scartata

L'altra lettura era che un segmento fosse un **raggruppamento derivato per profilo di mood**. Quattro<!--#--> ragioni contro, in ordine di forza.

**La prima è che renderebbe falsa una frase già pubblicata.** La nota metodologica del business case afferma che «il catalogo musicale assegna una traccia a più segmenti quando è pertinente a più d'uno». L'appartenenza multipla è una proprietà del campo dei generi: la stessa traccia vi compare una volta per ciascun genere a cui è associata. Il profilo di mood di una traccia è invece **unico** — sono tre<!--#--> numeri su tre<!--#--> assi — quindi un raggruppamento costruito su di esso assegnerebbe ogni traccia a un solo gruppo. La lettura per mood non è soltanto meno comoda: contraddice il testo che dovrebbe interpretare.

**La seconda è che introdurrebbe una circolarità.** Il KPI `BQ2-K2` misura quanto il profilo di mood di un segmento sia vicino a quello del catalogo video. Se il segmento fosse definito raggruppando per mood, quella misura calcolerebbe la distanza di mood di un insieme costruito per mood, e parte della sua variabilità fra segmenti sarebbe un artefatto della definizione invece che un fatto sui cataloghi.

**La terza è che la grana esiste già.** La pipeline produce una tabella in cui una riga è l'appartenenza di una traccia a un genere. La definizione adottata poggia su una struttura che c'è; l'alternativa richiederebbe un raggruppamento delle tracce per mood che nessun artefatto di questo progetto produce, e che non è assegnato ad alcuna feature.

**La quarta è la confidenza.** Il campo dei generi è letto dalla fonte, non costruito dall'analista. È la sola lettura compatibile con il fatto che il business case dichiari `BQ2-K1` di fonte `Spotify (reale)`. Con la lettura per mood, il segmento sarebbe un costrutto dell'analista e la fonte di quel KPI diventerebbe `Derivato`, con la confidenza che ne discende — cioè una modifica alla scheda di un documento già pubblicato, non una scelta interna al modello.

### Che cosa la decisione costa

Va detto, perché una decisione presentata senza il suo prezzo non è verificabile.

La graduatoria di `BQ2-K3` avrà **una voce per segmento**, cioè 114<!--@SP.genre.count-->: un numero alto per una lettura a colpo d'occhio, e un vincolo che chi costruirà la dashboard eredita da qui.

Il mood, inoltre, **non scompare dal framework**: cambia ruolo. Non è il criterio con cui i segmenti si formano, è l'attributo con cui i segmenti si **confrontano** — che è esattamente ciò che `BQ2-K2` misura. La barra «genere/mood» del business case non viene riscritta; viene sciolta, e il mood resta sull'altro lato dello scioglimento.

### Il nome nel modello e il nome nella fonte

Le tabelle e le misure di questo modello usano la parola **segmento**, che è quella del business case. La colonna conserva invece il nome della fonte, `track_genre`, perché rinominarla romperebbe la tracciabilità verso il contratto della pipeline.

L'equazione è dichiarata qui una volta sola: **un segmento è un genere della fonte**, e le due<!--#--> parole indicano la stessa cosa in tutto ciò che segue.

## 3. Le tabelle

Sette<!--#--> tabelle, organizzate in due<!--#--> gruppi che non si toccano: uno per il catalogo video, uno per il catalogo musicale. Ciascun gruppo ha una tabella di appartenenza che risolve il fatto che un elemento possa stare in più insiemi.

### 3.1 Lato video

| Tabella | Ruolo | Che cosa è una riga | Chiave | Righe | Da dove viene |
|---|---|---|---|---|---|
| `dim_title` | dimensione | un titolo del catalogo video | `show_id` | 8.807<!--@CL.NF.titles.rows.after--> | `data/processed/netflix_titles.csv` |
| `bridge_title_category` | ponte | l'assegnazione di una categoria a un titolo | `show_id` + `category` | 19.323<!--@CL.NF.category.assignments--> | `data/processed/netflix_title_category.csv` |
| `dim_category` | dimensione | una categoria del catalogo video | `category` | 42<!--@CL.NF.category.distinct--> | derivata dal ponte |
| `dim_category_mood` | dimensione | il profilo di mood atteso di una categoria | `category` | nessuna, oggi | la costruisce la feature successiva |

### 3.2 Lato musicale

| Tabella | Ruolo | Che cosa è una riga | Chiave | Righe | Da dove viene |
|---|---|---|---|---|---|
| `dim_track` | dimensione | una traccia, indipendentemente dai suoi segmenti | `track_id` | 89.741<!--@CL.SP.track.rows.after--> | `data/processed/spotify_tracks.csv` |
| `dim_segment` | dimensione | un segmento musicale | `segment` | 114<!--@SP.genre.count--> | derivata dal fatto |
| `fact_track_segment` | fatto | l'appartenenza di una traccia a un segmento | `track_id` + `track_genre` | 113.550<!--@CL.SP.pair.rows.after--> | `data/processed/spotify_track_genre.csv` |

### 3.3 Le due cardinalità che vanno lette insieme

Il catalogo musicale ha 89.741<!--@CL.SP.track.rows.after--> tracce e 113.550<!--@CL.SP.pair.rows.after--> appartenenze. **La differenza non è un errore**: è il fatto che una traccia appartiene a più segmenti, ed è la ragione per cui questo modello ha una tabella di fatto separata dalla dimensione invece di una tabella sola.

Lo stesso vale sul lato video: 8.807<!--@CL.NF.titles.rows.after--> titoli e 19.323<!--@CL.NF.category.assignments--> assegnazioni di categoria.

Chi confondesse le due<!--#--> grandezze non otterrebbe un errore: otterrebbe un numero plausibile e sbagliato. È il motivo di §5.

### 3.4 Sul conteggio dei segmenti, che viene da un artefatto diverso dagli altri

Tutte le altre cardinalità di questa sezione sono lette dal rendiconto della trasformazione, che descrive i dati come il modello li userà. Il conteggio dei segmenti viene invece dal profilo dei dati di **origine**, ed è legittimo per una ragione che va scritta invece di lasciata dedurre.

Il rendiconto registra ogni valore del profilo che dopo la trasformazione non vale più. Il conteggio dei segmenti non vi compare, né fra i valori privi di controparte né fra quelli fuori perimetro: per l'invariante di classificazione totale che la pipeline verifica a ogni esecuzione, significa che è stato riconfrontato sul dato trasformato e **non è cambiato**. La ragione di merito lo conferma: la deduplicazione ha rimosso 450<!--@CL.SP.pair.removed_rows--> righe ripetute, e una riga ripetuta non è mai l'ultima del proprio genere.

## 4. Perché i due lati non si toccano

Non esiste alcuna relazione fra il gruppo di tabelle video e quello musicale, e **non deve esistere**.

Non c'è alcuna chiave che leghi un titolo video a una traccia musicale. Non è una lacuna dei dati che qualcuno potrebbe colmare: le due<!--#--> tassonomie classificano lungo dimensioni diverse — quella musicale per stile sonoro, quella video per forma narrativa — e il business case dichiara che la sovrapposizione lessicale fra le due<!--#--> è trascurabile. Un titolo e una traccia non hanno nulla in comune su cui una relazione possa poggiare.

**Il confronto fra i due<!--#--> cataloghi avviene fra misure, mai fra righe.** Il KPI `BQ1-K2` confronta due<!--#--> mediane di durata; `BQ1-K3` e `BQ2-K2` confrontano profili aggregati sui tre<!--#--> assi di mood. Nessuno di questi calcoli ha bisogno di sapere quale traccia corrisponda a quale titolo, perché nessuno di essi mette in corrispondenza singoli elementi.

Tracciare comunque una relazione produrrebbe una giunzione che nessuna misura del framework usa — e che qualcuno, prima o poi, userebbe per sbaglio.

I due<!--#--> lati si toccheranno in un solo punto, e non con una relazione: la tabella `dim_category_mood` porterà il lato video sugli stessi tre<!--#--> assi su cui il lato musicale è già misurato. È una **commensurazione**, cioè il modo di rendere due<!--#--> grandezze confrontabili, non un legame fra righe.

## 5. La regola di lettura, come proprietà dello schema

Il contratto della pipeline dichiara una regola non negoziabile: i due<!--#--> insiemi musicali **non sono intercambiabili**, e la stessa avvertenza vale fra i due<!--#--> video. È una regola scritta in prosa, e una regola in prosa protegge solo chi la legge.

Questa sezione la trasforma in una proprietà dello schema: per ogni cosa che si voglia calcolare, esiste una tabella corretta e una che restituisce un valore **plausibile e sbagliato**.

| Si vuole calcolare | Tabella corretta | Tabella che dà un valore sbagliato |
|---|---|---|
| un totale del catalogo musicale | `dim_track`, che ha 89.741<!--@CL.SP.track.rows.after--> righe | `fact_track_segment`, che ne ha 113.550<!--@CL.SP.pair.rows.after--> e conta più volte le stesse tracce |
| qualunque cosa **per segmento** | `fact_track_segment`, dove l'appartenenza esiste | `dim_track`, che non sa a quali segmenti una traccia appartenga |
| un totale del catalogo video | `dim_title`, che ha 8.807<!--@CL.NF.titles.rows.after--> righe | `bridge_title_category`, che ne ha 19.323<!--@CL.NF.category.assignments--> |
| il numero di titoli **di una categoria** | `dim_title`, che la direzione bidirezionale di R1 rende filtrabile per categoria | `bridge_title_category`, le cui righe sono assegnazioni: entro una sola categoria il conteggio coincide, e smette di coincidere appena la selezione ne comprende più d'una |

**Perché l'errore è pericoloso e non fastidioso.** Nessuna delle colonne sbagliate produce un'eccezione, una cella vuota o un avviso. Producono un numero dell'ordine di grandezza giusto: 113.550<!--@CL.SP.pair.rows.after--> al posto di 89.741<!--@CL.SP.track.rows.after--> è una sovrastima del 26,53%<!--@CL.SP.track.inflation.after--> rispetto al totale corretto, e nessun lettore di una dashboard ha modo di accorgersene. È la ragione per cui questo modello separa le grane in tabelle distinte invece di lasciarle in una sola e affidarsi alla disciplina di chi scrive le misure.

**Come il modello rende difficile l'errore.** Un conteggio di titoli è una misura definita su `dim_title` e porta il nome dei titoli; un conteggio di assegnazioni è una misura diversa, definita sul ponte, e porta un nome diverso. Non esistono due<!--#--> strade per la stessa domanda: esistono due<!--#--> domande, con due<!--#--> nomi. È anche la ragione per cui il campo che elencava le categorie di un titolo **non entra nel modello** — il ponte lo sostituisce, e tenerli entrambi offrirebbe di nuovo la strada sbagliata.

### Due eccezioni a questa tabella, che vanno lette insieme a §18

Questa sezione dice quale tabella regge una domanda. **Non dice che ogni domanda che quella tabella regge abbia senso**, ed è una distinzione che la forma tabellare nasconde.

**La prima riguarda l'aggregazione per segmento.** Il conteggio delle righe di un segmento si calcola su `fact_track_segment`, cioè sulla tabella qui dichiarata corretta, e resta privo di significato per la ragione esposta in §18. È il solo caso in cui questa tabella indica la porta giusta verso una domanda sbagliata, e chi consulta §5 prima di scrivere una misura per segmento non ha nulla, qui, che lo mandi a leggerla: questo capoverso esiste per quello.

**La seconda riguarda una colonna.** `dim_track.genre_count` è un intero sulla dimensione, e la sua somma su tutte le tracce vale 113.550<!--@CL.SP.pair.rows.after--> — cioè restituisce il conteggio delle appartenenze **a partire dalla tabella che questa sezione dichiara corretta per i totali di catalogo**. Il numero è giusto per ciò che è e sbagliato per ciò che sembra. §17 nasconde le chiavi proprio per chiudere quella strada; questa colonna la riapre in forma numerica, ed è il prezzo dichiarato della sua presenza — vedi §10.4.

## 6. Le relazioni e le direzioni di filtro

Cinque<!--#--> relazioni. La direzione di filtro dice in quale verso una selezione si propaga, ed è la parte del modello che più facilmente si dà per scontata: una direzione sbagliata non produce un errore, produce numeri che cambiano a seconda di come si guarda la stessa cosa.

| # | Da | A | Cardinalità | Direzione | Perché |
|---|---|---|---|---|---|
| R1 | `dim_title` | `bridge_title_category` | uno a molti | **bidirezionale** | senza di essa non si può selezionare l'insieme dei titoli a partire da una categoria, che è ciò che `BQ1-K1` chiede |
| R2 | `dim_category` | `bridge_title_category` | uno a molti | singola | il ponte non deve restringere l'elenco delle categorie |
| R3 | `dim_category` | `dim_category_mood` | uno a uno | singola | il profilo estende la categoria, non la filtra |
| R4 | `dim_track` | `fact_track_segment` | uno a molti | singola | nessuna misura seleziona le tracce a partire dal fatto |
| R5 | `dim_segment` | `fact_track_segment` | uno a molti | singola | come sopra |

### La condizione che rende sicura R1, e che va verificata

Un filtro bidirezionale è sicuro solo finché fra le due<!--#--> tabelle che collega esiste **un solo cammino**. Se ne esistessero due<!--#-->, il motore dovrebbe scegliere quale seguire, e la scelta cambierebbe il risultato senza che nulla lo segnali.

Qui la condizione vale, ed è ispezionabile invece che sperata: il gruppo video ha un solo ponte, nessun ciclo, e i due<!--#--> gruppi sono disgiunti per quanto detto in §4. Fra `dim_title` e `dim_category` esiste quindi **un cammino solo** — R1 fino al ponte, R2 dal ponte alla categoria — ed è quel cammino, non la singola relazione, l'oggetto della condizione.

> **Obbligo per chiunque aggiunga in futuro una tabella o una relazione a questo modello**: verificare che fra `dim_title` e `dim_category` continui a esistere un solo cammino. Una seconda relazione che chiuda un ciclo rende ambiguo il filtro e produce valori diversi a seconda del contesto, **senza alcun errore visibile**.

**Non è però il solo punto del modello che può cedere in silenzio**, e scriverlo darebbe a chi lo sorveglia una quiete che non gli spetta. Ce ne sono almeno altri tre<!--#-->, ciascuno dichiarato dove vive: l'invariante che rende costruibile `dim_segment` (§13), la scala su cui il lato video porta i tre<!--#--> assi di mood (§15), e la confusione di grana descritta in §5 e §18. Li accomuna la forma del guasto — un numero esce comunque, e sembra ragionevole — e li distingue chi può provocarli. Questo riquadro riguarda il solo caso che si apre **aggiungendo una relazione**, che è la modifica più facile da fare senza accorgersi di averla fatta.

### Una chiave che porta due nomi

R5 congiunge `dim_segment[segment]` con `fact_track_segment[track_genre]`: gli stessi valori sotto due<!--#--> nomi diversi, per la scelta di §17 che adotta la parola del business case sulla dimensione e conserva quella della fonte sul fatto. È legale e non ambiguo, ma **va saputo prima di tracciare la relazione**, perché sul lato video vale la simmetria opposta — `category` si chiama così su entrambi i lati di R2 — e chi costruisce il modello si aspetta la stessa cosa qui.

È l'unica relazione del modello in cui i due<!--#--> lati non portano lo stesso nome di colonna.

### Quello che la direzione non può impedire

Con R1 bidirezionale, un conteggio calcolato **sul ponte** conta le assegnazioni e non i titoli. La direzione di filtro non lo impedisce, e nessuna direzione potrebbe. Lo impedisce la separazione delle misure descritta in §5: due<!--#--> domande, due<!--#--> nomi, due<!--#--> tabelle.

## 7. Le tre grane

Il business case presenta due<!--#--> granularità e afferma che «ogni scheda KPI dichiara in quale delle due<!--#--> opera». La formulazione non regge, ed è il difetto che il rilievo `R7` e la divergenza 7 della sua revisione hanno segnalato da due<!--#--> lati diversi.

Non regge perché la grana che una scheda dichiara è quella dell'**ingresso** — su quali righe il calcolo lavora — mentre nulla dichiara la grana del **risultato**, cioè a che cosa si riferisce il numero che ne esce. Sono cose diverse, e per diversi KPI non coincidono affatto.

Questo modello ne distingue tre<!--#-->, e obbliga ogni KPI a dichiararle tutte.

| Nozione | Che cosa fissa | La domanda a cui risponde |
|---|---|---|
| **grana di appartenenza** | quale riga stabilisce che un elemento appartiene a un insieme | come faccio a sapere che questa traccia è in questo segmento? |
| **grana di calcolo** | su quali righe l'aggregazione opera | che cosa sto mediando, contando o sommando? |
| **grana del risultato** | a che cosa si riferisce un numero pubblicato | questo numero descrive un segmento, un catalogo o una traccia? |

### Come si chiude il rilievo su `BQ2-K1`

La scheda di quel KPI dichiara «coppia traccia-segmento per l'appartenenza, traccia deduplicata per il calcolo», e la revisione osserva giustamente che è una terza modalità che la nota metodologica non prevedeva.

Sul dato trasformato, però, **non è una terza modalità**. La pipeline ha deduplicato le coppie, rimuovendone 450<!--@CL.SP.pair.removed_rows-->: entro un segmento ogni traccia compare già una volta sola. Ciò che la scheda chiamava «traccia deduplicata per il calcolo» è quindi una proprietà **garantita a monte** dalla tabella di fatto, non un'operazione che la misura debba compiere. Appartenenza e calcolo coincidono sulla coppia; il risultato è il segmento.

### Come si chiude la divergenza su `BQ2-K2`

La scheda dichiara la coppia traccia-segmento, e la formula confronta due<!--#--> profili mediani. Entrambe le affermazioni sono vere e smettono di contraddirsi appena si distinguono le nozioni: la coppia è la grana di **ingresso**, il segmento è la grana del **risultato**.

La correzione alle due<!--#--> affermazioni del business case è portata sul documento originale come nota accanto al testo, secondo la prassi di questo progetto: il testo che c'era resta, perché è la traccia di ciò che quella feature aveva scritto.

## 8. Gli otto KPI sulle tre grane

| KPI | Appartenenza | Calcolo | Risultato | Tabelle |
|---|---|---|---|---|
| `BQ1-K1` | assegnazione titolo-categoria | titolo distinto | un valore, sul catalogo video | `dim_title`, `bridge_title_category`, `dim_category` |
| `BQ1-K2` | non si applica | film sul lato video, traccia deduplicata sul musicale | un valore, fra i **film** del catalogo video e l'**intero** catalogo musicale | `dim_title`, `dim_track` |
| `BQ1-K3` | non si applica | traccia deduplicata sul musicale, categoria sul video | un valore, sul catalogo musicale | `dim_track`, `dim_category_mood` |
| `BQ2-K1` | coppia traccia-segmento | coppia traccia-segmento | **un valore per segmento** | `fact_track_segment`, `dim_segment` |
| `BQ2-K2` | coppia traccia-segmento | coppia traccia-segmento sul musicale, assegnazione titolo-categoria sul video | **un valore per segmento** | `fact_track_segment`, `dim_track`, `dim_segment`, `bridge_title_category`, `dim_category`, `dim_category_mood` |
| `BQ2-K3` | non si applica | nessuna propria: compone `BQ2-K1` e `BQ2-K2` | una graduatoria di segmenti | nessuna letta direttamente; eredita quelle dei due<!--#--> KPI che compone |
| `BQ3-K1` | fuori dal modello | fuori dal modello | fuori dal modello | nessuna |
| `BQ3-K2` | fuori dal modello | fuori dal modello | fuori dal modello | nessuna |

**Le due<!--#--> righe di BQ3 non sono una dimenticanza.** I valori di scenario della terza domanda di business non descrivono righe di un catalogo: non hanno una grana, non si aggregano e non si filtrano per segmento. Vivono in un artefatto proprio, [`reports/bq3_scenarios.json`](../reports/bq3_scenarios.json), e il modo in cui entrano in un report è una decisione delle feature successive. Dichiararli qui come fuori dal modello è più utile che ometterli, perché un elenco parziale lascerebbe chi legge a chiedersi se le righe mancanti siano state trattate o perse.

**Su `BQ2-K3`, che non legge alcuna tabella.** La sua scheda lo dichiara `Derivato (BQ2-K1 + BQ2-K2)`: è un ordinamento dei segmenti secondo la combinazione di due<!--#--> misure già calcolate, con il peso relativo dei due<!--#--> criteri dichiarato esplicitamente. Non tocca quindi alcun dato direttamente, ed è la ragione per cui la sua casella non elenca tabelle invece di elencarne una. La colonna esiste per dire proprio questo: un elenco vuoto e un elenco dimenticato si scrivono allo stesso modo, e questa riga distingue i due<!--#--> casi. Ne discende che `BQ2-K3` dipende dal profilo di mood del lato video **attraverso `BQ2-K2`**, e non per una lettura propria — vedi §15.

**Su `BQ1-K3` e `BQ2-K2`, che aggregano il lato video in due<!--#--> modi diversi.** Le loro caselle di calcolo non coincidono, e la differenza non è una svista: la regola sta in §11, ed è la sola parte di questo modello in cui la grana di calcolo di un KPI è diversa sui due<!--#--> lati del confronto.

**Su `BQ1-K1`, la trappola già segnalata dalla scheda.** Il denominatore è il conteggio dei titoli distinti, non delle assegnazioni di categoria. Sono 8.807<!--@CL.NF.titles.rows.after--> contro 19.323<!--@CL.NF.category.assignments-->, e il modello tiene le due<!--#--> misure su due<!--#--> tabelle diverse con due<!--#--> nomi diversi proprio perché la scheda non debba essere ricordata a memoria.

## 9. Quali colonne entrano nel modello, e perché

I quattro<!--#--> insiemi di partenza contengono molte più colonne di quante questo modello ne usi. Prenderle tutte sarebbe la scelta di comodo — non si butta via niente, si decide dopo — e sarebbe sbagliata: un modello che espone tutto invita a costruire misure che il framework non ha definito, e una misura non definita nel business case è un'estensione dello scope che la constitution vieta senza motivazione esplicita.

Il modello adotta quindi una regola dichiarata invece di decidere colonna per colonna.

> **Una colonna entra nel modello se, e solo se, vale almeno una di queste tre<!--#--> condizioni:**
> **(a)** una misura del framework la legge;
> **(b)** identifica una riga per un lettore umano;
> **(c)** rende visibile una proprietà strutturale del modello.

Ne discende la parte che conta: **l'assenza di una colonna è una decisione, non una dimenticanza.** §10 elenca perciò anche ciò che è stato lasciato fuori, con la ragione — perché un elenco di ciò che c'è non permette a nessuno di contestare ciò che manca.

**Perché una regola e non un giudizio caso per caso.** Un giudizio caso per caso non si può contestare: chi non è d'accordo su una colonna deve discuterla da sola, e chi la aggiungesse in futuro non avrebbe alcun criterio da rispettare. Con una regola, la discussione si sposta dove è utile — se la condizione valga per quella colonna — e chi vuole aggiungerne una deve dire quale delle tre<!--#--> soddisfa.

## 10. Il mapping dei campi

Ogni colonna dichiara da quale campo di quale insieme proviene. Dove non è una lettura diretta, la regola di derivazione è in §13.

### 10.1 `dim_title`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `show_id` | `show_id` | testo | chiave |
| `title` | `title` | testo | (b) |
| `release_year` | `release_year` | intero | (b) |
| `type` | `type` | `Movie` / `TV Show` | (a) — `BQ1-K2` misura i soli film |
| `movie_duration_min` | `movie_duration_min` | intero, vuoto per le serie | (a) — `BQ1-K2`, lato video |
| `is_repaired_duration` | `is_repaired_duration` | booleano | (c) — vedi §14 |

**Fuori**: `director`, `cast`, `country`, `date_added`, `rating`, `description`, `tvshow_seasons`, `listed_in`.

**Su `release_year`, una precisazione che serve.** Entra per identificare un titolo — due<!--#--> film possono avere lo stesso nome — e **non è una dimensione temporale**. Ordinare una misura su di esso produrrebbe una lettura di tendenza, che il business case esclude esplicitamente dal perimetro. Vedi §16.

**Su `listed_in`, l'esclusione che conta più delle altre.** Il contratto della trasformazione conserva quel campo sull'insieme alla grana titolo, dichiarando che va bene «purché nessuno lo conti». Nel modello è **sostituito** dal ponte: tenerli entrambi offrirebbe due<!--#--> strade per la stessa domanda, di cui una sbagliata. È la forma strutturale di un'avvertenza che la trasformazione poteva solo scrivere.

### 10.2 `bridge_title_category`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `show_id` | `show_id` | testo | chiave, verso `dim_title` |
| `category` | `category` | testo | chiave, verso `dim_category` |

Nessun'altra colonna, e non per parsimonia: **un ponte che porta attributi smette di essere un ponte** e diventa una tabella su cui qualcuno aggregherà.

### 10.3 `dim_category`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `category` | derivata, §13 | testo | chiave |

### 10.4 `dim_track`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `track_id` | `track_id` | testo | chiave |
| `track_name` | `track_name` | testo | (b) |
| `artists` | `artists` | testo | (b) |
| `duration_min` | derivata da `duration_ms`, §13 | decimale | (a) — `BQ1-K2`, lato musicale |
| `energy` | `energy` | decimale `0-1` | (a) — asse **energia**, §11 |
| `valence` | `valence` | decimale `0-1` | (a) — asse **positività**, §11 |
| `danceability` | `danceability` | decimale `0-1` | (a) — asse **ritmo**, §11 |
| `genre_count` | `genre_count` | intero | (c) — dice a quanti segmenti una traccia appartiene |
| `is_duration_zero` | `is_duration_zero` | booleano | (a) — vedi §14 |
| `has_conflicting_popularity` | `has_conflicting_popularity` | booleano | (c) — vedi §12 |

**Fuori**: `album_name`, `explicit`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `tempo`, `time_signature`, `popularity`, `is_popularity_zero`.

**Sull'esclusione delle altre caratteristiche audio.** Il business case fissa **tre<!--#--> assi comuni definiti a priori**, e nessun KPI ne usa altri. Un modello che ne esponesse dieci<!--#--> renderebbe naturale costruire una misura su un asse che nessuno ha definito, cioè aggiungere al framework una dimensione di analisi senza dichiararlo. L'esclusione è la stessa scelta dell'assenza della dimensione di calendario, presa due<!--#--> volte per la stessa ragione: **il modello non offre ciò che il framework non ha definito.**

`tempo` è escluso benché sia il candidato alternativo per l'asse ritmo — la ragione del rigetto è in §11. Sta fuori dal modello proprio perché nessuno lo adotti credendolo equivalente.

`popularity` e `is_popularity_zero` non sono qui perché vivono sul fatto: è la decisione di §12.

### 10.5 `dim_segment`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `segment` | derivata da `track_genre`, §13 | testo | chiave |
| `is_high_zero_genre` | `is_high_zero_genre` | booleano | (a) — vedi §14 |

### 10.6 `fact_track_segment`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `track_id` | `track_id` | testo | chiave, verso `dim_track` |
| `track_genre` | `track_genre` | testo | chiave, verso `dim_segment` |
| `popularity` | `popularity` | intero `0-100` | (a) — `BQ2-K1`, vedi §12 |
| `is_popularity_zero` | `is_popularity_zero` | booleano | (a) — vedi §14 |

**Fuori**: tutte le altre. Gli attributi della traccia si leggono attraverso la relazione R4; replicarli sul fatto creerebbe di nuovo la seconda strada che §5 esiste per chiudere.

## 11. I tre assi di mood

Il business case definisce tre<!--#--> assi comuni su cui i due<!--#--> cataloghi diventano confrontabili — **energia**, **positività**, **ritmo** — e dichiara che sul lato musicale sono misurati direttamente, mentre sul lato video vanno assegnati. Quali campi realizzino i tre<!--#--> assi non era però stato deciso da nessuno: è una decisione di modello, e questa sezione la prende.

| Asse | Campo | Scala |
|---|---|---|
| energia | `energy` | `0-1` |
| positività | `valence` | `0-1` |
| ritmo | `danceability` | `0-1` |

Nessuna normalizzazione, nessuna trasformazione, nessun riscalamento. È ciò che rende letteralmente vera l'affermazione del business case secondo cui sul lato musicale i tre<!--#--> assi sono letti direttamente.

### Come il lato video diventa un profilo di catalogo

`dim_category_mood` porta una riga per **categoria**: 42<!--@CL.NF.category.distinct--> profili. Nessuno dei KPI che la usano confronta però un segmento con una categoria — li confrontano entrambi con il **catalogo video**, che è un altro oggetto. Il passaggio dall'uno all'altro è un'aggregazione, e un'aggregazione non dichiarata è una decisione presa da chi scrive la misura senza sapere di prenderla.

Il modello la dichiara qui, e **non è la stessa per i due<!--#--> KPI**.

| KPI | Che cosa chiede del lato video | Come si aggrega |
|---|---|---|
| `BQ1-K3` | l'**intervallo** occupato dal catalogo video su ciascun asse | minimo e massimo sulle 42<!--@CL.NF.category.distinct--> righe di `dim_category_mood`, senza ponderazione |
| `BQ2-K2` | il **profilo mediano** del catalogo video | mediana di ciascun asse sulle 19.323<!--@CL.NF.category.assignments--> righe del ponte, ciascuna portando il profilo della propria categoria |

**Perché per `BQ1-K3` non si pondera.** La sua scheda chiede la quota di tracce che cade «all'interno dell'intervallo occupato dai generi del catalogo video». Un intervallo è una proprietà dell'**insieme dei profili assegnati**, non della composizione del catalogo: quante volte una categoria compaia non sposta né il minimo né il massimo. Ponderare qui non renderebbe il valore più giusto, lo renderebbe indefinito.

**Perché per `BQ2-K2` si pondera, e sul ponte.** Tre<!--#--> ragioni, in ordine di forza.

La prima è la **simmetria del confronto**, che è ciò che rende quella distanza una distanza. Sul lato musicale il profilo del segmento è una mediana sulle coppie: una traccia che appartiene a più segmenti contribuisce alla mediana di ciascuno. L'assegnazione titolo-categoria è l'esatto omologo video della coppia — un titolo che sta in più categorie contribuisce a ciascuna — e aggregare un lato sulle appartenenze e l'altro sulle etichette metterebbe a confronto due<!--#--> grandezze costruite in modo diverso.

La seconda è che **il catalogo video è fatto di titoli**, non di categorie. Una mediana non ponderata sulle 42<!--@CL.NF.category.distinct--> righe darebbe alla categoria più rara lo stesso peso della più diffusa, e il numero che ne esce descriverebbe la tassonomia invece del catalogo.

La terza è di costruibilità: è l'unica delle due<!--#--> forme che non richiede una **seconda** regola di aggregazione un livello più sotto. Mediare per titolo obbligherebbe prima a comporre in un profilo unico le categorie di ciascuno degli 8.807<!--@CL.NF.titles.rows.after--> titoli, cioè a decidere di nuovo la stessa cosa a una grana diversa.

**Che cosa questa regola non decide.** Nulla su **come** i 42<!--@CL.NF.category.distinct--> profili vengano costruiti: quello è il lavoro della feature successiva, e le sue condizioni sono in §15. Qui si fissa soltanto che cosa se ne fa una volta che esistono.

**Perché la decisione sta in questo documento e non nelle misure.** Perché cambia quali tabelle una misura tocca — `bridge_title_category` e `dim_category` entrano in `BQ2-K2` solo per questo — e ciò che cambia lo schema appartiene allo schema. Lasciata aperta, sarebbe stata una decisione che tre<!--#--> feature diverse potevano ciascuna supporre presa da un'altra.

### Perché il ritmo non è `tempo`

I primi due<!--#--> assi hanno un corrispondente ovvio. Il terzo ha due<!--#--> candidati, e la scelta va motivata perché l'altro è quello che il nome suggerisce.

`tempo` è la velocità in battiti al minuto. Adottarlo avrebbe due<!--#--> conseguenze, entrambe sfavorevoli. La prima è che **non vive sulla scala dichiarata**: renderlo confrontabile con gli altri due<!--#--> assi richiederebbe di normalizzarlo, cioè di interporre una trasformazione dove il business case dichiara che non ce n'è. La seconda è che normalizzare richiede di scegliere **su quale massimo** — e quella scelta è una delle decisioni che la revisione del business case ha già segnalato come indefinite e assegnato alle misure. Il modello importerebbe un problema aperto invece di risolverne uno.

`danceability` vive su `0-1` e la glossa del business case per l'asse ritmo — «regolarità e propulsione ritmica» — descrive un indice composito di regolarità del battito, non una frequenza. È la definizione del secondo campo, non del primo.

### Il limite di «misurato direttamente»

I tre<!--#--> campi sono **calcolati dalla fonte**, con un metodo che la fonte non pubblica in dettaglio. «Misurato direttamente» significa quindi una cosa più stretta di quanto sembri: **questo progetto li legge senza trasformarli**, non che siano una misura fisica di una proprietà del suono.

È uno strato interpretativo che sta a monte del progetto e su cui il progetto non ha alcuna presa. Non abbassa la confidenza dei KPI che lo usano — la scala di confidenza misura gli strati che questo progetto interpone, non quelli della fonte — ma va saputo da chi difende un numero davanti a qualcuno che chieda che cosa significhi esattamente «positività» pari a `0,42`.

## 12. La popolarità: da quale tabella si legge

Questa è la sezione che chi scriverà `BQ2-K1` deve leggere prima di scrivere la misura, perché senza di essa il numero dipende da quale tabella ha collegato per caso.

**Il fatto.** La trasformazione dichiara che sull'insieme alla grana traccia la popolarità è il **massimo osservato fra le repliche** della stessa traccia. Su 720<!--@CL.SP.track.popularity_conflict.tracks--> tracce le repliche discordavano, e su quelle righe il valore alla grana traccia non coincide con quello che la stessa traccia porta alla grana coppia. Lo scarto massimo è di 44<!--@CL.SP.track.popularity_conflict.spread_max--> punti su una scala `0-100`, e le tracce che si scostano di più di dieci<!--#--> punti sono 13<!--@CL.SP.track.popularity_conflict.spread_over_10-->.

> **Decisione: la misura legge la popolarità dalla tabella di fatto**, cioè il valore che la riga di *quel* segmento porta. Sulla dimensione delle tracce la colonna non entra affatto.

**La ragione dirimente non è di gusto.** È la regola di lettura non negoziabile della trasformazione: un'analisi per genere si calcola sull'insieme alla grana coppia. `BQ2-K1` è una mediana per segmento, quindi è un'analisi per genere, quindi legge da lì. La decisione non è un'opinione di questo documento: è l'applicazione di un vincolo già scritto.

**La ragione di merito la conferma.** Prendere il massimo fra le repliche significherebbe portare dentro un segmento un valore osservato su una riga di un **altro** segmento. Una traccia che sta in due<!--#--> segmenti contribuirebbe a entrambe le mediane con lo stesso numero, che descrive la sua popolarità nel migliore dei due<!--#--> — spostando verso l'alto la mediana del segmento in cui era meno popolare.

### Quale deduplicazione, perché la trasformazione ne compie due

Le due<!--#--> hanno esiti opposti, e confonderle cambia che cosa si crede di leggere.

Quella alla **grana coppia** — le 450<!--@CL.SP.pair.removed_rows--> righe di §3.4 e §7 — è dichiarata *priva di perdita*: le repliche di una stessa coppia sono identiche su ogni attributo, e la pipeline lo verifica prima di scartarle, fermandosi se ne trovasse di discordi. Quella alla **grana traccia** non lo è: dove le repliche di una traccia discordano, conserva il massimo osservato.

Ne discende il punto che conta per chi scrive `BQ2-K1`: **il valore di popolarità che `fact_track_segment` porta non è il prodotto di alcuna scelta.** È il valore osservato per quella coppia. La selezione del massimo appartiene interamente all'insieme alla grana traccia, che questo modello non usa.

**Che cosa resta comunque fuori dalla portata del modello.** Non esiste un valore unico della popolarità di una traccia, e il modello non lo costruisce: la fonte ne registra uno per ciascuna appartenenza, e su 720<!--@CL.SP.track.popularity_conflict.tracks--> tracce quei valori non coincidono. Il modello non risolve la discordanza — la tiene alla grana a cui esiste.

**A che cosa serve `has_conflicting_popularity`, dopo tutto questo.** Non a documentare una perdita, che il modello non subisce. Serve a rendere visibile sulla dimensione una proprietà strutturale del modello: **per quelle tracce la popolarità non è una proprietà della traccia**, e la stessa traccia contribuisce con numeri diversi alle mediane di segmenti diversi. È la condizione (c) di §9, per una ragione diversa da quella che le si potrebbe attribuire leggendo il titolo della colonna.

Va detto che **la stessa informazione è già derivabile** dal fatto, confrontando minimo e massimo di `popularity` per `track_id` — in una forma che dà anche l'entità dello scarto e non solo il segnale. La colonna è quindi una ridondanza, tenuta perché quel confronto richiede che a qualcuno venga in mente di farlo, e la marcatura no. È una comodità dichiarata come tale, non una necessità.

**Conseguenza per chi scriverà le misure**: nel modello **non esiste** una popolarità alla grana traccia, e la sua assenza è deliberata. Se una misura futura dovesse averne bisogno, il valore va ripreso dall'insieme alla grana traccia e la differenza va dichiarata, non assorbita.

## 13. Le derivazioni interne al modello

Tre<!--#--> costruzioni che gli insiemi di partenza non forniscono. Sono derivazioni **interne al modello**, non modifiche alla pipeline: nessuna aggiunge, seleziona o interpreta informazione, e per questo nessuna abbassa la confidenza di ciò che vi poggia.

| Derivazione | Regola |
|---|---|
| `dim_category` | i valori distinti di `category` nel ponte |
| `dim_segment` | i valori distinti di `track_genre` nel fatto, più `is_high_zero_genre` |
| `dim_track.duration_min` | `duration_ms` diviso `60000` |

**Su `dim_segment`, un invariante da verificare e non da assumere.** La marcatura `is_high_zero_genre` è costante entro un segmento: è una proprietà del segmento che l'insieme di partenza replica su ogni riga per comodità di lettura. La derivazione la fa risalire alla dimensione, e questo è corretto **solo se** l'invarianza tiene. Chi costruisce il modello deve quindi verificarla al caricamento: un segmento che portasse due<!--#--> valori diversi renderebbe la dimensione non costruibile, e va **segnalato** invece che risolto scegliendone uno.

**Su `duration_min`, il divieto di arrotondare.** La conversione è una divisione esatta e non porta alcun arrotondamento a livello di colonna. Arrotondare qui arrotonderebbe **ogni traccia prima della mediana**, che è una decisione statistica presa di nascosto e capace di spostare il risultato. L'arrotondamento è una scelta di presentazione e appartiene a chi scriverà le misure.

**Perché la conversione sta nel modello e non nella misura.** `BQ1-K2` è una differenza fra due<!--#--> mediane espresse in minuti. Se la conversione vivesse dentro la misura, i due<!--#--> lati arriverebbero al confronto per strade diverse — uno letto, l'altro calcolato — e la simmetria del confronto dipenderebbe da come la misura è scritta. Convertire nel modello mette i due<!--#--> lati sulla stessa unità **prima** che qualcuno li confronti.

**Il codice di queste derivazioni non è scritto qui.** La constitution ammette Power Query M fra i linguaggi di trasformazione, quindi scriverlo sarebbe legittimo; sarebbe però materializzazione, che questa feature non fa. Questo documento dichiara la regola; chi materializza la applica, e riporta ogni divergenza invece di aggiustarla.

## 14. Le marcature ereditate dalla trasformazione

La trasformazione non ha eliminato le righe problematiche: le ha **marcate**, per una decisione presa allora e mai ritirata. Il modello deve portare quelle marcature fino al punto in cui una misura le può leggere, altrimenti la decisione di conservarle non serve a nulla.

Ogni marcatura sale alla grana di cui è proprietà, non a quella su cui la trovi scritta.

| Marcatura | Proprietà di | Tabella | Che cosa condiziona |
|---|---|---|---|
| `is_high_zero_genre` | un segmento | `dim_segment` | `BQ2-K1`: 7<!--@CL.SP.zero.high_genres.count--> segmenti superano la soglia dichiarata dalla trasformazione |
| `is_popularity_zero` | un'appartenenza | `fact_track_segment` | `BQ2-K1`: è ciò che rende calcolabile la quota di zeri di un segmento |
| `is_duration_zero` | una traccia | `dim_track` | `BQ1-K2`, lato musicale: 1<!--@CL.SP.duration.zero.rows--> riga |
| `has_conflicting_popularity` | una traccia | `dim_track` | nessuna misura: segnala le tracce che contribuiscono con valori diversi alle mediane di segmenti diversi, §12 |
| `is_repaired_duration` | un titolo | `dim_title` | `BQ1-K2`, lato video: 3<!--@CL.NF.duration.repaired.rows--> titoli |

**Perché `is_high_zero_genre` sale sulla dimensione.** L'insieme di partenza la replica su ogni riga della grana coppia. Lasciarla lì autorizzerebbe ad aggregarla — a contare 113.550<!--@CL.SP.pair.rows.after--> volte una proprietà che vale 114<!--@SP.genre.count--> volte, ottenendo un numero che non significa niente.

**Perché `is_duration_zero` sale sulla dimensione delle tracce**, benché la trasformazione la registri alla grana coppia. La durata è una proprietà della traccia e non della sua appartenenza a un segmento; soprattutto, la sola misura che la riguarda — `BQ1-K2` — si calcola per dichiarazione della propria scheda sulle tracce deduplicate. Lasciarla sul fatto la renderebbe invisibile all'unica misura interessata.

Il suo valore non sta nel numero, che è una riga sola: sta nell'obbligo di **dichiarare** se quella traccia entri nella mediana, invece di non accorgersi che esiste.

**Il salto di grana va però verificato al caricamento, come quello di `is_high_zero_genre`.** Sono lo stesso tipo di operazione: una marcatura registrata alla grana coppia viene fatta risalire a una grana più larga, e questo è corretto solo se il valore è costante entro quella grana. Se una traccia portasse `is_duration_zero` con valori diversi su due<!--#--> appartenenze, la colonna non sarebbe costruibile, e il caso va **segnalato** invece che risolto scegliendone uno — la regola è quella di §13, e vale identica qui.

La ragione per cui questo salto non compare fra le derivazioni di §13 è che non costruisce una colonna: sceglie su quale tabella una colonna già esistente viva. L'obbligo di verifica, però, non dipende da quella differenza.

**Sulla quota di popolarità nulla, che è un obbligo e non un'opzione.** Le righe a popolarità nulla sono 15.844<!--@CL.SP.zero.rows.after-->, e la trasformazione ne ha registrato la concentrazione: 7<!--@CL.SP.zero.high_genres.count--> segmenti superano la soglia che essa stessa dichiara. Quanto la distribuzione sia disuguale nessun artefatto lo pubblica, e questo documento non lo afferma: afferma che la soglia è superata su alcuni segmenti, che è il fatto misurato su cui l'obbligo poggia. La revisione del business case ha stabilito che ogni misura calcolata sulla popolarità pubblichi accanto al proprio valore la quota di zeri del segmento, perché una mediana calcolata su un segmento pieno di zeri è trascinata verso il basso da un difetto della fonte e non da una debolezza di domanda. Il modello **rende quella quota calcolabile**, tenendo la marcatura alla grana su cui la misura opera; pubblicarla è compito di chi scriverà le misure.

## 15. La tabella che la feature successiva riempie

Tre<!--#--> KPI su otto<!--#--> non esistono senza il profilo di mood del lato video, che **questo documento non costruisce**: `BQ1-K3` e `BQ2-K2` lo leggono, `BQ2-K3` ne dipende **attraverso `BQ2-K2`**, che compone insieme a `BQ2-K1`. Sul lato musicale i tre<!--#--> assi sono letti dalla fonte; sul lato video vanno assegnati a ciascuna categoria, e assegnarli è un lavoro interpretativo che appartiene alla feature successiva.

Come i profili di categoria diventino il profilo di catalogo che quei KPI confrontano è deciso in §11, e non da chi riempie questa tabella.

Il modello ne dichiara la forma, con zero<!--#--> righe.

| Colonna | Tipo | Vincolo |
|---|---|---|
| `category` | testo | chiave, e deve essere una delle 42<!--@CL.NF.category.distinct--> categorie del catalogo video |
| `mood_energy` | decimale `0-1` | asse energia |
| `mood_valence` | decimale `0-1` | asse positività |
| `mood_danceability` | decimale `0-1` | asse ritmo |

**Perché la forma si fissa qui e il contenuto no.** Se la forma la decidesse chi riempie la tabella, questo modello dovrebbe essere riaperto per accoglierla — e la dipendenza fra le due<!--#--> feature si rovescerebbe a metà lavoro. Fissando la forma prima, riempirla non richiede di modificare nulla di ciò che questo documento ha chiuso.

Quattro<!--#--> obblighi discendono dalla forma, e non sono negoziabili da chi la riempie:

1. **la copertura attesa è totale**: una riga per ciascuna delle 42<!--@CL.NF.category.distinct--> categorie. Una copertura parziale è ammessa, ma va **dichiarata**, e le misure che leggono la tabella devono dire che cosa fanno sulle categorie mancanti — perché una categoria senza profilo sparisce silenziosamente da una media;
2. **le tre<!--#--> colonne stanno sulla stessa scala del lato musicale.** È la condizione che rende il confronto di `BQ2-K2` una distanza fra grandezze commensurabili. Una scala diversa anche su un solo asse rende la distanza priva di significato **senza produrre alcun errore visibile**: il numero esce comunque, e sembra ragionevole;
3. **la confidenza non sale.** La tabella è costruita dall'analista, non osservata: è lo strato interpretativo che tiene i tre<!--#--> KPI che la usano a confidenza media, e nessuna cura nella costruzione li porta ad alta. La cura riduce l'errore, non cambia la natura del dato;
4. **questo documento non dice né chi né come costruisca le righe.** È una decisione aperta della roadmap, e resta aperta.

## 16. Le assenze che sono decisioni

Un'assenza non si vede guardando uno schema. Queste due<!--#--> sono decisioni prese, e senza questa sezione chiunque materializzasse il modello le annullerebbe per abitudine.

### Nessuna dimensione di calendario

Il modello **non ha una tabella calendario**, e non è una dimenticanza.

Nessuno degli otto<!--#--> KPI del framework è definito su un asse temporale. Il business case dichiara inoltre che i cataloghi descrivono «una fotografia, non una traiettoria» — il lato video è fermo al 2021<!--@NF.num.release_year.max-->, il musicale al 2022<!--#--> — ed esclude esplicitamente dal perimetro ogni conclusione su dinamiche successive e ogni analisi di tendenza recente.

Una dimensione di calendario in questo modello renderebbe costruibile **con un trascinamento** proprio l'analisi che il business case vieta. Chi la usasse non commetterebbe alcun errore tecnico: otterrebbe un grafico corretto di una cosa che i dati non possono dire. **L'assenza della tabella è la forma strutturale di un limite già dichiarato a parole**, ed è più efficace della dichiarazione perché non richiede che qualcuno l'abbia letta.

Ne discende un vincolo per chi costruirà la dashboard: se una vista temporale servisse davvero, aggiungere la tabella è un'estensione del perimetro del progetto e va decisa come tale, non risolta aggiungendo una tabella.

### Il profilo di mood non è dentro la dimensione delle categorie

Le tre<!--#--> colonne di §15 potrebbero tecnicamente vivere come colonne aggiuntive di `dim_category`. Il modello le tiene separate, con una relazione a uno a uno, per una ragione che non è di ordine.

`dim_category` è **osservata**: contiene le etichette che la fonte ha assegnato. Il profilo di mood è **costruito dall'analista**. Fonderle in una tabella sola metterebbe fianco a fianco, indistinguibili in un elenco di campi, un dato letto e un dato interpretato — e nascondere quella giuntura è precisamente ciò che il principio di provenienza esiste per impedire. Chi guarda il modello deve poter vedere dove finisce l'osservazione e comincia l'interpretazione.

## 17. Nomi e convenzioni

**Lingua**: la prosa di questo documento è in italiano; ogni identificativo — tabelle, colonne, misure — è in inglese. È la convenzione del progetto, e la ragione è che gli identificativi sono la parte più costosa da rinominare a valle.

**Tabelle**: prefisso `dim_` per le dimensioni, `fact_` per i fatti, `bridge_` per i ponti. Il prefisso dice il ruolo, che è l'informazione che serve per sapere se un'aggregazione su quella tabella ha senso.

**Colonne**: `snake_case`. Il nome della fonte è conservato ovunque non ci sia una ragione per cambiarlo, perché ogni rinomina è un punto in cui la tracciabilità verso il contratto della trasformazione si interrompe. L'unica eccezione è `segment`, chiave della propria dimensione, dove il modello adotta la parola del business case — e l'equazione con il nome della fonte è dichiarata in §2.

**Misure**: i nomi sono quelli **semantici già pubblicati** dal business case — `music_adjacent_catalog_share`, `segment_demand_index`, e così via. Non è una scelta di questo documento: il business case dichiara che il nome semantico «è quello che diventerà il nome della misura nel modello dati», ed è un impegno già preso. Inventare qui una convenzione nuova significherebbe rompere l'unico collegamento fra la scheda di un KPI e la misura che lo calcola.

**Colonne nascoste**: le colonne chiave che servono solo a reggere una relazione non compaiono nell'elenco dei campi offerto a chi costruisce un grafico. Una colonna tecnica visibile è un invito a costruirci sopra una misura, e le chiavi sono la categoria su cui quell'errore è più facile — un conteggio di `track_id` sul fatto restituisce 113.550<!--@CL.SP.pair.rows.after-->, che non è il numero delle tracce.

## 18. Che cosa questo modello rende impossibile misurare

Ogni scelta di struttura è anche una porta chiusa, e le porte chiuse non si vedono guardando uno schema. Questa sezione le elenca, perché l'omissione di un limite è di fatto un'affermazione implicita.

**Non risponde a nessuna delle tre<!--#--> domande di business.** Questo documento non contiene alcun risultato. Chi cercasse qui il valore di un KPI o una graduatoria di segmenti non li troverà: il modello dice dove i numeri si calcoleranno, non quanto valgono.

**Non permette di raggruppare i segmenti in famiglie più larghe.** I segmenti sono quelli dichiarati dalla fonte, e sono 114<!--@SP.genre.count-->. Qualunque macro-raggruppamento sarebbe un secondo strato interpretativo che questo modello non introduce e che nessuna feature del progetto possiede.

**Non permette alcuna analisi temporale.** Vedi §16: è una decisione, non un limite subìto.

**Non permette di dimensionare un segmento contandone le righe** — ed è il limite più insidioso, perché il conteggio è l'operazione più naturale che un motore tabellare offre.

Il catalogo musicale era bilanciato per costruzione del campione: ogni segmento portava 1.000<!--@SP.genre.rows_min--> tracce, quindi contarle misurava il campionamento e non il mercato. Sul dato trasformato **non è più nemmeno bilanciato**: la deduplicazione ha tolto righe in modo non uniforme, e oggi esistono 17<!--@CL.SP.recalc.genre.row_counts_distinct--> conteggi di righe distinti fra i segmenti, con il meno numeroso a 904<!--@CL.SP.recalc.genre.rows_min--> righe.

La conseguenza è controintuitiva e va detta com'è: **contare le righe non è diventato meno inutile, è diventato peggio che inutile.** Prima il risultato era costante e la sua inutilità era evidente; ora varia, e varia per una ragione che non riguarda il mercato.

**Quanto vari, questo documento non lo dice, e l'omissione è deliberata.** Il rendiconto pubblica il conteggio minimo e quanti conteggi distinti esistano; non pubblica il massimo né alcuna misura di dispersione. Senza quelli, affermare che lo scostamento sia grande — o rassicurare che sia piccolo — sarebbe un numero senza fonte travestito da valutazione. Ciò che si può dire con i valori pubblicati è che i conteggi non sono più tutti uguali e che nulla nel risultato di un conteggio segnala perché. Il modello non può impedirlo; questa riga è tutto ciò che può fare.

**Non regge un confronto fra due<!--#--> cataloghi interi, benché `BQ1-K2` produca un numero solo.** I due<!--#--> lati di quel confronto non sono simmetrici: il lato musicale è il catalogo intero, il lato video sono i **soli film**. L'esclusione delle serie non è una decisione di questo modello — la scheda del KPI la dichiara, con la sua ragione: il catalogo video misura le serie in stagioni, e convertirle in minuti richiederebbe un'assunzione che i dati non contengono.

Il modello ne eredita però due<!--#--> conseguenze che vanno dette qui, perché nessuno le vedrà guardando lo schema. La prima è che «differenza fra la durata mediana del catalogo video e quella del catalogo musicale» è una lettura sbagliata di quel numero, e nulla nel modello la smentisce. La seconda è che il modello **non** rende impossibile quantificare la parte esclusa: `dim_title` conserva `type`, quindi quanti degli 8.807<!--@CL.NF.titles.rows.after--> titoli siano film è calcolabile. Ciò che manca non è il dato, è l'obbligo di pubblicarlo accanto al valore — ed è per questo che il vincolo è registrato in §19 invece di essere chiuso qui.

**Non permette di trattare i segmenti come popolazioni disgiunte**, benché tutto ciò che li riguarda sia presentato per segmento. Una traccia appartiene a più segmenti — è la ragione per cui il fatto ha 113.550<!--@CL.SP.pair.rows.after--> righe contro 89.741<!--@CL.SP.track.rows.after--> tracce — e ne discendono tre<!--#--> conseguenze che nessuno vede guardando una graduatoria.

La prima è che **le quantità per segmento non si sommano**: sommare su tutti i segmenti un conteggio di tracce non restituisce il catalogo, lo eccede. La seconda è che **la stessa traccia contribuisce a più mediane** — per i tre<!--#--> assi di mood con lo stesso identico valore, letto da `dim_track`, e per la popolarità con valori che possono differire, come §12 spiega. La terza riguarda `BQ2-K3`: ordina 114<!--@SP.genre.count--> insiemi che si sovrappongono, mentre una graduatoria si legge come un elenco di alternative fra cui scegliere.

Nessuna di queste è un difetto del modello: sono la struttura del dato, e il modello la rappresenta correttamente. Sono elencate qui perché la rappresentazione corretta di una sovrapposizione **assomiglia in tutto** a quella di una partizione, e la differenza non compare in nessun numero pubblicato.

**Non permette di dire nulla sui pubblici.** Non esiste in questo modello alcuna entità che rappresenti una persona, una visione, un ascolto o un abbonamento, perché nessuna delle due<!--#--> fonti ne contiene. Nessuna relazione di questo modello, per quanto ben disegnata, potrà mai essere letta come una relazione fra spettatori e ascoltatori.

**Copertura del dato**: catalogo video fermo al 2021<!--@NF.num.release_year.max-->, catalogo musicale al 2022<!--#-->. Il modello descrive due<!--#--> fotografie e **non ha alcun modo di rappresentare che siano di due<!--#--> momenti diversi** — il che è coerente con l'assenza della dimensione di calendario, e va letto insieme a quella.

**I due<!--#--> anni non hanno lo stesso statuto, ed è la parte che conta.** Quello del lato video è un fatto osservato: è il massimo del campo che `dim_title` porta come `release_year`, ed è ancorato all'artefatto che lo misura. Quello del lato musicale non lo è: **il catalogo musicale non espone alcun campo di data**, né alla grana traccia né a quella coppia, e nessuna colonna di questo modello ne porta uno. Il 2022<!--#--> è un'affermazione presa dalla documentazione della fonte — l'assunzione A2 del business case — e il profilo dei dati di origine dichiara esplicitamente di non poterla verificare.

Ne discende un limite più stretto di quello enunciato sopra: il modello non solo non rappresenta la distanza fra le due<!--#--> fotografie, ma **non potrebbe rappresentarla nemmeno volendo**, perché su un lato manca il dato con cui la si misurerebbe. Chi in futuro volesse una dimensione di calendario scoprirebbe che è costruibile solo per metà del modello.

### Tre inferenze da evitare

**Che una relazione nel modello indichi una relazione nel mondo.** Una relazione dichiara come i dati si giuntano, non che esista un legame causale o comportamentale fra le entità che rappresentano. Vale in particolare per il collegamento fra categorie video e profili di mood: è una corrispondenza costruita fra due<!--#--> tassonomie disgiunte, non una somiglianza osservata.

**Che un modello progettato sia un modello funzionante.** Nessuna affermazione di questo documento è stata verificata eseguendola, come §1 dichiara. Una direzione di filtro qui dichiarata sicura potrebbe rivelarsi ambigua davanti allo schermo.

**Che il modello garantisca la correttezza delle misure.** Il modello rende **difficile** la giunzione sbagliata; non rende impossibile la misura sbagliata. Una misura scritta contro la tabella giusta con la logica sbagliata produce un numero sbagliato, e nessuno schema può accorgersene. Contro questo esistono la revisione indipendente e l'ancoraggio dei valori, non la struttura.

## 19. I vincoli che le feature a valle ereditano

Questo modello lascia aperte alcune decisioni. Sono elencate qui, con chi le eredita, perché una decisione rinviata senza un punto in cui va presa è una decisione che si perde.

| Vincolo | Da dove viene | Chi lo chiude |
|---|---|---|
| a quale precisione si confrontano i valori del profilo e quelli del rendiconto | revisione della trasformazione, divergenza 1 | le misure |
| se le righe a durata degenere entrino nella mediana di `BQ1-K2` | marcatura `is_duration_zero`, §14 | le misure |
| l'arrotondamento e la precisione di presentazione di ogni misura | §13, e la convenzione sugli importi in euro fissata dagli scenari | le misure |
| ogni misura sulla popolarità pubblica accanto al proprio valore la quota di zeri del segmento | revisione del business case, divergenza 6 | le misure |
| il modo in cui i valori di scenario entrano nel report, non essendo un fatto di questo modello | §8 | le misure o la dashboard |
| `BQ1-K2` confronta i soli film con l'intero catalogo musicale: l'asimmetria va dichiarata accanto al valore, e la quota di film è calcolabile da `type` | §18 | le misure e la dashboard |
| il peso relativo con cui `BQ2-K3` combina `BQ2-K1` e `BQ2-K2`, che la sua scheda impone di dichiarare esplicitamente e che nessuno ha ancora fissato | §8 | le misure |
| la graduatoria dei segmenti ha 114<!--@SP.genre.count--> voci, molte per una lettura a colpo d'occhio | §2 | la dashboard |
| l'assenza della dimensione di calendario va esposta dove un lettore potrebbe costruirsi da sé una misura temporale | §16 | la dashboard |
| il conteggio delle righe di un segmento misura il campionamento e non il mercato | §18 | le misure e la dashboard |
| i segmenti si sovrappongono: le quantità per segmento non si sommano, e la graduatoria di `BQ2-K3` non è una partizione del catalogo | §18 | la dashboard |

**Sulla precisione, una precisazione che evita un equivoco.** Questo modello fissa i **tipi di dato** delle proprie colonne, e fissare un tipo non decide un criterio di confronto. La divergenza aperta riguarda con quale precisione due<!--#--> valori dello stesso fatto, registrati in due<!--#--> artefatti diversi, vadano dichiarati uguali o diversi. È una domanda sul metodo di confronto, non sulla rappresentazione, e questo documento non la tocca.
