# Contratto — il modello dati, e che cosa le feature a valle possono darne per assunto

**Feature**: 005 Data Model Design | **Data**: 2026-08-18

Questo file fissa l'interfaccia fra quattro cose che vivono separate: il **modello** disegnato qui, la **`006`** che riempirà una delle sue tabelle, la **`007`** che vi scriverà le misure, e la **`008`** che vi costruirà sopra la dashboard.

Estende il contratto degli output della `003`, [`specs/003-data-cleaning-etl/contracts/output-datasets.md`](../../003-data-cleaning-etl/contracts/output-datasets.md), e non lo sostituisce: quel file descrive i **dati**, questo descrive il **ruolo** che assumono. La sua regola di lettura non negoziabile — i due dataset musicali non sono intercambiabili — è il vincolo strutturale da cui questo contratto discende, e qui diventa una proprietà dello schema invece che una raccomandazione in prosa.

**Questo contratto dice *che cosa*. Il *perché* sta in [`docs/data_model.md`](../../../docs/data_model.md)**, che è il documento pubblicato, e le alternative scartate in [research.md](../research.md). La separazione è quella che il contratto della `003` ha adottato.

**Vincolo che vale su tutto il documento**: il modello qui descritto **non è mai stato materializzato**. Nessuna delle sue affermazioni è stata verificata eseguendola in Power BI. Chi lo costruisce è il primo a provarlo, ed è tenuto a riportare ogni divergenza invece di aggiustarla in silenzio.

---

## 1. La definizione che tutto il resto presuppone

> **Un segmento è un genere dichiarato dalla fonte musicale**: il valore del campo `track_genre`. L'insieme dei segmenti è l'insieme dei suoi valori distinti, e ne conta 114.

Chiude `R4` e la divergenza 1 della revisione della `001`. Ne discendono la grana di tre KPI, il numero di voci della graduatoria di `BQ2-K3` e il significato di «per segmento» ovunque compaia a valle.

**Il nome nel modello è `segment`, il nome nella fonte resta `track_genre`.** La colonna non viene rinominata, perché rinominarla romperebbe la tracciabilità verso il contratto della `003`; la tabella e le misure usano invece la parola del business case. L'equazione è dichiarata qui una volta e non si ripete a ogni riga.

## 2. Le sette tabelle

Due stelle **disgiunte**. Non esiste, e non deve esistere, alcuna relazione fra il lato video e il lato musicale: le due tassonomie non hanno chiave comune, e il confronto fra i cataloghi avviene fra misure aggregate, mai fra righe.

### 2.1 Lato video

| Tabella | Ruolo | Grana — cosa è una riga | Chiave | Righe | Origine |
|---|---|---|---|---|---|
| `dim_title` | dimensione | un titolo del catalogo video | `show_id` | 8.807 | `data/processed/netflix_titles.csv` |
| `bridge_title_category` | ponte | l'assegnazione di una categoria a un titolo | `show_id` + `category` | 19.323 | `data/processed/netflix_title_category.csv` |
| `dim_category` | dimensione | una categoria del catalogo video | `category` | 42 | **derivata**, vedi §5 |
| `dim_category_mood` | dimensione | il profilo di mood atteso di una categoria | `category` | 42 attese, **0 oggi** | **la riempie la `006`**, vedi §7 |

### 2.2 Lato musicale

| Tabella | Ruolo | Grana — cosa è una riga | Chiave | Righe | Origine |
|---|---|---|---|---|---|
| `dim_track` | dimensione | una traccia, indipendentemente dai suoi segmenti | `track_id` | 89.741 | `data/processed/spotify_tracks.csv` |
| `dim_segment` | dimensione | un segmento musicale | `segment` | 114 | **derivata**, vedi §5 |
| `fact_track_segment` | fatto | l'appartenenza di una traccia a un segmento | `track_id` + `track_genre` | 113.550 | `data/processed/spotify_track_genre.csv` |

### 2.3 La regola di lettura, come proprietà dello schema

| Si vuole calcolare | Tabella corretta | Tabella che dà un valore **sbagliato** |
|---|---|---|
| un totale del catalogo musicale | `dim_track` | `fact_track_segment`, che conta 113.550 dove le tracce sono 89.741 |
| qualunque cosa **per segmento** | `fact_track_segment` | `dim_track`, che non conosce l'appartenenza |
| un totale del catalogo video | `dim_title` | `bridge_title_category`, che conta 19.323 dove i titoli sono 8.807 |
| qualunque cosa **per categoria** | `bridge_title_category` | `dim_title`, il cui campo `listed_in` non è nel modello proprio per questo |

## 3. Le relazioni

| # | Da | A | Cardinalità | Direzione di filtro |
|---|---|---|---|---|
| R1 | `dim_title` | `bridge_title_category` | uno a molti | **bidirezionale** |
| R2 | `dim_category` | `bridge_title_category` | uno a molti | singola |
| R3 | `dim_category` | `dim_category_mood` | uno a uno | singola |
| R4 | `dim_track` | `fact_track_segment` | uno a molti | singola |
| R5 | `dim_segment` | `fact_track_segment` | uno a molti | singola |

**Condizione di sicurezza di R1, da verificare e non da assumere.** La bidirezionalità è ammessa perché fra `dim_title` e `dim_category` esiste **un solo cammino**: la stella video ha un unico ponte e nessun ciclo, e le due stelle sono disgiunte. La condizione è strutturale e ispezionabile.

> **Obbligo per chi aggiunge una tabella o una relazione a questo modello**: verificare che R1 resti l'unico cammino fra `dim_title` e `dim_category`. Una seconda relazione che chiuda un ciclo rende ambiguo il filtro e produce valori diversi a seconda del contesto, senza alcun errore visibile. È il solo punto del modello in cui una modifica futura può rompere qualcosa in silenzio.

**Perché R3 è a uno a uno e non un allargamento di `dim_category`**: il profilo di mood è costruito dall'analista, la dimensione delle categorie è osservata. Tenerle separate rende visibile la giuntura fra un dato letto e uno interpretato, che è ciò che il principio I chiede.

## 4. Le colonne

**Regola di ammissione, che vale per tutte le tabelle**: una colonna entra nel modello se (a) una misura del framework la legge, (b) identifica una riga per un lettore umano, oppure (c) rende visibile una proprietà strutturale del modello. Una colonna che non soddisfa nessuna delle tre **non entra**, e la sua assenza è una decisione dichiarata.

### 4.1 `dim_title`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `show_id` | `show_id` | testo | chiave |
| `title` | `title` | testo | (b) |
| `release_year` | `release_year` | intero | (b) — **non è una dimensione temporale**, vedi §6 |
| `type` | `type` | enumerato `Movie` / `TV Show` | (a) — `BQ1-K2` esclude le serie |
| `movie_duration_min` | `movie_duration_min` | intero, vuoto per le serie | (a) — `BQ1-K2`, lato video |
| `is_repaired_duration` | `is_repaired_duration` | booleano | (c) — 3 titoli con la durata recuperata dalla riparazione `D2` della `003` |

**Escluse**: `director`, `cast`, `country`, `date_added`, `rating`, `description`, `tvshow_seasons`, `listed_in`.

**`listed_in` è l'esclusione che conta.** Il contratto della `003` lo conserva sul dataset alla grana titolo «purché nessuno lo conti». Nel modello quel campo è **sostituito** dal ponte: tenerlo entrambi significherebbe offrire due strade per la stessa domanda, di cui una sbagliata. È la forma strutturale dell'avvertenza che la `003` poteva solo scrivere.

### 4.2 `bridge_title_category`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `show_id` | `show_id` | testo | chiave, verso `dim_title` |
| `category` | `category` | testo | chiave, verso `dim_category` |

Nessun'altra colonna. Un ponte che porta attributi smette di essere un ponte.

### 4.3 `dim_category`

| Colonna | Origine | Tipo | Perché entra |
|---|---|---|---|
| `category` | derivata, vedi §5 | testo | chiave |

### 4.4 `dim_track`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `track_id` | `track_id` | testo | chiave |
| `track_name` | `track_name` | testo | (b) |
| `artists` | `artists` | testo | (b) |
| `duration_min` | **derivata** da `duration_ms` | decimale | (a) — `BQ1-K2`, lato musicale. Vedi §5 |
| `energy` | `energy` | decimale 0-1 | (a) — asse **energia** di §5.3 |
| `valence` | `valence` | decimale 0-1 | (a) — asse **positività** di §5.3 |
| `danceability` | `danceability` | decimale 0-1 | (a) — asse **ritmo** di §5.3 |
| `genre_count` | `genre_count` | intero 1-9 | (c) — rende visibile l'appartenenza multipla su cui l'intero modello poggia |
| `is_duration_zero` | `is_duration_zero` | booleano | (a) — condiziona `BQ1-K2` |
| `has_conflicting_popularity` | `has_conflicting_popularity` | booleano | (c) — 720 tracce, la traccia della perdita descritta in §6 |

**Escluse**: `album_name`, `explicit`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `tempo`, `time_signature`, `is_popularity_zero`.

**Sull'esclusione delle altre caratteristiche audio.** §5.3 del business case fissa **tre** assi comuni «definiti a priori». Un modello che ne espone dieci invita a costruire misure su assi che il framework non ha definito, e una misura del genere sarebbe un'estensione dello scope che il principio VI vieta senza motivazione esplicita. L'esclusione è la stessa scelta dell'assenza della dimensione di calendario, applicata due volte per la stessa ragione.

**`tempo` è escluso benché sia il candidato alternativo per l'asse ritmo.** La ragione del rigetto sta in `docs/data_model.md`; qui basta che il campo non sia nel modello, così che nessuno lo adotti per sbaglio credendolo equivalente.

**`popularity` non compare in questa tabella**, ed è la decisione `D3`: vedi §6.

### 4.5 `dim_segment`

| Colonna | Origine | Tipo | Perché entra |
|---|---|---|---|
| `segment` | derivata da `track_genre`, vedi §5 | testo | chiave |
| `is_high_zero_genre` | `is_high_zero_genre` | booleano | (a) — 7 segmenti superano la soglia `D4` della `003` |

**`is_high_zero_genre` sale dal fatto alla dimensione.** Il contratto della `003` dichiara che è **costante entro un genere** e che sul dataset è replicato «per comodità di lettura». Lasciarlo sul fatto autorizzerebbe ad aggregarlo, cioè a sommare 113.550 volte una proprietà che vale 114 volte.

### 4.6 `fact_track_segment`

| Colonna | Campo di origine | Tipo | Perché entra |
|---|---|---|---|
| `track_id` | `track_id` | testo | chiave, verso `dim_track` |
| `track_genre` | `track_genre` | testo | chiave, verso `dim_segment` |
| `popularity` | `popularity` | intero 0-100 | (a) — `BQ2-K1`. **È qui e non su `dim_track`**: vedi §6 |
| `is_popularity_zero` | `is_popularity_zero` | booleano | (a) — rende calcolabile la quota di zeri per segmento |

**Escluse**: tutte le altre. Gli attributi della traccia si leggono attraverso R4; replicarli sul fatto creerebbe la seconda strada che §2.3 esiste per chiudere.

**`is_high_zero_genre` non compare**: è salita su `dim_segment`.

## 5. Le tre derivazioni, e il loro confine

Il modello contiene tre costruzioni che i quattro dataset non forniscono. Sono **derivazioni interne al modello**, non modifiche alla pipeline della `003`: nessuna aggiunge o interpreta informazione.

| Derivazione | Regola | Vincolo |
|---|---|---|
| `dim_category` | i valori distinti di `category` in `bridge_title_category` | nessuna selezione, nessun raggruppamento, nessuna etichetta nuova |
| `dim_segment` | i valori distinti di `track_genre` in `fact_track_segment`, più `is_high_zero_genre`, che è costante entro il gruppo | l'invarianza va **verificata** al caricamento, non assunta: un genere che portasse due valori diversi renderebbe la dimensione non costruibile, e va segnalato invece che risolto |
| `dim_track.duration_min` | `duration_ms` diviso 60000 | **nessun arrotondamento a livello di colonna.** Arrotondare qui arrotonderebbe ogni traccia prima della mediana, che è una decisione statistica presa di nascosto. L'arrotondamento è di presentazione e appartiene alla `007` |

**Il codice di queste derivazioni non è scritto da questa feature.** Il principio II ammette Power Query M; scriverlo sarebbe però materializzazione, che nessuna feature possiede oggi. Il contratto dichiara la regola; chi materializza la applica e riporta ogni divergenza.

## 6. Le cinque cose che la `007` non può decidere da sé, e che questo contratto fissa

### 6.1 La popolarità si legge dal fatto, mai dalla dimensione

Il contratto della `003` §1.4 dichiara che su `spotify_tracks.csv` la popolarità è il **massimo osservato fra le repliche**, e che su 720 tracce quel valore non coincide con quello che la stessa traccia porta alla grana coppia; lo scarto massimo è 44 punti.

**Il modello colloca `popularity` sul solo `fact_track_segment` e non la porta su `dim_track`.** La ragione dirimente è la regola di lettura non negoziabile della `003`: un'analisi per genere si calcola sulla tabella per genere, e `BQ2-K1` è una mediana per segmento. La ragione di merito la conferma: leggere il massimo importerebbe dentro un segmento un valore osservato su una riga di un altro segmento.

**Conseguenza per la `007`**: qualunque misura sulla popolarità legge la colonna del fatto. Non esiste nel modello una popolarità alla grana traccia, e la sua assenza è deliberata.

### 6.2 I tre assi di mood hanno un campo ciascuno, ed è dichiarato

| Asse di §5.3 | Campo | Scala |
|---|---|---|
| energia | `energy` | 0-1 |
| positività | `valence` | 0-1 |
| ritmo | `danceability` | 0-1 |

Nessuna normalizzazione, nessuna trasformazione. È ciò che rende vera l'affermazione di §5.3 secondo cui sul lato musicale i tre assi sono letti direttamente.

### 6.3 Le tre grane di ciascun KPI

Ogni KPI dichiara **grana di appartenenza**, **grana di calcolo** e **grana del risultato**. Chiude `R7` e la divergenza 7 della revisione della `001`, dove una sola nozione doveva reggerne tre.

| KPI | Appartenenza | Calcolo | Risultato | Tabelle |
|---|---|---|---|---|
| `BQ1-K1` | assegnazione titolo-categoria | titolo distinto | un valore, sul catalogo video | `dim_title`, `bridge_title_category`, `dim_category` |
| `BQ1-K2` | — | film per il lato video, traccia deduplicata per il musicale | un valore, fra i **film** del catalogo video e l'**intero** catalogo musicale | `dim_title`, `dim_track` |
| `BQ1-K3` | — | traccia deduplicata sul musicale, categoria sul video | un valore, sul catalogo musicale | `dim_track`, `dim_category_mood` |
| `BQ2-K1` | coppia traccia-segmento | coppia traccia-segmento | **un valore per segmento** | `fact_track_segment`, `dim_segment` |
| `BQ2-K2` | coppia traccia-segmento | coppia traccia-segmento sul musicale, assegnazione titolo-categoria sul video | **un valore per segmento** | `fact_track_segment`, `dim_track`, `dim_segment`, `bridge_title_category`, `dim_category`, `dim_category_mood` |
| `BQ2-K3` | — | nessuna propria: compone `BQ2-K1` e `BQ2-K2` | una graduatoria di 114 voci | nessuna letta direttamente; eredita quelle dei due KPI che compone |
| `BQ3-K1` | — | — | fuori dal modello | nessuna, vedi §8 |
| `BQ3-K2` | — | — | fuori dal modello | nessuna, vedi §8 |

**Sulla granularità ibrida di `BQ2-K1`**, che il rilievo `R7` segnalava: la scheda dichiarava «coppia traccia-segmento per l'appartenenza, traccia deduplicata per il calcolo». Sul dato trasformato non è una terza modalità. La pipeline della `003` ha deduplicato le coppie — 450 righe rimosse — quindi **entro un segmento ogni traccia compare già una volta sola**: la deduplicazione è garantita a monte e non è un'operazione che la misura debba compiere.

### 6.4 Come il lato video diventa un profilo di catalogo, e perché non allo stesso modo per i due KPI

`dim_category_mood` porta una riga per **categoria**. Né `BQ1-K3` né `BQ2-K2` confrontano un segmento con una categoria: entrambi lo confrontano con il **catalogo video**. Il passaggio è un'aggregazione, e il contratto la fissa perché cambia quali tabelle una misura tocca.

| KPI | Che cosa chiede del lato video | Come si aggrega |
|---|---|---|
| `BQ1-K3` | l'**intervallo** occupato sul catalogo video, per ciascun asse | minimo e massimo sulle 42 righe di `dim_category_mood`, **senza ponderazione** |
| `BQ2-K2` | il **profilo mediano** del catalogo video | mediana di ciascun asse sulle 19.323 righe di `bridge_title_category`, ciascuna portando il profilo della propria categoria |

**Perché `BQ1-K3` non pondera**: un intervallo è una proprietà dell'insieme dei profili assegnati, non della composizione del catalogo. Quante volte una categoria compaia non sposta né il minimo né il massimo.

**Perché `BQ2-K2` pondera, e sul ponte**: sul lato musicale il profilo del segmento è una mediana sulle **coppie**, e l'assegnazione titolo-categoria è l'omologo video della coppia. Aggregare un lato sulle appartenenze e l'altro sulle etichette metterebbe a confronto grandezze costruite in modo diverso, il che è precisamente ciò che una distanza non può fare.

**Conseguenza per la `007`**: `bridge_title_category` e `dim_category` entrano fra le tabelle di `BQ2-K2`, e non vi entrano per `BQ1-K3`. Il contratto **non** dice nulla su come i 42 profili vengano costruiti: quello è §7.

### 6.5 Che cosa la `007` eredita ancora aperto

| Questione | Origine | Perché non si chiude qui |
|---|---|---|
| a quale precisione si confrontano profilo e rendiconto | divergenza 1 della revisione `003` | il modello fissa **tipi di dato**, che è cosa diversa dal **criterio di confronto**. Fissare l'uno non decide l'altro |
| se le righe a durata degenere entrano nella mediana di `BQ1-K2` | marcatura `is_duration_zero` | è una decisione statistica, non strutturale. Il modello garantisce solo che la marcatura sia visibile alla misura |
| arrotondamento e precisione di presentazione di ogni misura | §5 di questo contratto, e `FR-015` della `004` per gli importi in euro | il modello non arrotonda per non decidere di nascosto |
| ogni misura sulla popolarità pubblica la quota di zeri del segmento | divergenza 6 della revisione `001` | è un obbligo di pubblicazione, non di struttura. Il modello lo rende **calcolabile**; pubblicarlo è della `007` |
| il peso relativo con cui `BQ2-K3` combina `BQ2-K1` e `BQ2-K2` | scheda di `BQ2-K3`, che impone di dichiararlo esplicitamente | è una scelta di composizione fra misure, non di struttura. Nessuno l'ha ancora fissata |
| che `BQ1-K2` confronti i soli film con l'intero catalogo musicale va dichiarato accanto al valore | nota di esclusione delle serie nella scheda del KPI | il modello conserva `type`, quindi la quota di film è calcolabile: manca l'obbligo di pubblicarla, che è della `007` e della `008` |

## 7. La tabella che la `006` riempie

`dim_category_mood` esiste nel modello con la forma dichiarata e **zero righe**. La `006` la riempie; nessuno la ridisegna.

| Colonna | Tipo | Vincolo |
|---|---|---|
| `category` | testo | chiave, e deve essere un membro di `catalogs.netflix_categories` |
| `mood_energy` | decimale 0-1 | asse energia di §5.3 |
| `mood_valence` | decimale 0-1 | asse positività di §5.3 |
| `mood_danceability` | decimale 0-1 | asse ritmo di §5.3 |

**Due obblighi non negoziabili**, che vincolano il contenuto della tabella:

1. **le tre colonne stanno sulla stessa scala del lato musicale.** È la condizione che rende il confronto di `BQ2-K2` una distanza fra grandezze commensurabili. Una scala diversa su un solo asse rende la distanza priva di significato senza produrre alcun errore visibile;
2. **la confidenza non sale.** La tabella è costruita dall'analista: è lo strato interpretativo che tiene `BQ1-K3`, `BQ2-K2` e `BQ2-K3` a confidenza **media**, e nessuna cura nella costruzione la porta ad alta.

**Due condizioni di dichiarazione**, che vincolano ciò che va scritto accanto alla tabella:

3. **copertura attesa totale**: 42 righe, una per categoria. Se la `006` decidesse di non coprirle tutte, l'obbligo effettivo non è la copertura ma la **dichiarazione** della scopertura, e le misure che leggono la tabella devono dire che cosa fanno sulle categorie mancanti;
4. **la decisione aperta `DA-1` resta aperta.** Questo contratto non dice né chi né come costruisca le righe: non è un vincolo, è la dichiarazione che un vincolo qui non viene posto.

**Che cosa la `006` non decide**: come i 42 profili si aggreghino in un profilo di catalogo. Lo fissa §6.4, e non è ridiscutibile riempiendo la tabella.

## 8. Che cosa questo contratto garantisce e cosa no

**Garantisce** che la `007` sappia, per ciascuno degli 8 KPI, su quale tabella calcolare, a che cosa si riferisce il risultato, e quale giunzione produrrebbe un numero sbagliato — senza riaprire il codice della pipeline e senza rileggere il business case.

**Garantisce** che la `006` conosca la forma esatta della tabella da riempire prima di cominciare, e che riempirla non richieda di modificare nulla di ciò che questa feature ha chiuso.

**Non garantisce che il modello funzioni.** Non è mai stato materializzato. Una direzione di filtro dichiarata sicura potrebbe rivelarsi ambigua, e una cardinalità dichiarata potrebbe non reggere al caricamento. Chi lo costruisce è il primo a provarlo.

**Non garantisce la correttezza delle misure.** Il modello rende **difficile** la giunzione sbagliata; non rende impossibile la misura sbagliata. Una misura scritta contro la tabella giusta con la logica sbagliata produce un numero sbagliato, e nessuno schema se ne accorge.

**Non copre BQ3.** I sei valori di scenario della `004` vivono in `reports/bq3_scenarios.json` e **non sono un fatto di questo modello**: non hanno una grana, non si aggregano e non si filtrano per segmento. Il modo in cui entrano nel report è una decisione della `007` o della `008`, e non è presa qui.

**Non copre il conteggio delle righe come misura di dimensione.** Il catalogo musicale era bilanciato per costruzione del campione; dopo la deduplicazione della `003` non lo è più — esistono 17 conteggi di righe distinti fra i segmenti, e il meno numeroso ne ha 904. Un conteggio per segmento produce oggi differenze **che sono un residuo della deduplicazione e non un segnale di mercato**. Il modello non può impedirlo, perché contare righe è l'operazione più naturale che un motore tabellare offre: può solo dichiararlo, e questa riga è la dichiarazione.
