# Implementation Plan: Synthetic Business Metrics

**Branch**: `004-synthetic-business-metrics` | **Date**: 2026-08-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-synthetic-business-metrics/spec.md`

## Summary

La feature produce **quattro artefatti e una modifica**: un file di parametri curato a mano e versionato, che congela il benchmark con la sua citazione; una derivazione deterministica che ne ricava sei valori; un artefatto di quei valori, versionato ed entrante nello spazio dei nomi della marcatura; un documento che dichiara metodo e limiti. La modifica è al controllo di coerenza e alla fonte unica della grammatica, che devono conoscere il terzo artefatto e il terzo documento.

**Ciò che governa l'intero piano è un'inversione di ordine.** In ogni feature precedente il codice viene prima e i numeri dopo. Qui no: FR-011a impone che i due fattori della banda siano fissati **prima** che la ricognizione sul benchmark cominci, perché sono l'unico numero libero della feature e sceglierli a valore noto li piegherebbe verso l'intervallo che «sembra giusto», in un modo che nessun controllo di questo progetto potrebbe rilevare. Il piano non si limita a dichiarare la precedenza: la rende verificabile spezzando il file dei parametri in **due commit**, il primo dei quali non contiene nemmeno un campo vuoto per il benchmark (T7). Chi dubita apre `git log`.

La Fase 0 ha trovato quattro cose. Due sono trappole che avrebbero prodotto un difetto silenzioso: `data/external/` è **già ignorato da git**, quindi la cartella che il nome suggeriva per il file dei parametri non lo avrebbe versionato (F1); e lo spazio dei nomi di `conventions` è **piatto**, con `rounding_decimals` già occupato, quindi la regola di arrotondamento sarebbe entrata in collisione con una convenzione di un'altra feature (F2). La terza è una trappola di aritmetica: il sospetto cadeva sul prodotto per 4,00 €, che è esatto, mentre è la **banda** a produrre `0,43499999999999994` proprio sul confine di arrotondamento (F3). La quarta conferma che `docs/business_case.md` non è sotto controllo, che è la premessa di fatto di FR-025a.

Il resto è piccolo, e va detto: la derivazione è **una moltiplicazione e due proporzioni**. Il lavoro di questa feature sta nella ricognizione, nella prosa e nel non sbagliare l'ordine.

## Technical Context

**Linguaggio/Versione**: Python 3 (verificato su 3.14.6). Nessuna funzionalità oltre a quelle disponibili da 3.8

**Dipendenze primarie**: nessuna. Sola libreria standard — `json`, `decimal`, `pathlib`. Decisione T2 in [research.md](./research.md)

**Storage**: file. Ingresso `data/benchmarks/bq3_tier_upgrade.json`, curato a mano e **versionato** (T1, FR-002); uscita `reports/bq3_scenarios.json`, generato e **versionato** (T3, FR-018a), più `docs/bq3_scenarios.md` (T8)

**Testing**: verifica per esecuzione secondo [quickstart.md](./quickstart.md) — doppia esecuzione con diff vuoto, prova senza `data/raw/` e senza rete, ispezione per assenza di rete e di generatori casuali, due prove di alterazione sul controllo di coerenza. Nessun framework introdotto (T9), per la stessa ragione della 002 e della 003

**Piattaforma target**: qualunque sistema con Python 3. Sviluppo su macOS. Nessuna dipendenza dal locale: i decimali si scrivono con separatore italiano per formattazione esplicita, mai per funzione dipendente dal locale — vincolo ereditato da F6 della 003

**Tipo di progetto**: un file di parametri curato a mano, uno script di derivazione da riga di comando, un controllo esteso, un documento, quattro aggiunte a un documento già mergiato. Nessuna applicazione, nessun servizio, **nessun dataset**

**Obiettivi di performance**: nessuno. La derivazione calcola sei valori

**Vincoli**: nessuna chiamata di rete a runtime (FR-008); nessun generatore casuale e nessun seed (FR-013); eseguibile senza `data/raw/` e senza rete (FR-017); aritmetica esatta e arrotondamento dichiarato (FR-015, T5); confidenza `bassa` e formato range non modificabili (FR-021); nessun numero nella prosa del business case (FR-025a, FR-027a); ~6 ore di lavoro effettivo, revisione inclusa (principio III)

**Scala/Ambito**: 1 benchmark, 2 fattori stipulati, 1 costante di prezzo, **6 valori pubblicati**, 37 requisiti, 7 criteri di successo, 4 aggiunte al business case

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni valore dichiara fonte e confidenza; confidenza bassa ⇒ range | ✅ tabella compilata nella spec: 4 famiglie, tutte a confidenza bassa, tutte a range | ✅ diventa meccanica: `sources` nell'artefatto rimanda al file dei parametri, e FR-021 è verificabile per ispezione |
| **I bis. Benchmark, 5 condizioni** | citazione, congelamento, nessuna rete, trasferimento, nessuna promozione | ✅ tutte e cinque tradotte in requisiti (FR-003, FR-002, FR-008, FR-007, FR-021) | ⚠️ **la condizione 1 non è ancora soddisfatta** — vedi sotto |
| **II. Riproducibilità** | trasformazioni come codice versionato | ✅ la derivazione è codice; la raccolta è il passaggio umano che la condizione 3 ammette purché congelato | ✅ F1 ha evitato la violazione: `data/external/` non avrebbe versionato il congelamento |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ stima 6 ore | ⚠️ regge, con un rischio esterno — vedi "Budget e rischio" |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde | ✅ 7 voci in "Limiti Dichiarati", 3 inferenze da evitare | ✅ invariato |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessuna GUI. La raccolta è manuale **per obbligo**, non per limite dello strumento | ✅ invariato |
| **VI. Coerenza Narrativa** | riconducibile a una domanda di business | ✅ BQ3, dichiarata nella spec | ✅ invariato |

**Esito**: nessuna violazione. La tabella "Complexity Tracking" resta vuota. Due punti di attenzione, nessuno dei due risolvibile tagliando requisiti.

**La condizione 1 non è soddisfatta, ed è il rischio della feature.** Una ricognizione preliminare non ha trovato la metrica esatta — quota della base esistente che passa a un tier superiore — in forma direttamente citabile e gratuitamente recuperabile. Il piano **non** la dà per trovata: la ricognizione è un task con due esiti dichiarati, e FR-006/FR-006a impongono di riportare a Valerio **entrambi**, tanto il fallimento quanto l'adozione con il proprio scarto di misura. Se nessuna fonte regge, la feature si ferma con quattro artefatti su cinque già prodotti e la decisione passa a Valerio. Vedi "Budget e rischio".

**Sul principio II, una precisazione che vale la pena scrivere.** Questa feature è la prima del progetto in cui un passaggio **non riproducibile per costruzione** entra nella catena. Non è un'eccezione strappata: è la condizione 3 della constitution, che ammette il passaggio umano proprio perché ne impone il congelamento. La linea è netta e verificabile — a monte del file dei parametri sta una persona con un browser, a valle non c'è nulla che una copia pulita non possa rifare. Il quickstart verifica la seconda metà; della prima resta la citazione, che è tutto ciò che si può chiedere a un fatto avvenuto una volta sola.

## Project Structure

### Documentation (this feature)

```text
specs/004-synthetic-business-metrics/
├── spec.md                          # specifica approvata, 37 requisiti, 6 decisioni
├── plan.md                          # questo file
├── research.md                      # Fase 0 — 4 ritrovamenti, 9 decisioni tecniche
├── data-model.md                    # Fase 1 — forma dei due file e catena di derivazione
├── quickstart.md                    # Fase 1 — le prove di verifica, in ordine
├── contracts/
│   └── parameters-and-scenarios.md  # Fase 1 — il contratto che la 007 leggerà
├── checklists/
│   └── requirements.md              # checklist di qualità + verbale della revisione di regia
└── tasks.md                         # Fase 2 — prodotto da /speckit.tasks, non da qui
```

### Source Code (repository root)

```text
data/
└── benchmarks/                      # NUOVA — versionata, al contrario delle altre di data/
    └── bq3_tier_upgrade.json        # T1 · curato a mano, in due commit (T7)

reports/
└── bq3_scenarios.json               # NUOVO — generato e versionato (FR-018a)

scripts/
├── build_bq3_scenarios.py           # NUOVO — la derivazione, deterministica (FR-013)
└── check_audit_coherence.py         # MODIFICATO — terzo artefatto, terzo documento in DOCUMENTS

docs/
├── bq3_scenarios.md                 # NUOVO — documento di lettura, severità stretta (T8)
├── convenzioni-marcatura.md         # MODIFICATO — §3, §5 e tabella di provenienza (FR-019)
└── business_case.md                 # MODIFICATO — A6, richiamo in §6, 2 note datate (FR-025..030)

data/README.md                       # MODIFICATO — la quarta cartella e perché è versionata (T1)
```

**`docs/roadmap.md` non è in questo elenco**, ed è deliberato. È artefatto di governance e appartiene alla regia ([`CLAUDE.md`](../../CLAUDE.md)): la feature non lo tocca. La dichiarazione dello scostamento sul seed che FR-024 impone va **negli artefatti della feature** — la sede naturale è `docs/bq3_scenarios.md`, che è il documento in cui il metodo si spiega — e non in una modifica alla roadmap. La nota in loco sulla roadmap è stata scritta dalla regia il 2026-08-16.

**Structure Decision**: nessuna struttura nuova. La feature si innesta sulle tre cartelle che il progetto già usa — `data/` per gli ingressi, `reports/` per gli artefatti generati, `docs/` per ciò che si legge — e ne aggiunge una sola sottocartella, `data/benchmarks/`, la cui **regola di versionamento è invertita** rispetto alle sorelle. L'inversione è deliberata e motivata in T1: le altre non sono versionate perché riproducibili, questa lo è perché non lo è. Va scritta in `data/README.md`, altrimenti il prossimo che legge quella pagina la prende per un errore.

## La catena, in una riga

```
benchmark (umano, congelato)  ─┐
fattori k (stipulati, PRIMA)  ─┼─→ build_bq3_scenarios.py ─→ reports/bq3_scenarios.json ─→ docs/bq3_scenarios.md
differenziale 4,00 € (da A4)  ─┘        deterministico              6 valori + convenzioni        ogni cifra ancorata
```

Tutto ciò che sta a sinistra è dichiarato a mano e versionato. Tutto ciò che sta a destra si rigenera. Non esiste un terzo posto in cui un numero possa nascere — ed è ciò che FR-014 chiede: cambiare il benchmark e rieseguire deve muovere tutti e sei i valori.

## Ordine di lavoro e punti di sosta

L'ordine non è libero, per T7. Cinque blocchi:

| # | Blocco | Vincolo di ordine | Esito |
|---|---|---|---|
| **A** | fattori della banda, differenziale, ragione — nel file dei parametri | **deve precedere B** (FR-011a) | commit isolato, che è la prova della precedenza |
| **B** | ricognizione del benchmark, citazione, scarto, assunzione di trasferimento | dopo A | commit separato · **riporto a Valerio in entrambi gli esiti** (FR-006, FR-006a) |
| **C** | derivazione, artefatto, estensione del controllo | dopo B | i sei valori esistono e sono verificabili |
| **D** | documento di lettura, `convenzioni-marcatura.md`, `data/README.md` | dopo C | ogni cifra ancorata, controllo verde in severità stretta |
| **E** | debito testuale sul business case, roadmap, revisione in contesto pulito | dopo D | chiusura di R13-BQ3 e del debito dell'ancoraggio |

**Il confine di sosta migliore è la fine di C**, e non coincide con un punto di stop del flusso. La regola che la 003 ha ricavato dalla propria finestra non pianificata — *il confine di pausa si sceglie dove il lavoro smette di produrre stato intermedio* — qui indica C: dopo C i sei valori sono congelati in un artefatto versionato e tutto ciò che resta è prosa, che non invecchia. Una sosta dentro B lascerebbe invece una ricognizione a metà, che è esattamente lo stato che costa di più riprendere.

## Budget e rischio

| Blocco | Ore | Contenuto |
|---|---|---|
| A | 0,5 | fattori, ragione, forma del file, `data/benchmarks/` committabile |
| B | **1,5** | ricognizione, valutazione delle fonti contro le cinque condizioni, citazione, scarto di misura, registro dei rigetti |
| C | 1,0 | derivazione in `Decimal`, artefatto, terzo artefatto nel controllo |
| D | 1,5 | documento marcato, severità stretta, tre modifiche alla fonte unica, `data/README.md` |
| E | 1,5 | A6, richiamo in §6, due note datate, roadmap, revisione in contesto pulito e chiusura dei rilievi |
| | **6,0** | |

**Il rischio è tutto in B, ed è esterno.** Non è un rischio di stima: è la possibilità che nessuna fonte soddisfi le cinque condizioni. Se accade, B non sfora — **si ferma**, e con esso C, D per la parte che dipende dai valori, ed E per la parte delle note. Restano consegnabili A, il registro dei rigetti, e la parte di E che non dipende dal benchmark. Il piano non prevede un ripiego automatico, perché FR-006 lo vieta: la decisione è di Valerio.

**Il secondo rischio è la stima di B stessa.** Una ricognizione che deve *rifiutare* fonti costa più di una che ne cerca una qualsiasi, e il registro dei rigetti (FR-005) è lavoro reale. 1,5 ore è la stima onesta; se B sfora, la linea di taglio dichiarata dal prompt di consegna — *ricerca e file dei parametri* da una parte, *derivazione e documento* dall'altra — cade esattamente fra B e C, ed è ancora disponibile.

**Ciò che non è un rischio**: C. Sei valori, nessun ramo, aritmetica esatta scelta in Fase 0. Se C sforasse sarebbe il segnale che qualcosa è stato frainteso, non che il lavoro era grande.

**Il terzo rischio è E, e la formulazione del confine di sosta lo nasconde.** «Da qui in avanti è tutta prosa, che non invecchia» è giusto come criterio di **pausa** — nulla di intermedio resta appeso — e ottimista come ipotesi di **budget**: E contiene quattro aggiunte a un artefatto già mergiato, tre modifiche alla fonte unica della grammatica, una revisione in contesto pulito e la chiusura dei suoi rilievi. Nella 003 la chiusura dei rilievi ha richiesto **nuovi valori** nel rendiconto, non riscritture di frasi, perché la regola D5 non ammette altra strada.

Il confine resta dov'è. Ciò che cambia è l'istruzione in caso di sforamento: **se E sfora, sfora dichiarandolo**. La parte da non comprimere è la chiusura dei rilievi, che nella 003 ha prodotto il valore maggiore dell'intera feature — non il documento, che è la parte più visibile e la più facile da consegnare incompleta senza che si veda.

## Complexity Tracking

Nessuna violazione della constitution da giustificare. La tabella resta vuota.
