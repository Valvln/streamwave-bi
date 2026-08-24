# Feature Specification: Dashboard — modello, pagine, misure a schermo

**Feature Branch**: `008a-dashboard-model-pages`

**Created**: 2026-08-24

**Status**: Draft

**Input**: User description: "Caricare il modello dati nel `.pbix` già materializzato, costruire le pagine, esporre a schermo gli otto KPI di `docs/kpi_measures.md` e la navigazione fra pagine. Il deliverable vive per intero nella GUI di Power BI Desktop, fuori dal confine dell'automazione (principio V): la sessione scrive il contratto di pagina come documento, Valerio lo esegue a mano, la sessione documenta l'esito. Tre punti di fermata invece di due. Due vincoli da rispettare e non scoprire dopo: l'issue `#18` e le 114 righe per segmento. Perimetro: nessuna narrazione né limiti a schermo in forma divulgativa (`008b`), nessun Tableau (`009`), nessuna modifica a `docs/roadmap.md`, nessuna scrittura in `data/raw/` o `data/processed/`, nessuna riapertura degli otto valori pubblicati dalla `007b`. Il `.pbix` non si committa."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come decisione, requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

---

## La domanda a cui questa spec risponde per prima

Le sette feature precedenti hanno prodotto documenti: testo e artefatti versionati, verificabili da chiunque cloni il repository. Questa produce un **file binario che nessuno script può leggere, che non viene committato, e che vive interamente dentro una GUI**. È la prima volta che accade, e la domanda che precede ogni scelta di layout è: *che cosa resta nel repository quando la feature è chiusa?*

La risposta di questa spec è che restano **due artefatti testuali e un riporto**: il **contratto di pagina**, che dichiara prima della costruzione quali KPI ciascuna pagina espone, con quale visuale, con quali filtri e come vi si arriva; l'**esito**, che dichiara dopo la costruzione che cosa esiste davvero e in che cosa si scosta dal contratto; e il **verbale di revisione** su entrambi. Il `.pbix` è il deliverable, ma non è la prova: la prova è che il disegno sia stato scritto prima, che gli scostamenti siano stati dichiarati invece di assorbiti, e che nessun numero sia arrivato a schermo senza provenire da un valore pubblicato.

Ne discende il vincolo che governa l'intera feature e che nessuna scelta di visuale può violare: **a schermo si può portare solo ciò che `docs/kpi_measures.md` ha già pubblicato, alla grana a cui l'ha pubblicato.** Una dashboard è il primo artefatto di questo progetto in cui un numero smette di essere una cifra in una tabella e diventa un'affermazione rivolta a un lettore; è anche il primo in cui un filtro lasciato acceso può cambiare quel numero senza che nulla lo segnali.

---

## Le decisioni che questa feature prende

Nove decisioni, numerate `F1`-`F9` per non collidere con le `E1`-`E9` della `007b`. Ciascuna riporta il contesto che l'ha sollevata, le opzioni sul tavolo, la scelta e la ragione.

### F1 — Tre fasi e un terzo punto di fermata: il contratto di pagina si scrive prima che Power BI venga aperto

**Il contesto**: il principio V esclude la GUI di Power BI Desktop dall'automazione. Nella `007b` l'unico passo fuori dal confine era `E9`, una verifica puntuale; qui è la feature intera. Un flusso in cui la sessione «implementa» non esiste: non c'è nulla che possa implementare.

**Le opzioni**: (a) la sessione scrive istruzioni operative passo-passo e Valerio le esegue mentre le legge, senza un'approvazione intermedia; (b) la sessione scrive un **contratto di pagina** — che cosa ogni pagina espone e perché, non come si clicca — Valerio lo approva o lo corregge, poi costruisce, poi riporta; (c) Valerio costruisce a intuito e la sessione documenta a posteriori ciò che è stato costruito.

**La decisione**: **(b)**, con un punto di fermata esplicito fra il contratto e la costruzione. Le tre fasi sono: **contratto** (scriptabile, sessione) → **costruzione** (manuale, Valerio, fuori da questa sessione) → **riporto e chiusura** (scriptabile, sessione).

**La ragione**: è il punto di massima leva della feature. Un errore di perimetro nel contratto costa una rilettura; lo stesso errore scoperto a schermo già costruito costa di rifare pagine — è la stessa lezione di `C1`, `CF-1` ed `E9`, applicata al layout invece che alla formula. (c) produrrebbe una documentazione che ratifica invece di vincolare, ed è esattamente la forma che la condizione 1 delle assegnazioni dell'analista (constitution, Vincoli di Dominio e di Dato) vieta per i valori: un criterio scritto dopo aver visto l'esito si piega a giustificarlo. (a) non ha il difetto di (c) ma non ha nemmeno il presidio: senza approvazione intermedia, il disegno e la sua esecuzione sono la stessa decisione presa due volte dalla stessa persona.

**Che cosa il contratto è e che cosa non è**: è un documento di **disegno** — quali KPI, quale visuale e perché contro la forma del dato, quali filtri, come ci si arriva. Non è un manuale di clic: la sequenza di operazioni nella GUI appartiene a chi costruisce, e prescriverla sarebbe pilotare la GUI per interposta prosa.

---

### F2 — La regola di invarianza a schermo, che chiude l'issue `#18` senza toccare alcuna formula

**Il contesto**: issue `#18` — `mood_profile_overlap` (`BQ1-K3`) calcola gli estremi degli assi con `MINX`/`MAXX` su `dim_category_mood` senza `ALL`. `docs/kpi_measures.md` §6.2 argomenta l'omissione dell'`ALL` per il filtro di *segmento*, che non raggiunge il lato video; nessun documento la argomenta per il filtro di *categoria*, a cui `dim_category_mood` è invece raggiungibile. Il valore pubblicato non è sbagliato — nessun filtro era attivo nel confronto di `E9` — ma una pagina filtrabile è precisamente il contesto in cui il difetto si manifesta.

**Le opzioni**: (a) correggere la formula DAX aggiungendo l'`ALL` mancante, e poi mettere `BQ1-K3` dove si vuole; (b) non mettere `BQ1-K3` accanto ad alcun filtro di categoria, lasciando la formula com'è; (c) entrambe.

**La decisione**: **(b)**, formulata come regola generale invece che come eccezione per un KPI: **un valore a schermo deve essere un valore pubblicato da `docs/kpi_measures.md`, alla grana a cui quel documento lo pubblica.** Le grane pubblicate sono tre e nessun'altra — catalogo intero (`BQ1-K1`, `BQ1-K2`, `BQ1-K3`), segmento (`BQ2-K1`, `BQ2-K2`, `BQ2-K3`, per tutti e 114 i segmenti), scenario (`BQ3-K1`, `BQ3-K2`, tre scenari). Nessuna pagina può quindi offrire un'interazione che produca un valore di KPI a una grana diversa: nessun filtro di categoria video, nessun filtro di anno, nessun filtro di tipo di titolo su una visuale che porta un KPI.

**La ragione**: la correzione (a) è probabilmente giusta in sé, ma non è di questa feature. Il testo DAX di `docs/kpi_measures.md` §4.2 è pubblicato, ancorato e verificato contro il motore; cambiarlo qui significa modificare un artefatto già mergiato, che per la prassi di questo progetto si fa con nota in loco e con una ragione che regga — e la ragione qui sarebbe *rendere possibile un'interazione che questa feature ha comunque deciso di non offrire*. (b) ottiene lo stesso risultato al costo di una riga nel contratto di pagina, e per di più copre un insieme di rischi più largo dell'`ALL` mancante: il filtro di categoria su `BQ1-K3` è il caso noto, ma nulla garantisce che sia l'unico.

**Che cosa questa decisione non chiude**: l'issue `#18` **resta aperta**. Questa feature dimostra che il difetto non si manifesta nelle pagine costruite, non che non esista. Chiuderla richiede la correzione della formula, che appartiene a chi vorrà esporre `BQ1-K3` in un contesto filtrabile — non necessariamente a nessuno.

---

### F3 — I 114 segmenti si presentano come quadrante più graduatoria completa, mai come sola cima

**Il contesto**: `docs/kpi_operators.md` §7.3, `docs/data_model.md` §19 e la nota di adozione su `business_case.md` §4 dichiarano tutti e tre lo stesso vincolo, e tutti e tre lo assegnano alla dashboard: la graduatoria di `BQ2-K3` ha una voce per segmento, quindi 114, che sono molte per una lettura a colpo d'occhio. Nessuno dei tre lo risolve, ed è corretto che non lo facciano — è un problema di presentazione.

**Le opzioni**: (a) una tabella completa con ricerca e ordinamento; (b) le prime *N* posizioni, con il resto raggiungibile altrove; (c) una visuale a dispersione domanda × affinità con le due soglie del quadrante come linee di riferimento, affiancata dalla graduatoria completa.

**La decisione**: **(c)**. La dispersione è la visuale primaria della pagina `BQ2`; la graduatoria completa dei 114 segmenti la accompagna sulla stessa pagina, ordinata per punteggio decrescente, con la quota di zeri accanto alla domanda e l'avvertimento sui segmenti `is_high_zero_genre` accanto al nome.

**La ragione**: `business_case.md` §4 formula `BQ2` come una domanda sul **quadrante** — «quali segmenti si collocano nel quadrante ad alta domanda e alta affinità» — e una dispersione con due linee di soglia è la forma in cui quella domanda si legge in un colpo d'occhio su 114 punti, che una tabella di 114 righe non offre a nessun prezzo. L'appartenenza al quadrante è inoltre un valore **booleano già pubblicato** per ogni segmento: la visuale mostra ciò che l'artefatto contiene, non una classificazione costruita a schermo.

(b) è l'opzione scartata con la ragione più netta, ed è la ragione per cui il vincolo non poteva essere «non affrontato»: una cima di graduatoria nasconde i 7 segmenti a mediana nulla, che stanno tutti oltre la posizione 96, e con essi nasconde l'unica cosa che `docs/kpi_measures.md` §7.4 chiede di non perdere — che la coda di quella graduatoria è in parte una classifica di copertura del dato e non di preferenza. (a) da sola non risponde alla domanda di business, ma è necessaria accanto a (c) perché la dispersione, mostrando i punti, non mostra i nomi.

---

### F4 — `BQ3` a schermo esiste solo come intervallo a tre scenari

**Il contesto**: `BQ3-K1` e `BQ3-K2` sono a confidenza **bassa**, e il principio I lo rende non negoziabile: dove la confidenza è bassa il valore va espresso come range best/base/worst, mai come numero singolo. `docs/kpi_measures.md` §8 aggiunge tre vincoli che vanno ripetuti ogni volta che quei numeri compaiono: il tasso è lordo, l'uplift non è scalabile per alcuna base utenti, l'uplift è a regime e non cumulato.

**La decisione**: la pagina `BQ3` porta i due KPI come **tre valori affiancati** (pessimista, centrale, ottimista), mai come una scheda singola con il valore centrale. Nessuna visuale della pagina moltiplica l'uplift per una quantità di utenti, per una durata o per qualunque altro fattore: il prodotto non esiste come valore pubblicato e sarebbe un totale che nessuno ha misurato, presentato con l'autorevolezza di uno misurato. Le unità — punti percentuali della base per `BQ3-K1`, euro per utente al mese per `BQ3-K2` — compaiono accanto ai valori.

**La ragione**: è l'unico punto in cui un principio non negoziabile prescrive direttamente una **forma di visuale**, e non prescriverlo qui significherebbe lasciarlo scoprire davanti allo schermo, dove una scheda singola è la scelta di default di qualunque strumento di reporting.

---

### F5 — Fonte e confidenza sono di questa feature; i limiti in forma divulgativa sono della `008b`

**Il contesto**: il perimetro di questa feature esclude la narrazione e i limiti portati a schermo in forma comprensibile a un lettore non tecnico, che `kpi_operators.md` §12 e il contratto della `007b` assegnano esplicitamente alla `008b`. Il principio I chiede però che **ogni numero mostrato in dashboard** dichiari fonte e livello di confidenza in modo leggibile dall'utente finale, ed è un principio non negoziabile.

**Le opzioni**: (a) rinviare anche le etichette di fonte e confidenza alla `008b`, trattandole come parte della narrazione; (b) portarle a schermo in questa feature, trattandole come parte della misura.

**La decisione**: **(b)**. Ogni KPI a schermo porta accanto la propria etichetta di fonte (`Netflix (reale)`, `Spotify (reale)`, `Sintetico`, `Derivato`) e di confidenza (alta, media, bassa), nella forma già fissata da `business_case.md` §5.4 e ripetuta invariata da `kpi_operators.md` §11. Sono etichette, non prosa: nessuna spiegazione di *perché* quella confidenza, che è ciò che la `008b` scriverà.

**La ragione**: (a) produrrebbe, alla fine di questa feature, un `.pbix` leggibile con otto numeri privi dell'etichetta che il principio I dichiara non negoziabile — e la roadmap prevede che quel file possa essere mostrato prima che la `008b` esista. Il confine fra le due feature non passa fra «numero» e «contesto»: passa fra **ciò che accompagna obbligatoriamente il numero** e **ciò che spiega al lettore come leggerlo**.

**Che cosa questo non fa, ed è dichiarato qui perché nessuno lo dia per fatto**: alla fine di questa feature il `.pbix` **non è un artefatto finito per un lettore esterno**. Mancano l'assunzione strutturale dei proxy — che la constitution impone di dichiarare in ogni artefatto rivolto all'utente finale — i limiti del principio IV e la narrazione. È la `008b` a chiuderli, ed è la ragione per cui il deliverable di questa feature è un file leggibile, non un file pubblicabile.

---

### F6 — La regola di decisione della North Star non va a schermo, perché `C2` non esiste come valore pubblicato

**Il contesto**: `business_case.md` §3 fissa tre condizioni — `C1`, `C2`, `C3` — e la regola con cui il loro esito congiunto decide se l'argomento di coerenza strategica è sostenuto. `docs/kpi_measures.md` pubblica `C1` come booleano ancorato (§2.3) e `C3` come booleano ancorato (§7.1). **`C2` non è pubblicata da nessuna parte**: è il confronto fra `mood_profile_overlap` e la soglia della maggioranza, e nessun artefatto lo contiene. È parte di quanto l'issue `#17` registra.

**Le opzioni**: (a) portare a schermo la regola di decisione con `C1` e `C3` e omettere `C2`; (b) calcolare `C2` come misura nuova e portarla a schermo con le altre due; (c) non portare a schermo la regola di decisione, ed esporre `C1` e `C3` solo accanto al proprio KPI.

**La decisione**: **(c)**. `C1` compare nella pagina `BQ1` accanto a `BQ1-K1`, `C3` nella pagina `BQ2` accanto a `BQ2-K3`; nessuna pagina compone le condizioni in un verdetto, e nessuna pagina nomina la regola «tre su tre».

**La ragione**: (a) è la peggiore delle tre, perché due condizioni verdi presentate insieme comunicano un esito che nessuno ha misurato — e l'omissione della terza non si vede. (b) produce un valore nuovo: un confronto fra un valore misurato e una soglia è esso stesso un valore misurato (regola di progetto, `docs/convenzioni-marcatura.md` §7), quindi `C2` avrebbe bisogno di un'ancora in un artefatto versionato, e scrivere artefatti non è nel perimetro di questa feature.

**Il ritrovamento che ne discende, registrato e non risolto qui**: la regola di decisione della North Star **non è esponibile a schermo finché `C2` non esiste come valore ancorato**. Riguarda direttamente la `008b`, che scrive la narrazione della North Star ed è la prima che avrà bisogno di quel verdetto. Va segnalato alla regia insieme all'esito di questa feature.

---

### F7 — Le soglie del quadrante a schermo sono misure, non numeri digitati

**Il contesto**: la decisione `F3` mette a schermo le due soglie di `BQ2-K3` come linee di riferimento della dispersione. Quelle due soglie sono valori pubblicati e ancorati in `docs/kpi_measures.md` §7.1, ma `§11.1` dichiara esplicitamente che **non sono state lette dal motore come valori a sé stanti**: vivono come variabili interne alla formula del quadrante ed `E9` le ha esercitate solo indirettamente.

**Le opzioni**: (a) disegnare le linee su valori costanti digitati a mano nella visuale; (b) esporre le due soglie come misure DAX proprie — la stessa espressione `MEDIANX ( ALL ( dim_segment ), … )` che già vive dentro `segment_entry_priority_quadrant` — e usarle come linee.

**La decisione**: **(b)**. E poiché esporle come misure significa poterle leggere, la loro lettura **va confrontata una volta** con il valore pubblicato: se coincide, chiude l'esclusione che `§11.1` dichiara; se diverge, è un ritrovamento da dichiarare con nota in loco su `docs/kpi_measures.md`, mai una correzione silenziosa.

**La ragione**: (a) porterebbe a schermo due numeri scritti a mano, cioè esattamente ciò che il principio I vieta — un valore la cui unica fonte è che qualcuno lo ha digitato. Il costo di (b) è nullo rispetto ad (a), perché la formula esiste già; il guadagno è che un'esclusione dichiarata da `E9` viene chiusa dall'unica feature che si trovi ad avere quelle misure sotto gli occhi.

---

### F8 — I nomi delle misure restano quelli semantici; ogni adattamento si dichiara

**Il contesto**: punto 5 del contratto di lettura della `007b` — `008a` può adattare il testo DAX (nomi di misura, organizzazione in cartelle) purché il valore prodotto resti quello verificato da `E9`; un adattamento che cambia il valore è un ritrovamento, non una libertà implicita.

**La decisione**: i nomi delle misure nel modello sono i **nomi semantici** di `business_case.md` §5.1, invariati — `music_adjacent_catalog_share`, `format_duration_gap`, `mood_profile_overlap`, `segment_demand_index`, `segment_catalog_affinity`, `segment_entry_priority_score`, `segment_entry_priority_quadrant`, `segment_entry_priority_rank` — più le companion `c1_music_above_median` e `segment_zero_share`. L'organizzazione in cartelle DAX è per domanda di business. Qualunque scostamento da questi nomi si dichiara nell'esito; qualunque adattamento che cambi un valore è un ritrovamento e si dichiara come tale.

**La ragione**: i nomi semantici sono dichiarati univoci sull'intero progetto da `business_case.md` §5.1 ed è la forma in cui compaiono in cinque documenti pubblicati. Rinominarli nel modello introdurrebbe un secondo vocabolario che nessun documento traduce.

---

### F9 — Che cosa conta come scostamento, e perché si dichiara invece di assorbirlo

**Il contesto**: fra il contratto approvato e le pagine costruite può esistere una differenza — una visuale che nella pratica non regge la forma del dato, un filtro che si rivela necessario, una pagina che si divide in due. Il rischio non è che accada: è che venga assorbita in silenzio, lasciando un contratto che descrive un file diverso da quello che esiste.

**La decisione**: è **scostamento** qualunque differenza fra il contratto approvato e le pagine costruite: tipo di visuale, numero di pagine, filtri e slicer presenti, nomi delle misure, elementi di navigazione. È **ritrovamento** — categoria più grave — qualunque differenza fra un valore letto a schermo e il valore pubblicato da `docs/kpi_measures.md`. Gli scostamenti si elencano nell'esito con la ragione; i ritrovamenti si dichiarano con nota in loco sul documento della `007b`, e non correggono in silenzio né il documento né lo schermo.

**La ragione**: è la stessa distinzione che `E9` ha reso concreta nella `007b` — un difetto trovato costruendo vale come dato, e vale solo se è dichiarato dove chi legge il valore lo incontra.

---

## Rapporto con le feature vicine

**Da `007b` eredita** gli otto valori, il testo DAX di ciascuna misura e il contratto di lettura. Non riapre nessuno dei tre.

**Alla `008b` lascia** la narrazione, i limiti in forma divulgativa, l'assunzione strutturale dei proxy a schermo, e il ritrovamento di `F6` sulla regola di decisione della North Star. Le pagine costruite qui sono la superficie su cui quella feature scriverà: questa spec non prescrive dove il testo andrà, ma il contratto di pagina lascia spazio dichiarato per esso.

**Alla `009` (Tableau) e alla `010` (case study)** non lascia nulla di nuovo, salvo il fatto che il `.pbix` leggibile esiste — che è la precondizione che la roadmap assegna alla `010`.

---

## Perimetro

**Questa feature non fa**, e per ciascuna voce è dichiarato a chi spetta:

- **narrazione, storytelling, limiti a schermo in forma comprensibile a un lettore non tecnico** — `008b`, già assegnato da `kpi_operators.md` §12 e dal contratto della `007b`;
- **Tableau** — `009`;
- **modifiche a `docs/roadmap.md`** — regia, mai una sessione esecutiva;
- **scritture in `data/raw/` o `data/processed/`** — la prima è in sola lettura per il principio II, la seconda è materiale di lavoro prodotto dalla pipeline;
- **riapertura degli otto valori pubblicati dalla `007b`** — un valore che risultasse sbagliato costruendo una pagina è un ritrovamento da dichiarare con nota in loco (`F9`), non una correzione;
- **nuove misure e nuovi valori** — nessun KPI nuovo, nessuna aggregazione nuova, nessun booleano nuovo (è la ragione di `F6`);
- **il commit del `.pbix`** — incorpora i dati, e `data/processed/` è fuori dal versionamento per scelta.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Un lettore apre il file e trova le tre domande di business, ciascuna con i propri KPI (Priority: P1)

Chi apre il `.pbix` incontra una pagina di ingresso con la North Star e la navigazione verso tre pagine, una per domanda di business. Ogni pagina porta a schermo i KPI di quella domanda, ciascuno con il proprio valore, la propria etichetta di fonte e la propria etichetta di confidenza.

**Why this priority**: è il deliverable. Senza questo non esiste dashboard, e le altre storie sono qualificazioni di questa.

**Independent Test**: aprire il file, contare i KPI a schermo e confrontarli con `docs/kpi_measures.md`: devono essere otto, nessuno mancante, nessuno in più.

**Acceptance Scenarios**:

1. **Given** il `.pbix` aperto sulla pagina di ingresso, **When** si percorrono le tre pagine di domanda, **Then** si incontrano tutti e otto i KPI, ciascuno con fonte e confidenza accanto.
2. **Given** una qualunque pagina, **When** si legge un valore di KPI, **Then** quel valore coincide con quello pubblicato da `docs/kpi_measures.md` per la stessa grana.
3. **Given** una qualunque pagina, **When** si cerca la navigazione, **Then** ogni altra pagina è raggiungibile senza passare dal riquadro delle schede di Power BI.

---

### User Story 2 — I 114 segmenti si leggono senza troncare e senza scambiare la coda per una classifica di preferenza (Priority: P1)

Chi cerca il segmento di ingresso vede in un colpo d'occhio quali segmenti stanno nel quadrante ad alta domanda e alta affinità, e può poi leggere la graduatoria completa senza che alcun segmento sia stato tolto per far stare la visuale nello schermo.

**Why this priority**: è il vincolo che tre documenti pubblicati assegnano esplicitamente a questa feature, ed è quello su cui una scelta comoda produce un artefatto che afferma il falso.

**Independent Test**: contare le righe della graduatoria a schermo — devono essere 114 — e verificare che i sette segmenti marcati `is_high_zero_genre` portino l'avvertimento accanto al nome.

**Acceptance Scenarios**:

1. **Given** la pagina `BQ2`, **When** si guarda la dispersione, **Then** le due soglie sono visibili come linee e i segmenti del quadrante sono distinguibili dagli altri.
2. **Given** la graduatoria completa, **When** si scorre fino in fondo, **Then** tutti i 114 segmenti sono presenti e nessuno è stato escluso dalla visuale.
3. **Given** un segmento marcato `is_high_zero_genre`, **When** lo si legge in graduatoria, **Then** accanto al suo indice di domanda compare la quota di zeri e l'avvertimento testuale.
4. **Given** due segmenti a pari punteggio, **When** si legge la loro posizione, **Then** portano la stessa posizione e la successiva salta, come `docs/kpi_measures.md` §7.2 prescrive.

---

### User Story 3 — Nessuna interazione a schermo produce un valore che nessun documento ha pubblicato (Priority: P1)

Chi usa un filtro, uno slicer o un'evidenziazione incrociata non può ottenere un valore di KPI a una grana diversa da quella pubblicata. In particolare, nessuna pagina che porti `BQ1-K3` offre un filtro di categoria video.

**Why this priority**: è la forma in cui l'issue `#18` viene neutralizzata, ed è il rischio specifico che la roadmap segnala alla feature che apre le pagine.

**Independent Test**: percorrere ogni pagina ed elencare ogni filtro, slicer e interazione incrociata attivi; per ciascuno, verificare che la grana risultante sia una delle tre pubblicate.

**Acceptance Scenarios**:

1. **Given** la pagina `BQ1`, **When** si cerca un filtro di categoria video, **Then** non ne esiste alcuno.
2. **Given** una selezione su un segmento nella pagina `BQ2`, **When** si legge il valore di `BQ2-K1`, `BQ2-K2` o `BQ2-K3`, **Then** è il valore pubblicato per quel segmento, non un ricalcolo su un sottoinsieme.
3. **Given** una qualunque pagina, **When** si prova a costruire un totale sommando una quantità su più segmenti, **Then** nessuna visuale della pagina lo offre.

---

### User Story 4 — Il modello è caricato con i tipi giusti, e lo si verifica prima di costruire (Priority: P1)

Chi costruisce controlla, prima di disegnare una sola pagina, che `energy`, `valence` e `danceability` di `dim_track` portino valori fra 0 e 1 e non nell'ordine delle centinaia.

**Why this priority**: è il difetto che `E9` ha trovato nella `007b` e che nessun controllo di questo repository può vedere. Se si ripresenta e non lo si nota, tre KPI su otto vanno a schermo sbagliati di due ordini di grandezza sotto un esito verde di ogni controllo automatico.

**Independent Test**: aprire il modello e leggere le tre colonne. Costa una lettura, come è costato a `E9`.

**Acceptance Scenarios**:

1. **Given** il modello caricato, **When** si ispezionano le tre colonne di mood, **Then** i valori stanno fra 0 e 1.
2. **Given** un valore fuori scala, **When** lo si trova, **Then** la costruzione si ferma, la tipizzazione si corregge, e il fatto si dichiara nell'esito come ricomparsa del difetto dell'issue `#11`.

---

### User Story 5 — Chi legge il repository sa che cosa la dashboard contiene senza poterla aprire (Priority: P2)

Chi clona il repository e non ha una licenza Power BI — o non ha il `.pbix`, che non è versionato — trova nel contratto di pagina e nell'esito quali pagine esistono, quali KPI espongono e in che cosa la costruzione si è scostata dal disegno.

**Why this priority**: è ciò che impedisce che l'unica traccia di una feature intera sia un file binario che nessuno può ispezionare. Non è P1 perché non è il deliverable: è la sua verificabilità.

**Independent Test**: leggere il contratto e l'esito senza aprire il `.pbix`, e ricostruire da lì che cosa esiste.

**Acceptance Scenarios**:

1. **Given** il contratto di pagina, **When** lo si legge, **Then** per ogni pagina si conoscono i KPI esposti, la visuale scelta con la sua ragione, i filtri presenti e la navigazione.
2. **Given** l'esito, **When** lo si confronta con il contratto, **Then** ogni differenza è elencata con la propria ragione, e le differenze non elencate non esistono.

---

### Edge Cases

- **La tipizzazione a locale si ripresenta** su una nuova apertura del modello (issue `#11`): la costruzione si ferma, si corregge, si dichiara. Non si costruisce sopra.
- **Un valore letto a schermo diverge da quello pubblicato**: è un ritrovamento (`F9`), non un errore da correggere in silenzio né a schermo né nel documento.
- **Una visuale non regge la forma del dato** — la dispersione di 114 punti risulta illeggibile, la graduatoria completa non entra nella pagina: è uno scostamento, si costruisce l'alternativa e si dichiara. Non si tronca la graduatoria (`F3`).
- **Un filtro serve davvero** per rendere leggibile una pagina: è ammesso solo se la grana che produce è una delle tre pubblicate, altrimenti è la regola di `F2` che vince sulla comodità.
- **Le due soglie del quadrante divergono** fra misura e valore pubblicato (`F7`): ritrovamento, nota in loco, e l'esclusione di `§11.1` resta aperta.
- **Un segmento manca dalla graduatoria** perché una relazione non propaga come atteso: la pagina non è conforme; è un difetto del modello, non una scelta di presentazione, e va dichiarato.
- **`data/processed/` non esiste** sulla macchina che apre il modello: il modello non si carica e la pipeline va rieseguita. Non è un difetto di questa feature, ma è la sua prima dipendenza.

---

## Requirements *(mandatory)*

### Il contratto di pagina (F1)

- **FR-001**: Il contratto di pagina DEVE esistere come documento versionato sotto `specs/008a-dashboard-model-pages/` **prima** che Power BI Desktop venga aperto per costruire.
- **FR-002**: Il contratto DEVE dichiarare, per ciascuna pagina: quali KPI espone, con quale visuale, con quale ragione motivata **contro la forma del dato** e non per preferenza estetica, quali filtri o slicer sono presenti, e come vi si arriva dalla navigazione.
- **FR-003**: Il contratto NON DEVE contenere valori dei KPI trascritti: cita le misure per nome e rinvia alla sezione di `docs/kpi_measures.md` che le pubblica. Una seconda copia di un valore è una copia che può divergere.
- **FR-004**: Il contratto DEVE dichiarare esplicitamente, per ogni pagina, quali interazioni **non** sono offerte e perché (regola di `F2`).
- **FR-005**: La sessione DEVE fermarsi dopo il contratto e attendere approvazione o correzione, senza procedere ad alcuna istruzione di costruzione.

### Il modello e le misure

- **FR-006**: Il modello caricato DEVE contenere le sette tabelle di `docs/data_model.md` §3 con le relazioni e le direzioni di filtro di §6.
- **FR-007**: Prima di costruire qualunque pagina, le colonne `energy`, `valence` e `danceability` di `dim_track` DEVONO essere verificate a occhio nel dominio `0-1` (issue `#11`).
- **FR-008**: Le misure nel modello DEVONO portare i nomi semantici di `business_case.md` §5.1 e le companion dichiarate in `F8`; ogni scostamento va dichiarato nell'esito.
- **FR-009**: Il testo DAX incollato nel modello DEVE essere quello pubblicato da `docs/kpi_measures.md`; un adattamento che cambia un valore è un ritrovamento (`F9`), non una libertà.
- **FR-010**: Le due soglie del quadrante, se portate a schermo, DEVONO esistere come misure e non come costanti digitate (`F7`), e la loro lettura DEVE essere confrontata una volta con il valore pubblicato.

### Che cosa va a schermo

- **FR-011**: Tutti e otto i KPI DEVONO essere esposti a schermo, nessuno mancante.
- **FR-012**: Ogni KPI a schermo DEVE portare accanto la propria etichetta di **fonte** e di **confidenza** (`F5`, principio I).
- **FR-013**: `BQ3-K1` e `BQ3-K2` DEVONO comparire come tre valori di scenario affiancati, mai come valore singolo, con le rispettive unità (`F4`).
- **FR-014**: Nessuna visuale DEVE moltiplicare `BQ3-K2` per una base utenti, per una durata o per qualunque altro fattore (`F4`).
- **FR-015**: `BQ2-K1` DEVE comparire sempre accompagnato dalla quota di zeri del segmento (`D7`), e i sette segmenti `is_high_zero_genre` DEVONO portare l'avvertimento accanto al nome.
- **FR-016**: La graduatoria di `BQ2-K3` DEVE esporre tutti i 114 segmenti, senza troncamenti, con la regola dei pari merito preservata (`F3`).
- **FR-017**: `C1` e `C3` POSSONO comparire accanto al proprio KPI; la regola di decisione della North Star e il verdetto congiunto NON DEVONO comparire (`F6`).
- **FR-018**: Nessuna visuale DEVE presentare un conteggio di righe per segmento, un totale sommato su più segmenti, o un asse temporale: sono le tre letture che `docs/data_model.md` §18 dichiara prive di significato, e la loro metà strutturale si chiude qui non rendendole possibili.

### Filtri, interazioni e navigazione (F2)

- **FR-019**: Nessun filtro, slicer o interazione incrociata DEVE produrre un valore di KPI a una grana diversa da catalogo intero, segmento o scenario.
- **FR-020**: Nessuna pagina che espone `BQ1-K3` DEVE offrire un filtro di categoria video (issue `#18`).
- **FR-021**: Ogni pagina DEVE essere raggiungibile da ogni altra tramite elementi di navigazione interni al report, senza ricorrere alle schede di Power BI.

### Il riporto e la chiusura (F9)

- **FR-022**: L'esito della costruzione DEVE essere documentato in `specs/008a-dashboard-model-pages/quickstart.md` o in una sezione dedicata: quali pagine esistono, quali KPI espongono, quali scostamenti e perché.
- **FR-023**: Ogni scostamento dal contratto DEVE essere elencato con la propria ragione; un adattamento non dichiarato è un difetto della feature, non una libertà di chi costruisce.
- **FR-024**: Ogni ritrovamento — valore a schermo diverso dal valore pubblicato, difetto di tipizzazione ricomparso, divergenza sulle soglie — DEVE essere dichiarato con nota in loco sull'artefatto che lo riguarda, senza riscrivere il valore originale.
- **FR-025**: Le issue `#11` e `#18` DEVONO essere lasciate in uno stato dichiarato: chiuse se il riporto le chiude, altrimenti aperte con una nota su quale evidenza manca ancora.

### Obblighi che nessun automatismo esegue

- **FR-026**: Il README DEVE essere allineato: riga di stato con link al verbale, deliverable elencato, `Setup` e `Struttura` allineati se qualcosa cambia nel modo di rigenerare o verificare il progetto.
- **FR-027**: La revisione in contesto pulito DEVE produrre `specs/008a-dashboard-model-pages/review.md`, con i quattro obblighi di `CLAUDE.md`; l'oggetto della revisione è il contratto di pagina e la documentazione dell'esito, non il `.pbix`.
- **FR-028**: `scripts/check_audit_coherence.py` DEVE restare verde. Questa feature non aggiunge documenti a `DOCUMENTS` — non pubblica nulla sotto `docs/` — e non modifica alcun artefatto versionato, salvo eventuali note in loco.
- **FR-029**: Il `.pbix` NON DEVE essere committato.

### Key Entities

- **Contratto di pagina**: il documento di disegno prodotto dalla fase 1; una sezione per pagina, con KPI esposti, visuale e ragione, filtri, navigazione, interazioni escluse.
- **Pagina**: unità di navigazione del report; appartiene a una domanda di business o è la pagina di ingresso.
- **Misura**: una delle otto misure principali più le companion; porta il nome semantico e produce il valore pubblicato dalla `007b`.
- **Scostamento**: differenza dichiarata fra contratto e costruito; non tocca i valori.
- **Ritrovamento**: differenza fra un valore osservato e un valore pubblicato; obbliga a una nota in loco.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tutti e otto i KPI sono a schermo, ciascuno con fonte e confidenza accanto; il conteggio si verifica leggendo le pagine e confrontandole con `docs/kpi_measures.md`.
- **SC-002**: Le tre domande di business hanno ciascuna una pagina, e ogni pagina è raggiungibile da ogni altra in un clic.
- **SC-003**: La graduatoria a schermo contiene 114 righe; nessun segmento è escluso e i sette a mediana nulla portano l'avvertimento.
- **SC-004**: Nessuna interazione offerta dalle pagine produce un valore di KPI a una grana non pubblicata; l'elenco dei filtri presenti, pagina per pagina, lo rende verificabile.
- **SC-005**: Le tre colonne di mood sono state verificate nel dominio `0-1` **prima** che la prima pagina fosse costruita, e l'esito è dichiarato.
- **SC-006**: Il contratto di pagina è stato approvato prima dell'apertura di Power BI, e la sua approvazione è tracciabile nella history git.
- **SC-007**: Ogni differenza fra contratto ed esito è elencata; chi legge i due documenti in sequenza sa che cosa esiste senza aprire il file.
- **SC-008**: `python3 scripts/check_audit_coherence.py` esce verde.
- **SC-009**: Il verbale di revisione esiste, ed è stato committato prima che l'artefatto revisionato venisse modificato.
- **SC-010**: Il README dichiara lo stato della feature, il deliverable e il link al verbale.

---

## Stima e scomposizione

**Stima**: ~5 ore, revisione e chiusura dei rilievi incluse, come da `docs/roadmap.md`.

Distribuzione attesa: ~1,5 h per il contratto di pagina, ~2 h per la costruzione manuale (fuori da questa sessione), ~1,5 h per riporto, revisione e chiusura. La feature è già il prodotto della scomposizione della `008` decisa dalla regia il 2026-08-21, e non va scomposta ulteriormente.

**Se dopo il punto di fermata sul contratto il lavoro sembra più grande**, la sessione si ferma e lo riporta invece di comprimere: la parte comprimibile sarebbe la revisione, che è la sola cosa che questa feature produce di verificabile.

---

## Assumptions

- Il `.pbix` esiste già materializzato sulla macchina di Valerio, con il difetto di tipizzazione corretto dalla `007b`. Questa feature carica il modello in quel file, non ne crea uno nuovo.
- `data/processed/` è presente sulla macchina che apre il modello, rigenerato da `scripts/build_datasets.py`.
- Nessuna licenza Power BI Pro è necessaria: il deliverable è un file locale, non un report pubblicato. La pubblicazione di prova è caduta dalla roadmap il 2026-08-21.
- Le pagine sono quattro — ingresso più una per domanda di business. È un'assunzione di disegno, non un vincolo: il contratto di pagina può proporne un numero diverso, e in tal caso la ragione si dichiara lì.
- La costruzione avviene su un solo schermo di dimensione ordinaria, in rapporto 16:9: la leggibilità di 114 punti e 114 righe si giudica lì, non su una stampa.

---

## Debito ereditato

Ogni voce riporta il rilievo o la divergenza puntuale, non un rimando generico.

| Voce | Da dove viene | Che cosa questa feature ne fa |
|---|---|---|
| issue `#11` — la tipizzazione a locale può ripresentarsi, e nessun presidio del repository se ne accorge | `007b`, `E9`; roadmap, «Il difetto di tipizzazione può ripresentarsi» | verifica a occhio prima di costruire (`FR-007`); l'issue si chiude solo se la regia considera il passo documentato un presidio sufficiente, altrimenti resta aperta con l'evidenza mancante dichiarata (`FR-025`) |
| issue `#18` — `mood_profile_overlap` senza `ALL` sul filtro di categoria | revisione `007b`, rilievo `R13` | neutralizzata dalla regola `F2`, **non chiusa**: nessuna pagina offre quel filtro, e la formula resta com'è |
| issue `#17` — `C2` e il terzo vincolo di `kpi_operators.md` §12 mai nominati in `docs/kpi_measures.md` | revisione `007b`, rilievo `R12` | è la ragione di `F6`; questa feature non la chiude e registra il ritrovamento che ne discende per la `008b` |
| graduatoria di `BQ2-K3` a 114 voci | `data_model.md` §19; `kpi_operators.md` §7.3; nota di adozione su `business_case.md` §4 | chiusa da `F3` |
| le tre letture prive di significato — conteggio righe per segmento, somme su segmenti, asse temporale | `data_model.md` §18 e §19 | la **metà strutturale** si chiude qui (`FR-018`): non si rendono possibili. La metà discorsiva — spiegare al lettore perché — resta alla `008b` |
| verificabilità del benchmark di `BQ3` | debito della `004`; roadmap: «va deciso prima che `008a` pubblichi quei numeri in una dashboard» | **non decidibile da questa feature**: è una decisione di governance. La feature procede sotto l'assunzione dichiarata che la citazione pubblicata in `docs/bq3_scenarios.md` §9 resti la fonte, e segnala alla regia che i valori di `BQ3` vanno a schermo con quel debito aperto |
| «fonte più vicina non citabile» (benchmark Antenna) | debito della `004`, marcato «prima di `008a`» | stesso trattamento: non è una decisione di questa feature; segnalata alla regia con l'esito |

---

## I punti di fermata

Tre, non due. Il terzo è l'aggiunta dichiarata di questa feature, e non è una nota a margine: è un task che si ferma.

1. **dopo `/speckit.specify`** — la spec torna in revisione alla regia prima di diventare un piano;
2. **dopo `/speckit.tasks`** — piano e task tornano insieme, e non si implementa senza che siano stati visti;
3. **il contratto di pagina, dentro l'implementazione**, prima che Power BI Desktop venga aperto (`F1`, `FR-005`).

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ1, BQ2 e BQ3** — tutte e tre. È la prima feature del progetto che le serve simultaneamente, perché il dashboard le espone tutte.
- **Contributo**: non produce alcuna risposta nuova. Porta a schermo le risposte già calcolate dalla `007b` nella forma in cui una persona può leggerle: una pagina per domanda, i KPI di quella domanda, la navigazione fra le tre. È il passaggio da *valore pubblicato in un documento tecnico* a *valore letto da chi decide* — ed è la ragione per cui il vincolo di `F2` esiste, perché è esattamente in quel passaggio che un numero può cambiare senza che nessuno se ne accorga.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

**Questa feature non introduce alcuna metrica nuova e non altera alcuna classificazione di confidenza.** La tabella riporta quella già fissata da `business_case.md` §5.4 e ripetuta invariata da `kpi_operators.md` §11 e `kpi_measures.md`; la colonna che conta per questa feature è l'ultima, perché è un vincolo sulla **forma della visuale**.

| Metrica | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| `music_adjacent_catalog_share` 🎯 | Netflix (reale) | alta | osservata direttamente sul catalogo, nessuno strato interpretativo | valore singolo |
| `format_duration_gap` | Derivato (Netflix + Spotify) | alta | due grandezze osservate, una sottrazione | valore singolo, con il proprio segno |
| `mood_profile_overlap` | Derivato (Netflix + Spotify) | media | dipende da `dim_category_mood`, assegnata e non osservata | valore singolo con nota |
| `segment_demand_index` | Spotify (reale) | media | indice della fonte, di cui la fonte non dichiara la costruzione | valore per segmento, **sempre con la quota di zeri accanto** |
| `segment_catalog_affinity` | Derivato (Netflix + Spotify) | media | dipende da `dim_category_mood` | valore per segmento, confrontabile fra segmenti e non in assoluto |
| `segment_entry_priority` | Derivato (`BQ2-K1` + `BQ2-K2`) | media | ereditata dai due KPI che compone | ordinamento e appartenenza al quadrante, **non fusi** |
| `premium_tier_adoption_rate` | Sintetico | bassa | dipende interamente dalle assunzioni di scenario | **range pessimista/centrale/ottimista, mai valore singolo** |
| `arpu_uplift` | Derivato (`BQ3-K1` + prezzi di A4) | bassa | come sopra | **range, mai valore singolo; mai moltiplicato per una base** |

**Assunzioni dietro i dati sintetici**: nessun dato sintetico è generato da questa feature. Quelli di `BQ3` sono citati dall'artefatto della `004` senza ricalcolo, con le assunzioni dichiarate lì; il debito sulla verificabilità del benchmark resta aperto ed è registrato sopra.

**Dove fonte e confidenza compaiono a schermo**: accanto a ciascun KPI, come etichette (`F5`). La spiegazione del *perché* di quella confidenza è della `008b`.

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: se StreamWave debba entrare nel mercato musicale. La dashboard espone le misure; la decisione è di chi legge, e nessuna pagina la formula.
- **Non risponde a**: che cosa i numeri significhino per un lettore non tecnico. Questa feature costruisce la superficie; la `008b` scrive ciò che vi si legge sopra.
- **Inferenza da evitare**: che una dashboard esistente sia una dashboard finita. Alla chiusura di questa feature il `.pbix` è **leggibile, non pubblicabile**: mancano l'assunzione strutturale dei proxy, i limiti del principio IV in forma comprensibile e la narrazione (`F5`).
- **Inferenza da evitare**: che l'assenza di un difetto a schermo dimostri l'assenza del difetto. Vale per l'issue `#18`, neutralizzata e non chiusa (`F2`), e per l'issue `#11`, verificata una volta su un modello e non presidiata da nulla.
- **Copertura del dato**: invariata — catalogo video fermo al 2021, catalogo musicale al 2022, nessun dato comportamentale, due cataloghi pubblici usati come proxy. Nessun valore di questa feature descrive StreamWave.
- **Quali limiti restano fuori dallo schermo, e a chi spettano**: la stima per eccesso di `BQ1-K3` (§4.3), la non interpretabilità assoluta di `BQ2-K2` (§6.3), l'asimmetria di `BQ1-K2` (§3.4), il vincolo di versione su `dim_category_mood`, la non scalabilità dell'uplift di `BQ3-K2`, il fatto che i sette segmenti a mediana nulla misurino la copertura della fonte e non la domanda. Sono elencati qui **per dichiarare che restano fuori**, non per anticipare come vadano scritti: quello è il deliverable della `008b`, e scriverne qui la forma sarebbe deciderlo al posto della feature che lo possiede.
- **Dove è esposto all'utente finale**: fonte e confidenza accanto a ogni KPI, e l'avvertimento sui sette segmenti accanto al loro nome in graduatoria. Nient'altro: è la conseguenza dichiarata di `F5`, non un'omissione.

---

## Come si verifica

Le prove eseguibili da chiunque abbia clonato il repository:

```bash
# le ancore dei documenti pubblicati restano verdi: questa feature non ne tocca alcuno
python3 scripts/check_audit_coherence.py
```

Le prove che richiedono il `.pbix` non sono eseguibili da uno script e non lo saranno mai — è il principio V. Sono elencate come prove manuali nel quickstart della feature, e il loro esito vive nel riporto: è la stessa forma di `E9` della `007b`, dove un'osservazione umana è un dato purché sia dichiarata come tale.
