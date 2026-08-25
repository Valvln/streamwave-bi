# Verbale di revisione — feature `008a`

**Data**: 2026-08-25 · **Oggetto**: il contratto di pagina e l'esito della costruzione della `008a`

## Come la revisione è stata condotta

**Configurazione**: subagent isolato, avviato con accesso a una cartella temporanea contenente **due soli file** e nessun altro. Non ha ricevuto la spec, il piano, i task, la roadmap, la constitution, la history git, né alcuno dei documenti sotto `docs/`. Non ha ricevuto il nome della feature né il contesto del progetto oltre a due frasi: che i documenti appartengono a un progetto di Business Intelligence in italiano, che il primo è il disegno di una dashboard scritto prima di aprire lo strumento e il secondo dichiara che cosa è stato costruito, e che sono destinati a lettori esterni che non possono aprire il file della dashboard.

**Vincolo di perimetro dato al revisore**: leggere solo quei due file; non uscire dalla cartella; non seguire i collegamenti relativi, che puntano a documenti non forniti; annotare come rilievo — non risolvere — ogni fonte non verificabile.

### Che cosa è stato revisionato

| File dato al revisore | Origine | Impronta `sha256` |
|---|---|---|
| `documento-1-contratto-di-pagina.md` | `specs/008a-dashboard-model-pages/contracts/page-contract.md`, copia integrale | `33da87fee9d938b67988acec14ac9ebc28a334a62945cd47573fbe969c148200` |
| `documento-2-esito-della-costruzione.md` | `specs/008a-dashboard-model-pages/quickstart.md`, dalla sezione «Esito della costruzione» alla fine | `7d2f6d067ce4e2d6135c65a06c25ca8f3dc55f3d3371120c9be6d906af3e04f9` |

**Ancoraggio**: commit `ccdfd09` per il contratto di pagina, invariato dalla sua approvazione. Il secondo documento è stato revisionato **allo stato dell'albero di lavoro** al 2026-08-25, non a un commit: le impronte qui sopra sono quindi l'ancora forte, il commit quella debole. È una deviazione dall'obbligo 3 di `CLAUDE.md`, dichiarata invece che taciuta.

### Che cosa non è stato revisionato

Il `.pbix`, che è il deliverable. Nessuno script e nessun subagent può aprirlo, ed è la ragione per cui l'oggetto della revisione sono i due documenti che lo rendono ispezionabile. Ne discende che i rilievi `R2`, `R5`, `R9` e `R25` riguardano ciò che il testo dichiara, non ciò che è stato costruito — il revisore lo dichiara esplicitamente in chiusura.

---

## I rilievi, come il revisore li ha formulati

Trascritti senza modifiche di sostanza. Le citazioni sono quelle scelte dal revisore.

### `R1` — bloccante

> «La sezione si chiude a zero, ed è l'esito atteso: questa feature non ha ricalcolato nulla, ha portato a schermo valori già verificati contro il motore dalla `007b`.» (documento 2, *I ritrovamenti*)

Lo stesso documento, tre paragrafi più sotto, racconta che il modello caricava `dim_title` con righe in eccesso e che quelle spurie «sarebbero entrate nella mediana dei film di `format_duration_gap` e nei conteggi per categoria della North Star, cambiando due valori pubblicati». Se quella materializzazione è la stessa che la `007b` aveva verificato contro il motore — e il documento 1 (`CP-2`) afferma che il `.pbix` esisteva già ed era stato letto dal motore — allora o quella verifica non copriva i due valori, o la coincidenza allora registrata non reggeva. Il documento non riconcilia i due fatti e usa la verifica della `007b` come ragione per cui zero ritrovamenti è «l'esito atteso»: è la premessa su cui poggia il risultato principale dell'intero esito, ed è la premessa che il documento stesso incrina.

### `R2` — sostanziale

> «È la proprietà che rende la pagina interattiva senza renderla bugiarda, e va riverificata a schermo (prova 9).» (documento 1, §2.1) · «9 — nessuna interazione a grana non pubblicata | T028-T030 | conforme; interazione fra le due visuali di `BQ2` disattivata» (documento 2)

Il contratto chiede che la prova 9 riverifichi a schermo che soglie e posizioni non si muovono alla selezione di un segmento. Disattivando l'interazione, quella verifica non è più eseguibile: l'esito la dichiara «conforme» senza dire che l'oggetto della verifica è venuto meno. Una prova il cui presupposto è stato rimosso non è una prova superata.

### `R3` — sostanziale

> «**Nessuno.** Gli otto valori letti a schermo coincidono con quelli pubblicati…» (documento 2, *I ritrovamenti*) · «l'esclusione non è più vera. È lo stesso caso di §3.4 e §7.1 — il documento canonico resta indietro rispetto al modello» (documento 2, *L'esito delle prove 2 e 11*)

Il documento accerta che un artefatto pubblicato contiene oggi tre affermazioni non più vere, e archivia la sezione dei ritrovamenti a zero. La parentesi che segue esclude esplicitamente solo i difetti di caricamento, il che fa leggere la tassonomia come esaustiva: un lettore esterno conclude che nulla è stato trovato, mentre qualcosa lo è stato.

### `R4` — sostanziale

> «| **BQ2 — Segmento di ingresso** | `BQ2-K1`, `BQ2-K2`, `BQ2-K3` | `segment_demand_index`, `segment_zero_share`, `segment_catalog_affinity`, `segment_entry_priority_score`, …» (documento 1, §1) · «| `BQ2-K3` | `Fonte: Derivato (BQ2-K1 + BQ2-K2) · Confidenza: media` |» (§1.1)

Nessuno dei due documenti dichiara mai quale identificativo di KPI corrisponda a quale misura su `BQ2`: sei misure per tre KPI, e il lettore deve indovinare. Se `BQ2-K2` è `segment_zero_share`, l'etichetta di fonte pubblicata è sbagliata; se è `segment_catalog_affinity`, allora `segment_zero_share` è un valore a schermo che non è un KPI — e a differenza della quota di titoli `Movie`, per cui il documento dichiara esplicitamente che non è un KPI, per la quota di zeri quella dichiarazione non esiste. Il lettore non può decidere, e una delle due letture rende falso un valore pubblicato.

### `R5` — sostanziale

> «**La quota di zeri è adiacente alla domanda per obbligo, non per comodità** (`D7`, `FR-015`)… Separarle in due colonne distanti, o renderne una nascondibile dall'utente, ricrea il difetto che la separazione esisteva per impedire.» (documento 1, §5.2)

L'esito non ne parla mai: la riga `BQ2` elenca «graduatoria completa dei 114 segmenti», nessuna delle dodici prove ha per oggetto l'adiacenza o la non nascondibilità, e la quota di zeri non compare in tutto il documento 2. Un obbligo dichiarato non verificabile è un obbligo che il lettore deve dare per soddisfatto sulla parola.

### `R6` — sostanziale

> «**Che cosa chiede**: che T013 accerti in quale forma il `.pbix` li porta oggi. Se sono digitati, il passaggio alla lettura dell'artefatto è un miglioramento e va registrato come tale» (documento 1, §9, `CP-2`)

L'esito non registra la risposta: non dice in quale forma i sei valori stavano nel `.pbix` prima, quindi non dice se ciò che è avvenuto sia un miglioramento o un non-evento. La verifica richiesta risulta chiusa senza essere stata riportata.

### `R7` — sostanziale

> «La loro domanda mediana è nulla: nella dispersione cadono tutti contro il bordo sinistro… Sono `country`, `iranian`, `jazz`, `latin`, `rock`, `romance`, `soul`.» (documento 1, §5.1)

Tre affermazioni misurate senza ancora: che la mediana di quei segmenti sia *nulla*, che *tutti e sette* cadano contro il bordo sinistro, e la composizione stessa dell'elenco. La citazione di `kpi_measures.md` §5.3 sostiene la *lettura* del flag, non i valori.

### `R8` — sostanziale

> «| segmento | `BQ2-K1`, `BQ2-K2`, `BQ2-K3` | il segmento, per tutti e 114 | · | scenario | `BQ3-K1`, `BQ3-K2` | lo scenario, per tutti e tre — mai riducendo a uno solo |» (documento 1, §2)

La riga «scenario» è incoerente con sé stessa: restringere «per tutti e tre» senza mai ridurre a uno solo non è una restrizione, e §6.1 non offre comunque alcuno slicer. La riga «segmento» promette una selezione che §5.4 non concede e che l'esito registra come assente. Un lettore esterno legge questa colonna come l'elenco di ciò che potrà fare, e non potrà farne nulla.

### `R9` — sostanziale

> «Power BI non offre l'evidenziazione come modalità di risposta né per una dispersione né per una tabella, e l'unica alternativa disponibile è il filtro» (documento 2, *Gli scostamenti*)

Affermazione universale sul comportamento di uno strumento, data come fatto accertato, senza fonte né descrizione di come sia stata accertata — e regge da sola uno scostamento dal contratto e l'apertura di una issue. La stessa forma ricorre nello scostamento su T024. Chi legge non può verificarle e non gli viene detto chi le ha verificate.

### `R10` — sostanziale

> «Trascritto qui perché il `.pbix` non è versionato: senza questo blocco le due colonne esisterebbero solo dentro un file che nessuno può leggere dal repository.» (documento 2)

La ragione vale identica per le quattro misure che questa feature ha scritto, il cui testo DAX non compare da nessuna parte nel documento. Il lettore riceve la forma esatta di ciò che non calcola nulla di nuovo e nessuna forma di ciò che produce due valori a schermo.

### `R11` — sostanziale

> «**Perimetro accertato**: è l'unico dei quattro file di `data/processed/` in cui record CSV e righe fisiche divergono. Le altre sei tabelle tornavano già prima della correzione, e la ragione è questa.» (documento 2)

Il modo in cui l'unicità è stata accertata non è dichiarato, e il documento afferma altrove che «nessuno script di questo repository entra nel modello». In più il conto non si segue: quattro file e sei altre tabelle, con una corrispondenza che nessuno dei due documenti descrive — quindi l'inferenza «e la ragione è questa» non è ricostruibile.

### `R12` — sostanziale

Convivono due numerazioni delle verifiche, `★n` e «prova n», che non coincidono (★1 = prova 2, ★3 = prova 11) e che nessuno dei due documenti mette in relazione. `★2` è citato in apertura e non compare mai altrove. Il documento 1 usa `(★3)` in §5.1 senza definirlo. Un lettore esterno non può contare le verifiche né sapere se ne manchi una.

### `R13` — sostanziale

> «**Da compilare nel blocco B**, dopo ★2 e ★3… «Le pagine che esistono» vuota significa che la costruzione non è iniziata.» (documento 2, blocco di apertura)

Il documento si apre dichiarandosi da compilare e spiegando come leggerne le parti vuote, mentre il corpo riporta una costruzione conclusa e nessuna voce vuota. È istruzione di compilazione rimasta nel testo pubblicato: chi lo riceve come resoconto autorevole comincia leggendo che non esiste ancora.

### `R14` — sostanziale

Entrambi i documenti poggiano su almeno sei sistemi di sigle mai sciolti — `FR-nnn`, `Fn`, `Dn`, `CPn`, `Tnnn`, `★n`, `En`, `An` — e su rimandi a `tasks.md`, `plan.md`, `research.md`. Il documento 1 dichiara di essere destinato a chi non può aprire la dashboard; nessuno dei due dichiara che il lettore debba avere il resto del repository, e senza quello buona parte delle giustificazioni è illeggibile.

### `R15` — minore

> «**Stato**: **da approvare** (punto di fermata 3)» (documento 1) · «### Gli scostamenti dal contratto approvato» (documento 2)

Un contratto ancora marcato «da approvare» e un esito che elenca scostamenti da «il contratto approvato». Manca la traccia dell'approvazione, che è ciò che rende gli scostamenti scostamenti e non semplici cambi di idea.

### `R16` — minore

> «`kpi_operators.md` §7.3, `data_model.md` §19 e la nota di adozione di `business_case.md` §4 lo chiamano tutti e tre **un problema della dashboard**» (documento 1, §5)

`kpi_operators.md` compare qui una sola volta; ovunque altrove §7.3 è attribuita a `kpi_measures.md`. Analogamente convivono `data-model.md` e `data_model.md`: il lettore non può sapere se siano uno o due artefatti. Sono le fonti di un'affermazione portante.

### `R17` — minore

La mappa di §1 è dichiarata come l'elenco di ciò che ogni pagina legge, ma omette le misure che le sezioni successive aggiungono: la companion della quota di titoli `Movie` su `BQ1`, `C3` e le due soglie su `BQ2`. La tabella che dovrebbe essere la sintesi è l'unica parte del contratto che non tiene conto di `CP-1` e `F7`.

### `R18` — minore

La tabella dei formati di §1.2 copre gli otto KPI e nessun altro valore, ma sullo schermo compaiono anche la quota di titoli `Movie` e la quota di zeri, entrambe quote per cui il formato conta esattamente per la ragione dichiarata in apertura di sezione.

### `R19` — minore

> «| navigazione | tre elementi cliccabili verso `BQ1`, `BQ2`, `BQ3` |» (documento 1, §3) · «Una barra di navigazione **persistente su tutte e quattro le pagine**, con quattro elementi» (§7)

Tre o quattro elementi sulla pagina di ingresso. Probabilmente conciliabile, ma il documento non lo dice, e il documento 2 eredita l'ambiguità.

### `R20` — minore

> «Le tabelle nel modello sono quindi otto invece delle sette di data-model.md §1.1, e le relazioni restano cinque.» (documento 2)

Il numero delle relazioni compare qui per la prima e unica volta in entrambi i documenti, senza ancora propria: il rinvio a §1.1 copre le sette tabelle, non le cinque relazioni.

### `R21` — minore

> «Tre impostazioni… **si sono già rivelate perdibili**: la tipizzazione delle colonne di mood (`#11`)…» (documento 2)

Delle tre, la prima è quella che lo stesso documento registra come «difetto assente» in questa materializzazione. Che sia stata persa in passato può essere vero, ma il documento non lo dice da nessuna parte.

### `R22` — minore

> «alla chiusura **va aperta** una issue analoga» · «Aperta come **`#20`**»

Il documento dice in un punto che l'issue è da aprire e in un altro che è aperta, con numero e data. Sono due stati diversi dello stesso documento lasciati entrambi nel testo.

### `R23` — minore

> «| 12 — la regola della North Star non compare | T031 | conforme |» (documento 2)

L'enunciato non è comprensibile: quale regola, e che cosa significa che «non compare». Nessuno dei due documenti contiene un antecedente. È l'unica delle dodici righe che non si lascia leggere.

### `R24` — minore

> «Nessuna di queste fasce contiene testo alla chiusura di questa feature… il `.pbix` è **leggibile, non pubblicabile**.» (documento 1, §8)

È l'affermazione più consequenziale del contratto per chi deve decidere che cosa fare del file, e l'esito non la conferma né la smentisce. Un lettore che si fermi al documento 2 non sa che ciò che è stato costruito non è pubblicabile.

### `R25` — minore

> «**Nessun tooltip di questa dashboard espone una misura**» (documento 1, §3.1)

Divieto formulato sull'intera dashboard, non sulla sola pagina di ingresso in cui si trova. L'esito non dichiara mai che i tooltip siano stati esaminati. Un «nessuno» esteso a quattro pagine resta senza riscontro.

---

## Dichiarazione di perimetro del revisore

Trascritta dalla chiusura della revisione.

> Ho letto per intero e una sola volta i due file indicati, nella cartella isolata. Non sono uscito dal perimetro: non ho aperto altri file, non ho elencato il contenuto della cartella oltre ai due percorsi che mi sono stati dati, non ho cercato nel repository, non ho letto history git e non ho seguito alcun collegamento relativo. Non ho tentato di farlo in nessun momento.
>
> Di conseguenza **non ho potuto verificare nulla di ciò che i documenti citano come fonte**: `business_case.md`, `kpi_measures.md` (né `kpi_operators.md`), `data-model.md`/`data_model.md`, `plan.md`, `tasks.md`, `research.md`, `roadmap.md`, la constitution, `reports/bq3_scenarios.json`, i file di `data/processed/` e le issue `#11`, `#18`, `#20`, `#21`. Tutti i valori ancorati a quelle fonti — i 114 segmenti, i 33 membri del quadrante, gli 8807 record attesi, i sette segmenti `is_high_zero_genre`, le dieci misure pubblicate, le sette tabelle, le cinque relazioni — li ho potuti controllare **solo per coerenza reciproca fra i due documenti**, non per corrispondenza al valore pubblicato. Su questo piano interno i conti tornano: 8807 + 2 = 8809; dieci misure pubblicate + due soglie + due companion = quattordici; sette tabelle + una disconnessa = otto; otto KPI ripartiti 1/3/3/2 sulle quattro pagine con l'unica ripetizione dichiarata; sette segmenti marcati nel documento 1 e sette contati nel documento 2. Non ho potuto verificare nulla di ciò che riguarda il `.pbix`, che i documenti stessi dichiarano non versionato e non leggibile dal repository — ed è la ragione per cui i rilievi R2, R5, R9 e R25 restano rilievi su ciò che il testo dichiara, non sul costruito.

---

## Blocco di chiusura — scritto dalla parte revisionata, 2026-08-25

Aggiunto in coda. **Il testo del revisore qui sopra non è stato toccato**, nemmeno dove un rilievo è stato giudicato non accolto: un verbale riscritto da chi è stato revisionato non è più un verbale.

**Come è stata applicata la soglia.** Si chiudono qui i soli rilievi per cui il deliverable, senza la correzione, **afferma il falso o si contraddice**. Tutto il resto è rinviato al tracker, e il rinvio è una decisione dichiarata come tale — non un rilievo lasciato cadere.

### Risolti

| Rilievo | Come | Dove |
|---|---|---|
| `R1` | l'esito non poggia più sulla verifica della `007b` ma su `T023`, il confronto diretto fra schermo e valori pubblicati fatto **dopo** la correzione dei difetti di caricamento. Riancorato, non riformulato | `quickstart.md`, *I ritrovamenti* |
| `R3` | la parentesi dichiara ora tutte e tre le categorie — ritrovamenti, difetti di caricamento, aggiunte — e afferma che insieme esauriscono ciò che la feature ha trovato | `quickstart.md`, *I ritrovamenti* |
| `R4` | aggiunta la tabella KPI ↔ misura per `BQ2`, con la dichiarazione esplicita che `segment_zero_share` non è un KPI e non porta etichette | `page-contract.md` §1 |
| `R8` | le tre righe della tabella delle grane dicono ora **nulla**, che è la verità: nessuna pagina offre un filtro. Corretta anche la riga gemella in `data-model.md` §1.4, che portava lo stesso difetto | `page-contract.md` §2, `data-model.md` §1.4 |
| `R13` | il blocco di apertura non dichiara più la sezione da compilare e dice invece che è completa e che è la fonte autorevole su ciò che esiste | `quickstart.md` |
| `R15` | lo stato del contratto dichiara data di approvazione e che cosa è stato approvato | `page-contract.md`, intestazione |
| `R21` | dichiarato che la tipizzazione si perse durante la `007b` — è l'origine dell'issue `#11` — e che ★1 è un esito di oggi, non una garanzia | `quickstart.md`, *Le issue* |
| `R22` | rimossa la formulazione «va aperta»: l'issue `#20` esiste, e i due punti che la citano lo dicono entrambi | `quickstart.md` |

### Indeboliti

Nessuno. Nessuna delle otto correzioni ritira una rivendicazione: `R1` sostituisce un'ancora debole con una più forte già disponibile, e le altre sette rimuovono contraddizioni o aggiungono ciò che mancava.

### Rinviati

Diciassette rilievi, raggruppati in quattro issue. Il raggruppamento è una scelta: diciassette issue separate sarebbero un arretrato che nessuno rilegge, e i rilievi di ciascun gruppo si chiudono con la stessa passata di lavoro. **Ogni rilievo è nominato dentro la propria issue**, così che nessuno sparisca senza numero.

| Issue | Rilievi | Tema |
|---|---|---|
| [`#22`](https://github.com/Valvln/streamwave-bi/issues/22) | `R2`, `R5`, `R6`, `R24`, `R25` | obblighi del contratto che l'esito non riporta come verificati. Si chiudono con una passata di verifica a schermo, non riscrivendo il testo |
| [`#23`](https://github.com/Valvln/streamwave-bi/issues/23) | `R7`, `R9`, `R11` | affermazioni date come accertate senza dire come e da chi |
| [`#24`](https://github.com/Valvln/streamwave-bi/issues/24) | `R12`, `R14`, `R16`, `R19`, `R23` | leggibilità per il lettore esterno: sigle mai sciolte, due numerazioni delle verifiche, nomi di file incoerenti |
| [`#25`](https://github.com/Valvln/streamwave-bi/issues/25) | `R10`, `R17`, `R18`, `R20` | completezza della mappa, dei formati e del DAX trascritto |

**`R9` merita una nota**, perché è il rilievo che questa feature meno può chiudere da sola: l'affermazione contestata — che Power BI non offra l'evidenziazione per dispersione e tabella — è vera per quanto chi ha costruito ha potuto accertare, ma è stata accertata provando, non consultando una fonte citabile. Rinviarla è la risposta onesta: dichiararla verificata sarebbe esattamente ciò che il rilievo contesta.

**Nessun rilievo è stato giudicato infondato.** I diciassette rinviati sono tutti riconosciuti; ciò che li distingue dagli otto chiusi è che nessuno di essi rende falso ciò che il deliverable afferma.
