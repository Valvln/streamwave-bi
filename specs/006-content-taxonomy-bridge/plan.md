# Implementation Plan: Content Taxonomy Bridge

**Branch**: `006-content-taxonomy-bridge` | **Date**: 2026-08-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/006-content-taxonomy-bridge/spec.md`

## Summary

La feature produce **quattro artefatti**, nell'ordine imposto da D1: un documento criterio, committato da solo; una proposta di un LLM invocato manualmente; una tabella congelata che porta insieme l'esito del congelamento e il registro della verifica indipendente; un documento pubblicato. Nessuno dei quattro è generato da uno script — è la differenza strutturale con la `004`, che questa fase ha isolato come ritrovamento F5: qui non esiste un passo di derivazione, perché D1 vieta a qualunque script di toccare il valore dopo il congelamento tanto quanto vieta a qualunque script di invocare il modello.

**Il ritrovamento che vale di più** è F3: gli estremi `0` e `1` dei tre assi sul lato musicale sono **già misurati e già ancorati** in `reports/data_profile.json` — `SP.num.energy.min/.max` e i due omologhi valgono esattamente `0` e `1` sull'intero insieme delle tracce. Il criterio (D1, passo 1; D2; D7) può quindi ancorare i propri estremi a sei identificativi già pubblici invece che a un'affermazione qualitativa o, peggio, a un titolo — che D7 vieta. Non chiude da sola la verifica indipendente di D9.1, che resta un giudizio su 126 righe, ma toglie al punto più fragile della feature — l'obbligo di scala che D2 chiama "quello che conta di più" — la sua parte più arbitraria.

**Il secondo ritrovamento** riguarda la forma dell'artefatto finale. `data/curated/dim_category_mood.json` deve essere insieme il congelamento non riscrivibile di D1 **e** il quarto membro di `ARTIFACTS` che FR-023 richiede. Il piano risolve la tensione facendo dello spazio `values` la rappresentazione canonica delle 126 celle — non una copia di un campo `rows` separato, che sarebbe una seconda fonte di verità senza uno script che la tenga allineata (§3 di [data-model.md](./data-model.md)).

Il resto è largamente procedurale: verificare l'indipendenza dichiarata fra chi propone e chi verifica, estendere il controllo di coerenza con una guardia meccanica separata dal ciclo di marcatura (D6, chiusura di R2), e tenere le due revisioni di D9 fisicamente distinte — cosa che il piano ha già assorbito scrivendo il modello dei dati e il contratto prima di toccare la questione dell'ordine di lavoro.

## Technical Context

**Linguaggio/Versione**: Python 3 stdlib (`json`, `hashlib`, `re`), coerente con 002-005. Nessuna dipendenza nuova

**Dipendenze primarie**: nessuna. L'unica invocazione di un LLM è manuale, fuori da qualunque script del repository (FR-005) — non è una dipendenza di questo codice, è un passaggio umano che il codice non orchestra

**Storage**: file versionati. `docs/mood_assignment_criteria.md` (criterio); `data/curated/dim_category_mood_proposal.json` (proposta, mai marcata); `data/curated/dim_category_mood.json` (tabella congelata, quarto membro di `ARTIFACTS`); `docs/content_taxonomy_bridge.md` (documento pubblicato, quinto membro di `DOCUMENTS`, severità stretta dalla nascita)

**Testing**: verifica per esecuzione e per ispezione secondo [quickstart.md](./quickstart.md) — dieci prove: precedenza in history, assenza di titoli citati, assenza di chiamate di rete negli script, indipendenza dichiarata fra proponente e verificatore, copertura e scala, campo `version`, fallimento meccanico del controllo su tassonomia divergente, esito verde in severità stretta, assenza di attributi di record individuale, assenza di promozione di confidenza. Nessun framework introdotto, per la stessa ragione della 002-004

**Piattaforma target**: qualunque sistema con Python 3. Nessuna dipendenza dal locale nei file prodotti — i decimali si scrivono con virgola nel `display`, punto nel `value`, per formattazione esplicita (vincolo ereditato da F6 della 003, applicato di nuovo qui)

**Tipo di progetto**: due documenti curati a mano, due file JSON curati a mano (uno dei quali entra nello spazio dei nomi marcato), un'estensione di uno script esistente. Nessuna applicazione, nessun servizio, **nessuna pipeline**

**Obiettivi di performance**: nessuno. 126 celle, un confronto insiemistico su 42 elementi

**Vincoli**: nessuno script MUST invocare il modello, mai (FR-005); nessuno script MUST rigenerare la tabella dopo il congelamento (FR-012); scala `0-1` identica al lato musicale su ogni cella (FR-013); copertura totale o dichiarata (FR-014); confidenza `media` non negoziabile in ogni artefatto (FR-017); nessun attributo di record individuale (FR-020); ~6 ore di lavoro effettivo, revisioni incluse (principio III)

**Scala/Ambito**: 1 criterio, 1 proposta, 126 celle congelate, 1 documento pubblicato, 26 requisiti, 8 criteri di successo, 1 estensione di script, 1 nota in loco su un artefatto già mergiato

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni valore dichiara fonte e confidenza | ✅ tabella compilata nella spec: `Sintetico`, confidenza `media`, non negoziabile | ✅ diventa meccanico: ogni cella in `values` porta `label`/`unit`; `MOOD.table.version` rende verificabile il legame di D5 |
| **I bis. Assegnazione dell'analista, 5 condizioni (v1.2.0)** | criterio prima del valore; valore congelato e mai rigenerato; versione dichiarata a valle; revisione indipendente con esito quantificato; nessuna promozione di confidenza | ✅ tutte e cinque tradotte in decisioni (D1, D5, D9.1, D4) e requisiti | ✅ la forma di `dim_category_mood.json` (§3 di data-model.md) rende la condizione 3 verificabile per lettura di `version`, e la condizione 4 verificabile per lettura di `verification.changes_count` |
| **II. Riproducibilità** | trasformazioni come codice versionato | ✅ non c'è trasformazione: il congelamento è la forma che la condizione 2 della quinta fonte ammette esplicitamente per un passaggio non riproducibile | ✅ F5 conferma che l'assenza di uno script di derivazione è la forma corretta, non un'omissione |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ stima 6 ore, taglio 006a/006b già dichiarato al confine di D9 se serve | ✅ regge — vedi "Budget e rischio" |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde | ✅ 5 voci in "Limiti Dichiarati", 4 inferenze da evitare | ✅ invariato |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessuna GUI. L'invocazione del modello è manuale **per obbligo**, non per limite dello strumento | ✅ invariato |
| **VI. Coerenza Narrativa** | riconducibile a una domanda di business | ✅ BQ1 e BQ2, tre KPI su otto, dichiarato nella spec | ✅ invariato |

**Esito**: nessuna violazione. La tabella "Complexity Tracking" resta vuota.

**Un punto di attenzione che il gate non intercetta.** La condizione 4 della quinta fonte — revisione indipendente con esito quantificato — è verificabile per lettura (`verification.changes_count` esiste, `verified_by` è dichiarato), ma **non** che l'indipendenza sia reale: nessun controllo automatico di questo progetto può verificare che chi ha scritto `verified_by` non sia, in pratica, la stessa persona che ha ottenuto la proposta sotto un nome diverso. È lo stesso limite dichiarato dalla `004` su `bq3_band_fixed_before`: la garanzia vale contro la variante più comune del difetto — il campo lasciato vuoto o riempito con lo stesso nome per abitudine — non contro una dichiarazione deliberatamente falsa. Contro quella esiste solo la revisione in contesto pulito di D9.2, che però guarda il documento pubblicato, non il registro di verifica. Il piano non ha una risposta migliore di quella che la constitution stessa dà altrove: la si dichiara invece di fingere che non esista.

## Project Structure

### Documentation (this feature)

```text
specs/006-content-taxonomy-bridge/
├── spec.md                              # specifica approvata, 26 requisiti, 9 decisioni
├── plan.md                              # questo file
├── research.md                          # Fase 0 — 5 ritrovamenti, 9 decisioni tecniche
├── data-model.md                        # Fase 1 — forma dei quattro artefatti
├── quickstart.md                        # Fase 1 — le dieci prove di verifica, in ordine
├── contracts/
│   └── dim-category-mood-contract.md    # Fase 1 — il contratto che la 007 leggerà
├── checklists/
│   └── requirements.md                  # checklist di qualità
├── review.md                            # revisione in contesto pulito di D9.2 — non ancora prodotto
└── tasks.md                             # Fase 2 — prodotto da /speckit.tasks, non da qui
```

### Source Code (repository root)

```text
docs/
├── mood_assignment_criteria.md          # NUOVO — il criterio, committato da solo (D1 passo 1)
├── content_taxonomy_bridge.md           # NUOVO — documento pubblicato, severità stretta dalla nascita
└── data_model.md                        # MODIFICATO — nota in loco su §15 condizione 4 (D8, FR-021)

data/
└── curated/                             # NUOVA — versionata, come benchmarks/ della 004 (T1, F1)
    ├── dim_category_mood_proposal.json  # NUOVO — proposta del modello (D1 passo 2)
    └── dim_category_mood.json           # NUOVO — tabella congelata, quarto membro di ARTIFACTS (D1 passo 4)

scripts/
└── check_audit_coherence.py             # MODIFICATO — quarto artefatto, quinto documento, guardia di copertura D6

docs/convenzioni-marcatura.md            # MODIFICATO — §3, §5, tabella di provenienza (FR-023)
data/README.md                           # MODIFICATO — già in questa fase (Fase 1), sezione curated/
```

**`docs/roadmap.md` non è in questo elenco**, deliberatamente. È artefatto di governance e appartiene alla regia (`CLAUDE.md`): la feature registra la chiusura di `DA-1` come eseguita e delle tre divergenze (FR-026), ma la nota vive **negli artefatti della feature** che la roadmap stessa indica — non è la `006` a riscrivere la sezione "Decisioni aperte" della roadmap, è la regia, con la stessa cautela già osservata dalla `004`.

**Structure Decision**: nessuna struttura nuova oltre `data/curated/`, la cui regola di versionamento è invertita rispetto alle sorelle di `data/`, come già `benchmarks/` — la motivazione per esteso è scritta in `data/README.md` in questa stessa fase, come la spec richiede esplicitamente nelle sue Assumptions.

## La catena, in una riga

```
criterio (persona, committato da solo)  ──┐
                                           │
proposta (LLM, invocato una volta)  ──────┼─→  verifica indipendente  ─→  tabella congelata
                                           │      (D9.1, contro il          (data/curated/
osservazioni musicali già ancorate  ──────┘       criterio, mai altro)      dim_category_mood.json)
(reports/data_profile.json, F3)                                                    │
                                                                                     ▼
                                                                          documento pubblicato
                                                                          (revisione D9.2, in contesto pulito)
```

A differenza della catena della `004`, non c'è un segmento a destra che "si rigenera": ogni nodo di questo grafo è scritto o congelato da una persona. L'unico elemento deterministico è il **confronto** che il controllo di coerenza esegue fra la tabella congelata e `catalogs.netflix_categories_normalized` — non una derivazione di valori, una verifica di un insieme.

## Ordine di lavoro e punti di sosta

L'ordine non è libero, per D1 e per il terzo punto di fermata che la roadmap ha già imposto alla `006` (risoluzione di `DA-1`, 2026-08-19). Cinque blocchi.

| # | Blocco | Vincolo di ordine | Esito |
|---|---|---|---|
| **A** | criterio, ancorato agli identificativi di F3, committato da solo | nessuno — è il primo passo possibile | commit isolato: nessun valore della tabella esiste ancora |
| **★** | **terzo punto di fermata**: il criterio è committato, nessun valore esiste. Prima di procedere, il criterio torna in revisione | dopo A, prima di B | è il punto di massima leva della feature (roadmap, `DA-1`): un criterio sbagliato produce tutti i valori sbagliati, e nessuno lo riscrive più dopo che i 126 numeri esistono |
| **B** | invocazione manuale del modello, proposta versionata con prompt/modello/data | dopo ★ | `data/curated/dim_category_mood_proposal.json` esiste, non ancora verificato |
| **C** | verifica indipendente (D9.1) contro il criterio, conteggio degli spostamenti, congelamento | dopo B | `data/curated/dim_category_mood.json` esiste, versione `1` — **chiude `006a`** |
| **D** | documento pubblicato, estensione del controllo di coerenza (D6), registrazione in `convenzioni-marcatura.md`, nota in loco su `data_model.md` §15 | dopo C | ogni cifra ancorata, controllo verde in severità stretta su cinque documenti |
| **E** | revisione in contesto pulito del documento (D9.2), chiusura dei suoi rilievi, README, roadmap | dopo D | **chiude `006b`** — chiusura di `DA-1` come eseguita, della divergenza 10 della `001`, della divergenza 5 della `002`, della parte generale della divergenza 5 della `003` |

**Il confine di sosta migliore, se la giornata si spezza, è la fine di C.** È lo stesso criterio della `004`: dopo C la tabella è congelata, versionata, verificabile riga per riga — nessuno stato intermedio resta appeso. Una sosta dentro B lascerebbe una proposta non ancora verificata, che non è pubblicabile né scartabile senza deciderlo.

**★ non è facoltativo e non coincide con nessuno dei due punti di stop generici del flusso** (dopo `/speckit.specify`, dopo `/speckit.tasks`). È specifico di questa feature, imposto dalla risoluzione di `DA-1`: "un terzo punto di fermata per la `006`, dopo il commit del criterio e prima che il modello proponga alcunché". Il task che lo implementa deve produrre un commit proprio e fermarsi lì fino a conferma esplicita — non una pausa naturale come la fine di C, un punto che il piano rende **eseguibile come task isolato**, come la spec richiede.

## Budget e rischio

| Blocco | Ore | Contenuto |
|---|---|---|
| A | 1,0 | criterio per tre assi, sei ancoraggi a `SP.num.*`, commit isolato |
| ★ | — | incluso in A: è un punto di verifica, non un blocco di lavoro a sé |
| B | 0,3 | invocazione manuale, versionamento di prompt/modello/data |
| C | 1,2 | verifica riga per riga, conteggio degli spostamenti, congelamento — **chiude `006a`** |
| D | 1,8 | documento, estensione dello script (quarto artefatto, guardia D6, quinto documento), tre modifiche a `convenzioni-marcatura.md`, nota in loco su `data_model.md` |
| E | 1,7 | revisione in contesto pulito, chiusura dei rilievi, README, roadmap — **chiude `006b`** |
| | **6,0** | |

**Il rischio principale è in A, e non è di stima: è di qualità del criterio.** Un criterio che non riesce ad ancorare in modo verificabile anche solo uno dei sei estremi lascia la verifica indipendente di C senza metro su quell'asse — esattamente il difetto che D2 chiama capace di "non produrre alcun errore visibile". F3 riduce questo rischio, non lo elimina: gli identificativi esistono, ma tradurli in una regola di assegnazione leggibile resta un giudizio.

**Il secondo rischio è D, per la stessa ragione della `004`.** Un'estensione di script con una guardia nuova (D6) costa più di un'estensione che aggiunge solo un quarto elemento a una tupla — la guardia di copertura è una funzione a sé, non un'aggiunta al ciclo esistente (T8, research.md), e va scritta, testata con l'alterazione della Prova 7, e ripristinata.

**Se D9 avesse fatto scoprire un lavoro più grande di quanto la stima assorbe**, il taglio non è da inventare: cade esattamente al confine fra C e D, che la spec chiama `006a`/`006b`. `006a` da solo è già un deliverable difendibile — la tabella esiste, copre le 42 categorie, è verificabile riga per riga contro il criterio.

**Ciò che non è un rischio**: B. Un'invocazione, un file, tre campi obbligatori.

## Complexity Tracking

Nessuna violazione della constitution da giustificare. La tabella resta vuota.
