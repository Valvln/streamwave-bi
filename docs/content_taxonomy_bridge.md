# Il profilo di mood delle categorie video

Come ciascuna categoria del catalogo video riceve tre<!--#--> valori di mood che nessuna fonte osserva, chi li ha assegnati, chi li ha verificati, e che cosa non autorizzano a concludere.

Questa pagina documenta l'**unico strato interpretativo del progetto**. Ogni altro numero pubblicato da StreamWave BI descrive un campo letto da una fonte o discende da uno per una trasformazione che chiunque può rieseguire; i valori di [`dim_category_mood.json`](../data/curated/dim_category_mood.json) no. Sono decisi da una persona.

**La cautela sta in cima e non in fondo, perché è la proprietà che definisce il resto.** Il riassunto onesto di ciò che segue è: *valori assegnati, non misurati, proposti da un modello linguistico in una sola invocazione manuale, verificati contro un criterio che l'autore della tabella aveva scritto lui stesso qualche ora prima, su categorie di un catalogo fermo al 2021<!--#-->.* Ogni pezzo di questa frase è argomentato sotto, e ciascuno è accompagnato dal presidio che lo rende almeno contestabile. Nessun presidio lo rende un dato osservato — e questo documento non prova a suggerire il contrario.

---

## 1. Che cosa questa feature produce

Una tabella: per ciascuna delle 42<!--@MOOD.coverage.rows--> categorie del catalogo video, tre<!--#--> valori decimali sul dominio `0-1` — `mood_energy`, `mood_valence`, `mood_danceability`. È l'oggetto che rende calcolabili `BQ1-K3` (l'intervallo di mood occupato dal catalogo video), `BQ2-K2` (la distanza fra il profilo mediano di un segmento musicale e quello del catalogo) e, attraverso quest'ultimo, `BQ2-K3`.

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

**L'ordine non è una sequenza di comodo: è ciò che il metodo offre al posto della parola.** Un criterio scritto dopo che i valori esistono è indistinguibile, a lettura, da un criterio scritto prima — si piega a giustificare i numeri invece di vincolarli, e nessuna lettura del testo può più accorgersene. Ciò che distingue i due<!--#--> casi non sta nel documento, sta nella cronologia:

```bash
git log --follow --oneline docs/mood_assignment_criteria.md \
  data/curated/dim_category_mood_proposal.json \
  data/curated/dim_category_mood.json
```

Il commit che introduce il criterio non contiene alcun valore della tabella, nemmeno di prova, e precede gli altri due<!--#-->.

**Che cosa questa prova stabilisce**: un fatto sullo stato dei file — che il criterio vi compare in un commit anteriore a quello che introduce qualunque valore.

**Che cosa non stabilisce**, e va detto perché l'intestazione del paragrafo potrebbe far credere il contrario: un fatto sullo stato di conoscenza di chi ha scritto. Nulla esclude che chi redigeva il criterio avesse già in mente il profilo che avrebbe assegnato a una categoria, e la cronologia git è riscrivibile da chi la produce. È lo stesso limite già dichiarato dalla `004` per i fattori di banda: la garanzia vale contro la variante più comune del difetto — il criterio adattato ai numeri dopo averli visti — non contro tutte.

### Perché il modello non entra nella pipeline

Il modello ha ricevuto il criterio e l'elenco delle categorie, in una cartella isolata fuori dal repository, e ha restituito le righe. Prompt, nome del modello e data dell'invocazione sono versionati insieme alla proposta.

Se quella chiamata vivesse dentro uno script, la derivazione a valle smetterebbe di essere deterministica: due<!--#--> esecuzioni potrebbero produrre tabelle diverse, e ogni numero pubblicato dalla `007` dipenderebbe da quale delle due<!--#--> qualcuno ha eseguito per ultima. È la ragione per cui `DA-1` ammette l'uso di un modello **solo** a questa condizione, e per cui la condizione è verificabile con una ricerca:

```bash
grep -rniE "openai|anthropic|api[._-]?key|requests\.(get|post)|urllib\.request" scripts/
```

### Le due revisioni sono distinte, e non è un dettaglio di processo

Questa feature ha attraversato **due<!--#--> controlli diversi**, in momenti diversi, con oggetti diversi. Tenerli separati è una decisione presa dopo che una revisione della spec aveva trovato che la prima stesura li faceva collassare in uno.

- **La verifica indipendente della proposta** (passo 3<!--#-->) guarda i valori. Confronta ogni cella con il criterio, che è l'**unico metro** di contestazione ammesso — non un'opinione sul mood di una categoria, e non un perimetro di lettura: chi verifica apre `reports/data_profile.json` per risolvere i sei<!--#--> identificativi di ancoraggio della scala, perché senza di essi l'obbligo che il criterio dichiara più importante non è verificabile affatto. È un passo di lavorazione, avviene prima del congelamento, ed è la condizione 4<!--#--> della quinta fonte dati della constitution.
- **La revisione in contesto pulito** guarda questa pagina. Un revisore riceve **solo** questo file — non il criterio, non la proposta, non la tabella — secondo il protocollo già usato dalle feature precedenti, e produce [`specs/006-content-taxonomy-bridge/review.md`](../specs/006-content-taxonomy-bridge/review.md).

Un solo passaggio non poteva fare bene entrambe le cose: chi confronta valori con un criterio tecnico non sta leggendo la prosa con l'occhio di chi cerca un'inferenza indebita, e chi legge la prosa isolato dal resto non ha — e non deve avere — il criterio davanti.

## 3. Che cosa la verifica indipendente ha trovato

La verifica è stata condotta da un attore distinto da quello che ha ottenuto la proposta, ed è registrata nel campo `verification` della tabella insieme a ciò che non copre.

**Ha spostato 2<!--@MOOD.review.changes_count--> celle.** Entrambe sull'asse del ritmo, entrambe citando lo stesso passaggio del criterio — il secondo segnale di §5, per cui un formato episodico a durata fissa ha una cadenza più alta di un formato a durata libera:

| Categoria | Asse | Valore congelato | Punto del criterio |
|---|---|---|---|
| `Anime Series`<!--@catalogs.mood_categories--> | `mood_danceability` | 0,55<!--@MOOD.category.anime_series.mood_danceability--> | §5, secondo segnale: la proposta la poneva alla stessa cadenza di `Anime Features`<!--@catalogs.mood_categories-->, 0,50<!--@MOOD.category.anime_features.mood_danceability-->, che è a durata libera |
| `Classic & Cult TV`<!--@catalogs.mood_categories--> | `mood_danceability` | 0,55<!--@MOOD.category.classic_cult_tv.mood_danceability--> | §5, stesso caso rispetto a `Classic Movies`<!--@catalogs.mood_categories-->, 0,50<!--@MOOD.category.classic_movies.mood_danceability--> |

**Questo numero non è un voto sulla proposta, ed è il punto in cui è più facile leggerlo male.** Non dice che la proposta era buona: dice quante celle la verifica ha potuto spostare *citando il criterio*, che è l'unica cosa che le era consentito fare. Dove la verifica ha trovato un problema che il criterio non le permetteva di risolvere, la cella è rimasta ferma e il problema è stato registrato altrove — vedi il ritrovamento `CF-1` qui sotto, che da solo tocca più celle di quante ne siano state spostate. Un conteggio basso può descrivere una proposta aderente al criterio oppure un criterio che non dà appigli: da solo non distingue i due<!--#--> casi, e questa pagina non chiede al lettore di assumere il primo.

### I tre ritrovamenti sul criterio

La verifica ha prodotto un esito che il conteggio degli spostamenti non poteva contenere: difetti del **criterio**, non celle da contestare. Sono registrati come `criterion_findings` nella tabella.

**`CF-1` — §2 e §5 si contraddicono sull'asse del ritmo.** §2 impone alle etichette generiche, geografiche e linguistiche di restare centrali su tutti gli assi «per assenza di segnale»; §5 attribuisce a ogni formato episodico a durata fissa una cadenza più alta di un formato a durata libera. Le etichette che sono insieme geografiche o generiche **ed** episodiche cadono sotto entrambe le regole, che dicono cose diverse: `TV Shows`<!--@catalogs.mood_categories-->, `International TV Shows`<!--@catalogs.mood_categories-->, `British TV Shows`<!--@catalogs.mood_categories-->, `Korean TV Shows`<!--@catalogs.mood_categories-->, `Spanish-Language TV Shows`<!--@catalogs.mood_categories-->.

Quelle celle **non sono state spostate**. La proposta segue §2, che è categorico ed esplicito; preferirle §5 sarebbe stato decidere sul criterio, non verificare contro il criterio — e §7 esclude esattamente quella mossa. Il conflitto resta aperto e si chiude riscrivendo il criterio, cioè in una versione successiva della tabella (§5 di questa pagina).

**`CF-2` — il criterio non ha una regola per le etichette di pubblico.** `Children & Family Movies`<!--@catalogs.mood_categories--> riceve positività 0,95<!--@MOOD.category.children_family_movies.mood_valence--> perché §4 la dichiara archetipo dell'estremo alto; `Teen TV Shows`<!--@catalogs.mood_categories--> resta centrale. La differenza discende dall'esistenza di un archetipo dichiarato, non da una regola che chi assegna possa applicare a un'etichetta di pubblico nuova. Nessuna cella spostata: la regola di scelta di §2 sostiene il centro. Il vuoto va colmato nel criterio, non nella tabella.

**`CF-3` — la granularità effettiva è più grossolana di quella dichiarata.** Il criterio fissa due<!--#--> cifre decimali; i valori proposti sono tutti multipli di 0,05<!--#-->, cioè una griglia che il criterio non chiede e non vieta. Non è contestabile citando un punto del criterio, quindi nessuna cella si muove — ma chi legge la tabella deve sapere che la precisione apparente della seconda cifra decimale non corrisponde a una distinzione che il processo abbia davvero fatto.

*(Il valore `0,05` non porta ancora perché non esiste come identificativo negli artefatti di questo progetto: il ritrovamento vive per esteso in `verification.criterion_findings` della tabella.)*

### Che cosa l'indipendenza dichiarata non copre

Chi ha verificato non ha prodotto la proposta, ed è ciò che la condizione 4<!--#--> richiede. Non è però isolamento assoluto: entrambe le sessioni ereditano le istruzioni di progetto che il sistema inietta, e la tabella lo dichiara nel campo `independence_residual` invece di tacerlo. Quelle istruzioni non contengono nulla sui profili di mood; il residuo resta ed è scritto.

Resta anche il fatto più semplice e più difficile da presidiare: **il criterio contro cui la proposta è stata verificata è stato scritto dalla stessa persona che pubblica questa tabella.** Un metro scritto da chi verrà misurato è meglio di nessun metro — è contestabile, sta in un file, e chiunque può leggerlo e trovarlo sbagliato, come `CF-1` mostra sia possibile. Non è la stessa cosa di un metro indipendente, e questa pagina non lo presenta come tale.

## 4. La copertura, e chi si accorgerebbe se la tassonomia cambiasse

La copertura è **totale**: una riga per ciascuna delle 42<!--@MOOD.coverage.rows--> categorie di `catalogs.netflix_categories_normalized`, l'elenco che la pipeline della `003` osserva sul catalogo video. Nessuna categoria manca, quindi non si pone la domanda di che cosa le misure a valle facciano di una categoria senza profilo.

**Non si pone oggi.** Se la tassonomia della fonte cambiasse in un aggiornamento futuro, si porrebbe — ed è la divergenza che la revisione della `002` aveva lasciato aperta con una formulazione precisa: nessuno sapeva chi si accorgerebbe. La risposta di questa feature non è una persona: è un controllo che fallisce.

`scripts/check_audit_coherence.py` confronta l'insieme delle categorie coperte dalla tabella con quello del catalogo video, **prima** di verificare qualunque documento, e si ferma con uscita diversa da zero<!--#--> se i due<!--#--> divergono — stampando quali categorie stanno da una parte e non dall'altra. Non serve che qualcuno se ne ricordi: serve solo che il controllo giri, ed è già la condizione che ogni feature esegue prima di proporre un commit.

**Il confronto è sugli insiemi, non sulle numerosità**, e la distinzione è il motivo per cui il presidio regge: una categoria rinominata a monte lascia i conteggi identici e gli insiemi diversi. È il caso che un controllo sul solo numero di righe lascerebbe passare.

L'obbligazione scritta non sparisce, cambia ruolo: chi tocca la tassonomia della fonte trova qui dichiarato che un controllo lo aspetta. Ma non è più lì che la garanzia poggia.

## 5. Il contratto di versione, per la `007` e per chiunque legga a valle

La tabella porta un campo `version`, oggi 1<!--@MOOD.table.version-->.

**Il contratto**: ogni valore pubblicato che dipende da `dim_category_mood` deve dichiarare **su quale versione della tabella è stato calcolato**. Vale per i tre<!--#--> KPI della `007`, in dashboard come in qualunque documento che li riporti.

La versione si incrementa quando una riga viene corretta dopo il congelamento — per un errore trovato, o per un difetto del criterio come `CF-1` che una revisione del criterio chiude — e la tabella registra che cosa è cambiato e perché. **Una revisione della tabella invalida i valori già pubblicati che ne dipendono**: non li corregge automaticamente, li invalida, e senza il legame esplicito fra valore e versione nessuno saprebbe quali.

La ragione per cui il contratto è scritto qui e non lasciato al buon senso della `007`: senza di esso una correzione lascerebbe in giro numeri «giusti quando sono stati scritti e mai più riverificati». È la stessa classe di difetto di un totale corretto in una feature precedente e rimasto citato altrove nella forma vecchia, che la roadmap registra come precedente da non ripetere.

## 6. Fonte e confidenza

| Metrica | Fonte | Confidenza |
|---|---|---|
| `mood_energy`, `mood_valence`, `mood_danceability` per ciascuna categoria | `Sintetico` | **media** |
| `BQ1-K3`, `BQ2-K2`, `BQ2-K3` (calcolati dalla `007`) | `Derivato` | **media**, non negoziabile |

**Perché `Sintetico` e non `Benchmark (esterno)`.** Un benchmark è un dato osservato su un operatore terzo e trasferito a StreamWave; qui non esiste alcun operatore terzo e non c'è nulla da citare fuori da questo repository. Etichettare la tabella come benchmark le presterebbe un'autorità che non ha — la citazione puntuale e verificabile presso terzi che quella fonte richiede, qui, non può esistere.

**L'etichetta è stata ammessa per emendamento, e la contemporaneità va dichiarata.** Fino alla versione precedente la constitution definiva `Sintetico` come dato generato da script versionati, e qui nessuno script genera nulla — è precisamente la condizione che rende ammissibile il metodo. La revisione della spec di questa feature ha trovato lo scoperto, e la constitution è stata emendata per ammettere le assegnazioni dell'analista congelate in un artefatto versionato come quinta fonte dati, a cinque<!--#--> condizioni: criterio scritto prima del valore, valore congelato e mai rigenerato, versione dichiarata a valle, verifica indipendente con esito quantificato, nessuna promozione di confidenza. Come per i benchmark della `004`, la regola e il suo primo caso d'uso sono contemporanei: la regola è più stringente di ciò che sostituiva, ma non è un vincolo esterno preesistente che il lavoro ha incontrato.

**La confidenza non sale, e non è una scelta.** È un obbligo di §15 di [`data_model.md`](data_model.md). Criterio dettagliato, proposta di un modello capace, verifica riga per riga, conteggio pubblicato: tutto questo riduce l'errore nella costruzione, e non cambia la natura del dato. La tabella è costruita, non osservata.

## 7. Limiti dichiarati

**L'assegnazione non è una misura.** Un `mood_energy` pari a 0,95<!--@MOOD.category.action_adventure.mood_energy--> per `Action & Adventure`<!--@catalogs.mood_categories--> non ha lo stesso statuto di un `energy` pari a `0.95` letto su una traccia musicale: il secondo è un campo della fonte, il primo è deciso da una persona. Confonderli significa trattare un giudizio come un'osservazione, e nel modello dati i due<!--#--> valori si incontrano sullo stesso asse — che è esattamente il punto in cui la confusione è più facile.

**Il profilo è dell'etichetta, non dei titoli.** Una categoria del catalogo è una promessa editoriale, e il suo profilo è il registro che quella promessa evoca — non la media dei contenuti che vi ricadono, che nessuno ha misurato. Un titolo che ricade in una categoria **non eredita** quel profilo, e nessuna conclusione su un singolo contenuto discende da qui.

**Nessun artefatto di questa feature cita un titolo del catalogo.** Né nome, né trama, né cast: gli ancoraggi si esprimono a livello di categoria o di genere musicale come archetipo. La regola chiude, per gli artefatti di questa feature, la parte generale di una divergenza che la revisione della `003` aveva lasciato aperta. Non è un vincolo che tolga qualcosa — l'assegnazione avviene a grana categoria — ma citare titoli renderebbe più facile leggere il profilo come «osservato su quegli esempi» invece che come ciò che è.

**Il valore centrale significa assenza di segnale, non equilibrio misurato.** Una categoria generica, geografica o linguistica riceve il centro perché la sua etichetta non dichiara un registro affettivo, non perché contenga contenuti opposti che si compensano. Le due<!--#--> letture portano a conclusioni diverse su qualunque aggregato le usi.

**Non risponde a**: se una categoria contenga *davvero*, in media, contenuti energici, positivi o ritmati — nessun campo del catalogo video misura energia, positività o ritmo. Né a se due<!--#--> categorie con mood simile condividano pubblico: il mood è un asse di posizionamento, non un dato comportamentale, e questo progetto non ha alcuna misura di audience.

**Nessun lessico causale.** Che una categoria abbia un profilo vicino a un segmento musicale non implica che l'una causi l'attrattività dell'altro, né che chi guarda la prima adotterebbe il secondo.

**La riproducibilità non è fra le proprietà di questa tabella.** Due<!--#--> persone che applicassero il criterio alle stesse categorie non otterrebbero le stesse righe, e il criterio lo dichiara fra i propri limiti. Ciò che il processo garantisce è che ogni scostamento sia **discutibile contro un testo** — non che sia unico.

**Copertura del dato**: il catalogo Netflix usato come proxy è fermo al 2021<!--#--> (`A2` del [business case](business_case.md)). Un cambio di tassonomia in un aggiornamento futuro rende la tabella disallineata; il controllo di §4 lo rileva fallendo, ma non impedisce che il disallineamento si produca.

**Che cosa nessuna verifica di questo progetto garantisce.** Il controllo di coerenza confronta questa pagina con la tabella che la alimenta, e la tabella con il catalogo delle categorie: verifica che gli artefatti non divergano fra loro. Nessuno di questi confronti guarda il mondo. Che un profilo assegnato sia *quello giusto* per una categoria non è una domanda a cui esiste risposta automatica — la sola difesa è il processo di §2, e la trasparenza con cui è descritto qui non è una risposta, è il modo di non fingere che la domanda non esista.

## 8. Come si verifica

```bash
python3 scripts/check_audit_coherence.py   # tassonomia, e ogni cifra di questa pagina contro la tabella
git log --follow --oneline docs/mood_assignment_criteria.md \
  data/curated/dim_category_mood.json      # l'ordine dei quattro passi
```

Nessuno dei due<!--#--> comandi richiede rete, credenziali o i dataset di origine: leggono soltanto artefatti versionati.

**Che cosa si può rifare, e che cosa no.** Si può **rieseguire ogni controllo**: coerenza fra documento e tabella, copertura, scala, ordine dei commit. **Non si può rifare l'assegnazione.** Non esiste uno script che la rigeneri, ed è deliberato: l'invocazione del modello è avvenuta una volta, fuori dalla pipeline, e il suo esito è congelato. Chi non è d'accordo con una riga non la ricalcola — la contesta citando il criterio, e se il criterio non regge, si corregge il criterio e la versione della tabella sale.

Ogni cifra pubblicata in questa pagina porta un'ancora invisibile all'identificativo che la produce, secondo le [convenzioni di marcatura](convenzioni-marcatura.md). Vale la **severità stretta**: una quantità priva di marcatore è un errore, non un avviso. Ciò che il controllo garantisce, e ciò che non può garantire, è dichiarato nella stessa pagina — e vale la pena rileggerlo qui, dove la distanza fra «ancorato» e «vero» è la più grande di tutto il progetto: **i marcatori dichiarano l'origine di un numero, non la sua verità.**
