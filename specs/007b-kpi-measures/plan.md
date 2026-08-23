# Implementation Plan: Misure DAX e documento dei KPI

**Branch**: `007b-kpi-measures` | **Date**: 2026-08-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/007b-kpi-measures/spec.md`

## Summary

La feature produce **un artefatto nuovo di calcolo** (`scripts/build_kpi_measures.py` → `reports/kpi_measures.json`), **un documento pubblicato** (`docs/kpi_measures.md`, otto KPI) e **quattro mutazioni** a materiale già mergiato: due decisioni nuove e due chiusure di vincoli aperti in `docs/kpi_operators.md` (D10, D11, nota in loco §11, chiusura §12), una nota in loco su `business_case.md` §3, l'estensione di `scripts/check_audit_coherence.py` (quinto artefatto, settimo documento) e la riga corrispondente in `docs/convenzioni-marcatura.md`.

A differenza della `007a` — che non produceva alcun dato, solo un documento di regole — questa feature è più vicina nella forma alla `004`: uno script deterministico che legge input già versionati e scrive un artefatto JSON con lo stesso schema `values`/`catalogs`/`conventions`/`sources`, riusando esplicitamente le convenzioni di `scripts/build_bq3_scenarios.py` (`Decimal`, `ROUND_HALF_UP` esplicito, nessuna lettura dell'orologio, formattazione non dipendente dal locale, impronta `sha256` degli input). La differenza con la `004` è che qui gli input sono cinque file già prodotti da quattro feature diverse (`data/processed/*.csv`, `data/curated/dim_category_mood.json`), non un unico file curato a mano.

**Il lavoro analitico è già chiuso in spec.** Le cinque decisioni nuove (E2-E6) e le tre verifiche (E1 come scelta di processo, E7, E8) sono argomentate per intero in [spec.md](./spec.md); questo piano non le riapre, le traduce in una sequenza di blocchi con un ordine di dipendenza dichiarato. L'unico passo che questo piano non può eseguire è **E9** — il confronto manuale contro il motore Power BI reale, che resta a carico di Valerio, dentro il perimetro della feature ma fuori da ciò che uno script produce.

**Il rischio principale è duplice, non singolo come nella `007a`.** Il primo è di trascrizione, come in ogni feature che ancora numeri contro artefatti esistenti. Il secondo — nuovo rispetto alla `007a` — è che lo script, applicando correttamente le regole scritte, riproduca comunque un comportamento diverso da quello che il motore DAX produrrebbe su un contesto di filtro o una propagazione di relazione non identica: è il rischio che E1 dichiara esplicitamente e che solo E9 può chiudere, non un controllo automatico di questo repository.

## Technical Context

**Linguaggio/Versione**: Python 3, solo libreria standard (`csv`, `json`, `hashlib`, `decimal`, `pathlib`). Nessuna dipendenza da `pandas` — non disponibile nell'ambiente di sviluppo di questa sessione, ed è comunque coerente con `scripts/build_bq3_scenarios.py` e con tutti gli script precedenti del progetto, nessuno dei quali dipende da librerie terze

**Dipendenze primarie**: nessuna nuova. `decimal.Decimal` con `ROUND_HALF_UP` esplicito per ogni arrotondamento (mai `ROUND_HALF_EVEN`, la modalità predefinita); nessun uso di `float` in nessun passaggio dell'aritmetica (E1, E5)

**Storage**: `reports/kpi_measures.json` (nuovo, **quinto** artefatto in `ARTIFACTS` — oggi `(PROFILE, CLEANING, SCENARIOS, MOOD)`, quattro membri). `reports/kpi_engine_check.json` (nuovo, **sesto** artefatto — rilievo bloccante della revisione di regia sul piano: l'esito di E9 non ha altrimenti alcuna ancora, perché `reports/kpi_measures.json` è generato dallo script ed è deterministico per FR-003, quindi non può contenere una lettura umana; questo secondo artefatto è **curato a mano, mai scritto da uno script**, sul precedente di `data/benchmarks/bq3_tier_upgrade.json`, e congela le otto letture del motore, la data, il riferimento allo stato del `.pbix`, l'esito del confronto — FR-029a). `docs/kpi_measures.md` (nuovo, **settimo** documento in `DOCUMENTS` — oggi sei membri, di cui `docs/data_audit.md` unico a severità non stretta — quindi **sesto in severità stretta**). Nessun nuovo artefatto sotto `data/`: lo script legge, non congela, alcun dato assegnato a mano

**Testing**: verifica per esecuzione e per ispezione secondo [quickstart.md](./quickstart.md) — determinismo dello script (due esecuzioni, diff vuoto), presenza e ancoraggio di ciascuno degli otto valori, l'invarianza del numeratore della North Star dichiarata come verificata o come ritrovamento, la quota di zeri e l'avvertimento sui 7 segmenti `is_high_zero_genre`, i tre vincoli di §12 e le issue `#7`/`#8` chiusi con riferimento esplicito, esito verde di `check_audit_coherence.py` su sette documenti e sei artefatti (cinque dopo il blocco C, sei dopo F0), la nota in loco su `business_case.md` §3, l'esito di E9 dichiarato per ciascuna misura, README allineato

**Piattaforma target**: qualunque sistema con Python 3. Nessuna dipendenza dal locale nella formattazione di presentazione (stessa `display_of()` di `build_bq3_scenarios.py`: virgola decimale esplicita, mai una funzione che dipende dalle impostazioni regionali della macchina — vincolo ereditato da un difetto reale della `003`)

**Tipo di progetto**: uno script di derivazione, un artefatto dati generato, un documento pubblicato, due mutazioni "nota in loco" a documenti già mergiati, un'estensione di script esistente, due aggiornamenti di documentazione infrastrutturale (`convenzioni-marcatura.md`, `README.md`). Nessuna applicazione, nessun servizio

**Obiettivi di performance**: nessuno dichiarato dalla spec. Il volume più grande che lo script attraversa è 113.550 righe di `spotify_track_genre.csv` (coppie traccia-segmento) e 89.741 righe di tracce deduplicate: un'iterazione con `csv.DictReader` e aggregazione in dizionari resta nell'ordine dei secondi, non è un vincolo di progettazione

**Vincoli**: determinismo totale (FR-001, FR-003 — due esecuzioni producono lo stesso file byte per byte); aritmetica esclusivamente in `Decimal` (FR-001); arresto esplicito senza scrivere alcun file su un'aggregazione vuota o un identificativo di categoria/segmento assente dai cataloghi attesi (FR-004, sullo stesso principio del `guard_rate` di `build_bq3_scenarios.py` — "meglio nessun file che un file parziale"); nessuna promozione di confidenza (Provenienza e Confidenza della spec); ~5 ore di lavoro effettivo, revisione inclusa, tempo di Valerio su E9 escluso dal conteggio (principio III)

**Scala/Ambito**: 8 KPI, di cui 3 pubblicano un valore per ciascuno dei 114 segmenti (`BQ2-K1`, `BQ2-K2`, `BQ2-K3`), 1 pubblica un conteggio per ciascuna delle 42 categorie come operatore di supporto (`BQ1-K1`/C1), 2 sono citazioni senza ricalcolo (`BQ3-K1`, `BQ3-K2`); 1 script nuovo; 2 artefatti JSON nuovi (`reports/kpi_measures.json` generato, `reports/kpi_engine_check.json` curato a mano); 1 documento pubblicato nuovo; 2 decisioni nuove in `kpi_operators.md` (D10, D11); 2 correzioni "nota in loco" a documenti già mergiati; 1 estensione di `check_audit_coherence.py` (tre righe: due in `ARTIFACTS`, una in `DOCUMENTS`); righe nuove in `convenzioni-marcatura.md`; 1 passo manuale non scriptabile (E9, 8 confronti)

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni valore dichiara fonte e confidenza | ✅ tabella compilata nella spec, ereditata per intero da `business_case.md` §5.4 e `kpi_operators.md` §11, nessuna promozione | ✅ invariato — E9 cambia lo **statuto epistemico** di un valore (calcolato → verificato), mai la sua confidenza dichiarata, che è un asse distinto per costruzione della constitution |
| **II. Riproducibilità** | trasformazioni come codice versionato | ✅ script deterministico sullo schema di `build_bq3_scenarios.py`, legge solo file già versionati o rigenerabili da `scripts/build_datasets.py` | ✅ US1 lo rende verificabile end-to-end: `data/raw/` → `build_datasets.py` → `build_kpi_measures.py`, non solo il secondo passo isolato. `reports/kpi_engine_check.json` non è una trasformazione sui dati — è un verbale di lettura (FR-029a), curato a mano sullo stesso precedente ammesso di `data/benchmarks/bq3_tier_upgrade.json`, e non introduce alcuna eccezione nuova al principio |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ stima 5 ore, secondo punto di stop dichiarato (dopo `/speckit.tasks`), due condizioni esplicite di fermata (E7 che riapre l'operatore di `BQ1-K1`, E9 che richiede di correggere lo script) | ✅ regge — vedi "Budget e rischio" |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde | ✅ sezione "Limiti Dichiarati" della spec, incluso il limite temporaneo di E9 (chiuso entro il merge, non oltre) | ✅ invariato |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessuno script apre Power BI o Tableau; E9 è un passo manuale di Valerio, non automatizzato — la nota di perimetro della regia lo colloca dentro il progetto e fuori dall'automazione, non fuori dal progetto | ✅ invariato — è il punto che la revisione della regia ha corretto esplicitamente rispetto alla prima stesura della spec |
| **VI. Coerenza Narrativa** | riconducibile a una domanda di business | ✅ tutte e tre — BQ1, BQ2, BQ3 — è la prima feature che pubblica un valore per tutti e otto i KPI del framework | ✅ invariato |

**Esito**: nessuna violazione. La tabella "Complexity Tracking" resta vuota.

**Un punto di attenzione che il gate non intercetta**: E9 verifica che il DAX trascritto e lo script producano lo stesso **numero** su otto misure, non che siano equivalenti su ogni possibile contesto di filtro che il modello potrebbe incontrare in una dashboard futura. Una coincidenza su questi otto valori riduce il rischio dichiarato da E1, non lo azzera per costruzione — è lo stesso tipo di limite che la `007a` aveva dichiarato per la propria revisione ("un'ancora tecnicamente valida può sostenere un ragionamento sbagliato"): qui, un valore che coincide oggi non garantisce che coincida sotto un filtro che nessuna delle 114+42+8 grandezze calcolate in questa feature esercita.

## Project Structure

### Documentation (this feature)

```text
specs/007b-kpi-measures/
├── spec.md                         # specifica approvata, 31 requisiti, 9 decisioni/verifiche (E1-E9)
├── plan.md                         # questo file
├── research.md                     # Fase 0 — le nove decisioni/verifiche in formato Decisione/Motivazione
├── data-model.md                   # Fase 1 — schema di reports/kpi_measures.json e forma di docs/kpi_measures.md
├── quickstart.md                   # Fase 1 — le prove di verifica, in ordine
├── contracts/
│   └── kpi-measures-contract.md    # Fase 1 — il contratto che 008a/008b leggeranno
├── checklists/
│   └── requirements.md             # checklist di qualità, già verificata, con nota della revisione di regia
├── review.md                       # revisione in contesto pulito — non ancora prodotto
└── tasks.md                        # Fase 2 — prodotto da /speckit.tasks, non da qui
```

### Source Code (repository root)

```text
scripts/
├── build_kpi_measures.py           # NUOVO — le otto misure, sullo schema di build_bq3_scenarios.py
└── check_audit_coherence.py        # MODIFICATO — una riga in ARTIFACTS, una in DOCUMENTS

reports/
├── kpi_measures.json                # NUOVO — quinto artefatto, generato dallo script
└── kpi_engine_check.json            # NUOVO — sesto artefatto, curato a mano (E9, FR-029a), mai scritto da uno script

docs/
├── kpi_measures.md                 # NUOVO — settimo documento, sesto in severità stretta
├── kpi_operators.md                # MODIFICATO — D10, D11, nota in loco §11 (issue #8), chiusura §12
├── business_case.md                # MODIFICATO — nota in loco §3 (US6, rilievo R11 della revisione 001)
└── convenzioni-marcatura.md        # MODIFICATO — tabella di severità, tabella di provenienza

README.md                           # MODIFICATO — tabella di stato, deliverable, conteggio documenti, Setup, Struttura
```

**`docs/roadmap.md` non è in questo elenco**, deliberatamente: appartiene alla regia (FR-028, CLAUDE.md). La feature non lo tocca.

**Le issue GitHub `#7` e `#8` non sono un file**, ma sono un deliverable di processo: questa feature propone la loro chiusura con riferimento al commit che chiude ciascuna, l'esecuzione (chiusura effettiva su GitHub) resta a Valerio (FR-027).

**Structure Decision**: lo script entra in `scripts/` accanto a `build_bq3_scenarios.py`, di cui riusa lo schema di artefatto e le convenzioni di arrotondamento; il documento entra in `docs/` accanto ai sei che già pubblicano misure o regole, sotto lo stesso regime di severità stretta introdotto dalla `005` ed esteso da ogni feature successiva. Nessuna struttura nuova sotto `data/`: questa feature non cura né assegna alcun valore, calcola soltanto — la stessa distinzione che il piano della `007a` aveva tracciato rispetto alla `006`, qui vista dal lato opposto.

## Ordine di lavoro e punti di sosta

Nove blocchi. A differenza della `007a` (quattro blocchi, un solo vincolo d'ordine), qui l'ordine è più fitto perché uno dei passi — E9 — è esterno allo script e deve leggere un documento già scritto prima di produrre il proprio esito, che a sua volta rientra nel documento prima che la revisione lo veda.

| # | Blocco | Vincolo di ordine | Esito |
|---|---|---|---|
| **A** | `scripts/build_kpi_measures.py`: le otto misure, E2/D10 (convenzione di mediana) applicata ovunque una mediana compare, E3 (doppia variante sulla durata degenere), E4 (quota film), E7 (conteggio diretto e confronto con 375) | nessuno | `reports/kpi_measures.json` scritto; due esecuzioni consecutive producono un file identico |
| **B** | `docs/kpi_measures.md`: otto sezioni, DAX trascritto per ciascuna, provenienza, confidenza, limiti; ogni misura porta lo stato iniziale «calcolato da script, verifica contro il motore in corso» | dopo A | documento completo, ogni numerale ancorato o marcato non-misurato |
| **C** | `scripts/check_audit_coherence.py` (settimo documento, quinto artefatto) e `docs/convenzioni-marcatura.md` (due righe nuove) | dopo B | `python3 scripts/check_audit_coherence.py` verde su sette documenti e cinque artefatti |
| **D** | `docs/kpi_operators.md`: **D10** (convenzione di mediana, chiude issue `#7`), **D11** (durata degenere, con riferimento al valore comparativo di A), nota in loco §11 (chiude issue `#8`), chiusura di §12 per E4/E5 | dopo A (D11 cita il valore comparativo che solo A produce) | §12 senza vincoli aperti; issue `#7`/`#8` pronte per la chiusura formale su GitHub |
| **E** | `business_case.md` §3: nota in loco (US6) | indipendente — nessuna dipendenza da A-D | §3 corretto, testo originale intatto |
| **★** | **E9** — Valerio, fuori da questa sessione: incolla il DAX di ciascuna delle otto sezioni di B nel `.pbix` già materializzato, legge gli otto valori, confronta con `reports/kpi_measures.json` | dopo B | otto esiti, ciascuno coincidenza o divergenza |
| **F0** | congela `reports/kpi_engine_check.json` (curato a mano, mai da script — FR-029a) con gli otto esiti di ★, la data, il riferimento allo stato del `.pbix`; aggiunge il sesto membro a `ARTIFACTS` e la riga in `docs/convenzioni-marcatura.md`; rilievo bloccante della revisione di regia sul piano — senza questo blocco l'esito di E9 non ha ancora e il controllo lo ferma | dopo ★ | `python3 scripts/check_audit_coherence.py` verde su sei artefatti |
| **F** | `docs/kpi_measures.md` aggiornato: ciascuna delle otto misure dichiara l'esito reale di ★, ancorato a `reports/kpi_engine_check.json` (F0) — «verificato contro il motore reale» o nota in loco con i due numeri e la causa | dopo F0 | il documento raggiunge la propria forma finale, pre-revisione |
| **G** | revisione in contesto pulito di `docs/kpi_measures.md` → `specs/007b-kpi-measures/review.md`, committato prima di qualunque correzione (i quattro obblighi di CLAUDE.md) | dopo F | verbale esiste ed è committato |
| **H** | correzioni strettamente necessarie ai rilievi del verbale; issue non necessarie rinviate con numero; proposta di chiusura `#7`/`#8`; README allineato; **riesecuzione di `check_audit_coherence.py`** — le correzioni possono toccare numeri e ancore, e l'ultimo verde precedente è a F0, cinque blocchi prima; riporto finale | dopo G | feature conclusa, controllo verde riconfermato dopo le correzioni |

**Il punto di massima leva è ★, non un blocco di scrittura.** In ogni feature precedente il rischio principale era di trascrizione o di analisi; qui è l'unico blocco che nessuno script di questo repository può eseguire, ed è anche l'unico il cui esito può obbligare a riaprire A (se la divergenza rivela un errore nello script) invece che solo B o D. È la ragione per cui F segue ★ invece di essere assorbito dentro B: B scrive il documento nella sua forma "calcolata", F lo porta alla forma "verificata o con ritrovamento dichiarato", e le due cose non devono essere confuse in un solo passaggio.

**Se la giornata si spezza, il confine di sosta migliore è la fine di D/E.** A quel punto lo script esiste, il documento esiste nella sua forma calcolata, il controllo meccanico passa, e i quattro debiti ereditati di `kpi_operators.md`/`business_case.md` sono chiusi. Ciò che resta — ★, F, G, H — dipende da un'azione di Valerio fuori da questa sessione e dalla revisione in contesto pulito: non è lavoro che si comprime per restare dentro un'unica sessione, è lavoro che aspetta un input esterno per definizione.

## Budget e rischio

| Blocco | Ore | Contenuto |
|---|---|---|
| A | 2,0 | lo script: otto misure, tre varianti aggiuntive (E3, E4, E7), guardia sugli insiemi vuoti (FR-004), schema `values`/`catalogs`/`conventions`/`sources` |
| B | 0,8 | scrittura del documento: otto sezioni, DAX trascritto, provenienza e limiti per KPI |
| C | 0,3 | estensione dello script (due righe, nessuna funzione nuova — più semplice della `006`, che introduceva un presidio di tassonomia; equivalente alla `007a`), righe di provenienza |
| D | 0,4 | D10, D11, nota in loco §11, chiusura §12 |
| E | 0,1 | nota in loco su `business_case.md` §3 |
| ★ | — | tempo di Valerio, fuori dalla stima (stessa esclusione della materializzazione del `.pbix`, `docs/roadmap.md`) |
| F0 | 0,1 | congelare `reports/kpi_engine_check.json`, estendere `ARTIFACTS` e `convenzioni-marcatura.md` — assorbito nel budget già previsto per F, non aggiunto |
| F | 0,1 | incorporare l'esito di ★ nel documento, per ciascuna delle otto misure, ancorato a F0 |
| G | 0,9 | revisione in contesto pulito, sui quattro obblighi di CLAUDE.md |
| H | 0,3 | correzioni strettamente necessarie, README, proposta di chiusura issue |
| | **5,0** | |

**Il rischio maggiore è in A, ed è di traduzione da regola a codice, non di analisi.** Le otto formule sono già fissate da `kpi_operators.md`; il lavoro di A è tradurle senza introdurre una lettura diversa da quella scritta — per esempio confondere il denominatore di `music_adjacent_catalog_share` (8.807 titoli distinti) con il totale delle assegnazioni (19.323), un errore che `kpi_operators.md` §2.1 nomina esplicitamente come "la trappola di questo KPI".

**Il secondo rischio è ★, ed è strutturalmente diverso da ogni rischio delle feature precedenti**: non è un rischio di scrittura, è un rischio di **fatto** — che il motore Power BI valuti il DAX trascritto in modo diverso da come lo script itera sulle stesse righe. Nessuna quantità di rilettura del codice lo riduce; solo l'esecuzione di ★ lo chiude, in un senso o nell'altro. Se ★ rivela una divergenza che richiede di correggere A, la sessione si ferma e lo riporta come il ritrovamento di priorità più alta (FR-031), invece di assorbirlo in silenzio dentro F.

**Se A rivelasse un lavoro più grande della stima** — in particolare se l'esecuzione di E7 (il conteggio diretto su `Music & Musicals`) non coincidesse con 375 in un modo che mette in dubbio l'operatore stesso di `BQ1-K1`, non solo il numero di origine — la sessione si ferma al secondo punto di stop e lo riporta, come la spec dichiara esplicitamente in "Stima e scomposizione".

**Ciò che non è un rischio**: C ed E, entrambi meccanici; G, che è la revisione standard del progetto con il proprio costo consueto.
