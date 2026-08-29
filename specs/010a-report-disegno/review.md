# Verbale di revisione in contesto pulito — `010a-report-disegno`

**Data**: 2026-08-29 · **Oggetto**: `specs/010a-report-disegno/contracts/page-contract.md` · **Revisore**: subagent in contesto isolato, senza accesso al repository

---

## Come è stata condotta

*Questa sezione è di chi ha organizzato la revisione. Il verbale del revisore comincia più sotto ed è trascritto integralmente.*

**Configurazione.** Un subagent ha ricevuto **due soli file**, copiati in una cartella temporanea fuori dal repository e rinominati per non rivelare la propria provenienza:

| File consegnato | Origine | Ruolo nel mandato |
|---|---|---|
| `argomento.md` | `docs/raccomandazione.md` | **il metro**, non l'oggetto: esplicitamente escluso dalla revisione |
| `contratto-di-pagina.md` | `specs/010a-report-disegno/contracts/page-contract.md` | **l'oggetto** |

Il subagent non aveva accesso al repository, alla history git, alla spec, al piano, ai documenti sotto `docs/`, agli artefatti sotto `reports/`, alle issue, né alla constitution. Non ha usato ricerca web.

### La versione revisionata, ancorata

| Documento | Commit di provenienza | `sha256` del contenuto consegnato |
|---|---|---|
| il contratto | `56ac663` — *feat: il contratto di pagina della 010a* | `8b017367044d990e64fb5c395fae60ebc60c9da6d14b56cb9f633373ff523999` |
| l'argomento (metro) | `f986ac3` — *fix: chiusi i nove rilievi della revisione sul deliverable* | `b32ade7b90b7d9f9563a6b987d03bff683f1db09db9e61ac1e2a96707940fa32` |

Stato del repository alla consegna: `25895c1`, ramo `010a-report-disegno`.

### Il perimetro, e la domanda che è stata fatta verificare

**Questa revisione ha una difficoltà propria, dichiarata prima di cominciare** in [plan.md](./plan.md), sezione «Il perimetro della revisione».

Il revisore deve poter giudicare se il disegno regge la spina dell'argomento: quindi riceve `docs/raccomandazione.md` insieme al contratto. Ma un revisore che ha letto entrambi **non può più dire se il contratto si legga da solo** — ed è la proprietà che conta per chi costruirà, che aprirà la `010b` con il contratto in mano e non con la raccomandazione.

Le due domande sono incompatibili nella stessa sessione. **È stata fatta verificare la prima**: *il disegno regge la spina dell'argomento?*

**La ragione della scelta**, ripetuta qui perché il verbale si legga da solo: la seconda domanda ha un presidio alternativo e la prima no. Se il contratto non si legge da solo, la `010b` lo scopre alla prima ora di lavoro e torna a chiedere — costoso, ma recuperabile. Se il disegno non regge la spina, la `010b` costruisce dieci pagine che ripetono il difetto per cui questa feature esiste, e il costo è l'intera feature.

**Che cosa questo lascia scoperto, dichiarato e non taciuto**: nessuno ha verificato in questa feature che il contratto si legga da solo. È un rischio accettato.

### Una nota sulla prima stesura di questo verbale

**La prima versione di questo file parafrasava il revisore invece di trascriverlo**, riportando i rilievi «nella sostanza, in forma compatta». È stata committata in quella forma e sostituita da questa su richiesta della regia.

Sta qui perché è precisamente il difetto contro cui l'obbligo di trascrizione esiste: `CLAUDE.md` dichiara che «ciò che nessun verbale garantisce è che chi trascrive non abbia ammorbidito», e una parafrasi scritta da chi è stato revisionato è il modo in cui quell'ammorbidimento accade in buona fede. Il testo che segue è integrale.

---

# — Verbale del revisore, trascritto integralmente —

# Verbale di revisione — contratto di pagina `010a-report-disegno`

**Data**: 2026-08-29 · **Revisore**: sessione indipendente, contesto isolato

---

## Apertura

**Che cosa ho letto.** I due soli file presenti nella cartella `revisione-010a/`, entrambi per intero:

- `argomento.md` — 226 righe, la raccomandazione della `009`, letta come **metro** e non come oggetto di revisione;
- `contratto-di-pagina.md` — 710 righe, il disegno delle dieci pagine, **oggetto della revisione**.

**Che cosa non ho letto.** Nulla al di fuori di quei due file. Non ho aperto `business_case.md`, `kpi_measures.md`, `kpi_operators.md`, `bq3_scenarios.md`, `data_model.md`, `data-model.md` (§13 lo cita con quel trattino), `plan.md`, il contratto della `008a`, il verbale della revisione della `008b`, la constitution, la roadmap, `reports/kpi_measures.json`, `reports/bq3_scenarios.json`, `data/curated/dim_category_mood.json`, né alcuna delle issue GitHub citate (`#18`, `#20`, `#21`, `#26`). Non ho aperto Power BI né alcun `.pbix`. Non ho consultato la history git.

**Uscite dal perimetro: nessuna.** Non ho usato ricerca web e non ho letto file fuori dalla cartella indicata. I comandi che ho eseguito sono stati `ls`, `wc` e `grep` **sui due soli file della cartella**, per verificare la coerenza interna dei rimandi di sezione e la ricorrenza di termini — nessuna lettura fuori perimetro.

**Conseguenza sul valore di questa revisione.** Tutti i rimandi a documenti esterni (`business_case.md §3`, `§4`, `§5.4`, `§6`; `kpi_measures.md §2.3`, `§5.3`, `§7.3`; `bq3_scenarios.md §8`; `data_model.md §18`; contratto `008a` §1.1, §3, §5.1, §5.2, §5.3, §6, §8; le quattro issue) sono per me **asserzioni non verificabili**. Dove il giudizio ne dipende, lo dichiaro nel rilievo stesso e nella sezione finale.

---

## Esito sulla domanda

**Sì, il disegno regge la spina dell'argomento** — e la regge sostanzialmente, non solo formalmente. Rispondo così alla domanda esplicita di mettere in dubbio il metro: ho cercato il caso «pagine nell'ordine giusto, risultato comunque un inventario» e **non l'ho trovato**.

La ragione è che l'ordine non è imposto dall'esterno alla materia, ma **estratto dalla materia**: le divisioni cadono sulle sottosezioni che `argomento.md` marca già per conto proprio (§1.1 del contratto lo dichiara, e il confronto lo conferma — §2 dell'argomento ha quattro sottosezioni, §3 ne ha due, e le pagine 4-5-6 e 7-8 vi corrispondono). Tre prove più forti della semplice corrispondenza:

1. **La pagina 6 esiste.** «Quanto la stima dovrebbe sbagliare» è il passaggio che l'argomento produce per rispondere a un'obiezione, ed è l'unico che nessun KPI del framework richiedeva. Un inventario mascherato non genera quella pagina: non c'è una misura che la reclami. Il disegno la genera perché segue il ragionamento.
2. **La pagina 2 mette insieme `BQ1-K1`, `BQ1-K3` e `BQ2-K3`**, che il framework teneva su due pagine diverse. §1.2 lo dichiara: la congiunzione — che *è* il verdetto — «non stava da nessuna parte». È il punto in cui il disegno rompe l'organizzazione per categoria di misura, non solo la riordina.
3. **`BQ1-K2` viene escluso** (§1.3, `CP-1`). Un inventario non lascia fuori una misura pubblicata. La completezza rispetto al framework è precisamente la proprietà che il disegno sacrifica, e lo fa dichiarandolo.

Le sette mosse che la consegna elenca trovano tutte una collocazione: domanda (p. 1), risposta (p. 2), perché regge (p. 4-5-6, con p. 3 come premessa sulle fonti), che cosa fare (p. 7-8), quanto vale (p. 9), che cosa la ribalterebbe e che cosa non si può concludere (p. 10).

I rilievi che seguono non ribaltano questo esito. Il più grave, `R1`, riguarda un punto in cui una visuale dice più di quanto l'argomento consenta; gli altri sono cuciture della spina, non la sua rottura.

---

## Rilievi

### `R1` — La pagina 7 marca i segmenti a domanda non misurata, ma non impedisce alla loro posizione di parlare — e la pagina 8 li ordina in coda con la stessa geometria
**Dove**: §9 (pagina 7, le tre marcature) e §10 (pagina 8, la tabella ordinata per punteggio decrescente).
**Gravità**: **sostanziale**.

Il contratto vede il problema e lo affronta bene per la dispersione: §9 dice che i sette segmenti a mediana nulla «cadono tutti contro il bordo sinistro, dove la posizione **si legge come "domanda bassa"**», e impone la marcatura. Il ragionamento è corretto e va conservato.

Ma la marcatura risolve solo metà del difetto, e la metà più facile. `argomento.md` §3 non chiede di *marcare* quei segmenti: chiede qualcosa di più stretto — **«la coda della graduatoria non si legge»**, e «dove quei 7 compaiono, compaiono con questa qualificazione e non altrimenti». Il divieto è sulla *lettura ordinale*, non sulla mancanza di un'etichetta.

Il disegno costruisce invece due geometrie che producono esattamente quella lettura ordinale:

- sulla pagina 7, un punto marcato che sta comunque **all'estremo sinistro di un asse chiamato «domanda»**. La marcatura dice «attenzione a questo punto»; la posizione continua a dire «questo segmento sta in fondo per domanda». Delle due affermazioni simultanee, la geometria è quella che si legge per prima e senza sforzo;
- sulla pagina 8, una tabella **ordinata per punteggio decrescente** in cui quei sette occupano la coda profonda — §10 lo dice esplicitamente. Il punteggio incorpora la domanda; la domanda non è misurata; la posizione in coda è quindi una posizione costruita su un'assenza di misura, presentata nella stessa colonna e con la stessa forma delle posizioni costruite su una misura.

§10 argomenta bene *perché non troncare* la coda — «una vista che tronca la coda mente per omissione» — e ha ragione. Ma da lì non discende che mostrare la coda ordinata sia sufficiente: il contratto ha dimostrato che troncare è peggio, non che ordinare sia innocuo. Fra le due opzioni ne mancava una terza, e il contratto non la considera né la scarta.

Il contratto affida la correzione al testo della `010b` (§17, pagina 8: «come la graduatoria **non** si legge»). È un rimedio più debole di quello che il contratto stesso pretende altrove: a §9 sostiene che senza marcatura «la visuale affermerebbe con la propria geometria ciò che il documento vieta di affermare a parole» — riconoscendo che una geometria non si corregge con una didascalia — e a §14 e §12.1 vieta una barra dei rischi ordinata perché «disegnarli ordinati sarebbe una graduatoria senza fonte». **La posizione in coda di un segmento la cui domanda non è misurata è quel medesimo caso**: un ordinamento la cui fonte, per quelle righe, non esiste. Il contratto vieta la graduatoria senza fonte a pagina 10 e la ammette a pagina 8, senza dichiarare che i due casi differiscono e perché.

Non prescrivo la soluzione — non è compito di questa revisione. Segnalo che il contratto deve **dichiarare una scelta** su questo punto e motivarla, invece di lasciarla implicita: oggi la geometria di pagina 8 afferma una graduatoria completa, e una parte di essa non è sostenuta da alcun valore.

*Perché sostanziale e non bloccante*: il contratto impone la marcatura, la colonna della quota di zeri adiacente e obbligatoria, e il divieto di nascondere quella colonna. Un lettore attento riceve il segnale. Ma un lettore competente contesterebbe che la posizione ordinale, che è il primo segnale che l'occhio riceve, resti non presidiata.

---

### `R2` — La pagina 8 porta una graduatoria a cui l'argomento nega proprio la funzione che una tabella ordinata suggerisce
**Dove**: §10, riga della tabella («ordinata per punteggio decrescente») e la giustificazione «la domanda "da quale segmento entrare" chiede un nome».
**Gravità**: **sostanziale**.

`argomento.md` §3 apre con una frase che il contratto non riprende mai: **«La raccomandazione non è entrare da un genere. È entrare da una regione del catalogo musicale, che i segmenti servono a caratterizzare — non a delimitare.»** E prosegue: «trattarli come alternative affermerebbe il falso»; «una scelta di catalogo si costruisce sulla regione; la graduatoria serve a orientarla, non a sostituirla».

Il contratto giustifica la tabella con: *«la domanda "da quale segmento entrare" chiede un nome. La tabella lo dà.»* Ma quella domanda, formulata così, è **precisamente la domanda che l'argomento dichiara mal posta**. L'argomento non risponde «da quale segmento»; risponde «da quale regione», e presenta i nomi come caratterizzazione della regione.

Il difetto non è la presenza della tabella — l'argomento stesso pubblica gli otto in graduatoria, e §10 ha ragione che la dispersione non porta nomi leggibili. Il difetto è **la motivazione**, che riformula lo scopo della pagina in un modo che l'argomento vieta, e **l'assenza di qualunque vincolo di disegno che presidi la distinzione regione/graduatoria**. Il contratto rinvia anche questo alla prosa della `010b` (§17, pagina 8), che è la stessa fascia già caricata di due altri avvertimenti.

Si noti l'asimmetria interna: a pagina 2 il contratto **non si accontenta** di affidare al testo la lettura corretta della congiunzione — costruisce una visuale che porta le condizioni «dentro l'esito, non accanto», perché «tre schede affiancate lasciano la congiunzione all'occhio di chi guarda» (§4). È il ragionamento giusto, applicato con rigore lì e non qui. La graduatoria di pagina 8 è la forma che lascia all'occhio esattamente la lettura che l'argomento vieta — che i segmenti siano alternative fra cui scegliere il primo — e il disegno non le oppone alcuna contro-forma.

*Perché sostanziale*: il contratto è difendibile — dichiara a §10 che «le due visuali fanno due mosse diverse» e cita l'insistenza di `raccomandazione.md` §3 che «la seconda non sostituisce la prima». Ma poi motiva la tabella con una frase che fa esattamente quella sostituzione, ed è una contraddizione fra due capoversi della stessa sezione.

---

### `R3` — La pagina 1 dichiara «nessun valore compare» e la pagina 3 anticipa una parte della risposta: l'ordine domanda→risposta ha una cucitura non dichiarata
**Dove**: §3 (pagina 1), §5 (pagina 3), e la mappa di §1.
**Gravità**: **sostanziale**.

La pagina 3 («Su che cosa poggia») sta **dopo** la risposta e **prima** delle tre condizioni. Il contratto non motiva mai questa collocazione: la mappa la assegna a «§1, capoverso sui proxy», e §5 argomenta perché è una pagina intera e perché è di sola prosa, ma **non perché stia in terza posizione**.

È un'omissione che pesa, perché la posizione è contestabile in entrambe le direzioni e il contratto non prende partito:

- l'argomento colloca il capoverso sui proxy **dentro §1**, subito dopo la risposta, ed è la posizione che il contratto replica. Coerente;
- ma l'argomento lo colloca lì **dichiarandolo «il limite più importante di questo documento»** e rimandando a §6 per la trattazione estesa — cioè lo tratta **due volte**, in apertura e in chiusura, e dice esplicitamente «va detto due volte» (§6). Il contratto invece **concentra la collocazione a pagina 3** e a pagina 10 lo «richiama, non introduce» (§12). Ha dimezzato una ripetizione che l'argomento dichiara deliberata.

Il contratto non dichiara di aver fatto questa scelta né perché. Dato che §5 costruisce la propria difesa proprio sull'argomento della sopravvivenza all'estrazione di una schermata («un report da cui si ritaglia una schermata deve portare quel limite dentro la schermata»), l'aver ridotto a un richiamo la seconda occorrenza — quella che l'argomento marca come necessaria — è una decisione presa e non motivata.

*Che cosa manca concretamente*: una riga che dichiari perché la premessa sulle fonti sta dopo la risposta e non prima, e perché il «va detto due volte» dell'argomento diventa «detto una volta e richiamato».

---

### `R4` — §13.1 e §13.2 sono citate come «§11» e «§12» in tutto il documento
**Dove**: righe 153, 156, 273, 274, 291, 314, 315, 316, 468 del contratto.
**Gravità**: **minore**.

Nove rimandi puntano le sei misure nuove a «§11» e la visuale esclusa a «§12». Nella numerazione effettiva del documento, §11 è «Pagina 9 — Quanto vale», §12 è «Pagina 10 — Che cosa lo ribalterebbe», e le misure stanno in **§13.1**, le visuali in **§13.2**, la nube esclusa in **§15**.

È il residuo di una rinumerazione: verosimilmente le sezioni delle pagine sono state inserite dopo, spostando in avanti le sezioni finali. Ogni riferimento del gruppo è sbagliato in modo consistente, il che conferma la causa meccanica.

Rileva perché il contratto è un documento **operativo**: la `010b` lo legge per costruire, e ogni volta che incontra «`M2` (nuova, §11)» va a §11 e trova la pagina degli scenari. È attrito su un documento che altrove è molto curato.

Nota collegata, stessa classe: **§13 cita `[data-model.md](../data-model.md)` con il trattino**, mentre §6.1 cita `data_model.md §18` con l'underscore. Uno dei due è sbagliato, e non posso stabilire quale — non ho accesso a nessuno dei due file (vedi sezione finale).

---

### `R5` — L'affermazione «una sola cifra compare in tutto il documento» è contraddetta dal documento stesso
**Dove**: intestazione, riga 11 («Che cosa questo documento non contiene»), contro §9 e §12.
**Gravità**: **minore**.

L'apertura afferma: «**Una sola cifra compare in tutto il documento**, il fattore `100.000` del §11». Ma il contratto ne contiene altre in posizione di fatto, fra cui:

- §9: «ascissa `segment_demand_index` (**scala `0-100`**), ordinata `segment_catalog_affinity` (**dominio `0-1`**)»;
- §8 e §13.2: «barra orizzontale su **asse `0-1` assoluto**»;
- §13.1: «conteggio **`0-3`**»;
- §12: «**quattro** condizioni di ribaltamento», «**tre** delle quattro»; §1.3: «**sette** KPI su otto» (in titolo di sezione e nel testo).

Le prime sono domini d'asse e le seconde numerali in lettere su fatti strutturali del disegno — nessuna è un valore di KPI trascritto, e la sostanza della regola («nessun valore di KPI trascritto») è **rispettata senza eccezioni** per quanto ho potuto verificare. Il difetto è nella formulazione dell'affermazione, che è più larga di ciò che il documento fa e quindi materialmente falsa come scritta.

Rileva più della media perché questo progetto tratta le affermazioni derivate come valori. «Una sola cifra in tutto il documento» è un conteggio su sé stesso, in posizione di fatto, e non regge alla verifica — che è il tipo di difetto che l'argomento a monte è costruito per non commettere.

---

### `R6` — §2 promette una regola valida su tutte le pagine, ma la tabella delle grane non copre due pagine
**Dove**: §2 e la tabella delle tre grane.
**Gravità**: **minore**.

La tabella elenca i valori sotto le tre grane e ne assegna a ciascuna che cosa una selezione può restringere. Non compaiono però i valori delle pagine 3 e 10: `CL.NF.titles.rows.after`, `KPI.BQ1K2.music_tracks` (pagina 3), `NF.num.release_year.max` (pagina 10), né `MOOD.coverage.rows` di pagina 5.

La riga «catalogo intero» elenca «`BQ1-K1`, `BQ1-K3`, le tre condizioni, il verdetto» — un elenco per KPI, non per valore, e quei quattro valori non sono KPI. Le sezioni di pagina risolvono comunque il caso vietando ogni interazione (§5.1, §12.1), quindi **il rischio pratico è nullo**. Ma §2 dichiara che la regola vale su «ogni pagina» e che «le grane pubblicate restano tre e non ne esiste una quarta»: un valore fuori dalle tre grane elencate è, letteralmente, fuori dalla tassonomia che la sezione dichiara esaustiva.

O quei valori appartengono alla grana «catalogo intero» e la riga va formulata perché li includa, o hanno statuto diverso e va detto quale.

---

### `R7` — La sincronizzazione della selezione fra pagine 7 e 8 è dichiarata come vincolo senza dichiarare che cosa succede alla pagina 8 quando la selezione arriva dalla 7
**Dove**: §10.1 e §9.1 («Ammessa: la selezione incrociata verso la pagina 8, come evidenziazione»).
**Gravità**: **minore**.

Il contratto dichiara con precisione ciò che la selezione **non** deve fare: non ricalcolare, non muovere soglie né posizioni, restare evidenziazione. Difende bene la distinzione, e cita `ALL ( dim_segment )` come ragione verificabile. Su questo non ho obiezioni.

Ciò che non dichiara è l'**effetto atteso a schermo** sulla pagina 8. Una tabella di 114 righe che riceve una selezione da un punto della dispersione può: evidenziare la riga lasciandola dov'è (il lettore non la vede, è fuori scroll); evidenziarla **e** portarla in vista; o evidenziarla e ordinare diversamente (che §10.2 vieterebbe). Il contratto vieta la terza, ma fra la prima e la seconda non sceglie — e la differenza è esattamente ciò che distingue la chiusura dell'issue `#21` dalla sua non-chiusura: un'evidenziazione che il lettore non può vedere non è una continuità di lettura, che è il termine con cui §10.1 definisce il difetto.

§10.1 dichiara onestamente di non poter accertare che il comportamento sia ottenibile. Ma qui non si tratta di ottenibilità: si tratta di **che cosa si sta chiedendo**, che è decisione del contratto e non della `010b`. Senza quella riga, la `010b` deve indovinare quale delle due sia la chiusura dell'issue.

---

### `R8` — «Il report porta sette KPI su otto»: il titolo di §1.3 è un'affermazione sul framework, in un documento che dichiara di averlo sciolto
**Dove**: §1.3, e `CP-1` in §18.
**Gravità**: **minore**.

Rilievo di coerenza interna, non di sostanza. §1.2 stabilisce che le pagine non portano le sigle e che l'ordine non è quello del framework; `CP-1` dichiara che «il report non è più leggibile come "la dashboard degli otto KPI"» e che «spiegarlo richiederebbe di nominare un framework che il report ha deliberatamente sciolto».

Eppure la copertura viene misurata e titolata **nell'unità del framework** — «sette su otto» — che è la metrica dell'artefatto respinto. Un disegno organizzato per mosse d'argomento avrebbe come metrica naturale «le sette mosse dell'argomento trovano tutte una pagina», non «sette KPI su otto».

Non è un difetto di sostanza: la decisione di escludere `BQ1-K2` è ben motivata, la sua contestabilità è dichiarata onestamente, e non chiedo di cambiarla. È il **residuo di categoria** nel titolo che segnalo: la sezione che dichiara sciolto il framework è titolata nella sua unità di misura. Lo noto anche perché §18 `CP-1` mette a fuoco l'aspetto giusto — «nessuna pagina spiega perché manchi» — che è un problema del lettore, non del conteggio.

---

## Che cosa il contratto fa bene

Elenco ciò che a mio giudizio **non va toccato**, perché una correzione dei rilievi sopra rischia di erodervi attorno.

**§1.1 — la regola molti-a-uno e il criterio di divisione.** È la migliore pagina del documento. Enuncia la regola, dimostra che l'asimmetria fra le due direzioni non è arbitraria (una pagina che serve più sezioni *è* l'inventario respinto), e soprattutto fornisce il **presidio contro l'abuso della regola stessa**: si divide quando l'argomento cambia mossa, non quando la sezione ha troppi numeri. La frase «pagine divise per capienza, che è di nuovo un inventario, solo con più fogli» è la formulazione esatta del difetto. E §1.1 chiude verificando che le divisioni cadono su sottosezioni già marcate dall'argomento: «i confini sono stati letti, non inventati». È il passaggio che rende l'esito di questa revisione positivo.

**§4 — la visuale del verdetto, e l'etichetta unica.** Il ragionamento «tre schede affiancate lasciano la congiunzione all'occhio di chi guarda» e la conseguente scelta di portare le condizioni *dentro* l'esito è il caso modello di forma-che-segue-l'argomento. La decisione collegata di §1.4 — **una sola etichetta di confidenza**, perché tre etichette «alta, media, media» inviterebbero alla lettura per media che `argomento.md` §2 esiste per impedire — è un'inferenza corretta e non ovvia dal documento a monte.

**§8 — il divieto di forma sulla pagina 6.** «Nessuna barra di errore, nessun intervallo, nessuna banda», con la ragione: comunicherebbero una dispersione stimata che nessun valore contiene, mentre il margine è una *condizione* sull'errore e non una stima. È il rilievo di tipo 2 della consegna — geometria che direbbe ciò che il documento vieta — visto e chiuso dal contratto stesso, prima che un revisore lo sollevasse. Ugualmente forte il divieto di slicer sulla soglia (§8.1): «la soglia è stata fissata prima di conoscere il valore, ed è quella la proprietà che rende la condizione difendibile; uno slicer la distruggerebbe e nessun controllo lo segnalerebbe».

**§7 — il vincolo di dichiarare l'asse escluso.** Che una dispersione su due assi di tre sia una **proiezione**, e che una proiezione non dichiarata si legga come la cosa intera «nascondendo due volte la stessa asimmetria che rende `BQ1-K3` una stima per eccesso», è l'osservazione più fine del documento. Anche la scelta di far mostrare alla dispersione **il vuoto dentro il rettangolo** — così che il limite si veda invece di essere solo affermato — è forma che porta argomento.

**§14 e §15 — il vuoto difeso e la visuale dichiarata assente.** Vietare la decorazione delle pagine di prosa con la ragione giusta («un grafico afferma con la propria geometria ciò che il testo non afferma»), e poi dichiarare la visuale migliore che il disegno **non** può avere «perché chi costruisce non la reinventi credendo che sia stata dimenticata», sono due presidi contro il difetto più prevedibile in fase di costruzione.

**§7 e §11 — la resistenza alla tentazione, dichiarata come tale.** «È la trasformazione più tentante e la più sbagliata» (slicer sulla soglia); «un campo in cui digitare la base abbonati trasformerebbe la rinuncia in un presidio mancato». E in §11 la distinzione fra il fattore `100.000` come **unità dichiarata** e una stima della base, con la ripresa della formulazione stretta di `argomento.md` §4 e il rifiuto esplicito della formulazione falsa «l'uplift non è scalabile». Il contratto qui legge l'argomento con precisione notevole e ne conserva le distinzioni sottili.

**§7, §18, §19 — l'onestà sui confini della propria autorità.** «Non può dichiarare che funzioni: questa sessione non ha aperto Power BI»; la chiusura *condizionata* dell'issue `#21`; il rifiuto di elencare per nome le tre impostazioni dell'issue `#20` per non creare una seconda copia; e §19 che dichiara previsti gli scostamenti davanti allo schermo, da annotare mentre accadono e non a memoria. Un contratto di disegno che dichiara che cosa non può accertare è più utile di uno che asserisce.

**§9 — il riconoscimento del difetto geometrico dei segmenti a domanda non misurata.** Nonostante `R1`, va detto chiaramente: il contratto **vede** che la posizione contro il bordo sinistro si legge come «domanda bassa» e che senza marcatura la visuale affermerebbe ciò che il documento vieta. Quel ragionamento è corretto e va conservato; `R1` chiede di portarlo fino in fondo, non di sostituirlo.

---

## Che cosa questa revisione non ha potuto verificare

1. **Ogni rimando a documento esterno.** Non ho letto `business_case.md`, `kpi_measures.md`, `kpi_operators.md`, `bq3_scenarios.md`, `data_model.md`, `plan.md`, `data-model.md`, la constitution, la roadmap, il contratto della `008a`, il verbale della `008b`. Non posso quindi verificare: che `business_case.md` §4 formuli davvero `BQ2` come domanda sul quadrante (§9); che §5.4 contenga la tabella delle etichette (§1.4); che §6 dichiari la diversa portata di `A1` e `A6` (§5); che `kpi_measures.md` §2.3 avverta che `C1` non è calcolabile dalla quota (§6); che §5.3 dica che il valore misura la copertura della fonte (§9); che §7.3 pubblichi `ALL ( dim_segment )` nelle due formule (§2.1); che `bq3_scenarios.md` §8 dichiari falsa la formulazione esclusa (§11); che `data_model.md` §18 elenchi l'asse temporale fra le letture prive di significato (§6.1); che il contratto `008a` §5.3 dichiarasse davvero l'assenza del conteggio dei membri (§18 `CP-4`).

2. **L'esistenza e il contenuto degli identificativi di ancora.** Non ho letto `reports/kpi_measures.json`, `reports/bq3_scenarios.json`, né `data/curated/dim_category_mood.json`. Non posso verificare che `KPI.BQ1K3.tracks_inside`, `KPI.BQ1K3.bound.*`, `MOOD.coverage.rows`, `KPI.BQ1K1.denominator_titles`, `NF.num.release_year.max`, `KPI.BQ2K3.threshold.demand`/`.affinity`, `catalogs.kpi_segments` esistano né che siano quelli giusti. **Ho verificato solo la coerenza interna fra i due documenti**: gli identificativi che compaiono in entrambi (`KPI.verdict.conditions_satisfied`, `KPI.BQ1K1.c1.above_median`, `KPI.BQ1K1.c1.median_of_42`, `KPI.BQ1K1.c1.category_count.music_musicals`, `KPI.BQ1K1.share`, `KPI.BQ1K3.overlap_share`, `KPI.BQ1K3.c2.satisfied`, `KPI.BQ1K3.c2.threshold`, `KPI.BQ1K3.c2.margin`, `KPI.BQ1K3.c2.margin_share_of_value`, `KPI.BQ2K3.c3_satisfied`, `KPI.BQ2K3.quadrant_members_count`, `KPI.BQ2K1.high_zero_segments_count`, `CL.NF.titles.rows.after`, `KPI.BQ1K2.music_tracks`, `SP.genre.count`, `conventions.kpi_mood_table_version`, `catalogs.kpi_high_zero_segments`, `BQ3.adoption.*`, `BQ3.uplift.*`) **coincidono senza eccezioni**. Non è poco, ma non è verifica contro la fonte.

3. **Le quattro issue GitHub** (`#18`, `#20`, `#21`, `#26`). Non ho potuto verificare che descrivano ciò che il contratto dice descrivano, né che siano nello stato dichiarato. In particolare non posso giudicare se la chiusura condizionata di `#21` (§10.1, `CP-3`) sia proporzionata al difetto che l'issue registra, né se i due documenti che `#26` lascia aperti siano davvero `kpi_operators.md` §9 e il contratto `008a` §8.

4. **Se le visuali reggano davanti allo schermo.** Non ho aperto Power BI. Non posso giudicare se una dispersione di 114 punti con tre marcature distinte resti leggibile, se una tabella di 114 righe sia navigabile, se una barra di navigazione a dieci elementi stia su 16:9 (§16 dichiara il problema e lascia la forma a chi costruisce — mi pare la scelta giusta, ma non posso confermarla), né se la sincronizzazione della selezione fra pagine sia ottenibile. Il contratto dichiara esso stesso questo limite, e la mia posizione non è migliore della sua.

5. **Se il `.pbix` contenga oggi qualcosa.** Il contratto dichiara di non averlo aperto e che nessuna sua riga afferma che cosa quel file contenga. Non l'ho aperto nemmeno io e non ho modo di verificare quella dichiarazione — che peraltro è la dichiarazione giusta da fare.

6. **La stima in ore della `010b`.** §13 dichiara di essere «la sezione su cui poggia la stima della `010b`», ma la stima non è in questo documento e non l'ho vista. Non posso giudicare se sei misure, quattro visuali nuove, una quinta forma nuova e dieci pagine siano proporzionate a essa.

7. **Il verbale della revisione che ha respinto la dashboard a quattro pagine.** La motivazione mi è stata riferita nella consegna («un decisore che non conclude niente non ha usato la dashboard, l'ha archiviata») e il contratto la cita a §1.1, §1.3 e §13.3. Ho preso quella motivazione come data. Se il verbale contenesse altri rilievi sulla `008b`, non posso sapere se questo disegno li chiuda.

---

*Fine del verbale.*

---

# — Fine del verbale del revisore —

*Il blocco che segue è di chi è stato revisionato e non fa parte della revisione. Il testo sopra non è stato modificato.*

---

## Blocco di chiusura — esito della verifica e decisioni prese

**Data**: 2026-08-29 · **Autore**: la sessione esecutiva della `010a`

### La decisione sulla ripartizione

`CLAUDE.md` prescrive dal 2026-08-22 che una feature chiuda **solo i rilievi strettamente necessari** e rinvii gli altri al tracker. La mia proposta iniziale rientrava in quella soglia — chiudere `R1`, `R2`, `R4`, `R5` e rinviare `R3` con gli altri.

**La regia ha deciso diversamente: chiudere tutti i rilievi da `R1` a `R5`, `R3` compreso.** È una decisione presa con il contesto che questa sessione non ha, ed è registrata qui perché il rinvio di `R3` sarebbe stato altrimenti la scelta prevedibile.

### Come ogni rilievo è stato chiuso

| Rilievo | Gravità | Esito | Come |
|---|---|---|---|
| `R1` | sostanziale | **risolto** | il contratto prende la terza opzione che il revisore osservava mancante: i segmenti a domanda non misurata **escono dall'ordinamento** e restano nella pagina, in un blocco senza colonna di posizione. Nuova §10.2 |
| `R2` | sostanziale | **risolto** | nuova §10.1, che dichiara mal posta la domanda «da quale segmento entrare» e oppone alla lettura per alternative **tre presidi strutturali** invece di affidarla al testo |
| `R3` | sostanziale | **risolto** | §5 motiva ora la terza posizione contro entrambe le alternative, e dichiara che la ripetizione dell'argomento è dimezzata con la ragione per cui a schermo la navigazione compra ciò che nel documento comprava la ripetizione |
| `R4` | minore | **risolto** | corretti i nove rimandi: `§11` → `§13.1` sulle misure, `§12` → `§15` sulla nube. Rinumerate le sottosezioni di §10, che una nuova sezione aveva reso ambigue. Chiarito che `data-model.md` e `docs/data_model.md` sono due file diversi |
| `R5` | minore | **risolto** | l'affermazione «una sola cifra compare in tutto il documento» era materialmente falsa ed è stata sostituita dall'enumerazione delle tre specie di cifra che il documento contiene, con la regola che le governa |
| `R6` | minore | **rinviato** | issue [`#32`](https://github.com/Valvln/streamwave-bi/issues/32) |
| `R7` | minore | **rinviato** | issue [`#33`](https://github.com/Valvln/streamwave-bi/issues/33) |
| `R8` | minore | **rinviato** | issue [`#34`](https://github.com/Valvln/streamwave-bi/issues/34) |

**Nessun rilievo è stato chiuso indebolendo un'affermazione.** È l'esito meno frequente e va dichiarato quando accade: qui non è accaduto. `R5` è il caso che più vi si avvicina — un'affermazione falsa sostituita da una più stretta — ma la nuova formulazione **dice di più**, non di meno: enumera tre specie di cifra dove la precedente ne dichiarava una sola.

### Che cosa la chiusura di `R1` ha prodotto oltre alla correzione

**Una asimmetria fra le pagine 7 e 8, dichiarata nel contratto invece di essere lasciata scoprire.** Il presidio della pagina 8 — togliere la posizione — non è trasferibile alla pagina 7: una dispersione non può sottrarre un punto a un asse senza toglierlo dalla vista, e la marcatura resta lì l'unico presidio disponibile. La differenza non è di rigore ma di forma del dato, ed è scritta a §10.2.

**Un costo dichiarato**: la pagina 8 porta due tabelle invece di una, e chi cerca un segmento deve sapere in quale guardare.

### Che cosa resta scoperto, e non è un rilievo del revisore

**Nessuno ha verificato che il contratto si legga da solo.** È la conseguenza dichiarata della composizione del perimetro: il revisore ha ricevuto anche `docs/raccomandazione.md`, e chi ha letto entrambi non può più rispondere a quella domanda. Il presidio alternativo è la `010b`, che aprirà il contratto senza l'argomento accanto e scoprirà alla prima ora se qualcosa non si regge.

### Verifiche rieseguite dopo le correzioni

| Verifica | Esito |
|---|---|
| `check_audit_coherence.py` | ✅ verde |
| `P2` — le cinque voci per pagina | ✅ tutte e dieci le pagine, invariato |
| rimandi interni al contratto | ✅ tutti risolvono contro una sezione esistente |
