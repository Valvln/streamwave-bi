# Revisione in contesto pulito — `docs/content_taxonomy_bridge.md`

**Data della revisione**: 2026-08-20
**Data della trascrizione**: 2026-08-20
**Oggetto**: `docs/content_taxonomy_bridge.md` alla versione del commit **`be38013`** — sha256 del contenuto letto: `059b6e9c9d942987eba6e1d7b1783db4a5f392c9e1690e8be5a8a84c0f9ccb31`

```bash
git show be38013:docs/content_taxonomy_bridge.md
```

Il documento sarà modificato per chiudere i rilievi: chi legge questo verbale contro la versione attuale può non ritrovare i passaggi citati. Vanno confrontati con la versione qui sopra, che è quella che il revisore ha letto.

## Come è stata condotta

**Natura**: contesto pulito, secondo il protocollo già usato per le feature `002`-`005`. La revisione è stata affidata a un **subagent isolato** che ha ricevuto **un solo file** — una copia di `docs/content_taxonomy_bridge.md` in una cartella vuota fuori dal repository — con il vincolo esplicito di non aprire nient'altro: non il criterio, non la proposta, non la tabella congelata, non gli script, non `git`, non la rete. I link relativi della copia sono deliberatamente rotti, e il mandato chiedeva di ignorarli invece di ricostruirli.

**È la seconda delle due revisioni che la spec tiene distinte** (D9). La prima — la verifica indipendente della proposta contro il criterio, condizione 4 della quinta fonte dati — è avvenuta prima del congelamento, con pieno accesso al repository, e il suo esito vive nel campo `verification` di `data/curated/dim_category_mood.json`. Questa guarda la prosa, e chi la esegue non ha e non deve avere il criterio davanti.

Il mandato chiedeva sei classi di difetto in ordine di priorità — affermazioni non sostenute dal documento stesso, limiti taciuti o attenuati, inferenze indebite, contraddizioni interne, ambiguità che cambiano la conclusione, promesse non consegnate — e chiedeva esplicitamente di **formulare in forma condizionale** i rilievi che dipendono da artefatti non leggibili, invece di aprirli per risolverli. Otto rilievi su sedici sono condizionali, ed è la forma corretta in questa posizione di lettura.

**Sull'ordine dei passi.** Il verbale è stato trascritto e committato **prima** che il documento venisse toccato, come `CLAUDE.md` prescrive. Nessun rilievo era stato chiuso al momento di questo commit.

**Due note di fedeltà della trascrizione**, che riguardano la forma e non il contenuto:

- il testo che segue è **integrale e non modificato**. Sono stati abbassati di un livello i titoli, perché il verbale entra come corpo di questo file. Nient'altro è stato toccato — inclusi i punti in cui il revisore ipotizza una semantica dei marcatori che poi risulta diversa da quella reale (`R10`, `R11`), e quelli in cui numera i rilievi come «5 bloccanti e 11 non bloccanti» pur presentandoli tutti in un unico elenco continuo;
- nei rilievi `R10` e `R11` il revisore **cita i marcatori alla lettera**, nella forma in cui compaiono nel sorgente. Nel verbale li ha racchiusi fra apici inversi, quindi restano visibili anche nella resa di questa pagina; la citazione non è stata alterata.

**Il verbale non si corregge.** Il blocco di chiusura, in coda, è l'unico testo che chi è stato revisionato può aggiungere: dichiara come ogni rilievo è stato chiuso, distinguendo *risolvendolo* da *indebolendo l'affermazione*, da *respingendolo con la prova*, da *rinviandolo*. Il testo del revisore resta come è arrivato, anche dove sbaglia.

---

## Verbale di revisione in contesto pulito — «Il profilo di mood delle categorie video»

### 1. Che cosa ho letto e che cosa no

**Letto**: un solo file, `documento.md`, ricevuto in una cartella isolata.

- dimensione: 22215 byte, 165 righe
- impronta del contenuto revisionato: `sha256 059b6e9c9d942987eba6e1d7b1783db4a5f392c9e1690e8be5a8a84c0f9ccb31`

Ho letto il **sorgente** del file, non la sua resa: vedo quindi anche i marcatori in commento HTML (`<!--@...-->`, `<!--#-->`) che un lettore della pagina renderizzata non vede. Alcuni rilievi (R10, R11) esistono solo a questo livello e li dichiaro come tali.

**Non letto, e mai aperto né cercato**, benché il documento li nomini: `data/curated/dim_category_mood.json` e il campo `verification`/`criterion_findings` che contiene; `data/curated/dim_category_mood_proposal.json` e il prompt/modello/data che dichiara versionati insieme; `docs/mood_assignment_criteria.md` e i suoi §2, §4, §5, §7; `reports/data_profile.json`; `scripts/check_audit_coherence.py`; `docs/roadmap.md` e la decisione `DA-1`; la constitution e la sua «quinta fonte dati»; `docs/data_model.md` §15; `docs/convenzioni-marcatura.md`; il business case e il suo limite `A2`; gli artefatti delle feature `002`, `003`, `004`, `007`; `specs/006-content-taxonomy-bridge/review.md`; il catalogo `catalogs.netflix_categories_normalized`.

**Non eseguito**: nessun comando `git`, nessuna ricerca in rete, nessuna ricerca nel repository. I due comandi che il documento propone in §2 e §8 non sono stati eseguiti.

**Uscite dal perimetro**: una sola, dichiarata. Ho eseguito `shasum -a 256`, `wc` e `ls` **sul solo file ricevuto e sulla sua cartella**, per ancorare la versione revisionata come richiede il metodo. Non ho letto nient'altro.

Conseguenza da tenere presente leggendo i rilievi che seguono: **ogni affermazione che il documento fa su un artefatto esterno è per me né vera né falsa.** Dove il difetto dipende da come quell'artefatto è fatto, il rilievo è formulato in forma condizionale. Non è un'attenuazione: è ciò che questa posizione di lettura consente di dire.

---

### 2. I rilievi

#### Bloccanti

---

##### R1 — Il documento promette «chi li ha assegnati, chi li ha verificati» e non lo consegna. Non si capisce se a verificare la proposta di un modello sia stata una persona o un altro modello. **BLOCCANTE**

Il sottotitolo annuncia: «Come ciascuna categoria […] riceve tre valori di mood che nessuna fonte osserva, **chi li ha assegnati, chi li ha verificati**, e che cosa non autorizzano a concludere».

Che cosa il testo consegna davvero:

- chi ha assegnato: «un modello linguistico in una sola invocazione manuale» (§0), «la **proposta** di un modello» (§2). Il **nome del modello non compare in questa pagina**: §2 dice che «Prompt, nome del modello e data dell'invocazione sono versionati insieme alla proposta», cioè in un file che il lettore di questa pagina non ha davanti;
- chi ha verificato: «**un attore** distinto da quello che ha ottenuto la proposta» (§3).

«Attore» non dice se sia un essere umano. E il testo, poche righe dopo, spinge verso la lettura opposta a quella che il resto della pagina suggerisce: «entrambe le **sessioni** ereditano le **istruzioni di progetto che il sistema inietta**» (§3, «Che cosa l'indipendenza dichiarata non copre»). Sessioni con istruzioni iniettate dal sistema sono sessioni di agente, non persone.

Le due letture non sono equivalenti e cambiano ciò che il documento afferma:

- **se il verificatore è una persona**, allora §2 («un LLM propone, una persona decide») descrive il processo e la «verifica indipendente» è ciò che il lettore assume;
- **se il verificatore è una seconda sessione di modello**, allora l'intera catena — proposta e verifica — è stata eseguita da modelli, la persona ha deciso solo di accettarne l'esito, e la «condizione 4 della quinta fonte dati» risulta soddisfatta da un modello che verifica un modello. È un metodo difendibile, ma è **un altro metodo**, e va scritto.

Perché è un difetto e non una preferenza: il documento si è dato per compito di rispondere a «chi», la risposta è la sola cosa che il lettore non può ricostruire da solo, e la formulazione scelta è compatibile con entrambe le risposte. In una pagina la cui tesi centrale è «questi valori sono decisi da una persona» (§0: «Sono decisi da una persona»), l'identità del decisore e quella del verificatore non possono restare implicite.

**Che cosa lo chiuderebbe**: dire in §3, in chiaro, che cosa fosse l'«attore» che ha verificato (persona? sessione di modello distinta? quale?) e riportare in §0 o §2 il nome del modello che ha prodotto la proposta, invece di rimandarlo a un artefatto. Se la verifica è stata condotta da una sessione di modello, dirlo e aggiungerlo all'elenco di §3 «Che cosa l'indipendenza dichiarata non copre».

---

##### R2 — I riferimenti «§2», «§4», «§5», «§7» indicano ora le sezioni del criterio ora quelle di questa pagina, e una sola volta è detto quale. **BLOCCANTE**

Passaggi:

- §3, tabella degli spostamenti: «`§5`, secondo segnale: la proposta la poneva alla stessa cadenza di `Anime Features`»;
- §3, `CF-1`: «**§2** impone alle etichette generiche […]; **§5** attribuisce a ogni formato episodico […]»; «§7 esclude esattamente quella mossa»;
- §3, `CF-2`: «perché **§4** la dichiara archetipo dell'estremo alto»;
- §3, `CF-1`, chiusura: «cioè in una versione successiva della tabella (**§5 di questa pagina**)»;
- §3, sopra la tabella: «il secondo segnale di **§5**».

In questa pagina, §2 è «I quattro passi», §4 è «La copertura», §5 è «Il contratto di versione», §7 è «Limiti dichiarati». Nessuna di queste sezioni contiene «segnali», «archetipi» o una regola sulle etichette geografiche. Il lettore che segue il riferimento come è scritto arriva ogni volta nel posto sbagliato — e la sola disambiguazione esplicita («§5 di questa pagina») lo autorizza attivamente a leggere tutte le altre occorrenze come riferimenti interni, perché quella è la marcatura che il documento usa quando vuole dire «qui».

Perché è un difetto di sostanza e non di stile: la tabella di §3 e i tre ritrovamenti `CF-*` sono **la prova centrale del documento** — sono ciò che dimostra che la verifica ha davvero misurato qualcosa contro un metro. Se il lettore non può risolvere i riferimenti, quella prova non è ispezionabile. E il collasso è insidioso perché entrambi i documenti hanno una numerazione di sezioni che parte da 1.

**Che cosa lo chiuderebbe**: qualificare ogni riferimento al criterio (`criterio §5`, o `mood_assignment_criteria.md §5`) e lasciare i «§N» nudi al solo uso interno — o l'inverso, purché sia uno solo.

---

##### R3 — «tutto questo riduce l'errore nella costruzione» e «un modello capace»: due affermazioni valutative che nulla nel documento sostiene, e la prima contraddice §7. **BLOCCANTE**

§6, ultimo capoverso: «Criterio dettagliato, proposta di un **modello capace**, verifica riga per riga, conteggio pubblicato: tutto questo **riduce l'errore** nella costruzione, e non cambia la natura del dato.»

Due problemi distinti.

**(a) «riduce l'errore»** è un'affermazione quantitativa e causale: dice che una grandezza — l'errore — è più bassa di quanto sarebbe stata. Il documento non misura alcun errore, non ha un valore di riferimento, e **dichiara altrove che non può averne uno**: §7, ultimo capoverso, «Nessuno di questi confronti guarda il mondo. Che un profilo assegnato sia *quello giusto* per una categoria non è una domanda a cui esiste risposta automatica». Se non esiste modo di sapere quanto un profilo sia sbagliato, non esiste modo di sapere che il processo abbia ridotto lo scarto. Le due frasi non possono essere vere insieme nel senso in cui la prima è scritta. È anche in tensione con §3, dove il documento è esemplare nel rifiutare esattamente questa mossa: «Questo numero non è un voto sulla proposta».

**(b) «un modello capace»** è un giudizio sulla qualità dello strumento, senza metro, senza nome del modello in pagina (cfr. R1) e senza nulla che lo sostenga. In una pagina che vieta i superlativi non ancorati, «capace» fa lavoro persuasivo gratis.

Perché è un difetto: è il punto in cui il documento cede alla tentazione che dichiara di voler evitare, e lo fa nella sezione che stabilisce la confidenza — cioè dove il lettore sta decidendo quanto fidarsi. Un lettore scettico che arriva a §6 dopo aver apprezzato il rigore di §3 legge «riduce l'errore» e retrocede su tutto il resto.

**Che cosa lo chiuderebbe**: riformulare in termini di ciò che il processo effettivamente offre, non di ciò che produce — per esempio «rende ogni valore contestabile contro un testo scritto prima», che è quanto §7 già dice correttamente («Ciò che il processo garantisce è che ogni scostamento sia **discutibile contro un testo**»). E togliere «capace», o sostituirlo col nome del modello.

---

##### R4 — Quattro affermazioni comparative o superlative senza alcun valore che le sostenga, in un documento che dichiara la regola opposta. **BLOCCANTE**

1. **§0**: «Questa pagina documenta l'**unico strato interpretativo del progetto**. **Ogni altro numero** pubblicato da StreamWave BI descrive un campo letto da una fonte o discende da uno per una trasformazione che chiunque può rieseguire». È un'affermazione universale su tutti gli altri numeri del progetto, e nulla in questa pagina la sostiene. Peggio: **il documento stesso la mette in dubbio**. §2 descrive il benchmark della `004` come un caso in cui «il passaggio irripetibile era la raccolta di una fonte esterna», e §6 dice che per quei benchmark «la regola e il suo primo caso d'uso sono contemporanei». Un valore raccolto una volta a mano da una fonte esterna non è «una trasformazione che chiunque può rieseguire». Se ne segue che o l'esclusiva di §0 è falsa, o va ristretta a qualcosa di più preciso di «unico strato interpretativo».
2. **§8, ultima riga**: «dove la distanza fra «ancorato» e «vero» è **la più grande di tutto il progetto**». È una graduatoria fra tutti i documenti del progetto: presuppone una misura di quella distanza per ciascuno, che non esiste.
3. **§2**: «la garanzia vale contro **la variante più comune del difetto** — il criterio adattato ai numeri dopo averli visti». Un'affermazione di frequenza relativa su una popolazione mai definita né osservata.
4. **§3**: «vedi il ritrovamento `CF-1` qui sotto, che **da solo tocca più celle di quante ne siano state spostate**». Questo è un confronto fra due conteggi: 2 (ancorato) e il numero di celle toccate da `CF-1`, **che non è mai scritto**. Il lettore può contare cinque etichette elencate in `CF-1` e supporre una cella per etichetta, ma deve fare due assunzioni non dichiarate (che l'asse coinvolto sia solo quello del ritmo, e che «toccare» significhi una cella per categoria). Il confronto è quindi un valore derivato pubblicato senza il valore da cui deriva.

Perché sono difetti e non preferenze: il documento stesso, in §8, si mette sotto la «**severità stretta**: una quantità priva di marcatore è un errore, non un avviso», e §3 dimostra di conoscere e rispettare la regola quando rinuncia ad ancorare `0,05` e lo dichiara. Quattro affermazioni comparative senza sostegno in un testo che si presenta come esemplare di quella disciplina non si leggono come sviste: si leggono come la prova che la disciplina copre solo le cifre e non i confronti — cioè, dal punto di vista del lettore esterno, che copre il caso facile.

**Che cosa lo chiuderebbe**: (1) restringere l'esclusiva a un'affermazione difendibile («l'unico strato in cui il valore non è letto da alcuna fonte», se è vero) o toglierla; (2) e (3) eliminarli, non hanno sostituto ancorabile; (4) pubblicare il conteggio delle celle toccate da `CF-1` come valore con identificativo proprio, o dire «cinque etichette sull'asse del ritmo» rendendo esplicito il criterio di conteggio.

---

##### R5 — §8 è la sezione che il lettore scettico usa per verificare, e promette più di quanto i suoi due comandi consegnino. **BLOCCANTE**

§8 presenta due comandi con due commenti:

```
python3 scripts/check_audit_coherence.py   # tassonomia, e ogni cifra di questa pagina contro la tabella
git log --follow --oneline docs/mood_assignment_criteria.md \
  data/curated/dim_category_mood.json      # l'ordine dei quattro passi
```

Tre scarti fra ciò che è promesso e ciò che i comandi possono fare, tutti verificabili sul solo testo:

**(a) «l'ordine dei quattro passi»**, ma il comando elenca **due** file su quattro passi. Manca `dim_category_mood_proposal.json`, che è l'artefatto del passo 2 e che §2 includeva nel comando equivalente. Senza di esso il passo 2 non compare nell'ordine. Inoltre l'artefatto del passo 3 è, per §2, «**il campo `verification` della tabella**», cioè un campo del file del passo 4: passo 3 e passo 4 sono lo stesso commit e **non sono ordinabili fra loro da alcun `git log`**. Al massimo il comando mostra 1 prima di 4, non «l'ordine dei quattro passi». Che il presidio centrale del metodo sia l'ordine (§2: «l'ordine non è una sequenza di comodo: è ciò che il metodo offre al posto della parola») rende questo scarto grave: la sezione «come si verifica» dichiara verificabile la cosa che il documento chiede di credere.

**(b) «Il commit che introduce il criterio non contiene alcun valore della tabella, nemmeno di prova»** (§2). È un'affermazione sul **contenuto** di un commit; `git log --oneline` mostra solo hash e oggetto e non può stabilirla. Il lettore che volesse controllarla deve inventarsi lui il comando (`git show`). Un'affermazione presentata come verificabile con uno strumento che non la verifica.

**(c) «ogni cifra di questa pagina contro la tabella»**: contraddetto dal documento stesso in §3, «*(Il valore `0,05` non porta ancora perché non esiste come identificativo negli artefatti di questo progetto)*». Se almeno una cifra non ha ancora, «ogni cifra» è falso; e più in generale diverse cifre della pagina non provengono dalla tabella ma da altri artefatti (il `2021` del business case, il conteggio degli identificativi di ancoraggio del criterio). Cfr. anche R10.

**Che cosa lo chiuderebbe**: allineare il comando a quello di §2 (tre file), dire che cosa l'ordine dei commit stabilisce davvero (passo 1 prima di 2 e 4; 3 e 4 congelati insieme), aggiungere il comando che ispeziona il contenuto del commit del criterio, e sostituire «ogni cifra» con «ogni cifra ancorata».

---

#### Non bloccanti, in ordine di gravità

---

##### R6 — §4: «Non serve che qualcuno se ne ricordi» descrive come automatico un presidio che il documento stesso mostra essere manuale.

§4: «La risposta di questa feature non è una persona: è un controllo che fallisce. […] **Non serve che qualcuno se ne ricordi: serve solo che il controllo giri**, ed è già la condizione che ogni feature esegue prima di proporre un commit. […] L'obbligazione scritta non sparisce, cambia ruolo […] **Ma non è più lì che la garanzia poggia.**»

Nel documento non compare alcun meccanismo che faccia girare il controllo da sé: §8 lo presenta come un comando che una persona digita, e §4 stesso lo àncora a una **consuetudine di processo** («la condizione che ogni feature esegue prima di proporre un commit»), cioè precisamente a qualcuno che se ne ricorda. La frase «serve solo che il controllo giri» sposta la dipendenza umana di un passo — dal ricordarsi della tassonomia al ricordarsi di lanciare lo script — e la presenta come eliminata.

Rilievo **condizionale**, non ho potuto verificarlo: se esiste un hook di pre-commit o una CI che esegue `check_audit_coherence.py` senza intervento, il passaggio è vero e manca solo la riga che lo dice; se il controllo si lancia a mano, il passaggio è falso come è scritto e «non è più lì che la garanzia poggia» è un'attenuazione di un limite reale.

**Che cosa lo chiuderebbe**: nominare il meccanismo che garantisce l'esecuzione, oppure riformulare in «il presidio non è più la memoria di chi tocca la tassonomia ma quella di chi lancia il controllo — che è una condizione più facile da rispettare perché non dipende dal sapere che questa tabella esiste».

---

##### R7 — Il prodotto di questa tabella è una distanza fra una scala assegnata e una scala osservata, e la pagina non dice mai che cosa renda le due confrontabili.

§1: la tabella «rende calcolabili […] `BQ2-K2` (**la distanza fra il profilo mediano di un segmento musicale e quello del catalogo**)».

§7: «Un `mood_energy` pari a 0,95 per `Action & Adventure` **non ha lo stesso statuto** di un `energy` pari a `0.95` letto su una traccia musicale […] Confonderli significa trattare un giudizio come un'osservazione, e nel modello dati **i due valori si incontrano sullo stesso asse** — che è esattamente il punto in cui la confusione è più facile.»

Il documento identifica benissimo il rischio, e poi non dice che cosa autorizzi comunque a **sottrarre** un numero dall'altro, che è ciò che una distanza fa. Calcolare una distanza fra due scale richiede che 0,55 assegnato e 0,55 osservato indichino la stessa posizione sull'asse — cioè una calibrazione. L'unico indizio che questa calibrazione esista è di passaggio e non è presentato come tale: §2 dice che chi verifica «apre `reports/data_profile.json` per risolvere i **sei identificativi di ancoraggio della scala**». Un lettore attento può sospettare che il criterio ancori la propria scala a valori osservati sul dominio musicale, ma la pagina non lo afferma mai, e §7 — che è l'elenco dei limiti — non contiene la voce che ci si aspetterebbe: *la distanza fra un profilo assegnato e un profilo misurato è confrontabile solo nella misura in cui la scala di assegnazione è stata ancorata a quella misurata*.

Rilievo **condizionale**: se il criterio calibra esplicitamente la scala su valori osservati, manca solo una frase in §7 che lo dica e ne dichiari il residuo; se non lo fa, `BQ2-K2` è una differenza fra unità diverse e il limite taciuto è il più importante della pagina. Non ho potuto verificarlo.

---

##### R8 — La candidezza del documento sul processo copre un'assenza mai nominata: nessuno ha mai confrontato questi valori con un secondo giudizio indipendente, e §7 lo dichiara in una forma che lo attenua.

§7, ultimo capoverso: «Che un profilo assegnato sia *quello giusto* per una categoria **non è una domanda a cui esiste risposta automatica** — la sola difesa è il processo di §2».

L'avverbio «automatica» fa un lavoro che non gli spetta. Una risposta **non** automatica a quella domanda esiste ed è ovvia per chiunque conosca il problema: far assegnare le stesse categorie a un secondo giudice indipendente e misurare l'accordo. Il documento non la esegue — legittimo — ma non la nomina neppure, e la formulazione lascia intendere che nessuna risposta sia disponibile, il che è diverso da «non è stata cercata». La stessa cosa accade in §7 poco sopra: «Due persone che applicassero il criterio alle stesse categorie **non otterrebbero** le stesse righe» — affermazione empirica su un esperimento che nessuno ha condotto (e per giunta appoggiata a un altro documento: «il criterio lo dichiara fra i propri limiti»).

Il punto generale, e la ragione per cui lo scrivo pur non essendo bloccante: questa pagina dichiara moltissimi limiti — §0, la coda di §2, la coda di §3, l'intero §7, la coda di §8 — e li dichiara bene. L'effetto cumulativo sul lettore è una fiducia che **la trasparenza sul processo non ha guadagnato sul merito**: tutto ciò che viene dichiarato riguarda come i valori sono stati prodotti, e nulla riguarda se siano buoni, perché nulla lo ha mai testato. Un documento così candido rischia di far concludere che la questione sia stata affrontata. §7 arriva a un passo dal dirlo e si ferma sull'avverbio.

**Che cosa lo chiuderebbe**: una riga che nomini il controllo di accordo fra giudici indipendenti come la verifica che darebbe una risposta, e dichiari che non è stata fatta e perché (costo, o assenza di un secondo giudice indipendente dal criterio).

---

##### R9 — §6: la tabella dichiara fonte `Sintetico`, il testo dice che è stata ammessa una «quinta fonte dati». Non si capisce se l'etichetta sia una delle quattro allargata o una nuova.

§6, tabella: fonte `Sintetico`. §6, prosa: «la constitution è stata emendata per ammettere le assegnazioni dell'analista congelate in un artefatto versionato **come quinta fonte dati**». §2 e §3 citano «la **condizione 4 della quinta fonte dati** della constitution».

Se è stata creata una quinta fonte, il suo nome non è `Sintetico` e la tabella di §6 usa un'etichetta che non è quella della fonte a cui il testo assoggetta la tabella; se invece la definizione di `Sintetico` è stata allargata, allora non è una «quinta» fonte ma la stessa fonte con una definizione nuova. Le due letture non possono essere vere insieme, e il lettore che voglia capire sotto quale regime la tabella è pubblicata non ha modo di deciderlo. Il capoverso è per il resto molto onesto — dice che la definizione precedente non copriva questo caso e che regola e caso d'uso sono contemporanei — ed è un peccato che la conclusione resti ambigua.

**Che cosa lo chiuderebbe**: usare in tabella lo stesso nome che la constitution dà alla fonte, quale che sia.

---

##### R10 — La riga che dichiara la disciplina dei marcatori è più forte di ciò che i marcatori del file fanno.

§8: «**Ogni cifra** pubblicata in questa pagina porta un'ancora invisibile **all'identificativo che la produce**».

Nel sorgente, molte cifre portano un marcatore che non è un identificativo — le occorrenze di `<!--#-->` su «tre», «quattro», «due», «sei», «cinque», su `2021` e su `0,05`. Il documento non spiega da nessuna parte che cosa `#` significhi (rimanda a `convenzioni-marcatura.md`, che il lettore non è tenuto ad aprire), e §3 dichiara esplicitamente un'eccezione: `0,05` «non porta ancora». Quindi «ogni cifra […] porta un'ancora all'identificativo che la produce» è, sul file stesso, falso — nella lettura più naturale della frase.

Rilievo **condizionale**, e visibile solo nel sorgente: se `#` è a sua volta un «marcatore» nel senso che §8 usa nella frase successiva («una quantità priva di marcatore è un errore»), allora la prima frase e la seconda usano due nozioni diverse senza distinguerle, e va riscritta la prima. Non ho letto le convenzioni di marcatura e non posso stabilire quale sia la semantica corretta.

---

##### R11 — Alcune quantità che sono fatti letti su un artefatto portano il marcatore delle quantità non misurate.

Sempre nel sorgente, e in dipendenza dalla stessa semantica non verificata di R10:

- «il catalogo Netflix usato come proxy è fermo al **2021**`<!--#-->`» (§7), che è un fatto sul dataset ed è persino attribuito a una fonte nella frase stessa (`A2` del business case);
- «il criterio fissa **due**`<!--#-->` cifre decimali» e «i valori proposti sono tutti multipli di **0,05**`<!--#-->`» (§3, `CF-3`), che sono fatti letti rispettivamente sul criterio e sulla tabella;
- «i **sei**`<!--#-->` identificativi di ancoraggio della scala» (§2), che è un fatto sul criterio;
- «le **42**`<!--@MOOD.coverage.rows-->` categorie» sono correttamente ancorate — cfr. però R12.

**Se** `#` significa «questa quantità non è un fatto misurato», questi marcatori sono dichiarazioni materialmente false su quantità che invece lo sono, e sono esattamente la categoria che nessun controllo automatico può intercettare. **Se** invece `#` significa soltanto «per questa quantità non esiste un identificativo pubblicato», il rilievo cade e resta solo R10. Non ho potuto verificarlo e non ho aperto le convenzioni.

Segnalo separatamente da R10 perché la correzione è diversa: R10 si chiude riscrivendo una frase, R11 — se fondato — si chiude pubblicando quegli identificativi.

---

##### R12 — Lo stesso identificativo àncora sia il numero di righe della tabella sia il numero di categorie del catalogo, e la seconda affermazione è quella che dovrebbe verificare la prima.

§1: «per ciascuna delle **42**`<!--@MOOD.coverage.rows-->` categorie del catalogo video».
§4: «una riga per ciascuna delle **42**`<!--@MOOD.coverage.rows-->` categorie **di `catalogs.netflix_categories_normalized`**».

`MOOD.coverage.rows` — a giudicare dal nome — è una proprietà della tabella di mood. In §4 quel numero è usato per dire quante categorie ha **il catalogo**: l'affermazione di copertura totale risulta così ancorata al proprio soggetto invece che alla fonte con cui va confrontato. È circolare come ancoraggio.

L'effetto pratico è limitato, e va detto: la garanzia vera di §4 non è quel numero ma il confronto **insiemistico** che lo script esegue, e il documento ha ragione da vendere quando spiega perché («una categoria rinominata a monte lascia i conteggi identici e gli insiemi diversi»). Ma un lettore che controlla gli ancoraggi trova qui un numero che sembra provenire dal catalogo e proviene dalla tabella.

Rilievo **condizionale** sulla semantica dell'identificativo, che non ho potuto ispezionare.

**Che cosa lo chiuderebbe**: ancorare l'occorrenza di §4 a un identificativo che conti le categorie del catalogo, distinto da quello che conta le righe della tabella. Se i due identificativi coincidessero, la copertura totale sarebbe una tautologia.

---

##### R13 — Nessuno dei due controlli che §2 descrive legge le affermazioni di questa pagina **sul criterio**, e la pagina non lo dice fra i limiti.

§2 stabilisce con cura che i controlli sono due e con oggetti disgiunti: la verifica indipendente «guarda i valori»; la revisione in contesto pulito «guarda questa pagina» e chi la esegue riceve «**solo** questo file — non il criterio, non la proposta, non la tabella». §7 chiude dicendo che il controllo di coerenza «confronta questa pagina con la tabella che la alimenta, e la tabella con il catalogo».

Ne segue un buco che nessuna delle tre garanzie copre: **le parafrasi che questa pagina fa del criterio**. Che «§2 imponga alle etichette generiche di restare centrali per assenza di segnale», che «§5 attribuisca a ogni formato episodico a durata fissa una cadenza più alta», che «§4 dichiari `Children & Family Movies` archetipo dell'estremo alto», che «§7 escluda» la mossa di preferire una regola all'altra: sono affermazioni sul contenuto di un altro documento, e sono **l'intera argomentazione di `CF-1`, `CF-2` e della tabella degli spostamenti**. Chi verifica i valori non legge questa prosa; chi legge questa prosa non ha il criterio; lo script confronta cifre. Un errore di parafrasi qui — anche in buona fede — non verrebbe intercettato da nulla, e produrrebbe un ritrovamento `CF-1` che sembra un difetto del criterio ed è un difetto della citazione.

Il documento è per il resto scrupolosissimo nel dichiarare che cosa non è coperto (§2 «Che cosa non stabilisce», §3 «Che cosa l'indipendenza dichiarata non copre», §7 in blocco). Questo è l'unico scoperto strutturale che non compare in nessuno di quegli elenchi.

**Che cosa lo chiuderebbe**: una riga in §7 o in coda a §2 che dichiari lo scoperto, oppure citare testualmente i passaggi del criterio invece di parafrasarli, così che la verifica diventi possibile per chiunque apra i due file.

---

##### R14 — Il `grep` di §2 è presentato come verifica di una condizione che non può stabilire.

§2: «per cui la condizione è **verificabile con una ricerca**», seguito da un `grep -rniE "openai|anthropic|api[._-]?key|requests\.(get|post)|urllib\.request" scripts/`.

La condizione da verificare è: «nessuno script chiama mai il modello». La ricerca proposta è un test negativo con tre limiti che il testo non nomina — copre solo `scripts/` e non il resto del repository; copre un elenco chiuso di stringhe (nessun altro fornitore, nessun client HTTP diverso da `requests`/`urllib`, nessuna chiamata via subprocess o via un file di configurazione); e soprattutto non dice nulla sul fatto che la tabella **sia stata** prodotta senza script, dato che uno script cancellato non compare in un `grep` dell'albero di lavoro.

Non è bloccante perché la condizione è comunque presidiata altrove — dal congelamento dell'artefatto — e perché il documento non nasconde che l'invocazione è avvenuta a mano. Ma «verificabile con una ricerca» promette di più di quanto un'assenza di risultati valga.

---

##### R15 — La «condizione 4» è dichiarata soddisfatta da un numero che il documento stesso dice non misurare la qualità.

§6 elenca fra le cinque condizioni della fonte «**verifica indipendente con esito quantificato**». L'esito quantificato è, in §3, «Ha spostato **2** celle», accompagnato dall'ottima avvertenza «Questo numero non è un voto sulla proposta […] Un conteggio basso può descrivere una proposta aderente al criterio oppure un criterio che non dà appigli: da solo non distingue i due casi».

Le due cose insieme dicono che la condizione costituzionale è soddisfatta da una quantificazione che, per esplicita ammissione, non quantifica ciò che al lettore interessa. Non è una contraddizione — la condizione chiede un numero, il numero c'è — ma è un punto in cui il documento potrebbe chiudere il cerchio e non lo fa: dire che cosa la condizione 4 intenda ottenere con quel numero, visto che chi lo pubblica ne dichiara l'ambiguità interpretativa. Senza quella riga, un lettore scettico può concludere che la condizione sia una formalità.

---

##### R16 — Il fatto che il catalogo sia Netflix usato come proxy compare per la prima volta a §7.

Il documento parla di «catalogo video» in §1, §2, §3 e §4, e nomina `catalogs.netflix_categories_normalized` in §4 senza commento. Solo a §7 si legge «il catalogo Netflix **usato come proxy**». Il riassunto di §0, che dichiara la volontà di mettere «la cautela in cima e non in fondo», menziona il 2021 ma non la natura di proxy.

Il lettore che abbandona la pagina prima di §7 — e §0 lo incoraggia a fidarsi del riassunto in cima — non sa che le categorie profilate non sono quelle di StreamWave. È il limite con l'effetto più ampio su tutti i KPI a valle e arriva più tardi di tutti gli altri.

---

### 3. Che cosa il documento fa bene

Da non rompere correggendo il resto.

1. **§3, il capoverso sul significato del «2».** «Questo numero non è un voto sulla proposta, ed è il punto in cui è più facile leggerlo male […] Un conteggio basso può descrivere una proposta aderente al criterio oppure un criterio che non dà appigli: da solo non distingue i due casi, e questa pagina non chiede al lettore di assumere il primo.» È il passaggio migliore della pagina: anticipa l'inferenza sbagliata, la nomina, e rifiuta di trarne vantaggio. Qualunque riscrittura deve conservarlo intatto.
2. **§2, «Che cosa questa prova stabilisce / Che cosa non stabilisce».** La distinzione fra un fatto sui file e un fatto sullo stato di conoscenza di chi scriveva, con l'ammissione che «la cronologia git è riscrivibile da chi la produce». È il modo corretto di presentare un presidio parziale, e vale come modello per tutte le altre affermazioni della pagina (compresa quella di §4, cfr. R6).
3. **La pubblicazione dei tre `CF-*`.** Un documento che pubblica i difetti del proprio metro, dichiara che le celle interessate **non** sono state spostate e spiega perché non spostarle fosse la scelta corretta (§3: «preferirle §5 sarebbe stato decidere sul criterio, non verificare contro il criterio»), fa esattamente ciò che il lettore scettico cerca. `CF-3` in particolare — la griglia a 0,05 sotto una dichiarazione a due decimali — è un'ammissione che nessuno avrebbe scoperto da fuori.
4. **§6, la contemporaneità dell'emendamento.** «La regola è più stringente di ciò che sostituiva, ma non è un vincolo esterno preesistente che il lavoro ha incontrato.» È l'obiezione più naturale a chi si scrive le proprie regole, sollevata dal documento prima che la sollevi il lettore.
5. **§7, «Il profilo è dell'etichetta, non dei titoli»** e il divieto di lessico causale. Chiudono le due inferenze che un lettore trarrebbe spontaneamente — dal profilo di categoria al singolo titolo, e dalla vicinanza di profilo a un nesso di causa — e le chiudono in modo netto e non attenuato.
6. **§4, la distinzione insiemi/numerosità.** «Una categoria rinominata a monte lascia i conteggi identici e gli insiemi diversi.» È il tipo di dettaglio che dimostra che il presidio è stato pensato, non dichiarato.
7. **§0 e §5.** La cautela in apertura invece che in coda, e un contratto di versione scritto **prima** che esista un consumatore che possa violarlo, con la distinzione fra invalidare e correggere.

---

### 4. Che cosa questa revisione non garantisce

- **Non garantisce che le affermazioni del documento su artefatti esterni siano vere.** Non ho aperto la tabella, la proposta, il criterio, gli script, la constitution, la roadmap né alcun documento delle altre feature. Se il criterio non dice ciò che §3 gli attribuisce, se la tabella non contiene i campi `verification`, `criterion_findings`, `independence_residual`, `version` che il testo le attribuisce, se lo script non esegue il confronto insiemistico descritto in §4, questa revisione non se ne è accorta e non poteva.
- **Non garantisce i valori.** Non ho visto una sola riga della tabella oltre alle cinque cifre citate nel testo, e non avrei comunque alcun metro per giudicare se `Action & Adventure` meriti 0,95 di energia. Questa revisione ha letto una descrizione di un processo, non il suo esito.
- **Non garantisce l'aritmetica degli ancoraggi.** Non ho risolto nessun identificativo `MOOD.*` né `catalogs.mood_categories`: non so se `0,55` sia davvero il valore congelato per `Anime Series`, né se `42` sia il numero di righe. R11 e R12 sono formulati su ciò che i nomi degli identificativi suggeriscono, non su ciò che contengono.
- **Non garantisce la semantica dei marcatori.** Non ho letto `convenzioni-marcatura.md`. Tutto ciò che dico su `<!--#-->` (R10, R11) è condizionato a un'ipotesi sul suo significato, dichiarata nei rilievi.
- **Non garantisce l'ordine dei fatti.** Non ho eseguito alcun comando `git`: che il criterio preceda i valori è per me un'affermazione del documento, non un fatto verificato. R5 riguarda ciò che il comando proposto *potrebbe* mostrare se eseguito, non ciò che mostra.
- **Non garantisce la completezza sui limiti taciuti.** Un limite che il documento non nomina e che dipende da come sono fatti gli artefatti che non ho letto è, per costruzione, invisibile a questa lettura. R7 è l'unico caso in cui il testo lasciava abbastanza tracce perché il sospetto si formasse; altri della stessa specie possono esserci senza aver lasciato tracce.
- **Non garantisce nulla sul pubblico reale.** Ho letto come «persona competente e scettica», che è un lettore ipotizzato. Un lettore che arrivi alla pagina da un link diretto a §6 o §7, senza aver letto §0, incontra un documento diverso da quello che ho letto io.

---

## Blocco di chiusura — a cura della sessione revisionata

**Data**: 2026-08-20 · **Aggiunto dopo** il commit `37cca7e`, che ha portato il verbale in questo repository senza che il documento fosse ancora stato toccato.

Il testo del revisore qui sopra non è stato modificato in alcun punto. Questo blocco dichiara come ciascun rilievo è stato chiuso, distinguendo quattro esiti: **risolto** (il difetto non c'è più), **indebolito** (l'affermazione è stata ritirata o ridotta a ciò che il documento può sostenere), **respinto con la prova** (il rilievo non è fondato, e la prova è citata), **rinviato** (riconosciuto e non chiuso qui, con la ragione).

### I cinque bloccanti

| | Esito | Come |
|---|---|---|
| `R1` | **risolto** | §3 dice ora in chiaro che a verificare è stata **una seconda sessione di modello**, non una persona, e che il ruolo della persona è un altro: decidere se accettare l'esito. §0 e §2 nominano `Claude Sonnet 5` e la data dell'invocazione invece di rimandarli alla proposta. «Proporre e verificare sono stati entrambi passi eseguiti da un modello» è ora la prima frase di «Che cosa l'indipendenza dichiarata non copre», come il rilievo chiedeva. |
| `R2` | **risolto** | §2 introduce una convenzione esplicita — «criterio §5» per il criterio, «§5» nudo per questa pagina — e tutte le occorrenze sono state qualificate. La disambiguazione singola «§5 di questa pagina», che il revisore indicava come la causa del collasso, è stata tolta perché non serve più. |
| `R3` | **risolto** | «riduce l'errore» sostituito da ciò che il processo produce davvero — «ogni valore contestabile citando un testo scritto prima che il valore esistesse» — con la ragione esplicita per cui la formulazione precedente era incompatibile con §7. «Un modello capace» sostituito da «un modello», e il nome sta in §0 e §2. |
| `R4` | **(1) indebolito, (2) (3) (4) risolti** | **(1)**: l'esclusiva è ora quella che la constitution usa per definire la classe di dato — «gli unici valori che nessuna fonte osserva e nessuna formula calcola» — e §0 nomina il controesempio che il revisore aveva trovato nel documento stesso, il parametro della `004`, dicendo in che cosa il caso differisce. È un indebolimento, non una riparazione: l'affermazione precedente non era difendibile. **(2)** e **(3)**: eliminate, non avevano sostituto ancorabile. **(4)**: il confronto fra conteggi è stato tolto; il rinvio a `CF-1` ora richiama l'elenco puntuale delle etichette, che il documento già pubblicava. |
| `R5` | **risolto, e ha scoperto un difetto più grave del rilievo** | §8 ha ora tre comandi: il controllo, la cronologia dei **tre** artefatti, e `git show --stat` sul commit che introduce il criterio — che è ciò che rende ispezionabile l'affermazione sul **contenuto** di quel commit, punto (b) del rilievo. Un capoverso dichiara che la cronologia ordina il passo 1 rispetto al 2 e al 4 e **non** ordina il 3 rispetto al 4, perché stanno nello stesso commit. «Ogni cifra» è diventato «ogni cifra ancorata». |

**Il ritrovamento dentro `R5`.** Verificando il comando che il rilievo chiedeva di allineare, è emerso che **il comando di §2 non funzionava**: `git log --follow` accetta un solo percorso e falliva con `fatal: --follow requires exactly one pathspec`. Era nel documento fin dalla prima stesura, è passato sotto un controllo di coerenza verde — che non esegue i comandi — e il revisore non poteva accorgersene perché il mandato gli vietava di eseguirli. Entrambe le occorrenze usano ora `git log --oneline --reverse --`, che elenca i tre commit dal più vecchio.

### Gli undici non bloccanti

| | Esito | Come |
|---|---|---|
| `R6` | **risolto** | §4 dichiara ora che **non esiste alcun hook di pre-commit né alcuna integrazione continua** in questo repository, e riformula il guadagno come il rilievo suggeriva: non l'eliminazione della dipendenza da una persona, ma il passaggio dalla memoria di chi tocca la tassonomia — che deve sapere che questa tabella esiste — a quella di chi lancia il controllo, che non deve sapere nulla dei profili di mood. |
| `R7` | **risolto** | Il rilievo era fondato e il sospetto del revisore era esatto: criterio §1 **ancora gli estremi ai valori osservati** sul lato musicale, e la tabella lo registra in `conventions.mood_scale_anchor`. §7 ha ora la voce che mancava, con il residuo che il revisore non poteva vedere — **l'ancoraggio è solo agli estremi**, nessun valore osservato calibra il centro dell'asse, e la corrispondenza fra le posizioni intermedie è un'assunzione del criterio. |
| `R8` | **risolto** | §7 nomina ora il controllo che darebbe una risposta — un secondo giudice indipendente e una misura dell'accordo — dichiara che non è stato fatto e dà la ragione vera, che non è il costo: un secondo giudice indipendente dal criterio non esiste in questo progetto. L'avverbio «automatica» non regge più il peso. Corretta anche l'affermazione empirica che il revisore segnalava di passaggio: «non otterrebbero le stesse righe» è diventata un'aspettativa dichiarata come tale. |
| `R9` | **risolto** | L'emendamento **non introduce una nuova etichetta di fonte** e lo dice: la classe vive sotto `Sintetico`, la cui definizione si allarga. §6 lo riporta e spiega perché la tabella dice `Sintetico` e non un nome nuovo. «Quinta fonte» è diventato «quinta **classe** di fonte» in tutte le occorrenze. |
| `R10` | **risolto** | La frase era falsa come scritta. §8 descrive ora le **due specie** di marcatore: l'ancora, che il controllo confronta con l'artefatto, e la dichiarazione di non-misurato, su cui il controllo non verifica nulla e registra soltanto che chi scrive ha considerato quel numero. La severità stretta è riferita all'assenza di entrambi. |
| `R11` | **un punto accolto, gli altri respinti con la prova** | **Accolto**: `2021` era ancorabile e non era ancorato. `docs/convenzioni-marcatura.md` §2 chiama questo «il caso peggiore» della categoria dei fatti dichiarati altrove, e il revisore ci è arrivato senza poter leggere quel testo. Ora porta `NF.num.release_year.max`, che è più forte del rimando ad `A2`. **Respinto per gli altri**: `<!--#-->` non significa «questa quantità non è un fatto misurato» ma «questa quantità **non è un valore di questi artefatti**» — convenzioni §2, che elenca fra i casi coperti proprio i fatti dichiarati altrove. «Due cifre decimali» e «sei identificativi» sono fatti letti sul criterio, che non è fra gli artefatti che ancorano; `conventions.mood_rounding` non li può ancorare perché le ancore a `conventions` accettano solo un letterale fra apici inversi con appartenenza esatta (`check_audit_coherence.py`, `resolve` e il ramo dei letterali). La prosa di §8 dice ora dove quei fatti vivono, che è l'onere che le convenzioni pongono su chi scrive. |
| `R12` | **risolto** | Il rilievo migliore del verbale, e trovato senza poter risolvere un solo identificativo. §4 àncora ora il conteggio del catalogo a `CL.NF.category.distinct` — che la pipeline della `003` osserva e pubblica — e quello della tabella a `MOOD.coverage.rows`, dicendo esplicitamente perché i due identificativi devono restare distinti. Il criterio usava già `CL.NF.category.distinct` per lo stesso numero: la circolarità era solo qui. |
| `R13` | **risolto** | Le regole del criterio su cui poggiano `CF-1` e `CF-2` sono ora **citate alla lettera** invece che parafrasate, con una nota che dichiara perché. E lo scoperto è dichiarato dove il revisore ha notato che mancava: la coda di §3 dice che nessuno dei controlli legge le affermazioni di questa pagina *sul criterio*, che un errore di citazione produrrebbe un `CF-*` che sembra un difetto del criterio, e che la sola difesa applicata è la citazione testuale. |
| `R14` | **risolto** | §2 distingue ora ciò che un esito vuoto stabilisce da ciò che non stabilisce, con i tre limiti che il revisore elencava — una sola cartella, un elenco chiuso di stringhe, nessuna traccia di uno script cancellato — e dichiara che il presidio vero è il congelamento, non la ricerca. |
| `R15` | **risolto** | §6 dice ora che cosa la condizione 4 ottiene con un numero: che la verifica lasci una traccia della propria estensione, confrontabile con l'elenco puntuale di §3. E che un conteggio pari a zero sarebbe stato un ritrovamento da dichiarare, non un successo — che è la ragione per cui la condizione chiede un esito *quantificato* e non un esito *positivo*. |
| `R16` | **risolto** | §0 dice ora, nel riassunto in cima, che il catalogo non è di StreamWave: è quello di Netflix, usato come proxy, e fermo al 2021. |

### Che cosa non è stato corretto, e perché

**Il criterio conserva la frase che `R4.1` contesta.** `docs/mood_assignment_criteria.md` §7 dice «questo è l'unico strato interpretativo del progetto», che è la stessa affermazione ritirata da §0 del documento pubblicato. **Non è stata corretta deliberatamente.** Il criterio è l'artefatto la cui prova sta nell'essere stato committato prima che qualunque valore esistesse: modificarlo ora, a valori congelati, sporcherebbe proprio il presidio che §2 descrive — un criterio ritoccato dopo aver visto i numeri, sia pure su una frase di motivazione. Il costo di lasciarla è che un lettore del criterio incontra un'affermazione che il documento pubblicato non sostiene più; il costo di toglierla è un commit sul criterio successivo alla tabella. Il secondo è più caro. La riscrittura del criterio è già dovuta per `CF-1`, e comporterà una versione successiva della tabella: la frase si corregge lì, dove la modifica del criterio è dichiarata e attesa.

**Il README è stato allineato** nello stesso passaggio, perché ripeteva sia l'esclusiva di `R4.1` sia l'ambiguità di `R1` sul verificatore.

### Verifiche eseguite dopo le correzioni

- `python3 scripts/check_audit_coherence.py` → **uscita 0**. La severità stretta ha respinto quattro numerali non marcati introdotti dalle correzioni stesse, che sono stati sistemati prima di questo blocco;
- i **tre comandi di §8** sono stati eseguiti e restituiscono tutti uscita 0 — inclusi i due che il difetto trovato dentro `R5` rendeva non eseguibili.
