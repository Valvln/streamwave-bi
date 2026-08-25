# Implementation Plan: Dashboard — modello, pagine, misure a schermo

**Branch**: `008a-dashboard-model-pages` | **Date**: 2026-08-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/008a-dashboard-model-pages/spec.md`

## Summary

La feature produce **un deliverable che non entra nel repository** — il `.pbix` con il modello caricato, le misure scritte, quattro pagine e la navigazione — e **tre artefatti testuali che ci entrano**: il contratto di pagina (disegno, scritto prima della costruzione), l'esito della costruzione (che cosa esiste davvero e in che cosa si scosta), il verbale di revisione su entrambi. Aggiunge un contratto di lettura per la `008b` e la `010`, allinea il README, e non tocca alcun documento sotto `docs/` salvo eventuali note in loco per un ritrovamento.

**È la prima feature del progetto il cui deliverable non è ispezionabile da uno script.** Le sette precedenti producevano testo o JSON: `scripts/check_audit_coherence.py` poteva confrontare ogni cifra pubblicata con l'artefatto che la genera. Qui il controllo resta verde per una ragione debole — non c'è nulla di nuovo da controllare — e la garanzia si sposta interamente su tre presidi umani in sequenza: il contratto scritto **prima**, l'esito dichiarato **dopo**, la revisione in contesto pulito su entrambi.

**Il lavoro analitico è già chiuso in spec.** Le nove decisioni `F1`-`F9` sono argomentate per intero in [spec.md](./spec.md); questo piano non le riapre, le traduce in blocchi con un ordine di dipendenza dichiarato e un punto di fermata in mezzo. Tre blocchi su otto **non sono eseguibili da questa sessione**: la verifica di tipizzazione, la costruzione delle pagine e la lettura delle due soglie stanno tutti dentro la GUI, cioè fuori dal confine del principio V.

**Il rischio principale non è di trascrizione, come nella `007b`, ma di ordine.** Un contratto approvato e poi disatteso in silenzio produce esattamente l'artefatto che questa feature esiste per evitare: una documentazione che descrive un file diverso da quello che esiste, senza che nulla lo segnali — perché nulla può segnalarlo.

## Technical Context

**Linguaggio/Versione**: nessun linguaggio nuovo. DAX per le misure — già scritto e pubblicato dalla `007b`, qui incollato e non riscritto (`F8`, `FR-009`). Nessuna riga di Python nuova: questa feature non aggiunge né modifica alcuno script

**Dipendenze primarie**: Power BI Desktop, a interazione **manuale** (constitution, principio V e «Vincoli di Dominio e di Dato»). Il modello legge `data/processed/*.csv` — quattro file prodotti da `scripts/build_datasets.py` — e `data/curated/dim_category_mood.json`, versionato

**Storage**: nessun artefatto nuovo sotto `reports/` o `data/`. Nessun documento nuovo sotto `docs/`, quindi **nessuna riga nuova in `DOCUMENTS` o `ARTIFACTS`** di `scripts/check_audit_coherence.py` e nessuna riga nuova nella tabella di severità di `docs/convenzioni-marcatura.md` — è la prima feature dalla `004` a non estendere il controllo, ed è dichiarato qui perché la sua assenza non venga letta come una dimenticanza. Il `.pbix` non è versionato (`FR-029`)

**Testing**: per esecuzione e per ispezione secondo [quickstart.md](./quickstart.md). **Due categorie distinte, e la distinzione è la cosa importante**: una prova eseguibile (`check_audit_coherence.py` verde, che qui certifica soltanto che nulla di pubblicato è stato rotto) e nove prove manuali che richiedono il `.pbix` aperto e non saranno mai automatizzabili. Il loro esito è un'osservazione umana dichiarata come tale, sulla forma già usata da `E9` della `007b`

**Piattaforma target**: Power BI Desktop su Windows, macchina di Valerio, schermo singolo in rapporto 16:9. La leggibilità di 114 punti e 114 righe si giudica lì

**Tipo di progetto**: un file binario non versionato, tre documenti di feature, un contratto di lettura, un allineamento di README. Nessuna applicazione, nessun servizio, nessuno script

**Obiettivi di performance**: nessuno dichiarato dalla spec. Il volume più grande che una visuale attraversa è 113.550 righe di `fact_track_segment` aggregate a 114 punti: nell'ordine dei secondi su un motore in memoria, non un vincolo di progettazione. Il vincolo reale non è la velocità ma la **leggibilità**: 114 punti in una dispersione e 114 righe in una tabella (`F3`)

**Vincoli**: nessun valore a schermo a una grana non pubblicata (`F2`, `FR-019`); nessuna scheda singola per `BQ3` (`F4`, `FR-013`); nessuna moltiplicazione dell'uplift (`FR-014`); nessuna misura nuova, nessun booleano nuovo (`F6`, perimetro); il testo DAX incollato è quello pubblicato (`FR-009`); ~5 ore di lavoro effettivo, revisione e chiusura incluse, **con le ~2 ore di costruzione manuale dentro il conteggio** e non fuori (principio III)

**Scala/Ambito**: 7 tabelle nel modello, 10 misure (8 principali più 2 companion), 4 pagine, 3 grane pubblicate, 114 segmenti in due visuali, 8 KPI a schermo con 8 coppie di etichette fonte/confidenza, 2 soglie esposte come misure e lette una volta, 2 issue da dichiarare (`#11`, `#18`), 1 ritrovamento già noto da registrare per la `008b` (`F6`), 0 script nuovi, 0 artefatti nuovi

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni numero mostrato in dashboard dichiara fonte e confidenza | ✅ `F5` porta le etichette a schermo accanto a ogni KPI; nessuna promozione di confidenza, tabella ereditata invariata da `business_case.md` §5.4 | ✅ rafforzato dalla Fase 1: `F7` elimina l'ultima classe di numeri a schermo privi di fonte — le due soglie, che diventano misure invece di costanti digitate |
| **II. Riproducibilità** | trasformazioni come codice versionato | ✅ nessuna trasformazione nuova: il modello legge i file che `scripts/build_datasets.py` produce, e nessuna colonna viene calcolata nella GUI oltre alle derivazioni già dichiarate da `data_model.md` §13 | ⚠️ **il `.pbix` non è rigenerabile da una copia pulita**, ed è una conseguenza del principio V, non una violazione di questo. Vedi Complexity Tracking, seconda riga |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ ~5 ore, ed è già il prodotto della scomposizione della `008` decisa dalla regia il 2026-08-21 | ✅ regge — vedi «Budget e rischio». Il confine di sosta naturale è il punto di fermata 3, che spezza la feature in due sessioni di lunghezza simile |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde, **e nella dashboard dove il consumatore è l'utente finale** | ✅ sezione «Limiti Dichiarati» della spec, con l'elenco esplicito di quali limiti restano fuori dallo schermo | ⚠️ **la metà «nella dashboard» non è soddisfatta alla chiusura di questa feature**: è il deliverable della `008b`. Vedi Complexity Tracking, prima riga |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessun task di questo piano apre Power BI; i tre blocchi che vi entrano sono istruzioni eseguibili da una persona | ✅ invariato — ed è il principio che dà forma all'intera feature, non un vincolo che la sfiora |
| **VI. Coerenza Narrativa** | riconducibile a una domanda di business | ✅ tutte e tre: è la feature che le porta a schermo | ✅ invariato |

**Esito**: nessuna violazione non giustificata. Due voci in Complexity Tracking, entrambe consapevoli e nessuna delle due nuova.

**Un punto di attenzione che il gate non intercetta.** I gate della constitution sono scritti per feature che producono artefatti ispezionabili: «la pipeline è rieseguibile da zero», «ogni numero pubblicato è etichettato». Qui il numero è etichettato **a schermo**, e la verifica di quell'etichetta è una persona che guarda. Il gate passa, ma passa perché qualcuno lo dichiara — non perché qualcosa lo controlli. È la ragione per cui l'ordine dei blocchi di questo piano è esso stesso un presidio, e per cui il punto di fermata 3 non è negoziabile.

## Project Structure

### Documentation (this feature)

```text
specs/008a-dashboard-model-pages/
├── spec.md                          # specifica approvata: 9 decisioni F1-F9, 29 requisiti, 10 criteri
├── plan.md                          # questo file
├── research.md                      # Fase 0 — le nove decisioni in formato Decisione/Motivazione/Alternative
├── data-model.md                    # Fase 1 — il modello nel .pbix: 7 tabelle, 10 misure, 3 grane
├── quickstart.md                    # Fase 1 — le prove di verifica, e la sezione in cui l'esito viene scritto
├── contracts/
│   ├── page-contract.md             # ★ prodotto nel blocco A, NON in questa fase: è il punto di fermata 3
│   └── dashboard-contract.md        # Fase 1 — che cosa 008b e 010 possono presupporre
├── checklists/
│   └── requirements.md              # checklist di qualità, già verificata
├── review.md                        # revisione in contesto pulito — non ancora prodotto
└── tasks.md                         # Fase 2 — prodotto da /speckit.tasks, non da qui
```

**`contracts/page-contract.md` è dichiarato qui ma non prodotto qui, ed è deliberato.** La Fase 1 di `/speckit.plan` produce normalmente tutti i contratti; questo no, perché è l'oggetto del terzo punto di fermata. Scriverlo adesso significherebbe farlo approvare insieme al piano, cioè fondere due decisioni che la spec ha separato apposta: *come si lavora* (piano) e *che cosa si costruisce* (contratto). La differenza non è formale — il contratto ha bisogno di essere letto da solo, con l'attenzione che si dà a un disegno, non in coda a un documento di processo.

**Dove va l'esito della costruzione.** `FR-022` ammette `quickstart.md` o una sezione dedicata. Questo piano sceglie **una sezione in coda a `quickstart.md`**, invece di un file a sé: le prove manuali e il loro esito sono la stessa cosa vista prima e dopo, e separarli produrrebbe due documenti che si citano a vicenda senza che nessuno dei due si legga da solo.

### Source Code (repository root)

```text
README.md                            # MODIFICATO — riga di stato, deliverable, Setup/Struttura se cambia qualcosa

docs/kpi_measures.md                 # MODIFICATO SOLO SE un ritrovamento lo impone (F9, FR-024) — nota in loco,
                                     #   nessuna riscrittura di valori
```

**Nessun'altra riga.** Nessuno script nuovo o modificato, nessun artefatto nuovo in `reports/` o `data/`, nessun documento nuovo in `docs/`, nessuna riga in `DOCUMENTS` o `ARTIFACTS`, nessuna riga nella tabella di severità di `docs/convenzioni-marcatura.md`, nessuna riga nella sua tabella di provenienza — la grammatica dei marcatori non cambia perché questa feature non pubblica alcun documento sottoposto al controllo.

**`docs/roadmap.md` non è in questo elenco**, deliberatamente: appartiene alla regia (`CLAUDE.md`). La feature non lo tocca, nemmeno per registrare i due debiti della `004` che la riguardano — li riporta, e la registrazione è della regia.

**Il `.pbix` non è in questo elenco** perché non entra nel repository (`FR-029`).

**Structure Decision**: tutto ciò che questa feature produce e che sopravvive al merge vive sotto `specs/008a-dashboard-model-pages/`. È l'opposto della `007b`, che scriveva in `scripts/`, `reports/`, `docs/` e nel README: qui la cartella della feature non è materiale di lavorazione ma **l'unica traccia ispezionabile del deliverable**, ed è la ragione per cui il README deve puntarvi esplicitamente (`FR-026`) invece di limitarsi a nominare un file che nessuno può aprire.

## Ordine di lavoro e punti di sosta

Otto blocchi. Tre — ★1, ★2, ★3 — sono di Valerio e stanno dentro la GUI; il piano li nomina, ne dichiara l'ordine e ne raccoglie l'esito, ma non li esegue.

| # | Blocco | Vincolo di ordine | Esito |
|---|---|---|---|
| **A** | `contracts/page-contract.md`: quattro pagine, per ciascuna i KPI esposti, la visuale con la ragione contro la forma del dato, i filtri presenti, le interazioni **non** offerte e perché, la navigazione | dopo il piano e i task | contratto completo, nessun valore di KPI trascritto (`FR-003`) |
| **⏸** | **PUNTO DI FERMATA 3** — il contratto torna a Valerio per approvazione o correzione, **prima** che Power BI venga aperto | dopo A | contratto approvato e committato |
| **★1** | Valerio: apre il modello e verifica a occhio che `energy`, `valence`, `danceability` di `dim_track` stiano fra 0 e 1 (issue `#11`) | dopo ⏸ | esito dichiarato: difetto assente, oppure presente, corretto e registrato come ricomparsa |
| **★2** | Valerio: incolla le dieci misure, costruisce le quattro pagine e la navigazione secondo il contratto approvato | dopo ★1 — **mai prima**: costruire sopra una tipizzazione sbagliata è il costo che `E9` ha evitato alla `007b` | quattro pagine esistenti; scostamenti annotati mentre accadono, non ricostruiti a memoria |
| **★3** | Valerio: legge le due soglie del quadrante esposte come misure e le confronta con i valori pubblicati in `docs/kpi_measures.md` §7.1 (`F7`) | dentro ★2, dopo che le misure esistono | coincidenza — che chiude l'esclusione dichiarata in §11.1 — oppure divergenza, che è un ritrovamento |
| **B** | `quickstart.md`, sezione «Esito della costruzione»: quali pagine esistono, quali KPI espongono, gli scostamenti con la ragione, l'esito di ★1 e ★3, lo stato delle issue `#11` e `#18` | dopo ★2 e ★3 | esito completo; chi legge sa che cosa esiste senza aprire il file |
| **C** | note in loco su `docs/kpi_measures.md`, **solo se** un ritrovamento le impone (`FR-024`) | dopo B | zero note se nessun ritrovamento — ed è l'esito atteso, non un'omissione |
| **D** | `contracts/dashboard-contract.md` allineato all'esito reale: che cosa la `008b` e la `010` possono presupporre, che cosa resta a loro carico | dopo B | contratto di lettura coerente con ciò che esiste, non con ciò che era stato disegnato |
| **E** | revisione in contesto pulito su `page-contract.md` e sulla sezione di esito → `review.md`, committato **prima** di qualunque correzione (i quattro obblighi di `CLAUDE.md`) | dopo D | verbale esiste ed è committato |
| **F** | chiusura dei soli rilievi strettamente necessari; gli altri come issue con numero; stato dichiarato di `#11` e `#18`; README allineato; riesecuzione di `check_audit_coherence.py`; riporto finale | dopo E | feature conclusa |

**Il punto di massima leva è A, e non è un'opinione di questo piano.** È la stessa struttura che `E9` ha reso concreta nella `007b`: un difetto trovato prima della costruzione costa una rilettura, lo stesso difetto trovato dopo costa di rifare le pagine. La differenza qui è che nella `007b` il presidio era una **verifica** e trovava errori di fatto, mentre qui è un'**approvazione** e intercetta errori di disegno — che non sono verificabili da nessuno strumento, solo leggibili da una persona che non li ha scritti.

**Se la giornata si spezza, il confine di sosta è ⏸.** È il punto in cui il repository resta coerente per costruzione: esistono spec, piano, task e contratto approvato, e non esiste ancora nulla che possa contraddirli. Ogni altro confine cade in mezzo a ★2, dove metà delle pagine esistono e l'esito non è scrivibile.

**Un vincolo d'ordine che vale la pena rendere esplicito**: ★1 prima di ★2, sempre. Non è una precauzione formale — è l'unica ragione per cui la `007b` ha speso due ore in più invece che rifare le pagine di questa feature.

## Budget e rischio

| Blocco | Ore | Contenuto |
|---|---|---|
| A | 1,5 | il contratto di pagina: quattro pagine, visuali motivate contro la forma del dato, filtri, interazioni escluse, navigazione |
| ★1 | 0,1 | la lettura delle tre colonne di mood |
| ★2 | 1,9 | costruzione manuale: modello, dieci misure, quattro pagine, navigazione |
| ★3 | — | assorbito in ★2: le soglie sono già misure, la lettura è un'occhiata |
| B | 0,4 | l'esito, con gli scostamenti e la loro ragione |
| C | 0,1 | note in loco, se servono — zero se nessun ritrovamento |
| D | 0,2 | il contratto di lettura per `008b` e `010`, allineato all'esito |
| E | 0,6 | revisione in contesto pulito su due documenti brevi |
| F | 0,2 | chiusura dei rilievi necessari, issue, README, riporto |
| | **5,0** | |

**La costruzione manuale è dentro la stima, non fuori.** Nella `007b` il tempo di Valerio su `E9` era escluso, perché `E9` era una verifica su un deliverable già prodotto dagli script. Qui la costruzione **è** il deliverable: escluderla darebbe una stima di 3 ore per una feature che la roadmap valuta 5, e lo scostamento a consuntivo misurerebbe una convenzione contabile invece del lavoro.

**Il rischio maggiore è in A, ed è di disegno.** Un contratto che sceglie una visuale che non regge la forma del dato — 114 punti illeggibili, una graduatoria che non entra in pagina — produce uno scostamento in ★2 e, nel caso peggiore, obbliga a riaprire A dopo che le pagine esistono. È mitigato dal punto di fermata, che è precisamente l'unico presidio disponibile: nessuno script può leggere un disegno.

**Il secondo rischio è di ordine, non di contenuto**: che ★2 si scosti dal contratto e lo scostamento venga assorbito invece che dichiarato. Nessun controllo di questo repository può accorgersene — è la classe di difetto che `docs/convenzioni-marcatura.md` §8 chiama la categoria della menzogna, contro cui esiste solo la revisione. Il presidio operativo è annotare gli scostamenti **mentre accadono**, dentro ★2, invece di ricostruirli a memoria in B.

**Il terzo rischio è la ricomparsa del difetto di tipizzazione** (issue `#11`), e ha una probabilità che nessuno conosce: si è manifestato una volta su una materializzazione, e il `.pbix` non è versionato. Costa 0,1 ore controllarlo e costerebbe l'intera ★2 non controllarlo.

**Ciò che non è un rischio**: `check_audit_coherence.py`, che resta verde perché questa feature non tocca nulla di ciò che controlla — e il piano lo dice apertamente invece di rivendicare quel verde come una garanzia sul proprio deliverable.

## Complexity Tracking

> Due violazioni consapevoli, entrambe registrate come la constitution impone (sezione Governance, «Verifica di conformità»).

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **Principio IV**: alla chiusura di questa feature la dashboard **non** porta a schermo i limiti dichiarati, che il principio richiede «dove il consumatore è l'utente finale» | la `008` è stata scomposta dalla regia il 2026-08-21 proprio per rientrare nel principio III: nove ore superavano il limite di una giornata lavorativa. La metà narrativa — limiti a schermo, assunzione strutturale dei proxy, storytelling — è il deliverable dichiarato della `008b`, che segue immediatamente | portare i limiti a schermo qui significherebbe ricomporre `008a` e `008b` in una feature da ~9 ore, che il principio III vieta di avviare. La mitigazione è dichiarata e non implicita: il `.pbix` è **leggibile, non pubblicabile** (`F5`), non viene pubblicato su alcun workspace, e la `008b` è la feature successiva in roadmap — non un rinvio indefinito |
| **Principio II**: il `.pbix` non è rigenerabile da una copia pulita del repository | è la conseguenza diretta del principio V, che colloca la GUI di Power BI Desktop fuori dall'automazione, e della scelta di non versionare un file che incorpora i dati. Vale dalla `005` e non è introdotta qui | l'alternativa sarebbe versionare il `.pbix`, che porterebbe dentro il repository copie dei dati che `data/processed/` tiene fuori per scelta, oppure generarlo da uno script, che significa pilotare la GUI. La mitigazione è che tutto ciò che nel `.pbix` è esprimibile come testo — schema, mapping, misure DAX, ora anche il disegno delle pagine — **è** testo versionato, che è esattamente ciò che il principio V prescrive di fare |
