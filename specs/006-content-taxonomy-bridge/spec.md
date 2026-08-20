# Feature Specification: Content Taxonomy Bridge

**Feature Branch**: `006-content-taxonomy-bridge`

**Created**: 2026-08-20

**Status**: Draft

**Input**: User description: "Riempie `dim_category_mood`, la tabella che assegna a ciascuna delle 42 categorie del catalogo video un profilo di mood su tre assi (`mood_energy`, `mood_valence`, `mood_danceability`, decimali 0-1). Serve `BQ1-K3`, `BQ2-K2` e, attraverso `BQ2-K2`, `BQ2-K3`. Costruzione in quattro passi ordinati (DA-1, risolta il 2026-08-19): criterio scritto e committato da solo, prima di qualunque valore; proposta di un LLM con prompt/modello/data versionati; revisione riga per riga contro il criterio, in contesto pulito, con conteggio degli spostamenti; tabella congelata in un artefatto versionato con numero di versione. Chiude la divergenza 10 della revisione 001 (governance della tabella), la divergenza 5 della revisione 002 (presidio sul cambio di tassonomia) e la parte generale della divergenza 5 della revisione 003 (attributi di record individuali negli artefatti versionati). Nessuna misura DAX, nessuna materializzazione in Power BI, nessuna modifica a §11 di `docs/data_model.md`."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come decisione, requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

---

## La domanda a cui questa spec risponde per prima

Ogni altro numero pubblicato da questo progetto descrive un dato osservato — un campo letto da Netflix o da Spotify — o discende in modo deterministico da uno di quei dati, tramite una trasformazione che chiunque può rieseguire e verificare. `dim_category_mood` è diversa, ed è l'unica tabella del progetto per cui questo vale: i suoi 126 valori (42 categorie × 3 assi) non sono osservati su nessuna fonte e non sono calcolati da nessuna formula. Sono **assegnati da una persona**, con l'assistenza di un LLM che propone una prima stesura.

Questo non è un dettaglio da dichiarare in fondo al documento fra i limiti. È la proprietà che definisce la feature, e la spec la mette qui, prima di ogni requisito, perché ogni altra decisione — come si costruisce il contenuto, chi lo approva, che etichetta di fonte porta, perché la confidenza dei tre KPI che lo consumano non può salire — discende da questo fatto e non avrebbe senso letta prima di saperlo.

---

## Le decisioni che questa spec prende

Sono otto. Ciascuna riporta le opzioni sul tavolo dove ce n'erano, la decisione presa, la sua ragione, e dove va dichiarata. I requisiti che le rendono verificabili stanno più sotto.

---

### D1 — Un LLM propone, una persona decide: i quattro passi e il loro ordine

**Il contesto**: `DA-1` della roadmap, risolta il 2026-08-19, ammette l'uso di un LLM per proporre le 42 righe, a condizione che **nessuno script chiami mai il modello**: è un passaggio non riproducibile il cui esito si congela in un artefatto versionato, sul modello del benchmark della `004`, con derivazione a valle deterministica.

**La decisione**: quattro passi, in quest'ordine, che è esso stesso il presidio contro la deriva da autore a ratificatore che la roadmap identifica come rischio principale.

1. **Il criterio.** Un documento — `docs/mood_assignment_criteria.md` — dichiara che cosa significa ogni valore di ciascun asse per una categoria video, su quale base, con esempi di ancoraggio agli estremi (0 e 1) per ciascun asse. È scritto e **committato da solo**: nel suo commit non esiste alcun valore della tabella, nemmeno di prova.
2. **La proposta.** Un LLM, invocato **manualmente e una sola volta**, riceve il criterio e produce una prima stesura delle 42 righe. Prompt, nome del modello e data di invocazione sono versionati insieme alla proposta in `data/curated/dim_category_mood_proposal.json`.
3. **La revisione.** Una sessione in contesto pulito — che riceve **solo** la proposta e il criterio, nient'altro (vedi D7) — verifica ogni riga contro il criterio del passo 1, che è l'unico metro ammesso, e produce la tabella rivista insieme al conteggio di quante righe ha spostato rispetto alla proposta.
4. **Il congelamento.** La tabella rivista si scrive in `data/curated/dim_category_mood.json`, versionata e mai rigenerata da uno script.

**La ragione dell'ordine**: è la stessa della `FR-011a` della `004` — un criterio fissato prima che il valore esista è distinguibile da un criterio adattato al valore dopo che è comparso, e la distinzione regge solo se l'ordine è verificabile in history git e non solo asserito in prosa.

---

### D2 — La scala dei tre assi è ereditata, non ridecisa

`docs/data_model.md` §11 fissa che sul lato musicale i tre assi sono `energy`, `valence`, `danceability`, letti dalla fonte **senza alcuna trasformazione**, su scala `0-1`. Questa spec non riapre quella decisione: la eredita come **vincolo non negoziabile** sul lato video.

**La decisione**: `mood_energy`, `mood_valence`, `mood_danceability` sono espressi sulla stessa scala `0-1`, con lo stesso significato di estremo — `0` e `1` sul lato video devono corrispondere a ciò che `0` e `1` significano sul lato musicale per lo stesso asse, non a una scala qualitativa a cinque livelli poi rinormalizzata. È il criterio del passo 1 di D1 a doverlo garantire, dichiarando per ciascun asse a quale osservazione musicale ancorare i propri estremi.

**La ragione per cui questo è l'obbligo che conta di più**: §15 lo dice esplicitamente — una scala diversa anche su un solo asse rende la distanza di `BQ2-K2` priva di significato **senza produrre alcun errore visibile**. Il numero esce comunque, sembra ragionevole, e nessun controllo di questo progetto lo intercetta: è un difetto che solo la revisione in contesto pulito può trovare, verificando gli esempi di ancoraggio del criterio contro osservazioni reali del lato musicale.

---

### D3 — Etichetta di fonte: `Sintetico`, non `Benchmark (esterno)`

**Il problema**: la tabella nasce da una proposta di un LLM, che potrebbe far pensare a un output "esterno" da citare come tale.

**La decisione**: la fonte è **`Sintetico`**, non `Benchmark (esterno)`. Le cinque condizioni sui benchmark (emendamento 1.1.0 della constitution) **non si applicano**: un benchmark è un dato osservato su un operatore terzo e trasferito a StreamWave, e qui non c'è alcun operatore terzo — c'è un'assegnazione dell'analista, assistita da un modello linguistico ma **decisa e approvata da una persona** contro un criterio che quella stessa persona ha scritto. È lo stesso caso dei fattori di banda della `004`, etichettati `Sintetico` come "stipulazione dell'analista: dichiara la fiducia nel trasferimento, non misura alcuna varianza" — qui la stipulazione non riguarda una banda ma un valore diretto, ma la natura di fonte è identica.

**La ragione per cui la distinzione conta**: `Benchmark (esterno)` implicherebbe una citazione puntuale verificabile presso terzi, che qui non esiste e non può esistere — non c'è nulla da citare fuori dal repository. Etichettarla come benchmark presterebbe alla tabella un'autorità che non ha.

---

### D4 — La confidenza resta `media`, per obbligo di §15 e non per scelta

**La decisione**: i tre KPI che leggono `dim_category_mood` (`BQ1-K3`, `BQ2-K2`, `BQ2-K3`) restano a confidenza **`media`**. Nessuna cura nella costruzione — criterio dettagliato, proposta di un modello capace, revisione riga per riga, conteggio degli spostamenti pubblicato — può farla salire ad `alta`.

**La ragione**: è il secondo obbligo non negoziabile di §15. La tabella è **costruita dall'analista**, non osservata: la cura riduce l'errore nella costruzione, non cambia la natura del dato. Questa spec non tratta la confidenza come un parametro da massimizzare — la tratta come un fatto già deciso a monte, dal modello dati, che questa feature non ha titolo per rinegoziare.

---

### D5 — Versionamento della tabella e contratto per la `007`

**Il contesto**: divergenza 10 della revisione `001`, chiusa dalla roadmap il 2026-08-19. Quattro risposte già date: costruisce la sessione della `006` sul proprio criterio; approva Valerio sull'esito della revisione in contesto pulito; una contestazione a una riga è legittima solo se cita il criterio; **le revisioni della tabella invalidano i valori già pubblicati che ne dipendono**.

**La decisione**: `dim_category_mood.json` porta un campo `version` (intero, a partire da `1`). Ogni volta che una riga viene corretta dopo il congelamento — per un errore trovato, non per un capriccio — la versione si incrementa e l'artefatto registra che cosa è cambiato e perché, sul modello di un changelog. Il **contratto per la `007`**, che consumerà i tre KPI: ogni valore pubblicato che dipende da `dim_category_mood` **deve dichiarare su quale versione della tabella è stato calcolato**. Questa spec non implementa quel requisito lato `007` — lo lascia esplicito perché la `007` lo trovi qui e non debba scoprirlo da sola.

**La ragione**: senza il legame esplicito fra valore pubblicato e versione della tabella, una correzione della tabella lascerebbe in giro numeri "giusti quando sono stati scritti e mai più riverificati" — la stessa classe di difetto del totale a ~65 ore corretto il 2026-08-17, che la roadmap cita esplicitamente come precedente da non ripetere.

---

### D6 — Chiusura della divergenza 5 della revisione `002`: il presidio sul cambio di tassonomia

**Il rilievo**: la `002` ha stabilito che `Music & Musicals` è l'unica categoria a contenuto musicale dichiarato del catalogo video, e `BQ1-K1` vi poggia. Nessuno ha mai stabilito chi si accorgerebbe se la tassonomia della fonte cambiasse — per esempio se un futuro refresh del dataset Netflix rinominasse la categoria o ne introducesse una nuova a contenuto musicale.

**La decisione**: questa feature tocca le 42 categorie una per una, quindi è quella che può fissare il presidio, e lo fissa così. `dim_category_mood` deve corrispondere **esattamente**, come insieme di chiavi, all'insieme distinto dei valori di `category` osservati in `dim_category` al momento della costruzione. La corrispondenza è una condizione verificabile — non un'osservazione affidata alla memoria di chi legge — e la sua verifica è responsabilità di **chiunque prossimo tocchi `data/raw/netflix_titles.csv` o rigeneri `dim_category`**: se quella verifica fallisce (una categoria di `dim_category` senza riga in `dim_category_mood`, o una riga di `dim_category_mood` che non corrisponde più a nessuna categoria osservata), il caso va **segnalato e non silenziato**, con la stessa regola già in uso per gli invarianti di §13-14 del modello dati.

**La ragione per cui questo chiude la divergenza**: prima non esisteva alcun oggetto la cui costruzione dipendesse dall'insieme delle 42 categorie riga per riga; ora esiste, e la sua stessa esistenza è il meccanismo di rilevazione — una tassonomia che cambia rompe l'allineamento in modo osservabile, non silenzioso, per chiunque riesegua la verifica di corrispondenza al passo successivo che tocca quella tassonomia.

---

### D7 — Chiusura della parte generale della divergenza 5 della revisione `003`: nessun attributo di record individuale

**Il rilievo**: se gli artefatti versionati possano contenere attributi di record individuali — non solo aggregati e identificativi. Il caso concreto (i tre titoli con durata riparata, nella `003`) era chiuso con i nomi registrati; la regola generale no.

**La decisione, per gli artefatti di questa feature**: **no**. Il criterio, la proposta, il verbale di revisione, la tabella congelata e il documento pubblicato **non citano titoli individuali del catalogo** — non il nome, non la trama, non il cast, non alcun altro campo specifico di una riga di `dim_title`. Gli esempi di ancoraggio richiesti dal criterio (D1, passo 1) si esprimono a livello di **categoria o di genere musicale come archetipo** — "una categoria come *Horror Movies* ancora l'estremo basso di positività", non "il film X ancora l'estremo basso di positività" — e a livello di osservazioni aggregate sul lato musicale già disponibili nel modello dati.

**La ragione**: l'assegnazione avviene a grana categoria, non a grana titolo — nessun passo del processo ha bisogno di guardare un titolo specifico per decidere il mood di una categoria — quindi la regola non toglie nulla che serva. Applicarla qui, sull'unico strato interpretativo del progetto, è anche il punto in cui il costo di sbagliare è più alto: un artefatto che citasse titoli renderebbe più facile leggere l'assegnazione come "osservata su quegli esempi" invece che come ciò che è, un giudizio dell'analista.

**Ciò che questa decisione non fa**: non generalizza la regola a tutti gli artefatti del progetto — quello resta, come per la regola sulle affermazioni derivate, un atto di governance che appartiene alla regia se la si vuole elevare oltre questa feature.

---

### D8 — Nota in loco su §15, condizione 4, di `docs/data_model.md`

**Il testo attuale**: «questo documento non dice né chi né come costruisca le righe. È una decisione aperta della roadmap, e resta aperta. Non è un vincolo: è la dichiarazione che un vincolo qui non viene posto, scritta perché nessuno la scambi per una dimenticanza.»

**La decisione**: la condizione non è più vera come scritta — `DA-1` l'ha decisa il 2026-08-19 — e va chiusa con una **nota in loco**, secondo la prassi di `CLAUDE.md`: il testo originale resta, la nota si aggiunge accanto e dichiara data, la decisione presa (un LLM propone, una persona decide, nessuno script chiama il modello a runtime — D1 di questa spec), e dove vive la motivazione per esteso (`docs/roadmap.md`, sezione «Decisioni aperte», `DA-1`). Non è una riscrittura: è un'aggiunta che chiude, sul passaggio esatto in cui il lettore la incontrerebbe.

---

## Rapporto con le feature vicine

**Questa feature non calcola KPI.** Produce la tabella che li rende calcolabili. La misura DAX, la sua espressione, e il valore che comparirà in dashboard sono della `007`, che eredita da qui il contratto di versione (D5) e il vincolo di confidenza (D4).

**Questa feature eredita §11 di `docs/data_model.md` senza toccarlo.** I campi degli assi (`energy`, `valence`, `danceability`) e le due regole di aggregazione — minimo/massimo non ponderati per `BQ1-K3`, mediana ponderata sul ponte per `BQ2-K2` — sono decisioni del modello dati, prese e chiuse. Questa spec non le ridiscute in nessun punto: le riporta solo dove servono a vincolare il proprio lavoro (D2).

**Questa feature non tocca `data/raw/` né la pipeline della `003`.** Legge l'elenco delle 42 categorie da `dim_category`, che è una derivazione del modello dati già decisa (§13), non ricostruisce nulla a monte.

---

## Perimetro

Ciò che questa feature **non** fa, e a chi spetta.

| Fuori perimetro | Ragione | A chi spetta |
|---|---|---|
| **Misure DAX**, anche in bozza | il KPI si calcola sopra la tabella, non dentro questa feature | `007` |
| **Materializzazione del modello dati in Power BI** | interazione con la GUI, fuori dal confine dell'automazione (principio V) | chore separato, tracciato in roadmap |
| **I campi degli assi e le due regole di aggregazione di §11** | decisioni già chiuse dal modello dati | `005`, già mergiata |
| **`data/raw/` e la pipeline della `003`** | nessuna lettura, nessuna riesecuzione | — |
| **Divergenza 1 della revisione `003`** (precisione profilo/rendiconto) | non riguarda questa tabella | `007` |
| **Chiamata al modello dentro uno script o una pipeline** | violerebbe la condizione della `DA-1` che rende ammissibile l'intero approccio | a nessuno: è vietato, non rinviato |
| **Emendamento alla constitution** | il principio V ammette già documentazione e dati sintetici generati con assistenza automatica; le cinque condizioni sui benchmark non si applicano (D3) | se servisse davvero, si ferma e si riporta — spetta alla regia |

---

## User Scenarios & Testing *(mandatory)*

Gli attori sono tre: **chi costruisce** (la sessione della `006`), **chi revisiona in contesto pulito** (una sessione o subagent isolato che vede solo criterio e proposta), **chi rilegge** (un membro del board, la `007`, chiunque riceva il repository).

### User Story 1 — Il criterio esiste prima di ogni valore (Priority: P1)

Chi costruisce scrive il criterio di assegnazione — che cosa significa ogni valore di ciascun asse, con esempi di ancoraggio agli estremi — e lo committa da solo, senza che alcun valore della tabella esista ancora, nemmeno di prova.

**Why this priority**: è il punto di massima leva dell'intera feature. Un criterio scritto dopo aver visto i valori — anche in perfetta buona fede — si piega a giustificarli invece di vincolarli, e nessun controllo di questo progetto potrebbe più accorgersene una volta che i 126 numeri esistono.

**Independent Test**: si apre la history git; il commit del criterio non tocca né `data/curated/dim_category_mood_proposal.json` né `data/curated/dim_category_mood.json`, e li precede.

**Acceptance Scenarios**:

1. **Given** una copia pulita del repository, **When** si cerca il primo commit che introduce `docs/mood_assignment_criteria.md`, **Then** quel commit non contiene alcun valore numerico della tabella.
2. **Given** il criterio, **When** lo si legge per ciascuno dei tre assi, **Then** dichiara la base di attribuzione e almeno un esempio di ancoraggio all'estremo basso e uno all'estremo alto, entrambi a livello di categoria o genere, mai di titolo individuale.
3. **Given** la history git, **When** si confronta il timestamp del commit del criterio con quello della proposta, **Then** il criterio precede.

---

### User Story 2 — La proposta è di un modello, invocato una volta, fuori dalla pipeline (Priority: P1)

Chi costruisce invoca manualmente un LLM con il criterio come istruzione, riceve una prima stesura delle 42 righe, e la versiona insieme a prompt, nome del modello e data.

**Why this priority**: senza questa storia non c'è nulla da revisionare, e la `DA-1` non ammette l'alternativa di scrivere le 126 cifre a mano senza la componente di lavoro con LLM che la roadmap prevede.

**Independent Test**: si apre `data/curated/dim_category_mood_proposal.json`; prompt, modello e data sono presenti e nessuno script del repository lo genera.

**Acceptance Scenarios**:

1. **Given** `data/curated/dim_category_mood_proposal.json`, **When** lo si ispeziona, **Then** contiene il prompt usato, il nome del modello, la data dell'invocazione, e 42 righe proposte sulla forma di §15 del modello dati.
2. **Given** l'intero repository, **When** si cerca una chiamata di rete verso un servizio LLM in uno script versionato, **Then** non se ne trova alcuna: l'invocazione è un passaggio manuale, non automatizzato.

---

### User Story 3 — La revisione in contesto pulito verifica riga per riga, e il conteggio degli spostamenti è pubblico (Priority: P1)

Chi revisiona riceve solo la proposta e il criterio — nessun'altra parte del repository — e verifica ogni riga contro il criterio, unico metro ammesso. Produce la tabella rivista e dichiara quante righe ha spostato rispetto alla proposta.

**Why this priority**: è il presidio contro cui l'intera decisione `DA-1` si gioca. Senza una revisione realmente indipendente dalla proposta, il lavoro del revisore scivola da autore a ratificatore — il rischio che la roadmap identifica esplicitamente.

**Independent Test**: si legge il verbale di revisione; dichiara in apertura di aver ricevuto solo criterio e proposta, e chiude con il conteggio degli spostamenti.

**Acceptance Scenarios**:

1. **Given** il verbale di revisione, **When** lo si legge in apertura, **Then** dichiara esplicitamente di aver ricevuto solo `docs/mood_assignment_criteria.md` e `data/curated/dim_category_mood_proposal.json`, e nient'altro del repository.
2. **Given** il verbale, **When** lo si legge in chiusura, **Then** dichiara il numero di righe (categoria × asse) modificate rispetto alla proposta.
3. **Given** un conteggio di spostamenti pari a zero, **When** il verbale lo dichiara, **Then** lo qualifica come ritrovamento — la proposta seguiva già il criterio — e non come conferma o successo del processo.
4. **Given** una contestazione a una riga nel verbale, **When** la si legge, **Then** cita il criterio del passo 1; una contestazione che non lo cita non è ammessa come tale.

---

### User Story 4 — La tabella congelata copre le 42 categorie sulla scala corretta, con versione dichiarata (Priority: P2)

Chi rilegge la tabella finale trova una riga per ciascuna delle 42 categorie di `dim_category`, tre valori decimali `0-1` per riga sulla stessa scala del lato musicale, e un numero di versione.

**Why this priority**: è il prodotto che i tre KPI a valle consumano direttamente. Senza copertura totale dichiarata e scala corretta, `BQ1-K3` e `BQ2-K2` producono numeri silenziosamente sbagliati o silenziosamente incompleti.

**Independent Test**: si confrontano le chiavi di `dim_category_mood.json` con l'insieme distinto di `category` in `dim_category`; coincidono, o la differenza è dichiarata esplicitamente nell'artefatto.

**Acceptance Scenarios**:

1. **Given** `data/curated/dim_category_mood.json`, **When** si contano le righe, **Then** sono 42, oppure meno con una dichiarazione esplicita di quali categorie mancano e perché.
2. **Given** i tre valori di una riga, **When** li si legge, **Then** sono numeri decimali nell'intervallo chiuso `0-1`.
3. **Given** l'artefatto, **When** lo si ispeziona, **Then** porta un campo `version` intero, a partire da `1`.
4. **Given** l'insieme delle chiavi `category` dell'artefatto, **When** lo si confronta con l'insieme distinto di `dim_category`, **Then** coincide esattamente, oppure la differenza è dichiarata (D6).

---

### Edge Cases

- **Un valore proposto dal modello cade fuori dall'intervallo `0-1`.** La revisione non lo corregge silenziosamente clippandolo: lo tratta come una riga da rivedere contro il criterio come ogni altra, e se resta fuori scala il congelamento si ferma con un errore dichiarato, non un valore artificialmente forzato in range.
- **La revisione contesta una riga senza citare il criterio.** Non è una contestazione ammissibile: è un'opinione sul mood di una categoria, e questa spec la esclude esplicitamente come metro (D1, D5 della `001`).
- **Il conteggio degli spostamenti è zero.** Va dichiarato come ritrovamento — la proposta seguiva già il criterio — non presentato come una conferma del processo (User Story 3, scenario 3).
- **La tassonomia della fonte cambia in un refresh futuro di `netflix_titles.csv`.** Il presidio di D6 rende il disallineamento verificabile meccanicamente; l'obbligo di eseguire quella verifica cade su chi tocca per primo quel dataset o la derivazione `dim_category`, non su questa feature.
- **La copertura è parziale.** È ammessa, ma va dichiarata esplicitamente nell'artefatto e nel documento pubblicato, insieme a che cosa fanno le misure a valle sulle categorie mancanti — altrimenti una categoria senza profilo sparisce silenziosamente da una media (§15).
- **Un esempio di ancoraggio nel criterio cita un titolo specifico invece di un archetipo di categoria.** Non è ammesso: viola D7. Il criterio va riscritto a livello di categoria o genere prima di essere committato.

---

## Requirements *(mandatory)*

### Il criterio (passo 1 di D1)

- **FR-001**: Il criterio di assegnazione MUST vivere in un documento versionato dedicato (`docs/mood_assignment_criteria.md`) e MUST essere committato **da solo**, in un commit che non contiene alcun valore della tabella, nemmeno di prova.
- **FR-002**: Il criterio MUST dichiarare, per ciascuno dei tre assi, che cosa significa ogni valore per una categoria video, su quale base, e MUST includere almeno un esempio di ancoraggio all'estremo basso e uno all'estremo alto per asse.
- **FR-003**: Gli esempi di ancoraggio del criterio NON DEVONO citare titoli individuali del catalogo video — nome, trama, cast o altro attributo specifico di una riga di `dim_title`. Si esprimono a livello di categoria o di genere musicale come archetipo (D7).
- **FR-004**: Il criterio MUST ancorare gli estremi di ciascun asse a osservazioni reali disponibili sul lato musicale del modello dati, in modo che chi revisiona possa verificare la scala richiesta da D2 senza ricorrere a un giudizio qualitativo indipendente.

### La proposta del modello (passo 2 di D1)

- **FR-005**: La proposta MUST provenire da un **unico** LLM, invocato **manualmente** con il criterio come istruzione. Nessuno script del repository MUST invocare il modello, né a runtime né in fase di build.
- **FR-006**: La proposta MUST essere versionata come artefatto distinto (`data/curated/dim_category_mood_proposal.json`) e MUST dichiarare, insieme alle 42 righe proposte, il prompt usato, il nome del modello e la data dell'invocazione.
- **FR-007**: La proposta NON DEVE essere trattata come la tabella finale in nessun artefatto della feature: resta un input alla revisione, non un output pubblicabile come tale.

### La revisione in contesto pulito e il congelamento (passi 3-4 di D1)

- **FR-008**: La revisione MUST ricevere **solo** il criterio (FR-001) e la proposta (FR-006), e nessun'altra parte del repository — né il modello dati, né le feature precedenti, né alcun altro contesto. È l'unico modo per verificare se le righe seguano il criterio dichiarato o lo abbiano seguito a posteriori.
- **FR-009**: Ogni contestazione a una riga in fase di revisione MUST citare il punto del criterio che la riga viola. Una contestazione priva di questo riferimento NON DEVE essere trattata come tale.
- **FR-010**: La revisione MUST produrre e pubblicare il **conteggio delle righe (categoria × asse) modificate** rispetto alla proposta. Un conteggio pari a zero MUST essere dichiarato come ritrovamento — la proposta seguiva già il criterio — e NON DEVE essere presentato come conferma del processo.
- **FR-011**: Il verbale della revisione MUST rispettare i quattro obblighi di `CLAUDE.md` per la revisione in contesto pulito — si scrive e si committa quando la revisione torna, prima di toccare la tabella finale; dichiara in apertura che cosa ha ricevuto (FR-008) e che cosa no; ancora la versione revisionata con commit e impronta; non si corregge — e vive in `specs/006-content-taxonomy-bridge/review.md`, sul modello di `specs/005-data-model-design/review.md`.
- **FR-012**: La tabella rivista dalla revisione MUST essere congelata nell'artefatto finale (`data/curated/dim_category_mood.json`) e NON DEVE essere rigenerata da alcuno script.

### Scala, copertura, versionamento (eredità di §11-15, D2, D4, D5)

- **FR-013**: I tre valori di ciascuna riga (`mood_energy`, `mood_valence`, `mood_danceability`) MUST essere decimali nell'intervallo chiuso `0-1`, sulla stessa scala e con lo stesso significato di estremo di `energy`, `valence`, `danceability` sul lato musicale, senza alcuna normalizzazione o trasformazione successiva.
- **FR-014**: La copertura attesa MUST essere totale — una riga per ciascuna delle 42 categorie distinte di `dim_category`. Una copertura parziale è ammessa solo se dichiarata esplicitamente nell'artefatto e nel documento pubblicato, insieme al comportamento delle misure a valle sulle categorie mancanti.
- **FR-015**: L'artefatto finale MUST portare un campo `version` (intero, a partire da `1`), incrementato a ogni correzione successiva al congelamento iniziale, con la ragione della correzione registrata nell'artefatto stesso.
- **FR-016**: Il documento pubblicato MUST dichiarare esplicitamente il contratto per la `007`: ogni valore pubblicato che dipende da `dim_category_mood` deve dichiarare su quale versione della tabella è stato calcolato.
- **FR-017**: La confidenza di `BQ1-K3`, `BQ2-K2` e `BQ2-K3` MUST restare **media** in ogni artefatto della feature. Nessun artefatto MUST presentarla come alta, indipendentemente dalla cura documentata nella costruzione.
- **FR-018**: La fonte dei valori di `dim_category_mood` MUST essere etichettata **`Sintetico`** in ogni artefatto rivolto al lettore. NON DEVE essere etichettata `Benchmark (esterno)`: le cinque condizioni della constitution su quella fonte non si applicano, perché non esiste un operatore terzo osservato (D3).

### Debito ereditato

- **FR-019**: `dim_category_mood` MUST essere verificata, al momento della costruzione, contro l'insieme distinto di `category` in `dim_category`: ogni categoria di `dim_category` priva di riga corrispondente, e ogni riga di `dim_category_mood` priva di categoria corrispondente, MUST essere segnalata esplicitamente, non risolta scegliendo in silenzio. L'obbligo di rieseguire questa verifica in futuro MUST essere dichiarato come responsabilità di chiunque tocchi successivamente `data/raw/netflix_titles.csv` o la derivazione di `dim_category`, chiudendo la divergenza 5 della revisione `002` (D6).
- **FR-020**: Nessun artefatto versionato di questa feature (criterio, proposta, verbale di revisione, tabella congelata, documento pubblicato) MUST contenere attributi di record individuali del catalogo video — titolo, trama, cast o altro campo specifico di una riga di `dim_title`. Sono ammessi aggregati e identificativi di categoria, chiudendo la parte generale della divergenza 5 della revisione `003` per gli artefatti di questa feature (D7).
- **FR-021**: `docs/data_model.md` §15, condizione 4, MUST ricevere una nota in loco che dichiari: data della nota, la decisione presa (`DA-1`: un LLM propone, una persona decide, nessuno script chiama il modello a runtime), e il rimando a `docs/roadmap.md`, sezione «Decisioni aperte», `DA-1`, come sede della motivazione per esteso. Il testo originale della condizione 4 NON DEVE essere riscritto o cancellato (D8).

### Documento pubblicato e controllo di coerenza

- **FR-022**: La feature MUST produrre un documento di lettura (`docs/content_taxonomy_bridge.md`) che dichiari, nell'ordine: la natura interpretativa della tabella (apertura di questa spec); i quattro passi di D1 con i relativi artefatti; il conteggio degli spostamenti della revisione (FR-010); il contratto di versione per la `007` (FR-016); i limiti dichiarati di questa feature.
- **FR-023**: Il documento pubblicato MUST entrare in `DOCUMENTS` di `scripts/check_audit_coherence.py` **sotto severità stretta**, come quarto artefatto nello spazio dei nomi della marcatura descritto in `docs/convenzioni-marcatura.md`, e MUST passare il controllo. La tabella di provenienza in coda a quel documento MUST registrare data e feature.
- **FR-024**: Ogni numerale scritto nel documento pubblicato in posizione di fatto misurato MUST portare un'ancora verso un artefatto della feature o verso un artefatto già ancorato di una feature precedente; nessun numerale MUST essere scritto in lettere per un fatto misurato (regola D5 della `003`, generale da `CLAUDE.md`).

### Obblighi che nessun automatismo esegue

- **FR-025**: La feature MUST aggiornare `README.md`: riga nella tabella di stato con link al proprio `review.md`, deliverable elencato, prosa dei deliverable estesa, sezioni `Setup` e `Struttura` allineate.
- **FR-026**: La feature MUST aggiornare `docs/roadmap.md` per registrare la chiusura di `DA-1` come **eseguita** (distinta dalla sua risoluzione di principio, già registrata il 2026-08-19) e la chiusura della divergenza 10 della revisione `001`, della divergenza 5 della revisione `002` e della parte generale della divergenza 5 della revisione `003`, ciascuna con riferimento puntuale a dove la chiusura vive in questa feature.

### Key Entities

- **Criterio di assegnazione** (`docs/mood_assignment_criteria.md`): documento versionato, committato da solo prima di ogni valore. Dichiara il significato di ciascun asse, la base di attribuzione, gli esempi di ancoraggio a livello di categoria/genere.
- **Proposta del modello** (`data/curated/dim_category_mood_proposal.json`): artefatto versionato, prodotto da un'unica invocazione manuale di un LLM. Contiene prompt, modello, data, 42 righe proposte. Input alla revisione, mai pubblicato come tabella finale.
- **Verbale di revisione** (`specs/006-content-taxonomy-bridge/review.md`): prodotto dalla sessione in contesto pulito che riceve solo criterio e proposta. Contiene la verifica riga per riga, il conteggio degli spostamenti, e — nel blocco di chiusura — come ogni contestazione è stata risolta.
- **Tabella congelata** (`data/curated/dim_category_mood.json`): l'artefatto finale, versionato con campo `version`, mai rigenerato da uno script. 42 righe attese, tre assi su scala `0-1`, chiave `category` verificata contro `dim_category`.
- **Documento pubblicato** (`docs/content_taxonomy_bridge.md`): prosa che dichiara natura interpretativa, processo, conteggio degli spostamenti, contratto di versione, limiti. Sotto severità stretta nel controllo di coerenza.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chi apre la history git trova il commit del criterio privo di qualunque valore della tabella, e precedente sia al commit della proposta sia a quello della tabella congelata.
- **SC-002**: Chi legge il verbale di revisione trova, in apertura, la dichiarazione di aver ricevuto solo criterio e proposta, e, in chiusura, il conteggio delle righe (categoria × asse) modificate rispetto alla proposta.
- **SC-003**: `dim_category_mood.json` porta una riga per ciascuna delle 42 categorie distinte di `dim_category` — o dichiara esplicitamente la differenza — con tre valori decimali `0-1` per riga e un campo `version`.
- **SC-004**: Nessun artefatto della feature presenta la fonte dei valori come `Benchmark (esterno)` o la confidenza dei tre KPI come alta.
- **SC-005**: `scripts/check_audit_coherence.py` passa in severità stretta su `docs/content_taxonomy_bridge.md`, e continua a passare sui documenti esistenti.
- **SC-006**: Nessun artefatto della feature cita un titolo, una trama o un cast specifico del catalogo video.
- **SC-007**: `README.md` e `docs/roadmap.md` riflettono la feature conclusa, verificabile a colpo d'occhio confrontando la tabella di stato del primo e la sezione «Decisioni aperte» del secondo con lo stato descritto in questa spec.

I sette criteri sono verificabili sul prodotto, da chi riceve il repository senza sapere come è stato costruito. La stima di 6 ore, revisione inclusa, è un vincolo di processo del principio III e non compare fra loro.

---

## Assumptions

- **L'insieme delle 42 categorie non cambia durante la costruzione di questa feature.** Se cambiasse a metà lavoro, la verifica di FR-019 lo intercetterebbe, ma la feature non è progettata per assorbire quel caso senza fermarsi.
- **Un solo ciclo proposta-revisione è sufficiente.** Se la revisione trovasse che il criterio stesso è carente — non le singole righe, ma la sua capacità di decidere un caso — la spec non prevede un secondo giro di proposta: il criterio va corretto e la proposta rifatta da capo, tornando al passo 1 di D1.
- **Il modello invocato al passo 2 non richiede accesso a dati proprietari di StreamWave.** Riceve solo il criterio, che è testo pubblico del repository: nessuna informazione riservata attraversa l'invocazione.
- **La `007` legge `dim_category_mood.json` così come pubblicato**, senza ricalcolarne i valori. Se li ricalcolasse, l'artefatto di questa feature diventerebbe una seconda fonte di verità, che il congelamento (FR-012) esiste per evitare.
- **`data/curated/` è il percorso corretto** per un artefatto non riproducibile e versionato, sul modello di `data/benchmarks/` della `004`. La motivazione per esteso — perché una nuova sottocartella e non `data/benchmarks/` stessa — va scritta in `data/README.md` in fase di piano, seguendo la prassi già in uso.

---

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: **BQ1 — Posizionamento** e **BQ2 — Segmento di ingresso**.
- **Contributo**: senza `dim_category_mood`, `BQ1-K3` (l'intervallo di mood occupato dal catalogo video) e `BQ2-K2` (la distanza fra il profilo mediano di un segmento musicale e quello del catalogo video) non sono calcolabili — mancherebbe l'intero lato video del confronto. `BQ2-K3`, che compone `BQ2-K1` e `BQ2-K2`, ne dipende a sua volta attraverso `BQ2-K2`. Tre KPI su otto — l'unico strato interpretativo del framework — poggiano interamente su questa tabella. Questa feature non calcola i tre KPI: costruisce l'oggetto che li rende calcolabili, con un processo tracciabile e revisionabile che è la sola difesa possibile per un dato che nessuna fonte osserva.

---

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

| Metrica | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| `mood_energy`, `mood_valence`, `mood_danceability` per ciascuna delle 42 categorie | `Sintetico` | **media** | assegnazione dell'analista, su proposta di un LLM invocato una sola volta e revisionata riga per riga in contesto pulito contro un criterio scritto e committato prima di ogni valore | valore singolo per asse, decimale `0-1` — non un range: la confidenza `media` non lo impone (a differenza della confidenza `bassa` di `BQ3`) |
| `BQ1-K3`, `BQ2-K2`, `BQ2-K3` (a valle, calcolati dalla `007`) | `Derivato` (`dim_category_mood` + dati musicali osservati) | **media**, non negoziabile | eredita la natura interpretativa della tabella; nessuna cura nella costruzione la fa salire | a discrezione della `007`, purché la confidenza dichiarata resti media |

**Assunzioni dietro i dati sintetici**, dichiarate per iscritto e versionate insieme al criterio che le implementa:

1. **Assunzione di ancoraggio di scala**: gli estremi `0` e `1` di ciascun asse video corrispondono, per significato, agli estremi osservati sul lato musicale per lo stesso asse (D2). È verificata dalla revisione in contesto pulito, non da alcun controllo automatico.
2. **Assunzione di indipendenza dal titolo**: il mood di una categoria si assegna senza guardare i titoli che la compongono (D7); ciò che il criterio ancora sono archetipi di categoria e genere, non esempi individuali.
3. **Assunzione di stabilità della tassonomia**: la tabella assume che le 42 categorie osservate al momento della costruzione restino quelle della fonte; la violazione è rilevabile, non prevenuta (D6).

**Nessuna promozione di confidenza**: i tre KPI restano a confidenza `media` in ogni artefatto della feature e di quelle a valle che la citano.

---

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: se una categoria video contenga *davvero*, in media, contenuti energici, positivi o ritmati. Il profilo di mood è un giudizio dell'analista su come quella categoria si posiziona rispetto alle altre 41, non una misura di alcuna proprietà osservabile del contenuto — nessun campo del catalogo video misura energia, positività o ritmo.
- **Non risponde a**: se due categorie video con mood simile condividano davvero pubblico. Il mood è un asse di posizionamento, non un dato comportamentale; nessuna misura di audience o di sovrapposizione di utenti esiste in questo progetto.
- **Inferenza da evitare — l'assegnazione non è una misura.** Un valore di `mood_energy` pari a `0,70` per una categoria non ha lo stesso statuto epistemico di un valore di `energy` pari a `0,70` per una traccia: il secondo è letto da un campo della fonte, il primo è deciso da una persona. Confondere i due significherebbe trattare un giudizio come un'osservazione.
- **Inferenza da evitare — la revisione riduce l'errore, non lo elimina.** Un processo a due persone (proponente artificiale, revisore umano) con un criterio scritto è più difendibile di un'assegnazione arbitraria, ma resta un giudizio. Nessuna cura nella costruzione lo trasforma in un fatto osservato, ed è per questo che la confidenza non sale (D4).
- **Inferenza da evitare — nessun lessico causale.** Che una categoria abbia un profilo di mood vicino a un segmento musicale non implica che l'una *causi* l'attrattività dell'altro, né che un utente della prima adotterebbe il secondo. È un posizionamento su tre assi comuni, non una relazione di causa.
- **Copertura del dato**: la tabella descrive le categorie osservate nel catalogo Netflix usato come proxy, fermo al 2021 (`A2` del business case). Un cambio della tassonomia della fonte in un refresh futuro rende la tabella potenzialmente disallineata, e il presidio di D6/FR-019 lo rende rilevabile ma non lo previene automaticamente.
- **Dove è esposto all'utente finale**: nel documento pubblicato (`docs/content_taxonomy_bridge.md`); nella nota in loco su §15 di `docs/data_model.md`; e — per la `007`, che eredita l'obbligo — accanto a ogni presentazione di `BQ1-K3`, `BQ2-K2` e `BQ2-K3` in dashboard, con la versione della tabella su cui il valore è calcolato (D5).
