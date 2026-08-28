# Verbale di revisione in contesto pulito — `T035`

**Oggetto**: il contratto di narrazione della `008b` (documento A) e la sezione «Esito della costruzione» (documento B).
**Metro dichiarato dalla consegna**: la leggibilità per il destinatario descritto in apertura del documento A — *un decisore che non ha letto alcun documento di questo repository*.

---

## 1. Che cosa è stato letto e che cosa no

**Letto, e nient'altro:**

- `documento-A-contratto-di-narrazione.md`, per intero, dalla prima riga all'ultima. Il file eccede la finestra di una singola lettura ed è stato letto in due passaggi contigui (righe 1-825 e 826-1037): nessuna porzione è stata saltata.
- `documento-B-esito-della-costruzione.md`, per intero.

**Non letto, e non cercato:**

- la spec della `008b`, il piano, `tasks.md`, `data-model.md`, `quickstart.md`;
- le feature precedenti, la `008a` inclusa, e qualunque documento sotto `docs/` — `business_case.md`, `data_model.md`, `kpi_measures.md`, `kpi_operators.md`, `bq3_scenarios.md`, `content_taxonomy_bridge.md`, `convenzioni-marcatura.md`, `roadmap.md`;
- la constitution e `CLAUDE.md`;
- il tracker e le issue `#11`, `#17`, `#18`, `#20`, `#21`, `#26`, `#27`;
- la history git, il commit `4c4d6e6` e qualunque diff;
- il file `.pbix`, e qualunque immagine o cattura di schermo che lo mostri;
- `scripts/check_audit_coherence.py`.

Nessuna ricerca nel filesystem, nessun `grep`, nessuna navigazione fuori dalla cartella di revisione, nessuna ricerca sul web.

**Gli impulsi di uscita dal perimetro che ho avuto e non ho seguito**, ciascuno con il punto su cui l'ho avuto. Sono elencati perché è la sola parte di questo verbale che rende verificabile, invece che asserito, il contesto pulito:

1. **`data_model.md` §18** — tre volte. La prima leggendo `BL-Q1-5`, per sapere se *«una lettura sbagliata di quel numero»* sia citato con lo stesso perimetro che il blocco gli dà; la seconda su `BL-Q2-7`, per capire quanto pesi la metà di `OB-20` che è caduta; la terza sul commento a `BL-Q2-10`, dove il documento A afferma che il modello *«qualcosa sui pubblici lo dice — ciò che manca è il livello»*, affermazione che il blocco a schermo non contiene e che non ho modo di collocare.
2. **`kpi_measures.md` §7.4** — leggendo la nota di indebolimento di `OB-15`, per giudicare se *«vanno esclusi da qualunque lettura della coda»* sia una prescrizione operativa o una raccomandazione. Il rilievo `R9` è formulato senza quella risposta, e ne dichiara la dipendenza.
3. **`quickstart.md`** — due volte: per sciogliere i simboli `★1` e `★3`, che il documento B usa senza definirli, e per contare quali delle dodici prove siano manuali, verifica che serve al rilievo `R18`. Il conteggio è stato fatto sulla sola tabella del documento B.
4. **Il contratto di pagina della `008a` §8 e `CP-1`** — leggendo *«la quota di film accanto al valore»* di `BL-Q1-5`, per sapere se quella quota sia davvero a schermo e davvero accanto. Il rilievo `R15` nasce esattamente dall'impossibilità di rispondere restando dentro il perimetro.
5. **Il `.pbix`, o una sua immagine** — l'impulso più forte, e ripetuto. Su `SC-1`, perché il documento B descrive la versione accorciata di `BL-IN-3` senza trascriverla, e quel blocco è l'unico testo a schermo di cui non conosco la lettera; e su `BQ2`, per sapere come i dieci blocchi siano disposti, dato che tre di essi portano lo stesso titolo.
6. **Il tracker** — su `#17` (l'esistenza e il numero delle condizioni della regola di decisione, che è il cuore del rilievo `R2`) e su `#27`.
7. **Un'altra copia del documento A** — quando ho visto che la numerazione delle sezioni salta dalla `§14` alla `§16`, ho pensato che il file mi fosse arrivato mutilo. Non ho cercato altrove: il salto è registrato come rilievo `R23` e, se è una svista di trasmissione, il rilievo cade da sé.

Nessuno di questi impulsi è stato seguito. Dove la risposta mancante cambia la portata di un rilievo, il rilievo lo dice.

---

## 2. Ancoraggio della versione revisionata

- **Commit del repository al momento della revisione**: `4c4d6e6`
- **Impronta SHA-256 del documento A**: `085f25f3d13e7938ec21a11dbc44ed684f48711f4729fe6833bf4428102eccc0`
- **Impronta SHA-256 del documento B (estratto)**: `c8f21ec57cce70cee72c4ec8b306633e2917688122c8d479fdd2cdf8d5c4f7c8`
- Il documento B è la sezione «Esito della costruzione» di un file più ampio, estratta a partire dalla sua intestazione fino alla fine del file. Non ho visto ciò che nel file precede quell'intestazione, e nessun rilievo presuppone di conoscerlo.

---

## 3. I rilievi

**Criterio di gravità, dichiarato una volta sola.**

- **alta** — leggendo lo schermo (o, per i rilievi sul documento B, leggendo il documento B), il destinatario **conclude qualcosa di falso**, oppure **non conclude nulla dove il testo crede di fargli concludere qualcosa**, oppure il documento B **dichiara verificato ciò che la sua stessa evidenza smentisce**;
- **media** — il lettore inciampa, deve rileggere, perde una parte del significato o si trova davanti a due frasi che sembrano darsi torto, ma non conclude il falso;
- **bassa** — difetto di finitura, di navigazione interna o di coerenza fra i documenti, visibile soprattutto a chi li manterrà.

La gravità è assegnata **sull'effetto sul lettore**, non sull'onere della correzione: alcuni rilievi `alta` si chiudono con una riga, alcuni `media` no.

---

### `R1` — In quattro pagine nessun testo dice a che cosa la dashboard serva — gravità **alta**

**Documento A**, pagina di ingresso, tutti e quattro i blocchi; e `BL-IN-2`, testo:

> `Non dice se convenga entrare nel mercato musicale.`

La pagina di ingresso è composta di quattro blocchi: uno dice che i numeri non riguardano StreamWave, uno dice a che cosa la dashboard non risponde, uno spiega come si legge un'etichetta, uno dice fin dove arrivano i dati. **Nessuno dice che cosa la dashboard risponda.** Il lettore descritto in apertura — quello che *«legge quattro pagine e se ne va»* — attraversa la prima pagina intera senza incontrare una sola affermazione al positivo.

L'effetto peggiora perché le pagine successive si chiamano `Segmento di ingresso` e `Impatto stimato`: il decisore legge *«non dice se convenga entrare»*, poi trova una pagina che gradua i segmenti di ingresso e una che stima l'impatto. Delle due l'una — o conclude che le pagine dicono ciò che l'ingresso nega, e allora ha imparato a non fidarsi del testo; o conclude che l'intero file è una lunga smentita di sé, e allora non ha ragione di leggere oltre.

**Che questa assenza non è imposta da alcun vincolo del contratto.** La Parte I §2 ammette tre registri, e il primo è *«che cosa il valore misura»*. Una frase come «questa dashboard misura quanto il catalogo di riferimento sia già musicale, quali segmenti musicali gli somigliano di più, e che cosa costerebbe per utente» sta interamente dentro il primo registro: non è raccomandazione, non è verdetto, non è previsione. L'assenza è una scelta di chi ha scritto, non una conseguenza di `N7`, e va dichiarata come scelta o riparata.

**Il conto complessivo.** Su `BQ2`, dei dieci blocchi, uno solo contiene un permesso — `BL-Q2-4`, *«Permette di confrontare i segmenti fra loro»* — e gli altri nove dicono che cosa non si può fare, che cosa il numero non misura, che cosa la posizione non significa, che le visuali non si filtrano e che la parola «domanda» non nomina la domanda. Trentadue blocchi di cautela per un lettore che legge quattro pagine e se ne va: il rapporto fra ciò che è permesso e ciò che è negato è tale che l'unica lettura razionale del destinatario è **non usare nessuno di questi numeri**. Se è questo il messaggio, va scritto una volta in chiaro invece di essere il residuo di trentuno negazioni; se non lo è, manca il suo contrario.

---

### `R2` — I nomi `C1` e `C3` compongono da soli la regola che il contratto vieta di comporre — gravità **alta**

**Documento A**, Parte I §3, e i blocchi `BL-Q1-3` e `BL-Q2-8`.

Il contratto vieta di contare le condizioni, di nominare `C2` e di pubblicare un esito complessivo, e argomenta così la sufficienza del rimedio adottato:

> `dire che una condizione da sola non decide non richiede di sapere quante siano.`

È vero della frase, e falso dello schermo. Il lettore incontra su `BQ1` un'entità chiamata **`C1`** e su `BQ2` una chiamata **`C3`**. Da queste due etichette ricava, senza alcuno sforzo e con certezza pratica, tre cose che il contratto ha deciso di non dirgli: che le condizioni sono almeno tre, che sono ordinate, e che ne esiste una di mezzo che la dashboard non gli mostra. Il divieto di nominare `C2` non impedisce a `C2` di comparire: la fa comparire **come buco**, che è la forma in cui un lettore la nota di più.

Il documento B registra a sua volta l'issue `#17` con la motivazione che questa feature *«dichiara soltanto... che l'esito congiunto non è a schermo — vero indipendentemente da quante condizioni esistano»*. È la stessa difesa, e ha lo stesso difetto: il lettore non ha bisogno che il documento gli dica quante siano, gliel'hanno detto i nomi.

**Un secondo difetto nello stesso apparato.** Sull'area della metrica di riferimento i blocchi si susseguono `BL-Q1-1`, `BL-Q1-1b`, `BL-Q1-2`, `BL-Q1-3`. Il titolo di `BL-Q1-2` è:

> `Questa quota non dice se C1 sia soddisfatta`

e `C1` viene sciolto **due blocchi dopo**, in `BL-Q1-3`. Il titolo è, per stipulazione del contratto stesso (Parte II), *«la riga che il lettore incontra per prima e serve a fargli decidere se leggere il resto»*: qui la prima riga che il lettore incontra contiene una sigla che non significa nulla per lui, e la decisione che quel titolo gli chiede di prendere è quindi presa nel buio. `OB-34` è servito alla lettera — la sigla è sciolta sulla stessa pagina — e la prova 11 è verde; l'ordine di lettura non è servito affatto. È esattamente il caso che il documento A dichiara di temere in apertura: *«un blocco esatto e incomprensibile è un difetto»*.

---

### `R3` — Sulla stessa pagina, `BL-Q3-4` dice che il valore è verificabile e `BL-Q3-9` dice che non lo è — gravità **alta**

**Documento A**, `BL-Q3-4`, testo:

> `La fonte è citabile, e il valore verificabile: ciò non innalza la confidenza.`

**Documento A**, `BL-Q3-9`, testo, stessa pagina `BQ3`:

> `Il valore centrale poggia su un comunicato pubblicato da un terzo, che non nomina lo studio da cui la cifra proviene: se ne constata che un comunicato la riporta, non che sia stata misurata in un modo che si possa giudicare.`

Il lettore trova, a pochi centimetri di distanza, l'affermazione che il valore **è verificabile** e la spiegazione che di quel valore **non si può verificare nulla oltre il fatto che un comunicato lo riporti**. Le due frasi si contraddicono nella lettura piana, e l'unica riconciliazione possibile — che «verificabile» in `BL-Q3-4` significhi «si può controllare che il comunicato dica quella cifra» e non «si può controllare che la cifra sia giusta» — richiede al lettore di attribuire alla parola *verificabile* un senso tecnico ristretto che nessun blocco gli fornisce.

Questa è la contraddizione più netta dell'intero deliverable, e **nessuno dei due documenti la elenca**. Il documento A registra su `BL-Q3-4` un indebolimento diverso (che *verificabile* e *vero per StreamWave* siano proprietà distinte); il documento B, che si dichiara la fonte autorevole *«dove i due divergono»*, elenca tre scostamenti e nessuno riguarda questo. Non è una divergenza fra contratto e schermo: è una contraddizione **dentro** il contratto, che lo schermo ha fedelmente riprodotto.

Va aggiunto che `BL-Q3-4` è, delle due, la frase più fragile anche da sola: *«La fonte è citabile, e il valore verificabile: ciò non innalza la confidenza»* concede due qualità e poi le dichiara irrilevanti, senza dire perché. Il lettore che si ferma lì non ricava un'informazione, ricava un'oscillazione.

---

### `R4` — Il titolo «Un debito aperto» su una pagina intitolata «Impatto stimato» sarà letto come un debito finanziario — gravità **alta**

**Documento A**, `BL-Q3-9`, titolo:

> `Un debito aperto`

Il blocco è dichiarato non tagliabile in nessun caso, ed è quello che, secondo il documento B, *«rende il file pubblicabile invece di impedirlo»*. Il documento A dichiara inoltre, nella nota di indebolimento, che *«Che il debito sia aperto è ora affidato al solo titolo, ed è sufficiente»*: l'intero peso di `OB-32` sta quindi su due parole.

Quelle due parole, su una pagina che si chiama **Impatto stimato**, sotto una tabella di scenari di ricavo, davanti a un decisore che di mestiere legge conti, non significano «un debito metodologico del progetto». Significano **una passività**. Il lettore cerca un importo, non lo trova, e o conclude che manca un numero o conclude che la stima ha un onere non quantificato a fronte. In entrambi i casi ha capito il contrario di ciò che il blocco dice, e il testo sotto — che parla di un comunicato e di uno studio non nominato — gli sembrerà rispondere a un'altra domanda.

«Debito» è gergo di questo repository. Il documento A vieta a sé stesso il gergo non sciolto nella terza riga della propria sezione di apertura, e qui lo usa nel punto in cui ha meno margine: un titolo che porta da solo un obbligo.

---

### `R5` — `BL-IN-3`: il solo taglio in costruzione poggia su una premessa che il documento B smentisce, e il blocco è a schermo **troncato** mentre il file è dichiarato pubblicabile — gravità **alta**

Due difetti sullo stesso blocco, tenuti insieme perché la loro somma è ciò che conta.

**(a) La ragione del taglio contraddice la tabella che la precede di venti righe.**
Documento B, `SC-1`:

> `**La ragione, dichiarata come è**: **non è una fascia insufficiente.** Le altre pagine entravano senza scorrimento, e il taglio è stato scelto per allineare l'altezza di questa fascia alle altre.`

Documento B, tabella «Che cosa è a schermo, pagina per pagina», righe `BQ1`, `BQ2`, `BQ3`, tutte e tre:

> `**no**, il testo scorre (`SC-3`)`

e `SC-3` in intestazione: `**Pagine**: tutte e quattro`.

Le altre pagine **non** entravano senza scorrimento: scorrono tutte. La sola giustificazione data all'unico taglio di contenuto avvenuto in costruzione — l'uniformità estetica con pagine che stavano dentro — descrive uno stato che il documento stesso dichiara inesistente. O `SC-1` è stato scritto prima che si scoprisse che le altre pagine scorrevano e non è stato rivisto (e allora la disciplina del «si scrive mentre accade» ha prodotto qui il suo effetto opposto, un testo vero al momento e falso adesso), o la ragione registrata non è quella vera. In nessuna delle due letture il taglio resta motivato, e il taglio è quello che ha portato via l'enunciato generale di `OB-03`.

La stessa contraddizione è ripetuta nella tabella, che attribuisce il taglio alla capienza — *«**no**, e la reazione è stata doppia: `BL-IN-3` è stato accorciato (`SC-1`)»* — cioè esattamente alla ragione che `SC-1` nega con enfasi. La tabella e lo scostamento dicono due cose diverse sullo stesso fatto.

**(b) A schermo c'è una frase che non afferma nulla, e il file è dichiarato pubblicabile.**
Documento B, `SC-1`:

> ```text
> Bassa: il numero dipende da ipotesi che i dati disponibili .
> ```
>
> `La frase si interrompe a metà e non afferma nulla. **Va riparata a schermo prima di chiudere `T013`**`

Il documento B dichiara, al presente e senza condizioni, che **il `.pbix` è pubblicabile dal 2026-08-28**, e nella stessa sezione dichiara che una delle tre righe della legenda di confidenza — su cui poggia la lettura di **tutti e otto** i numeri del file — è tronca. La riparazione è al futuro (*«va riparata»*), nessuna riga del documento dice che sia avvenuta, e la tabella «Che cosa è a schermo» non la menziona. Chi legge il documento B senza arrivare al corpo di `SC-1` conclude che il file è a posto; chi apre il file trova, sulla prima pagina, una definizione che si interrompe su una preposizione.

**Un terzo effetto, che è il più insidioso.** La tabella delle prove, riga 5:

> `**passata con uno scostamento già dichiarato**: `BL-IN-3` non coincide alla lettera, ed è `SC-1`. Nessun'altra differenza`

*«Nessun'altra differenza»* è falso per ammissione dello stesso documento, che qualifica il troncamento come *«un difetto di trascrizione dentro lo scostamento, che non è parte dello scostamento»*. La distinzione fra «scostamento» e «difetto di trascrizione dentro lo scostamento» è una categoria che esiste solo dentro questo documento: sullo schermo c'è una frase che non coincide con il contratto e non coincide nemmeno con la versione accorciata che si era deciso di mettere. Chiamarla in un altro modo non la toglie dalla riga «nessun'altra differenza», e chi legge quella riga della tabella — che è il modo in cui una tabella di prove viene letta — non la incontra.

---

### `R6` — La scatola «Il `.pbix` è pubblicabile» afferma ciò che il quinto trattino sotto di essa nega — gravità **alta**

**Documento B**, riquadro:

> `un file che espone otto numeri con la propria fonte, la propria confidenza, la ragione di quella confidenza e i limiti che ne governano la lettura può essere mostrato a chi non ha letto nulla di questo repository **senza che ne tragga una conclusione che i dati non sostengono**.`

**Documento B**, quinto trattino di «Che cosa «pubblicabile» non significa», undici righe più sotto:

> `chi non scorre non legge la seconda metà di un blocco — che è dove sta la parte prescrittiva.`

Le due frasi non possono essere vere insieme. Se la parte prescrittiva — cioè quella che dice al lettore che cosa non concludere — è raggiungibile solo scorrendo, e se chi non scorre non la legge, allora esiste un lettore che vede i numeri, non vede i limiti, e trae precisamente la conclusione che i dati non sostengono. La motivazione della pubblicabilità è formulata come proprietà del file (*«può essere mostrato... senza che»*), non come esito di una procedura, e come proprietà del file è smentita nella stessa pagina.

Va riconosciuto che il documento **non nasconde** la seconda frase, e che il criterio `N8` è stato fissato prima e non è stato allargato — è la parte onesta di questa sezione, ed è registrata al §4. Il difetto non è la reticenza: è che la **ragione in una riga**, che è la sola parte del riquadro che un lettore esterno porterà via, dice più di quanto il resto del documento consenta. Basterebbe che la ragione fosse formulata come ciò che è — *un file che porta a schermo, per ogni numero, la fonte, la confidenza, la ragione di quella confidenza e i limiti* — senza la promessa sul lettore, che è la parte non sostenuta.

Si aggiunge, sullo stesso punto, che il documento A dichiara `§13.1` che *«in otto casi su nove ciò che cade è la seconda metà del blocco — quella che dice al lettore che cosa non fare con il numero»*. Sommando i due fatti: la parte prescrittiva è stata accorciata in revisione **e** quel che ne resta è dietro uno scorrimento. Nessuno dei due documenti mette insieme queste due frasi, e messe insieme cambiano il colore della dichiarazione.

---

### `R7` — I numeri di `BQ3` non sono usabili perché l'orizzonte non è a schermo — gravità **alta**

**Documento A**, `BL-Q3-3`, testo:

> `L'orizzonte è quello dichiarato nel business case, oltre il quale la fiducia nelle ipotesi degrada al punto da rendere la stima non informativa.`

**Documento A**, `BL-Q3-6`, testo:

> `È un livello mensile, raggiunto a fine orizzonte e poi mantenuto.`

Il valore centrale della pagina è un uplift **per utente al mese raggiunto a fine orizzonte**. Un decisore che non sa se l'orizzonte sia di dodici mesi o di dieci anni non ha ricevuto un numero: ha ricevuto una grandezza priva della dimensione che la rende confrontabile con qualunque cosa. Ed è precisamente il tipo di lettore per cui questo testo è scritto, quello che non può aprire il business case.

Due aggravanti.

La prima: la frase che nomina l'orizzonte lo **definisce circolarmente** — l'orizzonte è quello oltre il quale la fiducia degrada al punto da rendere la stima non informativa. Il lettore impara che esiste una soglia, che oltre la soglia i numeri non valgono, e non impara dov'è la soglia. Non può quindi nemmeno sapere se la decisione che sta valutando cada dentro o fuori.

La seconda: è la conseguenza diretta della lista chiusa dei numerali (Parte I §1), che ammette a schermo `2021` e `2022` e nient'altro, e che dichiara che aggiungere una voce *«è una modifica di questo contratto, da riapprovare»*. Una regola nata per impedire che comparissero cifre senza fonte ha tolto dallo schermo l'unica cifra senza la quale il KPI più importante della quarta pagina non si legge. Il documento A dichiara in apertura, fra le tre conseguenze sulla forma, *«niente rimandi a documenti che il lettore non ha»*: `BL-Q3-3` è quel rimando, e non è il solo — `BL-Q1-3` e `BL-Q2-8` rimandano entrambi a *«il business case»* per sapere che cosa siano `C1` e `C3`.

---

### `R8` — `BL-Q3-8` consegna al lettore la ricetta dell'operazione che il progetto non può sostenere — gravità **alta**

**Documento A**, `BL-Q3-8`, testo:

> `Chiunque disponga di una stima di abbonati può moltiplicare, ma il totale sarebbe un numero che nessuno ha misurato.`

L'argomento del contratto (§4, riga 3) è che dire *«non è scalabile»* sarebbe falso e che questa è l'unica cosa vera dicibile. L'argomento regge sulla verità; non regge sull'effetto. Il destinatario di questa dashboard **è** una persona che dispone di una stima di abbonati di StreamWave: è la ragione per cui è nella stanza. Il blocco gli dice, in una riga, che l'operazione si fa in pochi secondi e che nessuno gliela vieta. La qualificazione che segue — *«un numero che nessuno ha misurato»* — è la seconda metà della frase, cioè la parte che l'intero documento A dichiara essere quella che i lettori perdono.

Il difetto diventa serio quando lo si somma a `BL-Q3-4`, dove `OB-27` è dichiarato indebolito e **cade proprio la dichiarazione che assumere il valore del benchmark per StreamWave sia un'ipotesi di trasferimento**. Sommando ciò che resta a schermo: il valore centrale viene da un operatore terzo (`BL-Q3-4`), l'ipotesi di trasferimento non è più nominata, e `BL-Q3-8` spiega come passare all'aggregato. Il percorso che porta il lettore a moltiplicare un tasso osservato su un'altra azienda per la base di abbonati di StreamWave è, a schermo, **completo e senza ostacoli**, e i due presidi che lo interrompevano sono uno caduto e uno relegato in coda di frase.

Nessuno dei due documenti nota questa composizione: `BL-Q3-4` e `BL-Q3-8` sono trattati come blocchi indipendenti, e ciascuno separatamente è difendibile.

---

### `R9` — `BL-Q2-2`, il blocco dichiarato non tagliabile, spiega con oggetti che il lettore non vede — gravità **alta**

**Documento A**, `BL-Q2-2`, testo:

> `Per questi segmenti l'indice di domanda non è basso: è non misurato dalla fonte. Più della metà delle loro righe porta popolarità nulla, la mediana cade dentro quella metà, e il valore che ne esce misura la copertura del dato invece della domanda.`

È il blocco che il contratto dichiara **non tagliabile in nessun caso** e *«l'unico punto della pagina in cui una lettura sbagliata è anche la più naturale»*. La sua frase centrale è costruita su tre oggetti che il destinatario non ha:

- **«le loro righe»** — righe di che cosa? Il lettore vede una graduatoria di segmenti, non una tabella di tracce. La parola presuppone la conoscenza che sotto ogni segmento ci sia un insieme di record, che è una nozione di modello dati;
- **«la mediana cade dentro quella metà»** — è la spiegazione statistica corretta del perché il valore risulti nullo, ed è illeggibile per chi non sappia già che l'indicatore è una mediana. Nessun blocco della pagina lo dice;
- **«la copertura del dato»** — gergo, e per giunta ambiguo: il lettore può capire «quanto dato abbiamo» oppure «quanta parte del mercato il dato copre», che sono cose diverse e portano a decisioni diverse.

L'apertura, poi, è tipograficamente e sintatticamente fragile: *«non è basso: è non misurato dalla fonte»*. La distinzione fra *non è basso* e *è non misurato* è tutta nella posizione della negazione. Letta a voce, e letta di fretta su uno schermo, si appiattisce su «è basso, non misurato» — cioè esattamente la formulazione esclusa che il blocco esiste per impedire.

Il paradosso è che l'**ultima** frase del blocco — *«La loro posizione in fondo alla graduatoria misura quindi l'assenza di segnale, non una priorità bassa»* — è chiara, concreta e sufficiente da sola. È la frase che il lettore raggiunge per ultima, ed è, per `SC-3`, quella che potrebbe non raggiungere affatto.

Va detto che non ho potuto leggere `kpi_measures.md` §7.4 e non so quindi quanto pesi la prescrizione caduta con `OB-15` (che i segmenti marcati *«vadano esclusi da qualunque lettura della coda»*). Il rilievo qui non riguarda quella metà: riguarda la metà che è rimasta e che, per come è scritta, non arriva.

---

### `R10` — Tre blocchi con lo stesso titolo nella stessa fascia, e la fascia scorre — gravità **media**

**Documento A**, `BL-Q2-1`, `BL-Q2-3`, `BL-Q2-5`, titolo identico:

> `Perché la confidenza è media`

e su `BQ1`, `BL-Q1-1` e `BL-Q1-4`, titolo identico:

> `Perché la confidenza è alta`

Il contratto stabilisce (Parte II) che il titolo *«è la riga che il lettore incontra per prima e serve a fargli decidere se leggere il resto»*. Tre titoli identici nella stessa fascia non fanno decidere nulla: il lettore che scorre vede la stessa riga tre volte e conclude, ragionevolmente, di essere tornato indietro o di leggere una ripetizione. Su `BQ1` il danno è contenuto, perché il contratto assegna a ciascuno un'area allineata alla propria scheda; su `BQ2` **lo spazio dichiarato è una fascia sola** («la fascia sotto la graduatoria»), i blocchi sono dieci, il testo scorre, e nessuno dei due documenti dice se e come i tre blocchi omonimi siano distinguibili.

Il soggetto è recuperabile dalla prima parola del testo (*«L'indice di domanda…»*, *«L'affinità…»*, *«Il punteggio di priorità…»*), e questo salva il rilievo dalla gravità alta. Ma è recuperabile solo da chi legge il testo, cioè da chi il titolo avrebbe dovuto convincere a leggerlo.

---

### `R11` — La parola «domanda», dichiarata il rischio numero uno, torna due pagine dopo in un secondo significato — gravità **media**

**Documento A**, Parte I §2: *«Il caso da cercare per primo è la parola «domanda»»*, e `BL-Q2-10` esiste per disinnescarla su `BQ2`:

> `Nomina un indice di popolarità pubblicato dalla fonte musicale, non un comportamento osservato.`

**Documento A**, `BL-Q3-2`, pagina `BQ3`, testo:

> `nessuna analisi di elasticità della domanda la sostiene.`

Qui *«domanda»* è usata nel senso economico ordinario — la disponibilità del mercato a pagare un prezzo — cioè esattamente il senso che `BL-Q2-10` ha appena escluso, e su una pagina diversa, dove la glossa non c'è. Il lettore che ha assorbito `BL-Q2-10` ha imparato che in questa dashboard «domanda» significa «indice di popolarità della fonte»; se applica quella lezione a `BL-Q3-2` legge che nessuna analisi di elasticità dell'indice di popolarità sostiene il prezzo, che non significa niente.

Aggravante minore, ma coerente: `BL-Q3-5` usa *«è una domanda a cui questi numeri non rispondono»* in un terzo senso, quello ordinario di interrogativo. Tre significati della stessa parola in quattro pagine, su una parola che il contratto stesso ha marcato come la più pericolosa.

**Documento B**, prova 8, dichiara: *«**passata** — la parola «domanda» è dichiarata su `BQ2` come indice della fonte (`BL-Q2-10`)»*. La prova ha verificato una pagina e la conclusione è scritta come se valesse per tutte.

---

### `R12` — `BL-IN-1` glossa una formula che a schermo non compare, e lascia sglossata quella che compare — gravità **media**

**Documento A**, `BL-IN-1`, ultima frase:

> `Ogni volta che qui si legge «il nostro catalogo», si intende il catalogo di riferimento.`

Ho letto la lettera di tutti e trentadue i blocchi: **«il nostro catalogo» non compare in nessuno**. Il lettore riceve quindi, nel blocco più importante della dashboard, un'istruzione per un caso che non si presenterà mai. L'effetto immediato è modesto — una frase in più — ma quello di secondo ordine no: la frase introduce una prima persona plurale che il resto del testo non usa, e suggerisce al lettore che da qualche parte, più avanti, la dashboard parlerà di «noi». Cercandola, non la trova.

Nel frattempo la formula che **compare davvero** resta senza glossa. `BL-Q1-3`, su `BQ1`:

> `il contenuto musicale non è residuale nel catalogo attuale`

*«il catalogo attuale»* — di chi? Il lettore ha letto trenta secondi prima che nessun dato di StreamWave esiste in questo progetto, e ora legge di un «catalogo attuale» in una frase che parla della condizione di una regola di decisione aziendale. Le due letture disponibili — il catalogo attuale di StreamWave, che non esiste, e il catalogo di riferimento, che è quello di Netflix — portano a conclusioni opposte sulla portata di `C1`, e il presidio costruito per questo caso preciso punta altrove.

---

### `R13` — `BL-IN-3`: la frase che resta scivola fra «confidenza alta» e «valore alto», e «corrispondenza costruita» non è sciolta in nessun punto — gravità **media**

**Documento A**, `BL-IN-3`, chiusa:

> `Un indicatore a confidenza alta è alto rispetto al catalogo di riferimento, non rispetto a StreamWave.`

La frase mette due volte la parola «alto» a distanza di sei parole, riferita la prima volta alla **confidenza** e la seconda al **valore**. La lettura naturale del destinatario è che un indicatore a confidenza alta sia *un indicatore alto*, cioè che l'etichetta dica qualcosa sulla grandezza del numero. È il contrario esatto di ciò che il blocco vuole. E secondo `SC-1` questa è **l'unica delle due frasi di chiusura sopravvissuta**: l'enunciato generale che la governava — *«Questa etichetta non dice quanto il numero descriva StreamWave»* — è caduto, quindi a schermo resta l'esempio senza la regola, e l'esempio è quello ambiguo.

**Secondo difetto, sullo stesso blocco.** La definizione di *media* dice:

> `Media: fra il dato e il numero si interpone almeno una corrispondenza costruita dall'analista o un'ipotesi dichiarata.`

*«Corrispondenza costruita»* è il concetto portante di tutta la scala, ricompare in `BL-Q1-1` e in `BL-Q1-4`, e **non è definito in nessun blocco**. Il lettore deve indovinare che significhi «una tabella che qualcuno ha compilato a mano per far parlare due cataloghi diversi». `BL-Q1-6` gliene dà per caso un esempio (*«una tabella che assegna a ciascuna categoria video un profilo…»*) ma tre blocchi e una pagina dopo. E `SC-1` registra che dalla definizione di *alta* è caduto proprio *«senza corrispondenze costruite né ipotesi interposte»*, cioè, come il documento B stesso dice, *«il contrappunto che rendeva leggibili media e bassa»*.

---

### `R14` — Il blocco che porta le sole due cifre della dashboard sta dove il documento dichiara che il lettore non guarda — gravità **media**

**Documento A**, apertura: il destinatario *«non aprirebbe una nota a piè di pagina»*.

**Documento A**, §5, motivazione della collocazione di `BL-IN-4`:

> `La copertura temporale sta a piè di pagina perché è l'unico blocco che vale identico su tutte le pagine e che il lettore ritrova dove si aspetta una nota di edizione.`

Il documento identifica il piè di pagina come il posto che il suo lettore ignora, e vi colloca l'unico blocco che porta cifre, e l'unico che regge una distinzione che lo stesso documento definisce *«la sola categoria di errore contro cui... non esiste presidio automatico»*. La difesa possibile — che una striscia a piè di pagina si vede senza essere «aperta» — è vera e non basta a chiudere la distanza fra le due affermazioni.

**Tre osservazioni sul testo dello stesso blocco:**

- la distinzione di statuto è affidata al contrasto fra *«è l'anno di uscita più recente presente nel dato»* e *«la documentazione della fonte indica»*. È una sfumatura di verbo, in un blocco a piè di pagina, per un lettore che non sta cercando sfumature. Che sia stata scelta *«non con un'etichetta accanto a ciascun anno, che il lettore salterebbe»* è ragionevole in astratto; nel concreto il rimedio è meno visibile del difetto che evitava;
- *«Sono fotografie di momenti diversi»* è **corretta e inerte**: dice al lettore che due fotografie sono di momenti diversi, senza dirgli che cosa rischia se le confronta. Sull'intera dashboard i due cataloghi vengono confrontati — è ciò che `BQ1` fa — e questa è l'unica frase che tocca il problema;
- nessun blocco dice che i dati sono **vecchi**. Il lettore vede `2021` e `2022`; se legge la dashboard nel 2026, l'informazione che gli serve non è che le due fotografie differiscono fra loro di un anno, ma che entrambe hanno diversi anni. *«Nessuna conclusione presentata qui riguarda ciò che è accaduto dopo»* lo implica e non lo dice.

---

### `R15` — Il documento B non descrive lo schermo: è un conteggio, e i rimandi restano senza referente verificato — gravità **media**

**Documento B** si dichiara *«la fonte autorevole su ciò che esiste a schermo»*. Ciò che offre, però, è la tabella «Che cosa è a schermo, pagina per pagina», che per `BQ2` dice per intero:

> `dieci: `BL-Q2-1` … `BL-Q2-10``

e per `BQ3`:

> `nove: `BL-Q3-1` … `BL-Q3-9``

Da queste righe non si ricava dove un blocco stia, accanto a quale visuale, sopra o sotto quale altro, se i titoli siano stati resi come titoli, se un blocco sia visibile senza scorrere. Per `BQ1` la tabella riporta il raggruppamento per area; per le due pagine più cariche, no. La conseguenza è che **il documento autorevole sullo schermo non permette di ricostruire lo schermo**, e che ogni rilievo sulla disposizione — `R10`, la sequenza `BL-Q2-3`/`BL-Q2-4`, la contiguità di `BL-Q1-1b` a `BL-Q1-1` — non è verificabile né da chi revisiona né da chi leggerà questo esito fra sei mesi.

**Il caso in cui questo costa di più sono i rimandi.** Il contratto ha scelto, per `FR-017`, di rimandare invece di ripetere, e a schermo restano almeno quattro espressioni che puntano a qualcosa che il lettore deve trovare con gli occhi:

- `BL-Q1-5`: *«la quota di film accanto al valore»*;
- `BL-Q2-2`: *«i segmenti che portano l'avvertimento in graduatoria»*;
- `BL-Q2-6`: *«Il quadrante»*, che presuppone che sullo schermo un quadrante sia visibile e riconoscibile;
- `BL-Q2-9`: *«un punto nella dispersione»* — e *«la dispersione»*, da sola, è per un lettore non tecnico più facilmente la varianza che un grafico.

Il documento A afferma che il primo è a schermo *«come misura dalla `008a` (`CP-1`)»*. **Nessuna delle dodici prove verifica che questi referenti esistano, siano visibili e siano dove il testo dice.** Se uno di essi non c'è — o c'è ma non «accanto» — il blocco corrispondente rimanda a nulla, e il lettore conclude di aver perso qualcosa. Ho avuto qui l'impulso più forte di uscire dal perimetro e non l'ho seguito: è precisamente il punto in cui **i documenti non si reggono da soli**, e la loro insufficienza è essa stessa il rilievo.

Il documento B, va riconosciuto, arriva da sé molto vicino a questa conclusione quando scrive, su `SC-2`, che *«nessuna delle dodici prove verifica le etichette, ed è una lacuna del disegno di questa feature»*. La lacuna è più larga di come la nomina: non riguarda le etichette, riguarda tutto ciò che sta **accanto** a un blocco.

---

### `R16` — La condizione 2 di `N8` è dichiarata «verificata» su un'evidenza che non copre ciò che la condizione chiede — gravità **media**

**Documento B**, tabella della pubblicabilità, condizione 2:

> `il *perché* di ogni livello di confidenza è a schermo, per tutti e otto i KPI | **verificata** | `BL-Q1-1`, `BL-Q1-4`, `BL-Q1-6` su `BQ1`; …`

L'evidenza portata è **l'elenco dei blocchi che spiegano un livello**. La condizione, però, non chiede che esistano otto spiegazioni: chiede che il perché **di ogni livello** sia a schermo, il che presuppone che ciascun blocco stia accanto al KPI giusto e che il livello di cui parla sia quello effettivamente etichettato sulla scheda. È esattamente l'accoppiamento che `SC-2` ha trovato rotto — un'etichetta che diceva `media` accanto al blocco che spiegava perché la confidenza fosse `alta` — e che il documento B dichiara, nella stessa pagina, non essere coperto da alcuna prova, trovato *«per caso e non per costruzione»*.

Il documento B ha quindi, in due sezioni diverse: la prova che l'accoppiamento non è verificato da nulla, un caso accertato in cui era sbagliato, e la dichiarazione «verificata» sulla condizione che dipende da quell'accoppiamento. Le tre cose non stanno insieme. L'esito onesto della condizione 2 è quello che il documento ha già saputo scrivere per la condizione 3: *«verificata sulla lettera, contestabile sulla sostanza»*.

Una nota minore sulla stessa riga: *«Per `BQ1-K1`, che compare su due pagine, la ragione sta una volta sola su `BQ1` (`N5`)»*. Significa che esiste una pagina in cui un KPI mostra un'etichetta di confidenza senza la propria spiegazione. Per il destinatario, che non è tenuto a leggere le pagine nell'ordine, è un limite reale, ed è registrato come una scelta di economia senza che l'effetto sul lettore sia nominato.

---

### `R17` — Numerali in lettere in posizione di quantità, e la prova 6 che li dichiara assenti — gravità **media**

**Documento A**, Parte I §1.1, la regola che il contratto si dà, dichiarata *«più severa»* e scritta perché la verifica *«non divent[i] una questione di interpretazione»*:

> `nessun blocco scrive «due», «tre», «sette», nemmeno riferito a cose che non sono misure, e nemmeno nella forma dei pronomi che contano al posto del numerale — «i due», «entrambi».`

A schermo, nella lettera dei blocchi:

- `BL-Q1-1b`: *«Il conteggio legge **una sola** etichetta del catalogo»* — ed è una quantità portante, tanto che il documento A la mette in grassetto quando spiega il blocco al §14;
- `BL-Q1-2`: *«si collochi nella **metà superiore** delle categorie per numero di titoli»*;
- `BL-Q2-2`: *«**Più della metà** delle loro righe porta popolarità nulla, la mediana cade dentro **quella metà**»*;
- `BL-Q2-7`: *«una stessa traccia appartiene a **più** segmenti»*;
- `BL-Q2-8`: *«esiste **almeno un** segmento musicale»*, *«nella **metà superiore** per domanda e nella **metà superiore** per affinità»*.

La regola esenta esplicitamente il solo articolo indeterminativo e non dice nulla di frazioni, di «una sola», di «almeno un». Chi verifica si trova quindi, al primo caso reale, davanti alla decisione interpretativa che la regola era stata scritta per evitare.

**Documento A**, §13, dichiara il vincolo *«**rispettato**»*; **documento B**, prova 6, dichiara *«**passata** — `2021` e `2022` solo su `BL-IN-4`, nessun'altra cifra su alcun blocco»*. La formulazione della prova scivola da «numerale» a «cifra», che è il perimetro più stretto, e sotto quel perimetro l'esito è vero: nessun'altra **cifra**. Sotto il perimetro che la regola dichiara, no.

Al di là della conformità, resta un fatto sul lettore: *«Più della metà delle loro righe porta popolarità nulla»* è **un'affermazione quantitativa su un fatto misurato, a schermo, senza alcun numero visibile che la sostenga**. È il lettore che deve credere sulla parola, ed è la categoria che questo progetto dichiara altrove di non ammettere.

---

### `R18` — I conteggi interni dei due documenti non tornano, in documenti la cui tesi è che nessun numero sta senza fonte — gravità **media**

Quattro casi, tutti verificabili senza uscire dai due file.

1. **Documento A**, §13.1, prima riga: *«l'accorciamento ha un prezzo su **tre obblighi**. Nessuno dei **tre blocchi** afferma il falso»*. La tabella che segue immediatamente ha **nove righe**, e sei righe più sotto lo stesso documento scrive *«in **otto casi su nove**»*. Il documento B conferma il nove: *«I **nove** obblighi che il contratto elenca in §13.1»*. La frase d'apertura della sezione che esiste per non nascondere gli indebolimenti ne dichiara un terzo.
2. **Documento A**, nota su `BL-Q1-7`: *«è il caso più oneroso **dei tre di questa pagina**»*. Su `BQ1`, la tabella §13.1 elenca due obblighi indeboliti, `OB-11` e `OB-12`.
3. **Documento A**, §8, sulla fascia di `BQ3`: *«porta **tre** assunzioni strutturali, **quattro** limiti di lettura e **un** debito di governance»* — otto, per una pagina che il documento stesso e il documento B contano a **nove** blocchi.
4. **Documento B**, «Chi garantisce che tutto questo sia vero»: *«Tre presidi umani e nessuno script: la revisione in contesto pulito che questo esito riceverà, **le undici prove manuali di lettura**, e la disciplina…»*. La tabella ha dodici prove, di cui la 1 è eseguibile e la 12 **non è stata eseguita**: le prove manuali effettivamente eseguite sono dieci. Il conteggio dei presidi include una prova che il documento dichiara, quattro righe più su, di non aver eseguito — e lo fa nel punto in cui elenca ciò che garantisce la pubblicabilità.

Nessuno di questi quattro cambia una conclusione. Insieme cambiano il credito che un lettore esterno concede al resto: sono documenti che chiedono di essere creduti sulla disciplina dei numeri.

---

### `R19` — `BL-Q1-7` e `BL-Q1-8` sembrano dare due origini diverse agli stessi estremi — gravità **media**

**Documento A**, `BL-Q1-7`:

> `La regione con cui il catalogo musicale viene confrontato è costruita prendendo, asse per asse, il valore minimo e quello massimo dei profili video.`

**Documento A**, `BL-Q1-8`, blocco successivo, stessa area:

> `Gli estremi di ciascun asse provengono dalla scala a passi regolari con cui sono stati assegnati i profili, non dal catalogo video in sé`

Il lettore ha appena appreso che gli estremi vengono **dai profili video**; legge subito dopo che vengono **dalla scala e non dal catalogo video**. La riconciliazione esiste — i profili sono assegnati per criterio, quindi i loro estremi sono estremi della scala — ma richiede un passaggio che nessuna delle due frasi compie, e il lettore che non lo compie conclude che i due blocchi si smentiscono.

**Un secondo difetto, più grave del primo per il tipo di lettore.** `BL-Q1-7` è il paragrafo tecnicamente più denso dell'intera dashboard: «regione», «asse per asse», e un esempio geometrico di due frasi su combinazioni che nessuna categoria occupa. Ciò che il lettore deve portare via è una cosa sola — *questo numero è gonfiato* — e sta nel titolo. Ciò che è caduto con l'indebolimento di `OB-11` è la sola informazione che gli serve dopo: **di quanto**, e che nessuno lo sappia. Il blocco ha quindi conservato la parte difficile e perso la parte utile. Aggiungo, per l'onestà del confronto con il §13.1 del documento A, che questo indebolimento l'avrei rilevato anche senza la tabella: un lettore a cui si dice che una stima è «per eccesso» e non si dice di quanto, non ha ricevuto una cautela, ha ricevuto un'inquietudine.

`BL-Q1-8` chiude con *«L'intervallo che ne risulta è ampio su ogni asse»* e si ferma lì: il lettore resta con un fatto tecnico e nessuna istruzione, e il legame con l'etichetta «media» accanto al numero — che è ciò che l'obbligo chiedeva — lo deve costruire da sé. Il titolo promette *«Perché questo valore è alto per costruzione»*; il testo non contiene mai le parole «alto» né «valore».

---

### `R20` — `BL-Q1-2` e `BL-Q1-3` danno di `C1` due definizioni che il lettore non può conciliare — gravità **media**

**Documento A**, `BL-Q1-2`:

> `C1 chiede invece se la categoria musicale si collochi nella metà superiore delle categorie per numero di titoli.`

**Documento A**, `BL-Q1-3`, blocco successivo:

> `C1 è il nome che il business case dà a una condizione della propria regola di decisione: il contenuto musicale non è residuale nel catalogo attuale.`

Due definizioni della stessa sigla, a un blocco di distanza, una operativa (una posizione in una graduatoria di categorie) e una qualitativa (non residuale). Sono compatibili se si accetta che la seconda sia la formulazione del business case e la prima il suo criterio operativo, ma nessuno dei due blocchi lo dice, e l'ordine di lettura presenta prima il criterio e poi l'enunciato. Il lettore che le confronta si chiede quale delle due sia `C1`; quello che non le confronta ne ricorda una a caso.

---

### `R21` — `BQ1` spiega con precisione un confronto di cui non dice mai a che cosa serva — gravità **media**

**Documento A**, `BL-Q1-4` e `BL-Q1-5`. Il primo dice perché la confidenza è alta (*«la differenza fra una durata mediana osservata sul lato video e una durata mediana osservata sul lato musicale»*); il secondo dice che il confronto è asimmetrico (*«Sul lato video entrano i soli film… Sul lato musicale entra invece il catalogo intero»*).

Le due spiegazioni sono corrette, chiare, e **inerti**. Il destinatario che legge di una differenza fra la durata mediana dei film e la durata mediana dei brani musicali non ha bisogno di sapere che il confronto è asimmetrico per costruzione: ha bisogno di sapere perché qualcuno abbia messo quel numero su una scheda. Un film dura un'ora e mezza, una canzone tre minuti; che la differenza sia grande non è una scoperta, e nessun blocco della pagina dice che cosa quella differenza governi — se sia un fatto di formato, di licenza, di consumo, di catalogo. Il lettore quindi capisce esattamente **come** il numero è costruito e continua a non sapere **perché** lo stia guardando.

È il caso più puro della categoria «corretto ma inerte», e nasce dalla stessa radice di `R1`: i registri ammessi contengono «che cosa il valore misura» e questo è stato interpretato come «con quali dati è calcolato» invece che «che cosa dice del mondo».

---

### `R22` — Quattro blocchi finiscono senza punto, in caselle che scorrono — gravità **bassa**

**Documento A**, testi letterali di `BL-Q2-1` (*«…come approssimazione della domanda di mercato»*), `BL-Q2-2` (*«…non una priorità bassa»*), `BL-Q2-4` (*«…in sé, non ha significato»*), `BL-Q2-6` (*«…tutti dentro o tutti fuori dal quadrante»*). Il documento B registra la stessa mancanza su `BL-IN-3` (*«Manca inoltre il punto finale all'ultima frase del blocco»*).

Preso da solo è un difetto di finitura. Preso insieme a `SC-3` non lo è: l'argomento con cui il documento B attenua lo scorrimento è che *«Una barra di scorrimento… **dichiara la propria esistenza**, e chi vede il testo tagliato a metà sa che continua»*. Il complemento di quell'argomento è che **chi vede un testo finito sa che è finito** — e un testo che si interrompe senza punto, dentro una casella che potrebbe scorrere, non offre quel segnale. Il lettore o scorre a vuoto o dubita di aver perso una riga. Quattro blocchi su dieci della pagina più carica sono in questa condizione, e uno del documento B — la riga di *bassa* — è davvero tronco (`R5`), il che rende il dubbio ragionevole invece che paranoico.

---

### `R23` — Riferimenti interni incoerenti fra i due documenti e dentro il documento A — gravità **bassa**

- **La `§15` non esiste.** Il documento A passa da «§14. Le due decisioni prese al punto di fermata» a «§16. Come si verifica che questo contratto sia stato rispettato». Nulla dichiara che una sezione sia stata rimossa. In un repository che pratica la nota in loco, un salto muto di numerazione è la forma di correzione che il metodo esclude — ammesso che sia una correzione e non un errore di trasmissione (§1, impulso 7).
- **`§13` e `§13.1` sono usate per la stessa destinazione.** `BL-IN-4`, `BL-Q1-7` e `BL-Q1-8` rimandano a *«§13»*; `BL-Q2-2`, `BL-Q2-6`, `BL-Q2-7`, `BL-Q3-1`, `BL-Q3-4` e `BL-Q3-9` rimandano a *«§13.1»*. La tabella degli indebolimenti è la seconda.
- **`data-model.md` e `data_model.md`** differiscono di un carattere e sono due cose diverse: il primo compare come collegamento a un artefatto di feature, il secondo come documento pubblicato citato per sezione. Chi manterrà questo contratto sbaglierà l'uno per l'altro, e la revisione non ha modo di accorgersene dall'interno.
- **Il documento B usa `★1`, `★3`, `BQ1-K1`, `BQ1-K2`** senza scioglierli. Sono leggibili solo con `quickstart.md` e `data-model.md` in mano. Il documento B è l'artefatto che una revisione esterna riceve: non si regge da solo su questi punti.

---

### `R24` — Il contratto stabilisce che ogni blocco ha un titolo, e cinque blocchi dopo ne presenta uno che non ce l'ha — gravità **bassa**

**Documento A**, Parte II, apertura: *«Ogni blocco ha un **titolo** e un **testo**»*. `BL-Q1-1b` non ha titolo, per scelta motivata e dichiarata nel blocco stesso. La regola generale andava scritta con l'eccezione, o non scritta come universale.

Nella stessa famiglia, un effetto sul lettore: due blocchi hanno un testo **grammaticalmente dipendente dal proprio titolo**. `BL-Q2-10` comincia con *«Nomina un indice di popolarità…»*, il cui soggetto è la parola «domanda» nominata nel titolo; `BL-Q3-7` comincia con *«È calcolato su una base assunta costante»*, il cui soggetto è «il tasso» del titolo. Poiché il contratto lascia a chi costruisce la resa tipografica del titolo, e poiché la funzione dichiarata del titolo è di essere un filtro che si può non seguire, un lettore che salti il titolo trova una frase senza soggetto.

---

### `R25` — Un difetto che non è un difetto: la difesa dei superlativi in `BL-Q1-7` — gravità **bassa**

**Documento A**, nota a `BL-Q1-7`:

> `**Sui superlativi che compaiono nel testo**: *«la categoria più energica»* e *«la più cupa»* non sono affermazioni su un fatto misurato…`

La nota è corretta e non era necessaria: nessun lettore leggerà *«un'energia pari a quella della categoria più energica»* come una graduatoria pubblicata, perché la frase non nomina alcuna categoria ed è esplicitamente un esempio di una costruzione geometrica. Il paragrafo difende il blocco da un'accusa che nessuno gli muoverebbe.

Lo registro perché la sua esistenza illumina un'asimmetria di attenzione che attraversa tutto il documento A: un paragrafo di argomentazione a presidio di una violazione formale che non c'è, **nello stesso blocco** in cui è caduta senza sostituzione la sola frase che diceva al lettore quanto il numero fosse gonfiato (`R19`). L'apparato dei divieti riceve cura in proporzione alla propria formalizzabilità, non al proprio effetto sul destinatario — che è la ragione per cui il metro dichiarato di questa revisione è quello che è.

---

## 4. Che cosa funziona, e non va toccato mentre si chiudono i rilievi

**Nel testo a schermo.**

- **`BL-IN-1`, il titolo**: `Questi numeri non descrivono StreamWave`. Cinque parole che portano l'affermazione più importante del deliverable, nella posizione in cui non si può mancarla, senza una sola parola di gergo. Nulla di ciò che segue nella dashboard è scritto altrettanto bene, ed è la riga giusta nel posto giusto.
- **Le sostituzioni concrete di `BL-IN-1`**: *«il catalogo video di Netflix sta al posto del catalogo attuale di StreamWave»*. Il lettore capisce l'intero impianto dei proxy da una frase, senza che la parola «proxy» compaia. È il modello di come tutti gli altri concetti tecnici andrebbero resi.
- **`BL-IN-2`, la forma a negazioni successive**, con la ragione dichiarata (*«un lettore che si ferma alla prima ha comunque letto una cosa vera e completa»*). È l'unico blocco costruito tenendo conto che il lettore possa fermarsi a metà, ed è, non a caso, quello che regge meglio lo scorrimento di `SC-3`.
- **`BL-Q1-5`, le prime tre frasi**: *«Sul lato video entrano i soli film. Le serie misurano la propria durata in stagioni. Sul lato musicale entra invece il catalogo intero.»* Tre frasi brevi, un fatto ciascuna, zero gergo, e la ragione tecnica dell'asimmetria resa senza nominarla. È la migliore prosa tecnica dell'insieme (il che non salva il blocco da `R21`, che riguarda ciò che manca dopo).
- **`BL-Q2-6`, «è una risposta per sì o per no»**: la resa più efficace di una soglia che si possa chiedere a una riga.
- **`BL-Q3-5`**: *«Chiedere con quale probabilità il valore vero cada dentro la banda è una domanda a cui questi numeri non rispondono.»* Formula il divieto come la domanda che il lettore avrebbe davvero fatto, invece che come una proprietà dell'oggetto. È il solo blocco che parla al lettore invece che del numero.
- **`BL-Q3-6`**: *«Non è un totale cumulato sul periodo e non è un dato annuo: nei primi mesi sarebbe minore.»* Concreto, immediatamente utilizzabile, e chiude tre fraintendimenti in una riga.
- **La formulazione gemella di `BL-Q1-3` e `BL-Q2-8`**, e la scelta di renderle identiche nell'attacco e nella chiusa. La frase *«Da sola, questa condizione non decide nulla»* è chiara e sufficiente; il difetto che `R2` descrive sta nei nomi delle condizioni, non in questa frase, e chiudendo `R2` non va toccata.
- **`BL-Q2-9`**, che dichiara a schermo un limite dello strumento invece di lasciarlo scoprire. È una scelta rara e va difesa se lo spazio stringe.

**Nel documento B**, e questo va detto con precisione, perché il rischio concreto è che i rilievi qui sopra vengano chiusi **cancellando le ammissioni invece dei difetti**:

- **le prove 5 e 10 marcate come non-verdi-piene**, con la ragione dichiarata: *«una tabella di prove tutte verdi accanto a una sezione con tre scostamenti è una tabella che si legge senza leggere l'altra»*. È giusto, ed è la riga più utile del documento;
- **la non esecuzione della prova 12 dichiarata come tale** invece che sostituita da un esito;
- **la ragione di `SC-1` nominata come estetica** e non travestita da vincolo di spazio — l'onestà del gesto resta anche se la premessa su cui poggia è sbagliata (`R5a`): sono due difetti diversi, e correggendo il secondo non va perso il primo;
- **l'ammissione che nessuna prova verifica le etichette**, e che `SC-2` è stato trovato per caso;
- **l'elenco «Che cosa "pubblicabile" non significa»**, in particolare il quinto trattino sullo scorrimento, che è la frase che rende contestabile la dichiarazione. Va tenuta anche — soprattutto — se la dichiarazione viene riformulata per `R6`;
- **la distinzione fra accorciamenti decisi in revisione e tagli fatti in costruzione**, con la ragione (*«un accorciamento in revisione è passato per un'approvazione, un taglio in costruzione no»*). È una distinzione reale e utile a chi legge da fuori;
- **la condizione 3 di `N8` marcata «verificata sulla lettera, contestabile sulla sostanza»**, con l'invito esplicito al revisore a contestarla. È la forma corretta, ed è la stessa che `R16` chiede di applicare alla condizione 2.

---

## 5. Giudizio complessivo sul metro dichiarato

**No: davanti al destinatario descritto, questi testi non si leggono ancora.** Non per imprecisione — sono, per quanto una revisione esterna possa giudicare, scrupolosi — ma per tre ragioni che si sommano.

**La prima è che manca l'altra metà.** Trentadue blocchi dicono al lettore che cosa non concludere; nessuno gli dice che cosa può concludere, e la pagina di ingresso, che è l'unica che leggerà tutta, è composta di quattro cautele. Il documento A teme, giustamente, che il lettore concluda troppo; il risultato è un testo davanti al quale l'unica mossa razionale è non concludere niente, e un decisore che non conclude niente non ha usato la dashboard — l'ha archiviata. Il registro «che cosa il valore misura», che il contratto ammette per primo, è stato usato per dire con quali dati il numero è calcolato, quasi mai per dire che cosa dice del mondo (`R1`, `R21`).

**La seconda è che ciò che è caduto è sistematicamente la parte utile.** Il documento A lo dichiara da sé — *«in otto casi su nove ciò che cade è la seconda metà del blocco»* — senza trarne la conseguenza: la seconda metà è quasi sempre la conseguenza pratica, e la prima metà è quasi sempre il meccanismo. Restano quindi a schermo, ripetutamente, la spiegazione difficile senza l'istruzione facile: si sa come è costruita la regione dei profili ma non di quanto la sovrapposizione sia gonfiata (`R19`); si sa che gli scenari vanno letti insieme ma non perché (`R7` di riflesso); si sa che il valore centrale viene da un terzo ma non che assumerlo per StreamWave sia un'ipotesi (`R8`). Il costo di questi accorciamenti è stato pagato tutto dallo stesso lato.

**La terza è che, in almeno quattro punti, il lettore capisce il contrario.** «Un debito aperto» su una pagina di impatto economico (`R4`); un valore dichiarato verificabile e, due blocchi più in là, non giudicabile (`R3`); «un indicatore a confidenza alta è alto» (`R13`); l'invito a moltiplicare senza il presidio che lo qualificava (`R8`). Sono quattro, sono localizzati, e sono la parte del lavoro che si può riparare in poche righe.

**Sulla dichiarazione di pubblicabilità.** Non la contesto sul criterio — `N8` è stato fissato prima e verificato dopo, che è il modo corretto — ma sulla **ragione in una riga**, che promette che il lettore non trarrà conclusioni non sostenute mentre lo stesso documento dichiara che chi non scorre non legge la parte che glielo impedirebbe (`R6`), e sulla **tempistica**: un file che porta a schermo, sulla prima pagina, una frase troncata a metà (`R5b`) non è pubblicabile oggi, qualunque cosa dicano le cinque condizioni, perché è la sola circostanza in cui il destinatario non incontra un testo discutibile ma un testo rotto. Nessuna delle due obiezioni chiede di allargare `N8`: la prima chiede di riformulare una frase, la seconda di finire una riparazione che il documento stesso ha già prescritto.

**La distanza fra qui e un sì non è grande, e non passa dalla riapertura del contratto.** Passa da cinque cose: riparare la riga tronca; ritrovare una frase sola che dica a che cosa serve guardare queste quattro pagine; mettere a schermo l'orizzonte, o dire perché non c'è; riconciliare `BL-Q3-4` con `BL-Q3-9`; cambiare il titolo `Un debito aperto`. Tutto il resto di questo verbale è, per gravità dichiarata, sotto quella soglia.

**Un'ultima nota sul disegno di questa revisione.** Il documento A, al §13.1, chiede che il revisore arrivi per conto proprio ai tre indebolimenti più onerosi e dichiara che, se li trova, la decisione va rivista. La prova, così com'è congegnata, non è eseguibile: la tabella degli indebolimenti sta **nello stesso documento** che il revisore riceve, e non c'è modo di leggere i blocchi senza aver letto anche la loro confessione. Dichiaro quindi quali avrei rilevato comunque, e su quali non posso pronunciarmi: **avrei rilevato** `OB-11` (`R19`: «stima per eccesso» senza dire di quanto è un'inquietudine, non una cautela), `OB-27` (`R8` e `R3`: il blocco è incoerente con `BL-Q3-9` e lascia aperta la moltiplicazione) e `OB-24` (`R7`: «vanno letti insieme» come istruzione senza motivo e senza oggetto chiaro). **Non mi sono accorto per conto mio** che mancasse qualcosa in `OB-15`, `OB-19` e `OB-20`: quei tre blocchi, letti da fuori, sembrano completi. Per quel che vale come misura, la brevità ha comprato più di quanto è costata su tre casi su sei, e su tre no.
