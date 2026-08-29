# Gli operatori delle misure

Con quale regola ciascuno degli otto<!--#--> KPI del [business case](business_case.md) verrà calcolato — formula, grana, tabelle da cui legge, confidenza ereditata, limiti dichiarati — e le nove<!--#--> decisioni analitiche che quelle regole hanno richiesto di prendere. *(Nota in loco — 2026-08-22, feature `007b`: le decisioni sono ora undici<!--#-->, per l'aggiunta di `D10` e `D11`. Vedi la nota in coda a §10.)*

**Data**: 2026-08-21 · **Feature**: `007a` · **Stato**: concluso, [revisionato in contesto pulito](../specs/007a-kpi-operators/review.md)

---

## 1. Che cosa è questo documento, e che cosa non contiene

**Non contiene alcun valore dei KPI.** Ogni altro documento di questo progetto che pubblica misure pubblica anche dei numeri; questo pubblica la **regola** con cui un numero, quando la `007b` lo calcolerà, sarà difendibile invece che arbitrario.

Dove una decisione ha avuto bisogno di un esempio concreto, il numero citato è un **input già ancorato** da una feature precedente — mai un risultato di questa. È la proprietà che rende leggibile ogni cifra della pagina: se porta un'ancora, viene da un artefatto che esisteva prima; se porta il marcatore di non-misurato, non è un fatto sui dati. La grammatica è quella di [`convenzioni-marcatura.md`](convenzioni-marcatura.md).

**Perché gli operatori si scrivono prima delle misure, e in un documento invece che dentro una formula.** Un operatore sbagliato non produce un valore sbagliato: li produce **tutti** quelli che ne dipendono. E mentre una formula scritta dentro una misura è visibile solo a chi apre lo strumento di reporting, un operatore scritto qui è contestabile da chiunque legga il repository — compreso chi lo ha scritto, prima di aver visto un solo numero uscirne.

**Che cosa questo documento non garantisce**, e va saputo prima di leggerlo: che una formula ben argomentata produca un numero corretto. Riduce l'arbitrarietà della regola, non l'incertezza del risultato. I limiti stanno in §12.

---

## 2. `BQ1-K1` — `music_adjacent_catalog_share`

**Domanda di business**: BQ1 — Posizionamento · **Confidenza**: **alta**, invariata rispetto a [`business_case.md`](business_case.md) §5.4 · **Decisioni di riferimento**: `D9.1`, `D9.2`, `D9.3`

Questo KPI porta **due<!--#--> operatori distinti**, non due<!--#--> letture dello stesso numero: la quota di catalogo già musicale, e la condizione `C1` della regola di decisione della North Star (`business_case.md` §3). Hanno grana diversa e rispondono a domande diverse.

### 2.1 L'operatore della quota

**Formula**: numero di titoli distinti assegnati alla categoria `Music & Musicals`<!--@catalogs.netflix_categories_musical-->, diviso il numero totale di titoli distinti del catalogo video.

**Grana**: appartenenza titolo-categoria per il numeratore, titolo distinto per il denominatore. Il denominatore **non** è il conteggio delle assegnazioni: sono 8.807<!--@CL.NF.titles.rows.after--> titoli distinti contro 19.323<!--@CL.NF.category.assignments--> assegnazioni, e la scheda avvertiva già che confonderli è la trappola di questo KPI.

**Provenienza nel modello dati**: `dim_title` (titoli distinti), `bridge_title_category` (l'appartenenza), `dim_category` (l'etichetta) — [`data_model.md`](data_model.md) §8 e §10.2.

**`D9.3` — il rapporto non nasce per giustapposizione.** [`data_audit.md`](data_audit.md) pubblica il numeratore e il denominatore a poche righe dalla frase sulla North Star, senza calcolarne il rapporto. Quei due<!--#--> numeri sono **input**, non la misura: un rapporto costruito su valori misurati è esso stesso un valore misurato, e finché non è calcolato esplicitamente e ancorato con un proprio identificativo la misura non è stata pubblicata. È l'applicazione diretta della regola sulle affermazioni derivate ([`convenzioni-marcatura.md`](convenzioni-marcatura.md) §7), non una regola nuova introdotta qui.

`data_audit.md` non viola nulla — dichiara di non contenere KPI, ed entrambi i numeri che pubblica sono ancorati. Ciò che resta indefinito è solo il rapporto, e definirlo come operatore è ciò che questa sezione fa. **La misura nasce quando la `007b` lo calcola e lo ancora per la prima volta.**

**`D9.1` — perché il numeratore, letto sul dato di origine, regge sul trasformato.** Il numeratore esiste come identificativo soltanto in [`data_profile.json`](../reports/data_profile.json), che descrive il catalogo **di origine**: vale 375<!--@NF.cat.music_musicals.titles--> titoli. Il rendiconto della trasformazione non pubblica alcun conteggio di titoli per categoria, quindi sul dato trasformato — che è quello su cui il modello opera — il numeratore non ha oggi un'ancora propria.

La risposta non è ricontare, ma **dichiarare l'invariante**, sullo stesso schema già adottato per il conteggio dei segmenti in `data_model.md` §3.4. Regge su due<!--#--> fatti già ancorati:

- il numero di titoli distinti non cambia con la trasformazione: 8.807<!--@NF.shape.rows--> sull'origine e 8.807<!--@CL.NF.titles.rows.after--> sul trasformato coincidono;
- le uniche righe toccate dalla riparazione sono 3<!--@CL.NF.duration.repaired.rows-->, e sono state riparate per **spostamento di campo** — un valore di durata finito nel campo sbagliato, riportato al proprio — non per imputazione né per eliminazione (`data_model.md` §14, colonna `is_repaired_duration`). La riparazione tocca la durata, non l'assegnazione di categoria;
- il ponte titolo-categoria non cambia né per numero di righe né per numero di categorie: le assegnazioni sono 19.323<!--@NF.cat.assignments--> sull'origine e 19.323<!--@CL.NF.category.assignments--> sul trasformato, le categorie distinte 42<!--@NF.cat.count--> e 42<!--@CL.NF.category.distinct-->.

**Che cosa questi fatti dimostrano, e che cosa no.** Dimostrano che la trasformazione non altera la cardinalità del ponte su nessuna delle sue due<!--#--> dimensioni. **Non** dimostrano che la corrispondenza fra titoli e categorie sia rimasta identica riga per riga: due<!--#--> totali che coincidono sono compatibili, in linea di principio, con riassegnazioni che si compensano. Nessun artefatto pubblica oggi il conteggio dei titoli per categoria sul dato trasformato, quindi quel confronto non è eseguibile da qui.

**Ne discende che l'invarianza del numeratore è un'assunzione dichiarata, non una conseguenza dedotta** — un'assunzione che i fatti sopra rendono difficile da violare senza che uno di essi si muova, ma pur sempre un'assunzione. Chi la volesse chiudere davvero deve pubblicare il conteggio per categoria sul trasformato, che è l'operatore di §2.2 e appartiene alla `007b`: eseguendolo, la verifica esce quasi gratis, ed è il momento in cui va fatta. **L'operatore dichiara quindi la catena per intero** — numeratore letto dall'origine, assunzione di invarianza esplicita e sostenuta dai tre<!--#--> fatti qui sopra, denominatore letto indifferentemente da un lato o dall'altro perché coincidono — invece di citare il numeratore come se fosse già un valore del modello dati.

### 2.2 `D9.2` — l'operatore di `C1`, che non è la quota

`C1` chiede che «il contenuto musicale non sia residuale nel catalogo attuale: la sua categoria si colloca nella metà superiore delle categorie per numero di titoli» (`business_case.md` §3). **Non è calcolabile dalla quota**, che è una proporzione sull'intero catalogo: `C1` chiede una graduatoria delle categorie e la posizione di una di esse rispetto alla mediana.

**Formula**: per ciascuna delle 42<!--@CL.NF.category.distinct--> categorie del catalogo video, il numero di titoli si conta raggruppando per categoria le righe di `bridge_title_category`. `C1` è soddisfatta se il conteggio di `Music & Musicals`<!--@catalogs.netflix_categories_musical--> **supera** la mediana dei 42<!--@CL.NF.category.distinct--> conteggi — condizione stretta, per coerenza con la stessa convenzione adottata in §7.2 per i quadranti, non per una ragione nuova a sé.

**Grana**: categoria. La somma dei conteggi per categoria restituisce il numero di assegnazioni, 19.323<!--@CL.NF.category.assignments-->, non quello dei titoli distinti: è la stessa distinzione fra grana di appartenenza e grana del risultato che `data_model.md` §18 dichiara per i segmenti musicali, applicata qui al lato video. Ciascuna riga del ponte è per costruzione un titolo distinto in quella categoria — nessuna assegnazione duplicata, `data_model.md` §10.2 — quindi il raggruppamento non richiede alcuna deduplicazione ulteriore.

**Provenienza nel modello dati**: `bridge_title_category`, `dim_category`.

**La ragione della scelta sul conteggio**: la formulazione di `C1` chiede quanti titoli popolino ciascuna categoria, non quanti titoli distinti esistano nell'intero catalogo. Usare il conteggio globale, o una sua quota, confonderebbe una proprietà del catalogo con una proprietà di una singola categoria.

**Che cosa questo operatore non fa**: non calcola la posizione della categoria nella graduatoria. Nessun conteggio di titoli per categoria è oggi pubblicato in alcun artefatto, e produrlo è compito della `007b`.

---

## 3. `BQ1-K2` — `format_duration_gap`

**Domanda di business**: BQ1 — Posizionamento · **Confidenza**: **alta**, invariata rispetto a `business_case.md` §5.4 · **Decisione di riferimento**: D5, che chiude anche la parte residua di `R13` su questo KPI

**Formula**: `format_duration_gap` = durata mediana di una traccia musicale, in minuti, **meno** durata mediana di un film del catalogo video, in minuti.

**Che cosa la misura pubblica**: il risultato della sottrazione **con il proprio segno** — un numero di minuti, positivo o negativo. Non il suo valore assoluto, e **non** il solo segno: la grandezza fa parte della misura, il nome stesso del KPI la implica. Ciò che questa decisione fissa è il verso della sottrazione e il fatto che il segno che ne esce non venga soppresso.

**Grana**: traccia deduplicata sul lato musicale, film sul lato video. Le serie sono escluse per dichiarazione della scheda — il catalogo video le misura in stagioni e convertirle richiederebbe un'assunzione che i dati non contengono.

**Provenienza nel modello dati**: `dim_track` (lato musicale), `dim_title` filtrata ai soli film (lato video) — `data_model.md` §8.

**La ragione del verso.** BQ1 formula la domanda come il posizionamento del contenuto musicale **rispetto a** quello video: la musica è il soggetto del confronto, il video il termine di paragone. Sottrarre nella direzione musica meno video mantiene questa struttura — un valore negativo dice «una traccia dura, in mediana, questo tanto in meno di un film». Il verso opposto sarebbe stato ugualmente calcolabile: la scelta è dichiaratamente convenzionale, ma un verso va fissato e questo è coerente con come la domanda è scritta.

**La ragione per pubblicare il segno invece del valore assoluto.** La scheda dichiara che questo KPI **non ha direzione** — non è un obiettivo da massimizzare, è un profilo descrittivo. Il segno, qui, non porta alcun giudizio di valore: porta l'informazione su quale dei due<!--#--> formati sia più lungo, che andrebbe perduta pubblicando il solo valore assoluto della differenza. La direzione di cui la scheda parla è **normativa** (quale verso sia desiderabile), non **aritmetica** (quale sia il segno del numero), e le due<!--#--> cose non si escludono.

**Un limite atteso, dichiarato prima che il numero esista.** Un film dura tipicamente decine di minuti e una traccia pochi: il valore sarà quasi certamente fortemente negativo. Non è un'anomalia né un segnale di allarme — è la conseguenza aritmetica della differenza di formato che il KPI esiste per misurare, ed è scritto qui perché nessuno lo scambi per un errore quando il numero comparirà.

**Due<!--#--> vincoli ereditati che questa feature non chiude**, e che restano a carico di chi implementa (`data_model.md` §19):

- **se le righe a durata degenere entrino nella mediana.** La marcatura `is_duration_zero` esiste sulla dimensione delle tracce e vale su 1<!--@CL.SP.duration.zero.rows--> riga; il modello la rende leggibile ma non decide se includerla. Il perimetro di questa feature non comprende quella decisione: chi la prenderà deve dichiararla accanto al valore, non assorbirla in silenzio;
    *(Chiuso il 2026-08-22 dalla feature `007b` come decisione **`D11`**: le righe a durata degenere **entrano** nella mediana, per la stessa disciplina con cui `D7` tratta gli zeri di popolarità — la trasformazione ha scelto di conservare e marcare, non di eliminare. La variante esclusa è comunque calcolata, e la differenza fra le due<!--#--> è pubblicata in [`kpi_measures.md`](kpi_measures.md) §3.3 perché la decisione sia verificabile invece che dichiarata a parole.)*
- **l'asimmetria del confronto va dichiarata accanto al valore.** Il lato video contribuisce con i soli film, il lato musicale con l'intero catalogo. La quota di film sul catalogo video è calcolabile dal campo che distingue film e serie, e va pubblicata insieme al risultato perché il confronto sia leggibile.

---

## 4. `BQ1-K3` — `mood_profile_overlap`

**Domanda di business**: BQ1 — Posizionamento · **Confidenza**: **media**, invariata rispetto a `business_case.md` §5.4 · **Decisione di riferimento**: D1

**Formula**: quota di tracce del catalogo musicale il cui profilo sui tre<!--#--> assi di mood cade **dentro** l'intervallo occupato dal catalogo video, dove «dentro» significa: `mood_energy` nell'intervallo dell'asse energia **e** `mood_valence` nell'intervallo dell'asse positività **e** `mood_danceability` nell'intervallo dell'asse ritmo. I tre<!--#--> intervalli sono quelli già fissati da `data_model.md` §11 — minimo e massimo, senza ponderazione, sulle 42<!--@CL.NF.category.distinct--> righe di `dim_category_mood`, ciascun asse indipendentemente dagli altri.

Geometricamente è un **parallelepipedo allineato agli assi**: il prodotto cartesiano di tre<!--#--> intervalli scalari, verificato con un AND logico.

**Grana**: traccia deduplicata sul lato musicale; categoria sul lato video, aggregata in tre<!--#--> intervalli scalari.

**Provenienza nel modello dati**: `dim_track` (colonne `energy`, `valence`, `danceability`, lette senza trasformazione), `dim_category_mood` (colonne `mood_energy`, `mood_valence`, `mood_danceability`) — `data_model.md` §11.

**Perché il prodotto cartesiano e non un inviluppo convesso.** `data_model.md` §11 non costruisce, per questo KPI, alcuna struttura congiunta a tre<!--#--> dimensioni: non esiste in quel documento un elenco dei profili di categoria come punti nello spazio, da cui un inviluppo potrebbe nascere. Esiste soltanto il minimo e il massimo di ciascun asse preso da solo. Un inviluppo convesso richiederebbe una **quarta**<!--#--> regola di aggregazione — la costruzione dell'insieme dei profili come oggetto geometrico — che nessun documento precedente ha mai fissato, e introdurla qui significherebbe decidere in questa feature un pezzo di modello dati che il modello non contiene. Il prodotto cartesiano è l'unica lettura **direttamente costruibile** da ciò che §11 ha già chiuso.

**Il limite che la scelta introduce, dichiarato e non corretto.** Un parallelepipedo contiene sempre l'inviluppo convesso che vi si iscrive, e in genere lo eccede: include combinazioni dei tre<!--#--> assi che nessuna categoria video occupa realmente — per esempio un'energia pari a quella della categoria più energica insieme a una positività pari a quella della categoria più cupa, anche se nessuna categoria è insieme l'una e l'altra. La quota che questo KPI pubblicherà è quindi una **stima per eccesso** della sovrapposizione reale, non la misura più stretta possibile. Correggerlo richiederebbe la struttura congiunta che il modello dati non fornisce, ed è fuori dal perimetro di questa feature riaprirlo.

**Sul confine dell'intervallo.** Gli intervalli sono **chiusi**: un valore uguale al minimo o al massimo osservato conta come dentro. È coerente con il fatto che minimo e massimo sono essi stessi valori assegnati a una categoria reale, non limiti teorici.

**Vincolo ereditato dalla tabella dei mood.** Questo operatore presuppone la stabilità degli **assi** e dei loro **estremi ancorati**, non dei valori delle celle: il ritrovamento `CF-1` di [`content_taxonomy_bridge.md`](content_taxonomy_bridge.md) §3 è aperto — criterio §2 e criterio §5 si contraddicono su alcune etichette — e una revisione del criterio produrrà una versione successiva della tabella. *(Nota in loco — 2026-08-21, chore `criterio-mood-cf1`: `CF-1` è stato chiuso riscrivendo il criterio in nota a §2 e §5 di [`mood_assignment_criteria.md`](mood_assignment_criteria.md); vedi `docs/roadmap.md` § Debito della feature 006.)* La formula qui definita non ne è invalidata. Il valore che ne uscirà sì: per il contratto di versione di `content_taxonomy_bridge.md` §5, ogni valore pubblicato che dipende da `dim_category_mood` deve dichiarare su quale versione della tabella è stato calcolato — oggi la 2<!--@MOOD.table.version-->.

---

## 5. `BQ2-K1` — `segment_demand_index`

**Domanda di business**: BQ2 — Segmento di ingresso · **Confidenza**: **media**, invariata rispetto a `business_case.md` §5.4 · **Decisioni di riferimento**: D7, e D6 citata qui come esempio

**Formula**: mediana dell'indice di popolarità delle righe del segmento, sulla scala `0-100`. Accanto al valore, **obbligatoriamente**, la quota di righe a popolarità nulla del segmento (vedi sotto).

**Grana**: coppia traccia-segmento. La popolarità si legge dalla **tabella di fatto**, cioè il valore che la riga di *quel* segmento porta, mai dalla dimensione delle tracce: è la regola di lettura non negoziabile di `data_model.md` §12, e non un'opzione di questa feature. Prendere il valore alla grana traccia porterebbe dentro un segmento un valore osservato su una riga di un altro segmento.

**Provenienza nel modello dati**: `fact_track_segment` (colonne della popolarità e `is_popularity_zero`), `dim_segment` (colonna `is_high_zero_genre`) — `data_model.md` §12 e §14.

### 5.1 D7 — la quota di zeri accanto al valore, non al posto di esso

**L'operatore.** Ogni misura calcolata sulla popolarità **deve** pubblicare, accanto al proprio valore, la quota di righe a popolarità nulla del segmento: il conteggio delle righe con `is_popularity_zero` vero diviso il conteggio delle righe del segmento, calcolata su `fact_track_segment` alla stessa grana coppia traccia-segmento su cui la mediana opera. Dove il segmento porta `is_high_zero_genre` vero — cioè supera la soglia di `50.0`<!--@conventions.zero_share_threshold_pct--> per cento dichiarata dalla trasformazione — il valore pubblicato porta anche un **avvertimento testuale esplicito**, non solo il numero. I segmenti in quella condizione sono 7<!--@CL.SP.zero.high_genres.count-->.

**La ragione.** Una mediana calcolata su un segmento pieno di zeri è trascinata verso il basso da un difetto della fonte — una traccia priva di segnale di popolarità sulla piattaforma di origine, non priva di domanda reale — non da una debolezza di domanda del segmento. Pubblicare la quota accanto al valore permette a chi legge di fare quella distinzione da sé, invece di leggere una mediana bassa come «domanda bassa» quando potrebbe essere «molti zeri». Le righe a popolarità nulla sono 15.844<!--@CL.SP.zero.rows.after--> in tutto.

**Che cosa questa decisione non fa.** Non introduce alcuna correzione statistica della mediana — ricalcolarla escludendo gli zeri sarebbe una decisione diversa, già scartata dalla trasformazione, che ha deciso di **includere** le righe a popolarità nulla e di marcarle invece di eliminarle. Questo operatore si limita a rendere visibile, accanto al valore, il fatto che lo condiziona.

**L'avvertimento si pubblica anche quando la mediana è alta.** Che un segmento a forte concentrazione di zeri abbia comunque una mediana alta non riduce l'obbligo di dichiarare la concentrazione: la rende semmai più notevole, perché il valore è stato raggiunto nonostante il difetto della fonte.

### 5.2 Il campione non è più bilanciato, e questo è un fatto ereditato

Il catalogo musicale era bilanciato per costruzione del campione: ogni segmento portava 1.000<!--@SP.genre.rows_min--> righe. Dopo la trasformazione **non lo è più**: esistono 17<!--@CL.SP.recalc.genre.row_counts_distinct--> conteggi di righe distinti fra i segmenti, con il meno numeroso a 904<!--@CL.SP.recalc.genre.rows_min--> righe (`data_model.md` §18).

**Quanto lo scostamento sia ampio, questo documento non lo dice**, e l'omissione è deliberata: nessun artefatto pubblica il conteggio massimo né alcuna misura di dispersione, quindi affermare che lo squilibrio sia grande — o rassicurare che sia piccolo — sarebbe una valutazione senza fonte. Chi scrive la misura eredita il **fatto**, non un giudizio sulla sua entità.

Ne discende un vincolo operativo che vale comunque: il conteggio delle righe di un segmento misura il campionamento e non il mercato, e non va usato per dimensionare un segmento. È la ragione per cui questo KPI poggia sulla domanda e mai sull'offerta.

### 5.3 D6 — a quale precisione due valori dello stesso fatto si dicono diversi

Questa decisione non entra nella formula del KPI: entra in **qualunque confronto** fra il profilo di dati e il rendiconto di trasformazione sulle quote di zeri per segmento, cioè nel materiale che chi presenta questo KPI userà per raccontarne la storia. Sta qui perché è qui che serve.

**Il fatto.** [`data_profile.json`](../reports/data_profile.json) memorizza le quote di zeri per segmento a una cifra decimale; [`cleaning_report.json`](../reports/cleaning_report.json) le memorizza a quattro<!--#-->. Confrontandole a tutte e quattro<!--#--> le cifre, i segmenti «cambiati» fra le due<!--#--> versioni risultano 78<!--@CL.SP.zero.by_genre.changed-->; quelli effettivamente spostati di oltre mezzo punto percentuale sono 3<!--@CL.SP.zero.by_genre.moved_over_half_point-->.

**La decisione.** Due<!--#--> valori dello stesso fatto, registrati nei due<!--#--> artefatti, si considerano **diversi** — limitatamente al confronto delle quote di zeri per segmento fra quei due<!--#--> artefatti, e a nessun altro confronto — se e solo se la differenza assoluta fra i due<!--#--> supera 0,5<!--#--> punti percentuali — condizione stretta, quindi uno spostamento di esattamente mezzo punto **non** conta come cambiato. Sotto quella soglia la differenza si attribuisce alla precisione di rappresentazione, non a uno spostamento reale prodotto dalla trasformazione.

**La ragione.** La precisione a una cifra decimale del profilo è esatta **per costruzione** finché ogni segmento ha lo stesso numero tondo di righe del campione originale: la quota di zeri ha allora una sola cifra decimale possibile, e il profilo la registra senza perdita. Dopo la deduplicazione i segmenti non hanno più conteggi uniformi (§5.2), e il rendiconto usa quattro<!--#--> cifre per restare esatto sul nuovo denominatore — ma questo non rende il profilo sbagliato: lo rende **arrotondato al proprio grado di risoluzione**, che è la metà dell'unità minima rappresentabile a una cifra. La soglia scelta sta un ordine di grandezza sopra quel pavimento di arrotondamento, quindi non scambia un arrotondamento per un cambiamento; e sta ben sotto la dimensione degli spostamenti realmente osservati, quindi non nasconde un cambiamento vero dentro la soglia. Non è la soglia più stretta possibile, ed è dichiarata come scelta e non come unica lettura corretta: la funzione che deve svolgere è separare pulitamente le due<!--#--> popolazioni, e lo fa con margine su entrambi i lati.

**Il perimetro della soglia, che è stretto.** Vale **solo** per il confronto delle quote di zeri per segmento fra quei due<!--#--> artefatti. Non è una regola generale di confronto per altre coppie di valori del progetto: è espressa in punti percentuali e non ha significato su un confronto fra conteggi o fra medie di altra natura. Estenderla richiede una decisione esplicita, non l'applicazione automatica di questa.

**Conseguenza per chi cita il confronto**: il numero di segmenti cambiati, quando qualcuno lo pubblicherà, è quello che si ottiene applicando la soglia — e chi lo cita deve dichiarare la soglia accanto ad esso, per la stessa ragione per cui ogni affermazione derivata porta la propria fonte.

---

## 6. `BQ2-K2` — `segment_catalog_affinity`

**Domanda di business**: BQ2 — Segmento di ingresso · **Confidenza**: **media**, invariata rispetto a `business_case.md` §5.4 · **Decisione di riferimento**: D2

**Formula**: `segment_catalog_affinity` = `1 − d`, dove `d` è la **media delle tre<!--#--> distanze assolute per asse** fra il profilo del segmento e il profilo del catalogo video:

```
d = ( |energia_segmento − energia_video|
    + |positività_segmento − positività_video|
    + |ritmo_segmento − ritmo_video| ) / 3
```

**Grana**: coppia traccia-segmento sul lato musicale, assegnazione titolo-categoria sul lato video. I due<!--#--> profili sono quelli già fissati da `data_model.md` §11 — sul lato musicale la mediana di ciascun asse sulle coppie traccia-segmento, sul lato video la mediana di ciascun asse sulle 19.323<!--@CL.NF.category.assignments--> righe del ponte, ciascuna portando il profilo della propria categoria.

**Provenienza nel modello dati**: `fact_track_segment`, `dim_track`, `dim_segment` sul lato musicale; `bridge_title_category`, `dim_category`, `dim_category_mood` sul lato video — `data_model.md` §8 e §11.

**Perché la distanza media assoluta e non l'euclidea.** Ciascun asse vive già sul dominio `0-1`, quindi ciascun termine assoluto è già in `0-1` e la loro media vi resta automaticamente: **nessuna costante di normalizzazione è necessaria**. La distanza euclidea, per restare nella scala dichiarata, richiede invece di dividere per la radice del numero di assi — una costante che non discende dai dati ma dalla geometria dello spazio scelto, e che va decisa a parte. La media delle distanze assolute è l'unica delle alternative considerate la cui scala discende **direttamente** da quella degli assi di partenza, senza alcuna scelta ulteriore. È l'argomento che decide, e regge da solo.

**Un argomento che non regge, e che non viene usato.** Sarebbe comodo dire che l'euclidea assume una regola di **compensazione** fra gli assi — uno scostamento piccolo su un asse che bilancia uno grande su un altro — mentre la media delle distanze assolute non la assume. È falso, e va detto invece di essere lasciato implicito: qualunque aggregazione additiva è pienamente compensativa, e la media delle distanze assolute lo è quanto l'euclidea. Le due<!--#--> differiscono nel **profilo** della compensazione — l'euclidea pesa di più gli scostamenti grandi — non nella sua presenza.

**L'unica alternativa davvero non compensativa** sarebbe il massimo degli scostamenti per asse: due<!--#--> profili sono vicini solo se lo sono su **ogni** asse, e nessuno scostamento può essere bilanciato da un altro. Non è stata scelta perché produrrebbe un'affinità governata dal solo asse peggiore, scartando l'informazione degli altri due<!--#--> — un comportamento difendibile per un vincolo di ammissibilità, non per un indice che deve ordinare i segmenti in modo graduale. La scelta di un operatore compensativo è quindi **deliberata e dichiarata**, non un effetto collaterale non visto.

**Che cosa il vincolo dell'ancoraggio impone comunque.** `content_taxonomy_bridge.md` §7 dichiara che gli assi sono ancorati **solo agli estremi** e che nessun valore osservato calibra il centro della scala. Non è questo a scegliere fra le due<!--#--> metriche — nessuna delle due<!--#--> è sostenuta dall'ancoraggio più dell'altra — ma è ciò che vieta di leggere la grandezza assoluta del risultato come se avesse un significato proprio, come il paragrafo seguente dichiara.

**Che cosa la scelta non risolve, e non deve fingere di risolvere.** Resta vero, come `content_taxonomy_bridge.md` §7 dichiara, che la **grandezza assoluta** di `d` non ha un'interpretazione indipendente dal criterio di mood: sottrarre un profilo assegnato da uno osservato presuppone che uno stesso numero indichi la stessa posizione sull'asse su entrambe le scale, e questo è sostenuto solo agli estremi. Ciò che questo operatore garantisce è che `d` sia calcolabile e **confrontabile con sé stessa fra segmenti diversi**, che è l'unica proprietà su cui §7 di questo documento può contare.

**Vincolo ereditato dalla tabella dei mood.** Come in §4: l'operatore presuppone la stabilità degli assi e dei loro estremi ancorati, non dei valori delle celle, aperti per `CF-1`. *(Nota in loco — 2026-08-21, chore `criterio-mood-cf1`: `CF-1` chiuso, vedi la nota a §4.)* Il valore che ne uscirà dichiara su quale versione della tabella è stato calcolato — oggi la 2<!--@MOOD.table.version-->.

---

## 7. `BQ2-K3` — `segment_entry_priority`

**Domanda di business**: BQ2 — Segmento di ingresso · **Confidenza**: **media**, invariata rispetto a `business_case.md` §5.4 — eredita il livello dei due<!--#--> KPI che compone, entrambi a media · **Decisioni di riferimento**: D3, D4, D8

Questo KPI **non legge alcuna tabella**: compone i due<!--#--> precedenti (`data_model.md` §8). Eredita perciò per intero la loro provenienza e i loro limiti. In particolare, attraverso `segment_catalog_affinity`, **presuppone la stabilità degli assi e dei loro estremi ancorati, non dei valori delle celle** di `dim_category_mood`, aperti per il ritrovamento `CF-1`. *(Nota in loco — 2026-08-21, chore `criterio-mood-cf1`: `CF-1` chiuso, vedi la nota a §4.)* La graduatoria che pubblicherà dichiara su quale versione della tabella è stata calcolata — oggi la 2<!--@MOOD.table.version-->.

Pubblica **due<!--#--> valori distinti per segmento**, con ruoli diversi e non intercambiabili.

### 7.1 D3 — la scala comune, e poi i pesi

I due<!--#--> ingredienti non sono commensurabili come stanno: la domanda è un indice `0-100`, l'affinità un indice `0-1`. Comporli richiede prima una scelta di scala, poi una scelta di peso.

**La scala**: la domanda si porta su `0-1` **per divisione per il proprio massimo teorico**, non per riscalamento sui valori minimo e massimo effettivamente osservati fra i segmenti. La ragione: è un indice delimitato per definizione, non un valore osservato senza limite superiore noto, quindi dividerlo per il proprio massimo è un'operazione fissa. Un riscalamento sui valori osservati renderebbe invece il punteggio composito di ogni segmento dipendente dal segmento più — o meno — domandato del gruppo, cioè una ridefinizione implicita ogni volta che l'insieme dei segmenti cambiasse. Qui l'insieme non cambia, i segmenti sono 114<!--@SP.genre.count-->; la divisione fissa evita comunque una dipendenza che non serve a nulla.

**I pesi**: **0,5<!--#--> e 0,5<!--#-->**. Non hanno alcun rapporto con la soglia di §5.3, che porta lo stesso numero per coincidenza: quella è una soglia di confronto in punti percentuali, questi sono i coefficienti di una combinazione lineare.

```
segment_entry_priority_score = 0,5 × domanda_normalizzata + 0,5 × affinità
```

**La ragione dei pesi uguali.** Nessun criterio esterno a questo progetto stabilisce che la domanda debba contare più o meno dell'affinità di catalogo per l'ingresso in un nuovo verticale, e la formulazione stessa di BQ2 (`business_case.md` §4) elenca le due<!--#--> dimensioni senza qualificarne una come primaria. In assenza di un argomento che favorisca l'una o l'altra, dichiarare un peso diverso sarebbe un **giudizio di business** che questa feature non ha titolo a prendere — introdurrebbe una preferenza che nessuna feature precedente ha argomentato e che nessuno ha espresso. Il peso uguale è quindi la scelta che **non aggiunge** un'assunzione non richiesta, non quella che si presume neutra in astratto: è dichiarata come tale, resta contestabile, e chi volesse un peso diverso deve portare una ragione di business esplicita.

### 7.2 D4 — il quadrante e il punteggio, entrambi

**L'appartenenza al quadrante** (booleana, per segmento): un segmento è «alta domanda, alta affinità» se la sua domanda è **sopra la mediana** dei 114<!--@SP.genre.count--> segmenti **e** la sua affinità è sopra la mediana degli stessi. La soglia è stretta: un segmento esattamente sulla mediana non entra nel quadrante alto. È un caso limite raro, dato che gli indici sono continui, ma va deciso perché altrimenti resterebbe implicito in chi implementa.

**Il punteggio pesato e la graduatoria** (continui, per segmento): `segment_entry_priority_score` di §7.1, che ordina tutti i segmenti in una posizione.

**Perché entrambi e non una scelta fra i due<!--#-->.** Rispondono a domande diverse. Il quadrante decide **se** un segmento supera una soglia doppia, ed è insensibile a quanto sopra la soglia si trovi: è lo strumento che opera direttamente la condizione `C3` della regola di decisione della North Star — «esiste almeno un segmento musicale che si colloca contemporaneamente nella metà superiore per domanda e nella metà superiore per affinità» (`business_case.md` §3) — a cui serve una risposta verificabile per sì o per no. Il punteggio decide **quanto** un segmento sia preferibile a un altro, anche fra due<!--#--> segmenti entrambi dentro o entrambi fuori dal quadrante: è ciò che la scheda chiede alla lettera, «posizione in graduatoria», e che una risposta binaria non produce.

Fondere i due<!--#--> in un solo numero — leggere «punteggio alto» come sinonimo di «nel quadrante» — nasconderebbe che un segmento può avere un punteggio alto restando **fuori** dal quadrante, per esempio con affinità molto alta e domanda appena sotto la mediana. È esattamente la distinzione che `C3` chiede di preservare.

**Conseguenza per chi implementa**: la misura pubblica entrambi i valori per ciascun segmento, non un valore unico che li confonda.

### 7.3 D8 — la direzione della graduatoria

La scheda dichiara «posizione alta = candidato migliore», che per una graduatoria è ambiguo: non dice se il candidato migliore occupi la prima posizione o quella con il punteggio numerico più alto. Era la parte residua di `R13` su questo KPI.

**La decisione**: la graduatoria ordina i segmenti per punteggio **decrescente**, e la prima posizione è quella del segmento con il punteggio più alto.

**La ragione**: è la lettura che rende letteralmente vero il testo già pubblicato nel business case, dove «posizione alta» significa alta in importanza e non alta come indice numerico di rango. La lettura opposta esisterebbe solo per una convenzione contraria, che nessuna scheda del business case adotta altrove. Dichiararlo qui chiude l'ambiguità senza toccare il testo del business case, che non era sbagliato — solo sotto-specificato.

**Un vincolo di presentazione, non di calcolo**: la graduatoria ha una voce per segmento, quindi 114<!--@SP.genre.count--> voci, che sono molte per una lettura a colpo d'occhio. È un problema della dashboard, non di questo operatore (`data_model.md` §19).

---

## 8. `BQ3-K1` — `premium_tier_adoption_rate`

**Domanda di business**: BQ3 — Impatto stimato · **Confidenza**: **bassa**, invariata rispetto a `business_case.md` §5.4 · **Decisione di riferimento**: nessuna

**Questo KPI non riceve alcun operatore nuovo qui, e l'assenza è dichiarata invece che lasciata dedurre.** È già derivato per intero dalla feature che ha prodotto gli scenari: formula, ancoraggio del valore centrale a un benchmark pubblico, fattori che generano i tre<!--#--> scenari, note d'unità e limiti vivono in [`bq3_scenarios.md`](bq3_scenarios.md) e nell'artefatto [`bq3_scenarios.json`](../reports/bq3_scenarios.json).

**Perché compare comunque in questo documento.** Un elenco parziale degli otto<!--#--> KPI lascerebbe chi legge a chiedersi se i due<!--#--> mancanti siano stati trattati o dimenticati. Questa sezione esiste per distinguere i due<!--#--> casi, esattamente come `data_model.md` §8 dichiara fuori dal modello le righe di BQ3 invece di ometterle.

**Che cosa resta vincolante da qui in avanti**: la confidenza è **bassa** e non sale — il valore dipende interamente dalle assunzioni di scenario e va sempre presentato come intervallo, mai come valore singolo. Il tasso è **lordo**: le disdette sono fuori dal perimetro del progetto, ed è la chiusura della parte BQ3 di `R13`.

---

## 9. `BQ3-K2` — `arpu_uplift`

**Domanda di business**: BQ3 — Impatto stimato · **Confidenza**: **bassa**, invariata rispetto a `business_case.md` §5.4 · **Decisione di riferimento**: nessuna

Come il precedente: **nessun operatore nuovo qui**, la derivazione è già chiusa per intero in `bq3_scenarios.md`.

**Che cosa resta vincolante da qui in avanti**, perché è la parte più facile da perdere leggendo la sola formula: l'unità è **euro per utente al mese** e **non è scalabile** — nessuna base utenti è quantificata in questo progetto, e moltiplicare l'uplift per una dimensione di base produrrebbe un totale che nessuno ha misurato, presentato con l'autorevolezza di uno misurato. L'uplift è inoltre **a regime**, non cumulato sull'orizzonte: moltiplicarlo per la durata dell'orizzonte dà un cumulato che vale solo sotto l'assunzione di base costante.

---

## 10. Le nove decisioni, in sintesi

> **Nota in loco — 2026-08-22, feature `007b`.** Il titolo dice nove<!--#--> e la tabella ne elenca ora undici<!--#-->. Il titolo non viene riscritto: era esatto quando la `007a` lo ha scritto, e le due<!--#--> decisioni aggiunte — `D10` sulla convenzione di mediana, `D11` sulle righe a durata degenere — sono state prese dalla `007b` e non dalla feature che possiede questa pagina. Chi conta le decisioni conti le righe della tabella, che è la forma autorevole; il titolo registra quante ne aveva la stesura originale.

> **Nota in loco — 2026-08-29, feature `009`, issue `#17`.** La tabella ne elenca ora dodici<!--#-->, per l'aggiunta di `D12` — l'operatore della condizione `C2`, argomentato per esteso nella nota in coda a §12. La regola resta quella dichiarata dalla nota precedente e non viene ripetuta altrove: **il conteggio autorevole sono le righe della tabella**, e ogni altra cifra su questa pagina — nel sommario, in §12, in §13 — registra quante decisioni esistevano quando quella frase è stata scritta. Nessuna di quelle frasi viene riscritta.

| | Che cosa fissa | Da dove viene | Dove è applicata |
|---|---|---|---|
| **D1** | appartenenza all'intervallo occupato come prodotto cartesiano di tre<!--#--> intervalli scalari | revisione `001`, divergenza 2 | §4 |
| **D2** | distanza come media delle distanze assolute per asse; affinità come complemento | revisione `001`, divergenza 3 | §6 |
| **D3** | scala comune per divisione per il massimo teorico; pesi uguali | revisione `001`, divergenza 4 | §7.1 |
| **D4** | quadrante **e** punteggio pesato, con ruoli distinti | revisione `001`, divergenza 4 | §7.2 |
| **D5** | verso della sottrazione musica meno video; risultato pubblicato con il proprio segno; chiude anche la parte di `R13` su `BQ1-K2` | revisione `001`, divergenza 8 (parte residua) e `R13` | §3 |
| **D6** | soglia di mezzo punto percentuale per dire «cambiato», limitata al confronto delle quote di zeri | revisione `003`, divergenza 1 | §5.3 |
| **D7** | quota di popolarità nulla obbligatoria accanto a ogni misura sulla popolarità | revisione `001`, divergenza 6 | §5.1 |
| **D8** | prima posizione della graduatoria = punteggio più alto | revisione `001`, `R13` (parte residua su `BQ2-K3`) | §7.3 |
| **`D9.1`** | invarianza del numeratore sul dato trasformato, dichiarata come assunzione e sostenuta da tre<!--#--> fatti ancorati | revisione `001` §3 | §2.1 |
| **`D9.2`** | operatore della condizione `C1`: conteggio dei titoli per categoria sul ponte, soglia mediana stretta | revisione `001` §3 | §2.2 |
| **`D9.3`** | il rapporto della North Star non è pubblicato per giustapposizione dei suoi due<!--#--> input | revisione `002`, divergenza 4 | §2.1 |
| **`D10`** | convenzione di mediana: ordinamento, media aritmetica dei due<!--#--> valori centrali su conteggio pari, nessun trattamento speciale dei pari merito | feature `007b`, issue `#7` | §2.2, §3, §5, §6, §7 |
| **`D11`** | le righe a durata degenere entrano nella mediana di `BQ1-K2`, con la variante esclusa calcolata e la differenza pubblicata | feature `007b`, §12 | §3 |
| **`D12`** | operatore della condizione `C2`: soglia di maggioranza semplice a 0,50<!--#-->, confronto **stretto** | feature `009`, issue `#17` | §12, nota in loco |

**Nessuna di queste decisioni pretende di essere l'unica difendibile.** Ciascuna dichiara le opzioni scartate e la ragione dello scarto; sono scelte argomentate, non deduzioni univoche. È il motivo per cui la pagina è stata sottoposta a una revisione in contesto pulito prima di essere considerata definitiva.

---

## 11. Provenienza e confidenza

Questa feature non introduce alcuna nuova fonte e **non altera alcuna classificazione di confidenza**: la tabella riporta quella già fissata da `business_case.md` §5.4.

| KPI | Nome semantico | Fonte | Confidenza | Formato | Operatore fissato da |
|---|---|---|---|---|---|
| `BQ1-K1` | `music_adjacent_catalog_share` | Netflix (reale) | alta | valore puntuale | D9 |
| `BQ1-K2` | `format_duration_gap` | Derivato (Netflix + Spotify) | alta | valore puntuale | D5, che chiude anche la parte residua di `R13` su questo KPI |
| `BQ1-K3` | `mood_profile_overlap` | Derivato (Netflix + Spotify) | media | valore puntuale con nota | D1 |
| `BQ2-K1` | `segment_demand_index` | Spotify (reale) | media | valore puntuale con nota | D7, D6 |

> **Nota in loco — 2026-08-22, feature `007b`, issue `#8`.** La riga di `BQ2-K1` dichiara l'operatore fissato da **`D7, D6`**. L'attribuzione di `D6` è **errata**, e la contraddice §5.3 di questa stessa pagina, che apre dichiarando: «questa decisione non entra nella formula del KPI». `D6` fissa una soglia di confronto fra due<!--#--> artefatti sulle quote di zeri per segmento; non fissa alcun operatore, e il perimetro che §5.3 le assegna è esplicitamente stretto. **Valore corretto della cella: `D7`.** La causa della divergenza è di prossimità — `D6` è argomentata dentro la sezione di `BQ2-K1` perché è lì che serve a chi presenta il KPI, e la tabella l'ha letta come se ne facesse parte. La cella non viene riscritta: il testo originale è la traccia di ciò che la `007a` aveva pubblicato, ed è esso stesso un dato. Fonte verificabile: §5.3, primo capoverso.
| `BQ2-K2` | `segment_catalog_affinity` | Derivato (Netflix + Spotify) | media | valore puntuale con nota | D2 |
| `BQ2-K3` | `segment_entry_priority` | Derivato (`BQ2-K1` + `BQ2-K2`) | media | ordinamento | D3, D4, D8 |
| `BQ3-K1` | `premium_tier_adoption_rate` | Sintetico | bassa | range best/base/worst | nessuno nuovo |
| `BQ3-K2` | `arpu_uplift` | Derivato (`BQ3-K1` + prezzi assunti) | bassa | range best/base/worst | nessuno nuovo |

**Perché la confidenza non può salire qui.** È un fatto deciso a monte, dal business case ed ereditato dal modello dati. Per i tre<!--#--> KPI che dipendono da `dim_category_mood` — `BQ1-K3`, `BQ2-K2` e, attraverso quest'ultimo, `BQ2-K3` — l'obbligo è esplicito e non negoziabile (`data_model.md` §15): la tabella è costruita dall'analista, non osservata, e nessuna cura nella costruzione di un operatore la sposta di classe. **La cura riduce l'arbitrarietà della formula, non la natura del dato.**

**Le assunzioni dietro le decisioni**, dichiarate per iscritto:

1. **indipendenza per asse** (D1, D2): l'appartenenza all'intervallo e la distanza fra profili trattano i tre<!--#--> assi come indipendenti, senza compensazione geometrica fra loro. È l'assunzione minima coerente con l'ancoraggio solo agli estremi, e non è verificata da alcun dato perché nessun dato la potrebbe verificare — il centro della scala non è ancorato;
2. **equipeso** (D3): domanda e affinità pesano allo stesso modo, per assenza di un criterio esterno che le differenzi;
3. **soglia mediana** (D4): «alta domanda» e «alta affinità» significano «sopra la mediana dei segmenti», non un valore assoluto — coerente con la formulazione ordinale di `business_case.md` §4.

---

## 12. Limiti dichiarati

**Non risponde a**: quale sia il valore di alcun KPI. Chi lo cercasse qui non lo troverà, e non per omissione.

**Non risponde a**: se le decisioni prese siano le uniche difendibili. Vedi §10.

**Un operatore fissato non è un valore verificato.** Che una formula sia ben argomentata non garantisce che il numero che ne uscirà sia corretto: resta da implementarla, da verificarla contro un motore reale, e da sottoporla alla propria revisione. Questo documento riduce l'arbitrarietà della formula, non l'incertezza del risultato.

**Il prodotto cartesiano di §4 non è la misura più stretta possibile.** Il valore che ne uscirà sovrastima la sovrapposizione reale rispetto a un inviluppo convesso. Non è un errore: è un limite strutturale della scelta, e la ragione per cui la scelta è stata fatta sta in §4.

**La distanza di §6 non è confrontabile con una distanza osservata altrove.** La sua grandezza assoluta ha senso solo relativamente ad altri segmenti calcolati con la stessa formula sugli stessi assi.

**Tre<!--#--> vincoli restano aperti e non li chiude questa feature.** Sono elencati in `data_model.md` §19 fra quelli assegnati alle misure, e questa pagina li registra come residui invece di deciderli fuori dal proprio perimetro:

- se le righe a durata degenere entrino nella mediana di `BQ1-K2` (§3);
- l'asimmetria di `BQ1-K2`, che confronta i soli film con l'intero catalogo musicale, da dichiarare accanto al valore (§3);
- l'arrotondamento e la precisione di presentazione di ciascuna misura.

Chi li chiuderà deve dichiararlo dove chiude, non assorbirli in silenzio.

> **Nota in loco — 2026-08-22, feature `007b`.** I tre<!--#--> vincoli sono chiusi. Il testo sopra non viene riscritto: era vero quando è stato scritto, e la traccia di che cosa la `007a` aveva lasciato aperto è essa stessa un dato. Dove ciascuno si chiude:
>
> - **la durata degenere** — decisione **`D11`**: le righe marcate `is_duration_zero` **entrano** nella mediana, per coerenza con `D7`. Entrambe le varianti sono calcolate e la loro differenza è pubblicata, in [`kpi_measures.md`](kpi_measures.md) §3.3;
> - **l'asimmetria di `BQ1-K2`** — la quota di titoli `Movie` sul catalogo video è pubblicata accanto al valore, in [`kpi_measures.md`](kpi_measures.md) §3.4. Il vincolo chiedeva di dichiararla, non di valutarla, e nessun giudizio sulla sua entità viene aggiunto;
> - **l'arrotondamento e la precisione** — una convenzione unica **per unità di misura** e non per KPI, dichiarata nella tabella di [`kpi_measures.md`](kpi_measures.md) §1.2 e nella convenzione `kpi_rounding` di [`reports/kpi_measures.json`](../reports/kpi_measures.json): `Decimal` ovunque, `ROUND_HALF_UP` esplicito, e l'arrotondamento applicato solo alla presentazione, mai prima di una mediana o di un confronto di soglia.
>
> **Un quarto vincolo si chiude qui**, e non era in questo elenco perché la `007a` non lo aveva riconosciuto come tale: la **convenzione di mediana su conteggio pari**, aperta come issue `#7` mentre quattro<!--#--> operatori di questa pagina già la usavano. È la decisione **`D10`** — ordinamento, media aritmetica dei due<!--#--> valori centrali su conteggio pari, nessun trattamento speciale dei pari merito.

> **Nota in loco — 2026-08-29, feature `009`, issue `#17`. La decisione `D12`: l'operatore di `C2`.** Questa pagina fissa gli operatori degli otto<!--#--> KPI e quello della condizione `C1` (§2.2), ma **non fissa quello di `C2`**. La condizione è formulata da `business_case.md` §3 come «i profili di mood dei due<!--#--> cataloghi si sovrappongono per la **maggioranza** del catalogo musicale», e «maggioranza» non è un operatore: non dichiara né la soglia né la strettezza del confronto. Finché resta così, `C2` non è calcolabile, e il verdetto della regola di decisione non è pubblicabile. **La decisione si prende qui**, dove vivono le altre undici<!--#-->, invece che dentro il documento che la applica.
>
> **La soglia è 0,50<!--#-->**, cioè la maggioranza semplice: più della metà del catalogo musicale. È la lettura letterale del termine, ed è quella che il business case può aver inteso avendo fissato la regola prima che i numeri esistessero — una soglia più severa, due<!--#--> terzi o tre<!--#--> quarti, sarebbe una stipulazione introdotta dopo aver visto il valore, che è precisamente la manovra che una regola fissata in anticipo esiste per impedire.
>
> **Il confronto è stretto**: `C2` è soddisfatta se la quota di sovrapposizione **supera** la soglia, non se la eguaglia. Non è una scelta nuova: è la stessa convenzione già adottata da `D9.2` per `C1` e da `D4` per il quadrante di `BQ2-K3`. Le tre<!--#--> condizioni della regola di decisione si leggono insieme, e leggerne una con una convenzione di confine diversa dalle altre due<!--#--> sarebbe una differenza senza ragione.
>
> **La scelta fra stretto e largo non cambia l'esito su questi dati.** La quota misurata, 0,8450<!--@KPI.BQ1K3.overlap_share-->, non cade sulla soglia: sta sopra con entrambe le convenzioni, e il caso di confine che le distingue non si presenta. La decisione è quindi presa per coerenza con `D9.2` e `D4`, non perché l'esito ne dipenda — e dichiararlo è ciò che impedisce di leggerla come una scelta fatta per ottenere il risultato.
>
> **Ciò che invece dalla soglia dipende è il margine.** La distanza fra il valore e la soglia — che `kpi_measures.md` pubblica come `KPI.BQ1K3.c2.margin` e che la raccomandazione usa per dire quanto la stima dovrebbe sovrastimare perché `C2` cada — **si restringe se la soglia è più severa**: con una soglia a due<!--#--> terzi varrebbe meno della metà di quanto vale con la maggioranza semplice. «Inconseguente per l'esito» e «inconseguente per il margine» sono due<!--#--> affermazioni diverse, e solo la prima è vera. Ogni pubblicazione del margine dichiara perciò la soglia da cui è misurato.
>
> **Che cosa questa decisione non fa**: non ricalcola `BQ1-K3`, il cui operatore resta `D1` e il cui valore resta quello pubblicato dalla `007b`. `D12` fissa soltanto come quel valore si legge come condizione. Il limite di `D1` — il prodotto cartesiano sovrastima la sovrapposizione reale, dichiarato tre<!--#--> capoversi sopra — si trasmette intatto a `C2`, ed è la ragione per cui `C2` è la più debole delle tre<!--#--> condizioni.

**Copertura del dato**: questa pagina eredita per intero i limiti già dichiarati dal business case e da `data_model.md` §18 — cataloghi proxy, non StreamWave; copertura temporale ferma agli anni dichiarati dalle assunzioni strutturali; nessun dato comportamentale. Non ne introduce di nuovi, perché non tocca alcun dato.

**Dove è esposto a chi legge la dashboard**: da nessuna parte. Questo è un documento tecnico. I limiti di §4, §6 e §7.2 devono essere ereditati e ripresentati in forma comprensibile da chi costruirà la narrazione, dove il lettore della dashboard li incontra.

---

## 13. Come si verifica

```bash
# ogni cifra ancorata di questa pagina contro gli artefatti versionati
python3 scripts/check_audit_coherence.py
```

Il controllo scandisce questa pagina in **severità stretta**: ogni quantità priva di ancora o di marcatore di non-misurato è un errore, non un avviso.

**Che cosa l'esito verde certifica, e che cosa no.** Certifica che ogni numero ancorato coincida con il valore dell'artefatto che lo produce. Non può accorgersi di un'affermazione che *avrebbe dovuto* essere ancorata, né impedire che un fatto misurato venga dichiarato non-misurato — contro la dichiarazione falsa esiste la revisione in contesto pulito, non il controllo. Soprattutto: **nessun controllo automatico verifica l'argomentazione**, che è la sostanza di questa pagina. Le undici<!--#--> decisioni sono difendibili o non lo sono per ragioni che nessuno script può leggere.
