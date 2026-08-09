# Revisione in contesto pulito — `docs/data_audit.md`

**Data**: 2026-08-08
**Oggetto**: `docs/data_audit.md` (239 righe), con l'artefatto `reports/data_profile.json` a cui rimanda.
**Natura della revisione**: condotta senza contesto pregresso.

**Cosa ho letto**: `docs/data_audit.md`, integralmente e una volta sola prima di formulare qualunque giudizio; `reports/data_profile.json`, aperto soltanto dopo la Prova 1 e soltanto per verificare la tracciabilità dei valori. Ho eseguito `python3 scripts/check_audit_coherence.py` e ho scritto verifiche indipendenti sul JSON.

**Cosa non ho letto**: nessun file sotto `specs/` — né la spec, né il piano, né i task, né la revisione della feature 001; `CLAUDE.md`, `README.md`, la constitution, `docs/roadmap.md`, `docs/business_case.md`. Nessun comando `git`: né log, né diff, né messaggi di commit. Non ho letto il sorgente di `scripts/profile_data.py` né quello di `scripts/check_audit_coherence.py`: del secondo ho usato solo l'output.

## Esito complessivo

Il documento supera la Prova 1 e regge la Prova 2 **là dove il suo meccanismo di tracciabilità arriva**: tutte e 106 le ancore presenti nel testo puntano a un identificativo esistente nel profilo e riportano esattamente il valore di visualizzazione registrato lì; nessuna eccezione, nessuna approssimazione tacita. Le verifiche aritmetiche indipendenti che ho potuto condurre sul solo artefatto tornano tutte.

Il problema è che il meccanismo **non arriva dappertutto, e il documento afferma il contrario**. §1 dichiara che «ogni numero di questo documento è prodotto da `scripts/profile_data.py`» e che «ogni valore ripreso dal profilo porta con sé un riferimento invisibile all'identificativo che lo contiene». Non è vero per i numeri scritti in lettere, che l'ancoraggio non copre e che il verificatore non vede nemmeno come avvisi. In quella zona d'ombra ho trovato **tre affermazioni errate**, di cui due contraddette dal documento stesso: che `cast` sia «il secondo campo più incompleto del catalogo» (è il terzo, e la tabella che lo precede di due righe lo dimostra); che su quattordici affermazioni verificate «dodici coincidono» (l'artefatto ne registra tredici concordi e una sola divergente, e il documento stesso qualifica la seconda come «non divergente»); che 18 valori invece di 14 suggeriscano «un dominio quattro volte più ricco» (sono quattro valori in più, un dominio 1,3 volte più ricco). Non è casuale che tutti e tre gli errori si annidino esattamente dove il controllo automatico non guarda: è la dimostrazione empirica che la garanzia dichiarata è più stretta di come è enunciata.

Sulla Prova 3 il perimetro tiene su quasi tutta la lunghezza — le sezioni «Inferenze da evitare» di §8 sono la parte migliore del documento, e sono scritte contro l'interesse di chi le scrive — ma cede in un punto sostanziale: §2.4 non si limita a contare le categorie musicali, emette un verdetto («la **confidenza alta regge**», «La North Star sopravvive al rilievo») su una misura del framework, in un documento che si apre dichiarando «Descrive, non corregge e non giudica». A questo si aggiunge una inclinazione di tono diffusa ma minore.

Il giudizio è quindi: **documento solido nell'impianto, con un difetto di copertura del meccanismo che ha già prodotto errori reali, e una crepa di perimetro localizzata**. Non è pronto a essere considerato chiuso così com'è.

---

## Prova 1 — Comprensione

**Metodo.** Una sola lettura integrale, dall'inizio alla fine, senza tornare indietro. Le risposte che seguono sono state formulate senza riaprire il documento e non sono state corrette a posteriori.

### Che cosa contengono i due dataset e a cosa servono

Un **catalogo video** (8.807 titoli, 12 campi: identificativo, tipo film/serie, titolo, regista, cast, paese, data di aggiunta, anno di uscita, classificazione per età, durata, categorie, descrizione) e un **catalogo musicale** (114.000 righe, 21 campi: identificativo di traccia, artisti, album, titolo, popolarità, durata, genere e un insieme di *audio feature* fra cui `energy`, `valence`, `danceability`). Entrambi sono cataloghi pubblici reali usati come **proxy**: il primo del catalogo attuale di StreamWave, il secondo del mercato musicale accessibile. Servono da base fattuale per il framework di misure del progetto, e il documento verifica campo per campo quali misure quei dati possono alimentare e quali no.

Risposta ottenuta senza domande di chiarimento.

### Tre caratteristiche dichiarate vincolanti, e cosa vincolano

1. **Il campo delle categorie video è multi-valore** (42 categorie, 19.323 assegnazioni su 8.807 titoli, 2,19 per titolo). Vincola: i conteggi per categoria **non sono sommabili** e non vanno accostati a un totale di catalogo senza dichiararlo.
2. **La riga del catalogo musicale non è la traccia** (114.000 righe, 89.741 identificativi distinti). Vincola: esistono due granularità non intercambiabili — coppia traccia-genere e traccia deduplicata — e **ogni misura deve dichiarare in quale opera**; i totali di catalogo vanno sulla seconda.
3. **Il campione musicale è bilanciato per costruzione** (1.000 righe esatte per ciascuno dei 114 generi). Vincola: **nessun dimensionamento di segmento può poggiare sul conteggio di righe**, che restituirebbe lo stesso numero per ogni genere; serve una variabile che vari.

Ne ho ricavate senza sforzo anche altre due: il formato misto della durata video (minuti per i film, stagioni per le serie, non convertibili), e l'esistenza di una sola categoria video a contenuto musicale.

### Due cose che il documento dichiara esplicitamente di non rispondere

- **Come i dati vadano puliti, deduplicati o trasformati** — rimandato alla feature 003.
- **Se le righe a popolarità zero vadano incluse, escluse o riportate a parte** — le conta e le localizza, la decisione è della feature 003.

(Ne dichiara altre due: non risponde a nessuna delle tre domande di business e non contiene KPI — in particolare non calcola il rapporto della North Star; e non dice se i dati siano idonei allo scopo.)

### Riesce a spiegare perché esiste?

Sì, e in modo puntuale: il paragrafo «Perché questo documento esiste» di §1 lo attribuisce al rilievo R8 della revisione della feature precedente — fatti sui dati che esistevano soltanto come prosa, senza uno script che li rigenerasse, con il principio II insoddisfatto per quei valori. È una delle cose meglio riuscite: la ragion d'essere è dichiarata al primo schermo, non desunta.

### Esito: **superata**

### Punti rimasti oscuri alla prima lettura

Li registro perché sono la parte più utile di questa prova.

- **Il «riferimento invisibile» di §1.** Alla prima lettura non ho capito *dove* fosse: nel Markdown reso non si vede nulla, e il documento non dice che si tratta di commenti HTML leggibili solo nel sorgente. Un lettore che apre il documento su GitHub vede numeri nudi e una promessa di tracciabilità che non può ispezionare senza cliccare «Raw». La promessa è mantenuta, ma il documento non spiega come constatarlo.
- **Quali siano i due dataset.** Il documento parla per tutta la sua lunghezza di «catalogo video» e «catalogo musicale» e non li nomina mai. Il profilo li identifica (nome file, dimensione, `sha256`); il documento no, e non rimanda a quel blocco. Chi legge questo documento da solo non sa quali dati abbia davanti.
- **§2.2, «il terzo dei tre è il secondo campo più incompleto».** Ho dovuto rileggere la frase due volte per capire a quale dei tre campi si riferisse, e alla verifica si è rivelata falsa (R1).
- **§6, «quattordici affermazioni verificate, dodici coincidono».** Alla prima lettura mi sono chiesto dove fossero elencate le dodici concordi. Non sono nel documento. Alla verifica il conto si è rivelato sbagliato (R2).
- **§3.5, la tabella delle quote a zero.** La prosa dice quattro generi sopra il 60%, la tabella ne mostra cinque, l'ultimo sotto soglia. La tabella non ha didascalia e non dichiara il criterio con cui è stata tagliata (R7).
- **§2.5, «quei tre campi sono valorizzati al 100%».** Non ho capito quali fossero i «tre campi»: il campo è uno solo (R6).

---

## Prova 2 — Verificabilità dei numeri

**Metodo.** Ho estratto dal sorgente Markdown tutte le occorrenze del pattern `numero<!--@ID-->`, ne ho risolto ciascun `ID` nella mappa `values` del profilo e ho confrontato il testo scritto con il campo `display` registrato. Sono **106 ancore, 88 identificativi distinti**. Ho poi cercato i numeri **privi** di ancora e ho verificato a mano quelli sostanziali. Infine ho ricalcolato in modo indipendente le identità aritmetiche interne al documento. Il controllo automatico l'ho eseguito, ma non gli ho creduto sulla parola: ho riscritto il confronto per conto mio.

### Tabella dei valori verificati

| # | Dove | Sede | Valore scritto | Identificativo | Nel profilo | Esito |
|---|---|---|---|---|---|---|
| 1 | §2.1 | prosa | 8.807 titoli | `NF.shape.rows` | 8.807 | coincide |
| 2 | §2.2 | tabella | 29,91% mancanti `director` | `NF.miss.director.pct` | 29,91% | coincide |
| 3 | §2.2 | tabella | 825 mancanti `cast` | `NF.miss.cast.count` | 825 | coincide |
| 4 | §2.3 | prosa | 19.323 assegnazioni | `NF.cat.assignments` | 19.323 | coincide |
| 5 | §2.4 | prosa | 375 titoli `Music & Musicals` | `NF.cat.music_musicals.titles` | 375 | coincide |
| 6 | §2.6 | tabella | 114,0 terzo quartile film | `NF.num.movie_duration_min.q3` | 114,0 | coincide |
| 7 | §2.6 | tabella | 17,0 massimo stagioni | `NF.num.tvshow_seasons.max` | 17,0 | coincide |
| 8 | §3.3 | prosa | 89.741 identificativi distinti | `SP.id.distinct` | 89.741 | coincide |
| 9 | §3.3 | tabella | 27,03% inflazione | `SP.id.inflation` | 27,03% (27.0322) | coincide |
| 10 | §3.5 | tabella | 33,2 media popolarità | `SP.num.popularity.mean` | 33,2 | coincide |
| 11 | §3.5 | tabella | 68,10% zero in `jazz` | `SP.pop.zero.by_genre.jazz` | 68,10% (68.1) | coincide |
| 12 | §3.6 | prosa | 212,9 secondi mediani | `SP.duration.median_s` | 212,9 | coincide |
| 13 | §4 | prosa | 5,26% dei generi | `X.genre_lexical.share` | 5,26% (5.2632) | coincide |
| 14 | §6 D1 | prosa | 17 valori rigenerati | `NF.card.rating` | 17 | coincide |
| 15 | §2.2 | tabella | 0 mancanti per **sei** campi | `NF.miss.title.count` | 0 | coincide, **ma copre un campo su sei** (R4) |
| 16 | §2.5 | prosa | «66 min, 74 min, 84 min» | *nessuno* | `catalogs.netflix_rating_out_of_domain` | presente nel profilo, **fuori dal meccanismo** (R4) |
| 17 | §2.2 | prosa | «il secondo campo più incompleto» | *nessuno* | contraddetto dalla tabella | **errato** (R1) |
| 18 | §6 | prosa | «quattordici … dodici coincidono» | *nessuno* | 14 verificate, **13** concordi | **errato** (R2) |
| 19 | §6 D1 | prosa | «quattro volte più ricco» | *nessuno* | 18 vs 14 → 1,3 volte | **errato** (R5) |
| 20 | §4 | prosa | «Tre delle sei corrispondenze» | *nessuno* | nessuna chiave, nessun criterio | **non tracciabile** (R8) |
| 21 | §8 | prosa | «fermo al 2022» | *nessuno* | assente per costruzione | **non tracciabile e dichiarato tale** — corretto |

### Verifiche aritmetiche indipendenti

Tutte tornano, ricalcolate sul solo artefatto:

- 6.131 + 2.676 = 8.807 (§2.1);
- somma dei titoli distinti delle **42** categorie nel profilo = **19.323**, esattamente le assegnazioni di §2.3; 19.323 / 8.807 = 2,194 → 2,19;
- 6.128 film con durata = 6.131 − 3 mancanti (§2.6 vs §2.2);
- 114.000 − 89.741 = 24.259; 24.259 / 114.000 = 21,28%; 24.259 / 89.741 = 27,03% (§3.3): le due letture sono entrambe corrette e correttamente distinte;
- 16.020 / 114.000 = 14,05% (§3.5);
- 6 / 114 = 5,26% (§4);
- le percentuali di completezza di §2.2 coincidono tutte con i conteggi divisi per 8.807.

### Il meccanismo funziona, e dove non funziona

Il pregio è reale e va detto con precisione: `reports/data_profile.json` è versionato, contiene 1.025 valori con `label`, `unit`, `granularity`, `dataset` e `field` per ciascuno, e registra in `sources` nome, dimensione e `sha256` dei due file di origine. **Ho potuto verificare ogni valore ancorato senza possedere i dati grezzi**, che è esattamente ciò che §1 promette. Le convenzioni che rendono riproducibili i valori derivati — `conventions.music_terms`, `conventions.lexical_rule`, `conventions.missing`, `conventions.rating_domain` — sono nel profilo e sono citate nel testo. Questa parte è fatta bene e non è frequente vederla fatta.

Il limite è la **copertura**. `check_audit_coherence.py` restituisce «documento e profilo coerenti» e segnala dieci gruppi di cifre non marcati (`66`, `74`, `84`, `100`, `60`, `6`, `18`, `18`, `2022`, `100`). Nessuno di questi dieci è un errore. Ma il verificatore **non vede i numeri scritti in lettere**, e i tre errori che ho trovato — R1, R2, R5 — sono tutti e tre scritti in lettere o come confronto verbale. L'esito verde del comando è quindi vero e insieme fuorviante: certifica le ancore, non il documento.

### Esito: **superata con riserva sostanziale**

Ogni numero ancorato è tracciabile e coincide. La frase di §1 «ogni numero di questo documento è prodotto da `scripts/profile_data.py`» è **falsa come enunciata**, e la sua falsità non è teorica: ha lasciato passare tre affermazioni errate.

---

## Prova 3 — Tenuta del perimetro

**Metodo.** Ho riletto il documento cercando attivamente: verbi e aggettivi valutativi; numeri che siano esiti di analisi anziché descrizioni del dato; conclusioni sulla decisione strategica, anche solo suggerite; asimmetrie di enfasi.

### Una violazione sostanziale

**§2.4, i tre capoversi finali.** Il documento conta le categorie a contenuto musicale — questa è descrizione — ma poi scrive:

> «**La conseguenza**: `BQ1-K1` non compie alcuna selezione fra categorie. Non c'è mappatura, non c'è strato interpretativo, e la **confidenza alta regge**. La North Star sopravvive al rilievo.»

Questo non è descrivere un dato: è **pronunciarsi sul livello di confidenza di una misura del framework**, cioè su un attributo di un artefatto che il documento dichiara di non contenere («Non contiene KPI», §8). L'apertura di §2.4 lo anticipa nello stesso registro: «non è una curiosità: da essa dipende la confidenza della North Star del progetto», e l'ipotesi contraria è formulata come un rischio scampato («`BQ1-K1` **non potrebbe più reggere** la confidenza alta»). «Regge» e «sopravvive» sono verdetti, e il secondo è anche una figura retorica di sollievo.

La constatazione ammissibile qui è: *le categorie che soddisfano il criterio dichiarato sono una sola.* Che cosa ne consegua per la confidenza di `BQ1-K1` è una valutazione della misura, e appartiene a chi possiede la misura.

Aggiungo un rilievo di forma su questa stessa sezione: §8 dichiara che «il rapporto fra i titoli musicali e il totale del catalogo, che è la formula della North Star, non compare né in questo documento né nel profilo. Il numeratore e il denominatore ci sono entrambi». È letteralmente vero, e il perimetro formale tiene. Ma il documento pubblica 375 e 8.807 a poche righe di distanza e chiama esplicitamente la prima «la conseguenza» per la North Star: la misura è a una divisione di distanza, e il lettore è stato accompagnato fin lì. Non lo chiamo violazione — lo segnalo come punto su cui decidere (Divergenza 4).

### Violazioni marginali: inclinazioni di tono

Nessuna di queste, da sola, sposta il giudizio del lettore sulla decisione strategica. Le riporto perché insieme fanno una voce, e la voce di un documento che «descrive e non giudica» dovrebbe essere più piatta di questa.

- §3.3: «È il **ritrovamento con le conseguenze più estese sull'intero progetto**.» Graduatoria di importanza, non constatazione. Che le conseguenze siano estese lo dimostrano i fatti che seguono; dirlo prima orienta.
- §2.5: titolo «**Un campo valorizzato e sbagliato**»; «È un **evidente** scivolamento di campo nella fonte»; «Il caso **merita attenzione oltre la sua dimensione**». Il fatto è inattaccabile — una durata nel campo della classificazione per età è fuori dal dominio dichiarato — ma «evidente» e «merita attenzione» sono dell'autore, non del dato.
- §3.1: «perché un campo che nessuno ha guardato è un campo che qualcuno userà per sbaglio». Aforisma. Motiva una scelta di profilazione con una massima, non con un fatto.
- §6: «lasciare un numero sbagliato in un documento già mergiato è **peggio** che modificarlo». Giudizio normativo su una prassi di lavoro, estraneo a un documento di profilazione.
- §8: «Qualunque dimensionamento costruito sui conteggi è **sbagliato prima di essere calcolato**.» Il contenuto è corretto e importante; la formulazione è retorica.
- §2.7: «il catalogo è **fortemente** concentrato sull'ultimo decennio». L'intensificatore non è nel dato: mediana 2017 e primo quartile 2013 sono il dato.
- §5: «con la **fragilità** di §3.5» (riga di `BQ2-K1`). In una tabella che la sua stessa intestazione dichiara «una constatazione sui campi, non un giudizio sulla misura», «fragilità» è un giudizio sulla misura.
- §2.1: «**nessun titolo è duplicato**, a differenza di quanto accade sul lato musicale». Il confronto anticipa §3.3 e presenta il primo catalogo come il caso in ordine e il secondo come il caso problematico, prima che il lettore abbia i numeri per giudicare.

### Un'asimmetria di presentazione

**§3.5** pubblica primo quartile, mediana, media, terzo quartile e massimo dell'indice di popolarità, e **omette il minimo** — che il profilo contiene (`SP.num.popularity.min` = 0,0). In una sezione intitolata «L'indice di popolarità **e la sua massa di zeri**», il minimo è il valore che àncora l'intero discorso. L'omissione non favorisce nessuna tesi, ma è l'unico punto in cui una tabella di distribuzione è incompleta rispetto al profilo, e capita proprio dove il tema è il valore mancante dalla tabella.

### Ciò che invece tiene, e va detto

- §8 «Inferenze da evitare» è la sezione migliore: tre inferenze scorrette sono nominate, spiegate e proibite, e tutte e tre andrebbero contro l'interesse di chi vuole far quadrare una tesi. «Descrivere un dataset non è approvarlo» è la frase giusta al posto giusto.
- §7 distingue la confidenza *sul dataset* dalla trasferibilità a StreamWave, e tiene A1 fuori dalla scala dichiarando perché. Non c'è nessun punto in cui il documento fa passare un fatto sui due cataloghi pubblici per un fatto su StreamWave.
- §3.4 e §8 dicono, due volte e senza attenuazioni, che la distribuzione dei generi è un artefatto del campionamento. È il fatto che più facilmente produrrebbe una conclusione strategica sbagliata, ed è disinnescato.
- §5 dichiara «assente» due misure su otto senza cercare surrogati, e §4 usa un proprio risultato per **non** riabilitare un piano di confronto già scartato («questo numero lo documenta, non lo riabilita»). Sono due punti in cui il documento lavora contro la comodità di chi lo scrive.

### Esito: **una violazione sostanziale (§2.4), otto marginali di tono, una asimmetria di presentazione**

---

## Rilievi

In ordine di gravità decrescente.

### R1 — §2.2: `cast` non è «il secondo campo più incompleto» — **errato**

**Dove**: §2.2, ultima frase: «`show_id`, `title` e `cast` non vi comparivano, e il terzo dei tre è **il secondo campo più incompleto del catalogo dopo il regista**».

**Cosa non va**: è falso. La tabella che precede questa frase di due righe elenca `country` con 831 valori mancanti (9,44%) e `cast` con 825 (9,37%). `cast` è il **terzo** campo più incompleto, dopo `director` e `country`.

**Perché conta**: non è un errore di stima, è un errore contraddetto dai numeri stampati nella stessa sezione, tre righe sopra. Un lettore attento lo trova in dieci secondi, e da lì in avanti legge ogni altra affermazione derivata del documento con sospetto — comprese quelle corrette. In un documento la cui intera ragion d'essere è chiudere il rilievo «fatti che esistono soltanto come prosa», un fatto che esiste soltanto come prosa **ed è sbagliato** colpisce la tesi al centro. Va corretto in «il terzo campo più incompleto» oppure riscritto senza graduatoria.

### R2 — §6: «dodici coincidono» è errato e si contraddice con D2 — **errato**

**Dove**: §6, primo capoverso: «Su quattordici affermazioni verificate, **dodici coincidono**. **Le due che non coincidono** sono registrate qui».

**Cosa non va**: il profilo registra 14 elementi in `divergences`. Di questi, **uno solo** ha `status: "diverge"` e una lista di scarti non vuota (V04, i «18 valori»). Il secondo citato, V13, ha `status: "ambiguo"` e **lista di scarti vuota**: coincide, o meglio non è confrontabile. Le affermazioni che coincidono sono **tredici**, non dodici. E il documento lo sa, perché duecento parole più sotto scrive di D2: «**Stato: ambiguo, non divergente**». La frase d'apertura di §6 contraddice quindi sia l'artefatto sia il proprio paragrafo D2.

**Perché conta**: è il conteggio con cui il documento certifica la propria opera di verifica sulla feature precedente. Se il numero che riassume la verifica è sbagliato, la verifica perde credito indipendentemente dal fatto che nel merito sia stata fatta bene — e nel merito lo è stata. Il conteggio corretto va scelto e reso coerente con D2: «quattordici affermazioni verificate, tredici coincidono; una diverge e una è ambigua» descrive esattamente ciò che il profilo contiene.

### R3 — §2.4: verdetto sulla confidenza della North Star — **perimetro, sostanziale**

**Dove**: §2.4, «**La conseguenza**: … la **confidenza alta regge**. La North Star sopravvive al rilievo», e in apertura «da essa dipende la confidenza della North Star del progetto».

**Cosa non va**: il documento si apre dichiarando «Descrive, non corregge e non giudica. Non contiene KPI» e §8 lo ripete. Stabilire che la confidenza di `BQ1-K1` resta alta è un giudizio su una misura, non una descrizione di un dato. Il fatto osservabile è che le categorie che soddisfano il criterio dichiarato sono una sola; tutto ciò che segue è inferenza sul framework.

**Perché conta**: è l'unico punto in cui il documento fa ciò che ha promesso di non fare, e lo fa in favore della tesi del progetto — la misura di punta ne esce confermata. Un lettore che dovesse contestare la North Star troverebbe qui la sua conferma già scritta dentro un documento che si presenta come neutrale, e non avrebbe modo di distinguere il fatto dalla valutazione perché sono nello stesso capoverso. Se il verdetto va dato, va dato altrove e da chi possiede la misura; qui basta il conteggio e il rimando.

### R4 — §1: la garanzia di tracciabilità è enunciata più larga di quanto sia — **errato nell'enunciato**

**Dove**: §1, «**Ogni numero** di questo documento è prodotto da `scripts/profile_data.py` e vive in `reports/data_profile.json`» e «**Ogni valore** ripreso dal profilo porta con sé un riferimento invisibile all'identificativo che lo contiene».

**Cosa non va**: il meccanismo copre 106 occorrenze, e sono tutte corrette. Non copre:

1. **i numeri scritti in lettere** — «quattordici», «dodici», «nove», «Tre delle sei», «quattro volte»: né ancorati, né segnalati come avvisi dal verificatore, che ragiona su gruppi di cifre;
2. **i valori letterali che vivono fuori da `values`** — le tre durate `66 min`, `74 min`, `84 min` (§2.5) stanno in `catalogs.netflix_rating_out_of_domain`, i sei nomi di genere di §4 in `catalogs.genre_lexical_matches`, i sette termini di §2.4 in `conventions.music_terms`. Sono nel profilo, ma nessuno di essi porta un'ancora e nessuno viene confrontato: se cambiassero, il documento resterebbe «coerente»;
3. **le celle che aggregano più campi** — l'ultima riga della tabella di §2.2 dichiara zero valori mancanti per sei campi (`show_id`, `type`, `title`, `release_year`, `listed_in`, `description`) e porta **una sola ancora**, `NF.miss.title.count`. Il profilo contiene tutti e sei i valori (`NF.miss.show_id.*`, `NF.miss.type.*`, …): cinque su sei semplicemente non vengono verificati.

**Perché conta**: R1, R2 e R5 stanno tutti e tre dentro la categoria 1. Non è un limite ipotetico: è il limite attraverso cui gli errori sono effettivamente passati, mentre `check_audit_coherence.py` stampava «documento e profilo coerenti». Finché l'enunciato di §1 resta assoluto, un lettore — e la sessione che erediterà questo documento — attribuirà all'esito verde una garanzia che non ha. Delle due l'una: si restringe l'enunciato dichiarando che cosa il controllo copre e che cosa no, o si estende la copertura (vietando i numeri in lettere per i fatti misurati, ancorando i valori letterali, spezzando le celle aggregate).

### R5 — §6 D1: «un dominio quattro volte più ricco» — **errato**

**Dove**: §6, D1, ultima frase: «Descrivere il campo come avente 18 valori suggerisce un dominio **quattro volte più ricco** di quanto sia.»

**Cosa non va**: i valori dichiarati sono 18, quelli effettivamente nel dominio 14. Sono **quattro valori in più**, cioè un dominio 1,29 volte più ricco. «Quattro volte più ricco» significherebbe 56 valori contro 14.

**Perché conta**: la gravità sta nel luogo. D1 è il paragrafo in cui il documento corregge un numero impreciso della feature precedente e spiega, con ragione, che «uno dei due è sbagliato come descrizione di un dominio». Chiuderlo con un rapporto sbagliato di un fattore tre indebolisce la correzione stessa. Basta «quattro valori più ricco», e la frase dice quello che voleva dire.

### R6 — §2.5: «quei tre campi sono valorizzati al 100%» — **errato (e confonde la distinzione che il paragrafo esiste per fare)**

**Dove**: §2.5: «**quei tre campi** sono **valorizzati al 100%** e contengono un dato sbagliato».

**Cosa non va**: il campo è **uno** — la classificazione per età — e i record interessati sono **tre righe**. Un insieme di tre righe non è «valorizzato al 100%»: è valorizzato, e basta. Il campo nel suo complesso, del resto, ha 4 valori mancanti (§2.2), quindi non è valorizzato al 100% nemmeno lui.

**Perché conta**: il capoverso esiste per stabilire che «completezza non è correttezza», ed è un punto giusto e utile che §8 riprende come inferenza da evitare. Enunciarlo con un soggetto sbagliato («tre campi» per «tre righe di un campo») e una percentuale che non si applica a quel soggetto rende contestabile l'esempio migliore del documento. Formulazione corretta: *quei tre valori non sono mancanti — sono presenti e fuori dominio; nessuna misura di completezza li segnala.*

### R7 — §3.5: la tabella delle quote a zero è tagliata senza regola dichiarata — **ambiguo**

**Dove**: §3.5, prosa «i generi con oltre il 60% di righe a zero sono **4**» seguita da una tabella di **cinque** righe, la quinta delle quali (`latin`, 58,80%) è sotto la soglia appena enunciata.

**Cosa non va**: la tabella non ha didascalia e non dichiara il criterio di selezione. Non è «i generi sopra il 60%», perché ne contiene uno sotto. Se è «i cinque generi con la quota più alta», va detto — e va detto anche che il sesto, `country` con il **58,70%**, resta fuori per **un decimo di punto**.

**Perché conta**: due sezioni prima, §2.4 e §4 fanno esattamente la cosa giusta — dichiarano `conventions.music_terms` e `conventions.lexical_rule` e spiegano che «il valore **non esiste senza la sua regola**». Qui la regola non c'è, in una tabella che è di fatto una classifica dei generi peggio serviti dall'indice di popolarità, cioè materiale che la feature 003 userà per decidere. Un lettore non può sapere se `country` sia stato omesso per una soglia, per un limite di righe o per una svista.

### R8 — §4: «Tre delle sei corrispondenze» non è tracciabile né motivato — **ambiguo**

**Dove**: §4: «**Tre delle sei** corrispondenze sono peraltro coincidenze di lingua o di pubblico di destinazione, non di contenuto.»

**Cosa non va**: nessuna ancora, nessuna chiave nel profilo (`X.genre_lexical.*` contiene solo `count` e `share`), nessun criterio dichiarato e nessuna indicazione di **quali** tre. Il lettore può tentare di indovinarle dai sei nomi pubblicati — `british`, `spanish`, `kids` sono i candidati ovvi — ma sta indovinando.

**Perché conta**: la frase precedente ha appena stabilito che un valore lessicale «non esiste senza la sua regola». Questa, che è una classificazione interpretativa delle sei corrispondenze in due tipi, arriva senza regola e senza fonte. È il caso di scuola del principio «nessun numero senza fonte» violato subito dopo essere stato applicato bene.

### R9 — §3.5: la tabella di distribuzione omette il minimo — **assente, dentro perimetro**

**Dove**: §3.5, tabella: primo quartile, mediana, media, terzo quartile, massimo.

**Cosa non va**: manca il minimo, che il profilo contiene (`SP.num.popularity.min` = 0,0). È l'unica tabella di distribuzione del documento incompleta rispetto all'artefatto: §2.6 pubblica regolarmente il minimo per entrambe le colonne.

**Perché conta**: il minimo è 0, ed è il valore su cui l'intera sezione è costruita — «e la sua massa di zeri». Pubblicarlo costa una riga e collega la distribuzione ai 16.020 zeri del capoverso successivo. Ometterlo non nasconde nulla, ma lascia il lettore a inferire da sé che la distribuzione tocca lo zero, in un documento che altrove non fa inferire niente.

### R10 — Inclinazioni di tono diffuse — **perimetro, marginale**

**Dove**: §3.3 «il ritrovamento con le conseguenze più estese sull'intero progetto»; §2.5 «evidente scivolamento», «merita attenzione oltre la sua dimensione»; §3.1 «un campo che nessuno ha guardato è un campo che qualcuno userà per sbaglio»; §6 «è peggio che modificarlo»; §8 «sbagliato prima di essere calcolato»; §2.7 «fortemente concentrato»; §5 «con la fragilità di §3.5»; §2.1 «a differenza di quanto accade sul lato musicale».

**Cosa non va**: sono valutazioni, graduatorie e massime in un documento che dichiara di constatare. Nessuna è falsa; nessuna è un dato.

**Perché conta**: preso singolarmente ogni caso è trascurabile e alcuni rendono il testo più leggibile. Presi insieme costruiscono un narratore che ha opinioni, e il documento ne ha dichiarato l'assenza al primo rigo. Il costo è concreto in un solo punto — «fragilità» dentro una tabella la cui intestazione promette «una constatazione sui campi, non un giudizio sulla misura» — e altrove è solo un debito di registro.

### R11 — I due dataset non sono mai nominati — **assente, probabilmente dentro perimetro**

**Dove**: tutto il documento; §1 li chiama «un **catalogo video**» e «un **catalogo musicale**».

**Cosa non va**: nome, provenienza e versione dei due file compaiono solo nel profilo (`sources`, con `sha256` e dimensione in byte), e §1 non rimanda a quel blocco. Il documento nomina lo script che rigenera il profilo, ma non da dove vengano i dati che quello script legge.

**Perché conta**: §1 promette che «chi non possiede i dati di origine può comunque verificarlo» — e sul confronto documento↔profilo è vero. Ma chi volesse rifare il profilo da capo, o anche solo sapere su quale versione del catalogo poggiano 8.807 e 114.000, non lo ricava da questo documento. Lo classifico come probabilmente fuori perimetro — l'inquadramento delle fonti può appartenere al business case — ma una riga in §1 che rimandi a `sources` e alle sue impronte costerebbe poco e chiuderebbe la catena.

---

## Divergenze da chiarire nella feature successiva

Non sono difetti: sono punti su cui va presa una decisione, e che questo documento non poteva prendere da solo.

**1. Che cosa deve coprire il vincolo di tracciabilità.** R4 mostra che oggi copre i gruppi di cifre ancorati e nient'altro. Le opzioni sono almeno tre e vanno scelte, non lasciate implicite: (a) vietare i numeri in lettere per qualunque fatto misurato, e ancorare tutto; (b) estendere il verificatore ai numerali scritti e ai valori letterali di `catalogs`/`conventions`; (c) restringere l'enunciato di §1 dichiarando esplicitamente il confine della garanzia. La (c) da sola non impedisce il ripetersi di R1 e R2.

**2. Le affermazioni derivate hanno statuto?** «Il secondo campo più incompleto» (R1), «tre delle sei corrispondenze» (R8), «quattro volte più ricco» (R5) non sono valori del profilo: sono confronti e classificazioni costruiti sui valori. Il progetto non ha una regola per loro, e sono la categoria in cui si concentrano gli errori. Va deciso se debbano diventare valori calcolati nel profilo o se vadano semplicemente proibiti in prosa.

**3. §5 contiene decisioni di modellazione, non solo constatazioni sui campi.** Due righe della tabella vanno oltre il censimento: «Il lato serie **resta fuori** per incompatibilità di unità» è una scelta di perimetro di `BQ1-K2`, e la nota finale «che l'intera terza domanda debba poggiare su **dati simulati** … è la conseguenza del fatto che nessuno dei 12 campi …» presuppone una decisione — simulare — che non è presa qui e non è attribuita a nessuna feature. Va stabilito dove quelle due decisioni sono formalmente prese e questo documento va allineato a rimandarvi.

**4. Numeratore e denominatore pubblicati, rapporto no.** §8 lo dichiara e formalmente il perimetro tiene. Va deciso se pubblicare 375 e 8.807 accanto alla frase «è la conseguenza per la North Star» costituisca, in sostanza, pubblicare la misura. Se sì, o si rimuove l'accostamento o si accetta che la North Star nasca qui e la si dichiari.

**5. Il criterio delle categorie musicali e la sua ampiezza.** §2.4 dice che il criterio «è deliberatamente più largo del necessario: se avesse selezionato più categorie, lo avremmo saputo». È un argomento valido su **questo** catalogo. Va deciso se il criterio venga riverificato quando la fonte cambia, e chi se ne accorge. Collegato: il disallineamento testuale con la descrizione «musical, documentari musicali, concerti, film sulla musica» è registrato e assegnato genericamente a «un momento precedente alla feature 007» — un'assegnazione senza titolare è un debito che nessuno prende.

**6. D2 resta deliberatamente irrisolto.** La scelta di non decidere al posto della feature 001 quale delle due letture aritmetiche intendesse è, a mio giudizio, corretta. Ma la decisione va presa da qualcuno prima che una misura di catalogo venga calcolata, altrimenti si ripropone identica al primo totale non deduplicato. È materia della feature 003 e va messa nero su bianco lì.

**7. La correzione degli artefatti già mergiati.** §6 afferma che «gli artefatti della 001 hanno ricevuto una nota di correzione» e ne dà la motivazione. Dall'interno di questo documento non è verificabile — e non ho letto quei file. Va chiarito se la prassi è modificare in loco o allegare un'errata, e va resa una regola, perché la giustificazione data qui («è peggio lasciare un numero sbagliato») è una scelta di metodo travestita da constatazione.

**8. La soglia e il taglio di §3.5.** Prima che la feature 003 decida che fare delle righe a popolarità zero, va fissato il criterio con cui si seleziona l'insieme dei generi interessati: la soglia del 60% è nel profilo come etichetta di un conteggio, ma il taglio a cinque righe della tabella no (R7), e `country` al 58,70% cadrebbe dentro o fuori a seconda di una decisione che nessuno ha ancora preso.

---

## Nota di verifica della sessione revisionata — 2026-08-09

*Aggiunta in coda dalla sessione che ha scritto il documento revisionato. Il verbale sopra **non è stato modificato**: un revisore indipendente che venisse riscritto da chi ha revisionato smetterebbe di essere indipendente. Questa nota registra l'esito della verifica dei rilievi, incluso quello che non ha retto.*

**Rilievi verificati e confermati**: R1, R3, R4, R5, R6, R7, R8, R9, R10, R11. Tutti corretti nel documento, tranne R3 e R4 che hanno richiesto una decisione oltre la correzione — vedi sotto.

**R2 non regge nel merito, e va comunque corretto nella forma.** Il rilievo sostiene che le affermazioni concordi siano tredici e non dodici. Il blocco `divergences` del profilo contiene esattamente **12 `coincide`, 1 `diverge`, 1 `ambiguo`**: «dodici coincidono» era aritmeticamente corretto. Il revisore ha conteggiato V13 fra le concordi perché ha la lista di scarti vuota, ma quella lista è vuota perché **V13 non ha alcun controllo associato**, non perché sia stata confrontata e abbia coinciso — il verbale stesso esita («coincide, o meglio non è confrontabile»).

Il rilievo resta però utile, e la sua utilità è indipendente dal suo errore: un lettore attento ha misletto quella frase, e il motivo era nella frase. «Le due che **non coincidono**» accostato a «ambiguo, **non divergente**» invitava esattamente alla confusione in cui il revisore è caduto. §6 è stata riscritta enumerando i tre stati separatamente, e i tre conteggi sono ora valori del profilo (`X.claims_001.*`) ancorati nel testo: la stessa affermazione, oggi, sarebbe verificata da un comando.

**R3 e R4 hanno prodotto una decisione, non solo una correzione.**

R3 contesta che §2.4 emetta un verdetto sulla confidenza di `BQ1-K1`. Il revisore non poteva saperlo — non ha letto la spec, come doveva — ma quella dichiarazione era **richiesta da FR-021**: il rilievo R11 della feature 001 andava chiuso in questa feature o in nessuna. La tensione che il verbale segnala è comunque reale e stava nell'inquadramento: il documento si apre dichiarando di non giudicare e poi giudica. §2.4 ora separa esplicitamente il fatto osservato dalla valutazione che ne discende, dichiara perché quest'ultima è lì, e rimanda il giudizio finale a chi possiede la misura.

R4 è il rilievo più utile del verbale ed è stato accolto per intero. Il controllo di coerenza è stato **esteso** invece che l'enunciato ristretto: riconosce ora i numerali scritti in lettere e i letterali di `catalogs`/`conventions`, e segnala fra gli avvisi anche i numerali non marcati. I marcatori del documento sono passati da 106 a 149. §1 dichiara inoltre in modo esplicito che cosa il controllo copre e che cosa no — perché estendere la copertura non elimina il confine, lo sposta.

**Sulla data.** Il verbale porta 2026-08-08 perché il prompt di consegna lo prescriveva; il revisore ha segnalato la discrepanza con la data di sistema e ha seguito il prompt, che è la condotta corretta. L'errore era nel prompt, cioè mio: la data giusta è il **2026-08-09**, ed è stata corretta in tutti gli artefatti della feature. L'intestazione del verbale è lasciata com'era, coerentemente con la scelta di non riscriverlo.
