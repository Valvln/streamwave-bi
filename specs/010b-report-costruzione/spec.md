# Feature Specification: il report che porta l'argomento a schermo — costruzione

**Feature Branch**: `010b-report-costruzione`

**Created**: 2026-08-29

**Status**: Draft

**Input**: User description: "Costruire il report a dieci pagine disegnato dal contratto di pagina della 010a, e scriverne la narrazione a schermo. Perimetro: sei misure DAX nuove (M1-M6), quattro visuali nuove più una quinta nuova come forma, quattro visuali riusate invariate, due pagine di sola prosa (3 e 10), navigazione persistente. Il contratto di narrazione si scrive prima di aprire Power BI. La visuale dichiarata non costruibile a §15 resta non costruita. Non si ridisegnano le pagine, non si ricalcola alcun KPI, non si pubblica il .pbix."

## Perché questa feature esiste

Nove feature hanno misurato, la `009` ha risposto, la `010a` ha disegnato. **Qui la risposta arriva davanti a una persona.**

È l'unica feature rimasta a toccare la GUI, ed è quella per cui tutto il resto è stato costruito. Il criterio di accettazione della constitution — *reggere la presentazione a un board reale* — non è soddisfatto da alcun artefatto di questo repository finché il report non esiste: `docs/raccomandazione.md` porta l'argomento su una pagina, e una pagina non è ciò che il principio IV chiede.

Il vincolo è [`specs/010a-report-disegno/contracts/page-contract.md`](../010a-report-disegno/contracts/page-contract.md), dieci pagine, revisionato in contesto pulito. **Il contratto dichiara che cosa deve esistere; questa feature accerta che cosa esiste.** Dove i due divergono prevale l'esito di questa feature, ed è il contratto stesso a stabilirlo (§7 del suo preambolo).

## Che cosa questa feature deve produrre

Due deliverable, e il secondo non è la descrizione del primo:

1. **il report a dieci pagine** dentro il `.pbix`, che **non è versionabile** e vive sul disco di Valerio;
2. **il contratto di narrazione** — `contracts/narrative-contract.md` — che porta il **testo letterale** a schermo. Esiste perché il `.pbix` non è versionabile: chi legge questo progetto da fuori non potrà aprirlo, e senza quel documento la prosa del report non esisterebbe nel repository.

Vi si aggiunge l'**esito della costruzione**, in `quickstart.md`, che è la fonte autorevole su ciò che esiste a schermo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — un decisore scorre dieci pagine e conclude qualcosa (Priority: P1)

Un decisore che non ha letto alcun documento di questo repository, che non è un tecnico, apre il report e scorre le pagine. Incontra la domanda, la risposta, su che cosa poggia, le tre condizioni una per volta, la regione da cui entrare, quanto vale, e che cosa lo ribalterebbe. **Alla fine sa che cosa può concludere** — non soltanto che cosa non può concludere.

**Why this priority**: è il metro su cui la `008b` è stata fermata e la `009` è passata. Il difetto nominato dalla revisione della `008b` è letterale: «trentadue blocchi dicono al lettore che cosa non concludere; nessuno gli dice che cosa può concludere». È l'issue [`#28`](https://github.com/Valvln/streamwave-bi/issues/28), e **si chiude qui o non si chiude**.

**Independent Test**: si prende il contratto di narrazione, si legge il testo di ciascuna pagina in sequenza senza il report davanti, e per ogni limite scritto si cerca l'affermazione positiva che gli sta accanto. Un limite senza il proprio permesso è un difetto.

**Acceptance Scenarios**:

1. **Given** il testo a schermo di una pagina qualunque, **When** vi compare un limite di ciò che i dati sostengono, **Then** sulla stessa pagina compare che cosa si può concludere nonostante quel limite.
2. **Given** il report aperto alla pagina iniziale, **When** il decisore la legge, **Then** trova a che cosa il report serve e che cosa risponde, non un elenco di cautele.
3. **Given** una pagina qualunque, **When** vi compare una sigla tecnica (`C1`, `C2`, `C3`, `BQ`), **Then** è sciolta sulla stessa pagina in cui compare, oppure non compare.
4. **Given** il report scorso dall'inizio alla fine, **When** si cerca la risposta alla domanda per cui l'analisi esiste, **Then** la si trova a pagina 2, prima di qualunque difesa dell'argomento.

---

### User Story 2 — ogni numero a schermo è il valore che l'artefatto pubblica (Priority: P1)

Chi verifica il report prende un numero qualunque a schermo, ne cerca l'ancora nel contratto di pagina, apre l'artefatto versionato e trova lo stesso valore. Nessun numero è stato digitato a mano in una visuale.

**Why this priority**: è il principio I, ed è la ragione per cui questo progetto esiste come portfolio. È anche il presidio che sulla `007b` ha trovato tre KPI sbagliati di **due ordini di grandezza** sotto un esito verde di ogni controllo del repository — l'issue [`#11`](https://github.com/Valvln/streamwave-bi/issues/11). Un report che sbaglia un valore senza che nulla lo segnali è peggiore di un report che non esiste.

**Independent Test**: per ciascuna delle sei misure nuove e per ciascun valore che una visuale porta, si confronta **una volta** la lettura dal motore con il `display` dell'ancora. Una divergenza è un ritrovamento da dichiarare, non un numero da accettare.

**Acceptance Scenarios**:

1. **Given** `M1`, `M4` e `M5`, **When** se ne legge il valore dal motore, **Then** coincide con `KPI.verdict.conditions_satisfied`, `KPI.BQ1K3.c2.margin` e `KPI.BQ1K3.c2.margin_share_of_value` rispettivamente.
2. **Given** una linea di riferimento a schermo — la mediana di pagina 4, le due soglie di pagina 7, la soglia di pagina 6 — **When** se ne cerca l'origine, **Then** è una misura letta dal modello e non una costante digitata nella visuale.
3. **Given** le tre impostazioni del modello dell'issue [`#20`](https://github.com/Valvln/streamwave-bi/issues/20), **When** il `.pbix` viene aperto, **Then** ciascuna è verificata prima che qualunque valore sia letto.

---

### User Story 3 — chi legge il repository da fuori trova la prosa del report (Priority: P2)

Chi clona il repository e non ha Power BI trova, nel contratto di narrazione, il testo letterale che sta a schermo, pagina per pagina, con l'indicazione di dove ciascun blocco va.

**Why this priority**: il `.pbix` non è versionabile. Senza questo documento la parte del deliverable che un lettore esterno può giudicare — la prosa — non esisterebbe nel repository. È il precedente della `008b`, ed è **la parte del suo lavoro che è sopravvissuta** alla revisione.

**Independent Test**: si apre il solo contratto di narrazione, senza il report, e si verifica che ogni blocco dichiari dove va, che cosa dice alla lettera, e da dove viene l'affermazione.

**Acceptance Scenarios**:

1. **Given** il contratto di narrazione, **When** lo si legge senza aprire il `.pbix`, **Then** il testo di tutte e dieci le pagine è presente alla lettera.
2. **Given** un blocco di testo del contratto, **When** se ne cerca l'origine, **Then** è dichiarata la sezione di documento pubblicato o il vincolo di contratto da cui discende.

---

### Edge Cases

- **Una visuale non regge davanti allo schermo.** È previsto dal disegno (§19 del contratto), non è un difetto. Lo scostamento si annota **mentre accade** e si elenca nell'esito con la propria ragione.
- **La sincronizzazione della selezione fra le pagine 7 e 8 non è ottenibile.** L'issue [`#21`](https://github.com/Valvln/streamwave-bi/issues/21) registra un accertamento precedente e **contrario**: Power BI non offre l'evidenziazione come modalità di risposta per una dispersione né per una tabella. Se non è ottenibile, `CP-3` non si acquisisce, l'issue resta aperta e diventa un ritrovamento.
- **Un valore letto dal motore diverge da quello pubblicato.** È un ritrovamento, si dichiara con nota in loco, e **non si corregge il KPI**: ricalcolare è fuori perimetro.
- **Il tempo non basta per dieci pagine.** Ciò che deve esistere è un **sottoinsieme di pagine complete**, non dieci pagine in bozza. La decisione su che cosa cade è di Valerio.

## Requirements *(mandatory)*

### Le sei misure nuove

- **FR-001**: il modello DEVE portare `M1` (`verdict_conditions_satisfied`), che conta quante delle tre condizioni sono soddisfatte, sul dominio `0-3`, componendo `c1_music_above_median`, `M2` e la companion di `C3`.
- **FR-002**: il modello DEVE portare `M2` (`c2_overlap_above_threshold`), la condizione `C2` come booleano, confrontando `mood_profile_overlap` con `M3`. **`M2` colma un'asimmetria del framework**: `C1` e `C3` hanno una companion booleana pubblicata, `C2` no.
- **FR-003**: il modello DEVE portare `M3` (`c2_threshold`), la soglia di `C2` esposta come misura invece che digitata, ancorata a `KPI.BQ1K3.c2.threshold`.
- **FR-004**: il modello DEVE portare `M4` (`c2_margin`), la distanza fra il valore misurato e la soglia.
- **FR-005**: il modello DEVE portare `M5` (`c2_margin_share_of_value`), il margine rapportato al valore misurato.
- **FR-006**: il modello DEVE portare `M6` (`arpu_uplift_per_100k`), la terna dell'uplift per ogni `100.000` abbonati, per un fattore dichiarato come **unità** e non come stima di una base. Se portare quei tre valori come colonne della tabella disconnessa risultasse più semplice, è equivalente e va dichiarato nell'esito.
- **FR-007**: la lettura dal motore di `M1`, `M4` e `M5` DEVE essere confrontata **una volta** con il valore che `reports/kpi_measures.json` pubblica. Una divergenza è un ritrovamento da dichiarare, non un numero da accettare.
- **FR-008**: nessuna delle sei misure DEVE ricalcolare un KPI o riaprire un operatore fissato.

### Le pagine

- **FR-009**: il report DEVE portare **dieci** pagine, nell'ordine e con i titoli della mappa di §1 del contratto di pagina, pagina iniziale compresa nel conteggio.
- **FR-010**: ciascuna pagina DEVE portare gli elementi che il contratto le assegna, con le visuali del tipo dichiarato e i valori con l'ancora dichiarata.
- **FR-011**: nessuna pagina DEVE offrire un'interazione che il contratto elenca fra quelle non offerte. In particolare, **nessun filtro** che produca un valore a una grana diversa da quelle pubblicate.
- **FR-012**: ogni valore a schermo DEVE portare le etichette di fonte e confidenza nella forma di `business_case.md` §5.4, su ogni pagina e senza eccezioni. La pagina 2 porta **una sola** etichetta, quella del verdetto.
- **FR-013**: le pagine 3 e 10 DEVONO essere di **sola prosa** e portare un'articolazione visibile fra le parti. Nessuna visuale vi si aggiunge per riempirle. In particolare, **nessuna barra dei rischi ordinata per gravità** a pagina 10.
- **FR-014**: la visuale dichiarata non costruibile a §15 del contratto — le tracce del catalogo musicale come nube sui tre assi — **NON DEVE** essere costruita.
- **FR-015**: le quattro visuali riusate (`008a`) DEVONO cambiare pagina e **non forma**.
- **FR-016**: la dispersione di pagina 5 DEVE dichiarare a schermo l'**asse escluso** e la versione della tabella di mood (`conventions.kpi_mood_table_version`).
- **FR-017**: le tre marcature della dispersione di pagina 7 — quadrante, domanda non misurata, resto — DEVONO restare distinguibili fra loro.
- **FR-018**: la tabella di pagina 8 DEVE portare la quota di zeri nella colonna **immediatamente adiacente** alla domanda, e i sette segmenti a domanda non misurata in un blocco proprio **senza colonna di posizione**, ordinati alfabeticamente.
- **FR-019**: il report DEVE portare una barra di navigazione **persistente su tutte e dieci le pagine**, interna al report, con un solo passaggio fra due pagine qualunque e l'ordine delle dieci pagine visibile.

### La narrazione

- **FR-020**: il contratto di narrazione DEVE essere scritto e **approvato prima** che Power BI venga aperto.
- **FR-021**: il contratto di narrazione DEVE portare il testo **letterale**, non la sua descrizione, con per ciascun blocco: dove va, che cosa dice, da dove viene.
- **FR-022**: ogni limite scritto a schermo DEVE stare accanto a **ciò che si può concludere nonostante quel limite**. È la chiusura dell'issue `#28`.
- **FR-023**: il testo a schermo DEVE essere leggibile da un decisore che non ha letto alcun documento del repository e non è un tecnico: nessun gergo non sciolto, nessun rimando a documenti che il lettore non ha, nessuna frase che abbia bisogno di una seconda frase altrove per non essere fraintesa.
- **FR-024**: il testo a schermo **NON DEVE** usare la formulazione «l'uplift non è scalabile», che `bq3_scenarios.md` §8 dichiara falsa. Usa la formulazione **stretta** di `raccomandazione.md` §4.
- **FR-025**: il testo a schermo DEVE dichiarare, dove i numeri di `BQ3` compaiono, il **debito della `004`** sulla verificabilità del benchmark.
- **FR-026**: i valori di `BQ3` **NON DEVONO** comparire isolati, nemmeno in una frase di sintesi: sempre come terna.
- **FR-027**: i nove rilievi dell'issue [`#29`](https://github.com/Valvln/streamwave-bi/issues/29) DEVONO essere riletti **prima** di scrivere, come catalogo dei modi in cui la prima narrazione ha fallito. Non si correggono: il testo si riscrive da zero.

### Le verifiche del modello

- **FR-028**: le tre impostazioni dell'issue `#20` DEVONO essere riverificate all'apertura del `.pbix`, leggendo l'issue e non una copia. L'issue **non si chiude**: un esito positivo oggi non prova un vincolo per sempre.
- **FR-029**: il modello DEVE essere accertato portare i sei valori di scenario da `reports/bq3_scenarios.json` come **tabella disconnessa**, senza relazione con il resto del modello.
- **FR-030**: se una pagina del disegno esponesse un filtro di categoria video, la formula di `mood_profile_overlap` (issue [`#18`](https://github.com/Valvln/streamwave-bi/issues/18)) DEVE essere chiusa prima. Il contratto dichiara che il difetto non si manifesta nelle pagine disegnate; la verifica è di questa feature.

### Gli esiti e il repository

- **FR-031**: l'esito della costruzione DEVE dichiarare quali pagine esistono e in quale stato, gli scostamenti dal contratto ciascuno con la propria ragione, e i ritrovamenti.
- **FR-032**: gli scostamenti DEVONO essere annotati **mentre accadono**. Uno scostamento ricostruito a posteriori è una razionalizzazione.
- **FR-033**: il [README](../../README.md) DEVE essere allineato: riga nella tabella di stato, deliverable elencato, prosa dei deliverable estesa, `Setup` e `Struttura`.
- **FR-034**: il controllo di coerenza DEVE essere verde sui documenti che questa feature pubblica o modifica.
- **FR-035**: la revisione in contesto pulito DEVE produrre `review.md` con i quattro obblighi di [CLAUDE.md](../../CLAUDE.md), e il verbale si trascrive **integralmente**.

### Che cosa questa feature non fa

- **FR-036**: **NON** ridisegna le pagine, non cambia l'ordine, non ne aggiunge né toglie. Uno scostamento si **dichiara**, non si esegue in silenzio.
- **FR-037**: **NON** ricalcola alcun KPI e **NON** riapre un operatore fissato.
- **FR-038**: **NON** modifica `docs/raccomandazione.md` né `docs/roadmap.md`.
- **FR-039**: **NON** pubblica il `.pbix` sul servizio.
- **FR-040**: **NON** chiude l'arretrato del tracker, che spetta alla `011`.
- **FR-041**: **NON** scrive in `data/raw/` né in `data/processed/`.
- **FR-042**: **NON** corregge `docs/kpi_operators.md` §9 né il contratto della `008a` §8 (issue `#26` e `#31`), che restano aperte.

## Success Criteria *(mandatory)*

- **SC-001**: un decisore che non ha letto alcun documento del repository scorre il report e sa dire, alla fine, **quale sia la risposta e a quali condizioni regge** — senza consultare `docs/`.
- **SC-002**: ogni limite scritto a schermo ha, sulla stessa pagina, l'affermazione positiva che gli sta accanto. **Zero limiti orfani** è l'esito atteso.
- **SC-003**: ogni numero a schermo coincide con il `display` dell'ancora che il contratto di pagina gli assegna. Ogni divergenza è dichiarata come ritrovamento.
- **SC-004**: dalle dieci pagine si raggiunge ogni altra pagina con **un solo passaggio**, tramite elementi interni al report.
- **SC-005**: il testo a schermo delle dieci pagine esiste **alla lettera** nel repository, leggibile senza aprire il `.pbix`.
- **SC-006**: le quattro decisioni di §18 del contratto di pagina hanno un esito dichiarato, `CP-3` incluso, e la chiusura condizionata dell'issue `#21` è risolta in un senso o nell'altro.
- **SC-007**: nessuna interazione del report produce un valore a una grana che nessun artefatto pubblica.

## Assumptions

- **A-1**: il `.pbix` della `008` esiste sul disco di Valerio e porta il modello, le misure pubblicate, le due soglie di `F7` e le due companion di `CP-1`. Questa feature vi **aggiunge** e non ricostruisce il modello da zero. Se il file non fosse disponibile, è un blocco da riportare, non da aggirare.
- **A-2**: il report **sostituisce** la dashboard a quattro pagine della `008`. Le quattro pagine vecchie non sopravvivono accanto alle dieci nuove: sarebbero due artefatti che rispondono alla stessa domanda in modo diverso.
- **A-3**: la scelta della coppia di assi di mood per la dispersione di pagina 5 è di chi costruisce (§19). La ricognizione ha accertato che gli estremi pubblicati sono **identici sui tre assi**, quindi la scelta non cambia la forma dell'inviluppo.
- **A-4**: le misure nuove sono venti in totale nel modello — dieci pubblicate, due soglie di `F7`, due companion di `CP-1` della `008a`, sei nuove — come `CP-2` dichiara.

## Dipendenze e debito ereditato

| Origine | Che cosa questa feature ne fa |
|---|---|
| contratto di pagina della `010a` | è il vincolo. Si esegue; gli scostamenti si dichiarano |
| issue `#28` | **si chiude qui o non si chiude**: la resa a schermo è di questa feature |
| issue `#29` | si chiude rileggendo i nove rilievi **prima** di scrivere, non correggendo il vecchio testo |
| issue `#33` | si chiude davanti allo schermo: quale comportamento la pagina 8 ha quando riceve la selezione dalla 7 |
| issue `#21` | si chiude **solo** se la sincronizzazione è ottenibile senza ricalcolare valori. Esiste un accertamento precedente contrario |
| issue `#20` e `#11` | le verifiche si rifanno; le issue **restano aperte** |
| issue `#18` | si chiude **prima** solo se una pagina del disegno esponesse un filtro di categoria |
| issue `#26` e `#31` | non si chiudono; il testo di questa feature non ripete la formulazione esclusa |
| debito della `004` | resta aperto e **va dichiarato a schermo** dove i numeri di `BQ3` compaiono |

## Key Entities

- **Pagina**: una delle dieci schermate, con un titolo, una parte dell'argomento che porta, le proprie visuali, i propri valori ancorati, il proprio spazio riservato al testo, e le proprie interazioni non offerte.
- **Misura**: un'espressione DAX nel modello. Sei sono nuove e nessuna calcola un KPI.
- **Blocco di narrazione**: un'unità di testo a schermo, con la propria collocazione, il proprio testo letterale e la propria origine.
- **Scostamento**: una divergenza fra ciò che il contratto prescrive e ciò che esiste, con la propria ragione, annotata mentre accade.
- **Ritrovamento**: un difetto o una divergenza scoperti costruendo, che questa feature dichiara e non necessariamente corregge.
