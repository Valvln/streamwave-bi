# Implementation Plan: Operatori delle misure

**Branch**: `007a-kpi-operators` | **Date**: 2026-08-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/007a-kpi-operators/spec.md`

## Summary

La feature produce **un solo artefatto nuovo**: `docs/kpi_operators.md`, un documento di prosa che definisce, per ciascuno degli otto KPI del business case, l'operatore con cui verrà calcolato. Nessun dato nuovo, nessuno script di derivazione, nessun valore numerico dei KPI — la differenza strutturale con la `006`, che congelava 126 celle: qui non esiste alcun artefatto dati da costruire, perché le nove decisioni (D1-D9) sono di analisi, non di assegnazione, e non richiedono né una proposta di modello né una verifica indipendente della proposta.

Il lavoro reale della feature è già stato fatto nella spec: le nove decisioni sono argomentate per intero, comprese le quattro che il prompt di consegna nomina come più esposte (D1-D4) e la coppia chiusa dalla revisione della regia (D9, che ora copre sia l'operatore mancante della condizione C1 della North Star sia l'invariante che rende valido sul dato trasformato il numeratore 375 letto sull'origine). Il piano non aggiunge decisioni: **traspone** quelle già prese in un documento pubblicato, verificabile meccanicamente, e le due modifiche che lo rendono coerente con il resto del repository — l'estensione di `scripts/check_audit_coherence.py` e la riga di provenienza in `docs/convenzioni-marcatura.md`.

**Il rischio principale non è tecnico, è di trascrizione.** Ogni numero che compare in `docs/kpi_operators.md` come esempio (375, 8.807, 0,5 punti percentuali, 114 segmenti) deve portare l'ancora esatta verso l'identificativo già esistente citato in spec — un'ancora copiata a mano sbagliata degrada in silenzio a marcatore di non-misurato (§4 di `convenzioni-marcatura.md`) e il controllo lo rileva solo se la severità stretta è già attiva sul documento.

## Technical Context

**Linguaggio/Versione**: Python 3 stdlib (`re`, `json`), per l'estensione di `scripts/check_audit_coherence.py`. Coerente con 002-006, nessuna dipendenza nuova. Il deliverable principale è prosa Markdown, non codice

**Dipendenze primarie**: nessuna. Nessuna invocazione di modello, nessuna pipeline, nessuna GUI

**Storage**: `docs/kpi_operators.md` (nuovo, sesto documento sotto `DOCUMENTS`, severità stretta dalla nascita). Nessun nuovo artefatto sotto `data/`: le nove decisioni non producono un artefatto congelato — a differenza di `dim_category_mood.json` della `006` — perché nessuna di esse assegna un valore che nessuna fonte osserva. Ogni numero citato come esempio ancora contro `reports/data_profile.json`, `reports/cleaning_report.json` o `data/curated/dim_category_mood.json`, già membri di `ARTIFACTS`

**Testing**: verifica per esecuzione e per ispezione secondo [quickstart.md](./quickstart.md) — dieci prove: presenza di un operatore per ciascuno degli otto KPI, assenza di valori numerici dei KPI, le quattro decisioni più esposte argomentate con opzione scartata e ragione, l'operatore di C1 distinto da quello della quota, l'invariante di D9.1 verificabile sui tre identificativi che cita, nessuna confidenza alterata rispetto a `business_case.md` §5.4, la soglia di D6 limitata al confronto delle quote di zeri, esito verde di `check_audit_coherence.py` in severità stretta su sei documenti, registrazione in `convenzioni-marcatura.md`, README allineato

**Piattaforma target**: qualunque sistema con Python 3. Nessuna dipendenza dal locale — il documento non introduce valori decimali propri, solo citazioni di valori già formattati altrove

**Tipo di progetto**: un documento curato a mano, un'estensione di uno script esistente, due aggiornamenti di documentazione (`README.md`, `docs/convenzioni-marcatura.md`). Nessuna applicazione, nessun servizio, nessuna pipeline, nessun artefatto dati

**Obiettivi di performance**: nessuno. Il controllo di coerenza scandisce un documento in più, non un volume di dati

**Vincoli**: nessun valore numerico dei KPI nel documento (FR-019); severità stretta dalla nascita, sesto documento (FR-020); ogni numerale porta ancora o marcatore di non-misurato (FR-021); nessuna alterazione della confidenza già fissata da `business_case.md` §5.4 (FR-015); la soglia di 0,5 punti percentuali resta limitata al confronto delle quote di zeri per genere (FR-010, corretto dalla revisione della regia); ~4 ore di lavoro effettivo, revisione inclusa (principio III)

**Scala/Ambito**: 8 operatori, 9 decisioni (di cui 3 articolate in sotto-decisioni: D9.1-D9.3), 28 requisiti, 7 criteri di successo, 1 estensione di script (una riga in `DOCUMENTS`, nessuna nuova funzione), 1 riga nuova nella tabella di provenienza di `convenzioni-marcatura.md`, 0 nuovi artefatti sotto `data/`

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni valore dichiara fonte e confidenza | ✅ tabella compilata nella spec: eredita per intero la classificazione di `business_case.md` §5.4, nessuna promozione | ✅ diventa meccanico: FR-015 vieta esplicitamente ogni operatore da alterare la confidenza; il controllo di coerenza verifica solo le ancore, la revisione in contesto pulito verifica che nessuna prosa la alteri in sostanza |
| **II. Riproducibilità** | trasformazioni come codice versionato | ✅ non c'è trasformazione: questa feature non genera alcun dato, definisce solo l'operatore che `007b` implementerà come misura DAX | ✅ invariato — nessun dato prodotto, nessuna pipeline toccata |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ stima 4 ore, terzo punto di stop specifico dichiarato (le quattro decisioni più esposte, già chiuse in spec) | ✅ regge — vedi "Budget e rischio". La spec dichiara esplicitamente di non proporre una scomposizione in due sotto-feature, perché le nove decisioni sono interdipendenti |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde | ✅ 7 voci in "Limiti Dichiarati", inclusi i due limiti strutturali introdotti dalle decisioni stesse (D1: stima per eccesso; D2: distanza non interpretabile in assoluto) | ✅ invariato |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessuna GUI, nessuna interazione con Power BI o Tableau | ✅ invariato |
| **VI. Coerenza Narrativa** | riconducibile a una domanda di business | ✅ tutte e tre — BQ1, BQ2, BQ3 — dichiarato come fatto insolito nella spec, con BQ3 senza operatori nuovi | ✅ invariato |

**Esito**: nessuna violazione. La tabella "Complexity Tracking" resta vuota.

**Un punto di attenzione che il gate non intercetta**: la severità stretta di FR-020 verifica che ogni numerale porti un'ancora o il marcatore di non-misurato, non che l'**argomentazione** intorno a un'ancora sia corretta. Un'ancora tecnicamente valida può comunque sostenere un ragionamento sbagliato — è esattamente la classe di difetto che la revisione della regia ha appena trovato in D9 (l'ancora di 375 esisteva, ma nessun operatore dichiarava su quale dato si potesse usare). Contro questo esiste solo la revisione in contesto pulito, non il controllo automatico: lo stesso limite che `docs/convenzioni-marcatura.md` §8 dichiara per ogni documento del progetto.

## Project Structure

### Documentation (this feature)

```text
specs/007a-kpi-operators/
├── spec.md                    # specifica approvata, 28 requisiti, 9 decisioni (D1-D9, D9 in tre parti)
├── plan.md                    # questo file
├── research.md                # Fase 0 — ritrovamenti e decisioni tecniche residue
├── data-model.md              # Fase 1 — forma del documento pubblicato, non di un dataset
├── quickstart.md              # Fase 1 — le dieci prove di verifica, in ordine
├── contracts/
│   └── kpi-operators-contract.md   # Fase 1 — il contratto che la 007b leggerà
├── checklists/
│   └── requirements.md        # checklist di qualità, già verificata
├── review.md                  # revisione in contesto pulito — non ancora prodotto
└── tasks.md                   # Fase 2 — prodotto da /speckit.tasks, non da qui
```

### Source Code (repository root)

```text
docs/
├── kpi_operators.md               # NUOVO — deliverable unico, sesto documento sotto DOCUMENTS, severità stretta dalla nascita
└── convenzioni-marcatura.md       # MODIFICATO — §5 (tabella di severità), Provenienza (nuova riga)

scripts/
└── check_audit_coherence.py       # MODIFICATO — una riga in DOCUMENTS; nessuna modifica ad ARTIFACTS, nessun nuovo artefatto dati

README.md                          # MODIFICATO — tabella di stato, deliverable, "I cinque documenti" → sei, Setup passo 5, Struttura
```

**`docs/roadmap.md` non è in questo elenco**, deliberatamente: è artefatto di governance e appartiene alla regia (`CLAUDE.md`). La feature non lo tocca (FR-026).

**Nessuna cartella nuova sotto `data/`.** È la differenza principale con la `006`: quella feature curava un artefatto che nessuna fonte osservava (`data/curated/`); questa non cura alcun valore — argomenta come otto KPI già definiti a livello concettuale in `business_case.md` si tradurranno in formule, leggendo esclusivamente tabelle e identificativi che le feature precedenti hanno già versionato.

**Structure Decision**: nessuna struttura nuova. Il documento entra in `docs/` accanto ai cinque che già pubblicano misure, sotto lo stesso regime di severità stretta di `docs/data_model.md` — il precedente diretto per un documento senza artefatto proprio le cui ancore risolvono contro gli artefatti delle feature precedenti.

## Ordine di lavoro e punti di sosta

Quattro blocchi, vincolati dal terzo punto di stop che il prompt di consegna impone esplicitamente a questa feature.

| # | Blocco | Vincolo di ordine | Esito |
|---|---|---|---|
| **A** | le nove decisioni (D1-D9), argomentate con opzioni scartate e ragioni | nessuno — è il lavoro già chiuso in spec, verificato dalla revisione della regia | spec approvata, tre rilievi bloccanti chiusi (B1, B2, B3) |
| **★** | **terzo punto di stop**: le quattro decisioni più esposte (D1-D4) sono riportate in forma compatta, con la propria ragione, prima di scrivere `docs/kpi_operators.md` | dopo A, prima di B | è il punto di massima leva della feature (prompt di consegna): un operatore sbagliato su queste quattro produce tutti i valori sbagliati di `BQ1-K3`, `BQ2-K2`, `BQ2-K3` — le tre condizioni della North Star ne dipendono per intero |
| **B** | scrittura di `docs/kpi_operators.md`: otto operatori, nove decisioni trasposte dal documento tecnico della spec a un documento leggibile in sequenza per KPI | dopo ★ | il documento esiste, ogni numerale ancorato o marcato non-misurato |
| **C** | estensione di `scripts/check_audit_coherence.py` (sesto documento in `DOCUMENTS`, severità stretta), riga in `docs/convenzioni-marcatura.md` | dopo B | `python3 scripts/check_audit_coherence.py` passa in severità stretta su sei documenti |
| **D** | revisione in contesto pulito del documento pubblicato, chiusura dei suoi rilievi, README | dopo C | verbale committato prima delle correzioni; README allineato; feature conclusa |

**★ è già stato eseguito nella sostanza**: la spec approvata contiene D1-D4 per esteso, con opzione scartata e ragione per ciascuna, e il riporto in forma compatta è nel messaggio che ha accompagnato l'apertura della spec alla regia. Il blocco resta comunque un task esplicito in `tasks.md`, perché la spec può ancora cambiare in fase di scomposizione dei task — è la stessa cautela che la `006` ha applicato al proprio punto di fermata.

**Il confine di sosta migliore, se la giornata si spezza, è la fine di B.** Dopo B il documento esiste per intero e ogni sua affermazione è verificabile a lettura; C e D sono verifica meccanica e revisione, non ulteriore analisi — uno stato che non lascia nulla a metà, sullo stesso criterio già adottato dalla `004` e dalla `006`.

## Budget e rischio

| Blocco | Ore | Contenuto |
|---|---|---|
| A | — | già chiuso: costo assorbito nella scrittura e revisione della spec, incluse le correzioni B1-B3 |
| ★ | 0,2 | riporto compatto delle quattro decisioni più esposte, verifica che nulla sia cambiato dalla spec approvata |
| B | 1,5 | scrittura del documento: otto sezioni per KPI, nove decisioni trasposte, ogni numerale ancorato |
| C | 0,6 | estensione dello script (una riga in `DOCUMENTS`, nessuna nuova funzione — più semplice della `006`, che aggiungeva anche un membro ad `ARTIFACTS` e una guardia di copertura nuova), riga di provenienza |
| D | 1,7 | revisione in contesto pulito, chiusura dei rilievi, README |
| | **4,0** | |

**Il rischio principale è in B, ed è di trascrizione, non di analisi.** Le nove decisioni sono già argomentate e verificate dalla regia; il lavoro di B è riorganizzarle per KPI e ricopiare correttamente ogni ancora citata come esempio. Un'ancora copiata male (per esempio `CL.NF.titles.rows.after` scritto senza il punto che separa `titles` da `rows`) degrada in silenzio a marcatore di non-misurato invece di fallire in modo visibile — è il rischio che `convenzioni-marcatura.md` §4 dichiara esplicitamente come costato un difetto reale sulla `003`.

**Il secondo rischio è C, per la ragione opposta della `006`.** Lì l'estensione dello script era il blocco più costoso del piano (guardia di copertura nuova, quarto artefatto). Qui è deliberatamente il più semplice: una riga sola in `DOCUMENTS`, nessuna funzione nuova, perché questa feature non introduce alcun artefatto dati che richieda una guardia di coerenza propria. Il rischio non è la complessità ma la tentazione di aggiungerne — l'ambito di questa feature esclude esplicitamente la materializzazione e qualunque calcolo, e C deve restare quello che è: una riga.

**Se B rivelasse un lavoro più grande di quanto la stima assorbe**, il taglio non è da inventare: la spec dichiara esplicitamente di non proporne uno, perché le nove decisioni sono interdipendenti (`BQ2-K3` compone `BQ2-K1` e `BQ2-K2`). In quel caso la feature si ferma e riporta, come il prompt di consegna prescrive, invece di comprimere l'argomentazione o di scomporre a metà lavoro.

**Ciò che non è un rischio**: A, già chiuso, e D, che è la revisione standard del progetto con il suo costo consueto.
