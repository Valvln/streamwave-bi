# Feature Specification: Operatori delle misure

**Feature Branch**: `007a-kpi-operators`

**Created**: 2026-08-21

**Status**: Draft

**Input**: User description: "Definire per intero, per ciascuno degli 8 KPI del business case, l'operatore analitico con cui ciascuna misura verrà calcolata, senza calcolare alcun valore. Deliverable unico: `docs/kpi_operators.md`. Chiude sette decisioni analitiche ereditate e mai prese — intervallo occupato (`BQ1-K3`), metrica di distanza (`BQ2-K2`), pesi e commensurabilità (`BQ2-K3`), quadranti contro combinazione pesata (`BQ2-K3`), segno della differenza (`BQ1-K2`), precisione del confronto, trattamento degli zeri — più due voci minori: la direzione residua di `R13` e se pubblicare numeratore/denominatore della North Star equivalga a pubblicare la misura (divergenza 4 della revisione `002`). Nessuna implementazione DAX, nessuna apertura di Power BI, nessuna esecuzione della pipeline."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come decisione, requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

---

## La domanda a cui questa spec risponde per prima

Ogni altro documento di questo progetto pubblica un numero. Questo non ne pubblica nessuno: pubblica la **regola** con cui un numero, quando qualcun altro lo calcolerà, sarà difendibile invece che arbitrario. È la stessa distinzione che la `006` ha fatto per il profilo di mood — criterio prima, valore dopo — applicata qui non a 126 celle assegnate da una persona, ma a otto formule che il business case ha lasciato sotto-specificate fin dalla prima revisione.

La ragione per cui questo lavoro è una feature a sé, e non un dettaglio che la `007b` avrebbe deciso scrivendo la misura DAX: un operatore sbagliato non produce un valore sbagliato, li produce **tutti** quelli che ne dipendono, e mentre una formula scritta dentro una misura è visibile solo a chi apre Power BI, un operatore scritto in un documento è contestabile da chiunque legga il repository — compreso chi lo scrive, prima di aver visto un solo numero uscirne. Nessuna delle sette decisioni che seguono guarda un risultato: tutte guardano solo la definizione dei KPI in `docs/business_case.md` §5.5, il modello dati in `docs/data_model.md`, e i vincoli che le feature precedenti hanno lasciato scritti.

---

## Le decisioni che questa spec prende

Sono nove: le sette ereditate dal prompt di consegna, più due voci minori che lo stesso prompt assegna a questo documento. Ciascuna riporta il rilievo o la divergenza che l'ha sollevata, le opzioni sul tavolo, la decisione presa, la sua ragione.

**Le quattro più esposte** — intervallo occupato (D1), metrica di distanza (D2), pesi e commensurabilità (D3), quadranti contro combinazione pesata (D4) — sono quelle che il prompt di consegna nomina esplicitamente al terzo punto di stop del flusso. Compaiono per prime.

---

### D1 — Intervallo occupato (`BQ1-K3`): prodotto cartesiano di tre intervalli scalari indipendenti

**Il contesto**: divergenza 2 della revisione `001` — «min-max, intervallo interquartile o altra copertura; e appartenenza verificata asse per asse oppure come regione congiunta sui tre assi». La scheda di `BQ1-K3` (`business_case.md` §5.5) chiede la quota di tracce che «cade all'interno dell'intervallo occupato dai generi del catalogo video sui tre assi». `docs/data_model.md` §11 ha già chiuso metà della domanda: per `BQ1-K3` l'aggregazione è «minimo e massimo sulle 42 righe di `dim_category_mood`, senza ponderazione» — **per ciascun asse, indipendentemente**. Non un inviluppo congiunto: tre intervalli scalari separati, `[min_e, max_e]`, `[min_v, max_v]`, `[min_d, max_d]`.

Resta aperta l'altra metà: come un punto a tre coordinate — il profilo di una traccia musicale su energia, positività, ritmo — decide se sta «dentro».

**Le opzioni**: (a) **prodotto cartesiano** — la traccia è dentro se e solo se ciascuna delle tre coordinate cade nel proprio intervallo scalare, indipendentemente dalle altre due: geometricamente, un parallelepipedo allineato agli assi; (b) **inviluppo convesso** — costruito sui 42 punti `(mood_energy, mood_valence, mood_danceability)` di `dim_category_mood`, una regione più stretta che scarta gli angoli del parallelepipedo dove nessuna categoria reale si trova; (c) altra costruzione congiunta (es. un ellissoide di covarianza).

**La decisione**: **(a), prodotto cartesiano**. Una traccia cade nell'intervallo occupato se e solo se `mood_energy ∈ [min_e, max_e]` **e** `mood_valence ∈ [min_v, max_v]` **e** `mood_danceability ∈ [min_d, max_d]`, i tre intervalli quelli già fissati da `data_model.md` §11.

**La ragione**: `data_model.md` §11 non costruisce, per `BQ1-K3`, alcuna struttura congiunta a tre dimensioni — non esiste, in quel documento, un elenco dei 42 punti `(e, v, d)` da cui un inviluppo potrebbe nascere; esiste solo il minimo e il massimo di ciascun asse preso da solo. Un inviluppo convesso richiederebbe una **quarta** regola di aggregazione — la costruzione dell'insieme dei 42 punti come oggetto geometrico — che nessun documento precedente ha mai fissato, e introdurla qui significherebbe decidere in questa feature un pezzo di modello dati che il suo documento non contiene. Il prodotto cartesiano è invece l'unica lettura **direttamente costruibile** da ciò che `data_model.md` §11 ha già chiuso: tre intervalli scalari, combinati con un AND logico.

**Il limite che la decisione introduce, dichiarato e non nascosto**: un prodotto cartesiano è per costruzione **più permissivo** di un inviluppo convesso che lo stesso insieme di punti genererebbe — il parallelepipedo contiene sempre l'inviluppo che vi si iscrive, e in genere lo eccede, includendo combinazioni dei tre assi che nessuna categoria video occupa realmente (per esempio, energia alta come nella categoria più energica ma positività bassa come nella categoria più cupa, anche se nessuna categoria video è insieme la più energica e la più cupa). La quota di tracce «dentro» che `BQ1-K3` pubblicherà è quindi una **stima per eccesso** della sovrapposizione reale, non la misura più stretta possibile. Il documento lo dichiara come limite, non lo corregge: correggerlo richiederebbe la struttura a 3D che `data_model.md` non fornisce, ed è fuori dal perimetro di questa feature riaprire quel modello.

---

### D2 — Metrica di distanza (`BQ2-K2`): distanza media assoluta per asse, complemento come affinità

**Il contesto**: divergenza 3 della revisione `001` — «quale distanza (euclidea, Manhattan, coseno), su quale massimo si normalizza». La scheda di `BQ2-K2` chiede il «complemento della distanza... normalizzata sulla scala 0-1». Il vincolo che la `006` ha lasciato scritto (`docs/content_taxonomy_bridge.md` §7) e che questa decisione deve onorare senza ripeterlo per esteso: gli assi sono ancorati **solo agli estremi** — nessun valore osservato calibra il centro della scala — quindi la corrispondenza fra le posizioni intermedie delle due scale è un'assunzione del criterio di mood, non un fatto misurato, e la grandezza assoluta di una distanza calcolata su questi assi non ha l'interpretazione che avrebbe fra due profili entrambi osservati. Resta però confrontabile con sé stessa fra segmenti diversi — è quella proprietà, e solo quella, su cui la scelta della metrica può contare.

**Le opzioni**: (a) **distanza euclidea**, normalizzata dividendo per `√3` (la distanza massima possibile fra due punti in un cubo `[0,1]³`); (b) **distanza media assoluta per asse** (city-block/Manhattan diviso per il numero di assi): `d = (|Δenergia| + |Δpositività| + |Δritmo|) / 3`; (c) distanza coseno.

**La decisione**: **(b)**. `segment_catalog_affinity = 1 − d`, con `d = (|energia_segmento − energia_video| + |positività_segmento − positività_video| + |ritmo_segmento − ritmo_video|) / 3`, dove il profilo del segmento è la mediana per asse sulle coppie traccia-segmento e il profilo del catalogo video è la mediana ponderata sul ponte titolo-categoria, entrambi secondo `data_model.md` §11.

**La ragione**: ciascun asse vive già su `[0,1]`, quindi ciascun termine `|Δasse|` è già in `[0,1]` e la loro media è automaticamente in `[0,1]` — nessuna costante di normalizzazione aggiuntiva è necessaria, a differenza della distanza euclidea, che richiede di dividere per `√3` per restare nella scala dichiarata. Quella divisione non è un dettaglio tecnico neutro: la distanza euclidea, per costruzione, permette a uno scostamento piccolo su un asse di **compensare** uno scostamento grande su un altro (attraverso la radice quadrata della somma dei quadrati), un'assunzione geometrica su come i tre assi si bilancino a vicenda. Dato che `content_taxonomy_bridge.md` §7 dichiara che solo gli estremi sono ancorati e **nessun valore osservato calibra il centro**, assumere una specifica regola di compensazione fra gli assi rivendica più struttura di quanta l'ancoraggio sostenga. La distanza media assoluta tratta i tre assi in modo indipendente e additivo — l'assunzione minima coerente con «solo gli estremi sono ancorati» — ed è anche l'unica delle tre opzioni che non richiede alcuna scelta aggiuntiva di normalizzazione, perché la scala risultante discende direttamente dalla scala dei tre assi di partenza.

**Che cosa questa scelta non risolve, e non deve fingere di farlo**: resta vero, come `content_taxonomy_bridge.md` §7 dichiara, che la grandezza assoluta di `d` — per esempio, se `d = 0,20` sia "vicino" o "lontano" — non ha un'interpretazione indipendente dal criterio di mood. Ciò che questa decisione garantisce è che `d` sia calcolabile e **confrontabile fra segmenti diversi con la stessa formula**, che è l'unica proprietà su cui `BQ2-K3` (D3-D4) può contare.

---

### D3 — Pesi e commensurabilità (`BQ2-K3`): normalizzazione per divisione, pesi uguali dichiarati

**Il contesto**: divergenza 4 della revisione `001`, prima metà — «quale trasformazione porta `BQ2-K1` e `BQ2-K2` su una scala comune, quali sono i pesi, chi li fissa». `BQ2-K1` (`segment_demand_index`) è un indice `0-100`; `BQ2-K2` (`segment_catalog_affinity`, D2) è un indice `0-1`. La scheda di `BQ2-K3` chiede il peso relativo «dichiarato esplicitamente» — comporli richiede prima una scelta di scala, poi una scelta di peso.

**La scelta di scala**: `BQ2-K1` si porta su `0-1` per **divisione per 100** — `segment_demand_index_norm = segment_demand_index / 100` — non per riscalamento min-max sull'insieme dei segmenti effettivamente osservati. La ragione: `BQ2-K1` è già un indice delimitato per definizione (`0-100`, non un valore osservato senza limite superiore noto), quindi dividerlo per il proprio massimo teorico è un'operazione fissa che non dipende da quali 114 segmenti esistano in un dato momento. Un riscalamento min-max renderebbe invece il punteggio composito di ogni segmento dipendente dal segmento più-o-meno-domandato del gruppo — una ridefinizione implicita ogni volta che l'insieme dei segmenti cambiasse, che qui non cambia (i 114 sono fissi, §2 di `data_model.md`) ma che introdurrebbe comunque una dipendenza che la divisione fissa evita.

**La scelta di peso**: **pesi uguali, 0,5 e 0,5**. `segment_entry_priority_score = 0,5 × (segment_demand_index / 100) + 0,5 × segment_catalog_affinity`.

**La ragione dei pesi uguali**: nessun criterio esterno a questo progetto stabilisce che la domanda debba contare più o meno dell'affinità di catalogo per l'ingresso in un nuovo verticale, e la formulazione della stessa `BQ2` (`business_case.md` §4) elenca le due dimensioni — «domanda relativa» e «affinità con il catalogo attuale» — senza qualificarne una come primaria. In assenza di un argomento che favorisca l'una o l'altra, dichiarare un peso diverso da 0,5/0,5 sarebbe un giudizio di business che questa feature non ha titolo a prendere — introdurrebbe una preferenza (per esempio, "la domanda conta di più perché genera ricavo più direttamente") che nessuna feature precedente ha argomentato e che il board non ha mai espresso. Il peso 0,5/0,5 è quindi la scelta che **non aggiunge** un'assunzione di business non richiesta, non quella che si presume "neutra" in astratto — è dichiarata come tale, non come l'unica oggettivamente corretta, e resta contestabile da chi in `008` volesse argomentare un peso diverso con una ragione di business esplicita.

---

### D4 — Quadranti contro combinazione pesata (`BQ2-K3`): entrambi, con ruoli distinti

**Il contesto**: stessa divergenza 4 della revisione `001`, seconda metà — «se prevale la lettura a quadranti di §4 o quella pesata della scheda». `business_case.md` §4 (BQ2) chiede «quali segmenti si collocano nel quadrante ad alta domanda e alta affinità?» — uno strumento a soglie ordinali, binario. La scheda di `BQ2-K3` in §5.5 descrive invece «ordinamento dei segmenti secondo la combinazione... con il peso relativo dei due criteri dichiarato esplicitamente» — un ordinamento continuo. Sono due strumenti diversi, e nessuno dei due documenti sceglie fra loro.

**La decisione**: `BQ2-K3` realizza **entrambi**, con ruoli distinti e non intercambiabili, non un compromesso fra i due.

1. **L'appartenenza al quadrante** (categoriale, per segmento): un segmento è "alta domanda, alta affinità" se il suo `segment_demand_index` è nella metà superiore (sopra la mediana) dei 114 segmenti **e** il suo `segment_catalog_affinity` è nella metà superiore degli stessi 114. È lo strumento che opera direttamente la condizione **C3** della regola di decisione della North Star (`business_case.md` §3): «esiste almeno un segmento musicale che si colloca contemporaneamente nella metà superiore per domanda e nella metà superiore per affinità con il catalogo». `BQ2-K3` deve poter rispondere a questa domanda con un sì/no verificabile, e un punteggio pesato continuo da solo non lo fa senza una soglia aggiuntiva — la soglia mediana **è** la lettura a quadranti.
2. **Il punteggio pesato e la graduatoria** (continua, per segmento): `segment_entry_priority_score` di D3, che ordina tutti i 114 segmenti in una posizione. È lo strumento che la scheda di `BQ2-K3` chiede alla lettera — «posizione in graduatoria» come formato di presentazione — e che una domanda binaria non può produrre.

**La ragione per cui non è una scelta fra i due**: rispondono a domande diverse. Il quadrante decide **se** un segmento supera una soglia doppia — è ciò che C3 richiede, ed è insensibile a quanto sopra la soglia un segmento si trovi. Il punteggio pesato decide **quanto** un segmento è preferibile a un altro, anche fra due segmenti entrambi dentro o entrambi fuori dal quadrante — è ciò che una priorità di ingresso, per essere operativa oltre un semplice sì/no, richiede. Fondere le due cose in un solo numero — per esempio, usare solo il punteggio pesato e leggere "alta priorità" come sinonimo di "nel quadrante" — nasconderebbe che un segmento può avere un punteggio pesato alto restando fuori dal quadrante (alta affinità, domanda appena sotto la mediana) o viceversa, ed è esattamente il tipo di distinzione che la condizione C3 chiede di preservare.

**Che cosa questo comporta per `007b`**: la misura pubblica entrambi i valori per ciascun segmento — l'appartenenza al quadrante (booleano) e il punteggio (continuo, la chiave della graduatoria) — non un valore unico che li confonda.

---

### D5 — Segno della differenza (`BQ1-K2`): musica meno video, segno pubblicato

**Il contesto**: divergenza 8 della revisione `001`, parte residua (la parte sulla durata mancante dei titoli è già chiusa dalla `003`, decisione D2). La scheda di `format_duration_gap` calcola «differenza tra la durata mediana di un film del catalogo video e la durata mediana di una traccia del catalogo musicale», senza dire il verso della sottrazione né se pubblicare il segno o il solo valore assoluto. La scheda dichiara esplicitamente, in `business_case.md` §5.5, **«Direzione: nessuna direzione — è un profilo, non un obiettivo»**.

**La decisione**: `format_duration_gap = mediana_durata_traccia_musicale_min − mediana_durata_film_video_min` (musica meno video). Il documento pubblica il **segno**, non il valore assoluto.

**La ragione del verso**: `BQ1` (`business_case.md` §4) formula la domanda come il posizionamento del contenuto musicale **rispetto a** quello video — la musica è il soggetto del confronto, il video il termine di paragone. Sottrarre nella direzione musica meno video mantiene questa struttura: un valore negativo dice "una traccia musicale dura, in mediana, questo tanto in meno di un film", che è la lettura naturale data la formulazione della domanda. La scelta è dichiaratamente arbitraria nel senso che l'altro verso sarebbe stato ugualmente calcolabile — ma un verso va fissato e dichiarato, e questo è coerente con come la domanda di business è scritta.

**La ragione per pubblicare il segno invece del valore assoluto**: la scheda dichiara esplicitamente che questo KPI **non ha una direzione** — non è un obiettivo da massimizzare o minimizzare, è un profilo descrittivo. Il segno, qui, non porta un giudizio di valore ("meglio" o "peggio"): porta solo l'informazione su quale dei due formati sia più lungo, che è informazione persa se si pubblica solo il valore assoluto. Pubblicare il segno non contraddice "nessuna direzione" — la direzione di cui la scheda parla è normativa (quale verso sia desiderabile), non aritmetica (quale sia il segno del numero).

**Un limite atteso, dichiarato prima che il numero esista**: dato che i film del catalogo video durano tipicamente decine di minuti e le tracce musicali pochi minuti, il valore sarà quasi certamente fortemente negativo. Non è un errore né un segnale di allarme — è la conseguenza aritmetica della differenza di formato che il KPI esiste per misurare, e il documento lo dichiara qui perché nessuno lo scambi per un'anomalia quando il numero comparirà in `007b`.

---

### D6 — Precisione del confronto: mezzo punto percentuale come soglia di "cambiato"

**Il contesto**: divergenza 1 della revisione `003`, ereditata e non chiusa da `docs/data_model.md` §19, che la assegna esplicitamente «alle misure». `reports/data_profile.json` memorizza le quote di zeri per genere a **una cifra decimale**; `reports/cleaning_report.json` le memorizza a **quattro**. Il criterio di confronto più stretto — tutte e quattro le cifre del rendiconto contro l'unica cifra del profilo — conta **78** generi "cambiati" fra le due versioni dell'articolo; i generi effettivamente spostati di oltre mezzo punto percentuale sono **3**.

**La decisione**: due valori dello stesso fatto, registrati in due artefatti diversi, si considerano **diversi** — cioè il genere si considera "cambiato" — se e solo se la differenza assoluta fra i due supera **0,5 punti percentuali**. Sotto quella soglia, la differenza si attribuisce alla precisione di rappresentazione (una cifra decimale nel profilo contro quattro nel rendiconto), non a uno spostamento reale prodotto dalla trasformazione.

**La ragione**: la precisione a una cifra decimale del profilo è esatta **per costruzione** finché ogni genere ha esattamente 1.000 righe (come nel campione di origine): la quota di zeri ha allora una sola cifra decimale possibile, e il profilo la registra senza perdita. Dopo la deduplicazione della `003` i generi non hanno più 1.000 righe uniformi, e il rendiconto usa quattro cifre per restare esatto sul nuovo denominatore — ma questo non rende il profilo "sbagliato": lo rende **arrotondato al proprio grado di risoluzione**, che è di mezzo decimo di punto (`0,05` punti percentuali, la metà dell'unità minima rappresentabile a una cifra). Una soglia di `0,5` punti percentuali sta un ordine di grandezza sopra quel pavimento di arrotondamento — quindi non confonde un arrotondamento con un cambiamento — e sta ben sotto la dimensione degli spostamenti reali osservati (i 3 generi mossi di oltre mezzo punto), quindi non nasconde un cambiamento vero dentro la soglia. Non è la soglia più stretta possibile, ed è dichiarata come scelta, non come unica lettura corretta: la funzione che deve svolgere è separare pulitamente le due popolazioni — arrotondamento contro spostamento reale — e `0,5` lo fa con margine su entrambi i lati.

**Conseguenza per chi cita questo confronto**: il denominatore di "generi cambiati" fra profilo e rendiconto, quando qualcuno lo pubblicherà, è **3**, non 78 — e chi cita quel numero deve dichiarare la soglia di 0,5 punti percentuali accanto ad esso, per la stessa ragione per cui ogni affermazione derivata porta la propria fonte (D5 di `CLAUDE.md`).

---

### D7 — Trattamento degli zeri: la quota di popolarità zero accanto a ogni misura sulla popolarità

**Il contesto**: divergenza 6 della revisione `001` — «incluse, escluse, o riportate come misura di fragilità accanto alla mediana». La parte sui dati è già chiusa dalla `003` (D1: le tracce a popolarità zero restano incluse e mai eliminate) e resa operativamente possibile dal modello dati (`data_model.md` §14: `is_popularity_zero` su `fact_track_segment`, alla grana coppia traccia-segmento; `is_high_zero_genre` su `dim_segment`). Resta da scrivere l'operatore.

**La decisione**: ogni misura calcolata sulla popolarità — in particolare `BQ2-K1` (`segment_demand_index`), e per composizione `BQ2-K3` — **deve** pubblicare, accanto al proprio valore, la quota di righe a popolarità zero del segmento: `zero_share_segmento = conteggio(is_popularity_zero = vero, nel segmento) / conteggio(righe del segmento)`, calcolata su `fact_track_segment` alla stessa grana coppia traccia-segmento su cui `BQ2-K1` stesso opera (`data_model.md` §12). Dove il segmento porta anche `is_high_zero_genre = vero` su `dim_segment` — cioè supera la soglia del 50% che la trasformazione della `003` dichiara — il valore pubblicato porta un avvertimento testuale esplicito, non solo il numero.

**La ragione**: una mediana di popolarità calcolata su un segmento pieno di zeri è trascinata verso il basso da un difetto della fonte (una traccia priva di segnale di popolarità sulla piattaforma di origine, non priva di domanda reale), non da una debolezza di domanda del segmento — ed è precisamente la distinzione che la revisione del business case aveva sollevato senza deciderla. Pubblicare la quota accanto al valore permette a chi legge di fare quella distinzione da sé, invece di leggere una mediana bassa come "domanda bassa" quando potrebbe essere "molti zeri".

**Che cosa questa decisione non fa**: non introduce una correzione statistica della mediana (per esempio, ricalcolarla escludendo gli zeri) — quella sarebbe una decisione diversa, già scartata dalla `003` D1, che ha deciso di includerli. Questa decisione si limita a rendere visibile, accanto al valore, il fatto che lo condiziona.

---

### D8 — Chiusura della parte residua di `R13`: direzione della graduatoria di `BQ2-K3`

**Il contesto**: `R13` della revisione `001` osserva che la direzione di `BQ2-K3`, «posizione alta = candidato migliore» (`business_case.md` §5.5), è ambigua per una graduatoria: non è detto se il candidato migliore occupi la posizione **1** o la posizione con il **punteggio più alto** — le due letture coincidono solo se l'ordinamento è esplicitamente decrescente. La parte di `R13` su `BQ1-K2` è chiusa da D5 qui sopra; la parte su `BQ3-K1` (disdette, stabilità della base) è già chiusa dalla `004`.

**La decisione**: il candidato migliore occupa la **posizione 1**. La graduatoria di `BQ2-K3` ordina i segmenti per `segment_entry_priority_score` (D3) **decrescente**, e la posizione 1 è il segmento con il punteggio più alto.

**La ragione**: è la lettura che rende "posizione alta = candidato migliore" (il testo già pubblicato in `business_case.md`) letteralmente vera nel linguaggio comune di una graduatoria — dove "primo" è la posizione più alta in importanza, non il valore numerico più alto dell'indice di posizione. La lettura alternativa (posizione 1 = punteggio più basso, con "posizione alta" a indicare un numero di posizione grande) esisterebbe solo per una convenzione opposta e non ha alcun sostegno nel testo esistente: nessuna scheda del business case usa "posizione" nel senso di rango crescente altrove. Dichiararlo qui chiude l'ambiguità senza toccare il testo del business case, che non era sbagliato — solo sotto-specificato.

---

### D9 — `BQ1-K1`: l'operatore di C1, il rapporto della North Star, e perché il numeratore regge sul dato trasformato

**Il contesto, in due parti che si chiudono insieme perché sono lo stesso passaggio su `BQ1-K1`.**

**Parte 1 — la condizione C1 non aveva operatore.** `business_case.md` §3 assegna a `BQ1-K1` la condizione **C1** della regola di decisione della North Star: «il contenuto musicale non è residuale nel catalogo attuale: la sua categoria si colloca nella **metà superiore** delle categorie per numero di titoli». Non è la stessa domanda della quota `music_adjacent_catalog_share` (375 su 8.807): C1 chiede una **graduatoria delle 42 categorie** per numero di titoli e la posizione di `Music & Musicals` rispetto alla mediana — grana diversa, operatore mai definito da nessuna feature precedente.

**Parte 2 — divergenza 4 della revisione `002`.** `docs/data_audit.md` pubblica **375** (titoli musicali) e **8.807** (titoli totali) a poche righe dalla frase sulla North Star, senza calcolare il rapporto — formalmente non contiene KPI, come dichiara, ma un lettore arriva alla divisione senza sforzo. La divergenza chiede se questo equivalga, in sostanza, a pubblicare la misura.

**Perché si chiudono nello stesso blocco**: entrambe riguardano su quale dato e con quale operatore `BQ1-K1` si calcola — la quota **e** la condizione C1 che ne dipende — e toccano lo stesso numero, 375, letto una volta come numeratore di un rapporto e una volta come conteggio di base per una graduatoria.

---

**D9.1 — Il numeratore 375 vive solo sul dato di origine: l'invariante che lo rende valido sul trasformato.**

`375` esiste come identificativo unicamente in `reports/data_profile.json` (`NF.cat.music_musicals.titles`), calcolato sul catalogo **di origine**. Nessun identificativo di `reports/cleaning_report.json` lo ripete: il rendiconto della trasformazione non pubblica un conteggio di titoli per categoria. `FR-014` di questo documento obbliga però ogni operatore a dichiarare da quali tabelle del **modello dati** legge, e il modello opera sul dato **trasformato** — dove il numeratore, così com'è, non ha ancora un'ancora propria.

La risposta non è ricontare: è scrivere l'**invariante**, sullo stesso schema già adottato dalla `005` per i 114 segmenti (roadmap, debito della `005` — «conteggio dei segmenti letto dal profilo di origine»: non si riconta, si dichiara perché il conteggio di origine regge sul trasformato). Qui l'invariante regge, verificabile con due soli fatti già ancorati: il numero di titoli distinti del catalogo non cambia dalla trasformazione — `NF.shape.rows` (origine, 8.807) e `CL.NF.titles.rows.after` (trasformato, 8.807) coincidono — e le uniche righe toccate dalla riparazione, `CL.NF.duration.repaired.rows` (3), sono state riparate per **spostamento di campo**, non per imputazione né eliminazione (`data_model.md` §14, `is_repaired_duration`): nessun titolo è stato aggiunto, rimosso, o ha cambiato la propria assegnazione di categoria. Poiché la trasformazione non tocca né il numero di titoli né le loro categorie, il conteggio dei titoli in `Music & Musicals` è anch'esso invariante, e `375` resta il numeratore corretto sul dato trasformato — pur non avendo, oggi, un'ancora propria in `reports/cleaning_report.json`.

**Conseguenza per l'operatore**: dichiara la catena per intero — numeratore letto dall'origine (`NF.cat.music_musicals.titles`), invariante argomentato sui due fatti sopra, denominatore letto indifferentemente dall'origine o dal trasformato perché coincidono (`NF.shape.rows` = `CL.NF.titles.rows.after` = 8.807) — invece di citare 375 come se fosse già un valore del modello dati.

---

**D9.2 — L'operatore di C1: graduatoria delle 42 categorie per numero di titoli, non la quota.**

C1 non è calcolabile da `music_adjacent_catalog_share`, che è una quota sull'intero catalogo. Il suo operatore è distinto: per ciascuna delle 42 categorie di `catalogs.netflix_categories_normalized`, il numero di titoli si conta raggruppando le righe di `bridge_title_category` per categoria — non gli 8.807 titoli distinti del catalogo (un conteggio globale, non per categoria) e non le 19.323 assegnazioni totali lette come un numero unico, ma la loro **suddivisione per categoria**: ciascuna riga del ponte è già, per costruzione, un titolo distinto in quella categoria (`data_model.md` §10.2 — nessun'altra colonna sul ponte, nessuna assegnazione titolo-categoria duplicata). La somma dei 42 conteggi per categoria restituisce 19.323, non 8.807: è la stessa distinzione fra grana di appartenenza e grana del risultato che `data_model.md` §18 dichiara per i segmenti musicali, applicata qui al lato video.

C1 è soddisfatta se il conteggio di titoli di `Music & Musicals` supera la **mediana** dei 42 conteggi per categoria — condizione stretta (`>`), per coerenza con la stessa convenzione già adottata in D4 per i quadranti di `BQ2-K3`, non per una ragione nuova a sé.

**La ragione della scelta sul conteggio**: la formulazione di C1 — «la sua categoria si colloca nella metà superiore delle categorie **per numero di titoli**» — chiede quanti titoli popolano ciascuna categoria, non quanti titoli distinti esistono nell'intero catalogo. Il conteggio per categoria sul ponte è l'unica lettura che risponde a questa domanda: usare 8.807 (o una sua quota) confonderebbe una proprietà dell'intero catalogo con una proprietà di una singola categoria.

**Che cosa questa decisione non fa**: non calcola la posizione di `Music & Musicals` nella graduatoria — nessun conteggio di titoli per categoria è oggi pubblicato in alcun artefatto, e produrlo è compito della `007b`. Questa feature dichiara solo l'operatore: su quale tabella si conta, a quale grana, con quale soglia.

---

**D9.3 — La North Star resta un rapporto da calcolare, non una giustapposizione.**

Sulla divergenza 4 della `002`: **nessuna delle due strade che offriva**, perché nessuna è nel perimetro di `007a` — rimuovere l'accostamento toccherebbe `docs/data_audit.md`, un artefatto di un'altra feature già mergiata; accettare che la North Star nasca lì accetterebbe una nascita implicita che la regola D5 vieta. Ciò che `007a` decide è l'**operatore** di `music_adjacent_catalog_share`: il rapporto **375 / 8.807** non è pubblicato come misura finché non è calcolato esplicitamente e ancorato con un proprio identificativo — la giustapposizione di due numeri già ancorati separatamente in `data_audit.md`, per quanto vicini in prosa, **non costituisce** aver pubblicato la misura, perché il rapporto stesso è un'affermazione derivata (D5 di `CLAUDE.md`: «un confronto, una graduatoria, un rapporto costruiti su valori misurati sono essi stessi valori misurati») e finché non porta un'ancora propria resta implicito.

**La ragione**: è l'applicazione diretta della regola D5 già in vigore nel progetto, non una regola nuova. `data_audit.md` non viola nulla — dichiara correttamente di non contenere KPI, e i due numeri che pubblica sono entrambi ancorati ai propri identificativi. Ciò che resta indefinito è solo il rapporto, e questa feature lo definisce come operatore: quando `007b` calcolerà `music_adjacent_catalog_share`, il valore risultante — non i suoi due input separati — è ciò che porta l'ancora della misura.

**Conseguenza per `007b`**: il documento `docs/kpi_operators.md` dichiara esplicitamente che 375 e 8.807 sono **input** già disponibili — il primo sul dato di origine con l'invariante di D9.1, il secondo su entrambi i lati per coincidenza — non la misura; la misura nasce quando il loro rapporto viene calcolato e ancorato per la prima volta, compito della `007b`. La stessa lettura per categoria di D9.2 fornisce l'operatore di C1, distinto e non sostitutivo della quota.

---

## Rapporto con le feature vicine

**Questa feature non calcola alcun KPI.** Produce le regole con cui la `007b` li calcolerà. Nessun valore numerico dei KPI compare in `docs/kpi_operators.md` — dove una decisione ha bisogno di un esempio concreto (D6 sulla soglia di 0,5 punti percentuali, D9 su 375/8.807), i numeri citati sono **input già ancorati da feature precedenti**, mai un risultato di questa.

**Questa feature eredita senza toccare**: `docs/data_model.md` §11 (i due campi degli assi, le due regole di aggregazione già chiuse per `BQ1-K3` e `BQ2-K2`), §12 (da quale tabella si legge la popolarità), §14 (le marcature `is_popularity_zero`, `is_high_zero_genre`, `is_duration_zero`), §19 (l'elenco dei vincoli assegnati «alle misure», di cui questa feature ne chiude quattro: precisione del confronto, trattamento degli zeri, segno di `BQ1-K2`, peso di `BQ2-K3`). Nessuna di queste sezioni viene riaperta o ridiscussa; questa spec le cita solo dove vincolano una decisione.

**Questa feature eredita da `content_taxonomy_bridge.md`** il vincolo di ancoraggio solo agli estremi (§7, citato in D2) e il fatto che la tabella dei mood non è definitiva — il ritrovamento `CF-1` è aperto e verrà chiuso da un chore con una versione 2 della tabella, prima della `007b`. Nessun operatore di questa feature presuppone che i **valori** attuali della tabella siano stabili: presuppone solo che gli **assi** e i loro estremi ancorati lo siano, che è un vincolo strutturale distinto e non tocca da `CF-1`.

**Questa feature non tocca `data/raw/` né rilegge la pipeline.** Ogni riferimento numerico che compare come esempio è letto da artefatti già versionati e già ancorati (`reports/data_profile.json`, `reports/cleaning_report.json`).

---

## Perimetro

Ciò che questa feature **non** fa, e a chi spetta.

| Fuori perimetro | Ragione | A chi spetta |
|---|---|---|
| **Implementare le misure in DAX**, aprire Power BI, calcolare o pubblicare qualunque valore dei KPI | l'operatore si scrive prima del valore, non insieme | `007b` |
| **Chiudere `CF-1` e produrre la versione 2 della tabella dei mood** | è un ritrovamento della `006`, non di questa feature | chore, prima di `007b` |
| **Materializzare il modello dati in Power BI** | interazione con la GUI, fuori dal confine dell'automazione (principio V) | chore, prima di `007b` |
| **Debito testuale della `001`** (rilievi R9, R10, R12 sul testo del business case) | correzioni terminologiche non analitiche | chore, prima di `007b` |
| **Debito testuale della `002`** (divergenza 3, allineamento di `docs/data_audit.md`) | citazione di decisioni prese altrove, non una decisione analitica | chore, prima di `007b` |
| **Come i KPI appaiono a schermo, storytelling, limiti esposti in dashboard** | è narrazione e presentazione, non definizione dell'operatore | `008a` / `008b` |
| **Ridiscutere §11 di `data_model.md`** (campi degli assi, aggregazione min-max e mediana ponderata) | decisioni già chiuse dal modello dati | `005`, già mergiata |

---

## User Scenarios & Testing *(mandatory)*

Gli attori sono due: **chi scrive** questo documento (la sessione della `007a`) e **chi lo eredita** — la `007b`, che deve poter implementare ogni misura leggendo solo `docs/kpi_operators.md` e il modello dati, senza dover riaprire alcuna revisione precedente per capire un operatore.

### User Story 1 — Le quattro decisioni più esposte sono argomentate prima che il documento esista (Priority: P1)

Chi scrive fissa intervallo occupato, metrica di distanza, pesi e commensurabilità, quadranti contro combinazione pesata — le quattro decisioni che il prompt di consegna nomina al terzo punto di stop — con la propria ragione esplicita, prima di scrivere `docs/kpi_operators.md`.

**Why this priority**: è il punto di massima leva della feature. Le sette decisioni non hanno lo stesso costo di errore: queste quattro condizionano tre KPI (`BQ1-K3`, `BQ2-K2`, `BQ2-K3`) che a loro volta condizionano due delle tre condizioni della regola di decisione della North Star (C2, C3). Un errore qui si propaga all'intero framework.

**Independent Test**: si leggono D1-D4 di questa spec; ciascuna cita l'opzione scartata e la ragione per cui è stata scartata, non solo l'opzione scelta.

**Acceptance Scenarios**:

1. **Given** D1, **When** la si legge, **Then** dichiara perché il prodotto cartesiano è stato preferito all'inviluppo convesso, e dichiara esplicitamente il limite che la scelta introduce (stima per eccesso della sovrapposizione).
2. **Given** D2, **When** la si legge, **Then** dichiara perché la distanza media assoluta è stata preferita all'euclidea, citando il vincolo di ancoraggio solo agli estremi di `content_taxonomy_bridge.md` §7.
3. **Given** D3 e D4, **When** le si legge insieme, **Then** è chiaro che `BQ2-K3` pubblica sia l'appartenenza al quadrante sia il punteggio pesato, con ruoli distinti e non come alternative.

---

### User Story 2 — L'operatore di `BQ1-K1` copre anche C1, non solo la quota (Priority: P1)

Chi eredita il documento trova, per `BQ1-K1`, non solo la definizione di `music_adjacent_catalog_share` ma anche l'operatore distinto della condizione C1 della North Star — la posizione di `Music & Musicals` nella graduatoria delle 42 categorie per numero di titoli — e la ragione per cui il numeratore 375, letto sul dato di origine, regge anche sul modello dati costruito sul trasformato.

**Why this priority**: C1 è una delle tre condizioni che sostengono l'argomento di coerenza strategica dell'intero progetto (`business_case.md` §3), ed è rimasta priva di operatore attraverso tutte le revisioni precedenti. Senza questa storia, `007b` arriverebbe a `BQ1-K1` e dovrebbe decidere da sola su quale conteggio ordinare le categorie e come trattare i pari merito — esattamente il tipo di decisione analitica che questa feature esiste per non lasciare a valle.

**Independent Test**: si legge D9 di questa spec; distingue esplicitamente l'operatore di C1 (D9.2) da quello della quota (D9.3), e argomenta separatamente perché il numeratore di origine regge sul dato trasformato (D9.1).

**Acceptance Scenarios**:

1. **Given** D9.1, **When** la si legge, **Then** dichiara che `375` è letto da `reports/data_profile.json` e argomenta l'invariante che lo rende valido sul dato trasformato citando `NF.shape.rows`, `CL.NF.titles.rows.after` e `CL.NF.duration.repaired.rows`.
2. **Given** D9.2, **When** la si legge, **Then** definisce l'operatore di C1 come il conteggio dei titoli per categoria su `bridge_title_category` raggruppato per categoria, con la mediana dei 42 conteggi come soglia stretta, e dichiara esplicitamente che questo conteggio non è oggi pubblicato in alcun artefatto.
3. **Given** D9.2, **When** la si confronta con D9.3, **Then** è chiaro che sono due operatori distinti sullo stesso KPI — uno per la condizione C1, uno per la quota — e non due letture alternative dello stesso numero.

---

### User Story 3 — Ogni operatore dichiara provenienza e non altera la confidenza già fissata (Priority: P1)

Chi eredita il documento trova, per ciascun operatore, da quali tabelle e colonne del modello dati legge, e nessuna dichiarazione che sposti la confidenza di un KPI oltre quella già fissata da `business_case.md` §5.4.

**Why this priority**: la confidenza di un KPI è un fatto già deciso a monte (dal business case, ereditato dal modello dati) — questa feature non ha titolo a rinegoziarla, esattamente come la `006` non ha potuto farlo salire per `BQ1-K3`, `BQ2-K2`, `BQ2-K3` nonostante la cura del proprio processo.

**Independent Test**: si confronta la tabella di confidenza di questa spec (sezione "Provenienza e Confidenza dei Dati") con `business_case.md` §5.4; i livelli coincidono per tutti e otto i KPI.

**Acceptance Scenarios**:

1. **Given** un operatore che usa `dim_category_mood` (D1, D2), **When** lo si legge, **Then** dichiara che la confidenza del KPI resta **media**, per lo stesso obbligo non negoziabile di `data_model.md` §15 che vincola già la `006`.
2. **Given** l'intero documento, **When** lo si confronta con `business_case.md` §5.4, **Then** nessun KPI cambia classificazione di confidenza.

---

### User Story 4 — I vincoli ereditati condizionano l'operatore senza diventare un giudizio (Priority: P2)

Chi scrive un operatore per segmento dichiara i vincoli ereditati dalle feature precedenti — campione sbilanciato, tabella dei mood non definitiva per `CF-1`, ancoraggio solo agli estremi — accanto all'operatore che li eredita, senza introdurre una valutazione della loro entità che nessun artefatto sostiene.

**Why this priority**: è la disciplina che la `005` ha già applicato al campione sbilanciato («il rendiconto non pubblica il massimo né alcuna misura di dispersione... chi in `007b` costruirà una misura per segmento eredita il fatto, non una valutazione») — questa feature la eredita a sua volta, senza retrocedere.

**Independent Test**: si cerca nel documento qualunque aggettivo di entità («grande», «piccolo», «trascurabile») accanto al fatto del campione sbilanciato o dell'ancoraggio solo agli estremi; non ce n'è nessuno che non sia già ancorato a un valore pubblicato altrove.

**Acceptance Scenarios**:

1. **Given** l'operatore di `BQ2-K1` (`segment_demand_index`), **When** lo si legge, **Then** dichiara che i conteggi per segmento non sono più uniformi (17 conteggi distinti, minimo 904, `data_model.md` §18) senza affermare se lo scostamento sia rilevante.
2. **Given** gli operatori di `BQ1-K3`, `BQ2-K2`, `BQ2-K3` (D1-D4), **When** li si legge, **Then** ciascuno dichiara che presuppone la stabilità degli assi e dei loro estremi ancorati, non dei valori attuali delle 42 celle — e cita `CF-1` come motivo.

---

### User Story 5 — Il documento è verificabile meccanicamente, non solo a lettura (Priority: P2)

Chi esegue `scripts/check_audit_coherence.py` su `docs/kpi_operators.md` trova ogni numerale in posizione di fatto misurato ancorato a un artefatto o marcato esplicitamente come non misurato, sotto severità stretta.

**Why this priority**: è il presidio che rende il documento coerente con il resto del progetto invece di un'eccezione silenziosa — il precedente diretto è `docs/data_model.md`, un documento senza artefatto proprio le cui ancore risolvono contro gli artefatti delle feature precedenti, già in severità stretta.

**Independent Test**: si esegue `python3 scripts/check_audit_coherence.py` dopo aver aggiunto `docs/kpi_operators.md` a `DOCUMENTS` con severità stretta; il controllo passa, e continua a passare sui documenti esistenti.

**Acceptance Scenarios**:

1. **Given** `docs/kpi_operators.md`, **When** `check_audit_coherence.py` lo scandisce, **Then** ogni numerale (es. `375`, `8.807`, `0,5` punti percentuali, `114` segmenti) porta un'ancora verso un identificativo esistente o il marcatore di non-misurato.
2. **Given** la tupla `DOCUMENTS` dello script, **When** la si ispeziona, **Then** contiene una nuova riga per `docs/kpi_operators.md` con severità stretta (`True`), sul modello della riga di `docs/data_model.md`.

---

### User Story 6 — La voce minore residua di `R13` è chiusa (Priority: P3)

Chi legge il documento trova la direzione della graduatoria di `BQ2-K3` dichiarata (D8), senza doverla cercare in un rilievo separato.

**Why this priority**: è una voce minore per costo di argomentazione, non per importanza di chiusura — lasciarla aperta lascerebbe `007b` a dover decidere un'ambiguità analitica senza il contesto che questa feature ha.

**Independent Test**: si cerca nel documento il riferimento a `R13`; compare con una decisione dichiarata, non solo con la citazione del rilievo.

**Acceptance Scenarios**:

1. **Given** l'operatore di `BQ2-K3`, **When** lo si legge, **Then** dichiara che la posizione 1 è il segmento con il punteggio più alto (D8).

---

### Edge Cases

- **Un profilo di traccia cade esattamente sul confine di un intervallo scalare** (D1). Gli intervalli sono chiusi (`[min, max]`, non aperti): un valore uguale al minimo o al massimo osservato conta come "dentro". È coerente con il fatto che minimo e massimo sono essi stessi valori osservati su una categoria reale, non limiti teorici.
- **Un segmento ha `segment_demand_index` o `segment_catalog_affinity` esattamente sulla mediana** (D4). La soglia del quadrante è "sopra la mediana" in senso stretto (`>`), non "sopra o uguale" — un segmento sulla mediana non entra nel quadrante alto. La scelta è dichiarata qui perché altrimenti resterebbe implicita in `007b`; non ha un impatto atteso rilevante dato che gli indici sono continui e una coincidenza esatta sulla mediana è un caso limite raro, ma va comunque decisa.
- **Un segmento porta `is_high_zero_genre = vero` e la sua mediana di popolarità è comunque alta.** L'avvertimento testuale di D7 si pubblica comunque, accanto al valore: il fatto che la mediana sia alta nonostante la concentrazione di zeri non riduce l'obbligo di dichiarare la concentrazione — anzi la rende più interessante da segnalare, perché il valore alto è stato raggiunto nonostante il difetto della fonte.
- **La versione 2 della tabella dei mood, dopo la chiusura di `CF-1`, sposta i valori delle 5 etichette in conflitto.** Nessun operatore di questa feature ne è invalidato: D1 e D2 presuppongono solo la stabilità degli assi e degli estremi ancorati, non dei valori delle celle (User Story 4, scenario 2). `007b` applicherà gli stessi operatori alla tabella versione 2 senza dover tornare qui.
- **Un genere nel confronto di D6 si sposta di esattamente 0,5 punti percentuali.** La soglia è un limite superiore incluso nel gruppo "non cambiato": la decisione usa "supera 0,5 punti" (`>`, stretto), quindi 0,5 esatto non conta come cambiato. Va dichiarato nel documento con la stessa esplicitezza della soglia stessa.

---

## Requirements *(mandatory)*

### Le quattro decisioni più esposte (D1-D4)

- **FR-001**: L'operatore di `BQ1-K3` MUST definire l'appartenenza di un profilo a tre coordinate all'intervallo occupato dal catalogo video come **prodotto cartesiano** dei tre intervalli scalari indipendenti già fissati da `docs/data_model.md` §11 — appartenenza verificata asse per asse con AND logico, non tramite inviluppo convesso o altra costruzione congiunta.
- **FR-002**: L'operatore di `BQ1-K3` MUST dichiarare esplicitamente che il prodotto cartesiano è una stima per eccesso della sovrapposizione reale rispetto a un inviluppo convesso, come limite della scelta e non come difetto da correggere in questa feature.
- **FR-003**: L'operatore di `BQ2-K2` MUST definire la distanza fra il profilo mediano di un segmento e il profilo del catalogo video come **media delle tre distanze assolute per asse** (`(|Δenergia| + |Δpositività| + |Δritmo|) / 3`), e `segment_catalog_affinity` come il suo complemento a 1.
- **FR-004**: L'operatore di `BQ2-K2` MUST citare esplicitamente il vincolo di `docs/content_taxonomy_bridge.md` §7 (ancoraggio solo agli estremi) come motivazione della metrica scelta, senza ripeterne il testo per esteso.
- **FR-005**: L'operatore di `BQ2-K3` MUST normalizzare `BQ2-K1` a scala `0-1` per divisione per 100 (non per riscalamento min-max sull'insieme dei segmenti osservati), e MUST dichiarare un peso pari a **0,5** per la componente di domanda normalizzata e **0,5** per la componente di affinità, con la ragione per cui i due pesi sono uguali.
- **FR-006**: L'operatore di `BQ2-K3` MUST pubblicare **due** valori distinti per segmento: l'appartenenza al quadrante alta-domanda/alta-affinità (booleano, soglia mediana su entrambi gli assi, condizione stretta `>`) e il punteggio pesato continuo di FR-005, con i rispettivi ruoli dichiarati esplicitamente e non presentati come alternativi.
- **FR-007**: L'operatore di `BQ2-K3` MUST dichiarare che l'appartenenza al quadrante di FR-006 è l'operatore che verifica direttamente la condizione C3 della regola di decisione della North Star (`docs/business_case.md` §3).

### Le tre decisioni restanti (D5-D7)

- **FR-008**: L'operatore di `BQ1-K2` MUST calcolare `format_duration_gap` come `mediana_durata_traccia_musicale_min − mediana_durata_film_video_min` (musica meno video), e MUST pubblicare il segno del risultato, non il valore assoluto.
- **FR-009**: L'operatore di `BQ1-K2` MUST dichiarare che il KPI non ha direzione normativa (eredità di `business_case.md` §5.5) e che il segno pubblicato porta solo informazione aritmetica su quale formato sia più lungo, non un giudizio di valore.
- **FR-010**: Il documento MUST fissare la soglia di "valore cambiato" a **0,5 punti percentuali** di differenza assoluta (condizione stretta, `>`), **limitata al confronto delle quote di zeri per genere** fra `reports/data_profile.json` e `reports/cleaning_report.json` — non a qualunque confronto fra i due artefatti — e MUST dichiarare la ragione della soglia (separazione fra pavimento di arrotondamento e spostamenti reali osservati). Un'estensione della soglia ad altre coppie di valori richiede una decisione esplicita, non l'applicazione automatica di questo requisito: la soglia è espressa in punti percentuali e non ha senso su un confronto fra conteggi o medie di altra natura.
- **FR-011**: Ogni operatore che coinvolge la popolarità (in particolare `BQ2-K1`) MUST richiedere la pubblicazione, accanto al proprio valore, della quota di righe a popolarità zero del segmento (`is_popularity_zero`, grana coppia traccia-segmento), e MUST richiedere un avvertimento testuale esplicito dove il segmento porta `is_high_zero_genre = vero`.

### La direzione della graduatoria (D8)

- **FR-012**: L'operatore di `BQ2-K3` MUST dichiarare che la posizione 1 della graduatoria è il segmento con il punteggio pesato più alto (ordinamento decrescente), chiudendo la parte residua di `R13` della revisione `001` su questo KPI.

### `BQ1-K1`: la quota, C1, e l'invariante sul dato trasformato (D9)

- **FR-013**: L'operatore di `BQ1-K1` MUST dichiarare che i valori 375 e 8.807 pubblicati in `docs/data_audit.md` sono input, non la misura, e che la misura (`music_adjacent_catalog_share`) nasce solo quando il loro rapporto viene calcolato e ancorato per la prima volta — compito della `007b`.
- **FR-013a**: L'operatore di `BQ1-K1` MUST dichiarare che il numeratore 375 è letto da `reports/data_profile.json` (dato di origine) e non ha un'ancora propria in `reports/cleaning_report.json`, e MUST argomentare esplicitamente l'invariante che lo rende valido sul dato trasformato: la coincidenza fra `NF.shape.rows` e `CL.NF.titles.rows.after`, e la natura non eliminativa delle 3 righe riparate in `CL.NF.duration.repaired.rows` (spostamento di campo, non imputazione né eliminazione).
- **FR-013b**: Il documento MUST definire l'operatore della condizione **C1** della regola di decisione della North Star (`docs/business_case.md` §3), distinto dall'operatore della quota di `BQ1-K1`: il conteggio dei titoli per categoria si calcola raggruppando le righe di `bridge_title_category` per categoria (non sugli 8.807 titoli distinti del catalogo, non sulle 19.323 assegnazioni lette come numero unico), e C1 è soddisfatta se il conteggio di `Music & Musicals` supera la mediana dei 42 conteggi per categoria, condizione stretta (`>`).

### Provenienza, confidenza e limiti (obbligo trasversale su ogni operatore)

- **FR-014**: Ciascuno degli otto operatori MUST dichiarare esplicitamente da quali tabelle e colonne di `docs/data_model.md` legge.
- **FR-015**: Nessun operatore MUST alterare la classificazione di confidenza già fissata da `docs/business_case.md` §5.4 per il proprio KPI; dove un operatore usa `dim_category_mood`, MUST ripetere che la confidenza resta **media** per l'obbligo non negoziabile di `docs/data_model.md` §15.
- **FR-016**: Ogni operatore che dipende da `dim_category_mood` (`BQ1-K3`, `BQ2-K2`, `BQ2-K3`) MUST dichiarare che presuppone solo la stabilità degli assi e dei loro estremi ancorati, non dei valori delle celle attualmente congelate, e MUST citare `CF-1` come motivo per cui i valori non sono definitivi.
- **FR-017**: Ogni operatore per segmento MUST dichiarare, dove rilevante, che il campione musicale non è più bilanciato dopo la trasformazione (17 conteggi di riga distinti, minimo 904 — `docs/data_model.md` §18) come **fatto ereditato**, senza introdurre una valutazione della sua entità che nessun artefatto pubblicato sostiene.
- **FR-018**: Nessun operatore MUST presupporre un conteggio dei 114 segmenti ricalcolato sul dato trasformato; se un operatore ne avesse bisogno, il documento MUST dichiararlo come ritrovamento e fermarsi, senza tentare di risolverlo (precedente: FR-032 della `002`).

### Documento pubblicato e controllo di coerenza

- **FR-019**: La feature MUST produrre `docs/kpi_operators.md`, con un operatore per ciascuno degli otto KPI di `docs/business_case.md` §5.5, nessun valore numerico dei KPI stessi, e le nove decisioni D1-D9 riportate o richiamate nel punto in cui l'operatore che vincolano viene definito.
- **FR-020**: Il documento MUST entrare in `DOCUMENTS` di `scripts/check_audit_coherence.py` sotto **severità stretta**, come sesto documento verificato dal controllo, sul precedente strutturale di `docs/data_model.md` — un documento senza artefatto proprio le cui ancore risolvono contro gli artefatti delle feature precedenti.
- **FR-021**: Ogni numerale scritto nel documento in posizione di fatto misurato MUST portare un'ancora verso un artefatto già versionato (`reports/data_profile.json`, `reports/cleaning_report.json`, `data/curated/dim_category_mood.json`, `docs/data_model.md`) o il marcatore esplicito di non-misurato, secondo `docs/convenzioni-marcatura.md`. Nessun numerale MUST essere scritto in lettere per un fatto misurato.
- **FR-022**: `docs/convenzioni-marcatura.md` MUST registrare `docs/kpi_operators.md` nella propria tabella di provenienza, con data e feature.

### Obblighi che nessun automatismo esegue

- **FR-023**: La feature MUST aggiornare `README.md`: riga nella tabella di stato con link a `specs/007a-kpi-operators/review.md`, deliverable elencato, la frase «I cinque documenti che pubblicano misure» estesa al sesto documento (audit, cleaning, scenari, modello, ponte, operatori), il commento del passo 5 di `Setup` allineato al nuovo conteggio, sezione `Struttura` allineata.
- **FR-024**: La feature MUST produrre `specs/007a-kpi-operators/review.md` secondo i quattro obblighi di `CLAUDE.md`: committato prima di correggere l'artefatto; dichiara in apertura che cosa ha letto e che cosa no; ancora commit e impronta del contenuto letto; non si corregge, con un blocco di chiusura che dichiara come ogni rilievo è stato chiuso (risolto / indebolito / respinto con prova / rinviato).
- **FR-025**: Nessun commit MUST essere eseguito di iniziativa dalla sessione esecutiva. Messaggio e contenuto si propongono; decide Valerio. Vale per `add`, `push`, apertura di PR, merge.
- **FR-026**: `docs/roadmap.md` NON DEVE essere modificato da questa feature: appartiene alla regia.

### Key Entities

- **`docs/kpi_operators.md`**: il deliverable unico della feature. Prosa in italiano, otto operatori (uno per KPI), nove decisioni argomentate (D1-D9), nessun valore numerico dei KPI. Sotto severità stretta nel controllo di coerenza.
- **Operatore**: per ciascun KPI, la regola completa di calcolo — formula, grana, provenienza dal modello dati, confidenza ereditata, limiti dichiarati — sufficiente perché `007b` scriva la misura DAX senza dover decidere nulla di analitico.
- **Decisione (D1-D9)**: un blocco autonomo che cita il rilievo o la divergenza di origine, le opzioni scartate, la scelta, la ragione. È l'unità con cui questo documento chiude un debito ereditato.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `docs/kpi_operators.md` definisce un operatore completo per ciascuno degli otto KPI di `docs/business_case.md` §5.5, verificabile confrontando l'elenco degli otto nomi semantici con quello della scheda.
- **SC-002**: Nessun numero nel documento è il risultato di un calcolo su dati reali: ogni valore citato è un input già ancorato da un artefatto di una feature precedente, verificabile per assenza di qualunque cifra priva di ancora o marcatore.
- **SC-003**: Le quattro decisioni più esposte (D1-D4) sono riportate, con la propria ragione, in forma compatta al terzo punto di stop del flusso, prima che `docs/kpi_operators.md` venga scritto.
- **SC-004**: `scripts/check_audit_coherence.py` passa in severità stretta su `docs/kpi_operators.md`, e continua a passare sui cinque documenti esistenti.
- **SC-005**: Nessun operatore del documento presenta la confidenza di un KPI diversa da quella già fissata in `docs/business_case.md` §5.4.
- **SC-006**: Chi legge solo `docs/kpi_operators.md` e `docs/data_model.md` — senza riaprire alcuna revisione precedente — può scrivere la misura DAX di ciascuno degli otto KPI senza dover prendere alcuna decisione analitica propria.
- **SC-007**: `README.md` riflette la feature conclusa, verificabile confrontando la tabella di stato con lo stato descritto in questa spec.

Sette criteri, verificabili sul prodotto da chi riceve il repository senza sapere come è stato costruito. La stima di 4 ore, revisione inclusa, è un vincolo di processo del principio III e non compare fra loro.

---

## Stima e scomposizione

**4 ore**, di cui ~1,5 per la revisione in contesto pulito e la chiusura dei rilievi — dichiarata nel prompt di consegna, non ricalcolata qui. Se le nove decisioni (in particolare le quattro più esposte, D1-D4) richiedono più di ~2 ore di argomentazione per essere prese in modo difendibile, la sessione esecutiva si ferma al terzo punto di stop e riporta invece di comprimere l'argomentazione: la scomposizione ulteriore è decisione di regia, non della sessione esecutiva — lo stesso vincolo che il prompt di consegna dichiara esplicitamente.

Questa spec non propone una scomposizione in due feature separate, a differenza della `006`: le nove decisioni sono interdipendenti in modo che una scomposizione a metà lascerebbe alcuni operatori (per esempio `BQ2-K3`, che compone `BQ2-K1` e `BQ2-K2`) privi delle decisioni da cui dipendono se le due metà finissero in sessioni diverse. Il documento si scrive per intero o non si scrive.

---

## Assumptions

- **La stabilità degli assi e degli estremi ancorati di `dim_category_mood` regge per l'intera durata di questa feature.** Se `CF-1` venisse chiuso a metà lavoro con una versione 2 che cambia anche gli estremi ancorati (non solo le celle in conflitto), gli operatori di D1 e D2 andrebbero riverificati — ma questa feature non è progettata per assorbire quel caso senza fermarsi, e comunque il chore che chiude `CF-1` è dichiarato **dopo** questa feature nella roadmap.
- **Le nove decisioni non richiedono alcun calcolo su dati reali per essere argomentate.** Ogni ragione portata in D1-D9 poggia su proprietà strutturali già dichiarate da feature precedenti (scale, grane, soglie), non su un'esplorazione dei dati che questa feature non fa.
- **`007b` legge `docs/kpi_operators.md` così come pubblicato, senza rinegoziare le decisioni.** Se una decisione si rivelasse insostenibile in fase di implementazione DAX — per esempio, un limite del linguaggio che rende un operatore non esprimibile come definito — quello è un ritrovamento della `007b`, da dichiarare con nota in loco su questo documento, non una libertà implicita di deviare in silenzio.
- **Il criterio di confronto di D6 (0,5 punti percentuali) si applica solo al confronto fra `reports/data_profile.json` e `reports/cleaning_report.json`** sulle quote di zeri per genere. Non è dichiarato come regola generale di confronto per altre coppie di valori del progetto, e non va estesa oltre quel caso senza una decisione esplicita.

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ1 — Posizionamento**, **BQ2 — Segmento di ingresso**, **BQ3 — Impatto stimato**. Le tre insieme, non una sola — ed è un fatto insolito rispetto alle feature precedenti, dichiarato qui invece di forzare questa feature dentro una domanda sola. `BQ3` non riceve operatori nuovi: i suoi due KPI (`premium_tier_adoption_rate`, `arpu_uplift`) sono già derivati per intero dalla `004`, con formula, ancoraggio e note d'unità pubblicate. Questa feature copre invece gli operatori mancanti di tutti e sei i KPI di `BQ1` e `BQ2`.
- **Contributo**: senza queste nove decisioni, tre dei sei KPI di `BQ1`/`BQ2` non hanno una formula univoca — `BQ1-K3`, `BQ2-K2` e `BQ2-K3` ammetterebbero più letture incompatibili — e tutte e tre le condizioni della regola di decisione della North Star (`business_case.md` §3, C1, C2 e C3) non sarebbero verificabili senza un operatore dichiarato: C1 tramite D9, C2 tramite D1, C3 tramite D4. Questa feature non calcola la risposta a nessuna delle tre domande: fissa le regole che la renderanno una risposta difendibile invece che un numero fra tanti ugualmente possibili.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

Questa feature non introduce alcuna nuova fonte dati: eredita per intero la classificazione già fissata da `docs/business_case.md` §5.4, e la tabella seguente la riporta senza modificarla, come richiesto da FR-015.

| KPI | Nome semantico | Fonte | Confidenza | Formato di presentazione | Operatore fissato da |
|---|---|---|---|---|---|
| `BQ1-K1` | `music_adjacent_catalog_share` | Netflix (reale) | alta | valore puntuale | D9 |
| `BQ1-K2` | `format_duration_gap` | Derivato (Netflix + Spotify) | alta | valore puntuale | D5, D8 (parte `R13`) |
| `BQ1-K3` | `mood_profile_overlap` | Derivato (Netflix + Spotify) | media | valore puntuale con nota | D1, D7 |
| `BQ2-K1` | `segment_demand_index` | Spotify (reale) | media | valore puntuale con nota | D6, D7 |
| `BQ2-K2` | `segment_catalog_affinity` | Derivato (Netflix + Spotify) | media | valore puntuale con nota | D2, D7 |
| `BQ2-K3` | `segment_entry_priority` | Derivato (`BQ2-K1` + `BQ2-K2`) | media | ordinamento | D3, D4, D8 |
| `BQ3-K1` | `premium_tier_adoption_rate` | Benchmark (esterno) + Sintetico | bassa | range best/base/worst | già chiuso dalla `004`, nessun operatore nuovo qui |
| `BQ3-K2` | `arpu_uplift` | Derivato (`BQ3-K1` + prezzi A4) | bassa | range best/base/worst | già chiuso dalla `004`, nessun operatore nuovo qui |

**Assunzioni dietro le decisioni**, dichiarate per iscritto:

1. **Assunzione di indipendenza per asse** (D1, D2): l'appartenenza all'intervallo occupato e la distanza fra profili trattano i tre assi di mood come indipendenti — nessuna compensazione geometrica fra energia, positività e ritmo. È l'assunzione minima coerente con l'ancoraggio solo agli estremi di `content_taxonomy_bridge.md` §7, non verificata da alcun dato perché nessun dato la potrebbe verificare (il centro della scala non è ancorato).
2. **Assunzione di equipeso** (D3): domanda e affinità di catalogo pesano allo stesso modo in `segment_entry_priority_score`, per assenza di un criterio esterno che le differenzi. È una scelta dichiarata, non l'unica difendibile.
3. **Assunzione di soglia mediana** (D4): "alta domanda" e "alta affinità" significano "sopra la mediana dei 114 segmenti", non un valore assoluto — coerente con la formulazione ordinale di `business_case.md` §4 («la soglia di ingresso è ordinale: conta la posizione relativa tra segmenti, non un valore assoluto»).

**Nessuna promozione di confidenza**: nessuna delle nove decisioni fa salire la confidenza di alcun KPI oltre quella già fissata dal business case.

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: quale sia il valore di alcun KPI. Questo documento definisce solo come calcolarli; nessun numero dei KPI compare qui, e chi lo cercasse in questa feature non lo troverà.
- **Non risponde a**: se le nove decisioni prese siano le uniche difendibili. Ciascuna dichiara le opzioni scartate e la ragione della scelta, ma nessuna pretende di essere l'unica lettura corretta della propria scheda — sono scelte argomentate, non deduzioni univoche, ed è il motivo per cui ciascuna è affidata alla revisione in contesto pulito prima di diventare definitiva.
- **Inferenza da evitare — un operatore fissato non è un valore verificato.** Che una formula sia ben argomentata non garantisce che il numero che ne uscirà sia corretto: resta da implementarla (`007b`), da verificarla contro un motore reale (materializzazione), e da sottoporla alla propria revisione. Questo documento riduce l'arbitrarietà della formula, non l'incertezza del risultato.
- **Inferenza da evitare — il prodotto cartesiano di D1 non è la misura più stretta possibile.** Chi legge `BQ1-K3` deve sapere che il valore pubblicato sovrastima la sovrapposizione reale rispetto a un inviluppo convesso, per la ragione dichiarata in D1 — non è un errore, è un limite strutturale della scelta.
- **Inferenza da evitare — la distanza di `BQ2-K2` non è confrontabile con una distanza osservata altrove.** La sua grandezza assoluta ha senso solo relativamente ad altri segmenti calcolati con la stessa formula sugli stessi assi (D2), non come una distanza fisica o percettiva assoluta.
- **Copertura del dato**: eredita per intero i limiti già dichiarati da `docs/business_case.md` (A1-A6) e da `docs/data_model.md` §18 — cataloghi proxy, non StreamWave; copertura ferma al 2021 (video) e al 2022 (musica, non verificabile); nessun dato comportamentale. Questa feature non ne introduce di nuovi, perché non tocca alcun dato.
- **Dove è esposto all'utente finale**: `docs/kpi_operators.md` è un documento tecnico, non rivolto al board — i suoi limiti (in particolare D1, D2, D4) devono essere ereditati e ripresentati in forma comprensibile da `008b`, che porta i limiti dichiarati sullo schermo dove il lettore della dashboard li incontra.
