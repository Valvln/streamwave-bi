# Research: Dashboard — modello, pagine, misure a schermo

**Feature**: 008a-dashboard-model-pages | **Data**: 2026-08-24

## Perché questo documento è corto

Il Technical Context di [plan.md](./plan.md) non contiene alcun `NEEDS CLARIFICATION`: le nove decisioni `F1`-`F9` sono già argomentate per intero in [spec.md](./spec.md), approvata dalla regia il 2026-08-24. Questo file le consolida nel formato Decisione/Motivazione/Alternative richiesto dalla Fase 0, con puntatore alla sezione di spec che le argomenta per esteso.

**Che cosa distingue questa Fase 0 dalle precedenti.** Nella `007a` le decisioni sceglievano fra letture alternative di una formula; nella `007b` fra modi di tradurre una formula in codice verificabile. Qui **quasi tutte scelgono fra modi di mostrare un numero già fissato**, e ne discende una differenza che vale la pena nominare: una decisione sbagliata non produce un valore sbagliato, produce un valore giusto letto male. È una classe di difetto che nessun controllo di questo repository può intercettare, perché il numero resta identico all'artefatto che lo genera — e per la quale l'unico presidio disponibile è che il disegno sia scritto prima e letto da chi non l'ha scritto.

**Due decisioni fanno eccezione e non riguardano la presentazione**: `F1`, che riguarda il processo, e `F7`, che riguarda la provenienza di due numeri che finiscono a schermo.

## Le nove decisioni, in formato Fase 0

### F1 — Tre fasi e un terzo punto di fermata

- **Decisione**: contratto di pagina (sessione) → approvazione (Valerio) → costruzione manuale (Valerio) → riporto e chiusura (sessione). Il punto di fermata sta fra il contratto e la costruzione.
- **Motivazione**: è il punto di massima leva. Un errore di disegno costa una rilettura se trovato nel contratto, e di rifare pagine se trovato a schermo — la stessa asimmetria che `E9` della `007b` ha reso concreta con due letture contro il costo di rifare le pagine di questa feature.
- **Alternative scartate**: istruzioni passo-passo eseguite senza approvazione intermedia (il disegno e la sua esecuzione diventano la stessa decisione presa due volte dalla stessa persona); costruzione a intuito documentata a posteriori (produce una documentazione che ratifica invece di vincolare — la stessa forma che la condizione 1 delle assegnazioni dell'analista vieta per i valori).
- **Riferimento**: spec.md, `F1`.

### F2 — La regola di invarianza a schermo

- **Decisione**: un valore a schermo dev'essere un valore pubblicato da `docs/kpi_measures.md`, alla grana a cui quel documento lo pubblica. Le grane pubblicate sono tre: catalogo intero, segmento, scenario. Nessuna pagina offre un'interazione che produca un valore di KPI a una grana diversa.
- **Motivazione**: neutralizza l'issue `#18` al costo di una riga di contratto, e copre un insieme di rischi più largo dell'`ALL` mancante — il filtro di categoria su `BQ1-K3` è il caso noto, non necessariamente l'unico.
- **Alternative scartate**: correggere la formula DAX aggiungendo l'`ALL` (modificherebbe un artefatto già mergiato, verificato contro il motore, per rendere possibile un'interazione che questa feature ha comunque deciso di non offrire); fare entrambe le cose (stesso costo del solo (a), stesso guadagno del solo (b)).
- **Che cosa non chiude**: l'issue `#18` resta aperta. Questa feature dimostra che il difetto non si manifesta nelle pagine costruite, non che non esista.
- **Riferimento**: spec.md, `F2`.

### F3 — Quadrante più graduatoria completa per i 114 segmenti

- **Decisione**: dispersione domanda × affinità con le due soglie come linee di riferimento, visuale primaria della pagina `BQ2`; graduatoria completa dei 114 segmenti sulla stessa pagina, con la quota di zeri accanto alla domanda e l'avvertimento accanto ai sette segmenti `is_high_zero_genre`.
- **Motivazione**: `business_case.md` §4 formula `BQ2` come una domanda sul quadrante, e una dispersione con due soglie è la forma in cui quella domanda si legge su 114 punti. L'appartenenza al quadrante è inoltre un booleano già pubblicato per ogni segmento: la visuale mostra ciò che l'artefatto contiene.
- **Alternative scartate**: le prime *N* posizioni (nasconderebbero i sette segmenti a mediana nulla, tutti oltre la posizione 96, e con essi l'avvertimento di `kpi_measures.md` §7.4 — è l'opzione scartata con la ragione più netta); la sola tabella completa con ricerca (non risponde alla domanda di business, ma resta necessaria accanto alla dispersione, che mostra i punti e non i nomi).
- **Chiude**: il vincolo che `data_model.md` §19, `kpi_operators.md` §7.3 e la nota di adozione su `business_case.md` §4 assegnano tutti e tre alla dashboard.
- **Riferimento**: spec.md, `F3`.

### F4 — `BQ3` solo come intervallo a tre scenari

- **Decisione**: i due KPI di `BQ3` compaiono come tre valori affiancati con le rispettive unità, mai come scheda singola; nessuna visuale li moltiplica per una base utenti, una durata o altro.
- **Motivazione**: il principio I lo impone per la confidenza bassa, ed è l'unico punto in cui un principio non negoziabile prescrive direttamente una forma di visuale. Non prescriverlo qui significherebbe lasciarlo scoprire davanti allo schermo, dove la scheda singola è il default di qualunque strumento.
- **Alternative scartate**: nessuna difendibile — una scheda con il valore centrale comunica una certezza che il dato non ha.
- **Riferimento**: spec.md, `F4`; `kpi_measures.md` §8.

### F5 — Fonte e confidenza qui, limiti divulgativi alla `008b`

- **Decisione**: ogni KPI a schermo porta accanto l'etichetta di fonte e quella di confidenza, nella forma di `business_case.md` §5.4. Nessuna spiegazione del perché: quella è narrazione.
- **Motivazione**: il confine fra le due feature non passa fra «numero» e «contesto», ma fra ciò che accompagna obbligatoriamente il numero (principio I, non negoziabile) e ciò che spiega come leggerlo (principio IV, deliverable della `008b`).
- **Alternative scartate**: rinviare anche le etichette alla `008b` — lascerebbe, alla chiusura di questa feature, otto numeri a schermo privi dell'etichetta che il principio I dichiara non negoziabile, in un file che la roadmap prevede possa essere mostrato prima che la `008b` esista.
- **Conseguenza dichiarata**: il `.pbix` alla chiusura di questa feature è leggibile, non pubblicabile.
- **Riferimento**: spec.md, `F5`; Complexity Tracking di plan.md, prima riga.

### F6 — La regola di decisione della North Star non va a schermo

- **Decisione**: `C1` compare accanto a `BQ1-K1`, `C3` accanto a `BQ2-K3`; nessuna pagina compone le condizioni in un verdetto né nomina la regola «tre su tre».
- **Motivazione**: `C2` non esiste come valore ancorato in alcun artefatto (parte dell'issue `#17`). Due condizioni verdi presentate insieme comunicherebbero un esito che nessuno ha misurato, e l'omissione della terza non si vedrebbe.
- **Alternative scartate**: mostrare la regola con `C1` e `C3` e omettere `C2` (la peggiore delle tre); calcolare `C2` come misura nuova — un confronto fra un valore misurato e una soglia è esso stesso un valore misurato (`convenzioni-marcatura.md` §7), avrebbe bisogno di un'ancora in un artefatto versionato, e scrivere artefatti è fuori dal perimetro.
- **Ritrovamento che ne discende**: la regola di decisione della North Star non è esponibile a schermo finché `C2` non esiste come valore ancorato. Riguarda la `008b` ed è segnalato alla regia.
- **Riferimento**: spec.md, `F6`.

### F7 — Le soglie del quadrante sono misure, non costanti

- **Decisione**: le due soglie di `BQ2-K3` esposte come misure DAX proprie — la stessa espressione `MEDIANX ( ALL ( dim_segment ), … )` che già vive dentro `segment_entry_priority_quadrant` — e la loro lettura confrontata una volta con il valore pubblicato.
- **Motivazione**: due numeri digitati a mano in una visuale sono valori la cui unica fonte è che qualcuno li ha scritti, che è precisamente ciò che il principio I vieta. La formula esiste già: il costo rispetto all'alternativa è nullo.
- **Alternative scartate**: linee di riferimento su valori costanti digitati.
- **Guadagno collaterale**: `kpi_measures.md` §11.1 dichiara che le due soglie **non** sono state lette dal motore come valori a sé stanti. Esporle come misure permette di leggerle: se coincidono, l'esclusione si chiude; se divergono, è un ritrovamento con nota in loco.
- **Riferimento**: spec.md, `F7`.

### F8 — Nomi semantici invariati

- **Decisione**: le misure nel modello portano i nomi semantici di `business_case.md` §5.1 più le due companion; organizzazione in cartelle DAX per domanda di business; ogni scostamento dichiarato nell'esito.
- **Motivazione**: i nomi semantici sono dichiarati univoci sull'intero progetto e compaiono in cinque documenti pubblicati. Rinominarli nel modello introdurrebbe un secondo vocabolario che nessun documento traduce.
- **Alternative scartate**: nomi abbreviati o localizzati per la leggibilità a schermo — l'etichetta visibile di una visuale può essere in italiano senza che il nome della misura cambi, quindi il guadagno è nullo e il costo è un vocabolario in più.
- **Vincolo ereditato**: punto 5 del contratto di lettura della `007b` — un adattamento che cambia il valore è un ritrovamento, non una libertà implicita.
- **Riferimento**: spec.md, `F8`.

### F9 — Scostamento e ritrovamento sono due categorie, non una

- **Decisione**: **scostamento** = differenza fra contratto approvato e pagine costruite (visuale, numero di pagine, filtri, nomi, navigazione), si elenca nell'esito con la ragione. **Ritrovamento** = differenza fra un valore letto a schermo e il valore pubblicato, si dichiara con nota in loco sul documento della `007b`.
- **Motivazione**: sono cose di gravità diversa e confonderle produrrebbe o un allarme su un cambio di visuale, o un silenzio su un numero che non torna. La distinzione è la stessa che la `007b` ha reso concreta: un difetto trovato costruendo vale come dato, e vale solo se è dichiarato dove chi legge il valore lo incontra.
- **Alternative scartate**: una categoria sola («differenze dal piano»), che appiattirebbe le due gravità.
- **Riferimento**: spec.md, `F9`.

## Che cosa questa Fase 0 non ha dovuto ricercare

**Le formule.** Sono pubblicate e verificate contro il motore reale dalla `007b`; questa feature le incolla e non le riscrive.

**I valori.** Sono pubblicati e ancorati; questa feature non ne calcola alcuno.

**Lo strumento.** Power BI Desktop è fissato dalla constitution, non scelto qui.

**La forma delle etichette di fonte e confidenza.** È già fissata da `business_case.md` §5.4 e ripetuta invariata da due documenti successivi.

Resta ricercabile una cosa sola, e non è ricercabile a tavolino: **se le visuali scelte reggano la forma del dato davanti a uno schermo reale.** È ciò che ★2 verifica, ed è la ragione per cui gli scostamenti sono previsti dal disegno invece che trattati come difetti.
