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

Sono nove. Ciascuna riporta le opzioni sul tavolo dove ce n'erano, la decisione presa, la sua ragione, e dove va dichiarata. I requisiti che le rendono verificabili stanno più sotto.

**Nota sulla revisione della regia.** Le decisioni D6 e D9 portano, in apertura, il rilievo che le ha corrette: la prima stesura di questa spec aveva scritto un presidio che non era meccanico (R2, bloccante) e aveva confuso due revisioni distinte in una sola (R3). Un terzo rilievo della stessa revisione — l'etichetta `Sintetico` non copriva un'assegnazione dell'analista il cui valore è esso stesso il dato pubblicato — non si chiude qui: ha richiesto un emendamento alla constitution, ora **v1.2.0**, che ammette le assegnazioni dell'analista congelate in un artefatto versionato come quinta fonte dati, a cinque condizioni: criterio scritto prima del valore (D1), valore congelato e mai rigenerato (D1), numero di versione dichiarato a valle (D5), revisione indipendente con esito quantificato (D9), nessuna promozione di confidenza (D4). Questa spec le anticipava nella sostanza; questa versione le dichiara esplicitamente dove serve.

---

### D1 — Un LLM propone, una persona decide: i quattro passi e il loro ordine

**Il contesto**: `DA-1` della roadmap, risolta il 2026-08-19, ammette l'uso di un LLM per proporre le 42 righe, a condizione che **nessuno script chiami mai il modello**: è un passaggio non riproducibile il cui esito si congela in un artefatto versionato, sul modello del benchmark della `004`, con derivazione a valle deterministica.

**La decisione**: quattro passi, in quest'ordine, che è esso stesso il presidio contro la deriva da autore a ratificatore che la roadmap identifica come rischio principale.

1. **Il criterio.** Un documento — `docs/mood_assignment_criteria.md` — dichiara che cosa significa ogni valore di ciascun asse per una categoria video, su quale base, con esempi di ancoraggio agli estremi (0 e 1) per ciascun asse. È scritto e **committato da solo**: nel suo commit non esiste alcun valore della tabella, nemmeno di prova.
2. **La proposta.** Un LLM, invocato **manualmente e una sola volta**, riceve il criterio e produce una prima stesura delle 42 righe. Prompt, nome del modello e data di invocazione sono versionati insieme alla proposta in `data/curated/dim_category_mood_proposal.json`.
3. **La verifica indipendente.** Chi non ha prodotto la proposta — ricevendo **solo** la proposta e il criterio, nient'altro — verifica ogni riga contro il criterio del passo 1, che è l'unico metro ammesso, e produce la tabella rivista insieme al conteggio di quante righe ha spostato rispetto alla proposta. Non è la revisione in contesto pulito di `CLAUDE.md`: è un passo di lavorazione distinto, chiuso da D9.
4. **Il congelamento.** La tabella rivista si scrive in `data/curated/dim_category_mood.json`, versionata e mai rigenerata da uno script.

**La ragione dell'ordine**: è la stessa della `FR-011a` della `004` — un criterio fissato prima che il valore esista è distinguibile da un criterio adattato al valore dopo che è comparso, e la distinzione regge solo se l'ordine è verificabile in history git e non solo asserito in prosa.

---

### D2 — La scala dei tre assi è ereditata, non ridecisa

`docs/data_model.md` §11 fissa che sul lato musicale i tre assi sono `energy`, `valence`, `danceability`, letti dalla fonte **senza alcuna trasformazione**, su scala `0-1`. Questa spec non riapre quella decisione: la eredita come **vincolo non negoziabile** sul lato video.

**La decisione**: `mood_energy`, `mood_valence`, `mood_danceability` sono espressi sulla stessa scala `0-1`, con lo stesso significato di estremo — `0` e `1` sul lato video devono corrispondere a ciò che `0` e `1` significano sul lato musicale per lo stesso asse, non a una scala qualitativa a cinque livelli poi rinormalizzata. È il criterio del passo 1 di D1 a doverlo garantire, dichiarando per ciascun asse a quale osservazione musicale ancorare i propri estremi.

**La ragione per cui questo è l'obbligo che conta di più**: §15 lo dice esplicitamente — una scala diversa anche su un solo asse rende la distanza di `BQ2-K2` priva di significato **senza produrre alcun errore visibile**. Il numero esce comunque, sembra ragionevole, e nessun controllo di questo progetto lo intercetta: è un difetto che solo la verifica indipendente della proposta (D9.1) può trovare, verificando gli esempi di ancoraggio del criterio contro osservazioni reali del lato musicale.

---

### D3 — Etichetta di fonte: `Sintetico`, non `Benchmark (esterno)`

**Il problema**: la tabella nasce da una proposta di un LLM, che potrebbe far pensare a un output "esterno" da citare come tale.

**La decisione**: la fonte è **`Sintetico`**, non `Benchmark (esterno)`. Le cinque condizioni sui benchmark (emendamento 1.1.0 della constitution) **non si applicano**: un benchmark è un dato osservato su un operatore terzo e trasferito a StreamWave, e qui non c'è alcun operatore terzo — c'è un'assegnazione dell'analista, assistita da un modello linguistico ma **decisa e approvata da una persona** contro un criterio che quella stessa persona ha scritto. È lo stesso caso dei fattori di banda della `004`, etichettati `Sintetico` come "stipulazione dell'analista: dichiara la fiducia nel trasferimento, non misura alcuna varianza" — qui la stipulazione non riguarda una banda ma un valore diretto, ma la natura di fonte è identica.

**La ragione per cui la distinzione conta**: `Benchmark (esterno)` implicherebbe una citazione puntuale verificabile presso terzi, che qui non esiste e non può esistere — non c'è nulla da citare fuori dal repository. Etichettarla come benchmark presterebbe alla tabella un'autorità che non ha.

**Nota — l'etichetta `Sintetico` da sola non bastava, ed è quello che ha prodotto l'emendamento.** La prima stesura di questa decisione si fermava qui, assumendo che l'etichetta esistente coprisse il caso. La revisione della regia ha trovato che non era così alla lettera: la constitution, fino alla v1.1.0, definiva `Sintetico` come «dati sintetici generati da script versionati», e qui nessuno script genera nulla — è la condizione stessa che rende ammissibile `DA-1`. La regia ha risposto con l'**emendamento 1.2.0**, che ammette le assegnazioni dell'analista congelate in un artefatto versionato come quinta fonte, sotto l'etichetta `Sintetico`, a cinque condizioni. D1, D4, D5 e D9 di questa spec le soddisfano; FR-018 lo dichiara.

---

### D4 — La confidenza resta `media`, per obbligo di §15 e non per scelta

**La decisione**: i tre KPI che leggono `dim_category_mood` (`BQ1-K3`, `BQ2-K2`, `BQ2-K3`) restano a confidenza **`media`**. Nessuna cura nella costruzione — criterio dettagliato, proposta di un modello capace, revisione riga per riga, conteggio degli spostamenti pubblicato — può farla salire ad `alta`.

**La ragione**: è il secondo obbligo non negoziabile di §15. La tabella è **costruita dall'analista**, non osservata: la cura riduce l'errore nella costruzione, non cambia la natura del dato. Questa spec non tratta la confidenza come un parametro da massimizzare — la tratta come un fatto già deciso a monte, dal modello dati, che questa feature non ha titolo per rinegoziare.

---

### D5 — Versionamento della tabella e contratto per la `007`

**Il contesto**: divergenza 10 della revisione `001`, chiusa dalla roadmap il 2026-08-19. Quattro risposte già date: costruisce la sessione della `006` sul proprio criterio; approva Valerio sull'esito della verifica indipendente della proposta — D9.1, che è il passo a cui la formulazione della roadmap si riferiva prima che D9 distinguesse le due revisioni; una contestazione a una riga è legittima solo se cita il criterio; **le revisioni della tabella invalidano i valori già pubblicati che ne dipendono**.

**La decisione**: `dim_category_mood.json` porta un campo `version` (intero, a partire da `1`). Ogni volta che una riga viene corretta dopo il congelamento — per un errore trovato, non per un capriccio — la versione si incrementa e l'artefatto registra che cosa è cambiato e perché, sul modello di un changelog. Il **contratto per la `007`**, che consumerà i tre KPI: ogni valore pubblicato che dipende da `dim_category_mood` **deve dichiarare su quale versione della tabella è stato calcolato**. Questa spec non implementa quel requisito lato `007` — lo lascia esplicito perché la `007` lo trovi qui e non debba scoprirlo da sola.

**La ragione**: senza il legame esplicito fra valore pubblicato e versione della tabella, una correzione della tabella lascerebbe in giro numeri "giusti quando sono stati scritti e mai più riverificati" — la stessa classe di difetto del totale a ~65 ore corretto il 2026-08-17, che la roadmap cita esplicitamente come precedente da non ripetere.

---

### D6 — Chiusura della divergenza 5 della revisione `002`: il presidio è un controllo che fallisce, non un promemoria *(corretta in risposta a R2, bloccante)*

**Il rilievo**: la `002` ha stabilito che `Music & Musicals` è l'unica categoria a contenuto musicale dichiarato del catalogo video, e `BQ1-K1` vi poggia. Nessuno ha mai stabilito chi si accorgerebbe se la tassonomia della fonte cambiasse. La prima stesura di questa decisione scriveva il presidio come un'obbligazione su una persona futura — «chiunque prossimo tocchi `data/raw/netflix_titles.csv`» — che è **esattamente** il «qualcuno se ne accorge» che la divergenza 5 della `002` lamentava: un'obbligazione dichiarata, non un meccanismo che la faccia rispettare.

**La decisione**: il presidio è un **controllo che fallisce**, non una responsabilità che qualcuno deve ricordarsi di eseguire. La strada esiste ed è già a portata: `reports/cleaning_report.json` porta, in `catalogs.netflix_categories_normalized`, le 42 categorie osservate dalla pipeline della `003` — un artefatto **già versionato**, che **non richiede `data/raw/`**, e che `scripts/check_audit_coherence.py` **apre già** come uno dei tre artefatti uniti nel proprio spazio dei nomi. Il controllo viene esteso (FR-019) a confrontare l'insieme delle chiavi `category` di `data/curated/dim_category_mood.json` con quella lista, e a **fallire — uscita diversa da zero, come ogni altro errore del controllo — se i due insiemi divergono**: una categoria della lista normalizzata priva di riga nella tabella dei mood, o una riga della tabella dei mood che non corrisponde più a nessuna categoria della lista.

**La ragione per cui questo è meccanico e il precedente non lo era**: chiunque riesegua il controllo — non solo chi per caso si trova a toccare la tassonomia della fonte — viene fermato se i due insiemi divergono, su qualunque copia del repository e in qualunque momento. Non serve che una persona se ne ricordi: serve solo che il controllo giri, ed è già una condizione sotto severità stretta (FR-023). È la stessa differenza, applicata qui, fra un controllo che elenca e uno che ferma, che regge già la severità stretta del progetto.

**L'obbligazione scritta non sparisce: cambia ruolo.** Resta utile come **complemento** — chi tocca la tassonomia della fonte trova, in documentazione, la dichiarazione che un controllo lo aspetta — ma non è più il meccanismo su cui la chiusura della divergenza si regge. Il meccanismo è il controllo che fallisce.

---

### D7 — Chiusura della parte generale della divergenza 5 della revisione `003`: nessun attributo di record individuale

**Il rilievo**: se gli artefatti versionati possano contenere attributi di record individuali — non solo aggregati e identificativi. Il caso concreto (i tre titoli con durata riparata, nella `003`) era chiuso con i nomi registrati; la regola generale no.

**La decisione, per gli artefatti di questa feature**: **no**. Il criterio, la proposta, il registro di verifica indipendente, la tabella congelata, il verbale della revisione in contesto pulito e il documento pubblicato **non citano titoli individuali del catalogo** — non il nome, non la trama, non il cast, non alcun altro campo specifico di una riga di `dim_title`. Gli esempi di ancoraggio richiesti dal criterio (D1, passo 1) si esprimono a livello di **categoria o di genere musicale come archetipo** — "una categoria come *Horror Movies* ancora l'estremo basso di positività", non "il film X ancora l'estremo basso di positività" — e a livello di osservazioni aggregate sul lato musicale già disponibili nel modello dati.

**La ragione**: l'assegnazione avviene a grana categoria, non a grana titolo — nessun passo del processo ha bisogno di guardare un titolo specifico per decidere il mood di una categoria — quindi la regola non toglie nulla che serva. Applicarla qui, sull'unico strato interpretativo del progetto, è anche il punto in cui il costo di sbagliare è più alto: un artefatto che citasse titoli renderebbe più facile leggere l'assegnazione come "osservata su quegli esempi" invece che come ciò che è, un giudizio dell'analista.

**Ciò che questa decisione non fa**: non generalizza la regola a tutti gli artefatti del progetto — quello resta, come per la regola sulle affermazioni derivate, un atto di governance che appartiene alla regia se la si vuole elevare oltre questa feature.

---

### D8 — Nota in loco su §15, condizione 4, di `docs/data_model.md`

**Il testo attuale**: «questo documento non dice né chi né come costruisca le righe. È una decisione aperta della roadmap, e resta aperta. Non è un vincolo: è la dichiarazione che un vincolo qui non viene posto, scritta perché nessuno la scambi per una dimenticanza.»

**La decisione**: la condizione non è più vera come scritta — `DA-1` l'ha decisa il 2026-08-19 — e va chiusa con una **nota in loco**, secondo la prassi di `CLAUDE.md`: il testo originale resta, la nota si aggiunge accanto e dichiara data, la decisione presa (un LLM propone, una persona decide, nessuno script chiama il modello a runtime — D1 di questa spec), e dove vive la motivazione per esteso (`docs/roadmap.md`, sezione «Decisioni aperte», `DA-1`). Non è una riscrittura: è un'aggiunta che chiude, sul passaggio esatto in cui il lettore la incontrerebbe.

---

### D9 — Due revisioni distinte, in momenti diversi, con oggetti diversi *(chiusura di R3)*

**Il rilievo**: la prima stesura dava alla «revisione» del passo 3 solo il criterio e la proposta — corretto per verificare le 126 righe, ma quella verifica **non è** la revisione in contesto pulito che `CLAUDE.md` prescrive per ogni feature. Ne conseguiva che `docs/content_taxonomy_bridge.md`, il documento pubblicato, sarebbe arrivato su `main` senza che nessuno lo avesse letto isolato dal resto del repository — la `006` sarebbe stata la **prima feature su sei** a farlo — e un verbale unico avrebbe mascherato l'assenza invece di dichiararla.

**La decisione**: sono due controlli, in momenti diversi, con oggetti diversi, e questa spec li tiene distinti invece di farne collassare uno nell'altro.

1. **La verifica indipendente della proposta** — condizione 4 della fonte «assegnazione dell'analista» ammessa dalla constitution v1.2.0: l'assegnazione è verificata da chi non l'ha prodotta, contro il criterio del passo 1 e nessun altro metro, con l'esito versionato insieme alla misura di quanto ha corretto. È un **passo di lavorazione**, avviene **prima del congelamento** (passo 3 di D1), e il suo oggetto è la proposta. Non richiede l'isolamento stretto da subagent della revisione in contesto pulito, perché la condizione che la constitution pone qui è l'**indipendenza di chi verifica**, non l'assenza di contesto: chi verifica deve poter leggere il criterio con piena cognizione di causa, non ignorare che il resto del progetto esiste.
2. **La revisione in contesto pulito del documento pubblicato** — l'obbligo generale di `CLAUDE.md`, identico nella forma a quello già eseguito per le feature `002`-`005`: un revisore riceve **solo** `docs/content_taxonomy_bridge.md`, nessun altro file del repository — non il criterio, non la proposta, non la tabella congelata — secondo il protocollo già in uso (modello: `specs/005-data-model-design/review.md`). Avviene **alla fine**, dopo che il documento esiste, e produce `specs/006-content-taxonomy-bridge/review.md` con i quattro obblighi di `CLAUDE.md`.

**Perché non è la stessa cosa letta due volte**: la prima verifica se 126 valori seguono un criterio — un controllo quantitativo, riga per riga, contro un metro tecnico che non lascia spazio all'opinione. La seconda verifica se il documento che *racconta* quella costruzione contiene affermazioni derivate senza sostegno o limiti taciuti — un controllo qualitativo sulla prosa, della stessa natura di ogni altra revisione in contesto pulito del progetto. Un solo passaggio non può fare bene entrambe le cose: chi confronta 126 numeri con un criterio non sta leggendo la prosa con l'occhio di chi cerca un'inferenza indebita, e chi legge la prosa isolato dal resto non ha — e non deve avere — il criterio davanti per ricontrollare i numeri.

**Sul costo, e sulla scomposizione**: la prima verifica è meccanica — dell'ordine dei minuti, non delle ore. La seconda è la revisione standard del progetto, con il suo costo consueto. Le 6 ore stimate reggono. Il confine fra le due è però anche il confine più utile per una scomposizione, se il piano ne trova bisogno: vedi «Stima e scomposizione» più sotto.

---

## Rapporto con le feature vicine

**Questa feature non calcola KPI.** Produce la tabella che li rende calcolabili. La misura DAX, la sua espressione, e il valore che comparirà in dashboard sono della `007`, che eredita da qui il contratto di versione (D5) e il vincolo di confidenza (D4).

**Questa feature eredita §11 di `docs/data_model.md` senza toccarlo.** I campi degli assi (`energy`, `valence`, `danceability`) e le due regole di aggregazione — minimo/massimo non ponderati per `BQ1-K3`, mediana ponderata sul ponte per `BQ2-K2` — sono decisioni del modello dati, prese e chiuse. Questa spec non le ridiscute in nessun punto: le riporta solo dove servono a vincolare il proprio lavoro (D2).

**Questa feature non tocca `data/raw/` né la pipeline della `003`.** Legge l'elenco delle 42 categorie da `catalogs.netflix_categories_normalized` (`reports/cleaning_report.json`), un artefatto già versionato dalla `003` che non richiede `data/raw/` (D6); non ricostruisce nulla a monte. Per costruzione di §13 del modello dati, quell'insieme coincide con i valori distinti di `category` che `dim_category` porterà una volta materializzata.

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
| **Emendamento alla constitution** | è servito davvero: la revisione della regia ha trovato che l'etichetta `Sintetico` non copriva un'assegnazione dell'analista il cui valore è esso stesso il dato pubblicato (D3). Il protocollo di questa riga ha funzionato come dichiarato — la spec non lo ha scritto da sola, l'ha segnalato, e la regia ha prodotto **constitution v1.2.0** | fatto, dalla regia — non da questa feature |

---

## User Scenarios & Testing *(mandatory)*

Gli attori sono quattro: **chi costruisce** (la sessione della `006`), **chi verifica** la proposta contro il criterio senza averla prodotta (D9.1), **chi revisiona in contesto pulito** il documento pubblicato, vedendo solo quello (D9.2), **chi rilegge** (un membro del board, la `007`, chiunque riceva il repository).

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

### User Story 3 — La proposta è verificata da chi non l'ha prodotta, e il conteggio degli spostamenti è pubblico (Priority: P1)

Chi verifica riceve la proposta e il criterio, controlla ogni riga contro il criterio — unico metro ammesso — e non è la persona (o la sessione) che ha ottenuto la proposta dal modello. Il numero di righe spostate rispetto alla proposta si scrive nell'artefatto congelato, non solo in prosa altrove.

**Why this priority**: è la condizione 4 della fonte «assegnazione dell'analista» della constitution v1.2.0, ed è il presidio contro cui l'intera decisione `DA-1` si gioca. Senza indipendenza reale fra chi propone e chi verifica, il lavoro scivola da autore a ratificatore — il rischio che la roadmap identifica esplicitamente. **Non è** la revisione in contesto pulito di `CLAUDE.md`: è un passo di lavorazione distinto, chiuso da D9.

**Independent Test**: si confronta chi ha ottenuto la proposta con chi firma la verifica; sono persone o sessioni diverse. Il campo del conteggio spostamenti in `data/curated/dim_category_mood.json` non è vuoto.

**Acceptance Scenarios**:

1. **Given** la proposta e il criterio, **When** la verifica avviene, **Then** chi la esegue non ha prodotto la proposta.
2. **Given** l'artefatto congelato, **When** lo si ispeziona, **Then** riporta il numero di righe (categoria × asse) modificate rispetto alla proposta.
3. **Given** un conteggio pari a zero, **When** lo si dichiara, **Then** è qualificato come ritrovamento — la proposta seguiva già il criterio — e non come conferma o successo del processo.
4. **Given** una contestazione a una riga, **When** la si legge, **Then** cita il punto del criterio violato; una contestazione priva di questo riferimento non è ammessa come tale.

---

### User Story 4 — La tabella congelata copre le 42 categorie sulla scala corretta, con versione dichiarata (Priority: P2)

Chi rilegge la tabella finale trova una riga per ciascuna delle 42 categorie di `catalogs.netflix_categories_normalized`, tre valori decimali `0-1` per riga sulla stessa scala del lato musicale, e un numero di versione.

**Why this priority**: è il prodotto che i tre KPI a valle consumano direttamente. Senza copertura totale dichiarata e scala corretta, `BQ1-K3` e `BQ2-K2` producono numeri silenziosamente sbagliati o silenziosamente incompleti.

**Independent Test**: si confrontano le chiavi di `dim_category_mood.json` con `catalogs.netflix_categories_normalized`; coincidono, o la differenza è dichiarata esplicitamente nell'artefatto.

**Acceptance Scenarios**:

1. **Given** `data/curated/dim_category_mood.json`, **When** si contano le righe, **Then** sono 42, oppure meno con una dichiarazione esplicita di quali categorie mancano e perché.
2. **Given** i tre valori di una riga, **When** li si legge, **Then** sono numeri decimali nell'intervallo chiuso `0-1`.
3. **Given** l'artefatto, **When** lo si ispeziona, **Then** porta un campo `version` intero, a partire da `1`.
4. **Given** l'insieme delle chiavi `category` dell'artefatto, **When** `scripts/check_audit_coherence.py` lo confronta con `catalogs.netflix_categories_normalized`, **Then** il controllo **fallisce** se i due insiemi divergono, e non si limita ad avvisare (D6, FR-019).

---

### User Story 5 — Il documento pubblicato passa la revisione in contesto pulito standard prima di arrivare su `main` (Priority: P2)

Chi revisiona il documento riceve **solo** `docs/content_taxonomy_bridge.md`, secondo lo stesso protocollo isolato delle feature precedenti, e produce un verbale prima che il documento venga corretto.

**Why this priority**: senza questa storia la `006` sarebbe la prima feature su sei a pubblicare un documento mai letto isolato dal resto del repository — un'omissione che un verbale unico avrebbe mascherato invece di dichiararla (D9, chiusura di R3).

**Independent Test**: si legge `specs/006-content-taxonomy-bridge/review.md`; dichiara in apertura di aver ricevuto solo il documento pubblicato, con commit e impronta della versione letta, e precede in history git le correzioni al documento.

**Acceptance Scenarios**:

1. **Given** il verbale, **When** lo si legge in apertura, **Then** dichiara di aver ricevuto solo `docs/content_taxonomy_bridge.md` e nient'altro del repository — né il criterio, né la proposta, né la tabella congelata.
2. **Given** la history git, **When** si confronta il commit del verbale con quello delle eventuali correzioni al documento, **Then** il verbale precede.
3. **Given** il blocco di chiusura del verbale, **When** lo si legge, **Then** dichiara come ogni rilievo è stato chiuso — risolvendolo, indebolendo l'affermazione, respingendolo con la prova, o rinviandolo.

---

### Edge Cases

- **Un valore proposto dal modello cade fuori dall'intervallo `0-1`.** La verifica indipendente non lo corregge silenziosamente clippandolo: lo tratta come una riga da rivedere contro il criterio come ogni altra, e se resta fuori scala il congelamento si ferma con un errore dichiarato, non un valore artificialmente forzato in range.
- **La verifica contesta una riga senza citare il criterio.** Non è una contestazione ammissibile: è un'opinione sul mood di una categoria, e questa spec la esclude esplicitamente come metro (D1, D5 della `001`).
- **Il conteggio degli spostamenti è zero.** Va dichiarato come ritrovamento — la proposta seguiva già il criterio — non presentato come una conferma del processo (User Story 3, scenario 3).
- **La tassonomia della fonte cambia in un refresh futuro di `netflix_titles.csv`.** `scripts/check_audit_coherence.py` fallisce alla prima esecuzione successiva, perché l'insieme delle chiavi di `dim_category_mood.json` non coincide più con `catalogs.netflix_categories_normalized` rigenerato dalla pipeline (D6). Il fallimento non dipende da chi si ricorda di controllare: dipende solo dal controllo essere eseguito, ed è già una condizione sotto severità stretta.
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

### La verifica indipendente della proposta (passo 3 di D1; condizione 4, constitution v1.2.0) — vedi D9

- **FR-008**: La proposta MUST essere verificata da chi non l'ha prodotta, contro **solo** il criterio (FR-001) e nessun'altra parte del repository — né il modello dati, né le feature precedenti, né alcun altro contesto. È l'unico modo per verificare se le righe seguano il criterio dichiarato o lo abbiano seguito a posteriori. Questo passo NON DEVE essere confuso con la revisione in contesto pulito di `CLAUDE.md` (FR-011a): è un passo di lavorazione interno alla costruzione della tabella, non richiede l'isolamento stretto da subagent, e avviene prima del congelamento.
- **FR-009**: Ogni contestazione a una riga in fase di verifica MUST citare il punto del criterio che la riga viola. Una contestazione priva di questo riferimento NON DEVE essere trattata come tale.
- **FR-010**: La verifica MUST produrre il **conteggio delle righe (categoria × asse) modificate** rispetto alla proposta, e quel conteggio MUST essere registrato come campo dedicato nell'artefatto congelato (FR-012), non solo dichiarato in prosa altrove. Un conteggio pari a zero MUST essere dichiarato come ritrovamento — la proposta seguiva già il criterio — e NON DEVE essere presentato come conferma del processo.

### Il congelamento (passo 4 di D1)

- **FR-012**: La tabella verificata MUST essere congelata nell'artefatto finale (`data/curated/dim_category_mood.json`) e NON DEVE essere rigenerata da alcuno script.

### La revisione in contesto pulito del documento pubblicato (obbligo generale di `CLAUDE.md`) — vedi D9

- **FR-011a**: `docs/content_taxonomy_bridge.md` MUST essere sottoposto a una revisione in contesto pulito **distinta e successiva** a FR-008–FR-010, condotta secondo il protocollo già in uso nel progetto: un revisore riceve **solo** il documento pubblicato — non il criterio, non la proposta, non la tabella congelata, non alcun altro file del repository — sul modello di `specs/005-data-model-design/review.md`.
- **FR-011b**: Il verbale di questa revisione MUST rispettare i quattro obblighi di `CLAUDE.md` — si scrive e si committa quando la revisione torna, prima di correggere il documento; dichiara in apertura che cosa ha letto e che cosa no (FR-011a); ancora la versione letta con commit e impronta; non si corregge, con un blocco di chiusura che dichiara come ogni rilievo è stato chiuso — e vive in `specs/006-content-taxonomy-bridge/review.md`.

### Scala, copertura, versionamento (eredità di §11-15, D2, D4, D5)

- **FR-013**: I tre valori di ciascuna riga (`mood_energy`, `mood_valence`, `mood_danceability`) MUST essere decimali nell'intervallo chiuso `0-1`, sulla stessa scala e con lo stesso significato di estremo di `energy`, `valence`, `danceability` sul lato musicale, senza alcuna normalizzazione o trasformazione successiva.
- **FR-014**: La copertura attesa MUST essere totale — una riga per ciascuna delle 42 categorie elencate in `catalogs.netflix_categories_normalized` (`reports/cleaning_report.json`), che per costruzione di §13 del modello dati coincidono con l'insieme distinto di `category` che `dim_category` porterà una volta materializzata. Una copertura parziale è ammessa solo se dichiarata esplicitamente nell'artefatto e nel documento pubblicato, insieme al comportamento delle misure a valle sulle categorie mancanti.
- **FR-015**: L'artefatto finale MUST portare un campo `version` (intero, a partire da `1`), incrementato a ogni correzione successiva al congelamento iniziale, con la ragione della correzione registrata nell'artefatto stesso.
- **FR-016**: Il documento pubblicato MUST dichiarare esplicitamente il contratto per la `007`: ogni valore pubblicato che dipende da `dim_category_mood` deve dichiarare su quale versione della tabella è stato calcolato.
- **FR-017**: La confidenza di `BQ1-K3`, `BQ2-K2` e `BQ2-K3` MUST restare **media** in ogni artefatto della feature. Nessun artefatto MUST presentarla come alta, indipendentemente dalla cura documentata nella costruzione.
- **FR-018**: La fonte dei valori di `dim_category_mood` MUST essere etichettata **`Sintetico`** in ogni artefatto rivolto al lettore. NON DEVE essere etichettata `Benchmark (esterno)`: le cinque condizioni della constitution su quella fonte non si applicano, perché non esiste un operatore terzo osservato (D3).

### Debito ereditato

- **FR-019**: `scripts/check_audit_coherence.py` MUST essere esteso a confrontare l'insieme delle chiavi `category` di `data/curated/dim_category_mood.json` con l'insieme `catalogs.netflix_categories_normalized` già letto da `reports/cleaning_report.json`, e MUST **fallire** — uscita diversa da zero, non un avviso — se i due insiemi non coincidono esattamente. È il meccanismo che chiude la divergenza 5 della revisione `002` (D6). La responsabilità di rieseguire il controllo quando la tassonomia della fonte cambia resta dichiarata in documentazione come complemento, non come sostituto del meccanismo.
- **FR-020**: Nessun artefatto versionato di questa feature (criterio, proposta, registro di verifica indipendente, tabella congelata, verbale della revisione in contesto pulito, documento pubblicato) MUST contenere attributi di record individuali del catalogo video — titolo, trama, cast o altro campo specifico di una riga di `dim_title`. Sono ammessi aggregati e identificativi di categoria, chiudendo la parte generale della divergenza 5 della revisione `003` per gli artefatti di questa feature (D7).
- **FR-021**: `docs/data_model.md` §15, condizione 4, MUST ricevere una nota in loco che dichiari: data della nota, la decisione presa (`DA-1`: un LLM propone, una persona decide, nessuno script chiama il modello a runtime), e il rimando a `docs/roadmap.md`, sezione «Decisioni aperte», `DA-1`, come sede della motivazione per esteso. Il testo originale della condizione 4 NON DEVE essere riscritto o cancellato (D8).

### Documento pubblicato e controllo di coerenza

- **FR-022**: La feature MUST produrre un documento di lettura (`docs/content_taxonomy_bridge.md`) che dichiari, nell'ordine: la natura interpretativa della tabella (apertura di questa spec); i quattro passi di D1 con i relativi artefatti, comprese le due revisioni distinte di D9; il conteggio degli spostamenti della verifica indipendente (FR-010); il contratto di versione per la `007` (FR-016); i limiti dichiarati di questa feature.
- **FR-023**: Il documento pubblicato MUST entrare in `DOCUMENTS` di `scripts/check_audit_coherence.py` **sotto severità stretta**, come quinto documento verificato dal controllo. I valori di `data/curated/dim_category_mood.json` MUST entrare in `ARTIFACTS` come quarto artefatto unito nello spazio dei nomi della marcatura, con la stessa verifica di collisione già in uso per i tre esistenti. `docs/convenzioni-marcatura.md` MUST registrare entrambi nella propria tabella di provenienza, con data e feature.
- **FR-024**: Ogni numerale scritto nel documento pubblicato in posizione di fatto misurato MUST portare un'ancora verso un artefatto della feature o verso un artefatto già ancorato di una feature precedente; nessun numerale MUST essere scritto in lettere per un fatto misurato (regola D5 della `003`, generale da `CLAUDE.md`).

### Obblighi che nessun automatismo esegue

- **FR-025**: La feature MUST aggiornare `README.md`: riga nella tabella di stato con link al proprio `review.md`, deliverable elencato, prosa dei deliverable estesa, sezioni `Setup` e `Struttura` allineate.
- **FR-026**: La feature MUST aggiornare `docs/roadmap.md` per registrare la chiusura di `DA-1` come **eseguita** (distinta dalla sua risoluzione di principio, già registrata il 2026-08-19) e la chiusura della divergenza 10 della revisione `001`, della divergenza 5 della revisione `002` e della parte generale della divergenza 5 della revisione `003`, ciascuna con riferimento puntuale a dove la chiusura vive in questa feature.

### Key Entities

- **Criterio di assegnazione** (`docs/mood_assignment_criteria.md`): documento versionato, committato da solo prima di ogni valore. Dichiara il significato di ciascun asse, la base di attribuzione, gli esempi di ancoraggio a livello di categoria/genere.
- **Proposta del modello** (`data/curated/dim_category_mood_proposal.json`): artefatto versionato, prodotto da un'unica invocazione manuale di un LLM. Contiene prompt, modello, data, 42 righe proposte. Input alla revisione, mai pubblicato come tabella finale.
- **Registro di verifica indipendente** (campo dedicato dentro `data/curated/dim_category_mood.json`, D9.1): prodotto da chi verifica la proposta contro il criterio senza averla generata. Contiene il conteggio delle righe (categoria × asse) modificate e, quando il conteggio è zero, la dichiarazione che si tratta di un ritrovamento e non di una conferma.
- **Verbale della revisione in contesto pulito** (`specs/006-content-taxonomy-bridge/review.md`, D9.2): prodotto da chi riceve **solo** il documento pubblicato, secondo il protocollo standard del progetto. Contiene i rilievi sulla prosa e, nel blocco di chiusura, come ciascuno è stato chiuso.
- **Tabella congelata** (`data/curated/dim_category_mood.json`): l'artefatto finale, versionato con campo `version` e con il registro di verifica indipendente, mai rigenerato da uno script. 42 righe attese, tre assi su scala `0-1`, chiave `category` verificata meccanicamente contro `catalogs.netflix_categories_normalized` (D6).
- **Documento pubblicato** (`docs/content_taxonomy_bridge.md`): prosa che dichiara natura interpretativa, processo, conteggio degli spostamenti, contratto di versione, limiti. Sotto severità stretta nel controllo di coerenza.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chi apre la history git trova il commit del criterio privo di qualunque valore della tabella, e precedente sia al commit della proposta sia a quello della tabella congelata.
- **SC-002**: Chi apre `data/curated/dim_category_mood.json` trova il conteggio delle righe (categoria × asse) modificate dalla verifica indipendente rispetto alla proposta; se il conteggio è zero, il documento pubblicato lo dichiara come ritrovamento e non come conferma (D9.1).
- **SC-003**: Chi legge `specs/006-content-taxonomy-bridge/review.md` trova, in apertura, la dichiarazione di aver ricevuto **solo** `docs/content_taxonomy_bridge.md`, e il verbale precede, in history git, ogni correzione al documento (D9.2).
- **SC-004**: `dim_category_mood.json` porta una riga per ciascuna delle 42 categorie di `catalogs.netflix_categories_normalized` — o dichiara esplicitamente la differenza — con tre valori decimali `0-1` per riga e un campo `version`; `scripts/check_audit_coherence.py` **fallisce**, non avvisa, se le chiavi non coincidono con quella lista (D6).
- **SC-005**: Nessun artefatto della feature presenta la fonte dei valori come `Benchmark (esterno)` o la confidenza dei tre KPI come alta.
- **SC-006**: `scripts/check_audit_coherence.py` passa in severità stretta su `docs/content_taxonomy_bridge.md`, e continua a passare sui documenti esistenti.
- **SC-007**: Nessun artefatto della feature cita un titolo, una trama o un cast specifico del catalogo video.
- **SC-008**: `README.md` e `docs/roadmap.md` riflettono la feature conclusa, verificabile a colpo d'occhio confrontando la tabella di stato del primo e la sezione «Decisioni aperte» del secondo con lo stato descritto in questa spec.

Gli otto criteri sono verificabili sul prodotto, da chi riceve il repository senza sapere come è stato costruito. La stima di 6 ore, revisioni incluse, è un vincolo di processo del principio III e non compare fra loro.

---

## Stima e scomposizione

**6 ore**, principio III. Se in fase di `/speckit.plan` il lavoro supera 6-7 ore, il taglio non è da inventare: cade esattamente al confine fra le due revisioni di D9.

- **`006a`** — criterio, proposta, verifica indipendente della proposta (D9.1), tabella congelata. Chiude con un artefatto verificabile da solo: la tabella esiste, copre le 42 categorie di `catalogs.netflix_categories_normalized` (o dichiara la differenza), sta sulla scala corretta, ed è difendibile riga per riga contro il criterio.
- **`006b`** — documento pubblicato, sua revisione in contesto pulito (D9.2), registrazione nel controllo di coerenza (incluso il fallimento meccanico di D6/FR-019), contratto di versione per la `007`. Rende `006a` leggibile da fuori.

La linea non è arbitraria: è il punto in cui il lavoro cambia natura, da costruzione e verifica quantitativa a scrittura e revisione di prosa, ed è per questo che regge come taglio anche se la stima complessiva non lo richiedesse.

---

## Assumptions

- **L'insieme delle 42 categorie non cambia durante la costruzione di questa feature.** Se cambiasse a metà lavoro, il controllo esteso da FR-019 lo intercetterebbe alla prima esecuzione, ma la feature non è progettata per assorbire quel caso senza fermarsi.
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
| `mood_energy`, `mood_valence`, `mood_danceability` per ciascuna delle 42 categorie | `Sintetico` | **media** | assegnazione dell'analista, su proposta di un LLM invocato una sola volta e verificata riga per riga da chi non l'ha prodotta, contro un criterio scritto e committato prima di ogni valore (constitution v1.2.0, quinta fonte, cinque condizioni) | valore singolo per asse, decimale `0-1` — non un range: la confidenza `media` non lo impone (a differenza della confidenza `bassa` di `BQ3`) |
| `BQ1-K3`, `BQ2-K2`, `BQ2-K3` (a valle, calcolati dalla `007`) | `Derivato` (`dim_category_mood` + dati musicali osservati) | **media**, non negoziabile | eredita la natura interpretativa della tabella; nessuna cura nella costruzione la fa salire | a discrezione della `007`, purché la confidenza dichiarata resti media |

**Assunzioni dietro i dati sintetici**, dichiarate per iscritto e versionate insieme al criterio che le implementa:

1. **Assunzione di ancoraggio di scala**: gli estremi `0` e `1` di ciascun asse video corrispondono, per significato, agli estremi osservati sul lato musicale per lo stesso asse (D2). È verificata dalla verifica indipendente della proposta (D9.1), non da alcun controllo automatico.
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
- **Copertura del dato**: la tabella descrive le categorie osservate nel catalogo Netflix usato come proxy, fermo al 2021 (`A2` del business case). Un cambio della tassonomia della fonte in un refresh futuro rende la tabella disallineata; il controllo esteso da D6/FR-019 lo rileva meccanicamente alla prima esecuzione successiva — fallendo, non avvisando — ma non impedisce che il disallineamento si produca.
- **Dove è esposto all'utente finale**: nel documento pubblicato (`docs/content_taxonomy_bridge.md`); nella nota in loco su §15 di `docs/data_model.md`; e — per la `007`, che eredita l'obbligo — accanto a ogni presentazione di `BQ1-K3`, `BQ2-K2` e `BQ2-K3` in dashboard, con la versione della tabella su cui il valore è calcolato (D5).
