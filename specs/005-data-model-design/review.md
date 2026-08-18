# Revisione in contesto pulito — `docs/data_model.md`

**Data della revisione**: 2026-08-18
**Data della trascrizione**: 2026-08-18
**Oggetto**: `docs/data_model.md` alla versione del commit **`388981b`** — sha256 del contenuto letto: `9cba6f71315b387b6170c122a1758f399c2a1f81cf0b9394d867c90704951939`

```bash
git show 388981b:docs/data_model.md
```

Il documento sarà modificato per chiudere i rilievi: chi legge questo verbale contro la versione attuale può non ritrovare i passaggi citati. Vanno confrontati con la versione qui sopra, che è quella che il revisore ha letto.

## Come è stata condotta

**Natura**: contesto pulito. La revisione è stata affidata a un **subagent isolato** che ha ricevuto **un solo file** — una copia di `docs/data_model.md` in una cartella vuota fuori dal repository — con il vincolo esplicito di non aprire nient'altro: niente `specs/`, niente `docs/`, niente artefatti sotto `reports/`, niente `git`, niente rete. Il revisore non ha partecipato alla stesura e non ha potuto chiedere chiarimenti.

La forma è **più stretta** di una sessione umana a cui si incolla il testo: una sessione vuota vede ciò che le si dà, ma potrebbe raggiungere il resto; questa non aveva modo di sapere che il resto esistesse. Il revisore dichiara di sua iniziativa, in apertura, di non essere uscito dal perimetro e di aver eseguito una sola operazione con strumenti — la lettura del file.

Il mandato chiedeva di rispondere a **tre domande** prima di formulare qualunque rilievo, di cercare in particolare le affermazioni derivate senza sostegno e i limiti mancanti, e di **non proporre correzioni**: il compito del revisore è rilevare.

**Sull'ordine dei passi, che questa volta è quello giusto.** Il verbale è stato trascritto e committato **prima** che il documento venisse toccato, come `CLAUDE.md` prescrive. È l'obbligo che la `004` aveva mancato, recuperando il verbale dopo e dichiarandolo come recupero; qui non c'è nulla da recuperare, e la garanzia che chi trascrive non abbia ammorbidito nulla è quella che l'ordine dei passi può dare.

**Due note di fedeltà della trascrizione**, che riguardano la forma e non il contenuto:

- il testo che segue è **integrale e non modificato**. Sono stati abbassati di un livello i titoli, perché il verbale entra come corpo di questo file, ed è stata rimossa la coda tecnica che l'infrastruttura aggiunge in fondo a ogni risposta di un subagent. Nient'altro è stato toccato — inclusi i punti in cui il verbale rinvia a un proprio rilievo con una sigla diversa da quella con cui lo numera più sotto;
- nel rilievo `R13` il revisore **cita i marcatori di non-misurato alla lettera**, nella forma in cui compaiono nel sorgente del documento. Sono commenti HTML e restano invisibili nella resa di questa pagina: chi legge il verbale reso vede due anni senza il marcatore di cui il rilievo parla, e per vederli deve aprire il sorgente di questo file. La citazione non è stata alterata per renderla visibile, perché alterarla sarebbe correggere il verbale.

**Il verbale non si corregge.** Il blocco di chiusura, in coda, è l'unico testo che chi è stato revisionato può aggiungere: dichiara come ogni rilievo è stato chiuso, distinguendo *risolvendolo* da *indebolendo l'affermazione*. Il testo del revisore resta come è arrivato, anche dove sbaglia.

---

## Verbale

### 1. Apertura

**Che cosa ho letto.** Un solo file, per intero e una sola volta in lettura completa (con rilettura di §2, §3.4, §5, §8, §12 e §18):

`/private/tmp/claude-501/-Users-valerioquaranta-Documents-BI-Streamwave-proj/ebd722e9-49b0-4395-b4bd-af81a18bb484/scratchpad/revisione-005/data_model.md`

**Che cosa non ho letto.** Nulla d'altro. Nessuna uscita dal perimetro: non ho aperto altri file, non ho elencato cartelle, non ho eseguito comandi, non ho ispezionato git, non ho consultato rete. In particolare **non ho visto** e non ho verificato nulla di: `business_case.md`, `docs/data_cleaning.md`, `docs/convenzioni-marcatura.md`, la constitution, il contratto della pipeline, il «rendiconto della trasformazione», il «profilo dei dati di origine», `reports/bq3_scenarios.json`, le schede dei singoli KPI, e i verbali di revisione citati (rilievi `R4`, `R7`, divergenze 1, 6, 7). Non ho la spec né il piano di questa feature.

**Che cosa questo comporta.** Ogni volta che il documento dice «il business case dichiara», «la trasformazione dichiara», «la revisione ha stabilito», io leggo un'asserzione di seconda mano che non posso confrontare con la fonte. Lo segnalo dove pesa. Allo stesso modo, **nessuno dei valori ancorati è verificabile da me**: posso solo controllarne la coerenza aritmetica interna, cosa che ho fatto dove i numeri si parlano fra loro.

**Sui marcatori.** Sono leggibili e non ostacolano la lettura. Non ne ho trovato nessuno sintatticamente rotto o troncato. Non li ho revisionati come sintassi. Ho però trattato come oggetto di revisione, perché il mandato lo chiede espressamente, **la classificazione di un fatto come misurato o non misurato** — che è un'affermazione di merito, non una convenzione tipografica: vedi R13.

**Un'annotazione sull'unico calcolo che ho fatto io.** Per valutare alcuni passaggi ho eseguito qualche aritmetica sui numeri pubblicati (113.550 + 450, 113.550/89.741, 114.000/114). Dove uso un risultato mio lo dichiaro come mio, perché la categoria «affermazione derivata senza fonte» è proprio quella su cui rilevo.

---

### 2. Esito complessivo

Il documento è **notevolmente sopra la media** per un artefatto di questo tipo. Fa cose che quasi nessun modello dati scritto fa: dichiara di non essere stato eseguito (§1), separa la grana d'ingresso da quella del risultato (§7), giustifica le esclusioni di colonna con una regola invece che caso per caso (§9), elenca ciò che il modello rende impossibile (§18) e nomina chi eredita ogni decisione rinviata (§19). La prosa è tesa, quasi mai decorativa, e in molti punti argomenta contro sé stessa prima che lo faccia il lettore.

**Si regge da solo? Quasi.** Un lettore che ha in mano solo questo può capire l'architettura, i nomi, le grane e il perché delle esclusioni. Non può però, con questo solo documento, **scrivere le misure**: mancano due cose senza le quali chi scrive `BQ1-K3` e `BQ2-K2` deve inventare una decisione analitica (come si aggrega il profilo di mood del lato video dalle 42 righe per categoria a un profilo di catalogo — R2), e la riga di `BQ2-K3` in §8 è direttamente contraddetta da §15 (R1). Chi costruisce la dashboard sta meglio: eredita vincoli chiari.

**Il difetto di carattere del documento** — quello da cui discende metà dei rilievi che seguono — è che **argomenta più forte di quanto misuri**. Quando ha un numero lo ancora scrupolosamente; quando non ce l'ha, non tace, ma alza il registro retorico. «È l'unico modo», «è il solo punto», «non hanno nulla in comune», «chiunque prenderebbe per un segnale di mercato», «non sono negoziabili»: sono sei affermazioni che il documento non può sostenere e che, in un testo per il resto così attento, si notano proprio perché tutto il resto è cauto. In due casi (R4, R9) l'affermazione forte è **falsa alla luce di altri passaggi dello stesso documento**.

Il secondo difetto è più circoscritto ma più insidioso: **la sezione §18, che è la sezione dei limiti, ha buchi che le altre sezioni riempiono senza dirlo**. Il più grave è R3.

---

### 3. Le tre domande

#### 3.1 Che cosa è un «segmento», e da dove viene?

**Risposta.** Un segmento è un genere dichiarato dalla fonte musicale: il valore del campo `track_genre` dell'insieme alla grana coppia. L'insieme dei segmenti è l'insieme dei suoi valori distinti, e sono 114. Nel modello vive come colonna `segment`, chiave della dimensione `dim_segment`, derivata prendendo i valori distinti di `track_genre` nella tabella di fatto (§13). La parola «segmento» viene dal business case, il nome della colonna dalla fonte, e §2 e §17 dichiarano che le due parole indicano la stessa cosa.

**Quanto mi è costata.** Poco per la definizione: §2 la mette in blockquote, isolata, con l'alternativa scartata e quattro ragioni. È il pezzo meglio costruito del documento. **Molto** per la seconda metà della domanda — «da dove viene» — perché la definizione dice che i segmenti sono i valori distinti di un campo *del dato trasformato*, mentre il numero 114 viene, per ammissione di §3.4, **dal profilo dei dati di origine**. Ho dovuto rileggere §3.4 tre volte e non sono arrivato a convincermi (R9). Un lettore che si ferma a §2 esce con l'impressione che 114 sia stato contato sul dato che il modello userà; non lo è stato.

**Chiarimento che avrei voluto e non ho avuto.** Se `dim_segment.segment` e `fact_track_segment.track_genre` portano gli stessi valori sotto due nomi diversi (R18), e la relazione R5 li congiunge, il documento non dice mai esplicitamente che la relazione è fra colonne di nome diverso. È l'unico punto in cui ho dovuto dedurre una cosa che chi materializza deve sapere per forza.

#### 3.2 Su quale tabella si conta il catalogo musicale, e perché l'altra darebbe un valore diverso?

**Risposta.** Su `dim_track`, che ha 89.741 righe, una per traccia. `fact_track_segment` ne ha 113.550 perché una riga è l'appartenenza di una traccia a un segmento, e una traccia che sta in più segmenti vi compare più volte: contarne le righe conta le appartenenze, non le tracce. Il documento aggiunge che l'errore non produce alcun avviso, solo un numero dell'ordine di grandezza giusto.

**Quanto mi è costata.** Nulla. È la domanda a cui il documento risponde meglio, e risponde tre volte: §3.3 la prepara, §5 la mette in tabella con la colonna «Tabella che dà un valore sbagliato», §17 la ripete a proposito delle colonne nascoste. Non ho dovuto dedurre né indovinare.

**Chiarimento di cui ho sentito il bisogno.** Uno, e mi ha portato a due rilievi. La tabella di §5 promette che per ogni cosa esista «una tabella corretta e una che restituisce un valore **plausibile e sbagliato**». Per il catalogo musicale la promessa è mantenuta. Per le altre tre righe della stessa tabella non lo è: la riga 4 propone come «tabella sbagliata» una tabella a cui il documento ha appena tolto la colonna necessaria (R4), e la riga 2 dichiara `fact_track_segment` corretta per «qualunque cosa per segmento», mentre §18 dedica quattro capoversi a spiegare che contarne le righe per segmento è «peggio che inutile» (R10).

#### 3.3 Che cosa questo modello rende impossibile misurare?

**Risposta, con ciò che §18 dichiara.** (a) Nessun risultato: il modello dice dove i numeri si calcolano, non quanto valgono; (b) nessun raggruppamento dei 114 segmenti in famiglie più larghe; (c) nessuna analisi temporale, per assenza deliberata della dimensione di calendario; (d) nessun dimensionamento di un segmento per conteggio di righe, perché il campione era bilanciato per costruzione e la deduplicazione ha reso quel conteggio variabile senza renderlo informativo; (e) nulla sui pubblici, perché non esiste alcuna entità che rappresenti una persona, una visione, un ascolto o un abbonamento; (f) nessuna rappresentazione del fatto che le due fotografie siano di momenti diversi. §18 aggiunge tre inferenze da evitare, di cui la terza è che il modello non garantisce la correttezza delle misure.

**Quanto mi è costata.** Il testo di §18 è esplicito e non richiede deduzione. Il **costo vero è stato ricostruire ciò che §18 non dice**, e per farlo ho dovuto tornare su §8, §10.1 e §12. Ne ho trovate quattro:

- **il confronto di `BQ1-K2` esclude le serie dal lato video** e le confronta con l'intero catalogo musicale, e il modello rimuove i mezzi per sapere quanto pesi la parte esclusa (R3);
- **i segmenti si sovrappongono**, quindi le aggregazioni per segmento non sono su popolazioni disgiunte, non si sommano, e una graduatoria le tratta come se lo fossero (R11);
- **oggi tre KPI su otto non sono calcolabili affatto**, perché `dim_category_mood` ha zero righe: §15 lo dice come programma di lavoro, §18 non lo dice come limite;
- **manca la regola di aggregazione del profilo di mood del lato video** (R2), che non è un limite ma un buco.

E una delle sei dichiarate mi sembra falsa così com'è scritta: la (e) sui pubblici, contro un nome di misura pubblicato nello stesso documento (R8).

**Chiarimento di cui ho sentito il bisogno.** Se «impossibile misurare» significhi *strutturalmente impedito* o *sconsigliato*. §18 mescola le due cose senza distinguerle: (c) è strutturale (la tabella non c'è), (d) è puramente esortativo — «Il modello non può impedirlo. Questa riga è tutto ciò che può fare» — e (b) è a metà. Il titolo della sezione promette la prima categoria e consegna in prevalenza la seconda.

---

### 4. Rilievi

#### R1 — `BQ2-K3` è dichiarato dipendente da `dim_category_mood` in §15 e indipendente da essa in §8

§15 apre così: «Tre KPI su otto — `BQ1-K3`, `BQ2-K2` e `BQ2-K3` — **non esistono senza il profilo di mood del lato video**, che questo documento non costruisce».

§8 assegna a `BQ2-K3`: «Appartenenza: non si applica | Calcolo: segmento | Risultato: una graduatoria di segmenti | **Tabelle: `dim_segment`**».

Le due affermazioni non possono essere vere insieme. `dim_segment` porta due colonne, `segment` e `is_high_zero_genre` (§10.5): su di essa, sola, non è costruibile alcuna graduatoria, tantomeno una che «non esiste senza il profilo di mood del lato video», che sta in un'altra tabella nemmeno elencata.

**Perché conta.** §8 è la tabella che chi scriverà le misure userà come indice: per ogni KPI, quali tabelle toccare. È l'interfaccia principale fra questo documento e la feature successiva. Una riga di quella tabella è inutilizzabile, e il lettore non ha modo di sapere se l'errore sia in §8 o in §15 — cioè se `BQ2-K3` componga altre misure (nel qual caso l'elenco delle tabelle è concettualmente vuoto e andrebbe detto) o legga direttamente dati (nel qual caso l'elenco è incompleto). Segnalo anche che `BQ2-K3` è l'unico KPI il cui elenco di tabelle non contiene la tabella su cui il suo «Calcolo» dichiarato opera in modo verificabile.

#### R2 — Il profilo di mood del lato video è definito per categoria, ma nessuna regola dice come diventa un profilo di catalogo

§15 fissa la forma di `dim_category_mood`: una riga per categoria, con `mood_energy`, `mood_valence`, `mood_danceability`. §11 dice che sul lato video gli assi «vanno assegnati» a ciascuna categoria. §4 dice che i due lati si toccheranno in `dim_category_mood`, che «porterà il lato video sugli stessi tre assi».

Ma `BQ2-K2` «misura quanto il profilo di mood di un segmento sia vicino a quello del **catalogo video**» (§2, seconda ragione), e `BQ1-K3` produce «un valore, sul catalogo musicale» confrontandolo con `dim_category_mood` (§8). In entrambi i casi serve un profilo **di catalogo**, cioè un'aggregazione delle 42 righe per categoria in tre numeri. Il documento non dice mai come.

Peggio: §8 elenca per `BQ1-K3` le tabelle «`dim_track`, `dim_category_mood`» e per `BQ2-K2` «`fact_track_segment`, `dim_track`, `dim_segment`, `dim_category_mood`». **Né `dim_title` né `bridge_title_category` compaiono in nessuna delle due.** L'elenco implica quindi che il profilo di catalogo video sia una media non ponderata sulle 42 categorie — cioè che una categoria con 12 titoli pesi quanto una con 3.000. Se invece l'intenzione è ponderare per numero di titoli, i due elenchi di tabelle sono incompleti e le relazioni necessarie (R1, R2) sono coinvolte.

**Perché conta.** È una decisione analitica sostanziale, non un dettaglio implementativo: ponderare o no cambia il valore di due KPI su otto e la graduatoria di un terzo. Il documento dichiara in §9 che «una misura non definita nel business case è un'estensione dello scope che la constitution vieta senza motivazione esplicita» — e qui lascia a chi scrive le misure una scelta che ricade esattamente in quella categoria, senza registrarla in §19 fra i vincoli ereditati. §19 elenca otto decisioni rinviate; questa, che è la più pesante che ho trovato, non c'è.

#### R3 — `BQ1-K2` confronta i soli film con l'intero catalogo musicale, e §18 non lo dichiara fra i limiti

§10.1 fa entrare `type` con la motivazione «(a) — `BQ1-K2` misura i soli film», e `movie_duration_min` «intero, vuoto per le serie». §8 conferma: «`BQ1-K2` | Calcolo: **film sul lato video**, traccia deduplicata sul musicale | Risultato: un valore, **sui due cataloghi**».

Il lato video del confronto è quindi un sottoinsieme del catalogo, il lato musicale è l'intero catalogo. Il risultato è dichiarato «sui due cataloghi», ma su un lato non lo è. §18, che è la sezione che elenca ciò che il modello non permette, non menziona la cosa; §19, che elenca i vincoli ereditati, nemmeno.

Aggravante: `tvshow_seasons` è nell'elenco dei campi «Fuori» di §10.1, e nessuna colonna del modello dice quanti degli 8.807 titoli siano film. **Chi legge il modello non può quantificare la parte di catalogo che `BQ1-K2` non copre**, e non gli viene detto che esiste.

**Perché conta.** §18 apre con «l'omissione di un limite è di fatto un'affermazione implicita». Questa è l'omissione che quella frase descrive: un lettore della dashboard che vede «differenza fra la durata mediana del catalogo video e quella del catalogo musicale» leggerà «catalogo video» come il catalogo, perché nulla nel modello lo smentisce. È inoltre l'unico caso che ho trovato in cui il documento *ha* la scelta esplicita in due punti (§8 e §10.1) e non la porta nella sezione dei limiti, dove porta scelte molto meno consequenziali.

#### R4 — La riga 4 della tabella di §5 contraddice la giustificazione di R1 in §6 e l'uso di `BQ1-K1` in §8

§5 dichiara: «per ogni cosa che si voglia calcolare, esiste una tabella corretta e una che restituisce un valore **plausibile e sbagliato**», e poi: «Nessuna delle colonne sbagliate produce un'eccezione, una cella vuota o un avviso».

Riga 4 della tabella: «qualunque cosa **per categoria** | corretta: `bridge_title_category` | sbagliata: `dim_title`, che nel modello non porta più l'elenco delle proprie categorie».

Tre problemi che si sommano.

1. **Contraddice R1.** §6 giustifica l'unica direzione bidirezionale del modello così: «senza di essa **non si può selezionare l'insieme dei titoli a partire da una categoria**, che è ciò che `BQ1-K1` chiede». Con R1 bidirezionale, una misura su `dim_title` filtrata per categoria funziona ed è corretta. `dim_title` non è quindi la tabella che dà un valore sbagliato «per categoria»: è la tabella che R1 esiste per rendere utilizzabile per categoria.
2. **Contraddice §8.** `BQ1-K1` ha «Calcolo: titolo distinto» e fra le tabelle `dim_title`, `bridge_title_category`, `dim_category`. È un calcolo per categoria su `dim_title`.
3. **Contraddice la premessa della sezione.** Se `dim_title` «non porta più l'elenco delle proprie categorie», il tentativo non produce un valore plausibile e sbagliato: non produce nulla. La riga descrive un'impossibilità, non una trappola, e smentisce la frase «Nessuna delle colonne sbagliate produce ... una cella vuota» tre righe più sotto.

**Perché conta.** §5 si presenta come «la regola di lettura, come proprietà dello schema», ed è la sezione che il documento richiama più volte (§3.3, §6, §10.1, §10.6, §17) come il presidio contro l'errore silenzioso. Una delle sue quattro righe è insieme falsa e in contrasto con il resto del modello. Chi la applica alla lettera eviterebbe `dim_title` proprio dove `BQ1-K1` lo richiede.

#### R5 — «è l'unico modo di sapere quali righe sono affette» è falso all'interno dello stesso modello, e la marcatura che giustifica traccia una perdita che il modello non subisce

§12, sulla marcatura `has_conflicting_popularity`: «resta sulla dimensione delle tracce, visibile, proprio perché la perdita non resti implicita — **è l'unico modo di sapere quali righe sono affette**».

Non è l'unico modo. `fact_track_segment` porta `popularity` a grana coppia (§10.6) e `dim_track` porta `genre_count` (§10.4): una traccia con valori di popolarità discordanti fra le proprie righe di fatto è individuabile confrontando minimo e massimo per `track_id` sul fatto. Il modello contiene già l'informazione, in una forma che dà anche lo scarto, non solo il flag.

C'è di più, e pesa più della parola «unico». La stessa sezione dichiara: «Sulla dimensione delle tracce la colonna non entra affatto» e «nel modello **non esiste** una popolarità alla grana traccia». La «perdita» descritta in §12 — la scelta del massimo fra le repliche — è una proprietà **dell'insieme alla grana traccia, che il modello ha deliberatamente escluso**. Il modello non subisce quella perdita: legge il valore per coppia. `has_conflicting_popularity` non è quindi «la traccia della perdita descritta in §12» (§14): è la traccia di una perdita di un artefatto che il modello non usa.

Coerentemente, §14 le assegna «Che cosa condiziona: **nessuna misura**», e §10.4 la fa entrare con il criterio «(c) — rende visibile una proprietà strutturale del modello». Ma una proprietà di un insieme escluso dal modello non è una proprietà strutturale del modello.

**Perché conta.** È l'unica colonna del modello la cui ragione d'essere, come scritta, non si regge: nessuna misura la legge, l'informazione è già derivabile, e ciò che documenta appartiene a un dataset fuori dal modello. §9 stabilisce che «l'assenza di una colonna è una decisione, non una dimenticanza» e che chi vuole aggiungerne una «deve dire quale delle tre soddisfa»: qui la condizione dichiarata non è soddisfatta, nella sezione che quella regola dovrebbe applicare.

#### R6 — §12 e §3.4/§7 descrivono la deduplicazione in due modi incompatibili, e la differenza cade su `BQ2-K1`

Tre passaggi:

- §3.4: «la deduplicazione ha rimosso 450 righe **ripetute**, e una riga ripetuta non è mai l'ultima del proprio genere»;
- §7: «La pipeline ha deduplicato le coppie, rimuovendone 450: entro un segmento ogni traccia compare già una volta sola»;
- §12: «Non esiste un valore giusto: **la fonte ne portava due, e la deduplicazione ne ha dovuto scegliere uno**».

I primi due descrivono la rimozione di righe *ripetute*, cioè identiche: nessuna scelta di valore è in gioco, ed è per questo che l'argomento di §3.4 («una riga ripetuta non è mai l'ultima del proprio genere») funziona. Il terzo descrive una deduplicazione che **ha dovuto scegliere fra due valori diversi**, cioè fra righe non identiche.

Se vale il terzo, allora: (a) le 450 righe non erano semplici ripetizioni e l'argomento di §3.4 perde la sua «ragione di merito»; (b) soprattutto, **la popolarità che `fact_track_segment` porta è essa stessa il prodotto di una selezione non dichiarata** — e §12 costruisce la propria decisione («la misura legge la popolarità dalla tabella di fatto») proprio sulla premessa che quel valore sia quello osservato per quella coppia, contrapposto al massimo scelto sull'altro insieme.

Il documento non chiarisce se le repliche discordanti stiano *entro* una coppia (traccia+genere), nel qual caso il problema è quello appena detto, o *fra* coppie diverse della stessa traccia, nel qual caso §12 è coerente ma «la deduplicazione ne ha dovuto scegliere uno» è scritto male. Ho riletto §12 quattro volte e non l'ho risolto.

**Perché conta.** §12 si apre dichiarandosi «la sezione che chi scriverà `BQ2-K1` deve leggere prima di scrivere la misura». Il punto su cui resta ambigua è precisamente la provenienza del valore che quella misura legge.

#### R7 — «È il solo punto di questo modello in cui una modifica futura può rompere qualcosa in silenzio» è contraddetto da almeno tre altri passaggi

§6, nel riquadro d'obbligo su R1: «**È il solo punto di questo modello in cui una modifica futura può rompere qualcosa in silenzio**, e questa riga esiste perché chi la farà lo sappia prima».

Il documento ne indica almeno tre altri, due dei quali con la stessa formula:

- §15, obbligo 2: «Una scala diversa anche su un solo asse rende la distanza priva di significato **senza produrre alcun errore visibile**: il numero esce comunque, e sembra ragionevole»;
- §13, su `dim_segment`: «un segmento che portasse due valori diversi renderebbe la dimensione non costruibile» — un invariante che «va verificato e non assunto», cioè una cosa che può cedere;
- §5, l'intera premessa: la confusione di grana «non otterrebbe un errore: otterrebbe un numero plausibile e sbagliato», e §18 aggiunge un quarto caso — il conteggio delle righe per segmento, che «il modello non può impedire».

**Perché conta.** Non è un cavillo lessicale: la frase è dentro un **riquadro d'obbligo** rivolto a chi modificherà il modello in futuro, e gli dice, in sostanza, che se sorveglia un punto è a posto. È l'unico luogo del documento in cui un'esagerazione retorica produce un'istruzione operativa sbagliata.

#### R8 — §11 giustifica la scelta di `danceability` con ciò che quel campo misura, dopo aver dichiarato che la fonte non lo pubblica

§11, «Perché il ritmo non è `tempo`»: «`danceability` vive su `0-1` e la glossa del business case per l'asse ritmo — «regolarità e propulsione ritmica» — **descrive un indice composito di regolarità del battito**, non una frequenza. È la definizione del secondo campo, non del primo».

§11, tre capoversi più sotto, «Il limite di «misurato direttamente»»: «I tre campi sono **calcolati dalla fonte, con un metodo che la fonte non pubblica in dettaglio**».

Il documento non può insieme non sapere come `danceability` sia calcolato e sapere che coincide con «un indice composito di regolarità del battito». L'unico argomento che sopravvive alla seconda affermazione è quello di scala — `danceability` vive su `0-1`, `tempo` no — che il documento presenta come la *prima* delle due conseguenze sfavorevoli, cioè come argomento accessorio rispetto a quello di merito.

**Perché conta.** La scelta del campo che realizza l'asse ritmo è una delle poche decisioni analitiche che questo documento prende in proprio («Quali campi realizzino i tre assi non era però stato deciso da nessuno: è una decisione di modello, e questa sezione la prende»). Regge su due gambe, di cui una il documento sega da sé venti righe dopo. La decisione resta probabilmente giusta; la motivazione pubblicata no.

#### R9 — L'argomento di §3.4 sul conteggio dei segmenti è un argomento dal silenzio, poggia su un termine mai definito, ed è indebolito da §18

§3.4 sostiene che 114, letto sul profilo dei dati di origine, valga anche sul dato trasformato, così: «Il rendiconto registra **ogni** valore del profilo che dopo la trasformazione non vale più. Il conteggio dei segmenti non vi compare, né fra i valori privi di controparte né fra quelli fuori perimetro: per **l'invariante di classificazione totale che la pipeline verifica a ogni esecuzione**, significa che è stato riconfrontato sul dato trasformato e non è cambiato».

Tre difetti, in ordine.

1. **«L'invariante di classificazione totale» non è definito, né qui né altrove nel documento.** È il perno logico dell'intero argomento — è ciò che trasforma un'assenza in una conferma — e un lettore che ha solo questo documento non può sapere che cosa affermi. Mi sono fermato qui e non ho potuto verificare oltre.
2. **È un'inferenza dall'assenza.** Regge solo se il rendiconto è esaustivo *e* se il conteggio dei segmenti rientrava nell'insieme dei valori riconfrontati. Il documento afferma la prima condizione («ogni valore») e deduce la seconda dall'assenza dalla lista, il che è circolare: se il valore non fosse stato riconfrontato affatto, sarebbe ugualmente assente dalla lista.
3. **§18 fornisce un controesempio alla premessa.** «Il catalogo musicale **era** bilanciato per costruzione del campione: ogni segmento aveva lo stesso numero di tracce. Sul dato trasformato **non è più nemmeno bilanciato**». Ecco un valore del profilo che dopo la trasformazione non vale più. Compare nel rendiconto? Il documento non lo dice, e lo ancora a un artefatto dal nome diverso (`CL.SP.recalc.genre.row_counts_distinct`) rispetto a tutti gli altri valori della trasformazione (`CL.SP.*`, `CL.NF.*`). O il rendiconto non registra ogni valore invalidato — e la premessa di §3.4 cade — oppure lo registra e §18 sceglie di citare un altro artefatto, e allora resta da spiegare perché.

La «ragione di merito» che §3.4 aggiunge — «una riga ripetuta non è mai l'ultima del proprio genere» — è solida **ma copre solo la deduplicazione**, cioè presuppone che la deduplicazione sia l'unica operazione che ha rimosso righe. Il documento non lo dichiara. §14 dice che la trasformazione «non ha eliminato le righe problematiche: le ha marcate», il che lo suggerisce, ma non lo afferma.

**Perché conta.** 114 è il numero più ripetuto del documento (§2, §3.2, §14, §18, §19), è la cardinalità dell'unità di analisi di un'intera domanda di business, ed è l'unico valore di cardinalità che non viene dall'artefatto da cui vengono tutti gli altri. §3.4 esiste apposta per giustificarlo, dichiarando di volerlo fare «per una ragione che va scritta invece di lasciata dedurre» — e la ragione scritta, per essere valutata, richiede di aprire un artefatto che il lettore non ha.

#### R10 — §5 dichiara `fact_track_segment` la tabella corretta per «qualunque cosa per segmento»; §18 dedica quattro capoversi a dire che contarne le righe per segmento è peggio che inutile

§5, riga 2: «qualunque cosa **per segmento** | corretta: `fact_track_segment`, dove l'appartenenza esiste | sbagliata: `dim_track`, che non sa a quali segmenti una traccia appartenga».

§18: «**Non permette di dimensionare un segmento contandone le righe** — ed è il limite più insidioso, perché il conteggio è l'operazione più naturale che un motore tabellare offre». E: «contare le righe non è diventato meno inutile, è diventato **peggio che inutile**».

Il conteggio delle righe per segmento è «qualunque cosa per segmento» eseguito sulla tabella che §5 dichiara corretta. Le due sezioni non si contraddicono formalmente — §5 parla di quale tabella, §18 di quale operazione — ma §5 è formulata come regola universale («per ogni cosa che si voglia calcolare») e non porta l'eccezione, mentre §18 è a tredici sezioni di distanza e non richiama §5.

**Perché conta.** §5 è la sezione che il documento presenta come il presidio strutturale contro l'errore, e la trappola che §18 chiama «il limite più insidioso» passa attraverso la porta che §5 dichiara sicura. Chi scrive le misure consulta §5; non c'è nulla che lo rimandi a §18 prima di scrivere `COUNTROWS`.

#### R11 — Manca fra i limiti il fatto che i segmenti si sovrappongono, quindi non sono popolazioni sommabili né confrontabili come disgiunte

Il documento stabilisce che una traccia appartiene a più segmenti (§2, §3.3) e che le appartenenze sono 113.550 contro 89.741 tracce. Ne discendono almeno tre conseguenze che §18 non elenca:

- **le quantità per segmento non si sommano**: la somma su tutti i segmenti di qualunque conteggio di tracce non dà il catalogo, e supera 89.741;
- **la stessa traccia contribuisce a più mediane**: §12 lo dice per il caso del massimo di popolarità («Una traccia che sta in due segmenti contribuirebbe a entrambe le mediane con lo stesso numero»), ma lo presenta come difetto di un'alternativa scartata, non come proprietà permanente del modello adottato — che resta vera per i tre assi di mood, letti da `dim_track` e quindi *identici* per tutte le appartenenze di una traccia;
- **`BQ2-K3` ordina 114 popolazioni sovrapposte** come se fossero alternative fra cui scegliere, che è il modo in cui una graduatoria viene letta.

Aggiungo che l'asimmetria di trattamento fra popolarità e mood non è mai discussa: §12 spende una sezione intera per portare la popolarità sulla grana coppia, e i tre assi di mood restano sulla dimensione delle tracce senza che il documento dica se la fonte li registrasse per coppia o per traccia. Se li registrava per coppia, la stessa argomentazione di §12 si applicherebbe e non è stata applicata; se per traccia, andava detto in una riga.

**Perché conta.** `BQ2-K2` e `BQ2-K3` producono rispettivamente «un valore per segmento» e «una graduatoria di segmenti». Un lettore di dashboard legge una graduatoria come una partizione. Il documento non gli dice mai che non lo è.

#### R12 — «Non permette di dire nulla sui pubblici» contro `segment_demand_index`

§18: «**Non permette di dire nulla sui pubblici.** Non esiste in questo modello alcuna entità che rappresenti una persona, una visione, un ascolto o un abbonamento, perché nessuna delle due fonti ne contiene».

§17: «i nomi sono quelli semantici già pubblicati dal business case — `music_adjacent_catalog_share`, **`segment_demand_index`**, e così via».

Un indice di domanda per segmento, costruito su `popularity` (§12: «`BQ2-K1` è una mediana per segmento»), è un'affermazione su pubblici — su quanti ascoltano e quanto. La premessa dell'argomento è corretta (non esiste un'entità persona) ma la conclusione è più larga: dal non avere righe-persona non discende non poter dire nulla sui pubblici, discende non poterlo dire *a livello individuale, e solo per il tramite di un proxy della fonte*.

**Perché conta.** Il documento non definisce mai che cosa sia `popularity` — è l'unico campo sostanziale del modello di cui non spiega la semantica, mentre spende una sezione su `danceability` e una su `duration_ms`. Il limite vero che manca a §18 è proprio quello: che `popularity` è un indicatore della fonte, di costruzione non dichiarata, e che ogni conclusione di domanda di mercato vi poggia sopra. Al suo posto §18 mette una negazione assoluta che il documento stesso smentisce.

#### R13 — Le due date di copertura sono fatti misurati sui dati e sono dichiarate non misurate

§16: «il lato video è fermo al 2021<!--#-->, il musicale al 2022<!--#-->». §18, sotto l'intestazione «**Copertura del dato**»: «catalogo video fermo al 2021<!--#-->, catalogo musicale al 2022<!--#-->».

Che un catalogo si fermi a un anno è una proprietà osservabile del dato — è il massimo di un campo, calcolabile sull'insieme che il modello descrive, e `dim_title` porta `release_year` proprio da quel campo. In entrambe le occorrenze i due anni sono dichiarati come non misurati.

Non rilevo la sintassi del marcatore, che non è mio compito: rilevo **la classificazione**, che è un'affermazione di merito. È esattamente la categoria che nessun controllo automatico può vedere, e sono i due soli casi che ho trovato in tutto il documento. In §18 la classificazione è particolarmente stridente, perché la frase sta sotto un titolo — «Copertura del dato» — che annuncia un fatto sul dato.

Un caso adiacente, di segno diverso: in §5 la frase «113.550 al posto di 89.741 è una sovrastima di **poco più di un quarto**» porta un rapporto derivato da due valori misurati che non ha né ancora né marcatore, a differenza di ogni altro numerale del documento. Vedi anche R14 sulla sua ambiguità.

#### R14 — Affermazioni derivate senza sostegno, concentrate in §18 e §5

Cinque, in ordine di peso.

1. **§18: «oggi esistono 17 conteggi di righe distinti fra i segmenti, con il meno numeroso a 904 righe»**, da cui «il risultato varia, e la variazione è un residuo della deduplicazione che **chiunque prenderebbe per un segnale di mercato**». Il documento pubblica il minimo e il numero di valori distinti, **non il massimo e non la dispersione**. Il lettore non può quindi valutare la conclusione. Con i numeri pubblicati altrove — 113.550 appartenenze e 450 righe rimosse (§3.4, §7) — il totale prima della deduplicazione era 114.000, che su 114 segmenti bilanciati fa 1.000 per segmento (questa è **una mia aritmetica**, non un'affermazione del documento). Se è così, lo scostamento massimo è 96 righe su 1.000, cioè meno del 10%, e le rimozioni valgono lo 0,4% delle righe. Che «chiunque» leggerebbe una dispersione di quell'ordine come segnale di mercato è un'affermazione forte che i numeri pubblicati non sostengono, e che i numeri non pubblicati (il massimo) permetterebbero di valutare.
2. **§18: «Il catalogo musicale era bilanciato per costruzione del campione: ogni segmento aveva lo stesso numero di tracce».** È un fatto misurato — «lo stesso numero» è un numero — enunciato senza il numero e senza fonte. È il valore da cui dipende l'intero argomento del punto precedente, ed è l'unica quantità sostanziale del documento che compare in prosa senza essere pubblicata.
3. **§5: «una sovrastima di poco più di un quarto».** Oltre a non essere ancorata (R13), è ambigua: rispetto a 89.741 lo scarto è il 26,5% («poco più di un quarto», vero); rispetto a 113.550 è il 21,0% («poco più di un quinto», e la frase sarebbe falsa). Il documento non dichiara il denominatore.
4. **§14: «Le righe a popolarità nulla sono 15.844 e non sono distribuite in modo uniforme fra i segmenti».** La non uniformità è un'affermazione derivata; il documento non pubblica alcuna misura di dispersione. Il dato adiacente — «7 segmenti superano la soglia» — la rende plausibile ma non la dimostra, e i due valori sono presentati in punti diversi della sezione senza essere collegati.
5. **§12, per contrasto.** È il caso opposto e vale la pena notarlo: qui il documento pubblica tre valori (720 tracce discordanti, scarto massimo 44 punti, 13 tracce oltre i 10 punti) e ne trae una decisione presentata come dirimente. I numeri dicono che il fenomeno tocca lo 0,8% delle tracce e che 707 delle 720 discordano di dieci punti o meno. Il documento non commenta la scala dell'effetto — cioè non dice se la decisione cambi qualche mediana in modo osservabile. Non è un errore; è l'unico punto in cui la misura pubblicata **sgonfia** l'argomento e il documento non lo raccoglie.

#### R15 — `genre_count` e `is_high_zero_genre` sono seconde strade verso fatti già derivabili, cioè esattamente ciò che §5 e §10.6 esistono per impedire

Il documento fissa un principio e lo applica due volte: «tenerli entrambi offrirebbe **due strade per la stessa domanda**, di cui una sbagliata» (§10.1, su `listed_in`); «replicarli sul fatto creerebbe di nuovo la seconda strada che §5 esiste per chiudere» (§10.6). Poi lo viola due volte in direzione opposta, replicando sulla dimensione ciò che il fatto già contiene.

- **`dim_track.genre_count`**, ammessa con «(c) — dice a quanti segmenti una traccia appartiene». È il conteggio delle righe di fatto di quella traccia, quindi già calcolabile. Peggio: la sua somma su `dim_track` vale 113.550 — cioè riproduce **sulla tabella dichiarata sicura** esattamente il numero che §17 addita come la trappola («un conteggio di `track_id` sul fatto restituisce 113.550, che non è il numero delle tracce»). Il modello nasconde le chiavi per impedire quel numero e poi lascia visibile una colonna numerica che lo restituisce sommandola.
- **`dim_segment.is_high_zero_genre`**, ammessa con «(a)». È, per costruzione, «la quota di zeri del segmento supera la soglia dichiarata dalla trasformazione» — e la quota di zeri è calcolabile dal fatto tramite `is_popularity_zero`, che §14 dichiara essere «ciò che rende calcolabile la quota di zeri di un segmento». Due strade verso lo stesso fatto, di cui una congelata su una soglia che il documento non pubblica.

Aggiungo su `is_high_zero_genre` un problema di classificazione: è ammessa con il criterio **(a)**, «una misura del framework la legge», ma il documento non dice mai quale misura la legge né che cosa ne faccia. §14 scrive «`BQ2-K1`: 7 segmenti superano la soglia dichiarata dalla trasformazione», che è un fatto, non un uso. L'obbligo che §14 descrive — pubblicare la quota di zeri accanto a ogni misura sulla popolarità — è soddisfatto da `is_popularity_zero`, non da questa colonna.

**Perché conta.** §9 costruisce una regola a tre condizioni proprio perché «chi vuole aggiungerne una deve dire quale delle tre soddisfa», e §9 promette che «l'assenza di una colonna è una decisione, non una dimenticanza». La simmetria richiederebbe che anche la presenza lo sia. Su tre colonne su dieci di `dim_track` e una su due di `dim_segment`, la condizione dichiarata non regge all'esame (qui due, più `has_conflicting_popularity` di R5).

#### R16 — `is_repaired_duration` è classificata (c) mentre la sua gemella `is_duration_zero` è classificata (a), per lo stesso ruolo

§10.1: «`is_repaired_duration` | booleano | **(c)** — vedi §14».
§10.4: «`is_duration_zero` | booleano | **(a)** — vedi §14».
§14: entrambe compaiono nella stessa tabella, con la stessa colonna «Che cosa condiziona»: `is_duration_zero` → «`BQ1-K2`, lato musicale: 1 riga»; `is_repaired_duration` → «`BQ1-K2`, lato video: 3 titoli».

Due marcature che condizionano lo stesso KPI, sui due lati dello stesso confronto, entrano nel modello con due criteri diversi. Se `BQ1-K2` legge la prima, legge anche la seconda, e (a) è la condizione giusta per entrambe; se non le legge, (a) è sbagliata per entrambe. Il criterio (c) — «rende visibile una proprietà strutturale del modello» — non descrive una riparazione di dato applicata a 3 titoli.

**Perché conta.** È un difetto piccolo, ma cade nell'unico punto del documento che chiede di essere applicato meccanicamente da altri: §9 chiude con «chi vuole aggiungerne una deve dire quale delle tre soddisfa». Un criterio applicato in modo incoerente dal documento che lo istituisce non vincola nessuno.

#### R17 — `is_duration_zero` viene alzata di grana senza l'invariante che §13 pretende per l'unico altro caso identico

§14: «**Perché `is_duration_zero` sale sulla dimensione delle tracce**, benché la trasformazione la registri alla grana coppia».
§13, su `is_high_zero_genre`, che compie lo stesso tipo di salto: «La derivazione la fa risalire alla dimensione, e questo è corretto **solo se** l'invarianza tiene. Chi costruisce il modello deve quindi verificarla al caricamento: un segmento che portasse due valori diversi renderebbe la dimensione non costruibile, e va **segnalato** invece che risolto scegliendone uno».

`is_duration_zero` è registrata a grana coppia e portata sulla traccia: se una traccia portasse valori diversi su due appartenenze, si porrebbe lo stesso identico problema, e il documento non lo menziona. Inoltre **`is_duration_zero` non compare fra le derivazioni di §13**, che dichiara «Tre costruzioni» ed elenca `dim_category`, `dim_segment` e `duration_min`. Se il salto di grana di `is_high_zero_genre` è una derivazione da regolare, quello di `is_duration_zero` lo è allo stesso titolo.

Il documento offre una ragione perché in questo caso il rischio sia nullo — la durata è una proprietà della traccia — ma è la stessa ragione che offre per `is_high_zero_genre` («è una proprietà del segmento che l'insieme di partenza replica su ogni riga per comodità di lettura»), dove la considera insufficiente e pretende la verifica.

#### R18 — La chiave della relazione R5 congiunge colonne di nome diverso, e il documento non lo dice mai

§3.2: `dim_segment` ha «Chiave: `segment`»; `fact_track_segment` ha «Chiave: `track_id` + `track_genre`».
§10.5: la colonna di `dim_segment` è `segment`, «derivata da `track_genre`».
§10.6: `track_genre` è «chiave, verso `dim_segment`».
§6, R5: `dim_segment` → `fact_track_segment`, uno a molti.

La relazione congiunge quindi `dim_segment[segment]` con `fact_track_segment[track_genre]`: due nomi per la stessa colonna sui due lati della stessa relazione. È legale ed è la conseguenza dichiarata della scelta di §17 («L'unica eccezione è `segment`»), ma **il documento non lo scrive in nessun punto**, e sul lato video la simmetria opposta (`category` su entrambi i lati, §3.1 e §10.2) induce ad aspettarsi il contrario.

Un secondo effetto della stessa scelta: §5 e §17 insistono che il modello faccia coincidere un nome con una grana («due domande, con due nomi»), e qui lo stesso valore porta due nomi in due tabelle, il che è la situazione inversa e crea l'ambiguità speculare — chi vede `track_genre` sul fatto e `segment` sulla dimensione può ragionevolmente chiedersi se siano la stessa cosa. §2 dichiara l'equazione «una volta sola», ma la dichiara fra *segmento* e *genere* come parole, non fra `segment` e `track_genre` come colonne di tabelle diverse.

#### R19 — Le quattro ragioni di §2 sono ordinate «per forza» e la prima è la più debole, per criteri che il documento stesso applica altrove

§2: «Quattro ragioni contro, **in ordine di forza**». La prima: «**La prima è che renderebbe falsa una frase già pubblicata**».

Due osservazioni.

- **Il criterio è in contrasto con la prassi che il documento segue in §7.** Là, di fronte a due affermazioni del business case che non reggono, il documento non le tratta come vincoli: «La correzione alle due affermazioni del business case è portata sul documento originale come nota accanto al testo, secondo la prassi di questo progetto». Se una frase pubblicata si corregge con una nota quando è sbagliata, il fatto che una definizione la renderebbe falsa non può essere la ragione *più forte* per scartarla. Sarebbe al massimo un costo, come la quarta ragione riconosce esplicitamente («cioè una modifica alla scheda di un documento già pubblicato»).
- **L'argomento interno alla prima ragione è asserito, non dimostrato.** «Il profilo di mood di una traccia è invece **unico** — sono tre numeri su tre assi — quindi un raggruppamento costruito su di esso assegnerebbe ogni traccia a un solo gruppo». Il «quindi» non discende: un raggruppamento su tre coordinate continue può assegnare una traccia a più gruppi (per prossimità, per soglia su ciascun asse, per sovrapposizione). Il documento tratta come necessaria una proprietà di una sola famiglia di raggruppamenti possibili.

La seconda ragione — la circolarità di `BQ2-K2` — è invece rigorosa e autosufficiente, e a mio giudizio da sola decisiva. Anche la quarta contiene un superlativo non sostenuto: «È **la sola** lettura compatibile con il fatto che il business case dichiari `BQ2-K1` di fonte `Spotify (reale)`» — dove il documento subito dopo mostra che l'alternativa è compatibile a patto di aggiornare una scheda, cioè che non è incompatibile ma costosa.

**Perché conta.** §2 è la decisione portante del documento, quella che chiude un rilievo di revisione precedente e definisce l'unità di analisi di un'intera domanda di business. È argomentata bene; l'ordinamento dichiarato mette in testa l'argomento più fragile, e chi volesse contestare la decisione attaccherebbe quello.

#### R20 — §4 giustifica l'assenza di una chiave fra titoli e tracce con un fatto sulle tassonomie, e conclude più di quanto la premessa dia

§4: «Non c'è alcuna chiave che leghi un titolo video a una traccia musicale. Non è una lacuna dei dati che qualcuno potrebbe colmare: le due tassonomie classificano lungo dimensioni diverse — quella musicale per stile sonoro, quella video per forma narrativa — e il business case dichiara che **la sovrapposizione lessicale fra le due è trascurabile**. Un titolo e una traccia **non hanno nulla in comune** su cui una relazione possa poggiare».

La premessa riguarda `category` e `track_genre`, cioè le tassonomie, e sostiene al massimo che non si può congiungere una categoria a un genere. La conclusione riguarda `show_id` e `track_id`, cioè le righe. Sono due affermazioni indipendenti: un legame fra titoli e tracce non passerebbe per le etichette di classificazione (colonne sonore, artisti, anni). Inoltre «trascurabile» non è «nullo», e «nulla in comune» sale di un gradino sopra entrambi.

**Perché conta.** Meno degli altri: la conclusione è quasi certamente vera e la decisione è giusta. Ma §4 è la sezione che sostiene un divieto («**non deve esistere**») e il divieto poggia su un sillogismo che non chiude. Rilievo minore per impatto, non per correttezza.

#### R21 — I «quattro obblighi» di §15, dichiarati non negoziabili, sono in realtà due obblighi, una facoltà e una non-decisione

§15: «Quattro obblighi discendono dalla forma, e **non sono negoziabili** da chi la riempie».
Obbligo 1: «la copertura attesa è totale ... **Una copertura parziale è ammessa**, ma va dichiarata».
Obbligo 4: «questo documento **non dice né chi né come** costruisca le righe. È una decisione aperta della roadmap, e resta aperta».

Il primo si autoindebolisce nella frase successiva a quella che lo enuncia: l'obbligo effettivo non è la copertura totale, è la dichiarazione. Il quarto non è un obbligo, è la constatazione che un obbligo non viene posto. Restano non negoziabili il 2 (stessa scala) e il 3 (la confidenza non sale), che lo sono davvero.

**Perché conta.** Minore, ma §15 è l'unica sezione che detta condizioni a una feature che non ha ancora cominciato, e la parola «non negoziabili» è ciò che le dà forza. Applicata a un elenco per metà non vincolante, la indebolisce anche dove sarebbe legittima.

#### R22 — Minori, raggruppati

Li elenco senza svilupparli, con il passaggio.

- **§1 sovradichiara la propria ignoranza.** «Nessuna affermazione di questo documento è stata verificata eseguendola» convive con §1 stessa («nessun numero di questo documento è stato scritto a mano») e con §6 («è **ispezionabile** invece che sperata»). Le cardinalità *sono* verificate, da artefatti eseguiti, solo non dal motore. La frase assoluta, ripetuta identica in §18, è più umile del vero e per questo lievemente fuorviante.
- **§6, precisione della frase che il riquadro d'obbligo impone di verificare.** «R1 è quindi **l'unico cammino** fra `dim_title` e `dim_category`» — R1 collega `dim_title` al ponte; il cammino fra le due dimensioni è R1 + R2. Chi in futuro dovrà «verificare che R1 resti l'unico cammino» deve verificare una frase che, letta alla lettera, è già falsa oggi.
- **§7 promette più di quanto §8 mantenga.** «obbliga ogni KPI a dichiararle tutte» — poi §8 registra «non si applica» per tre KPI e «fuori dal modello» per due. È difendibile, ma è una dichiarazione di non applicabilità, non una dichiarazione della grana.
- **§13 chiama «interne al modello» una derivazione che legge fuori dal modello.** `dim_segment` si costruisce «più `is_high_zero_genre`», che secondo §13 stesso «l'insieme di partenza ... replica su ogni riga»: un campo dell'insieme di origine che nessuna tabella del modello porta (`fact_track_segment` ha quattro colonne, §10.6, e non è fra queste). Inoltre §10.5 presenta `is_high_zero_genre` come lettura diretta («Campo di origine: `is_high_zero_genre`»), mentre `segment`, nella stessa tabella, rimanda a §13.
- **§16 promette «Le assenze che sono decisioni» e ne elenca due**, mentre il documento ne dichiara almeno altre due con la stessa formula: `listed_in` («è **sostituito** dal ponte», §10.1) e la popolarità a grana traccia («la sua assenza è **deliberata**», §12). §9 rimanda a §10, il che attenua ma non annulla: un lettore che cerca le assenze deliberate va al titolo che le promette.
- **§19 introduce «la convenzione sugli importi in euro fissata dagli scenari»** senza che nulla nel documento abbia mai parlato di importi, euro o scenari monetari — gli scenari compaiono solo in §8 come `reports/bq3_scenarios.json`, fuori dal modello. È l'unico punto in cui mi sono fermato per una parola che il documento non introduce.
- **§10.2, la regola sui ponti condanna implicitamente il fatto.** «un ponte che porta attributi smette di essere un ponte e diventa una tabella su cui qualcuno aggregherà» — che è la descrizione esatta di `fact_track_segment`, che porta `popularity` e `is_popularity_zero` e su cui §18 avverte che qualcuno aggregherà. Le due tabelle di appartenenza hanno lo stesso ruolo strutturale, prefissi diversi e regole di contenuto opposte; §17 dice che «il prefisso dice il ruolo», ma il criterio che distingue i due ruoli non è mai enunciato.

---

### 5. Divergenze da chiarire

Non sono difetti: sono punti su cui qualcuno deve decidere, e su cui il documento non ha torto.

**D1 — La sezione §12 vale il proprio peso?** La decisione su quale tabella legga la popolarità è argomentata su due livelli (regola non negoziabile della trasformazione, più ragione di merito) e occupa una sezione intera dichiarata di lettura obbligatoria. I numeri che pubblica dicono che il fenomeno tocca 720 tracce su 89.741 e che 13 di esse discordano di più di dieci punti. La decisione resta giusta per la prima ragione, che è normativa e non dipende dalla scala; ma il documento non dichiara la scala dell'effetto, e chi legge non sa se stia leggendo di una correzione sostanziale o di una formalità. Va deciso se pubblicare quella valutazione o dichiarare che non è stata fatta.

**D2 — Che cosa significa «impossibile» nel titolo di §18.** La sezione mescola impossibilità strutturali (calendario), impossibilità di dominio (pubblici), e operazioni possibilissime ma sconsigliate (conteggio righe, macro-raggruppamenti). Le tre categorie impongono comportamenti diversi a chi costruisce la dashboard: la prima non richiede nulla, la terza richiede un presidio esplicito. §19 ne porta a valle solo una («il conteggio delle righe di un segmento misura il campionamento e non il mercato»). Va deciso se la distinzione vada resa.

**D3 — Se il conteggio dei segmenti debba essere ricontato sul dato del modello.** Indipendentemente da chi abbia ragione in R9, la posizione del documento è che 114 valga anche a valle *per inferenza*. Esiste l'alternativa di ricontarlo sul dato trasformato e ancorarlo lì, che eliminerebbe l'intera §3.4. È una decisione fra costo e argomento, e appartiene a chi conosce il costo.

**D4 — Se `has_conflicting_popularity` e `genre_count` debbano restare.** R5 e R15 mostrano che le motivazioni pubblicate non reggono; non mostrano che le colonne siano dannose. `genre_count` è comoda e ha un rischio (la somma); `has_conflicting_popularity` è una segnalazione di qualità che nessuna misura legge. Tenerle è legittimo, ma con criteri diversi da quelli scritti.

**D5 — Chi decide l'aggregazione del profilo di mood video (R2).** Se la decisione sia di questo modello, della feature che riempie `dim_category_mood`, o delle misure, è precisamente il tipo di domanda che §19 esiste per registrare. Oggi non è registrata da nessuna parte, e il rischio è che ciascuna delle tre feature supponga che l'abbia presa un'altra.

**D6 — Se `BQ1-K2` debba restare un confronto film-contro-catalogo (R3).** Il perimetro può essere corretto — confrontare la durata di un film con quella di una traccia ha più senso che confrontarla con una stagione — ma è una scelta analitica che nessun documento sembra aver dichiarato come tale, e il modello ne rimuove le tracce escludendo `tvshow_seasons`. Va deciso se sia una scelta di questa feature, ereditata dal business case, o non ancora presa da nessuno.

---

**Nota finale sul perimetro.** Dei rilievi qui sopra, R9 dipende in parte da artefatti che non ho potuto aprire (il rendiconto della trasformazione, il profilo di origine, la definizione dell'«invariante di classificazione totale»): se quegli artefatti contengono ciò che il documento presuppone, resta comunque il fatto che il documento non è autosufficiente su quel punto, che è ciò che ho rilevato. R1, R2, R3, R4, R5, R7, R8, R10, R11, R14, R15, R16, R17, R18 sono invece interamente verificabili all'interno del solo file che ho letto, e chi vuole contestarli non ha bisogno di nient'altro che di quello.
