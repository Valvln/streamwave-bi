# Contratto di pagina: il report che porta l'argomento a schermo

**Feature**: `010a-report-disegno` | **Data**: 2026-08-29 | **Stato**: proposto al punto di fermata 2

Questo documento è il disegno delle dieci pagine del report che **sostituisce** la dashboard a quattro pagine della `008`. È scritto **prima** che Power BI Desktop venga aperto: nel momento in cui viene proposto, il report non esiste.

**Che cosa questo documento è.** Un **vincolo**: dichiara che cosa deve esistere. Non è un accertamento e non descrive alcun file. Il `.pbix` non è versionato, vive sul disco di Valerio, e questa sessione non lo ha aperto per alcuna ragione: nessuna riga di questo contratto afferma che cosa quel file contenga oggi. Ciò che esisterà lo accerterà la `010b`, nella sezione di esito del proprio `quickstart.md`, e **in caso di divergenza quella è la fonte autorevole, non questa**.

**Che cosa questo documento non contiene, deliberatamente.**

- **Nessun valore di KPI trascritto.** I valori si citano per **identificativo di ancora** verso gli artefatti versionati, mai come cifra. Una seconda copia di un valore è una copia che può divergere dall'originale senza che nulla lo segnali, ed è un difetto che questo progetto ha già incontrato. **Una sola cifra compare in tutto il documento**, il fattore `100.000` del §11: non è un fatto misurato ma un'**unità dichiarata** — la stessa categoria delle soglie nella grammatica dei marcatori — e `raccomandazione.md` §4 la marca infatti come non-misurata.
- **Nessun testo a schermo.** La prosa, i limiti in forma divulgativa, il tono sono della `010b`, che ha il proprio contratto di narrazione. La sezione 13 dichiara dove quel testo andrà, perché quella feature non debba ridisegnare le pagine per farvelo entrare.
- **Nessuna misura DAX scritta.** Le sei misure nuove sono **specificate** — nome, contenuto, tabelle di lettura, pagina richiedente — e le scrive la `010b`.

**Da dove viene ciò che questo disegno porta a schermo.** L'argomento è quello di [`docs/raccomandazione.md`](../../../docs/raccomandazione.md), pubblicato dalla `009` e approvato da una revisione in contesto pulito. Questo contratto **non lo riscrive e non lo corregge**: lo impagina. Dove il disegno avesse trovato un difetto in quel documento, sarebbe un ritrovamento da portare alla regia — e non ne ha trovati.

---

## 1. La mappa: quale pagina porta quale parte dell'argomento

**Dieci pagine, pagina iniziale compresa nel conteggio, nessuna pagina finale separata.** La convenzione è dichiarata qui perché la forchetta ammessa — fra 8 e 12 — ammette entrambe, e un conteggio senza convenzione non è verificabile.

| # | Pagina | Che parte dell'argomento porta | Sezione servita di `raccomandazione.md` |
|---|---|---|---|
| 1 | **La domanda** | perché l'analisi esiste, e a quali condizioni si risponderà | «Che cosa è questo documento» |
| 2 | **La risposta** | il verdetto, e la regola di decisione fissata prima dei valori | §1 |
| 3 | **Su che cosa poggia** | i due cataloghi sostitutivi, e che nessun numero è misurato su StreamWave | §1, capoverso sui proxy |
| 4 | **La prima condizione** | la musica non è residuale nel catalogo attuale | §2, «La prima» |
| 5 | **La seconda condizione** | il catalogo musicale ricade nella regione di carattere del video | §2, «La seconda» |
| 6 | **Quanto dovrebbe sbagliare** | il margine di `C2`: una condizione sull'errore, non una stima dell'errore | §2, «Quanto la stima dovrebbe sbagliare» |
| 7 | **La regione di ingresso** | esiste una regione ad alta domanda e alta affinità | §3, «La regione» |
| 8 | **Che cosa la regione contiene** | la graduatoria completa, e l'esclusione dei segmenti a domanda non misurata | §3, «La regione» e «Un'esclusione che va dichiarata» |
| 9 | **Quanto vale** | la terna degli scenari, e il fattore di conversione su una base | §4 |
| 10 | **Che cosa lo ribalterebbe** | le condizioni di ribaltamento, e che cosa non si può concludere | §5 e §6 |

### 1.1 La regola che governa la mappa, e perché è la decisione più importante del disegno

> **Una pagina serve esattamente una sezione; una sezione può ricevere più pagine.** La corrispondenza è **molti-a-uno**, e la direzione non è reversibile.

Dieci pagine su sei sezioni: la corrispondenza uno-a-uno è aritmeticamente impossibile e va risolta in una direzione prima di disegnare, non a metà. Le due direzioni non sono simmetriche:

- **una pagina che serve più sezioni** è un inventario. È esattamente la dashboard a quattro pagine — ciascuna copriva una domanda di business intera, cioè più mosse dell'argomento affastellate — ed è il difetto per cui questa feature esiste;
- **più pagine che servono una sezione** è la forma normale di un argomento lungo: una sezione che cambia mossa al proprio interno chiede due schermate, non due paragrafi sulla stessa.

**Il criterio con cui una sezione si divide, che è il presidio contro la divisione arbitraria**: si divide quando **l'argomento cambia mossa** — dall'affermazione all'obiezione, dalla regione all'esclusione, dalla stima alla sua qualificazione — **non quando la sezione ha troppi numeri per una pagina sola**. La seconda ragione produrrebbe pagine divise per capienza, che è di nuovo un inventario, solo con più fogli.

**Il criterio non è stato applicato a tavolino**: le divisioni cadono su sottosezioni che `raccomandazione.md` marca già per conto proprio. §2 ne ha quattro, §3 ne ha due. I confini sono stati letti, non inventati.

**Una sola pagina serve due sezioni, ed è l'eccezione dichiarata.** La pagina 10 tiene insieme §5 e §6 perché entrambe dicono che cosa l'analisi non stabilisce, e la distinzione fra «lo ribalterebbe» e «non lo si può concludere» è una distinzione di prosa, non di visuale: separarle produrrebbe due pagine di sola prosa consecutive, di cui la seconda senza una mossa propria.

### 1.2 L'ordine è quello della risposta, non quello delle domande

Le pagine **non portano i titoli `BQ1`, `BQ2`, `BQ3`** e non sono ordinate per essi. Ogni KPI compare dove l'argomento lo usa; la sigla resta leggibile nelle etichette di provenienza, non nell'intestazione della pagina.

L'ordine `BQ1`→`BQ2`→`BQ3` è l'ordine in cui le domande sono state **poste**, ed è quello giusto per [`business_case.md`](../../../docs/business_case.md), che le pone. Non è l'ordine in cui si **risponde**: una risposta comincia dalla conclusione e poi la difende, mentre il framework comincia dal posizionamento e arriva all'impatto.

**La conseguenza è visibile e va dichiarata.** `BQ1-K1`, `BQ1-K3` e `BQ2-K3` compaiono tutti e tre sulla pagina 2: **sono** le tre condizioni, e provengono da due domande di business diverse. Nella dashboard vecchia stavano su due pagine distinte, e la loro congiunzione — che è il verdetto — non stava da nessuna parte.

### 1.3 Il report porta sette KPI su otto

`BQ1-K2` (`format_duration_gap`) e la quota di titoli `Movie` che ne dichiara l'asimmetria **non compaiono su alcuna pagina**.

**La ragione**: `BQ1-K2` non è una delle tre condizioni della regola di decisione, e `raccomandazione.md` non lo cita mai. Descrive una distanza di formato fra i due cataloghi — informativo, e fuori dall'argomento che questo report porta. Includerlo richiederebbe una pagina che nessuna sezione serve, cioè una violazione della regola di §1.1.

**È la decisione più contestabile di questo disegno, e non viene nascosta in una nota.** La completezza rispetto al framework era la proprietà organizzatrice della dashboard vecchia, ed è precisamente ciò che la revisione in contesto pulito ha respinto. Chi ritenesse che un report debba portare tutti gli otto KPI sta chiedendo un artefatto diverso da questo, non una correzione di questo.

### 1.4 Le etichette di fonte e confidenza

Ogni valore a schermo porta le due etichette nella forma di `business_case.md` §5.4, su **ogni** pagina e senza eccezioni. La tabella non viene ricopiata qui: è pubblicata là e nel contratto della `008a` §1.1, e una terza copia è una terza cosa che può divergere.

**Una sola etichetta è nuova**, e riguarda il verdetto congiunto della pagina 2:

> `Fonte: Derivato (C1 + C2 + C3) · Confidenza: media`

La confidenza è media e **non è la media delle tre**. È la conseguenza che `raccomandazione.md` §2 argomenta: una congiunzione non è più affidabile del suo termine meno affidabile, e trattare la confidenza come una media lascerebbe che l'affidabilità alta della prima condizione coprisse quella media delle altre due. È anche la ragione per cui la visuale del verdetto porta **una** etichetta e non tre — vedi §4.

---

## 2. La regola che governa ogni pagina

Enunciata qui una volta sola. Le sezioni di pagina la citano, non la ripetono.

> **Regola di invarianza a schermo.** Un valore a schermo deve essere un valore pubblicato da un artefatto versionato, **alla grana a cui quell'artefatto lo pubblica**. Nessuna pagina offre un'interazione che produca un valore a una grana diversa.

Le grane pubblicate restano tre, come nella `008a`, e non ne esiste una quarta:

| Grana | Valori | Che cosa una selezione può legittimamente restringere |
|---|---|---|
| catalogo intero | `BQ1-K1`, `BQ1-K3`, le tre condizioni, il verdetto | **nulla**: il valore è unico e non ha varianti pubblicate |
| segmento | `BQ2-K1`, `BQ2-K2`, `BQ2-K3` | **nulla per via di filtro**: i valori dei segmenti (`SP.genre.count`) sono tutti pubblicati e stanno tutti a schermo insieme. Una selezione può evidenziarne uno, non ricalcolare su un sottoinsieme |
| scenario | `BQ3-K1`, `BQ3-K2` | **nulla**: i tre scenari sono un intervallo e si leggono insieme; ridurre a uno solo è vietato |

### 2.1 Il corollario, che vale su tutte e dieci le pagine

**La selezione incrociata è ammessa; il filtro non lo è.** Selezionare un punto o una riga per evidenziare il corrispondente altrove non cambia alcun valore. Un filtro ricalcola, e ricalcolare è il modo in cui nasce una quarta grana.

Sulle pagine 7 e 8 la distinzione regge per una ragione verificabile e non per convenzione: `segment_entry_priority_quadrant` e `segment_entry_priority_rank` portano `ALL ( dim_segment )` dentro la formula pubblicata ([`kpi_measures.md`](../../../docs/kpi_measures.md) §7.3), quindi soglie e posizioni **non si muovono** quando un segmento viene selezionato.

**Questa proprietà va riverificata a schermo dalla `010b`**, e non è una formalità: la selezione fra le due pagine è sincronizzata (§10), che è una configurazione che la dashboard vecchia non aveva.

### 2.2 Perché la regola sta qui e non dentro le formule

L'issue [`#18`](https://github.com/Valvln/streamwave-bi/issues/18) osserva che `mood_profile_overlap` legge gli estremi degli assi di mood senza un `ALL` sulla categoria: un filtro di categoria video restringerebbe silenziosamente l'inviluppo e produrrebbe un valore diverso da quello pubblicato, senza alcun segnale. La correzione della formula chiuderebbe quel caso; la regola chiude **la classe** di cui quel caso è un membro.

**L'issue resta aperta.** Questo disegno dimostra che il difetto non si manifesta nelle pagine disegnate, non che non esista.

---

## 3. Pagina 1 — La domanda

**Sezione servita**: «Che cosa è questo documento».

**Che parte dell'argomento porta**: perché l'analisi esiste, e a quali condizioni si risponderà. È la pagina che pone la domanda e dichiara il criterio, **prima** che il verdetto compaia.

**Perché è compresa nel conteggio delle pagine.** Porta un pezzo dell'argomento — la domanda e il criterio — e non è un frontespizio. Contarla fuori suggerirebbe che sia decorazione.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| la regola di decisione | **diagramma delle tre condizioni** come struttura, senza esiti: tre elementi e la congiunzione che li lega | il criterio è stato pubblicato **prima** che i valori esistessero, ed è la proprietà più difendibile dell'intera analisi. Mostrarlo come struttura vuota — le condizioni senza il loro esito — è la sola forma che comunica *questo è ciò che avevamo deciso di verificare* invece di *questo è ciò che abbiamo trovato* |
| navigazione | elementi cliccabili verso le nove pagine successive | — |

**Nessun valore compare su questa pagina.** Il diagramma porta i **nomi** delle tre condizioni, non i loro esiti: gli esiti sono della pagina 2, e anticiparli qui trasformerebbe la pagina della domanda in una seconda pagina della risposta.

**Le tre condizioni si nominano con le etichette di `business_case.md` §3**, non con prosa nuova. Riportare il nome di una condizione esistente non è narrazione; spiegare che cosa quella condizione significhi lo è, ed è della `010b`.

### 3.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| qualunque filtro o slicer | non c'è alcun valore da filtrare |
| tooltip che calcolano | un tooltip è una visuale, e una visuale può calcolare a una grana qualunque. Nessun tooltip di questo report espone una misura |
| gli esiti delle tre condizioni | sono della pagina 2. Mostrarli qui distruggerebbe la sola cosa che questa pagina fa |

---

## 4. Pagina 2 — La risposta

**Sezione servita**: §1.

**Che parte dell'argomento porta**: il verdetto, e la regola di decisione che lo determina.

**La forma del dato detta la forma della pagina, e qui la detta in modo stringente.** Le tre condizioni non sono tre misure indipendenti: sono una **congiunzione**, e la regola dice che l'argomento regge solo se valgono tutte e tre.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| il verdetto congiunto | **una visuale di stato a tre elementi**, con il conteggio delle condizioni soddisfatte al centro e le tre condizioni dentro l'esito, non accanto | tre schede affiancate mostrano tre fatti e lasciano la congiunzione all'occhio di chi guarda. Una visuale che porta le tre condizioni **dentro** l'esito mostra la regola, che è ciò che rende il verdetto verificabile invece che asserito |
| la risposta in forma di esito | l'esito booleano del verdetto, letto da misura | è un booleano, e un booleano non ha altra forma che sé stesso |

**Valori a schermo, con l'ancora di ciascuno:**

| Valore | Ancora | Misura che lo porta |
|---|---|---|
| condizioni soddisfatte, su tre | `KPI.verdict.conditions_satisfied` | `M1` (nuova, §11) |
| l'argomento è sostenuto | `KPI.verdict.all_satisfied` | `M1` la compone |
| `C1` soddisfatta | `KPI.BQ1K1.c1.above_median` | `c1_music_above_median` (esiste) |
| `C2` soddisfatta | `KPI.BQ1K3.c2.satisfied` | `M2` (nuova, §11) |
| `C3` soddisfatta | `KPI.BQ2K3.c3_satisfied` | `C3` companion (dichiarata da `CP-1` della `008a`) |

**Una sola etichetta di fonte e confidenza su questa pagina**, quella del verdetto (§1.4). Tre etichette — alta, media, media — inviterebbero esattamente alla lettura che `raccomandazione.md` §2 esiste per impedire: che la confidenza del verdetto sia la media delle tre. Le tre condizioni portano la propria confidenza **dentro** la visuale, subordinata a quella del verdetto.

**Perché non una scheda sola col conteggio.** Nasconderebbe quali condizioni siano soddisfatte e quale sia la più debole, cioè tutto ciò che rende il verdetto discutibile — e un verdetto che non si può discutere non si può nemmeno verificare.

### 4.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| qualunque filtro | i quattro valori sono unici sul catalogo intero e non hanno varianti pubblicate |
| selezione di una condizione che isola le altre | la congiunzione è il valore. Isolare una condizione produrrebbe un verdetto parziale, che è la lettura che questa pagina esiste per impedire |
| drill-through verso la pagina della condizione | ammesso come **navigazione**, non come drill-through che porta un contesto di filtro. La distinzione è quella di §2.1 |

---

## 5. Pagina 3 — Su che cosa poggia

**Sezione servita**: §1, capoverso sui proxy.

**Che parte dell'argomento porta**: che nessun numero del report è una misura fatta su StreamWave. È la collocazione delle assunzioni `A1` e `A6`.

**Questa pagina è di sola prosa**, e la ragione non è di capienza: **le due assunzioni di trasferimento non entrano nella scala di confidenza per costruzione**. Non esiste un numero che le misuri, e la loro assenza dalla scala è precisamente la loro proprietà. Una visuale costruita qui dovrebbe rappresentare qualcosa che nessun valore contiene.

**Perché una pagina intera e non una nota a piè di schermo.** `raccomandazione.md` §6 le tratta in una sezione propria perché **sopravvivano all'estrazione di una frase**: un report da cui si ritaglia una schermata per una slide deve portare quel limite dentro la schermata, non sotto. Una nota ricorrente su dieci pagine si legge come boilerplate e smette di essere letta alla terza.

| Elemento | Che cosa porta | Ragione |
|---|---|---|
| l'articolazione dei due cataloghi | i due cataloghi sostitutivi accanto ai due cataloghi di StreamWave che il progetto **non ha**, come struttura visibile | ciò che questa pagina deve dare all'occhio è **struttura**, non un grafico: la sostituzione è una relazione fra quattro cose, due delle quali assenti, e una relazione si disegna |
| `A1` | i cataloghi sostitutivi rappresentano StreamWave — dichiarata, non verificata | è il limite più importante del report |
| `A6` | il benchmark economico descrive un altro operatore, su un altro mercato | si applica solo ai valori di `BQ3`, e la differenza con `A1` va mantenuta visibile |

**Due valori compaiono, e sono gli unici**: la numerosità dei due cataloghi sostitutivi.

| Valore | Ancora |
|---|---|
| titoli del catalogo video | `CL.NF.titles.rows.after` |
| tracce del catalogo musicale | `KPI.BQ1K2.music_tracks` |

**Perché questi due sì.** Non descrivono StreamWave: descrivono i sostituti, ed è ciò che la pagina afferma. Portano le proprie etichette di fonte e confidenza come qualunque altro valore.

**La differenza fra `A1` e `A6` va resa visibile e non appiattita.** `A1` si applica identica a **tutti** i valori del report; `A6` solo a quelli di `BQ3`. Presentarle come due voci equivalenti di un elenco suggerirebbe che abbiano la stessa portata, e `business_case.md` §6 dichiara che non ce l'hanno.

### 5.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| qualunque interazione | è una pagina di prosa e di struttura. Non c'è nulla da selezionare |
| grafica aggiunta per riempirla | un grafico costruito per riempire una pagina di prosa afferma con la propria geometria ciò che il testo non afferma. Vedi §14 |

---

## 6. Pagina 4 — La prima condizione

**Sezione servita**: §2, «La prima».

**Che parte dell'argomento porta**: nel catalogo video attuale la musica non è una nicchia dimenticata. Sta nella metà più popolata delle categorie.

**La forma del dato.** `C1` confronta un conteggio con la mediana dei conteggi di tutte le categorie video (`CL.NF.category.distinct`). Il valore che decide non è il conteggio da solo: è la sua **posizione** fra gli altri.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| la posizione della categoria musicale | **distribuzione di tutte le categorie video per numero di titoli**, ordinata, con la categoria musicale marcata e la mediana come linea di riferimento | è la sola forma che mostra *perché* la condizione è soddisfatta invece di asserirlo. Una scheda porterebbe il solo conteggio e lascerebbe il lettore senza il metro con cui confrontarlo. La condizione è una posizione, e una posizione si vede |
| `BQ1-K1` 🎯, la North Star | scheda, con le due etichette | è un valore unico sul catalogo intero, privo di dimensione di scomposizione. Una barra avrebbe bisogno di un asse che non esiste |

**Valori a schermo, con l'ancora di ciascuno:**

| Valore | Ancora | Misura |
|---|---|---|
| titoli della categoria musicale | `KPI.BQ1K1.c1.category_count.music_musicals` | `c1_music_above_median` la usa |
| mediana dei conteggi delle categorie video | `KPI.BQ1K1.c1.median_of_42` | linea di riferimento, letta come misura |
| numero di categorie del catalogo video | `CL.NF.category.distinct` | i punti della distribuzione |
| `C1` soddisfatta | `KPI.BQ1K1.c1.above_median` | `c1_music_above_median` (esiste) |
| quota della categoria musicale sul catalogo | `KPI.BQ1K1.share` | `music_adjacent_catalog_share` (esiste) |
| titoli del catalogo video, denominatore | `KPI.BQ1K1.denominator_titles` | — |

**La quota e la condizione stanno sulla stessa pagina e non sono la stessa cosa.** `kpi_measures.md` §2.3 avverte che `C1` **non è calcolabile dalla quota**: sono due letture diverse dello stesso catalogo. La distribuzione le tiene distinte per costruzione — la quota è un rapporto, la condizione è una posizione nell'ordinamento — e la vicinanza non le fonde perché la visuale mostra da dove ciascuna viene.

**La precisazione che `raccomandazione.md` §2 impone**, ed è testo della `010b` ma vincola il disegno: «non residuale» non significa «grande». La distribuzione lo rende visibile senza dirlo — la categoria musicale sta sopra la mediana **e** è una barra piccola in valore assoluto — ed è il caso in cui una visuale fa il lavoro che altrimenti tocca a un capoverso di cautela.

**La linea della mediana è una misura, non una costante digitata.** Un numero digitato in una visuale è un valore la cui unica fonte è che qualcuno l'ha scritto, che è ciò che il principio I vieta. Il valore è ancorato a `KPI.BQ1K1.c1.median_of_42` e va confrontato **una volta** con quell'ancora.

### 6.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| **qualunque filtro di categoria video** | è il caso noto dell'issue `#18`, e qui colpirebbe anche `music_adjacent_catalog_share` e `c1_music_above_median`, che contano titoli per categoria (§2.2) |
| filtro sul tipo di titolo (`Movie` / `TV Show`) | `BQ1-K1` è definito sull'intero catalogo: un filtro produrrebbe un valore che nessun artefatto pubblica |
| filtro di anno | non esiste alcun KPI pubblicato per anno; l'asse temporale è una delle letture prive di significato di `data_model.md` §18 |
| selezione di una categoria nella distribuzione che filtra la scheda | ricalcolerebbe la North Star su una categoria sola. **Ammessa l'evidenziazione**, che non ricalcola |
| drill-down verso i titoli | porta a grana titolo, che non è una delle tre |

---

## 7. Pagina 5 — La seconda condizione

**Sezione servita**: §2, «La seconda».

**Che parte dell'argomento porta**: la gran parte del catalogo musicale ricade nella regione di carattere che il catalogo video occupa già. È il termine **più debole** dell'argomento, e la pagina lo mostra invece di dichiararlo soltanto.

**La forma del dato, che è la ragione della visuale scelta.** La regione video è descritta prendendo su ciascuno dei tre assi l'estremo minimo e massimo: è una **scatola** che contiene la regione reale ma è più grande di essa. Il limite di questa condizione non è nel valore, è nella forma della regione — e una forma si disegna.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| i due cataloghi sui tre assi | **dispersione delle categorie video** su due dei tre assi di mood, con l'inviluppo disegnato come rettangolo | mostra la scatola **e** mostra che la scatola è larga: le categorie occupano una parte del rettangolo, e il vuoto fra i punti e i bordi è il limite dichiarato della condizione, reso visibile senza doverlo affermare |
| la quota di tracce dentro l'inviluppo | scheda accanto alla dispersione, con le etichette | è un valore unico sul catalogo musicale intero. Non è scomponibile per categoria né per segmento |

**Valori a schermo, con l'ancora di ciascuno:**

| Valore | Ancora | Misura |
|---|---|---|
| quota di tracce dentro l'inviluppo | `KPI.BQ1K3.overlap_share` | `mood_profile_overlap` (esiste) |
| tracce dentro l'inviluppo | `KPI.BQ1K3.tracks_inside` | — |
| estremi dell'inviluppo, asse energia | `KPI.BQ1K3.bound.mood_energy.min` / `.max` | bordi del rettangolo, letti come misure |
| estremi dell'inviluppo, asse positività | `KPI.BQ1K3.bound.mood_valence.min` / `.max` | come sopra |
| estremi dell'inviluppo, asse ritmo | `KPI.BQ1K3.bound.mood_danceability.min` / `.max` | come sopra |
| `C2` soddisfatta | `KPI.BQ1K3.c2.satisfied` | `M2` (nuova, §11) |
| soglia di `C2` | `KPI.BQ1K3.c2.threshold` | `M3` (nuova, §11) |
| profilo di mood delle categorie video | `MOOD.category.<categoria>.<asse>` in `data/curated/dim_category_mood.json` | i punti della dispersione |
| numero di categorie coperte dalla tabella di mood | `MOOD.coverage.rows` | — |

**Quale coppia di assi, e il vincolo che ne discende.** Gli assi sono tre — energia, positività, ritmo — e una dispersione ne porta due. **La scelta è di chi costruisce**, con un vincolo che non è negoziabile: **l'asse escluso va dichiarato a schermo**. Una scatola disegnata su due assi di tre è una **proiezione**, e una proiezione non dichiarata si legge come la cosa intera — nascondendo due volte la stessa asimmetria che rende `BQ1-K3` una stima per eccesso.

**La versione della tabella di mood va dichiarata a schermo**, ed è `conventions.kpi_mood_table_version`. È l'obbligo della terza condizione delle assegnazioni dell'analista (constitution): ogni valore pubblicato che dipende da quella tabella dichiara su quale versione è stato calcolato. Senza quel legame, una revisione della tabella lascia a valle numeri corretti quando sono stati scritti e mai più riverificati.

**Il limite di questa condizione compare qui, non solo a pagina 10.** La stima è **per eccesso**: la sovrapposizione reale è minore o uguale al valore pubblicato, e quanto minore il progetto non lo misura. È la ragione per cui la dispersione mostra il vuoto dentro il rettangolo invece di mostrare solo il rettangolo.

### 7.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| **qualunque filtro di categoria video** | è il caso letterale dell'issue `#18`: restringerebbe l'inviluppo e cambierebbe `BQ1-K3` senza alcun segnale. Su questa pagina il difetto sarebbe **visibile e ingannevole insieme** — il rettangolo si stringerebbe e sembrerebbe corretto |
| selezione di una categoria che ricalcola la quota | stessa ragione. **Ammessa l'evidenziazione** del punto |
| filtro sulle tracce | `mood_profile_overlap` conta le tracce dentro l'inviluppo: filtrarle produrrebbe una quota che nessun artefatto pubblica |
| la nube delle tracce come visuale | vedi §12: nessun artefatto la pubblica, e la sua grana non è pubblicata |
| il terzo asse come slicer che ruota la dispersione | produrrebbe tre proiezioni fra cui scegliere, e la scelta suggerirebbe che una sia *la* vista. Sono tutte parziali allo stesso modo, e la dichiarazione dell'asse escluso lo dice meglio di un controllo |

---

## 8. Pagina 6 — Quanto dovrebbe sbagliare

**Sezione servita**: §2, «Quanto la stima dovrebbe sbagliare perché la risposta cambi».

**Che parte dell'argomento porta**: di quanto la stima dovrebbe sovrastimare perché la seconda condizione cada. È il passaggio più forte dell'intero argomento, **e nella dashboard vecchia non esisteva**: la `009` lo ha prodotto rispondendo a una domanda che il progetto non aveva mai posto.

**Perché una pagina propria e non un capoverso della precedente.** È l'unica parte della sezione «che cosa lo farebbe cambiare» che porta valori ancorati, e la mossa dell'argomento cambia: da *ecco quanto vale la condizione* a *ecco quanto dovremmo aver sbagliato perché cada*. Sono due cose diverse, e la seconda è quella che un board contesterebbe per prima.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| il margine di `C2` | **barra orizzontale su asse `0-1` assoluto**, con il valore misurato, la soglia come riferimento, e la distanza fra i due etichettata | mostra che la distanza dalla soglia è ampia, su un asse che non è riscalato sui valori osservati. L'asse assoluto è ciò che impedisce alla barra di sembrare più o meno larga a seconda dello zoom |
| il margine in forma relativa | valore accanto alla barra, con le etichette | è la forma in cui l'argomento si legge — quanto la sovrapposizione reale dovrebbe essere più bassa della stima, in rapporto alla stima stessa — e la barra da sola non la dà |

**Valori a schermo, con l'ancora di ciascuno:**

| Valore | Ancora | Misura |
|---|---|---|
| valore misurato della sovrapposizione | `KPI.BQ1K3.overlap_share` | `mood_profile_overlap` (esiste) |
| soglia di `C2` | `KPI.BQ1K3.c2.threshold` | `M3` (nuova, §11) |
| margine assoluto | `KPI.BQ1K3.c2.margin` | `M4` (nuova, §11) |
| margine relativo al valore | `KPI.BQ1K3.c2.margin_share_of_value` | `M5` (nuova, §11) |

**Che cosa la visuale deve impedire, ed è la sola ragione per cui questa pagina esiste in questa forma.** Non deve suggerire che il margine sia una **stima dell'errore**: nessuno ha misurato di quanto l'inviluppo ecceda la regione reale, e il report non lo afferma. È una **condizione sull'errore** — dice quanto grande dovrebbe essere l'errore perché la conclusione si ribalti, non quanto grande sia.

**Ne discende un divieto di forma, non una raccomandazione**: nessuna barra di errore, nessun intervallo attorno al valore, nessuna banda. Entrambe le forme comunicano una dispersione stimata, e qui non ce n'è alcuna. La barra su asse assoluto con una linea di soglia è la forma che dice *ecco dove siamo, ecco dov'è il confine* senza dire nulla su dove sia il vero.

**Il secondo fatto che la stessa barra porta**, e va etichettato perché si legga: la risposta non cambierebbe con **nessuna soglia fino al valore misurato stesso**. Sulla barra è la distanza fra la linea di soglia e il valore, cioè ciò che la visuale già disegna. Non serve una seconda visuale: serve una seconda etichetta.

**La soglia è una stipulazione, non una misura**, e va marcata come tale a schermo. È la lettura letterale del termine «maggioranza» che il business case usa, fissata prima di guardare il valore. Chi ritenesse che «maggioranza» debba significare qualcosa di più severo troverebbe lo stesso esito con un margine più stretto — ed è un'informazione che appartiene alla pagina, non a una nota.

### 8.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| uno slicer che muove la soglia | è la trasformazione più tentante e la più sbagliata: renderebbe la soglia un parametro di chi guarda. La soglia è stata fissata **prima** di conoscere il valore, ed è quella la proprietà che rende la condizione difendibile. Uno slicer la distruggerebbe e nessun controllo lo segnalerebbe |
| qualunque filtro | i quattro valori sono unici sul catalogo intero |
| una banda o un intervallo attorno al valore | vedi sopra: comunicherebbe una dispersione stimata che nessun valore contiene |

---

## 9. Pagina 7 — La regione di ingresso

**Sezione servita**: §3, «La regione».

**Che parte dell'argomento porta**: esiste una regione del catalogo musicale insieme molto richiesta e molto affine a ciò che StreamWave già offre. È anche la terza condizione, `C3`.

**Perché `C3` non ha una pagina propria.** La terza condizione **è** questa regione: darle una pagina separata fra la 6 e la 7 la staccherebbe dai segmenti che la rendono vera, cioè dall'unica cosa che la rende utile a chi deve decidere.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| la dispersione dei segmenti | dispersione: ascissa `segment_demand_index` (scala `0-100`), ordinata `segment_catalog_affinity` (dominio `0-1`), due linee di riferimento, tre marcature distinte | `BQ2` è formulata da `business_case.md` §4 letteralmente come una domanda sul quadrante. Una dispersione con due linee di riferimento è la forma in cui quella domanda si legge su tutte le unità **senza ordinarle**. L'appartenenza al quadrante è un booleano già pubblicato per ogni segmento: la visuale mostra ciò che l'artefatto contiene, non una classificazione costruita a schermo |
| `C3` | indicatore booleano accanto alla dispersione | un booleano non ha altra forma che sé stesso |

**Valori a schermo, con l'ancora di ciascuno:**

| Valore | Ancora | Misura |
|---|---|---|
| domanda di un segmento | `KPI.BQ2K1.<segmento>.demand_index` | `segment_demand_index` (esiste) |
| affinità di un segmento | `KPI.BQ2K2.<segmento>.affinity` | `segment_catalog_affinity` (esiste) |
| appartenenza al quadrante | `KPI.BQ2K3.<segmento>.quadrant_high_high` | `segment_entry_priority_quadrant` (esiste) |
| soglia di domanda | `KPI.BQ2K3.threshold.demand` | soglia di `F7` (dichiarata dalla `008a`) |
| soglia di affinità | `KPI.BQ2K3.threshold.affinity` | soglia di `F7` (dichiarata dalla `008a`) |
| segmenti nel quadrante | `KPI.BQ2K3.quadrant_members_count` | — |
| `C3` soddisfatta | `KPI.BQ2K3.c3_satisfied` | `C3` companion (dichiarata da `CP-1`) |
| segmenti a domanda non misurata | `KPI.BQ2K1.high_zero_segments_count` | — |
| numero di segmenti del catalogo musicale | `SP.genre.count` | i punti della dispersione |

**Le tre marcature della dispersione**, che portano informazione e non decorazione, e devono restare distinguibili fra loro:

| Marcatura | Che cosa distingue |
|---|---|
| appartenenza al quadrante | i segmenti con `segment_entry_priority_quadrant` vero |
| domanda non misurata dalla fonte | i segmenti con `dim_segment[is_high_zero_genre]` vero |
| il resto | — |

**Perché i segmenti a domanda non misurata devono essere marcati nella dispersione, e non solo nella tabella.** La loro domanda mediana è nulla: nella dispersione cadono tutti contro il bordo sinistro, dove la posizione **si legge come «domanda bassa»**. `kpi_measures.md` §5.3 dice esattamente il contrario — il valore misura la copertura della fonte, non la domanda — e senza marcatura la visuale affermerebbe con la propria geometria ciò che il documento vieta di affermare a parole.

**Perché le linee di riferimento sono misure e non costanti digitate**: due numeri digitati in una visuale sono valori la cui unica fonte è che qualcuno li ha scritti. Le espressioni esistono già come variabili interne a `segment_entry_priority_quadrant`; esporle come misure permette di **leggerle** e confrontarle una volta con l'ancora.

**Il conteggio dei membri del quadrante compare, a differenza della `008a`.** Là non compariva, perché la dispersione lo mostra e un conteggio sarebbe stato un valore in più da ancorare senza che nulla lo richiedesse. Qui lo richiede l'argomento: `raccomandazione.md` §2 usa quel conteggio come **l'esito della terza condizione**, e la pagina che porta `C3` senza il numero che la soddisfa lascerebbe l'esito senza il proprio metro. È uno scostamento dal contratto precedente, dichiarato come tale.

### 9.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| filtro su qualunque attributo di `dim_track` o riga di `fact_track_segment` | `segment_demand_index` è una mediana sulle righe del fatto **senza `ALL`**: filtrare le tracce sposterebbe la mediana e produrrebbe un indice che nessun artefatto pubblica. È la forma più insidiosa della quarta grana, perché la visuale continuerebbe a chiamarsi «domanda» |
| filtro di popolarità, di anno, di durata | come sopra: cambiano la mediana o introducono un asse temporale |
| conteggio delle righe di un segmento come dimensione del punto | misura il **campionamento** e non il mercato, e a schermo si leggerebbe come una dimensione del segmento |
| totale, somma o media su più segmenti | i segmenti si sovrappongono: una traccia appartiene a più segmenti, e un totale conterebbe più volte le stesse tracce |

**Ammessa**: la selezione incrociata verso la pagina 8, come evidenziazione. Vedi §10.

---

## 10. Pagina 8 — Che cosa la regione contiene

**Sezioni servite**: §3, «La regione» e «Un'esclusione che va dichiarata».

**Che parte dell'argomento porta**: quali segmenti la regione contiene, in quale ordine, e quali di essi portano una domanda che la fonte non ha misurato.

**Perché la graduatoria è su una pagina propria e non accanto alla dispersione.** Non è per capienza — sarebbe la ragione che §1.1 vieta — ma perché **le due visuali fanno due mosse diverse**: la dispersione dice *esiste una regione*, la tabella dice *ecco che cosa contiene, e in quale ordine*. Sono le due metà che `raccomandazione.md` §3 tiene distinte, e su cui insiste che la seconda non sostituisce la prima.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| la graduatoria completa | **tabella, una riga per segmento e nessuna esclusa**, ordinata per punteggio decrescente | la dispersione mostra i punti e non i nomi: su quel numero di unità nessuna etichetta è leggibile, e la domanda «da quale segmento entrare» chiede un nome. La tabella lo dà, e dà la posizione esatta che la dispersione non può dare |

**Le colonne, e l'ordine non è libero:**

| Colonna | Misura o campo | Ancora |
|---|---|---|
| posizione | `segment_entry_priority_rank` (esiste) | `KPI.BQ2K3.<segmento>.rank` |
| segmento | `dim_segment[segment]`, con l'avvertimento accanto al nome dove `is_high_zero_genre` è vero | `catalogs.kpi_segments` |
| domanda | `segment_demand_index` (esiste) | `KPI.BQ2K1.<segmento>.demand_index` |
| quota di zeri | `segment_zero_share` (esiste), **nella colonna immediatamente adiacente alla domanda** | `KPI.BQ2K1.<segmento>.zero_share` |
| affinità | `segment_catalog_affinity` (esiste) | `KPI.BQ2K2.<segmento>.affinity` |
| punteggio | `segment_entry_priority_score` (esiste) | `KPI.BQ2K3.<segmento>.score` |
| quadrante | `segment_entry_priority_quadrant` (esiste) | `KPI.BQ2K3.<segmento>.quadrant_high_high` |

**La quota di zeri è adiacente alla domanda per obbligo, non per comodità.** Sono due misure e non una proprio perché una misura unica renderebbe possibile portarne a schermo una sola. Separarle in colonne distanti, o renderne una nascondibile dall'utente, ricrea il difetto che la separazione esisteva per impedire.

**Perché tutte le righe e non una cima di graduatoria.** I segmenti a mediana nulla stanno tutti nella coda profonda, e una vista alle prime posizioni li escluderebbe **insieme all'avvertimento che li accompagna**. Il lettore vedrebbe una classifica pulita e non saprebbe che una parte della coda non misura la priorità ma la copertura della fonte. Una vista che tronca la coda non è parziale: **mente per omissione**.

**I sette segmenti a domanda non misurata**, con la loro ancora di appartenenza: `catalogs.kpi_high_zero_segments`. L'avvertimento accanto al nome è una **marcatura, non una spiegazione** — il perché è testo della `010b`.

**I pari merito**: due segmenti con lo stesso punteggio portano la stessa posizione e la successiva salta di altrettante unità. È il comportamento di `RANKX ( …, Skip )` già nella formula pubblicata; la tabella non deve reintrodurre un ordinamento secondario che spareggi, perché uno spareggio per nome produrrebbe un ordine riproducibile ma **arbitrario, presentato con l'autorevolezza di un risultato**.

### 10.1 L'issue `#21` si chiude, e come

**Il difetto**: nella dashboard a quattro pagine dispersione e graduatoria stavano sulla stessa pagina e **non si evidenziavano a vicenda**. Selezionare un punto non marcava la riga corrispondente.

**Che cosa cambia in questo disegno.** Su due pagine il problema cambia natura: non è più un'interazione mancante fra visuali vicine, è una **continuità di lettura fra due schermate**. La selezione di un segmento sulla pagina 7 deve restare selezionata sulla pagina 8, e viceversa.

**Come si realizza**: sincronizzando la selezione fra le due pagine. Resta **evidenziazione e non filtro** — le soglie e le posizioni portano `ALL ( dim_segment )` e non si muovono (§2.1).

**Che cosa questo contratto può e non può dire.** Può dichiarare il vincolo: le due pagine si evidenziano a vicenda, e la selezione non ricalcola alcun valore. **Non può dichiarare che funzioni**: questa sessione non ha aperto Power BI e non ha verificato che quel comportamento sia ottenibile nella forma prevista. La `010b` lo verifica a schermo e lo dichiara nel proprio esito.

**L'issue si chiude solo quando quella verifica è passata.** Se il comportamento non fosse ottenibile, l'issue resta aperta e questo paragrafo diventa un ritrovamento della `010b`.

### 10.2 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| filtro «prime N posizioni» | tronca la coda, cioè il difetto di §10 |
| possibilità di nascondere la colonna della quota di zeri | ricrea il difetto che la sua adiacenza obbligatoria impedisce |
| riga di totale, somma o media su più segmenti | i segmenti si sovrappongono e un totale conterebbe più volte le stesse tracce |
| ordinamento secondario che spareggia i pari merito | vedi sopra |
| drill-through al livello traccia | porta a una grana che non è pubblicata |
| filtro su qualunque attributo di `dim_track` o `fact_track_segment` | sposterebbe la mediana della domanda (§9.1) |

**Ammessa**: la selezione incrociata verso la pagina 7, in entrambe le direzioni, come evidenziazione.

---

## 11. Pagina 9 — Quanto vale

**Sezione servita**: §4.

**Che parte dell'argomento porta**: quanto varrebbe l'espansione, e che cosa quei numeri diventano su una base di abbonati.

**La forma del dato qui è diversa da tutte le altre, e la pagina lo riflette.** Non ci sono misure da calcolare: ci sono sei valori di scenario congelati dalla `004` in [`reports/bq3_scenarios.json`](../../../reports/bq3_scenarios.json). Non c'è aggregazione, non c'è dimensione di calcolo, non c'è relazione con il resto del modello.

| Elemento | Visuale | Ragione, contro la forma del dato |
|---|---|---|
| `BQ3-K1` e `BQ3-K2` | **tabella**, due righe (un KPI ciascuna) e tre colonne (`Pessimista`, `Centrale`, `Ottimista`), più una colonna di unità | i tre valori non sono una serie né una distribuzione: sono tre ipotesi alternative, e nessuna è più probabile delle altre. Una tabella li affianca senza ordinarli e senza attribuire loro una magnitudine visiva. Una barra suggerirebbe un confronto quantitativo fra scenari, che le assunzioni non sostengono |
| il fattore di conversione | **seconda tabella**, tre colonne, con l'unità dichiarata in intestazione | è la stessa terna espressa su un'unità dichiarata. La forma è la stessa perché la natura del dato è la stessa: tre ipotesi, non una distribuzione |

**Valori a schermo, con l'ancora di ciascuno:**

| Valore | Ancora |
|---|---|
| adozione, pessimista / centrale / ottimista | `BQ3.adoption.worst` / `.base` / `.best` |
| uplift, pessimista / centrale / ottimista | `BQ3.uplift.worst` / `.base` / `.best` |
| uplift per 100.000 abbonati, la terna | derivato da `BQ3.uplift.*` tramite `M6` (nuova, §12) |

**Il divieto di scheda singola è strutturale, non una raccomandazione.** Il principio I lo impone per la confidenza bassa: un valore singolo comunica una certezza che il dato non ha. **I valori si presentano sempre come terna, mai isolati, nemmeno in una frase di sintesi** — e prendere il valore centrale perché sta meglio in una slide è precisamente ciò che il divieto esiste per impedire.

**Il divieto di moltiplicazione resta intero.** Nessuna visuale, nessuna misura, nessuna colonna moltiplica l'uplift per una **base utenti di StreamWave**. Nessuna base è quantificata in questo progetto, e un totale così ottenuto sarebbe un numero che nessuno ha misurato con l'autorevolezza di uno misurato.

**Perché il fattore di conversione non viola quel divieto**, e va detto con precisione perché è il punto in cui è più facile sbagliare: `M6` **converte l'unità** della terna, non stima un totale. Il fattore — 100.000 — è dichiarato a schermo **come unità** e non è una stima della base di StreamWave. Chi conosce la propria base divide per 100.000 e moltiplica: l'operazione resta sua, e il risultato eredita per intero la confidenza bassa della terna.

**La formulazione sull'uplift, che chiude l'issue [`#26`](https://github.com/Valvln/streamwave-bi/issues/26) per questo contratto.** Si usa la formulazione **stretta**, la stessa che `raccomandazione.md` §4 adotta:

> Qui nessuna base viene quantificata e nessun artefatto del progetto offre una chiave per farlo. Non è un presidio: è una rinuncia, e non impedisce a valle l'operazione che scoraggia.

**Mai** «l'uplift non è scalabile», che [`bq3_scenarios.md`](../../../docs/bq3_scenarios.md) §8 dichiara falsa: il valore **è** scalabile, ed è ciò che il fattore di conversione insegna a fare. L'issue `#26` **resta aperta** sui due documenti che portano ancora la formulazione esclusa — `kpi_operators.md` §9 e il contratto di pagina della `008a` §8 — e questa feature non li corregge.

**Il debito della `004` è aperto, e va dichiarato dove pesa.** Il valore centrale della terna di adozione non è una misura di questo progetto: è un **benchmark esterno**, e il comunicato che lo pubblica non nomina lo studio da cui proviene né dichiara la numerosità del campione. Non esiste copia archiviata né identificativo permanente. La verificabilità di quel benchmark è registrata come debito in [`docs/roadmap.md`](../../../docs/roadmap.md), la sua risoluzione è una **decisione di governance** che questa feature non prende, e la pagina che porta quei numeri lo dichiara.

**L'assunzione `A6` è richiamata qui**, non introdotta: la sua collocazione è la pagina 3. Il richiamo è necessario perché `A6` si applica **solo** ai valori di questa pagina, e una pagina di scenari che non lo ricordasse lascerebbe l'assunzione a tre schermate di distanza dai soli numeri che tocca.

### 11.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| slicer di scenario che riduce a uno | è il divieto di scheda singola per un'altra via: un intervallo ridotto a un valore è un valore singolo, e il fatto che l'utente lo abbia scelto non lo rende misurato |
| un campo in cui digitare la base abbonati | trasformerebbe la rinuncia in un presidio mancato: il report calcolerebbe il totale che dichiara di non voler calcolare, e lo presenterebbe con la propria autorevolezza |
| qualunque altro filtro | i sei valori non hanno dimensioni |
| selezione incrociata con il resto del report | i valori di scenario non hanno relazione con le tabelle del catalogo, **e non devono averne**: una relazione renderebbe possibile filtrarli per segmento o per categoria, producendo scenari che nessuno ha stimato |
| misure derivate dai sei valori oltre a `M6` | vedi il divieto di moltiplicazione |

---

## 12. Pagina 10 — Che cosa lo ribalterebbe

**Sezioni servite**: §5 e §6.

**Che parte dell'argomento porta**: le condizioni alle quali la raccomandazione si ribalterebbe, e che cosa non si può concludere.

**Questa pagina è di sola prosa**, e la ragione è che tre delle quattro condizioni di ribaltamento **non portano valori**. La quarta — di quanto la stima dovrebbe sbagliare — ha la propria pagina, la 6, perché è l'unica ancorata.

**Perché è l'ultima pagina, e perché non esiste una pagina conclusiva dopo di essa.** Una pagina di sintesi finale ripeterebbe la risposta già data alla pagina 2, e la ripetizione in coda a un argomento è il punto in cui una raccomandazione si ammorbidisce: si riassume, e riassumendo si perde la qualificazione. `raccomandazione.md` chiude sulla stessa posizione — «che cosa questa raccomandazione non è» — che è la più scomoda e la più onesta.

| Elemento | Che cosa porta | Ragione |
|---|---|---|
| le condizioni di ribaltamento | l'articolazione **condizione → conseguenza**, una per riga, visibile come struttura | ciò che questa pagina deve dare all'occhio è l'articolazione, non un grafico: per ciascuna condizione è scritto **che cosa succederebbe**, non soltanto che un rischio esiste, e la struttura a due colonne è ciò che rende visibile che la seconda metà c'è sempre |
| che cosa non si può concludere | i limiti dichiarati, come elenco strutturato | — |

**Le quattro condizioni di ribaltamento**, con la conseguenza di ciascuna:

| Se | Allora |
|---|---|
| la tabella che assegna il carattere alle categorie video venisse rivista | la seconda condizione andrebbe **ricalcolata da capo**, e con essa il verdetto. Non è un rischio remoto: è il modo normale in cui quella tabella evolve |
| la sovrastima fosse maggiore del margine | l'esito passerebbe da tre condizioni su tre a due — **sostegno parziale**, non «argomento non sostenuto». Il valore è a pagina 6 |
| i cataloghi sostitutivi non rappresentassero StreamWave | **nessuna delle tre condizioni direbbe più nulla su StreamWave**, indipendentemente da quanto ciascuna sia stata calcolata con cura. È `A1`, la cui collocazione è la pagina 3 |
| arrivassero dati che il progetto non ha | dati comportamentali sostituirebbero l'assunzione di rappresentatività con un'osservazione; dati di costo non toccherebbero la coerenza ma potrebbero rendere l'operazione insostenibile; dati più recenti potrebbero raccontare un'altra storia |

**I limiti che questa pagina porta**, e nessuno di essi è nuovo: non è un business case finanziario e manca interamente il lato dei costi; non descrive StreamWave; non dice che il pubblico attuale vorrebbe la musica, perché la sovrapposizione è fra **caratteristiche di contenuto** e non fra persone osservate; non è una previsione, e la banda fra pessimista e ottimista **non è un intervallo di confidenza**.

**Un solo valore compare su questa pagina**, ed è la copertura temporale dei dati:

| Valore | Ancora |
|---|---|
| anno più recente del catalogo video | `NF.num.release_year.max` |

**Gli altri due anni — il catalogo musicale e il benchmark — non sono ancorabili** e vanno marcati come non misurati. Il catalogo musicale **non espone alcun campo di data**: il suo anno è un'affermazione presa dalla documentazione della fonte, e il profilo dei dati dichiara esplicitamente di non poterla verificare. È una differenza di statuto fra i due anni, e appiattirla a schermo affermerebbe che entrambi sono osservati.

**Le assunzioni `A1` e `A6` sono richiamate, non introdotte.** La loro collocazione è la pagina 3.

### 12.1 Interazioni non offerte, e perché

| Non offerto | Perché |
|---|---|
| qualunque interazione | è una pagina di prosa e di struttura |
| una visuale dei rischi ordinata per gravità | **nessun valore ordina quei rischi**, e disegnarli ordinati sarebbe una graduatoria senza fonte. È il caso concreto e prevedibile contro cui §14 esiste |

---

## 13. Le misure e le visuali che la `010b` dovrà costruire

**È la sezione su cui poggia la stima della `010b`.** Consuma [data-model.md](../data-model.md) §2 e §3 invece di riprodurlo: là ciascuna voce ha la propria motivazione per esteso.

### 13.1 Le sei misure nuove

Nessuna calcola un KPI: quattro leggono valori già pubblicati, una compone un conteggio, una converte una terna su un'unità dichiarata.

| # | Nome proposto | Che cosa calcola | Legge da | Pagina |
|---|---|---|---|---|
| `M1` | `verdict_conditions_satisfied` | quante delle tre condizioni sono soddisfatte, conteggio `0-3` | compone `c1_music_above_median`, `M2` e la companion `C3` | 2 |
| `M2` | `c2_overlap_above_threshold` | la condizione `C2` come booleano | `mood_profile_overlap` contro `M3` | 2, 5 |
| `M3` | `c2_threshold` | la soglia di `C2`, esposta come misura invece che digitata | costante ancorata a `KPI.BQ1K3.c2.threshold` | 5, 6 |
| `M4` | `c2_margin` | la distanza fra il valore misurato e la soglia | `mood_profile_overlap` meno `M3` | 6 |
| `M5` | `c2_margin_share_of_value` | il margine rapportato al valore misurato | `M4` diviso `mood_profile_overlap` | 6 |
| `M6` | `arpu_uplift_per_100k` | la terna dell'uplift per ogni 100.000 abbonati | la tabella disconnessa degli scenari, per un fattore dichiarato | 9 |

**`M2` esiste perché `C2` è l'unica delle tre condizioni senza una companion booleana pubblicata.** `C1` ha `c1_music_above_median`, verificata contro il motore; `C3` nasce dalla decisione `CP-1` della `008a`; `C2` esiste solo come valore continuo più una soglia. Senza `M2` la visuale del verdetto avrebbe due booleani e un numero. **È un'asimmetria del framework che nessuna feature precedente aveva rilevato**, e questo disegno la registra come ritrovamento invece di risolverla in silenzio.

**`M1`, `M4` e `M5` portano valori che `reports/kpi_measures.json` già pubblica.** La loro lettura dal motore va confrontata **una volta** con il valore pubblicato: una divergenza è un ritrovamento, non un numero da accettare.

**Su `M6`, se la `010b` trovasse più semplice** portare quei tre valori come colonne della tabella disconnessa invece che come misura, è equivalente e va dichiarato nell'esito.

### 13.2 Le quattro visuali nuove

| # | Visuale | Tipo | Pagina | Che cosa la alimenta |
|---|---|---|---|---|
| `V1` | il verdetto congiunto | stato a tre elementi dentro un esito unico | 2 | `c1_music_above_median`, `M2`, `C3`, `M1` |
| `V2` | i due cataloghi sui tre assi | dispersione delle categorie video con inviluppo | 5 | `data/curated/dim_category_mood.json`, `KPI.BQ1K3.bound.*` |
| `V3` | il margine di `C2` | barra orizzontale su asse `0-1` assoluto | 6 | `mood_profile_overlap`, `M3`, `M4`, `M5` |
| `V4` | il fattore di conversione | tabella a tre colonne, unità in intestazione | 9 | `reports/bq3_scenarios.json` via `M6` |

**Una quinta visuale è nuova come forma ma non come dato**: la distribuzione delle categorie video per numero di titoli, a pagina 4. Legge gli stessi valori che la `008a` portava come scheda, in una forma che la dashboard vecchia non aveva.

### 13.3 Le quattro visuali riusate, invariate

| Visuale | Pagina | Origine |
|---|---|---|
| dispersione dei segmenti | 7 | contratto `008a` §5.1 |
| graduatoria completa, una riga per segmento | 8 | contratto `008a` §5.2 |
| terna degli scenari | 9 | contratto `008a` §6 |
| scheda della North Star | 4 | contratto `008a` §3 |

**Le due visuali di `BQ2` cambiano pagina ma non forma, ed è deliberato.** La revisione della `008b` non ha trovato difetti in quelle due visuali: ha trovato che stavano in un inventario. Ridisegnarle avrebbe rimesso in discussione scelte già verificate a schermo per un guadagno che nessuno sta chiedendo.

### 13.4 Le tre verifiche del modello da rifare — issue `#20`

Il `.pbix` **non è versionato**, e tre impostazioni del modello si possono riperdere a ogni riapertura. **Chi costruisce le rifà**, e questa feature non chiude e non tocca quell'issue.

Le tre impostazioni sono quelle registrate nell'issue [`#20`](https://github.com/Valvln/streamwave-bi/issues/20). Questo contratto **non le elenca per nome**: non ha aperto il file, non può accertare quali siano oggi disattese, e un elenco copiato da un'issue in un contratto di disegno è una seconda copia che può divergere. Chi costruisce legge l'issue.

**Perché il richiamo esiste comunque.** Un'impostazione riperduta non produce un errore: produce un valore diverso senza segnale. È la stessa classe di difetto della quarta grana, e il presidio è lo stesso — dichiararlo prima, verificarlo dopo.

---

## 14. Le due pagine di sola prosa, e perché non si decorano

Le pagine 3 e 10 non portano alcuna visuale. **Non è un vuoto da riempire.**

Ciò che una pagina di sola prosa deve dare all'occhio è **struttura** — un'articolazione visibile fra le parti — non un grafico. La pagina 3 articola i due cataloghi sostitutivi contro i due che il progetto non ha; la pagina 10 articola condizione e conseguenza, una per riga.

**Un grafico costruito per riempire una pagina di prosa è peggio di un vuoto**, perché afferma con la propria geometria qualcosa che il testo non afferma. Il caso concreto, prevedibile e vietato è una **barra dei rischi ordinata per gravità** a pagina 10: nessun valore ordina quei rischi, e disegnarli ordinati sarebbe una graduatoria senza fonte — cioè ciò che il principio I vieta.

---

## 15. La visuale che i dati non sostengono

**Le tracce del catalogo musicale come nube sui tre assi di mood, con l'inviluppo sovrapposto.**

Sarebbe stata la forma migliore per la pagina 5: renderebbe visibile **quanta parte della scatola è vuota**, che è esattamente ciò che «stima per eccesso» significa. `V2` la sostituisce con le categorie video, che sono ancorate, e ottiene una parte dello stesso effetto.

**Non entra nel contratto**, per tre ragioni che valgono insieme: nessun artefatto pubblica quella nube; la sua grana è la traccia e nessun KPI è pubblicato a quella grana; portarla a schermo significherebbe pubblicare valori che nessun documento del progetto pubblica, violando la regola di §2.

**È dichiarata qui perché chi costruisce non la reinventi credendo che sia stata dimenticata**, e non la costruisca credendo di migliorare il disegno.

**Un secondo materiale che il disegno non usa**, e la ragione è diversa: **non esiste alcun profilo di mood per segmento musicale pubblicato come valore ancorato**. `reports/kpi_measures.json` porta per ciascun segmento affinità e distanza, non le tre coordinate. Un confronto di profili segmento per segmento richiederebbe tre misure nuove sui tre assi — leggibili da `dim_track`, che porta le colonne — e questo disegno **non le chiede**: la seconda condizione è un'affermazione sull'**intero** catalogo musicale, e portare i segmenti a pagina 5 anticiperebbe la parte «con che cosa entrare» che viene dopo.

---

## 16. Navigazione

Una barra di navigazione **persistente su tutte e dieci le pagine**, con l'elemento della pagina corrente marcato come tale. Da ciascuna pagina si raggiunge ogni altra con un solo passaggio, tramite elementi interni al report.

**Il riquadro delle schede di Power BI non è navigazione**: è un'affordance dello strumento, non del report, e chi guarda il file in modalità di lettura o in un contenitore incorporato può non averlo. Un report che dipende da esso ha una navigazione che funziona solo sulla macchina di chi lo ha costruito.

**Le etichette della barra sono i titoli di pagina di §1**, non prosa nuova.

**Una considerazione che il disegno lascia a chi costruisce.** Dieci elementi in una barra sono molti, e su uno schermo 16:9 la barra potrebbe non reggerli in forma leggibile. Il contratto **non prescrive la soluzione** — un raggruppamento, due livelli, elementi più stretti — perché è una scelta di forma che si giudica davanti allo schermo. Prescrive il vincolo: **un solo passaggio fra due pagine qualunque**, e l'ordine delle dieci pagine visibile nella barra, perché la barra è il solo posto in cui la spina dell'argomento è visibile tutta insieme.

---

## 17. Dove la `010b` scriverà

Lo spazio elencato qui è **riservato, non vuoto**. Una pagina disegnata senza questo spazio costringerebbe la feature successiva a ridisegnare le pagine per farvi entrare il proprio testo, e ridisegnare significa rimettere in discussione scelte già approvate.

| Pagina | Spazio riservato | Che cosa ci andrà |
|---|---|---|
| 1 | fascia sotto il diagramma delle condizioni | che cosa il report risponde e che cosa non risponde; la domanda in forma leggibile |
| 2 | fascia sotto la visuale del verdetto | che cosa la risposta **non** dice — non dice che l'espansione sarà redditizia, dice che sarebbe coerente; perché la confidenza è media e non la media delle tre |
| 3 | **l'intera pagina**, che è di sola prosa | `A1` e `A6` in forma divulgativa, e perché nessuna delle due entra nella scala di confidenza |
| 4 | fascia sotto la distribuzione | la distinzione fra quota e condizione `C1`; che «non residuale» non significa «grande» |
| 5 | fascia sotto la dispersione, la più alta delle pagine con visuale | la stima per eccesso; perché il dato del lato video è costruito e non osservato; l'ampiezza dell'inviluppo |
| 6 | fascia sotto la barra | che il margine è una **condizione sull'errore** e non una stima dell'errore; che la soglia è una stipulazione fissata prima del valore |
| 7 | fascia sotto la dispersione | che cosa significano mediana e affinità; che i segmenti si sovrappongono e non si sommano |
| 8 | fascia sotto la graduatoria | la lettura dei sette segmenti a domanda non misurata; che contare le righe non dimensiona un mercato; come la graduatoria **non** si legge |
| 9 | fascia sotto le due tabelle, la più alta del report | il tasso lordo; il livello mensile che non è un cumulato; il debito della `004`; la formulazione stretta sull'uplift |
| 10 | **l'intera pagina**, che è di sola prosa | le quattro condizioni di ribaltamento con la propria conseguenza; i limiti dichiarati |

**Nessuna di queste fasce contiene testo alla chiusura di questa feature.** Il principio IV non è soddisfatto nella sua metà «nella dashboard» finché la `010b` non chiude, ed è la deviazione registrata nel Complexity Tracking di [plan.md](../plan.md).

---

## 18. Le decisioni su cui questo contratto chiede una conferma

Sono i punti in cui il disegno **estende o contraddice** ciò che era già stato fissato, e per questo tornano a Valerio invece di essere dati per acquisiti.

### `CP-1` — Il report porta sette KPI su otto

`BQ1-K2` e la sua companion non compaiono (§1.3).

**Decisione proposta**: restano fuori. L'argomento non li usa, e includerli richiederebbe una pagina che nessuna sezione serve.

**Alternativa scartata**: includerli per completezza rispetto al framework. È la proprietà organizzatrice della dashboard vecchia, ed è ciò che la revisione ha respinto.

**Che cosa comporta**: il report non è più leggibile come «la dashboard degli otto KPI». Chi cercasse `BQ1-K2` non lo troverebbe, e nessuna pagina spiega perché manchi — perché spiegarlo richiederebbe di nominare un framework che il report ha deliberatamente sciolto. **È l'aspetto più contestabile di questa decisione.**

### `CP-2` — Sei misure nuove, di cui una colma un'asimmetria del framework

Le sei misure di §13.1.

**Decisione proposta**: si scrivono nella `010b`. Nessuna calcola un KPI; quattro portano valori già pubblicati e vanno confrontate una volta con la propria ancora.

**Che cosa chiede in più**: che `M2` sia riconosciuta come ciò che è — la companion booleana che `C2` non ha mai avuto, mentre `C1` e `C3` ce l'hanno. Colmarla è una conseguenza del disegno, non il suo scopo, e va registrata come tale.

**Che cosa comporta**: le misure nel modello diventano venti — dieci pubblicate, due soglie di `F7`, due companion di `CP-1` della `008a`, sei nuove.

### `CP-3` — L'issue `#21` si chiude, ma la chiusura è condizionata

Dispersione e graduatoria si evidenziano a vicenda attraverso due pagine (§10.1).

**Decisione proposta**: si chiude, **a condizione che la `010b` verifichi a schermo** che la sincronizzazione della selezione sia ottenibile senza ricalcolare alcun valore.

**Che cosa chiede**: che la chiusura dell'issue sia riconosciuta come **condizionata** e non come acquisita. Questa sessione non ha aperto Power BI: se il comportamento non fosse ottenibile nella forma prevista, l'issue resta aperta e diventa un ritrovamento della `010b`.

### `CP-4` — Il conteggio dei membri del quadrante compare, in scostamento dalla `008a`

Il contratto della `008a` §5.3 dichiarava esplicitamente che nessun conteggio dei membri del quadrante compare come valore a sé. Questo disegno lo porta a schermo (§9).

**Decisione proposta**: compare. L'argomento lo usa come **l'esito della terza condizione**, e una pagina che porta `C3` senza il numero che la soddisfa lascerebbe l'esito senza il proprio metro.

**Che cosa chiede**: che lo scostamento sia riconosciuto come tale. Il contratto precedente aveva ragione nel proprio perimetro — là il conteggio era un valore in più senza che nulla lo richiedesse — e qui qualcosa lo richiede. **Non è una correzione di quel contratto**: è una decisione diversa in un disegno diverso, e i due contratti restano entrambi validi per il proprio artefatto.

---

## 19. Che cosa questo contratto non decide

**I colori, i caratteri, le dimensioni esatte.** Sono di chi costruisce, con **una eccezione**: le tre marcature della dispersione di §9 — quadrante, domanda non misurata, resto — devono restare distinguibili fra loro, perché la distinzione porta informazione e non decorazione.

**Quale coppia dei tre assi di mood porta la dispersione di pagina 5.** È di chi costruisce, con il vincolo che l'asse escluso sia dichiarato a schermo (§7).

**Come i dieci elementi di navigazione stanno in una barra leggibile** (§16). Il vincolo è il passaggio singolo e l'ordine visibile; la forma si giudica davanti allo schermo.

**L'ordine in cui le pagine vengono costruite.** È fissato dai task della `010b`, non da qui.

**Che cosa accade se una visuale non regge davanti allo schermo.** È l'unica cosa che questo disegno non poteva verificare a tavolino, ed è la ragione per cui gli scostamenti sono **previsti** dal disegno invece di essere trattati come difetti. Uno scostamento si annota **mentre accade** e si elenca nell'esito con la propria ragione; non si ricostruisce a memoria alla fine.

**In quale forma il `.pbix` porta oggi i sei valori di scenario.** Il file non è versionato e questa sessione non lo ha aperto. La decisione `CP-2` della `008a` resta il vincolo dichiarato: i sei valori raggiungono il modello da `reports/bq3_scenarios.json` come tabella disconnessa. Accertare che sia così è della `010b`.
