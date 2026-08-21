# Il profilo di mood delle categorie video

Come ciascuna categoria del catalogo video riceve tre<!--#--> valori di mood che nessuna fonte osserva, chi li ha assegnati, chi li ha verificati, e che cosa non autorizzano a concludere.

I valori di [`dim_category_mood.json`](../data/curated/dim_category_mood.json) sono **gli unici del progetto che nessuna fonte osserva e nessuna formula calcola**. È la definizione con cui la constitution nomina la classe di dato a cui appartengono, ed è più stretta della formula che verrebbe spontanea — «l'unico strato interpretativo» — che questa pagina non rivendica: anche il parametro di scenario della `004` poggia su un dato raccolto una volta a mano, e nemmeno quello è una trasformazione che chiunque può rieseguire. La differenza sta altrove, ed è netta: lì il valore di partenza è osservato su qualcuno, qui non è osservato su nessuno.

**La cautela sta in cima e non in fondo, perché è la proprietà che definisce il resto.** Il riassunto onesto di ciò che segue è: *valori assegnati, non misurati, proposti da `Claude Sonnet 5` in una sola invocazione manuale, verificati da una seconda sessione di modello contro un criterio che l'autore della tabella aveva scritto lui stesso qualche ora prima, su categorie di un catalogo che non è di StreamWave — è quello di Netflix, usato come proxy, e fermo al 2021<!--@NF.num.release_year.max-->.* Ogni pezzo di questa frase è argomentato sotto, e ciascuno è accompagnato dal presidio che lo rende almeno contestabile. Nessun presidio lo rende un dato osservato — e questo documento non prova a suggerire il contrario.

---

## 1. Che cosa questa feature produce

Una tabella di 42<!--@MOOD.coverage.rows--> righe, una per ciascuna categoria del catalogo video, e per ciascuna riga tre<!--#--> valori decimali sul dominio `0-1` — `mood_energy`, `mood_valence`, `mood_danceability`. È l'oggetto che rende calcolabili `BQ1-K3` (l'intervallo di mood occupato dal catalogo video), `BQ2-K2` (la distanza fra il profilo mediano di un segmento musicale e quello del catalogo) e, attraverso quest'ultimo, `BQ2-K3`.

**Questa feature non calcola quei KPI.** Le misure, la loro espressione e i valori che compariranno in dashboard appartengono alla `007`, che eredita da qui il contratto di §5 e il vincolo di confidenza di §6.

Non produce alcuno script di derivazione. Non esiste un comando che rigeneri la tabella, e non è una mancanza: è la condizione stessa che rende ammissibile il metodo (§2).

## 2. I quattro passi, e perché l'ordine è il presidio

La decisione di processo è `DA-1` di [`roadmap.md`](roadmap.md), risolta il 2026-08-19: **un LLM propone, una persona decide**, e nessuno script chiama mai il modello. L'invocazione è un passaggio umano non riproducibile il cui esito si congela in un artefatto versionato — lo stesso schema del benchmark della `004`, dove il passaggio irripetibile era la raccolta di una fonte esterna invece della proposta di un modello.

I quattro<!--#--> passi, nell'ordine in cui sono stati eseguiti:

| | Passo | Artefatto |
|---|---|---|
| 1<!--#--> | il **criterio** di assegnazione, scritto e committato da solo | [`docs/mood_assignment_criteria.md`](mood_assignment_criteria.md) |
| 2<!--#--> | la **proposta** di un modello, invocato manualmente una sola volta | [`data/curated/dim_category_mood_proposal.json`](../data/curated/dim_category_mood_proposal.json) |
| 3<!--#--> | la **verifica indipendente**, riga per riga contro il criterio | il campo `verification` della tabella |
| 4<!--#--> | il **congelamento** della tabella verificata | [`data/curated/dim_category_mood.json`](../data/curated/dim_category_mood.json) |

**Una nota di lettura**, perché anche il criterio ha sezioni numerate e la collisione è facile: da qui in avanti «criterio §5» indica una sezione di [`mood_assignment_criteria.md`](mood_assignment_criteria.md), mentre un «§5» senza qualificazione indica una sezione di questa pagina.

**L'ordine non è una sequenza di comodo: è ciò che il metodo offre al posto della parola.** Un criterio scritto dopo che i valori esistono è indistinguibile, a lettura, da un criterio scritto prima — si piega a giustificare i numeri invece di vincolarli, e nessuna lettura del testo può più accorgersene. Ciò che distingue i due<!--#--> casi non sta nel documento, sta nella cronologia:

```bash
git log --oneline --reverse -- docs/mood_assignment_criteria.md \
  data/curated/dim_category_mood_proposal.json \
  data/curated/dim_category_mood.json
```

Il commit che introduce il criterio non contiene alcun valore della tabella, nemmeno di prova, e precede gli altri due<!--#-->.

**Che cosa questa prova stabilisce**: un fatto sullo stato dei file — che il criterio vi compare in un commit anteriore a quello che introduce qualunque valore.

**Che cosa non stabilisce**, e va detto perché l'intestazione del paragrafo potrebbe far credere il contrario: un fatto sullo stato di conoscenza di chi ha scritto. Nulla esclude che chi redigeva il criterio avesse già in mente il profilo che avrebbe assegnato a una categoria, e la cronologia git è riscrivibile da chi la produce. È lo stesso limite già dichiarato dalla `004` per i fattori di banda: la garanzia vale contro una variante del difetto — il criterio riscritto per adattarlo ai numeri dopo averli visti — e non contro le altre.

### Perché il modello non entra nella pipeline

Il modello — `Claude Sonnet 5`, invocato il 2026-08-20 — ha ricevuto il criterio e l'elenco delle categorie, in una cartella isolata fuori dal repository, e ha restituito le righe. Prompt, nome del modello e data dell'invocazione sono versionati insieme alla proposta, dove chiunque può rileggerli.

Se quella chiamata vivesse dentro uno script, la derivazione a valle smetterebbe di essere deterministica: due<!--#--> esecuzioni potrebbero produrre tabelle diverse, e ogni numero pubblicato dalla `007` dipenderebbe da quale delle due<!--#--> qualcuno ha eseguito per ultima. È la ragione per cui `DA-1` ammette l'uso di un modello **solo** a questa condizione. Una ricerca ne mostra il sintomo più evidente:

```bash
grep -rniE "openai|anthropic|api[._-]?key|requests\.(get|post)|urllib\.request" scripts/
```

**Che cosa un esito vuoto stabilisce, e che cosa no.** Stabilisce che nessuno script oggi presente in `scripts/` contiene una delle stringhe cercate. Non stabilisce che nessuno script chiami un modello: guarda una sola cartella, cerca un elenco chiuso di nomi — nessun altro fornitore, nessun client HTTP diverso da quei due<!--#-->, nessuna chiamata passata a un sottoprocesso o nascosta in un file di configurazione — e non vede uno script cancellato, che in un albero di lavoro non lascia traccia. Il presidio vero non è questa ricerca: è che la tabella sia congelata e che nessun comando la rigeneri (§8). La ricerca serve a rendere il sintomo controllabile in un secondo, non a chiudere la questione.

### Le due revisioni sono distinte, e non è un dettaglio di processo

Questa feature ha attraversato **due<!--#--> controlli diversi**, in momenti diversi, con oggetti diversi. Tenerli separati è una decisione presa dopo che una revisione della spec aveva trovato che la prima stesura li faceva collassare in uno.

- **La verifica indipendente della proposta** (passo 3<!--#-->) guarda i valori. Confronta ogni cella con il criterio, che è l'**unico metro** di contestazione ammesso — non un'opinione sul mood di una categoria, e non un perimetro di lettura: chi verifica apre `reports/data_profile.json` per risolvere i sei<!--#--> identificativi con cui il criterio ancora la propria scala (criterio §1), perché senza di essi l'obbligo che il criterio dichiara più importante non è verificabile affatto. È un passo di lavorazione, avviene prima del congelamento, ed è la condizione 4<!--#--> della quinta classe di fonte dati della constitution (§6).
- **La revisione in contesto pulito** guarda questa pagina. Un revisore riceve **solo** questo file — non il criterio, non la proposta, non la tabella — secondo il protocollo già usato dalle feature precedenti, e produce [`specs/006-content-taxonomy-bridge/review.md`](../specs/006-content-taxonomy-bridge/review.md).

Un solo passaggio non poteva fare bene entrambe le cose: chi confronta valori con un criterio tecnico non sta leggendo la prosa con l'occhio di chi cerca un'inferenza indebita, e chi legge la prosa isolato dal resto non ha — e non deve avere — il criterio davanti.

## 3. Che cosa la verifica indipendente ha trovato

**Chi ha verificato non è una persona: è una seconda sessione di modello**, quella che ha implementato questa feature, distinta da quella isolata che aveva prodotto la proposta e che non l'aveva vista prima di riceverla. Una persona interviene, ma in un punto diverso e va detto quale: decide se accettare l'esito della verifica e della revisione in contesto pulito, e con ciò se congelare la tabella. Il confronto riga per riga contro il criterio — che è ciò che la condizione 4<!--#--> chiede — l'ha eseguito il modello. Il registro della verifica sta nel campo `verification` della tabella, insieme a ciò che non copre.

**Ha spostato 3<!--@MOOD.review.changes_count--> celle.** *(Nota in loco — 2026-08-21, chore `criterio-mood-cf1`: la terza riga, `Teen TV Shows`, non viene dalla verifica del 2026-08-20 come le prime due<!--#--> — è una correzione di un errore di copertura di quella verifica, trovato dalla ricognizione della regia in `docs/roadmap.md` § Debito della feature 006 e chiuso da questo chore. Vedi `verification.changes` nella tabella per la distinzione.)* Tutte e tre<!--#--> sull'asse del ritmo, tutte citando lo stesso passaggio del criterio — il secondo segnale di criterio §5, che alla lettera dice: «un formato episodico a durata fissa ha una cadenza più alta di un formato a durata libera».

| Categoria | Asse | Valore congelato | Punto del criterio |
|---|---|---|---|
| `Anime Series`<!--@catalogs.mood_categories--> | `mood_danceability` | 0,55<!--@MOOD.category.anime_series.mood_danceability--> | criterio §5, secondo segnale: la proposta la poneva alla stessa cadenza di `Anime Features`<!--@catalogs.mood_categories-->, 0,50<!--@MOOD.category.anime_features.mood_danceability-->, che è a durata libera |
| `Classic & Cult TV`<!--@catalogs.mood_categories--> | `mood_danceability` | 0,55<!--@MOOD.category.classic_cult_tv.mood_danceability--> | criterio §5, stesso caso rispetto a `Classic Movies`<!--@catalogs.mood_categories-->, 0,50<!--@MOOD.category.classic_movies.mood_danceability--> |
| `Teen TV Shows`<!--@catalogs.mood_categories--> | `mood_danceability` | 0,55<!--@MOOD.category.teen_tv_shows.mood_danceability--> | criterio §5, stesso caso: episodico a durata fissa, non generico/geografico/linguistico. Corretto il 2026-08-21, non il 2026-08-20 |

**Questo numero non è un voto sulla proposta, ed è il punto in cui è più facile leggerlo male.** Non dice che la proposta era buona: dice quante celle la verifica ha potuto spostare *citando il criterio*, che è l'unica cosa che le era consentito fare. Dove la verifica ha trovato un problema che il criterio non le permetteva di risolvere, la cella è rimasta ferma e il problema è stato registrato altrove — vedi il ritrovamento `CF-1` qui sotto, che elenca una per una le etichette le cui celle sono rimaste ferme proprio perché il criterio si contraddice su di esse. Un conteggio basso può descrivere una proposta aderente al criterio oppure un criterio che non dà appigli: da solo non distingue i due<!--#--> casi, e questa pagina non chiede al lettore di assumere il primo.

### I tre ritrovamenti sul criterio

La verifica ha prodotto un esito che il conteggio degli spostamenti non poteva contenere: difetti del **criterio**, non celle da contestare. Sono registrati come `criterion_findings` nella tabella.

**`CF-1` — criterio §2 e criterio §5 si contraddicono sull'asse del ritmo.** Criterio §2 prescrive che l'etichetta generica riceva il profilo «**centrale su tutti e tre<!--#--> gli assi, per assenza di segnale, non per equilibrio misurato**», e che per l'etichetta geografica o linguistica «valga la stessa regola dell'etichetta generica»; criterio §5 attribuisce a ogni «formato episodico a durata fissa […] una cadenza più alta di un formato a durata libera». Le etichette che sono insieme geografiche o generiche **ed** episodiche cadono sotto entrambe le regole, che dicono cose diverse: `TV Shows`<!--@catalogs.mood_categories-->, `International TV Shows`<!--@catalogs.mood_categories-->, `British TV Shows`<!--@catalogs.mood_categories-->, `Korean TV Shows`<!--@catalogs.mood_categories-->, `Spanish-Language TV Shows`<!--@catalogs.mood_categories-->.

Quelle celle **non sono state spostate**. La proposta segue criterio §2, che è categorico ed esplicito; preferirle criterio §5 sarebbe stato decidere sul criterio, non verificare contro il criterio — e criterio §7 esclude esattamente quella mossa. Il conflitto resta aperto e si chiude riscrivendo il criterio, cioè in una versione successiva della tabella (§5). *(Nota in loco — 2026-08-21, chore `criterio-mood-cf1`: chiuso. Il criterio riscritto aggiunge, in nota a §2 e §5, la regola per cui il segnale di formato prevale sull'assenza di segnale; le cinque<!--#--> celle si sono spostate — tabella versione 2<!--@MOOD.table.version-->, vedi `changelog` nella tabella.)*

**`CF-2` — il criterio non ha una regola per le etichette di pubblico.** `Children & Family Movies`<!--@catalogs.mood_categories--> riceve positività 0,95<!--@MOOD.category.children_family_movies.mood_valence--> perché criterio §4 la nomina «archetipo dell'estremo alto» su quell'asse; `Teen TV Shows`<!--@catalogs.mood_categories--> resta centrale. La differenza discende dall'esistenza di un archetipo dichiarato, non da una regola che chi assegna possa applicare a un'etichetta di pubblico nuova. Nessuna cella spostata: la regola di scelta di criterio §2 — «se per assegnare un valore serve immaginare quali titoli stiano nella categoria, l'assegnazione sta uscendo dal criterio» — sostiene il centro. Il vuoto va colmato nel criterio, non nella tabella. *(Nota in loco — 2026-08-21, chore `criterio-mood-cf1`: il vuoto di regola è chiuso — criterio riscritto, nota a §2. Su `Teen TV Shows` specificamente, la ricognizione della regia in `docs/roadmap.md` § Debito della feature 006 ha trovato un errore di copertura distinto, non un vuoto di regola: la cella andava mossa già dalla verifica del 2026-08-20 con la stessa motivazione usata per `Anime Series` e `Classic & Cult TV` sopra. `mood_danceability` è ora 0,55<!--@MOOD.category.teen_tv_shows.mood_danceability-->; `mood_energy` e `mood_valence` restano centrali, per assenza di ogni altro segnale.)*

**`CF-3` — la granularità effettiva è più grossolana di quella dichiarata.** Criterio §6 fissa due<!--#--> cifre decimali; i valori proposti sono tutti multipli di 0,05<!--#-->, cioè una griglia che il criterio non chiede e non vieta. Non è contestabile citando un punto del criterio, quindi nessuna cella si muove — ma chi legge la tabella deve sapere che la precisione apparente della seconda cifra decimale non corrisponde a una distinzione che il processo abbia davvero fatto.

*(Le citazioni fra virgolette in questo blocco sono testuali. È una scelta, non uno stile: una parafrasi del criterio non è verificabile da nessuno dei controlli di §2 — vedi la coda di questa sezione.)*

*(Il valore `0,05` non porta ancora perché non esiste come identificativo negli artefatti di questo progetto: il ritrovamento vive per esteso in `verification.criterion_findings` della tabella.)*

### Che cosa l'indipendenza dichiarata non copre

Chi ha verificato non ha prodotto la proposta, ed è ciò che la condizione 4<!--#--> richiede. Ma **proporre e verificare sono stati entrambi passi eseguiti da un modello**, e la condizione, così com'è scritta, è soddisfatta da un modello che ne verifica un altro. Non è però isolamento assoluto nemmeno fra i due<!--#-->: entrambe le sessioni ereditano le istruzioni di progetto che il sistema inietta, e la tabella lo dichiara nel campo `independence_residual` invece di tacerlo. Quelle istruzioni non contengono nulla sui profili di mood; il residuo resta ed è scritto.

**Le parafrasi di questa pagina sul criterio non sono verificate da nulla**, e va detto perché è l'unico scoperto strutturale di tutto il metodo. I due<!--#--> controlli di §2 hanno oggetti disgiunti: chi verifica i valori non legge questa prosa, chi legge questa prosa non ha il criterio davanti, e il controllo di coerenza confronta cifre. Un errore nel riportare che cosa il criterio dice — anche in buona fede — non verrebbe intercettato da nessuno di questi, e produrrebbe un ritrovamento `CF-*` che sembra un difetto del criterio ed è un difetto della citazione. La sola difesa applicata è quella di sopra: citare il criterio alla lettera dove l'argomento dipende da ciò che dice, così che chiunque apra i due<!--#--> file possa fare il confronto che nessun controllo fa.

Resta anche il fatto più semplice e più difficile da presidiare: **il criterio contro cui la proposta è stata verificata è stato scritto dalla stessa persona che pubblica questa tabella.** Un metro scritto da chi verrà misurato è meglio di nessun metro — è contestabile, sta in un file, e chiunque può leggerlo e trovarlo sbagliato, come `CF-1` mostra sia possibile. Non è la stessa cosa di un metro indipendente, e questa pagina non lo presenta come tale.

## 4. La copertura, e chi si accorgerebbe se la tassonomia cambiasse

La copertura è **totale**: il catalogo video ha 42<!--@CL.NF.category.distinct--> categorie distinte — è il conteggio che la pipeline della `003` osserva e pubblica — e la tabella ha 42<!--@MOOD.coverage.rows--> righe. I due<!--#--> numeri hanno identificativi diversi apposta: se la copertura fosse ancorata al solo conteggio delle righe della tabella, l'affermazione verificherebbe sé stessa. Nessuna categoria manca, quindi non si pone la domanda di che cosa le misure a valle facciano di una categoria senza profilo.

**Non si pone oggi.** Se la tassonomia della fonte cambiasse in un aggiornamento futuro, si porrebbe — ed è la divergenza che la revisione della `002` aveva lasciato aperta con una formulazione precisa: nessuno sapeva chi si accorgerebbe. La risposta di questa feature non è una persona: è un controllo che fallisce.

`scripts/check_audit_coherence.py` confronta l'insieme delle categorie coperte dalla tabella con quello del catalogo video, **prima** di verificare qualunque documento, e si ferma con uscita diversa da zero<!--#--> se i due<!--#--> divergono — stampando quali categorie stanno da una parte e non dall'altra.

**Che cosa questo presidio sposta, detto senza gonfiarlo.** Non elimina la dipendenza da una persona: non esiste in questo repository alcun hook di pre-commit né alcuna integrazione continua che esegua il controllo da sé, e §8 lo presenta per quello che è, un comando che qualcuno digita. Ciò che cambia è **quale** memoria serve. Prima occorreva che chi tocca la tassonomia della fonte sapesse che questa tabella esiste e ne dipendesse; ora basta che chi lavora sul repository lanci il controllo di coerenza, che è la condizione che ogni feature esegue comunque prima di proporre un commit e che non richiede di sapere nulla dei profili di mood.

**Il confronto è sugli insiemi, non sulle numerosità**, e la distinzione è il motivo per cui il presidio regge: una categoria rinominata a monte lascia i conteggi identici e gli insiemi diversi. È il caso che un controllo sul solo numero di righe lascerebbe passare.

L'obbligazione scritta non sparisce, cambia ruolo: chi tocca la tassonomia della fonte trova qui dichiarato che un controllo lo aspetta. Ma non è più su di essa che la garanzia poggia.

## 5. Il contratto di versione, per la `007` e per chiunque legga a valle

La tabella porta un campo `version`, oggi 2<!--@MOOD.table.version-->.

**Il contratto**: ogni valore pubblicato che dipende da `dim_category_mood` deve dichiarare **su quale versione della tabella è stato calcolato**. Vale per i tre<!--#--> KPI della `007`, in dashboard come in qualunque documento che li riporti.

La versione si incrementa quando una riga viene corretta dopo il congelamento — per un errore trovato, o per un difetto del criterio come `CF-1` che una revisione del criterio chiude — e la tabella registra che cosa è cambiato e perché. **Una revisione della tabella invalida i valori già pubblicati che ne dipendono**: non li corregge automaticamente, li invalida, e senza il legame esplicito fra valore e versione nessuno saprebbe quali.

La ragione per cui il contratto è scritto qui e non lasciato al buon senso della `007`: senza di esso una correzione lascerebbe in giro numeri «giusti quando sono stati scritti e mai più riverificati». È la stessa classe di difetto di un totale corretto in una feature precedente e rimasto citato altrove nella forma vecchia, che la roadmap registra come precedente da non ripetere.

## 6. Fonte e confidenza

| Metrica | Fonte | Confidenza |
|---|---|---|
| `mood_energy`, `mood_valence`, `mood_danceability` per ciascuna categoria | `Sintetico` | **media** |
| `BQ1-K3`, `BQ2-K2`, `BQ2-K3` (calcolati dalla `007`) | `Derivato` | **media**, non negoziabile |

**Perché `Sintetico` e non `Benchmark (esterno)`.** Un benchmark è un dato osservato su un operatore terzo e trasferito a StreamWave; qui non esiste alcun operatore terzo e non c'è nulla da citare fuori da questo repository. Etichettare la tabella come benchmark le presterebbe un'autorità che non ha — la citazione puntuale e verificabile presso terzi che quella fonte richiede, qui, non può esistere.

**L'etichetta è stata ammessa per emendamento, e la contemporaneità va dichiarata.** Fino alla versione precedente la constitution definiva `Sintetico` come dato generato da script versionati, e qui nessuno script genera nulla — è precisamente la condizione che rende ammissibile il metodo. La revisione della spec di questa feature ha trovato lo scoperto, e la constitution è stata emendata per ammettere le **assegnazioni dell'analista congelate in un artefatto versionato**: è la quinta *classe* di dato che la constitution riconosce, e l'emendamento dichiara esplicitamente di **non** introdurre una nuova etichetta di fonte — la classe vive sotto `Sintetico`, la cui definizione si allarga. Per questo la tabella di qui sopra dice `Sintetico` e non un nome nuovo: non esiste un nome nuovo.

Le condizioni sono cinque<!--#-->: criterio scritto prima del valore, valore congelato e mai rigenerato, versione dichiarata a valle, verifica indipendente con esito quantificato, nessuna promozione di confidenza. Come per i benchmark della `004`, la regola e il suo primo caso d'uso sono contemporanei: la regola è più stringente di ciò che sostituiva, ma non è un vincolo esterno preesistente che il lavoro ha incontrato.

**Che cosa la condizione 4<!--#--> ottiene con un numero, visto che quel numero non misura la qualità.** Ottiene che la verifica lasci una traccia della propria estensione, e che quella traccia sia leggibile senza fidarsi di chi l'ha prodotta: un conteggio esiste, è pubblicato, e si può confrontare con l'elenco puntuale degli spostamenti in §3. Non ottiene un giudizio sulla proposta, e la constitution non pretende che lo faccia. Un conteggio pari a zero<!--#--> non sarebbe stato un successo da rivendicare ma un ritrovamento da dichiarare come tale — ed è la ragione per cui la condizione chiede *un esito quantificato* e non *un esito positivo*.

**La confidenza non sale, e non è una scelta.** È un obbligo di §15 di [`data_model.md`](data_model.md). Criterio scritto prima, proposta di un modello, confronto riga per riga, conteggio pubblicato: ciò che tutto questo produce è che ogni valore sia **contestabile citando un testo scritto prima che il valore esistesse**. Non produce un errore più piccolo, perché non esiste alcuna misura dell'errore da cui partire — §7 lo dice, e le due<!--#--> affermazioni devono restare compatibili. La tabella è costruita, non osservata, e nessuna cura nella costruzione la sposta di classe.

## 7. Limiti dichiarati

**L'assegnazione non è una misura.** Un `mood_energy` pari a 0,95<!--@MOOD.category.action_adventure.mood_energy--> per `Action & Adventure`<!--@catalogs.mood_categories--> non ha lo stesso statuto di un `energy` pari a `0.95` letto su una traccia musicale: il secondo è un campo della fonte, il primo è deciso da una persona. Confonderli significa trattare un giudizio come un'osservazione, e nel modello dati i due<!--#--> valori si incontrano sullo stesso asse — che è esattamente il punto in cui la confusione è più facile.

**La distanza fra un profilo assegnato e uno misurato regge solo quanto regge l'ancoraggio agli estremi.** `BQ2-K2` sottrae un profilo del lato video da uno del lato musicale, e sottrarre presuppone che uno stesso numero — 0,55<!--#--> assegnato e 0,55<!--#--> osservato — indichi la stessa posizione sull'asse. Ciò che lo sostiene non è nulla di implicito: criterio §1 ancora gli estremi di ciascun asse ai valori **osservati** sul lato musicale — i sei<!--#--> identificativi `SP.num.*` di `reports/data_profile.json` — e la tabella lo registra nel campo `conventions.mood_scale_anchor`. Il limite è che **l'ancoraggio è solo agli estremi**: nessun valore osservato calibra il centro dell'asse, e la corrispondenza fra le posizioni intermedie delle due<!--#--> scale è un'assunzione del criterio, non un fatto misurato. Una distanza calcolata su questi assi è quindi confrontabile con sé stessa fra segmenti diversi, ma la sua grandezza assoluta non ha l'interpretazione che avrebbe fra due<!--#--> profili entrambi osservati.

**Il profilo è dell'etichetta, non dei titoli.** Una categoria del catalogo è una promessa editoriale, e il suo profilo è il registro che quella promessa evoca — non la media dei contenuti che vi ricadono, che nessuno ha misurato. Un titolo che ricade in una categoria **non eredita** quel profilo, e nessuna conclusione su un singolo contenuto discende da qui.

**Nessun artefatto di questa feature cita un titolo del catalogo.** Né nome, né trama, né cast: gli ancoraggi si esprimono a livello di categoria o di genere musicale come archetipo. La regola chiude, per gli artefatti di questa feature, la parte generale di una divergenza che la revisione della `003` aveva lasciato aperta. Non è un vincolo che tolga qualcosa — l'assegnazione avviene a grana categoria — ma citare titoli renderebbe più facile leggere il profilo come «osservato su quegli esempi» invece che come ciò che è.

**Il valore centrale significa assenza di segnale, non equilibrio misurato.** Una categoria generica, geografica o linguistica riceve il centro perché la sua etichetta non dichiara un registro affettivo, non perché contenga contenuti opposti che si compensano. Le due<!--#--> letture portano a conclusioni diverse su qualunque aggregato le usi.

**Non risponde a**: se una categoria contenga *davvero*, in media, contenuti energici, positivi o ritmati — nessun campo del catalogo video misura energia, positività o ritmo. Né a se due<!--#--> categorie con mood simile condividano pubblico: il mood è un asse di posizionamento, non un dato comportamentale, e questo progetto non ha alcuna misura di audience.

**Nessun lessico causale.** Che una categoria abbia un profilo vicino a un segmento musicale non implica che l'una causi l'attrattività dell'altro, né che chi guarda la prima adotterebbe il secondo.

**La riproducibilità non è fra le proprietà di questa tabella.** Non c'è ragione di attendersi che due<!--#--> persone che applicassero il criterio alle stesse categorie ottengano le stesse righe, e il criterio lo dichiara fra i propri limiti — nessuno però l'ha provato, ed è un'aspettativa, non un esito. Ciò che il processo garantisce è che ogni scostamento sia **discutibile contro un testo** — non che sia unico.

**Copertura del dato**: il catalogo Netflix usato come proxy si ferma al 2021<!--@NF.num.release_year.max-->, che è l'anno di uscita più recente presente nel dataset (`A2` del [business case](business_case.md)). Un cambio di tassonomia in un aggiornamento futuro rende la tabella disallineata; il controllo di §4 lo rileva fallendo, ma non impedisce che il disallineamento si produca.

**Che cosa nessuna verifica di questo progetto garantisce.** Il controllo di coerenza confronta questa pagina con la tabella che la alimenta, e la tabella con il catalogo delle categorie: verifica che gli artefatti non divergano fra loro. Nessuno di questi confronti guarda il mondo.

Che un profilo assegnato sia *quello giusto* per una categoria è una domanda a cui **una risposta esiste, e non è stata cercata**: far assegnare le stesse categorie a un secondo giudice indipendente dal criterio e misurare l'accordo fra i due<!--#--> esiti. Non è stato fatto, e la ragione non è il costo: è che un secondo giudice indipendente dal criterio, in questo progetto, non esiste — chi lo applicherebbe sarebbe un'altra sessione dello stesso sistema, con lo stesso testo davanti, e l'accordo che ne uscirebbe misurerebbe la chiarezza del criterio più della bontà dei valori. Resta che **nulla ha mai testato il merito** di queste righe: tutto ciò che questa pagina dichiara riguarda come sono state prodotte. La sola difesa è il processo di §2, e la trasparenza con cui è descritto qui non è una risposta — è il modo di non fingere che la domanda non esista.

## 8. Come si verifica

```bash
# tassonomia, e ogni cifra *ancorata* di questa pagina contro gli artefatti
python3 scripts/check_audit_coherence.py

# l'ordine dei commit dei tre artefatti, dal piu' vecchio
git log --oneline --reverse -- docs/mood_assignment_criteria.md \
  data/curated/dim_category_mood_proposal.json \
  data/curated/dim_category_mood.json

# che cosa contiene il commit che introduce il criterio
git show --stat $(git log --format=%H --follow -- docs/mood_assignment_criteria.md | tail -1)
```

Nessuno dei tre<!--#--> comandi richiede rete, credenziali o i dataset di origine: leggono soltanto artefatti versionati.

**Che cosa la cronologia stabilisce davvero**, perché è meno di «l'ordine dei quattro<!--#--> passi» e la differenza conta. Stabilisce che il passo 1<!--#--> precede il passo 2<!--#--> e il passo 4<!--#-->. **Non** ordina il passo 3<!--#--> rispetto al 4<!--#-->: l'artefatto della verifica è un campo *dentro* la tabella congelata, quindi i due<!--#--> passi stanno nello stesso commit e nessun `git log` può separarli. E il terzo comando serve perché l'affermazione «il commit del criterio non contiene alcun valore della tabella» riguarda il **contenuto** di un commit, che `--oneline` non mostra: l'elenco dei file toccati da quel commit la rende ispezionabile in una riga.

**Che cosa si può rifare, e che cosa no.** Si può **rieseguire ogni controllo**: coerenza fra documento e tabella, copertura, scala, ordine dei commit. **Non si può rifare l'assegnazione.** Non esiste uno script che la rigeneri, ed è deliberato: l'invocazione del modello è avvenuta una volta, fuori dalla pipeline, e il suo esito è congelato. Chi non è d'accordo con una riga non la ricalcola — la contesta citando il criterio, e se il criterio non regge, si corregge il criterio e la versione della tabella sale.

Ogni quantità pubblicata in questa pagina porta un marcatore invisibile, secondo le [convenzioni di marcatura](convenzioni-marcatura.md), e i marcatori sono di due<!--#--> specie. Il primo è un'**ancora** a un identificativo di un artefatto versionato, e il controllo confronta il numero scritto con il valore di quell'identificativo. Il secondo dichiara che la quantità **non è un valore di quegli artefatti** — un numerale di struttura del discorso, o un fatto che vive altrove: la granularità fissata dal criterio, il conteggio dei suoi ancoraggi, il ritrovamento `0,05` di `CF-3`. Sul secondo il controllo non verifica nulla: registra che chi scrive ha considerato quel numero e ha dichiarato dove sta.

Vale la **severità stretta**: una quantità priva di entrambi i marcatori è un errore, non un avviso. Ciò che il controllo garantisce, e ciò che non può garantire, è dichiarato nella stessa pagina delle convenzioni — e vale la pena rileggerlo qui, perché su questo documento la differenza è più visibile che altrove: **i marcatori dichiarano l'origine di un numero, non la sua verità.** Un profilo di mood ancorato resta un profilo assegnato.
