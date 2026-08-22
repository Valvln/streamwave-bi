# Verbale di revisione in contesto pulito — `docs/kpi_measures.md`

**Feature**: `007b-kpi-measures` · **Data della revisione**: 2026-08-22

## Come è stata condotta

Un subagent isolato ha ricevuto **una sola copia di `docs/kpi_measures.md`**, rinominata `documento.md`, in una cartella fuori dal repository. Nessuno degli altri artefatti della feature — spec, piano, task, script, artefatti JSON, gli altri documenti di `docs/`, la history git — gli è stato reso disponibile, e le istruzioni gli vietavano esplicitamente di cercarli.

**La versione revisionata è ancorata**, perché il documento verrà riscritto per chiudere i rilievi e un verbale che citi passaggi non più esistenti diventa illeggibile:

| | |
|---|---|
| commit che contiene il testo revisionato | `c6e5e08` |
| `sha256` del contenuto letto | `154e76c0319fdf9a04afb751272928c840c07a35beaea6bf8f4d53a090f0cedd` |
| righe del documento letto | 701 |

*(La prima stesura di questa tabella indicava `1c2623d`, che era il `HEAD` del repository quando la copia è stata presa: le modifiche di E9 erano allora ancora nell'area di lavoro. Il commit che le ha congelate è `c6e5e08`, ed è quello il cui contenuto corrisponde all'impronta qui sopra — verificabile con `git show c6e5e08:docs/kpi_measures.md | shasum -a 256`. Correzione all'intestazione, che è di chi è stato revisionato; il testo del revisore non è toccato.)*

**Il testo che segue è del revisore e non viene corretto**, nemmeno dove sbaglia. Chi è stato revisionato aggiunge il proprio blocco in coda.

---

## Verbale

### Apertura — perimetro

**Ho letto un solo file**, per intero (702 righe):
`…/scratchpad/revisione-isolata/documento.md`

**Non ho letto**: il business case, `kpi_operators.md`, `data_model.md`, `content_taxonomy_bridge.md`, `convenzioni-marcatura.md`, `bq3_scenarios.md`, la constitution, nessun file sotto `specs/`, nessun artefatto JSON (`kpi_measures.json`, `kpi_engine_check.json`, `bq3_scenarios.json`), nessuno script, nessun `.pbix`, nessuna history git. Non ho eseguito `git` né alcun comando che tocchi il repository.

**Due uscite dal perimetro, entrambe da dichiarare:**

1. Ho eseguito un `grep` (`terzo|C2|E9|008a|008b|vincol`) **sul solo `documento.md`**, dentro la cartella isolata. Nessun altro file è stato toccato.
2. Per un errore di battitura in un percorso ho tentato una lettura su `/Users/valerioquaranta/Documents/BI/Streamwave_proj/…` (percorso inesistente). La chiamata è fallita con «file does not exist» e **non ha restituito alcun contenuto**: nessuna informazione dal repository è entrata in questa revisione. Lo dichiaro perché l'obbligo è sull'atto, non sull'esito.

Tutte le verifiche numeriche qui sotto sono state fatte a mano sui soli valori pubblicati nella pagina.

---

### Impressione generale

**Il documento fa il suo lavoro, e lo fa a un livello che ho visto raramente in documentazione analitica.** Ho ricalcolato a mano tutto ciò che la pagina rende ricalcolabile e non ho trovato **un solo errore aritmetico**: la quota di §2.1 (375/8807), il gap di §3.1, la quota di film di §3.4 (6131/8807), la sovrapposizione di §4.1 (75832/89741), tutti i punteggi dell'appendice come `0,5·domanda/100 + 0,5·affinità`, l'arrotondamento `ROUND_HALF_UP` sui casi al limite (`groove` 0,59375→0,5938, `latin` 0,37625→0,3763). Ho verificato anche le due cose che il documento non chiede di credere ma afferma: **la soglia di domanda 36,5 è effettivamente la mediana delle 114 domande** (57 segmenti stanno sopra, il 57° vale 37,0 e il 58° 36,0) e **la soglia di affinità 0,8210 è esattamente la mediana delle 114 affinità** (57 sopra, 0,8220 di `classical` e 0,8200 di `grunge` a cavallo). Ho contato i membri del quadrante riga per riga nell'appendice: **sono 33**, come dichiarato, e ogni «sì»/«no» rispetta la soglia stretta, incluso il caso di frizione `grunge` (0,8200 contro 0,8210). Un documento in cui il conteggio dichiarato sopravvive a un controllo manuale su 114 righe è raro.

**Quello che invece non regge è il modo in cui il documento dichiara sé stesso verificato.** Le §§2–8 chiudono tutte con la stessa frase — «**verificato** — la lettura del motore coincide con il valore pubblicato» — mentre la §11.1 dice, correttamente e con notevole onestà, che di 114 segmenti ne sono stati letti 3. Il risultato è che l'affermazione più forte della pagina è ripetuta otto volte in posizione di massima visibilità, e la sua smentita sta in una sezione che il lettore raggiunge alla fine. La §11 è ottima; le otto righe che la precedono la contraddicono. Stessa dinamica, in miniatura, in due frasi di apertura («ogni cifra che segue nasce qui», «ogni valore di questa pagina è calcolato da `build_kpi_measures.py`») che la §8 rende false due schermate dopo.

**Il terzo motivo di interesse è anche il punto in cui la disciplina si allenta.** La pagina costruisce un impianto severo — ogni quantità ancorata o marcata, i confronti derivati sono essi stessi valori — e poi lo viola proprio dove racconta il ritrovamento più prezioso: il valore erroneo `-253,8667` è un'osservazione dal motore pubblicata senza ancora né marcatore, protetta dal fatto di stare dentro un backtick, e «due ordini di grandezza» è un moltiplicatore derivato che nessun valore della pagina sostiene. È l'esatta categoria di errore che il documento dichiara di voler prevenire.

---

### Rilievi

#### A. Rendono il documento falso o insostenibile

---

**R1 — Lo stato «verificato contro il motore reale», ripetuto in otto sezioni, afferma più di quanto la §11 sostenga.**

> §§2.4, 3.4, 4.3, 5.4, 6.3, 7.4, 8 (identico otto volte): «**Stato di verifica contro il motore reale (E9)**: **verificato** — la lettura del motore coincide con il valore pubblicato: sì`<!--@ENGINE.check.all_match-->`»
> §11.1: «Ciascuna restituisce 114 valori, e ne sono stati letti 3: `pop` […]; `jazz` […]; `sleep` […] **che le altre righe coincidano non è verificato**»

Il difetto non è la §11, che è impeccabile; è che la frase ripetuta usa il singolare definito «**il** valore pubblicato» in sezioni dove i valori pubblicati sono decine e quasi nessuno è stato letto dal motore. Tre casi puntuali, in ordine di gravità:

- **§6** pubblica come valori di punta `british` 0,9277 e `sleep` 0,6408 e chiude con «la lettura del motore coincide con il valore pubblicato». `sleep` è fra i tre campionati; **`british` no**. La frase copre un valore che il confronto non ha toccato.
- **§7** pubblica le due soglie (36,5 e 0,8210), il conteggio del quadrante (33) e le prime cinque posizioni, e chiude con la stessa frase. Nessuna di queste grandezze è un valore per segmento campionato: le soglie sono mediane su tutti i 114 e il conteggio è un aggregato su tutti i 114. La §11.1 elenca «`segment_entry_priority`, **sui segmenti campionati**» — cioè non queste.
- **§2.3 e §5.2** trascrivono misure DAX (`c1_music_above_median`, `segment_zero_share`) e **§7.3** ne trascrive tre (`…_score`, `…_quadrant`, `…_rank`). La pagina contiene **dieci** formule DAX, ma la §11 dice «incollando le **otto** misure nel modello» e conta «misure confrontate: 8». Quindi C1, la quota di zeri, il quadrante e la graduatoria non sono mai passati dal motore — e tutte e tre le sezioni che li pubblicano portano il bollino «verificato».

Aggravante di forma: la frase àncora il proprio «sì» a `ENGINE.check.all_match`, che è un esito **al livello della misura** («8 su 8 misure confrontate coincidono»), usato per sostenere un'affermazione **al livello del valore**. È lo stesso salto che il documento condanna altrove.

Aggiungo che la riga di intestazione — «**Stato**: concluso, verificato contro il motore reale» — è la prima cosa che si legge e la meno qualificata di tutte.

**Perché conta**: è l'unica affermazione della pagina che un lettore esterno non può controllare da sé, ed è quella su cui poggia la fiducia in tutto il resto. Detta com'è, un lettore che si fermi alla §7 crede che la graduatoria dell'appendice sia stata confrontata con Power BI. La §11.1 dice il contrario, e con parole ottime («3 segmenti su 114 restano 3 su 114»). La correzione è piccola e non toglie nulla al lavoro: la frase ripetuta deve portare in sé il proprio perimetro (per esempio, distinguere «misura verificata sui segmenti campionati» da «valore verificato»), non rinviarlo a una sezione a valle.

---

**R2 — Due affermazioni di apertura sono rese false dalla §8 e dalle ancore della pagina stessa.**

> §1: «È il primo del progetto in cui un numero pubblicato è un risultato di questa feature e non un input ereditato da una precedente: **ogni cifra che segue nasce qui**»
> §11: «**Ogni valore di questa pagina è calcolato da `scripts/build_kpi_measures.py`**»

Entrambe sono smentite dal documento:

- la §8 dichiara esplicitamente il contrario — «Questa feature non calcola nulla per questi due KPI», «`reports/kpi_measures.json` non contiene alcuna voce `BQ3`» — e pubblica sei valori di scenario ancorati a `BQ3.*`, cioè all'artefatto della `004`;
- decine di cifre in prosa portano ancore `CL.*`, `SP.*`, `MOOD.*`: 8.807 titoli, 19.323 assegnazioni, 42 categorie, 114 segmenti, 89.741 tracce, la versione 2 della tabella dei mood. Sono per definizione input ereditati.

**Perché conta**: la prima frase è un'affermazione di metodo, e il metodo è ciò che questo documento vende. Una frase assoluta («ogni cifra») che la sezione 8 confuta è il tipo di errore che un lettore ostile trova per primo. La correzione è di una parola — *ogni valore di KPI calcolato in questa pagina*, non *ogni cifra* — e non indebolisce niente di sostanziale.

---

**R3 — «Tre misure divergevano di due ordini di grandezza» è un moltiplicatore derivato che nessun valore della pagina sostiene.**

> §11.2: «Al primo, **tre misure divergevano di due ordini di grandezza**: `segment_catalog_affinity` restituiva valori negativi nell'ordine delle centinaia — per `sleep`, `-253,8667` contro lo 0,6408 atteso — e con essa `segment_entry_priority` […] e `mood_profile_overlap`»

Tre problemi in una frase:

- il moltiplicatore è affermato per **tre** misure e mostrato per **una**. Per `segment_entry_priority` e `mood_profile_overlap` nessun valore erroneo è pubblicato;
- per `mood_profile_overlap` il moltiplicatore è quasi certamente **sbagliato in modo qualitativo**: se le tre colonne di `dim_track` valevano centinaia, nessuna traccia cadeva dentro l'intervallo `[0,0500; 0,9500]` e la misura restituiva 0 (o quasi), che non è «due ordini di grandezza» rispetto a 0,8450 — è un azzeramento;
- anche sul solo caso mostrato la quantificazione non torna: da 0,6408 a −253,8667 il rapporto in modulo è ≈ 400, cioè fra due e tre ordini.

**Perché conta**: è esattamente la categoria di affermazione — un rapporto fra valori misurati, scritto in prosa, senza identificativo — che il documento tratta con la massima severità altrove (§2.4: «un confronto fra valori misurati è esso stesso un valore misurato, e questa è la forma in cui si pubblica»). Trovarla nel racconto del ritrovamento più importante è il punto in cui la pagina si applica uno standard più basso di quello che dichiara.

---

**R4 — La spiegazione della causa, come è scritta, predice un difetto che non si è verificato.**

> §11.2: «Le colonne `energy`, `valence` e `danceability` di `dim_track` erano caricate nel modello con il punto decimale interpretato come **separatore delle migliaia** […] un `Change Type` eseguito con locale italiano su un file scritto in notazione inglese.»
> «**Perché `segment_demand_index` non era toccata**, ed è la firma che ha permesso di riconoscere la causa: `popularity` è un intero e non ha punto decimale da fraintendere.»

La «firma» spiega una sola delle misure sopravvissute. Ma **`format_duration_gap` legge `dim_track[duration_min]`** — dichiarata in §3.1 come `duration_ms / 60000`, «senza alcun arrotondamento a livello di colonna», e il cui valore pubblicato è 3,55 — cioè **un'altra colonna decimale della stessa tabella `dim_track`**, caricata dallo stesso `Change Type`. Se la causa fosse quella descritta, la mediana delle tracce sarebbe uscita a migliaia di minuti e il KPI sarebbe stato fra i divergenti. Non lo è stato.

Le spiegazioni possibili sono almeno due (la colonna è calcolata dentro il modello e non tipizzata in caricamento; oppure il file di origine per quella colonna è scritto diversamente), ma il documento non ne offre nessuna.

**Perché conta**: la §11.2 è il pezzo forte del documento — è il ritrovamento che giustifica l'esistenza dell'intero confronto. Un lettore attento arriva alla riga della «firma», ricorda `duration_min` di §3.1 e sospetta che la diagnosi sia incompleta; se la diagnosi è incompleta, la correzione applicata al modello potrebbe esserlo, e con essa l'esito verde di §11.1. Basta una proposizione che dica perché `duration_min` è al riparo.

---

**R5 — Un valore osservato è pubblicato senza ancora e senza marcatore, in una pagina dichiarata in severità stretta.**

> §11.2: «per `sleep`, `-253,8667` contro lo 0,6408`<!--@KPI.BQ2K2.sleep.affinity-->` atteso»

`-253,8667` è una **lettura dal motore reale**: un fatto misurato, con quattro decimali, prodotto da questa feature e per il quale la §11 dichiara che esiste un artefatto apposito (`reports/kpi_engine_check.json`, «è da quell'artefatto, e non da un numero scritto a mano in questa prosa, che ogni valore del confronto riceve la propria ancora»). Il valore atteso accanto ad esso è ancorato; **quello osservato no**, e non porta nemmeno il marcatore di non-misurato. Sta dentro un backtick, il che verosimilmente lo sottrae al controllo automatico.

**Perché conta**: la §12 promette al lettore che «ogni quantità priva di ancora o di marcatore di non-misurato è un errore, non un avviso». Questo è un controesempio, in una pagina che si presenta come il documento in cui quella promessa è più stretta che altrove. È anche il caso peggiore possibile, perché la frase immediatamente precedente rivendica proprio che i valori del confronto non si scrivono a mano in prosa.

---

**R6 — Fatti misurati che portano il marcatore di non-misurato.**

> §2.3: «la quota di §2.1 dice che è il **4`<!--#-->`** per cento circa»
> §7.2: «`metal` […] con punteggio 0,6915, più alto di quello di **105`<!--#-->`** altri segmenti»

Entrambe le cifre sono corrette (0,0426 → 4,26 %; posizione 9 su 114 → 105 sotto, e ho verificato che nessun segmento pareggi il punteggio di `metal`). Ma entrambe sono **riformulazioni di valori misurati** — la prima di `KPI.BQ1K1.share`, la seconda di `KPI.BQ2K3.metal.rank` e di `SP.genre.count` — e portano il marcatore che dichiara il contrario.

**Perché conta**: dichiarare non-misurato ciò che è misurato è, per costruzione, l'unica falsità che nessun controllo automatico può intercettare — la sola contro cui esiste la revisione in contesto pulito. Sono due, sono innocue nel valore e non lo sono nella grammatica: la pagina che definisce lo standard è la pagina peggiore su cui violarlo.

---

#### B. Rendono il documento migliorabile

---

**R7 — Due segmenti con lo stesso punteggio pubblicato ricevono posizioni diverse, contro la regola dichiarata due sezioni prima.**

> §7.2: «**Sui pari merito**: due segmenti con lo stesso punteggio ricevono la **stessa** posizione, e la successiva salta di altrettante unità.»
> §9: riga 85 `death-metal` punteggio **0,4963**; riga 86 `salsa` punteggio **0,4963**.

L'appendice applica la regola tre volte in modo visibile (22/22→24, 41/41→43, 44/44→46) e poi presenta questo caso, che a occhio la contraddice. Ricostruendo i valori esatti la contraddizione si scioglie — `death-metal` vale ≈0,49633 e `salsa` ≈0,49627, e la graduatoria opera sugli esatti — ma **il documento non lo dice mai**: la §7.1 dichiara che *le soglie* sono calcolate sui valori esatti, la §7.2 non dice nulla di analogo per l'ordinamento. Chi controlla l'appendice riga per riga (cioè esattamente il lettore che questo documento merita) trova qui la sua unica apparente incoerenza. Una frase in §7.2 — *l'ordinamento opera sui valori esatti, quindi due punteggi identici in tabella possono avere posizioni distinte* — la chiude.

---

**R8 — I pesi 0,5/0,5 non producono l'influenza paritaria che la loro simmetria suggerisce, e il documento non lo dice.**

> §7.3: «`0.5 * DIVIDE ( [segment_demand_index], 100 ) + 0.5 * [segment_catalog_affinity]`»

Sui valori pubblicati nella pagina stessa: la domanda normalizzata spazia da 0,00 (i sette a mediana nulla) a 0,66 (`pop`), cioè **0,66 di escursione**; l'affinità spazia da 0,6408 (`sleep`) a 0,9277 (`british`), cioè **0,2869**. A parità di peso nominale, la domanda muove il punteggio circa **2,3 volte** più dell'affinità, e la graduatoria è in larga misura una graduatoria di domanda travestita da composizione paritaria.

Il documento argomenta bene *perché* non si riscala sugli osservati (`D3`, e la ragione è solida). Ciò che manca è la conseguenza per chi legge la graduatoria. Nota che questo rilievo si combina con §6.3, che dichiara la **grandezza assoluta** dell'affinità priva di interpretazione indipendente — e poi la §7.3 la usa proprio come grandezza assoluta, sommandola a una quota. La §7 non affronta mai questa tensione con la §6.

*(Le due cifre che cito qui sono derivate da valori pubblicati e andrebbero, se accolte, ancorate come tali — non scritte in prosa.)*

---

**R9 — Il «ritrovamento» di §5.3 potrebbe essere una conseguenza di definizione, e il lettore non ha modo di stabilirlo.**

> §5.3: «**l'insieme dei segmenti a mediana nulla coincide esattamente con quello dei segmenti marcati `is_high_zero_genre`**: sì»
> poco sotto: «più della metà delle righe di ciascuno porta popolarità nulla, la mediana cade dentro quella metà»

La seconda frase spiega la prima *in una direzione*: se la quota di zeri supera 0,5, la mediana **è necessariamente** nulla — non è un ritrovamento, è aritmetica. Il contenuto empirico sta nella direzione opposta (nessun segmento non marcato ha mediana nulla — vero qui: `alternative` a 0,4845 ha mediana 1,0, `dance` a 0,4798 ha 1,0), ma per riconoscerlo il lettore deve sapere **come `is_high_zero_genre` è definito**, e il documento non lo dice mai in nessun punto. Presentare come «ritrovamento» ciò che potrebbe essere una tautologia è un rischio di credibilità evitabile con una riga di definizione.

---

**R10 — L'unica coppia di superlativi che il lettore non può verificare sulla pagina.**

> §5.4: «il segmento **meno numeroso** porta 904 righe contro le 1000 del **più numeroso**»

Gli altri superlativi del documento sono controllabili nell'appendice: `pop` è davvero il massimo di domanda, `british` il massimo di affinità, `sleep` il minimo (li ho verificati tutti e tre). Qui no: **l'appendice non ha una colonna con il numero di righe per segmento**, quindi che 904 sia il minimo e 1000 il massimo su 114 segmenti è affermato e non mostrato. Le due cifre hanno un'ancora ciascuna; l'affermazione di estremalità non ne ha una propria — che è la distinzione su cui la pagina insiste in §2.4.

---

**R11 — Codici e sigle usati prima (o del tutto) senza introduzione, per un lettore esterno.**

- **`E9`** compare otto volte, sempre come «(E9)», e **non è mai definito né rinviato a un documento**. Tutti gli altri codici (`D1`…`D11`, `C1`, `C3`) portano almeno un puntatore a `kpi_operators.md` o `business_case.md`; `E9` no.
- **`008a`** e **`008b`** compaiono come referenti («non è stato rinviato alla `008a`», «compito di chi costruirà la narrazione (`008b`)») senza che si dica che sono feature future.
- **`is_high_zero_genre`** è usato come criterio decisivo in §5.1, §5.3, §7.4 e §9 senza che la sua soglia sia mai dichiarata (vedi R9).
- **`NF.cat.music_musicals.titles`** in §2.4 è presentato come «il dato di **origine**», ma ha la forma di un'ancora e il lettore non capisce se sia un file, una tabella o una chiave d'artefatto.

Nessuno di questi rende falsa la pagina; tutti insieme costano al lettore esterno — che è il destinatario dichiarato — più attrito di quanto il resto del documento gli chieda.

---

**R12 — Dei tre vincoli aperti annunciati, la pagina ne rende conto di due.**

> §3.3: «Era il **primo dei tre** vincoli lasciati aperti da `kpi_operators.md` §12»
> §3.4: «**Secondo** vincolo aperto di §12»

Il terzo non compare mai — ho controllato l'intero testo. O è chiuso altrove e va detto dove, o resta aperto e va detto che resta aperto e a chi spetta. Così com'è, il documento apre un conteggio e lo lascia scoperto. (Analogamente `C1` e `C3` sono trattate e **`C2` non è mai nominata**: se non riguarda questi KPI, una mezza riga lo chiarisce; se li riguarda, manca.)

---

**R13 — In §4.2 i limiti del parallelepipedo si calcolano senza `ALL`, e lì l'omissione non è argomentata.**

> §4.2: `VAR EnergyMin = MINX ( dim_category_mood, dim_category_mood[mood_energy] )`
> §6.2: «Le tre variabili del lato video **non** portano un `ALL` sul lato musicale, e l'omissione è deliberata: […] nessuna relazione propaga il filtro di segmento al ponte»

L'argomento della §6.2 è corretto ma riguarda il **filtro di segmento**. `dim_category_mood` è invece raggiungibile da un filtro di **categoria** (è la tabella che la §6.2 stessa attraversa con `RELATED` da `dim_category`). Una visuale filtrata per categoria — cosa del tutto naturale in una pagina di dashboard — restringerebbe silenziosamente i minimi e i massimi, e con essi la sovrapposizione, senza che nulla lo segnali. Se la scelta è deliberata (per esempio perché la misura è pensata solo come scalare di pagina) va detto qui come è detto in §6.2; se non lo è, è un `ALL` mancante.

---

**R14 — Un'affermazione di riproducibilità che la pagina non tratta come tratta le altre.**

> §1.1: «**Due esecuzioni consecutive producono file identici byte per byte**, e lo stesso vale rigenerando prima `data/processed/`.»

È il confronto fra due osservazioni — cioè, per la regola che la §2.4 enuncia con enfasi, **esso stesso un valore misurato** — e sostiene la garanzia su cui poggia tutto il documento. Eppure è l'unica verifica della pagina pubblicata come pura asserzione in prosa, mentre l'invarianza del numeratore (§2.4) e l'accordo col motore (§11) ricevono entrambe un esito booleano ancorato. Il contrasto è vistoso proprio perché §2.4 spiega bene perché non ci si accontenta di «due numeri uguali accostati».

---

### Cosa non ho potuto valutare

- **La correttezza di ogni valore rispetto ai dati.** Non ho visto `reports/kpi_measures.json`, `kpi_engine_check.json`, `bq3_scenarios.json` né i dati in `data/processed/`. Tutto ciò che ho verificato è **coerenza interna alla pagina**: che i valori pubblicati siano fra loro compatibili, non che siano quelli giusti. Un errore coerentemente propagato dallo script sarebbe passato indenne da questa revisione — come del resto la §11.2 e la §12 dichiarano entrambe con precisione.
- **Se le ancore si risolvano.** Ho letto i commenti `<!--@…-->` come testo. Che ogni chiave esista nell'artefatto e vi corrisponda è ciò che `check_audit_coherence.py` verifica, e io non l'ho eseguito.
- **La grammatica di marcatura.** Non ho letto `convenzioni-marcatura.md`. I rilievi R5 e R6 poggiano **sulla descrizione che il documento dà di sé stesso** in §1 e §12 («ogni quantità priva di ancora o di marcatore di non-misurato è un errore»); se la grammatica reale prevede un'esclusione strutturale per i valori dentro backtick, R5 va riformulato come un problema di onestà verso il lettore anziché come una violazione di regola — ma non decade, perché il lettore vede comunque un numero osservato senza provenienza.
- **La fedeltà ai documenti a monte.** Non posso verificare le citazioni virgolettate di `C1` e `C3`, i riferimenti a `kpi_operators.md` §2.1/§3/§4/§5/§6/§7/§12, a `data_model.md` §4/§8/§10.2/§11/§12/§13/§14/§15, a `content_taxonomy_bridge.md` §5/§7, né che le decisioni `D1`–`D11` dicano ciò che qui viene attribuito loro. In particolare **non posso verificare se il terzo vincolo aperto di §12 esista davvero** (R12): so solo che questa pagina lo annuncia e non lo tratta.
- **La correttezza sintattica e semantica del DAX contro il modello reale.** Ho letto le dieci formule come codice e le trovo plausibili e coerenti con la prosa che le accompagna (uso di `DIVIDE`, comparatori stretti dove le soglie sono dichiarate strette, `Skip` in `RANKX` coerente con la regola dei pari merito). Non ho il `.pbix` e non posso dire se le relazioni che `RELATED` presuppone esistano.
- **Se il difetto di tipizzazione sia stato effettivamente corretto**, e se la correzione copra anche le colonne che R4 mette in questione.
- **La riga di intestazione «revisionato in contesto pulito», con link a `specs/007b-kpi-measures/review.md`.** La segnalo senza classificarla come rilievo: al momento in cui leggo, quel verbale è questo, e non esisteva. È un'affermazione che diventerà vera; chi la committa dovrebbe assicurarsi che non arrivi su `main` prima del file che cita.
