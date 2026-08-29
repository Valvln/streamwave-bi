# Feature Specification: Il verdetto e la raccomandazione

**Feature Branch**: `009-verdetto-raccomandazione`

**Created**: 2026-08-29

**Status**: Draft

**Input**: User description: "Pubblicare `C2` come valore ancorato con il proprio operatore, applicare la regola di decisione già scritta in `business_case.md` §3, e trasformarne l'esito in `docs/raccomandazione.md` — la risposta al board che il progetto non ha mai prodotto. Cinque prodotti: l'operatore di `C2` e la sua soglia, con nota in loco su `kpi_operators.md` §12; `C2` come booleano ancorato più il margine di robustezza rispetto alla stima per eccesso di `kpi_measures.md` §4.3; il verdetto congiunto ancorato, esteso dentro `reports/kpi_measures.json`; il documento nuovo `docs/raccomandazione.md`; la tabella di sensibilità parametrica su `BQ3-K2`. Chiude la issue `#17` e la sostanza della `#28`. Perimetro: nessun Power BI, nessuna impaginazione, nessun ricalcolo di KPI esistenti, nessuna quantificazione della base utenti, nessuna modifica a `docs/roadmap.md` o a `data/`."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come decisione, requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

---

## La domanda a cui questa spec risponde per prima

Nove feature hanno costruito un apparato di misura e nessuna ha risposto alla domanda per cui esiste. La revisione in contesto pulito della `008b` lo ha detto in una riga — *«un decisore che non conclude niente non ha usato la dashboard, l'ha archiviata»*.

La domanda che precede ogni riga di questa feature non è però *quale sia la risposta*: è **con quale titolo una sessione esecutiva può darla**. La risposta a questa seconda domanda è ciò che rende la feature eseguibile invece che arbitraria, e sta in un fatto già nel repository: [`business_case.md`](../../docs/business_case.md) §3 contiene una regola di decisione a tre condizioni, **fissata e pubblicata prima che i numeri esistessero**, con la lettura di ciascun esito già scritta. Due condizioni su tre sono soddisfatte e ancorate; la terza è calcolabile e non è mai stata pubblicata.

**Questa feature non decide se la risposta sia sì. Esegue una regola scritta da altri, in un momento in cui nessuno poteva sapere che numeri sarebbero usciti.** Il verdetto che ne esce non è un giudizio della sessione che lo pubblica: è l'applicazione di un criterio pubblico a valori già misurati. È la sola forma in cui una conclusione può comparire in questo repository senza contraddire il principio I — un numero senza fonte non è ammesso, e un giudizio senza regola dichiarata è la stessa cosa un livello più in alto.

Ne discende il vincolo che governa l'intera feature: **dove la regola esiste, la si applica e basta; dove la regola manca, si dichiara che la si sta scrivendo, e si argomenta**. C'è esattamente un punto in cui manca, ed è l'operatore di `C2`.

---

## Le decisioni che questa feature prende

Otto decisioni, numerate `V1`-`V8`. Ciascuna riporta il debito o la lacuna che l'ha sollevata, le opzioni sul tavolo, la scelta e la ragione. La lettera `V` non è mai stata usata in questo progetto per una sigla di decisione, ed è già coperta dall'esclusione strutturale del controllo di coerenza.

---

### V1 — L'operatore di `C2`: soglia a metà del catalogo musicale, condizione stretta

**Il contesto.** `C2` chiede che «la **maggioranza** del catalogo musicale accessibile ricada nella regione di mood già occupata dal catalogo video» (`business_case.md` §3). La misura che la serve è `BQ1-K3`, che vale `0,8450` — ma «maggioranza» **non ha operatore in alcun documento del progetto**. È il terzo vincolo aperto di [`kpi_operators.md`](../../docs/kpi_operators.md) §12 nella parte che riguarda `C2`, ed è la issue [`#17`](https://github.com/Valvln/streamwave-bi/issues/17) (rilievo `R12` della revisione `007b`).

**Le opzioni**: (a) maggioranza semplice, soglia `0,50`, condizione **stretta** — la quota deve **superare** la metà; (b) maggioranza semplice, soglia `0,50`, condizione **larga** — una quota esattamente pari a metà soddisfa; (c) una maggioranza qualificata — due terzi, tre quarti — argomentata come «maggioranza sostanziale»; (d) una soglia relativa, per esempio la quota che ci si attenderebbe da una regione di mood costruita a caso.

**La decisione**: **(a)**. `C2` è soddisfatta se e solo se `mood_profile_overlap` **supera** `0,50`. Soglia stretta: una quota esattamente pari a metà **non** soddisfa la condizione.

**La ragione, in tre passi.**

*Perché `0,50` e non una soglia qualificata.* «Maggioranza», in italiano e senza qualificazione, significa più della metà. Le opzioni (c) e (d) sono difendibili in astratto ma richiederebbero un argomento che il business case non contiene: chi ha scritto `C1` e `C3` ha usato la mediana — cioè metà dell'insieme — in entrambe, e leggere la terza condizione con un metro più severo introdurrebbe una severità che nessuno ha chiesto, **dopo** aver visto il valore. È esattamente la mossa che la regola di decisione esiste per impedire. La direzione opposta — una soglia più bassa — sarebbe peggio: renderebbe la condizione più facile a numeri noti.

*Perché stretta e non larga.* Per coerenza con le due condizioni sorelle, entrambe già fissate come strette: `C1` in `D9.2` («**supera** la mediana»), `C3` in `D4` («un segmento esattamente sulla mediana non entra nel quadrante»). La convenzione del progetto sui confronti di soglia è la condizione stretta, ed è già dichiarata due volte. Adottarne una terza diversa qui costringerebbe chi legge a ricordare quale delle tre condizioni usa quale confine.

*Perché la scelta è quasi priva di conseguenze, e va detto.* Il valore misurato dista molto dalla soglia in entrambe le letture: **la distinzione fra stretta e larga non cambia l'esito di `C2` su questi dati**, e non lo cambierebbe nemmeno una soglia a due terzi. La decisione va comunque presa e dichiarata — altrimenti resterebbe implicita in chi implementa, che è il difetto che `D4` esiste per evitare — ma dichiararla senza dire che è inconseguente su questi dati significherebbe attribuirle un peso che non ha. Chi contesta la soglia deve sapere che contestarla non ribalta nulla: **ciò che ribalterebbe `C2` è dichiarato in `V3`, e non è la soglia.**

**Dove si registra**: nota in loco in coda a `kpi_operators.md` §12, senza riscrivere il testo esistente, e una riga nella tabella delle decisioni di §10 come **`D12`**. La nota chiude la parte di issue `#17` che riguarda l'operatore.

---

### V2 — `C2` è un valore dell'artefatto, non un confronto fatto in prosa

**Il contesto.** La regola `D5` sulle affermazioni derivate ([`convenzioni-marcatura.md`](../../docs/convenzioni-marcatura.md) §7) stabilisce che un confronto costruito su valori misurati è esso stesso un valore misurato: o esiste nell'artefatto con un identificativo proprio, o non si scrive. `C2` è il confronto fra `0,8450` e una soglia.

**Le opzioni**: (a) scrivere in prosa «`0,8450` supera `0,50`, quindi `C2` è soddisfatta», ancorando i due numeri; (b) pubblicare `C2` come voce booleana dell'artefatto, con la soglia come voce propria, e ancorare l'esito.

**La decisione**: **(b)**, sullo schema identico già usato per `C1` (`KPI.BQ1K1.c1.above_median`) e `C3` (`KPI.BQ2K3.c3_satisfied`).

**La ragione**: (a) è precisamente la forma che `D9.3` ha vietato per la North Star — «il rapporto non nasce per giustapposizione» — e che le tre affermazioni errate trovate dalla revisione della `002` avevano in comune. Un esito che il lettore deve ricavare accostando due numeri è un calcolo fatto a mente, e nessun controllo lo verifica. In più: `C1` e `C3` esistono come booleani ancorati, e pubblicare la terza condizione in una forma diversa dalle sue due sorelle renderebbe la regola di decisione leggibile solo a chi sa che le tre voci vivono in tre posti diversi.

---

### V3 — Il margine di robustezza: quanto la stima dovrebbe sbagliare perché `C2` cada

**Il contesto.** `kpi_measures.md` §4.3 dichiara che `0,8450` è una **stima per eccesso**: il parallelepipedo allineato agli assi contiene sempre l'inviluppo convesso che vi si iscrive e in genere lo eccede, quindi la sovrapposizione reale è **minore o uguale** al valore pubblicato, «e quanto minore questo progetto non lo misura». Il rilievo `R19` della revisione `008b` osserva che a schermo di tutto questo resta solo l'inquietudine: il blocco ha conservato la parte difficile — come è costruita la regione — perdendo quella utile, di quanto il valore è gonfiato.

**Le opzioni**: (a) lasciare il limite come dichiarazione qualitativa, come oggi; (b) stimare la sovrapposizione reale costruendo l'inviluppo convesso; (c) pubblicare la **distanza fra il valore e la soglia** come valore ancorato, e leggerla come la sovrastima massima che `C2` tollera.

**La decisione**: **(c)**. L'artefatto guadagna la distanza `mood_profile_overlap − soglia` come voce propria, e `docs/raccomandazione.md` la usa per dire, in una frase che un decisore può ripetere: perché `C2` cada, la stima dovrebbe eccedere la sovrapposizione reale di più di quel margine.

**La ragione.** (a) è ciò che ha prodotto il rilievo `R19` e non va ripetuto. (b) è **fuori perimetro e resterebbe fuori anche con più tempo**: `data_model.md` §11 non costruisce alcuna struttura congiunta a tre dimensioni, e un inviluppo convesso richiederebbe una regola di aggregazione che nessun documento ha fissato — `kpi_operators.md` §4 lo dichiara esplicitamente come limite strutturale, non correggibile lì. (c) non stima nulla di nuovo: è aritmetica su due valori già pubblicati, ed è esattamente la classe di affermazioni che `D5` obbliga ad ancorare.

**Che cosa il margine dice, e che cosa non dice** — la precisazione va nella spec perché è la sola parte di questa decisione che si può sbagliare scrivendola. Il margine dice: *l'errore della stima dovrebbe essere maggiore di tanto perché la conclusione cambi*. **Non** dice che l'errore sia minore di tanto: nessuno ha misurato l'errore, e questa feature non lo misura. È un argomento di robustezza rispetto a un limite dichiarato — un'affermazione condizionale, non una stima dell'errore — e la prosa che lo pubblica deve rendere impossibile la seconda lettura.

**Ciò che questa decisione realizza sul metodo, e che vale più della condizione stessa**: un limite dichiarato smette di essere un'inquietudine e diventa un argomento. È il modello di che cosa significa sbilanciarsi con rigore, ed è la ragione per cui il rilievo `R19` lo aveva chiesto per nome.

---

### V4 — Il verdetto congiunto vive nell'artefatto delle misure, non in un artefatto nuovo

**Il contesto.** Il verdetto — quante delle tre condizioni sono soddisfatte, e quale delle tre letture di `business_case.md` §3 si applica — è un'affermazione derivata da tre valori misurati, quindi per `D5` esiste come ancora o non si scrive. Resta da decidere **dove**.

**Le opzioni**: (a) un artefatto nuovo, `reports/verdict.json`, con il proprio script; (b) estendere `reports/kpi_measures.json` tramite `scripts/build_kpi_measures.py`; (c) scriverlo a mano in un artefatto curato, sullo schema di `reports/kpi_engine_check.json`.

**La decisione**: **(b)**, che è anche la preferenza dichiarata dalla regia.

**La ragione**: le tre condizioni sono già calcolate dallo stesso script e vivono già nello stesso artefatto — `C1` e `C3` ci sono, `C2` ci entra con questa feature. Un artefatto nuovo costerebbe una riga in `ARTIFACTS` di `check_audit_coherence.py`, una nella tabella di provenienza di `convenzioni-marcatura.md`, e una catena di derivazione fra due artefatti che non compra nulla: il verdetto leggerebbe da `kpi_measures.json` valori che lo script che lo produce ha appena calcolato. (c) è la forma riservata a ciò che **nessuno script può produrre** — una lettura umana, un benchmark raccolto a mano — e il verdetto non è di quella classe: è una funzione deterministica di tre booleani.

**Il vincolo che la scelta impone**: nessuna collisione di prefisso e nessuna nuova voce fuori dallo spazio dei nomi `KPI.`. Le voci nuove sono `KPI.BQ1K3.c2.*` e `KPI.verdict.*`, entrambe dentro il prefisso già verificato contro le collisioni.

---

### V5 — La confidenza del verdetto è la più bassa fra quelle che lo determinano: **media**

**Il contesto.** Il verdetto compone tre condizioni a confidenza diversa: `C1` poggia su `BQ1-K1`, confidenza **alta**; `C2` su `BQ1-K3`, **media**; `C3` su `BQ2-K3`, **media**. Il business case vieta di comporre misure di livelli diversi in un numero solo, «perché il numero risultante nasconderebbe al lettore che una delle sue metà è meno affidabile dell'altra» (`business_case.md`, scheda `BQ2-K3`).

**Le opzioni**: (a) dichiarare il verdetto a confidenza **media**, la più bassa fra le tre; (b) non attribuirgli alcuna confidenza, perché è un esito logico e non una misura; (c) attribuirgli la confidenza di ciascuna condizione separatamente e lasciare al lettore la sintesi.

**La decisione**: **(a)**, con l'argomento esplicito che segue — non per convenzione, perché la convenzione da sola non basterebbe.

**La ragione, e perché il divieto di composizione non è violato.** Il divieto del business case riguarda la fusione di misure di confidenza diversa in **un numero**, dove l'operazione aritmetica mescola le due componenti e le rende indistinguibili. Il verdetto non è quello: è una **congiunzione logica** di tre esiti che restano pubblicati e ancorati **ciascuno separatamente**, ognuno con la propria confidenza dichiarata. Il lettore non perde nulla, perché le tre condizioni continuano a esistere una per una.

Ne discende però la regola di ereditarietà, che è più severa della media e va applicata: una congiunzione è vera solo se lo sono tutti i suoi termini, quindi **la fiducia che si può riporre nel verdetto non può eccedere quella riposta nel suo termine più debole**. Una media aritmetica delle tre confidenze sarebbe l'errore opposto e più insidioso: farebbe salire il verdetto sopra `C2` grazie alla solidità di `C1`, cioè lascerebbe che la condizione più forte coprisse la più debole. **Il verdetto è quindi a confidenza media, e la ragione è `C2`.**

**Il corollario che la raccomandazione deve portare a schermo**: se una sola condizione dovesse cadere, cadrebbe `C2` — è la più debole delle tre per costruzione, non per accidente — ed è la ragione per cui il margine di `V3` è la parte più importante di questa feature.

---

### V6 — La raccomandazione è un documento a sé, ed è ordinata come un argomento, non come un inventario

**Il contesto.** La dashboard delle feature `008a`/`008b` è impaginata lungo le tre domande di business — una pagina per domanda — cioè è un inventario di misure. Il verbale della `008b` mostra che a un decisore serve la spina opposta.

**Le opzioni**: (a) aggiungere una sezione conclusiva a `kpi_measures.md`; (b) un documento nuovo, `docs/raccomandazione.md`, ordinato per argomento.

**La decisione**: **(b)**, con questo ordine di sezioni, che è la spina portante del documento e non un indice: **la risposta** → **perché** → **con che cosa entrare** → **quanto vale** → **che cosa lo farebbe cambiare** → **che cosa questa raccomandazione non è**.

**La ragione**: `kpi_measures.md` è organizzato per KPI e si rivolge a chi verifica; questa feature scrive per **un decisore che non ha letto alcun documento del repository e non guarda uno schermo**. Sono due lettori diversi, e un documento che serve entrambi non serve nessuno dei due. La sezione «che cosa lo farebbe cambiare» è ciò che distingue una raccomandazione da un'opinione, e **nessun documento del progetto la contiene ancora**: è la parte che, se il lavoro sfora, non va compressa.

**Il vincolo che nasce dal destinatario**: il documento non presuppone alcuna lettura precedente. Ogni sigla che usa — `BQ1`, `C2`, `is_high_zero_genre` — o è sciolta al primo uso o non compare. È il rilievo `R11` della revisione `007b` applicato preventivamente al documento in cui conta di più.

---

### V7 — Che cosa si raccomanda è una regione del catalogo, non un segmento da scegliere

**Il contesto.** La graduatoria di `BQ2-K3` ordina 114 segmenti e il quadrante ne contiene 33. Nominare il primo è un ordinale su un fatto misurato, ammesso solo perché ancorato (`KPI.BQ2K3.pop.rank`). Ma [`data_model.md`](../../docs/data_model.md) §18 dichiara che i segmenti **si sovrappongono** — una traccia appartiene a più segmenti quando è pertinente a più d'uno — e che contare le righe non li dimensiona.

**La decisione**: la sezione «con che cosa entrare» raccomanda **una regione del catalogo caratterizzata da segmenti**, e dichiara esplicitamente che i segmenti non sono alternative disgiunte fra cui scegliere né quantità sommabili. Il primo in graduatoria si nomina, ancorato, come il candidato di punta; il quadrante si presenta come l'insieme dei candidati, con la sua numerosità ancorata.

**La ragione**: una raccomandazione che trattasse i 33 segmenti come una partizione — «scegliete questo, non quello» — **affermerebbe il falso**, e lo farebbe nel documento più citabile del progetto. La sovrapposizione non è un dettaglio tecnico: cambia che cosa significa «entrare da qui».

**I due vincoli ereditati che questa sezione deve rispettare, entrambi con riferimento puntuale:**

- i 7 segmenti marcati `is_high_zero_genre` portano **domanda non misurata dalla fonte**, non domanda bassa (`kpi_measures.md` §5.3 e §7.4). Nessuna lettura della coda della graduatoria è ammessa senza quell'esclusione dichiarata: la coda è in parte una classifica di copertura del dato, non di preferenza;
- le quantità dei segmenti non si sommano e il conteggio delle righe misura il campionamento, non il mercato (`data_model.md` §18; `kpi_operators.md` §5.2).

---

### V8 — La sensibilità su `BQ3-K2` è parametrica, e il carattere illustrativo si **marca**, non si scrive soltanto

**Il contesto.** La revisione della `001` decise di non quantificare alcuna base di abbonati. Il rilievo `R8` della `008b` mostra il prezzo: al lettore resta la ricetta della moltiplicazione senza il presidio che la qualificava, davanti a un lettore che una stima di abbonati ce l'ha — *«è la ragione per cui è nella stanza»*.

**Le opzioni**: (a) ripetere il divieto e fermarsi; (b) quantificare una base di StreamWave; (c) una tabella di sensibilità in cui il moltiplicatore lo mette chi legge — l'uplift mensile per alcune basi di riferimento dichiarate come illustrazione parametrica.

**La decisione**: **(c)**. Le basi di riferimento sono **stipulazioni di chi scrive per illustrare l'aritmetica**, non stime della base di StreamWave, e portano il **marcatore di non-misurato** — non solo la dichiarazione in prosa. Ciascuno dei tre scenari di `BQ3` compare per ogni base: la tabella non estrae mai il solo valore centrale.

**La ragione**: (b) è fuori perimetro per una decisione di revisione già presa e non riapribile qui. (a) è lo stato attuale, ed è ciò che il rilievo `R8` giudica insufficiente. (c) non introduce alcun numero senza fonte: le basi sono ipotesi dichiarate di chi legge, e `convenzioni-marcatura.md` §2 ha il marcatore esatto per questa categoria — le soglie e le stipulazioni di chi analizza, che non sono osservazioni sui dati. Marcarle invece di descriverle è ciò che rende la dichiarazione verificabile dal controllo invece che affidata alla buona fede della prosa.

**La formulazione da non usare, con la ragione.** [`bq3_scenarios.md`](../../docs/bq3_scenarios.md) §8 dichiara che «non è scalabile» **è falsa**: il valore *è* scalabile, chiunque disponga di una stima di abbonati lo moltiplica in pochi secondi. Ciò che è vero è più stretto: *qui nessuna base utenti viene quantificata, e l'artefatto non offre alcuna chiave per farlo — non è un presidio, è una rinuncia*. La raccomandazione usa la formulazione stretta. Usare quella comoda ripeterebbe l'errore che l'issue [`#26`](https://github.com/Valvln/streamwave-bi/issues/26) ha già registrato sul contratto di pagina della `008a`.

---

## Rapporto con le feature vicine

| Feature | Rapporto |
|---|---|
| `007b` | fornisce tutti i valori che questa feature legge; `C2` è la lacuna che la sua revisione ha registrato come issue `#17` |
| `008a`, `008b` | superate come deliverable a schermo; il verbale della `008b` è la ragione di questa feature, e la sua issue `#28` è il debito che qui si chiude nella sostanza |
| `010a` | riceve questa raccomandazione come **spina dell'impaginazione**: il report nuovo si disegna lungo questo argomento, e non si può disegnare prima che sia scritto |
| `010b` | porta a schermo ciò che qui è scritto; nessuna decisione di resa visiva appartiene a questa feature |
| `011` | raccoglie l'arretrato del tracker, incluse le issue che questa feature lascia aperte |

---

## Perimetro

**Che cosa questa feature non fa**, e a chi spetta:

| Fuori perimetro | A chi spetta |
|---|---|
| aprire Power BI Desktop, toccare il `.pbix` | a nessuno qui: `010b` costruisce il report nuovo |
| disegnare le pagine del report, decidere visuali o impaginazione | `010a` |
| ricalcolare un KPI esistente o riaprire un operatore già fissato | a nessuno: un valore che risultasse sbagliato è un **ritrovamento** da dichiarare con nota in loco, non da correggere in silenzio |
| quantificare la base utenti di StreamWave | a nessuno (revisione `001`): la sensibilità di `V8` è parametrica |
| risolvere il debito della `004` sulla verificabilità del benchmark | alla regia: è governance. Qui si **dichiara aperto** dove i numeri di `BQ3` compaiono |
| chiudere le issue `#11`, `#18`, `#20`, `#21`, `#26`, `#27`, `#29`, `#30` | non a questa feature: restano aperte, in uno stato dichiarato nell'esito |
| chiudere la issue `#28` per intero | ne chiude la **sostanza** (`R2`, e la materia di `R1`, `R7`, `R8`, `R19`, `R21`); l'impaginazione è di `010a`, la resa a schermo di `010b` |
| modificare `docs/roadmap.md` | alla regia |
| scrivere in `data/raw/` o `data/processed/` | a nessuno: sola lettura (principio II) |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Un decisore che non ha letto nulla arriva a una decisione (Priority: P1)

Un membro del board apre `docs/raccomandazione.md` senza aver letto alcun altro documento del repository, senza guardare uno schermo e senza competenza tecnica. Nella prima frase trova la risposta; scendendo trova perché, con che cosa entrare, quanto vale, che cosa la ribalterebbe, e che cosa la raccomandazione non è.

**Why this priority**: è il deliverable. Nessuna delle altre storie ha valore se questa fallisce.

**Independent Test**: si consegna il solo `docs/raccomandazione.md` a una revisione in contesto pulito, senza spec, senza piano, senza gli altri documenti, e le si chiede se un decisore possa concludere qualcosa. È esattamente la configurazione della revisione obbligatoria di questa feature.

**Acceptance Scenarios**:

1. **Given** un lettore che non ha letto alcun documento del repository, **When** legge la sola sezione di apertura, **Then** sa qual è la risposta e con quale cautela va presa, senza dover risalire ad alcun altro file.
2. **Given** lo stesso lettore, **When** cerca che cosa ribalterebbe la conclusione, **Then** trova una sezione dedicata con condizioni nominate, non un rimando ad altri documenti.
3. **Given** una sigla del progetto (`BQ1`, `C2`, un nome di misura), **When** compare nel documento, **Then** è sciolta al primo uso.

---

### User Story 2 — `C2` esiste come valore ancorato e la regola di decisione si legge per intero (Priority: P1)

`C1` e `C3` erano pubblicate e ancorate; `C2` no, ed è la ragione per cui la `008a` decise di non portare a schermo la regola di decisione (`F6`) e la `008b` la lasciò comparire come buco (rilievo `R2`). Dopo questa feature le tre condizioni si leggono nella stessa forma, dallo stesso artefatto.

**Why this priority**: senza `C2` il verdetto non è calcolabile, e senza il verdetto la storia 1 non ha contenuto.

**Independent Test**: si esegue `python3 scripts/build_kpi_measures.py` e si verifica che l'artefatto contenga la soglia, l'esito booleano di `C2` e il margine; si esegue il controllo di coerenza e si verifica che le ancore del documento risolvano.

**Acceptance Scenarios**:

1. **Given** `reports/kpi_measures.json` rigenerato, **When** si cercano le tre condizioni, **Then** tutte e tre esistono come voci booleane con etichetta propria.
2. **Given** la soglia di `C2`, **When** la si cerca, **Then** è una voce dell'artefatto e non un numero scritto nella prosa.
3. **Given** `docs/kpi_operators.md`, **When** si cerca l'operatore di `C2`, **Then** è dichiarato in una nota in loco con la propria sigla di decisione, e il testo preesistente di §12 non è stato riscritto.

---

### User Story 3 — Il limite della stima per eccesso diventa un argomento di robustezza (Priority: P1)

Chi legge la raccomandazione incontra il fatto che `C2` poggia su una stima per eccesso e, nella stessa frase, quanto quella stima dovrebbe sbagliare perché la conclusione cambi.

**Why this priority**: è il rilievo `R19` della revisione `008b`, ed è il punto in cui questa feature dimostra il proprio metodo invece di dichiararlo.

**Independent Test**: si verifica che il margine esista come valore ancorato e che la prosa che lo pubblica non sia leggibile come una stima dell'errore.

**Acceptance Scenarios**:

1. **Given** il margine, **When** compare nel documento, **Then** porta un'ancora verso l'artefatto.
2. **Given** la frase che lo pubblica, **When** la si legge, **Then** afferma una condizione sull'errore («dovrebbe superare»), mai una stima dell'errore («l'errore è minore di»).

---

### User Story 4 — I numeri di `BQ3` sono usabili senza essere fraintesi (Priority: P2)

La sezione «quanto vale» presenta i tre scenari come intervallo, con l'orizzonte di 12 mesi **a schermo e non per rimando** (rilievo `R7`), il tasso dichiarato lordo, l'uplift dichiarato livello mensile a regime, e una tabella di sensibilità in cui il moltiplicatore lo mette chi legge.

**Why this priority**: è la sezione che un decisore userà per prima e quella in cui un fraintendimento costa di più. Non è P1 perché la risposta della storia 1 regge anche senza di essa.

**Independent Test**: si verifica che nessuno scenario compaia isolato dagli altri due, che l'orizzonte sia scritto nella stessa sezione dei valori, e che ogni numero della tabella di sensibilità porti il marcatore di non-misurato o l'ancora.

**Acceptance Scenarios**:

1. **Given** i valori di `BQ3`, **When** compaiono, **Then** compaiono sempre come terna best/base/worst, mai come valore singolo.
2. **Given** la tabella di sensibilità, **When** la si legge, **Then** le basi di riferimento sono dichiarate e **marcate** come illustrazione parametrica, non come stima della base di StreamWave.
3. **Given** la formulazione sull'uplift, **When** la si confronta con `bq3_scenarios.md` §8, **Then** usa la formulazione stretta e non «non è scalabile».
4. **Given** il debito della `004` sulla verificabilità del benchmark, **When** i numeri di `BQ3` compaiono, **Then** è dichiarato aperto lì, non taciuto.

---

### User Story 5 — Le due assunzioni di trasferimento sopravvivono all'estrazione di una frase (Priority: P2)

`A1` (i cataloghi sono proxy, non StreamWave) e `A6` (il benchmark descrive un altro operatore) restano fuori dalla scala di confidenza per costruzione. La raccomandazione è l'artefatto più citabile fuori contesto che il progetto abbia prodotto: se una sola cosa deve sopravvivere all'estrazione di una frase, sono quelle due.

**Why this priority**: è il rischio strutturale di questo deliverable, e nessun controllo automatico lo presidia.

**Independent Test**: si estrae la frase di apertura da sola e si verifica che non affermi nulla su StreamWave che `A1` non regga.

**Acceptance Scenarios**:

1. **Given** la sezione di apertura, **When** se ne estrae la sola risposta, **Then** la frase non attribuisce a StreamWave alcuna misura diretta.
2. **Given** `A1` e `A6`, **When** si cercano nel documento, **Then** compaiono in una sezione propria e non solo in nota.

---

### User Story 6 — Il repository resta coerente e verificabile (Priority: P2)

Il controllo di coerenza copre l'ottavo documento, la grammatica registra la nuova riga di provenienza, il README non presenta drift.

**Why this priority**: è la condizione di merge di ogni feature di questo progetto.

**Independent Test**: `python3 scripts/check_audit_coherence.py` esce con stato 0 e dichiara otto documenti.

**Acceptance Scenarios**:

1. **Given** `docs/raccomandazione.md`, **When** si esegue il controllo, **Then** il documento è scandito in severità stretta e ogni numerale porta l'ancora o il marcatore.
2. **Given** il README, **When** lo si confronta con lo stato del repository, **Then** tabella di stato, elenco dei deliverable, prosa, `Setup` e `Struttura` sono allineati.

---

### Edge Cases

- **La rigenerazione dell'artefatto cambia un valore su cui il documento poggia.** Lo script è deterministico e i dati non cambiano in questa feature; se un valore cambiasse, sarebbe un ritrovamento da dichiarare con nota in loco, non da assorbire.
- **Il margine di `V3` risulta piccolo.** Su questi dati non accade, ma la prosa non deve dipendere dall'esito: se il margine fosse stretto, la frase da scrivere è che `C2` è fragile — la struttura del documento regge entrambi gli esiti, e questa è la proprietà che la rende una regola e non una giustificazione.
- **Una condizione risultasse non soddisfatta.** Il business case ha già scritto la lettura dei tre esiti; il documento applica quella che corrisponde al conteggio, senza riscriverne alcuna.
- **Il controllo segnala come quantità priva di marcatore una sigla nuova.** Le sigle `V1`-`V8` vivono nella spec, non nel documento pubblicato; nel documento pubblicato entra la sola `D12`, coperta dall'esclusione strutturale già esistente.
- **La revisione in contesto pulito solleva un rilievo che il deliverable rende falso.** Si chiude dentro la feature; tutto il resto va sul tracker con un numero.

---

## Requirements *(mandatory)*

### L'operatore di `C2` e la sua registrazione (V1)

- **FR-001**: La feature MUST fissare l'operatore di `C2` come confronto stretto di `mood_profile_overlap` con una soglia di maggioranza semplice pari a `0,50`, e MUST argomentare la scelta con le opzioni scartate, sullo schema delle decisioni `D1`-`D11`.
- **FR-002**: `docs/kpi_operators.md` MUST guadagnare una **nota in loco** in coda a §12 che dichiara l'operatore di `C2`, con data, feature, e riferimento alla issue `#17`. Il testo preesistente di §12 NON DEVE essere riscritto.
- **FR-003**: La tabella delle decisioni di `docs/kpi_operators.md` §10 MUST guadagnare la riga **`D12`**, con la stessa struttura delle undici righe esistenti (che cosa fissa, da dove viene, dove è applicata).
- **FR-004**: La nota di FR-002 MUST dichiarare che la scelta fra soglia stretta e larga non cambia l'esito di `C2` su questi dati, perché una decisione presentata come consequenziale quando non lo è attribuisce a sé stessa un peso che non ha.

### I valori nuovi nell'artefatto (V2, V3, V4)

- **FR-005**: `scripts/build_kpi_measures.py` MUST calcolare e pubblicare in `reports/kpi_measures.json` la soglia di `C2` come voce propria, l'esito booleano di `C2`, e il margine fra `mood_profile_overlap` e la soglia, ciascuno con etichetta e unità dichiarate secondo le convenzioni già in uso nello script.
- **FR-006**: Lo script MUST calcolare e pubblicare il **verdetto congiunto**: il numero di condizioni soddisfatte sulle tre, e l'esito booleano della congiunzione. Entrambi MUST avere identificativo proprio: sono affermazioni derivate, e per `D5` esistono come ancora o non si scrivono.
- **FR-007**: Nessun artefatto nuovo MUST essere creato: le voci entrano in `reports/kpi_measures.json`, dentro lo spazio dei nomi `KPI.` già verificato contro le collisioni.
- **FR-008**: Lo script MUST restare deterministico — nessuna lettura dell'orologio, nessun generatore casuale, aritmetica in `decimal.Decimal` — e due esecuzioni consecutive MUST produrre un file identico byte per byte.
- **FR-009**: Il verdetto pubblicato MUST dichiarare la propria dipendenza dalla versione della tabella dei mood (`MOOD.table.version`), perché `C2` poggia su `dim_category_mood` e [`content_taxonomy_bridge.md`](../../docs/content_taxonomy_bridge.md) §5 stabilisce che una revisione della tabella **invalida** il valore invece di correggerlo.
- **FR-010**: Nessun valore già pubblicato MUST essere ricalcolato o modificato da questa feature. Se una rigenerazione producesse un valore diverso da quello pubblicato, la divergenza MUST essere dichiarata come ritrovamento con nota in loco, mai assorbita.

### Il documento pubblicato (V6, V7, V8)

- **FR-011**: La feature MUST produrre `docs/raccomandazione.md`, ordinato in questa sequenza: la risposta; perché (le tre condizioni con esito e ancora); con che cosa entrare; quanto vale; che cosa lo farebbe cambiare; che cosa questa raccomandazione non è.
- **FR-012**: La sezione di apertura MUST contenere la risposta come **frase**, non come descrizione di ciò che i dati mostrano, e MUST portare la cautela già incorporata nel business case — l'esito non dice che l'espansione sarà redditizia, dice che sarebbe coerente.
- **FR-013**: La sezione «perché» MUST presentare le tre condizioni ciascuna con il proprio esito ancorato e la propria confidenza, e MUST dichiarare la confidenza del verdetto secondo `V5`, con l'argomento dell'ereditarietà dal termine più debole.
- **FR-014**: La sezione «con che cosa entrare» MUST raccomandare una **regione del catalogo caratterizzata da segmenti** e MUST dichiarare esplicitamente che i segmenti si sovrappongono, non si sommano e non si dimensionano contando le righe (`data_model.md` §18).
- **FR-015**: La stessa sezione MUST escludere i 7 segmenti marcati `is_high_zero_genre` da qualunque lettura della coda della graduatoria, dichiarando che portano domanda **non misurata dalla fonte** e non domanda bassa (`kpi_measures.md` §5.3 e §7.4).
- **FR-016**: Ogni ordinale o superlativo riferito a un fatto misurato — il primo in graduatoria, la numerosità del quadrante — MUST portare la propria ancora (corollario (a) di `D5`).
- **FR-017**: La sezione «quanto vale» MUST presentare `BQ3-K1` e `BQ3-K2` sempre come terna best/base/worst, MUST scrivere l'orizzonte di 12 mesi nella sezione stessa e non per rimando, MUST dichiarare il tasso **lordo** e l'uplift come **livello mensile a regime** e non cumulato.
- **FR-018**: La stessa sezione MUST portare una tabella di sensibilità dell'uplift su basi di riferimento dichiarate e **marcate** come illustrazione parametrica, con tutti e tre gli scenari per ciascuna base, e MUST usare la formulazione stretta di `bq3_scenarios.md` §8 invece di «non è scalabile».
- **FR-019**: La stessa sezione MUST dichiarare aperto il debito della `004` sulla verificabilità del benchmark — il valore centrale poggia su un comunicato che non nomina lo studio, e la verifica esterna dipende da un indirizzo che potrebbe smettere di rispondere (`bq3_scenarios.md` §9).
- **FR-020**: La sezione «che cosa lo farebbe cambiare» MUST nominare le condizioni che ribalterebbero la risposta, incluse: una revisione della tabella dei mood; una sovrastima della sovrapposizione maggiore del margine di `V3`; il fallimento dell'assunzione di trasferimento.
- **FR-021**: Il documento MUST portare una sezione propria su `A1` e `A6`, che restano fuori dalla scala di confidenza per costruzione (`business_case.md` §6), scritta in modo che sopravviva all'estrazione di una singola frase.
- **FR-022**: Ogni sigla del progetto usata nel documento MUST essere sciolta al primo uso; il documento NON DEVE presupporre la lettura di alcun altro file.

### Marcatura, controllo, coerenza del repository

- **FR-023**: `docs/raccomandazione.md` MUST entrare in `DOCUMENTS` di `scripts/check_audit_coherence.py` sotto **severità stretta**, come ottavo documento verificato e settimo sotto quel regime.
- **FR-024**: Ogni numerale in posizione di fatto misurato in `docs/raccomandazione.md` MUST portare l'ancora verso un artefatto versionato o il marcatore di non-misurato, secondo `docs/convenzioni-marcatura.md`; i numerali in lettere MUST essere evitati per qualunque fatto misurato (corollario (b) di `D5`).
- **FR-025**: `docs/convenzioni-marcatura.md` MUST guadagnare una riga nella tabella di severità di §5 e una nella tabella di provenienza, con data e feature.
- **FR-026**: `python3 scripts/check_audit_coherence.py` MUST uscire con stato 0 dopo ogni modifica di questa feature.

### Obblighi che nessun automatismo esegue

- **FR-027**: La feature MUST aggiornare `README.md`: riga nella tabella di stato con link al verbale, deliverable elencato, prosa dei deliverable estesa al documento nuovo, `Setup` e `Struttura` allineati, conteggio dei documenti verificati aggiornato. Il passaggio «Il file è leggibile, non pubblicabile» e il capoverso che lo segue restano veri e NON DEVONO essere toccati.
- **FR-028**: La feature MUST produrre `specs/009-verdetto-raccomandazione/review.md` secondo i quattro obblighi di `CLAUDE.md`: committato quando la revisione torna e **prima** di toccare l'artefatto; dichiara in apertura che cosa è stato letto e che cosa no, incluse le uscite dal perimetro; ancora commit e impronta del contenuto letto; non si corregge, e porta un blocco di chiusura che distingue **risolto**, **indebolito** e **rinviato** per ciascun rilievo, nominando l'issue per ogni rinvio.
- **FR-029**: Il perimetro della revisione MUST essere composto in modo da rendere visibile la **duplicazione di affermazioni**: la raccomandazione ripete affermazioni che vivono già in `business_case.md`, `kpi_measures.md` e `bq3_scenarios.md`, e una divergenza fra due copie sarebbe invisibile sia al revisore su estratti isolati sia al controllo automatico. È il ritrovamento della chiusura della `008b`.
- **FR-030**: Si chiudono dentro la feature **solo i rilievi strettamente necessari** — quelli senza cui il deliverable afferma il falso o pubblica un valore che non regge. Tutto il resto MUST essere registrato come issue sul tracker e dichiarato come rinvio nel blocco di chiusura.
- **FR-031**: La feature MUST chiudere la issue `#17` e la sostanza della `#28`, ciascuna con riferimento verificabile a dove la chiusura vive. Le issue `#11`, `#18`, `#20`, `#21`, `#26`, `#27`, `#29`, `#30` MUST restare aperte, in uno stato dichiarato nell'esito.
- **FR-032**: Nessun commit MUST essere eseguito di iniziativa. Messaggio e contenuto si propongono; decide Valerio. Vale per `add`, `push`, apertura di PR, merge e chiusura delle issue.
- **FR-033**: `docs/roadmap.md` NON DEVE essere modificato da questa feature: appartiene alla regia.
- **FR-034**: Nessuno script di questa feature MUST scrivere in `data/raw/` o `data/processed/` (principio II).

### Key Entities

- **`C2`**: la seconda condizione della regola di decisione della North Star; esito booleano derivato dal confronto fra `mood_profile_overlap` e la soglia di maggioranza.
- **Soglia di maggioranza**: stipulazione di chi analizza, `0,50`, con confronto stretto; è una convenzione dichiarata, non un'osservazione sui dati.
- **Margine di robustezza**: distanza fra `mood_profile_overlap` e la soglia; valore derivato che quantifica la sovrastima che `C2` tollera.
- **Verdetto congiunto**: numero di condizioni soddisfatte ed esito della congiunzione; affermazione derivata a confidenza media.
- **Base di riferimento**: valore di abbonati stipulato da chi legge per illustrare l'aritmetica dell'uplift; non è una stima della base di StreamWave e porta il marcatore di non-misurato.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `docs/raccomandazione.md` esiste e contiene, nell'ordine, le sei sezioni di FR-011.
- **SC-002**: Le tre condizioni della regola di decisione esistono come voci booleane ancorate nello stesso artefatto, e il verdetto congiunto ha un identificativo proprio.
- **SC-003**: `python3 scripts/build_kpi_measures.py` eseguito due volte produce un artefatto identico byte per byte.
- **SC-004**: `python3 scripts/check_audit_coherence.py` esce con stato 0 verificando otto documenti, di cui sette in severità stretta.
- **SC-005**: Nessun numerale in posizione di fatto misurato in `docs/raccomandazione.md` è privo di ancora o di marcatore.
- **SC-006**: Il margine di robustezza è pubblicato come valore ancorato, e la frase che lo accompagna afferma una condizione sull'errore e non una stima dell'errore.
- **SC-007**: L'operatore di `C2` è registrato in `docs/kpi_operators.md` come `D12`, con nota in loco che non riscrive il testo preesistente.
- **SC-008**: `specs/009-verdetto-raccomandazione/review.md` esiste, è committato prima di qualunque correzione al deliverable, e il suo blocco di chiusura distingue risolto/indebolito/rinviato per ogni rilievo, nominando l'issue per ogni rinvio.
- **SC-009**: `README.md` non presenta alcun disallineamento con lo stato del repository.
- **SC-010**: La issue `#17` e la sostanza della `#28` sono chiuse con riferimento verificabile; le altre otto issue citate nel perimetro restano aperte e dichiarate.

---

## Stima e scomposizione

**~6 ore**, revisione e chiusura dei rilievi incluse. Distribuzione attesa: ~1 h per l'operatore di `C2`, le ancore e lo script; ~3 h per `docs/raccomandazione.md`; ~2 h per revisione e chiusura.

La feature sta sotto il limite del principio III e non va scomposta. **Se dopo il secondo punto di fermata il lavoro sembrasse più grande, la sessione si ferma e lo riporta invece di comprimere**: la parte comprimibile sarebbe la sezione «che cosa lo farebbe cambiare», che è la sola che distingue questo documento da un riassunto dei precedenti.

---

## Assumptions

- I valori pubblicati da `reports/kpi_measures.json` e `reports/bq3_scenarios.json` sono corretti e non vengono riaperti: questa feature li legge, non li verifica di nuovo.
- La tabella dei mood resta alla versione su cui `BQ1-K3` è stato calcolato; una sua revisione invaliderebbe `C2` e con essa il verdetto, ed è il contratto di versione dichiarato in FR-009.
- Il destinatario della raccomandazione dispone di una stima della base abbonati che questo progetto non ha: è l'ipotesi che rende utile la tabella di sensibilità di `V8`, e non introduce alcun numero nel repository.
- Nessuna sessione di questa feature ha accesso al `.pbix`, che resta sul disco di Valerio e non viene toccato.

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ1**, in via principale — la regola di decisione della North Star è definita su `BQ1-K1` e `BQ1-K3`, e `C2` è una misura di posizionamento. La feature serve però **tutte e tre**: `C3` viene da `BQ2` e la sezione «con che cosa entrare» risponde alla domanda del segmento di ingresso; la sezione «quanto vale» porta i valori di `BQ3`.
- **Contributo**: chiude il ciclo. Le feature precedenti hanno prodotto le misure con cui le tre domande si rispondono; questa **applica la regola che le compone** e pubblica la risposta al livello della decisione, che è il livello a cui le tre domande erano state poste.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

| Metrica | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| soglia di maggioranza di `C2` | stipulazione dichiarata | — | non è una misura: è una convenzione di chi analizza, come le soglie mediane di `C1` e `C3` | valore singolo, dichiarato come soglia |
| `C2` — esito booleano | Derivato (`BQ1-K3` + soglia) | **media** | eredita da `BQ1-K3`, che dipende da `dim_category_mood`, costruita dall'analista e non osservata | esito booleano ancorato |
| margine di robustezza di `C2` | Derivato (`BQ1-K3` + soglia) | **media** | stessa catena di `C2`; è aritmetica esatta su due valori già pubblicati | valore singolo ancorato |
| numero di condizioni soddisfatte | Derivato (`C1` + `C2` + `C3`) | **media** | eredita il livello più basso fra le tre, che è quello di `C2` e `C3` — vedi `V5` | conteggio ancorato |
| verdetto congiunto | Derivato (`C1` + `C2` + `C3`) | **media** | congiunzione logica: la fiducia non può eccedere quella del termine più debole | esito booleano ancorato |
| valori citati di `BQ1-K1`, `BQ1-K3`, `BQ2-K3` | già pubblicati dalla `007b` | invariata | citati, non ricalcolati | come pubblicati |
| valori citati di `BQ3-K1`, `BQ3-K2` | Benchmark (esterno) + Sintetico | **bassa** | invariata dalla `004`; l'ancoraggio a una fonte citabile non innalza la confidenza | **esclusivamente** range best/base/worst |
| basi di riferimento della tabella di sensibilità | stipulazione di chi legge | — | non sono misure e non sono stime della base di StreamWave: sono ipotesi dichiarate, marcate come non-misurate | illustrazione parametrica, con i tre scenari per ciascuna base |

**Assunzioni dietro i dati sintetici**: nessun dato sintetico è generato da questa feature. I valori di `BQ3` sono citati dall'artefatto della `004`, che li deriva da un benchmark esterno congelato sotto l'assunzione di trasferimento `A6`.

**Le due assunzioni che restano fuori dalla scala**: `A1` (i cataloghi sono proxy di StreamWave) e `A6` (il benchmark descrive un altro operatore) qualificano la **validità esterna**, che questa scala non misura (`business_case.md` §6). Nessun livello di confidenza di questa tabella, nemmeno il più alto, autorizza a trattare un numero come una misura diretta di StreamWave.

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: se l'espansione sarà **redditizia**. La regola di decisione misura la **coerenza strategica**: dice che l'espansione sarebbe un'estensione del catalogo esistente, non che produrrà un ritorno. Manca il lato costi — licenze, infrastruttura, organico — e senza di esso questo resta un business case di opportunità (`business_case.md` §8).
- **Non risponde a**: quanto sia grande il mercato di un segmento musicale, né quale sia la dimensione della base abbonati di StreamWave. La tabella di sensibilità è parametrica per questa ragione, non per prudenza retorica.
- **Non risponde a**: se il pubblico attuale vorrebbe la musica. La sovrapposizione che `C2` misura è fra **caratteristiche di contenuto**, non fra persone osservate; nessuna misura di questo progetto autorizza a parlarne in termini di trasferibilità di pubblico.
- **Inferenza da evitare**: che il margine di robustezza sia una **stima dell'errore** della sovrapposizione. È una condizione sull'errore — quanto dovrebbe essere grande perché la conclusione cambi — e nessuno in questo progetto ha misurato quanto l'errore effettivamente sia.
- **Inferenza da evitare**: che i segmenti del quadrante siano alternative disgiunte fra cui scegliere, o che le loro quantità si sommino. Si sovrappongono per costruzione (`data_model.md` §18).
- **Inferenza da evitare**: che l'uplift si possa moltiplicare per un orizzonte e ottenere un cumulato. È un livello mensile a regime, e il cumulato varrebbe solo sotto l'assunzione di base costante.
- **Inferenza da evitare**: che un verdetto ancorato sia un verdetto verificato contro il mondo. È l'applicazione di una regola dichiarata a valori misurati su cataloghi proxy: l'ancora garantisce l'origine del numero, non la sua verità.
- **Copertura del dato**: catalogo video fermo al 2021, catalogo musicale al 2022. Nessuna conclusione riguarda dinamiche di mercato successive. Il benchmark che alimenta `BQ3` è del 2018 e descrive un altro operatore su un altro mercato.
- **Dipendenza di versione**: `C2` e con esso il verdetto poggiano su `dim_category_mood` alla versione dichiarata. Una revisione della tabella **invalida** il valore invece di correggerlo (`content_taxonomy_bridge.md` §5), e il verdetto lo dichiara dove viene pubblicato.
- **Dove è esposto all'utente finale**: in `docs/raccomandazione.md`, nella sezione «che cosa questa raccomandazione non è» e, per i limiti che condizionano un numero specifico, accanto a quel numero. La resa a schermo di questi limiti nel report nuovo appartiene alla `010b`; questa feature ne fissa il contenuto in forma leggibile da un decisore, non la loro impaginazione.
