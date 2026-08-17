# Modello dati — StreamWave BI

> 🚧 **Documento in lavorazione — feature `005`.** Le sezioni con un segnaposto non sono ancora scritte. Il documento non è ancora registrato nel controllo di coerenza e il [README](../README.md) non vi rinvia: nessuno lo sta leggendo come definitivo.

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
| qualunque cosa **per categoria** | `bridge_title_category` | `dim_title`, che nel modello non porta più l'elenco delle proprie categorie |

**Perché l'errore è pericoloso e non fastidioso.** Nessuna delle colonne sbagliate produce un'eccezione, una cella vuota o un avviso. Producono un numero dell'ordine di grandezza giusto: 113.550<!--@CL.SP.pair.rows.after--> al posto di 89.741<!--@CL.SP.track.rows.after--> è una sovrastima di poco più di un quarto, e nessun lettore di una dashboard ha modo di accorgersene. È la ragione per cui questo modello separa le grane in tabelle distinte invece di lasciarle in una sola e affidarsi alla disciplina di chi scrive le misure.

**Come il modello rende difficile l'errore.** Un conteggio di titoli è una misura definita su `dim_title` e porta il nome dei titoli; un conteggio di assegnazioni è una misura diversa, definita sul ponte, e porta un nome diverso. Non esistono due<!--#--> strade per la stessa domanda: esistono due<!--#--> domande, con due<!--#--> nomi. È anche la ragione per cui il campo che elencava le categorie di un titolo **non entra nel modello** — il ponte lo sostituisce, e tenerli entrambi offrirebbe di nuovo la strada sbagliata.

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

Qui la condizione vale, ed è ispezionabile invece che sperata: il gruppo video ha un solo ponte, nessun ciclo, e i due<!--#--> gruppi sono disgiunti per quanto detto in §4. R1 è quindi l'unico cammino fra `dim_title` e `dim_category`.

> **Obbligo per chiunque aggiunga in futuro una tabella o una relazione a questo modello**: verificare che R1 resti l'unico cammino fra `dim_title` e `dim_category`. Una seconda relazione che chiuda un ciclo rende ambiguo il filtro e produce valori diversi a seconda del contesto, **senza alcun errore visibile**. È il solo punto di questo modello in cui una modifica futura può rompere qualcosa in silenzio, e questa riga esiste perché chi la farà lo sappia prima.

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
| `BQ1-K2` | non si applica | film sul lato video, traccia deduplicata sul musicale | un valore, sui due<!--#--> cataloghi | `dim_title`, `dim_track` |
| `BQ1-K3` | non si applica | traccia deduplicata | un valore, sul catalogo musicale | `dim_track`, `dim_category_mood` |
| `BQ2-K1` | coppia traccia-segmento | coppia traccia-segmento | **un valore per segmento** | `fact_track_segment`, `dim_segment` |
| `BQ2-K2` | coppia traccia-segmento | coppia traccia-segmento | **un valore per segmento** | `fact_track_segment`, `dim_track`, `dim_segment`, `dim_category_mood` |
| `BQ2-K3` | non si applica | segmento | una graduatoria di segmenti | `dim_segment` |
| `BQ3-K1` | fuori dal modello | fuori dal modello | fuori dal modello | nessuna |
| `BQ3-K2` | fuori dal modello | fuori dal modello | fuori dal modello | nessuna |

**Le due<!--#--> righe di BQ3 non sono una dimenticanza.** I valori di scenario della terza domanda di business non descrivono righe di un catalogo: non hanno una grana, non si aggregano e non si filtrano per segmento. Vivono in un artefatto proprio, [`reports/bq3_scenarios.json`](../reports/bq3_scenarios.json), e il modo in cui entrano in un report è una decisione delle feature successive. Dichiararli qui come fuori dal modello è più utile che ometterli, perché un elenco parziale lascerebbe chi legge a chiedersi se le righe mancanti siano state trattate o perse.

**Su `BQ1-K1`, la trappola già segnalata dalla scheda.** Il denominatore è il conteggio dei titoli distinti, non delle assegnazioni di categoria. Sono 8.807<!--@CL.NF.titles.rows.after--> contro 19.323<!--@CL.NF.category.assignments-->, e il modello tiene le due<!--#--> misure su due<!--#--> tabelle diverse con due<!--#--> nomi diversi proprio perché la scheda non debba essere ricordata a memoria.

## 9. Quali colonne entrano nel modello, e perché

*Sezione non ancora scritta — `T011`.*

## 10. Il mapping dei campi

*Sezione non ancora scritta — `T012`, `T013`.*

## 11. I tre assi di mood

*Sezione non ancora scritta — `T014`.*

## 12. La popolarità: da quale tabella si legge

*Sezione non ancora scritta — `T015`.*

## 13. Le derivazioni interne al modello

*Sezione non ancora scritta — `T016`.*

## 14. Le marcature ereditate dalla trasformazione

*Sezione non ancora scritta — `T017`.*

## 15. La tabella che la feature successiva riempie

*Sezione non ancora scritta — `T018`.*

## 16. Le assenze che sono decisioni

*Sezione non ancora scritta — `T019`.*

## 17. Nomi e convenzioni

*Sezione non ancora scritta — `T020`.*

## 18. Che cosa questo modello rende impossibile misurare

*Sezione non ancora scritta — `T021`.*

## 19. I vincoli che le feature a valle ereditano

*Sezione non ancora scritta — `T022`.*
