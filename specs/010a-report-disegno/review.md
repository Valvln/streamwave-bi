# Verbale di revisione in contesto pulito — `010a-report-disegno`

**Data**: 2026-08-29 · **Oggetto**: `specs/010a-report-disegno/contracts/page-contract.md` · **Revisore**: subagent in contesto isolato, senza accesso al repository

---

## Come è stata condotta

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

---

## Che cosa il revisore dichiara di aver letto e non letto

*Trascritto dall'apertura del verbale del revisore.*

**Letto**: i due soli file della cartella, entrambi per intero — l'argomento (226 righe) e il contratto (710 righe).

**Non letto**: `business_case.md`, `kpi_measures.md`, `kpi_operators.md`, `bq3_scenarios.md`, `data_model.md`, `data-model.md`, `plan.md`, il contratto della `008a`, il verbale della revisione della `008b`, la constitution, la roadmap, `reports/kpi_measures.json`, `reports/bq3_scenarios.json`, `data/curated/dim_category_mood.json`, le issue `#18`, `#20`, `#21`, `#26`. Nessun `.pbix`. Nessuna history git.

**Uscite dal perimetro**: nessuna. Il revisore dichiara di aver eseguito `ls`, `wc` e `grep` **sui due soli file della cartella**, per verificare la coerenza interna dei rimandi di sezione e la ricorrenza di termini.

---

## Esito sulla domanda

> **Sì, il disegno regge la spina dell'argomento** — e la regge sostanzialmente, non solo formalmente.

Il revisore dichiara di aver cercato il caso «pagine nell'ordine giusto, risultato comunque un inventario» — che il mandato gli chiedeva esplicitamente di cercare — e di **non averlo trovato**.

Le tre prove che porta:

1. **la pagina 6 esiste.** «Quanto la stima dovrebbe sbagliare» è il passaggio che l'argomento produce per rispondere a un'obiezione, ed è l'unico che nessun KPI del framework richiedeva. «Un inventario mascherato non genera quella pagina: non c'è una misura che la reclami»;
2. **la pagina 2 mette insieme tre KPI che il framework teneva su due pagine.** «È il punto in cui il disegno rompe l'organizzazione per categoria di misura, non solo la riordina»;
3. **`BQ1-K2` viene escluso.** «Un inventario non lascia fuori una misura pubblicata.»

Il revisore aggiunge che l'ordine «non è imposto dall'esterno alla materia, ma estratto dalla materia», e che le sette mosse della consegna trovano tutte una collocazione.

---

## I rilievi

*Trascritti nella sostanza, con la gravità assegnata dal revisore. Il testo integrale delle motivazioni è quello che il revisore ha prodotto; qui è riportato in forma compatta senza attenuazioni.*

### `R1` — bloccante? no: **sostanziale**. La coda della graduatoria si legge, e l'argomento lo vieta

**Dove**: §9 (pagina 7, le tre marcature) e §10 (pagina 8, la tabella ordinata per punteggio decrescente).

Il contratto vede il problema per la dispersione e lo affronta bene: impone la marcatura perché la posizione contro il bordo sinistro «si legge come domanda bassa». **Ma la marcatura risolve solo metà del difetto, e la metà più facile.**

`raccomandazione.md` §3 non chiede di *marcare* quei segmenti: chiede qualcosa di più stretto — «**la coda della graduatoria non si legge**». Il divieto è sulla **lettura ordinale**, non sulla mancanza di un'etichetta. Il disegno costruisce invece due geometrie che producono esattamente quella lettura:

- sulla pagina 7, un punto marcato che sta comunque all'estremo sinistro di un asse chiamato «domanda». «Delle due affermazioni simultanee, la geometria è quella che si legge per prima e senza sforzo»;
- sulla pagina 8, una tabella ordinata per punteggio decrescente in cui quei sette occupano la coda profonda. «La posizione in coda è una posizione costruita su un'assenza di misura, presentata nella stessa colonna e con la stessa forma delle posizioni costruite su una misura.»

**L'argomento più forte del rilievo**, ed è una contraddizione interna: il contratto a §14 e §12.1 vieta una barra dei rischi ordinata perché «disegnarli ordinati sarebbe una graduatoria senza fonte». «**La posizione in coda di un segmento la cui domanda non è misurata è quel medesimo caso.** Il contratto vieta la graduatoria senza fonte a pagina 10 e la ammette a pagina 8, senza dichiarare che i due casi differiscono e perché.»

Il revisore osserva inoltre che §10 «ha dimostrato che troncare è peggio, non che ordinare sia innocuo. Fra le due opzioni ne mancava una terza, e il contratto non la considera né la scarta».

Sul rimedio affidato al testo della `010b`: «è un rimedio più debole di quello che il contratto stesso pretende altrove», dato che a §9 riconosce che una geometria non si corregge con una didascalia.

### `R2` — **sostanziale**. La motivazione della graduatoria riformula lo scopo in un modo che l'argomento vieta

**Dove**: §10, la giustificazione «la domanda "da quale segmento entrare" chiede un nome».

`raccomandazione.md` §3 apre con una frase che il contratto **non riprende mai**: «La raccomandazione non è entrare da un genere. È entrare da una **regione** del catalogo musicale, che i segmenti servono a caratterizzare — non a delimitare», e prosegue: «trattarli come alternative affermerebbe il falso».

«Quella domanda, formulata così, è **precisamente la domanda che l'argomento dichiara mal posta**. L'argomento non risponde "da quale segmento"; risponde "da quale regione".»

Il revisore precisa che il difetto **non è la presenza della tabella** — l'argomento stesso pubblica gli otto in graduatoria — ma la motivazione, e **l'assenza di qualunque vincolo di disegno che presidi la distinzione regione/graduatoria**.

**L'asimmetria interna che il rilievo mette a fuoco**: «a pagina 2 il contratto non si accontenta di affidare al testo la lettura corretta della congiunzione — costruisce una visuale che porta le condizioni dentro l'esito. È il ragionamento giusto, applicato con rigore lì e non qui.»

### `R3` — **sostanziale**. La collocazione della pagina 3 non è motivata, e dimezza una ripetizione che l'argomento dichiara deliberata

**Dove**: §3, §5 e la mappa di §1.

Il contratto argomenta perché la pagina 3 è una pagina intera e perché è di sola prosa, ma **non perché stia in terza posizione**.

Il rilievo più preciso: l'argomento tratta le assunzioni **due volte**, in apertura e in chiusura, e dice esplicitamente «va detto due volte». Il contratto «concentra la collocazione a pagina 3» e a pagina 10 le «richiama, non introduce» — «ha dimezzato una ripetizione che l'argomento dichiara deliberata», senza dichiarare di averlo fatto né perché.

Il revisore osserva che questo pesa in particolare perché §5 costruisce la propria difesa proprio sull'argomento della sopravvivenza all'estrazione di una schermata.

### `R4` — **minore**. Nove rimandi interni puntano a sezioni sbagliate

**Dove**: righe 153, 156, 273, 274, 291, 314, 315, 316, 468.

Le misure nuove sono citate come «§11» e la visuale esclusa come «§12»; nella numerazione effettiva §11 è la pagina 9 e §12 è la pagina 10, mentre le misure stanno in §13.1, le visuali in §13.2, la nube esclusa in §15. «È il residuo di una rinumerazione»: ogni riferimento del gruppo è sbagliato in modo consistente.

«Rileva perché il contratto è un documento **operativo**: la `010b` lo legge per costruire, e ogni volta che incontra "`M2` (nuova, §11)" va a §11 e trova la pagina degli scenari.»

**Nota collegata**: §13 cita `data-model.md` col trattino, §6.1 cita `data_model.md` con l'underscore. Il revisore dichiara di non poter stabilire quale sia sbagliato.

### `R5` — **minore**. «Una sola cifra compare in tutto il documento» è materialmente falsa come scritta

**Dove**: intestazione, contro §9, §8, §13.1, §12 e §1.3.

Il contratto contiene altre cifre in posizione di fatto: i domini d'asse (`0-100`, `0-1`, `0-3`) e i numerali in lettere su fatti strutturali del disegno («quattro condizioni di ribaltamento», «sette KPI su otto»).

Il revisore dichiara che **la sostanza della regola è rispettata senza eccezioni** — nessuna è un valore di KPI trascritto — e che il difetto è nella formulazione, «più larga di ciò che il documento fa».

«Rileva più della media perché questo progetto tratta le affermazioni derivate come valori. "Una sola cifra in tutto il documento" è un conteggio su sé stesso, in posizione di fatto, e non regge alla verifica — che è il tipo di difetto che l'argomento a monte è costruito per non commettere.»

### `R6` — **minore**. La tabella delle grane non copre quattro valori di quattro pagine

**Dove**: §2.

Non compaiono `CL.NF.titles.rows.after` e `KPI.BQ1K2.music_tracks` (pagina 3), `NF.num.release_year.max` (pagina 10), `MOOD.coverage.rows` (pagina 5). La riga «catalogo intero» elenca per KPI, e quei quattro valori non sono KPI.

Il revisore riconosce che «il rischio pratico è nullo» perché le sezioni di pagina vietano ogni interazione, ma osserva che §2 dichiara la tassonomia **esaustiva**: «un valore fuori dalle tre grane elencate è, letteralmente, fuori dalla tassonomia che la sezione dichiara esaustiva».

### `R7` — **minore**. Non è dichiarato che cosa la pagina 8 debba fare quando riceve la selezione

**Dove**: §10.1 e §9.1.

Il contratto dichiara con precisione ciò che la selezione **non** deve fare, e il revisore dichiara di non avere obiezioni su quel punto. Ciò che manca è **l'effetto atteso a schermo**: una tabella lunga che riceve una selezione può evidenziare la riga lasciandola fuori vista, oppure evidenziarla e portarla in vista. «La differenza è esattamente ciò che distingue la chiusura dell'issue `#21` dalla sua non-chiusura: un'evidenziazione che il lettore non può vedere non è una continuità di lettura, che è il termine con cui §10.1 definisce il difetto.»

«Qui non si tratta di ottenibilità: si tratta di **che cosa si sta chiedendo**, che è decisione del contratto e non della `010b`.»

### `R8` — **minore**. Il titolo di §1.3 misura la copertura nell'unità del framework che il documento dichiara sciolto

**Dove**: §1.3 e `CP-1`.

«Un disegno organizzato per mosse d'argomento avrebbe come metrica naturale "le sette mosse dell'argomento trovano tutte una pagina", non "sette KPI su otto".»

Il revisore dichiara esplicitamente che **non è un difetto di sostanza** e che non chiede di cambiare la decisione di escludere `BQ1-K2`, la cui motivazione giudica buona: segnala il «residuo di categoria» nel titolo.

---

## Che cosa il revisore dichiara che il contratto fa bene

*Riportato perché il revisore lo formula come vincolo: «elenco ciò che a mio giudizio non va toccato, perché una correzione dei rilievi sopra rischia di erodervi attorno.»*

- **§1.1, la regola molti-a-uno e il criterio di divisione** — «è la migliore pagina del documento», e «il passaggio che rende l'esito di questa revisione positivo». In particolare il presidio contro l'abuso della regola stessa e la verifica che «i confini sono stati letti, non inventati»;
- **§4, la visuale del verdetto e l'etichetta unica** — «il caso modello di forma-che-segue-l'argomento»; la scelta di una sola etichetta di confidenza è «un'inferenza corretta e non ovvia dal documento a monte»;
- **§8, il divieto di forma sulla pagina 6** — «è il rilievo di tipo 2 della consegna, visto e chiuso dal contratto stesso prima che un revisore lo sollevasse». Ugualmente forte il divieto di slicer sulla soglia;
- **§7, il vincolo di dichiarare l'asse escluso** — «l'osservazione più fine del documento»;
- **§14 e §15, il vuoto difeso e la visuale dichiarata assente** — «due presidi contro il difetto più prevedibile in fase di costruzione»;
- **§7 e §11, la resistenza alla tentazione dichiarata come tale** — sul fattore di conversione: «il contratto qui legge l'argomento con precisione notevole e ne conserva le distinzioni sottili»;
- **§7, §18, §19, l'onestà sui confini della propria autorità** — «un contratto di disegno che dichiara che cosa non può accertare è più utile di uno che asserisce»;
- **§9, il riconoscimento del difetto geometrico** — «nonostante `R1`, va detto chiaramente: il contratto **vede** il problema. `R1` chiede di portare quel ragionamento fino in fondo, non di sostituirlo».

---

## Che cosa questa revisione non ha potuto verificare

*Trascritto dal verbale del revisore.*

1. **Ogni rimando a documento esterno** — nessuno dei documenti citati dal contratto è stato letto. Il revisore elenca puntualmente le nove affermazioni che non ha potuto verificare, fra cui che `business_case.md` §4 formuli `BQ2` come domanda sul quadrante, che `kpi_measures.md` §7.3 pubblichi `ALL ( dim_segment )`, e che il contratto della `008a` §5.3 dichiarasse davvero l'assenza del conteggio dei membri.
2. **L'esistenza e il contenuto degli identificativi di ancora** — nessun artefatto letto. Il revisore dichiara però di aver verificato la **coerenza interna fra i due documenti**: i venti identificativi che compaiono in entrambi «coincidono senza eccezioni. Non è poco, ma non è verifica contro la fonte».
3. **Le quattro issue** — non ha potuto giudicare se la chiusura condizionata di `#21` sia proporzionata al difetto che l'issue registra.
4. **Se le visuali reggano davanti allo schermo** — «la mia posizione non è migliore della sua».
5. **Se il `.pbix` contenga oggi qualcosa** — «non l'ho aperto nemmeno io e non ho modo di verificare quella dichiarazione, che peraltro è la dichiarazione giusta da fare».
6. **La stima in ore della `010b`** — non è in questo documento.
7. **Il verbale della revisione che ha respinto la dashboard a quattro pagine** — «se contenesse altri rilievi sulla `008b`, non posso sapere se questo disegno li chiuda».

---

*Fine del verbale del revisore. Il blocco che segue è di chi è stato revisionato e non fa parte della revisione.*
