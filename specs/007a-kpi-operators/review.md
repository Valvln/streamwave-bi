# Verbale di revisione in contesto pulito — `docs/kpi_operators.md`

**Feature**: `007a-kpi-operators` · **Data**: 2026-08-21

## Come la revisione è stata dispacciata

La revisione è stata affidata a un **subagent isolato** — modello `Claude Sonnet 5` — che ha ricevuto **un solo file**: una copia di `docs/kpi_operators.md` in una cartella vuota **fuori dal repository**, con il vincolo esplicito di non aprire nient'altro. Non ha ricevuto la spec, il piano, i task, il quickstart, gli altri documenti di `docs/`, gli artefatti di `reports/`, né alcuna history git.

La forma è più stretta di una sessione umana a cui si incolla il testo: una sessione vuota vede ciò che le si dà, ma potrebbe raggiungere il resto; questa non aveva modo di sapere che il resto esistesse. È la stessa forma già adottata in [`specs/005-data-model-design/review.md`](../005-data-model-design/review.md).

Chi ha scritto il documento non lo ha revisionato.

## La versione revisionata

| | |
|---|---|
| File | `docs/kpi_operators.md` |
| Commit | `23da280966e7381c174ff04e7624e256b6518d62` (`23da280`) |
| Messaggio | `feat: gli operatori delle otto misure e le nove decisioni che li fissano` |
| sha256 del contenuto letto | `ef4b542b4072087b1801823a87c04205b3b7e62d7c3909ef7f1880c254ff2627` |
| Righe | 323 |

Il documento verrà riscritto per chiudere i rilievi: i passaggi citati nel verbale vanno cercati in quella versione, non nella corrente.

## Che cosa segue

Il testo sotto è il verbale del revisore, **riportato integralmente e senza modifiche**. Non viene corretto, nemmeno dove sbaglia. L'esito della verifica di ciascun rilievo sta nel blocco di chiusura in coda, che è l'unica aggiunta ammessa.

---

# Verbale di revisione — `kpi_operators.md`

## 1. Apertura — perimetro della lettura

Ho letto **esclusivamente** il file indicato: `kpi_operators.md`, 324 righe, dalla riga 1 all'ultima. Non ho aperto, cercato o consultato nient'altro: non `business_case.md`, non `data_model.md`, non `data_audit.md`, non `content_taxonomy_bridge.md`, non `convenzioni-marcatura.md`, non `bq3_scenarios.md`, non i report JSON citati, non la history git, non alcuna risorsa di rete. Non ho usato strumenti di ricerca fuori dalla cartella indicata. Non so come questo documento sia stato costruito, chi lo abbia scritto, né se le citazioni interne (a `data_model.md §11`, `§14`, `§18`, `§19`, alle revisioni `001`/`002`/`003`, ai valori ancorati con `&lt;!--@...--&gt;`) siano corrette: le tratto come affermazioni non verificabili da questo solo file, e lo dichiaro esplicitamente ogni volta che rilevo qualcosa che dipenderebbe da quella verifica. Non ci sono state uscite dal perimetro dichiarato.

Il documento stesso dichiara di non contenere valori dei KPI, solo regole di calcolo (operatori). Ho verificato questa dichiarazione internamente — cercando cifre che sembrassero risultati anziché input — e la trovo rispettata: ogni numero che ho incontrato è o un conteggio/input marcato con ancora (`&lt;!--@...--&gt;`), o un numerale in lettere marcato come non misurato (`&lt;!--#--&gt;`), coerentemente con la grammatica che il documento stesso descrive (che non ho potuto verificare contro `convenzioni-marcatura.md`, non letto).

---

## 2. I rilievi

### R1 — Bloccante. L'argomento di invarianza per il numeratore di `BQ1-K1` (§2.1, `D9.1`) non dimostra ciò che afferma

Il passaggio (righe 41-46) vuole stabilire che il conteggio di titoli in `Music &amp; Musicals` è lo stesso sul dato di origine e sul dato trasformato, così da poter usare il valore 375 letto dal profilo di origine come se fosse un valore del modello dati corrente. Per farlo cita **due** fatti: (a) il numero totale di titoli distinti non cambia (8.807 = 8.807); (b) le uniche righe toccate dalla riparazione sono 3, e la riparazione è uno spostamento di campo sulla *durata*, non un'imputazione o un'eliminazione.

Da questi due fatti il testo conclude: «la trasformazione non aggiunge titoli, non ne rimuove e non ne cambia l'assegnazione di categoria». Ma **nessuno dei due fatti citati riguarda l'assegnazione di categoria**. Il fatto (a) dice che il *conteggio totale* di titoli non cambia — che è compatibile con titoli rimossi e altri aggiunti in pari numero, o con riassegnazioni di categoria che lascino invariato il totale. Il fatto (b) riguarda esclusivamente la colonna della durata, non `bridge_title_category`. La riga 31 dichiara peraltro che il numero di assegnazioni (19.323) è diverso dal numero di titoli (8.807), quindi il ponte titolo-categoria subisce una qualche trasformazione rispetto a un'ipotetica corrispondenza 1:1 — ed è proprio su *quella* trasformazione che l'argomento di invarianza avrebbe bisogno di un fatto ancorato, e non lo fornisce.

In altre parole: il documento promette che chi implementa non debba fidarsi di un numero non ancorato, ma qui chiede di fidarsi di una conclusione («l'assegnazione di categoria non cambia») che le premesse citate non sostengono. Ciò che lo renderebbe difendibile: un terzo fatto ancorato specifico su `bridge_title_category` — ad esempio l'assenza di righe scartate o rimappate nella costruzione del ponte — oppure, in mancanza, la dichiarazione esplicita che l'invarianza sull'assegnazione di categoria è un'**assunzione** e non una conseguenza dimostrata dei due fatti citati.

### R2 — Bloccante. La motivazione di `D2` (§6) per preferire la distanza media assoluta all'euclidea confonde due proprietà distinte

Il passaggio (righe 169-171) sostiene che la distanza euclidea «permette a uno scostamento piccolo su un asse di compensare uno scostamento grande su un altro» — un'assunzione geometrica non giustificata dall'ancoraggio solo agli estremi — mentre la media delle distanze assolute «tratta i tre assi in modo indipendente e additivo» e non richiederebbe questa assunzione.

Il problema: la proprietà che il documento chiama «compensazione» (uno scostamento piccolo su un asse che bilancia uno grande su un altro, producendo lo stesso valore aggregato) non è una peculiarità della distanza euclidea. È una proprietà di **qualunque aggregazione lineare o quasi-lineare di più assi**, media aritmetica inclusa: se un profilo ha `|1, 0, 0|` e un altro `|0.33, 0.33, 0.33|`, la media delle distanze assolute li tratta come equivalenti (0,33 in entrambi i casi) esattamente nello stesso senso in cui l'euclidea li tratterebbe come vicini fra loro (a meno del fattore di scala). Nella letteratura sui metodi multicriterio, una somma o media pesata è di fatto il caso paradigmatico di aggregazione **pienamente compensativa** — non quello che la evita.

L'unico argomento che il passaggio dimostra davvero è quello enunciato più avanti nello stesso paragrafo: la media delle distanze assolute non richiede una **costante di normalizzazione aggiuntiva** (la divisione per √3 dell'euclidea) per restare nel dominio `0-1`. Questo è un punto valido e sufficiente da solo a motivare la scelta. Ma il documento lo salda a un secondo argomento — l'assenza di un'assunzione di compensazione — che non è stabilito e che, per come è formulato, sembra applicarsi altrettanto alla scelta fatta quanto a quella scartata. Poiché `D2` è la decisione analitica più elaborata del documento e viene ereditata da `D3`/`BQ2-K3` (§7), il difetto non è isolato.

Che cosa lo renderebbe difendibile: rimuovere l'argomento sulla «compensazione» e mantenere solo quello sulla normalizzazione — che regge da solo — oppure sostituire l'argomento con uno che distingua correttamente le due proprietà (per esempio: un operatore non lineare come il massimo per-asse sarebbe l'aggregazione davvero non compensativa, e va argomentato perché non è quella scelta).

### R3 — Bloccante. Le tabelle §10 e §11 si contraddicono sull'attribuzione di `D8`

La tabella di sintesi (§10, riga «D8») definisce `D8` in modo univoco come «prima posizione della graduatoria = punteggio più alto», applicata in `§7.3` — cioè a `BQ2-K3` (`segment_entry_priority`). Il testo di `§7.3` è coerente con questo.

La tabella di provenienza e confidenza (§11) attribuisce però `D8` **anche** a `BQ1-K2`: «Operatore fissato da: D5, D8 (parte `R13`)». Il testo di `§3`, che discute `BQ1-K2`, non nomina mai `D8` — parla solo di «la parte residua di `R13` su questo KPI» come cosa distinta da `D5`, senza etichettarla.

Questo è un conflitto diretto fra due tabelle dello stesso documento: o `D8` è in realtà due decisioni distinte che condividono per errore lo stesso identificativo (il che vanifica la tracciabilità che le sigle `D1`-`D9` dovrebbero garantire — è letteralmente lo scopo di §10), oppure la riga di `BQ1-K2` in §11 è sbagliata e andrebbe corretta rimuovendo il riferimento a `D8` o etichettando come decisione nuova la parte residua di `R13` citata in §3. Un documento che promette a chi implementa zero ambiguità residue non può lasciare le proprie tabelle di riferimento in disaccordo fra loro su quale decisione governi quale KPI.

### R4 — Bloccante. `D9.2` è citata ma mai definita

Riga 23: «**Decisioni di riferimento**: `D9.1`, `D9.2`, `D9.3`» in apertura di §2. Il corpo di §2.1 discute `D9.3` (righe 35-37) e `D9.1` (righe 39-46) per esteso. `D9.2` non ricompare **in nessun punto successivo del documento** — non in §2.2, non nella tabella di sintesi di §10 (che elenca solo `D9` come voce unica, senza scomporla in sotto-voci), non in §11. Un lettore che cerchi che cosa `D9.2` fissa non lo trova. O manca un passaggio del testo, o l'etichetta è residua di una versione precedente del documento e andrebbe rimossa dalla riga 23.

### R5 — Minore/operativo. Il metodo di calcolo della mediana non è mai specificato

La mediana è l'operatore statistico più usato nel documento: compare in `BQ1-K1/C1` (§2.2, mediana di 42 conteggi — numero pari di categorie), `BQ2-K1` (§5, mediana della popolarità per segmento), `BQ2-K2` (§6, mediana di ciascun asse su entrambi i lati), `BQ2-K3` (§7.2, mediana su 114 segmenti — numero pari). In nessun punto il documento dichiara la convenzione per il caso di conteggio pari di osservazioni (media dei due valori centrali è la convenzione standard, ma non è mai scritta) né come trattare eventuali valori ripetuti al centro della distribuzione. Per variabili continue l'impatto pratico è probabilmente trascurabile, ma per il conteggio di titoli per categoria (§2.2, valori interi, 42 categorie) il caso è meno innocuo: la mediana di 42 interi può non essere un intero, e il confronto «supera la mediana» richiede che l'implementatore scelga comunque una convenzione — la stessa cosa che il documento in §7.2 dichiara doversi decidere esplicitamente («va deciso perché altrimenti resterebbe implicito in chi implementa») per la soglia stretta del quadrante, ma non applica a sé stesso per la definizione di mediana. È un'incoerenza di standard interno, oltre a un buco di completezza operativa.

### R6 — Minore. La tabella §11 attribuisce a `D6` un ruolo che il testo di §5.3 esplicitamente nega

§11, riga `BQ2-K1`: «Operatore fissato da: D7, D6». Ma §5.3 dichiara testualmente: «Questa decisione non entra nella formula del KPI» (riga 139), essendo `D6` una soglia di confronto fra due artefatti di rendicontazione, non un ingrediente dell'operatore `segment_demand_index`. La colonna della tabella si chiama proprio «Operatore fissato da», e includervi `D6` senza la riserva presente nel corpo del testo può far credere a chi legge solo la tabella che `D6` intervenga nel calcolo del KPI, cosa che il documento stesso esclude altrove.

---

## 3. Le divergenze

### Divergenza 1 — §3, `format_duration_gap`: «pubblica il segno, non il valore assoluto» ammette due letture incompatibili

Riga 68: «Il documento pubblica il **segno** del risultato, non il valore assoluto.» Due letture sono entrambe plausibili dal solo testo:

- **Lettura A**: il KPI finale, quando la `007b` lo calcolerà, esporrà **solo** il segno (`+`/`−`), scartando la grandezza in minuti — un `format_duration_gap` che non porta più l'informazione di "quanto".
- **Lettura B**: *questo documento* (che per dichiarazione di §1 non contiene alcun valore) si limita a fissare la **convenzione di segno** dell'operatore, senza esprimersi sulla grandezza — che la `007b` calcolerà come numero completo, con segno, quando i dati esisteranno.

Il resto del paragrafo non scioglie l'ambiguità in un senso univoco: la frase «porta l'informazione su quale dei due formati sia più lungo, che andrebbe perduta pubblicando il solo valore assoluto» (riga 76) sembra confrontare "segno" con "valore assoluto" come le due componenti di un numero con segno — supportando la lettura B, dato che se si scartasse tutto tranne il segno si perderebbe comunque la grandezza, non solo se si pubblicasse il valore assoluto. Ma la riga 78 parla di «quando il numero comparirà», il che presuppone che un numero (non solo un simbolo) sarà effettivamente pubblicato — anche questo compatibile con B più che con A. Nessuna delle due letture è però resa esplicita: il documento non dice mai, in termini inequivocabili, se `format_duration_gap` come misura finale sarà un valore in minuti con segno o un semplice indicatore di segno. Per un KPI il cui stesso nome (*gap*) implica una grandezza, questa non è un'ambiguità trascurabile, ed è esattamente il tipo di decisione che il documento dichiara di voler chiudere per conto di chi implementa.

Non ho trovato altre divergenze di questo tipo (due letture ammesse e non scelte) nel resto del documento: le altre nove decisioni sono argomentate e chiuse, anche dove l'argomentazione stessa è debole (R1, R2).

---

## 4. Che cosa il documento fa bene

Vale la pena dirlo con la stessa esattezza dei rilievi, perché i punti di forza sono reali e non generici:

- **La disciplina sulle affermazioni derivate è applicata, non solo dichiarata.** §2.1 (D9.3) rifiuta esplicitamente di calcolare il rapporto della North Star per giustapposizione di numeratore e denominatore già pubblicati altrove — esattamente il tipo di errore che il progetto dichiara di voler evitare — e §5.2 rifiuta di quantificare "quanto" sia sbilanciato il campione perché nessun artefatto pubblica il massimo o una misura di dispersione. Sono due casi in cui il documento si nega un'affermazione comoda per mancanza di fonte, invece di scriverla e sperare che nessuno controlli.
- **La distinzione di grana è tenuta a fuoco costantemente**, ed è dichiarata come "trappola" esplicita più volte (§2.1: titoli distinti vs. assegnazioni; §2.2: la stessa distinzione applicata al lato video; §5: valore letto dalla tabella di fatto e mai dalla dimensione). È precisamente la categoria di errore più insidiosa in un modello a stella, ed è trattata con attenzione reale, non con una menzione di circostanza.
- **Il documento dichiara sistematicamente che cosa un operatore *non* fa** (§2.2, §6, §9) invece di lasciarlo intuire. Questo riduce lo spazio per un'estensione impropria da parte di chi implementa.
- **Le scelte "comode ma non ovvie" sono segnalate come tali**, non presentate come le uniche corrette: il peso 0,5/0,5 di `D3` (§7.1) e la soglia di mezzo punto di `D6` (§5.3) sono entrambe accompagnate da una dichiarazione esplicita che sono scelte, non deduzioni, con il perimetro della loro validità dichiarato (§5.3 è particolarmente accurato nel delimitare a cosa la soglia si applica e a cosa no).
- **§13 è onesto sul limite del controllo automatico**: dichiara esplicitamente che nessuno script verifica l'argomentazione, il che è vero — ed è precisamente la ragione per cui i rilievi R1 e R2 di questo verbale sono difetti che nessun controllo di coerenza avrebbe potuto trovare.

Il difetto ricorrente, quando c'è, non è la sciatteria ma l'eccesso di ambizione argomentativa: il documento a volte cerca di giustificare una scelta con più ragioni di quante ne servano (R2), o costruisce una catena di inferenza con un anello mancante (R1) invece di dichiarare più modestamente un'assunzione. Sono difetti dello stesso tipo che un secondo giro di revisione, mirato specificamente ai passaggi di `§2.1` e `§6`, risolverebbe con probabilità alta.
