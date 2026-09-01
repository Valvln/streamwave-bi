# Ricognizione: che cosa la `010b` ha accertato prima di costruire

**Feature**: `010b-report-costruzione` | **Data**: 2026-08-29

Questo documento raccoglie ciò che è stato letto e accertato **prima** che la spec fosse scritta, e prima che Power BI fosse aperto. Non contiene decisioni: le decisioni stanno in [spec.md](spec.md) e in [plan.md](plan.md).

---

## R-1. Il contratto di pagina si legge da solo? La prima lettura senza l'argomento accanto

**Perché questa verifica esiste, e perché tocca a questa sessione.** Il revisore in contesto pulito della `010a` ha ricevuto il contratto di pagina **insieme** a [`docs/raccomandazione.md`](../../docs/raccomandazione.md). Poteva quindi giudicare se il disegno reggesse l'argomento — non se il contratto si reggesse **da solo**. È dichiarato come rischio accettato nel verbale della `010a`, ed è la ragione per cui questa sessione è la prima a poterlo accertare: ha letto il contratto per intero **prima** di aprire la raccomandazione.

**Il metodo, dichiarato perché la verifica sia contestabile.** Il contratto è stato letto integralmente, dalla §1 alla §19, come primo file della sessione. `raccomandazione.md` è stato aperto **dopo**. Ciò che segue è quanto è risultato non ricostruibile dal solo contratto, annotato durante quella lettura.

**L'esito, in una riga: il contratto si legge da solo per costruire, non per capire perché.** Le sue prescrizioni sono eseguibili senza l'argomento accanto; le sue **giustificazioni** in tre punti non lo sono.

### I tre punti in cui il contratto rinvia a un documento che chi costruisce potrebbe non avere aperto

| # | Dove | Che cosa non è ricostruibile dal solo contratto | Conseguenza pratica |
|---|---|---|---|
| `L-1` | §1, tabella della mappa, colonna «Sezione servita» | la colonna è l'**unico** legame fra una pagina e la parte di argomento che porta, ed è espressa in riferimenti (`§2, «La prima»`) invece che in contenuto. Chi non ha la raccomandazione aperta ha dieci pagine e nessun modo di sapere se il taglio regga | nessuna: la colonna «Che parte dell'argomento porta», accanto, porta il contenuto in chiaro. Il rinvio è ridondante, non portante |
| `L-2` | §1.1, «i confini sono stati letti, non inventati» | l'affermazione difende la divisione delle sezioni in pagine dichiarando che le divisioni cadono su sottosezioni che `raccomandazione.md` marca già per conto proprio. **Non è verificabile dal contratto**: richiede di contare le sottosezioni di §2 e §3 del documento esterno | nessuna sulla costruzione. È un'affermazione sul metodo del disegno, non un vincolo da eseguire |
| `L-3` | §10.1 | è l'unico punto in cui il contratto **cita alla lettera** la raccomandazione, e lo fa perché il vincolo di disegno più forte della pagina 8 discende da quelle tre frasi. La citazione è riportata per esteso nel contratto | nessuna: la citazione è nel contratto. È l'unico dei tre rinvii costruito per non aver bisogno del documento esterno, ed è il modello che gli altri due non seguono |

### Che cosa questo significa, detto senza ammorbidire

**Il contratto è costruibile senza la raccomandazione.** Ogni §3-§12 dichiara pagina per pagina l'elemento, la visuale, la ragione contro la forma del dato, i valori con la propria ancora e le interazioni non offerte con il perché di ciascuna. Questa sessione ha potuto pianificare dieci pagine intere prima di aprire il documento dell'argomento, e non ha incontrato una sola prescrizione ambigua per mancanza di quel contesto.

**Ciò che si perde leggendolo da solo non è il che cosa, è il perché una pagina esiste.** Le sezioni §1 e §1.1 — la mappa e la regola molti-a-uno — sono le più esposte: argomentano che le dieci pagine seguono la spina di un argomento, e quella spina è nel documento esterno. Un costruttore che eseguisse il contratto senza aver letto la raccomandazione costruirebbe le pagine giuste **e non saprebbe difendere l'ordine in cui stanno**.

**Perché non è un difetto da correggere e va comunque dichiarato.** Un contratto di pagina che riportasse per esteso l'argomento che impagina sarebbe una seconda copia dell'argomento, cioè precisamente ciò che questo progetto vieta altrove per i valori e per la stessa ragione: due copie divergono e nessun controllo se ne accorge. Il rinvio è la scelta corretta. Ciò che il verbale della `010a` non poteva sapere, e che questa sessione accerta, è che **il rinvio cade sulle giustificazioni e non sulle prescrizioni** — ed è la differenza fra un rischio accettato che si è rivelato innocuo e uno che si è rivelato costoso.

**Un solo miglioramento sarebbe stato possibile a costo nullo**, ed è registrato come ritrovamento per la regia, non come rilievo: §1.1 avrebbe potuto dichiarare **quante** sottosezioni ha ciascuna delle due sezioni divise, come fa §10.1 con la propria citazione. Sarebbe stato un fatto strutturale del disegno — la stessa specie dei numerali che §11 del contratto dichiara ammessi — e avrebbe reso `L-2` verificabile senza aprire nulla.

---

## R-2. Le tre impostazioni del modello da riverificare — issue [`#20`](https://github.com/Valvln/streamwave-bi/issues/20)

Il contratto §13.4 rinvia all'issue e deliberatamente non le elenca. Sono state lette dall'issue e sono queste:

| # | Impostazione | Che cosa produce se è riperduta |
|---|---|---|
| `S-1` | tipizzazione di `energy`, `valence`, `danceability` nel dominio `0-1` | è l'issue [`#11`](https://github.com/Valvln/streamwave-bi/issues/11): il punto decimale letto come separatore delle migliaia porta `0.396` a valere `396`. **Tre KPI su otto sbagliati di due ordini di grandezza**, senza alcun errore a schermo |
| `S-2` | `QuoteStyle.Csv` sull'origine di `dim_title` | due record si spezzano in quattro, e i conteggi del catalogo video cambiano |
| `S-3` | colonna `scenario` di `bq3_scenarios` | l'intervallo di `BQ3` perde le etichette degli scenari |

**Perché la verifica non è una formalità.** Nessuna delle tre produce un errore: producono un **valore diverso senza segnale**. `S-1` è il precedente per cui il confronto fra motore e valore pubblicato esiste come presidio in questo progetto.

**Questa feature le rifà e non chiude l'issue.** Un esito positivo oggi non prova un vincolo per sempre: è la ragione registrata sulla `008a`, e vale identica qui.

---

## R-3. Un fatto che l'issue [`#21`](https://github.com/Valvln/streamwave-bi/issues/21) registra e che il contratto §10.3 non riporta

**Il contratto §10.3 prescrive** che la selezione si sincronizzi fra le pagine 7 e 8, restando evidenziazione e non filtro, e dichiara di non poter dire che funzioni.

**L'issue `#21` dice qualcosa di più preciso, ed è un accertamento già fatto dalla `008a` davanti allo schermo**:

> Power BI non offre l'evidenziazione come modalità di risposta per una dispersione né per una tabella: l'unica alternativa è il filtro, che farebbe sparire gli altri segmenti dalla graduatoria.

**Che cosa ne discende per `CP-3`.** La chiusura condizionata dell'issue non è una verifica di routine: esiste un accertamento precedente e **contrario** all'ottenibilità nella forma prevista, fatto sullo stesso strumento. Il contratto non lo riporta — non per omissione, ma perché §13.4 applica la stessa disciplina alle issue: non se ne fanno seconde copie.

**La conseguenza sul piano di questa feature.** La verifica di `CP-3` va fatta **presto**, non alla fine: se il comportamento non è ottenibile, l'issue resta aperta, diventa un ritrovamento, e le pagine 7 e 8 si costruiscono comunque — perché nessun valore dipende da quella sincronizzazione. È un rischio di chiusura di issue, non un rischio di costruzione.

**L'issue [`#33`](https://github.com/Valvln/streamwave-bi/issues/33) si innesta esattamente qui** e va letta insieme: chiede quale dei due comportamenti — evidenziare lasciando la riga dov'è, o evidenziare portandola in vista — sia quello richiesto. Se `CP-3` non fosse ottenibile, `#33` decade come domanda; se lo fosse, va risposta davanti allo schermo.

---

## R-4. I valori pubblicati che le sei misure nuove devono ritrovare

Letti da [`reports/kpi_measures.json`](../../reports/kpi_measures.json) **prima** di scrivere le misure, perché il confronto di §13.1 sia un confronto e non una conferma di ciò che si è appena scritto.

| Misura | Ancora | Valore pubblicato (`display`) |
|---|---|---|
| `M1` | `KPI.verdict.conditions_satisfied` | `3` |
| — | `KPI.verdict.all_satisfied` | `sì` |
| `M2` | `KPI.BQ1K3.c2.satisfied` | `sì` |
| `M3` | `KPI.BQ1K3.c2.threshold` | `0,5000` |
| `M4` | `KPI.BQ1K3.c2.margin` | `0,3450` |
| `M5` | `KPI.BQ1K3.c2.margin_share_of_value` | `0,4083` |
| `M6` | derivata da `BQ3.uplift.worst` / `.base` / `.best` | `0,60` / `1,20` / `2,40` euro per utente al mese |

**Che cosa questa tabella è e che cosa non è.** È il termine di confronto, letto dall'artefatto versionato. **Non** è un valore da digitare in una visuale: le misure si scrivono in DAX e leggono dal modello, e questa tabella serve a dire se ciò che il motore restituisce coincide. Una divergenza è un ritrovamento.

---

## R-5. Le ancore degli altri valori a schermo, verificate risolvibili

Verificate contro gli artefatti versionati prima della costruzione, perché una pagina non si disegni attorno a un'ancora che non esiste.

| Ancora | Artefatto | `display` |
|---|---|---|
| `CL.NF.titles.rows.after` | `reports/cleaning_report.json` | `8.807` |
| `CL.NF.category.distinct` | `reports/cleaning_report.json` | `42` |
| `KPI.BQ1K2.music_tracks` | `reports/kpi_measures.json` | `89741` |
| `SP.genre.count` | `reports/data_profile.json` | `114` |
| `NF.num.release_year.max` | `reports/data_profile.json` | `2021` |
| `MOOD.coverage.rows` | `data/curated/dim_category_mood.json` | `42` |
| `KPI.BQ1K1.c1.category_count.music_musicals` | `reports/kpi_measures.json` | `375` |
| `KPI.BQ1K1.c1.median_of_42` | `reports/kpi_measures.json` | `248,00` |
| `KPI.BQ1K1.share` | `reports/kpi_measures.json` | `0,0426` |
| `KPI.BQ1K1.denominator_titles` | `reports/kpi_measures.json` | `8807` |
| `KPI.BQ1K3.overlap_share` | `reports/kpi_measures.json` | `0,8450` |
| `KPI.BQ1K3.tracks_inside` | `reports/kpi_measures.json` | `75832` |
| `KPI.BQ1K3.bound.<asse>.min` / `.max` | `reports/kpi_measures.json` | `0,0500` / `0,9500` sui tre assi |
| `KPI.BQ2K3.threshold.demand` | `reports/kpi_measures.json` | `36,5` |
| `KPI.BQ2K3.threshold.affinity` | `reports/kpi_measures.json` | `0,8210` |
| `KPI.BQ2K3.quadrant_members_count` | `reports/kpi_measures.json` | `33` |
| `KPI.BQ2K1.high_zero_segments_count` | `reports/kpi_measures.json` | `7` |
| `KPI.BQ2K3.c3_satisfied` | `reports/kpi_measures.json` | `sì` |
| `conventions.kpi_mood_table_version` | `reports/kpi_measures.json` | `2` |

**Una osservazione sui tre assi di mood, che vincola la scelta della coppia di §7 del contratto.** Gli estremi pubblicati sono **identici sui tre assi**: `0,0500` come minimo e `0,9500` come massimo su energia, positività e ritmo. L'inviluppo è quindi un cubo, non una scatola irregolare, e **qualunque coppia di assi produce lo stesso rettangolo**. La scelta della coppia è quindi indifferente rispetto alla forma dell'inviluppo, e va fatta su ciò che distingue meglio i punti delle categorie video — che è una scelta davanti allo schermo, come §19 del contratto dichiara.

**Perché va detto, e non è una curiosità.** Il contratto §7 argomenta che la dispersione «mostra la scatola **e** mostra che la scatola è larga», e che il vuoto fra i punti e i bordi è il limite reso visibile. Con estremi uguali sui tre assi quel vuoto è **massimo per costruzione**: il rettangolo è quasi l'intero dominio `0-1`. La visuale fa quindi il proprio lavoro in modo più forte di quanto il contratto potesse sapere a tavolino, ed è un accertamento a favore del disegno, non contro.

---

## R-6. La grana dei valori dei segmenti, verificata

`reports/kpi_measures.json` pubblica per **ciascuno** dei `114` segmenti: `demand_index`, `zero_share`, `rows`, `affinity`, `distance`, `score`, `rank`, `quadrant_high_high`. Tutte le colonne che la tabella di pagina 8 richiede (§10.1 del contratto) sono quindi pubblicate alla grana a cui la tabella le porta, e la regola di invarianza di §2 è soddisfatta per costruzione su quella pagina.

---

## R-7. La formulazione esclusa sull'uplift — issue [`#26`](https://github.com/Valvln/streamwave-bi/issues/26) e [`#31`](https://github.com/Valvln/streamwave-bi/issues/31)

Le due issue coprono in parte lo stesso difetto: la formulazione «l'uplift non è scalabile» sopravvive su `docs/kpi_operators.md` §9 (`#31`) e sul contratto di pagina della `008a` §8 (`#26`).

**Questa feature non le chiude e non tocca quei due documenti.** Ciò che questa feature deve fare è **non ripetere** quella formulazione: il testo a schermo usa la formulazione stretta, la stessa di [`docs/raccomandazione.md`](../../docs/raccomandazione.md) §4 e del contratto di pagina §11.
