# Implementation Plan: il report che porta l'argomento a schermo — disegno

**Branch**: `010a-report-disegno` | **Date**: 2026-08-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/010a-report-disegno/spec.md`

## Summary

La feature produce **un deliverable** — [`contracts/page-contract.md`](./contracts/), il disegno delle dieci pagine del report che sostituisce la dashboard a quattro pagine — e i documenti che lo sostengono: le nove decisioni di disegno, l'input per la `010b`, le prove di verifica, il verbale di revisione. Allinea il README e non tocca alcun documento sotto `docs/`.

**È una feature di solo testo che disegna un artefatto binario che non esisterà mai in questo repository.** Il `.pbix` non è versionato; questa sessione non lo apre e non può accertarne nulla. Ne discende il vincolo che governa l'intera feature: **il contratto dichiara che cosa deve esistere, mai che cosa esiste**. La `010b` accerterà.

**Il lavoro analitico è chiuso in [research.md](./research.md)**, nove decisioni `G1`-`G9`. Questo piano non le riapre: le traduce in blocchi con un ordine di dipendenza e un punto di fermata in mezzo.

**Il rischio principale è il collasso della corrispondenza pagina→sezione.** Dieci pagine su sei sezioni: se la corrispondenza si legge come uno-a-uno, il disegno forza sei pagine e ricompatta l'inventario, oppure ne inventa quattro dividendo per capienza — che è lo stesso inventario con più fogli. `G1` fissa la direzione (una pagina serve una sezione; una sezione può ricevere più pagine) e il criterio di divisione (cambia la **mossa** dell'argomento, non la capienza). È la decisione più importante del piano, ed è la ragione per cui è la prima.

**Il secondo rischio è di compressione, e la regia lo ha già nominato.** La parte che si comprimerebbe per prima è l'elenco delle misure e visuali nuove, ed è la peggiore da comprimere: è l'input su cui poggia la stima della `010b`, la feature più grande mai aperta e la sola rimasta a toccare la GUI. Il blocco che la produce è quindi **prima** del contratto, non dopo — vedi «Ordine dei blocchi».

## Technical Context

**Linguaggio/Versione**: nessuno. Questa feature non scrive né modifica alcuna riga di Python, di DAX o di Power Query. Le sei misure DAX nuove sono **specificate**, non scritte: nome, contenuto, tabelle di lettura, pagina richiedente. Chi le scrive è la `010b`

**Dipendenze primarie**: nessuna. Non apre Power BI Desktop per alcuna ragione (spec, `FR-026`). Legge artefatti versionati — `reports/kpi_measures.json`, `reports/bq3_scenarios.json`, `data/curated/dim_category_mood.json` — in sola lettura, per verificare che le ancore citate esistano

**Storage**: nessun artefatto nuovo sotto `reports/` o `data/`. Nessun documento nuovo sotto `docs/`, quindi **nessuna riga nuova in `DOCUMENTS` o `ARTIFACTS`** di `scripts/check_audit_coherence.py` e nessuna riga nuova nella tabella di severità di `docs/convenzioni-marcatura.md`. È la seconda feature dalla `004` a non estendere il controllo, dopo la `008a`, ed è dichiarato qui perché l'assenza non venga letta come una dimenticanza

**Testing**: due prove eseguibili e dieci per ispezione, secondo [quickstart.md](./quickstart.md). Le due eseguibili certificano poco e la loro debolezza è dichiarata lì: una verifica un'assenza di danno, l'altra che le ancore citate siano risolvibili. Tutto ciò che conta — che l'ordine sia quello dell'argomento, che nessuna pagina sia un inventario — è un'osservazione umana

**Piattaforma target**: nessuna. Il documento prodotto è Markdown e si legge ovunque. La piattaforma su cui il disegno atterrerà — Power BI Desktop, schermo singolo 16:9 — è quella della `010b`, e questa feature la presuppone senza toccarla

**Tipo di progetto**: un contratto di disegno e quattro documenti di feature, più un allineamento di README. Nessuno script, nessun artefatto, nessun file binario

**Obiettivi di performance**: nessuno. Il vincolo di leggibilità delle due visuali dense — 114 punti e 114 righe — è ereditato dalla `008a`, che lo ha già verificato a schermo, e questa feature non lo ridiscute

**Vincoli**: nessun valore trascritto nel contratto, solo identificativi di ancora (`FR-003`); nessuna affermazione sullo stato del `.pbix` (`FR-002`); fra 8 e 12 pagine con la convenzione dichiarata (`FR-007`); ogni pagina serve esattamente una sezione (`G1`); la formulazione stretta sull'uplift (`FR-020`, issue `#26`); ~6 ore di lavoro effettivo, revisione e chiusura dei rilievi incluse (principio III)

**Scala/Ambito**: 10 pagine, 6 sezioni dell'argomento servite, 7 KPI su 8 a schermo, 10 misure esistenti e 4 dichiarate dalla `008a`, 6 misure nuove, 4 visuali nuove e 4 riusate, 2 pagine di sola prosa, 1 visuale dichiarata non costruibile, 3 ritrovamenti, 4 issue da dichiarare (`#20`, `#21`, `#26`, `#28`), 1 debito di governance da richiamare (la `004`), 0 script nuovi, 0 artefatti nuovi, 0 documenti sotto `docs/` toccati

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni numero mostrato dichiara fonte e confidenza | ✅ `FR-017` porta le etichette su ogni pagina; nessuna promozione di confidenza, tabella ereditata invariata | ✅ rafforzato: `M3` elimina l'ultima soglia digitabile del disegno, e `G5` impedisce che la congiunzione erediti la confidenza del suo termine più forte |
| **II. Riproducibilità** | trasformazioni come codice versionato | ✅ nessuna trasformazione: la feature non tocca dati e non scrive script | ✅ invariato. Il `.pbix` che il disegno descrive resta non rigenerabile, ed è conseguenza del principio V — non di questo, e non di questa feature |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ ~6 ore, ed è già il prodotto della scomposizione della `010` decisa dalla regia | ✅ regge. Il punto di fermata 2 spezza la feature in due sessioni di lunghezza simile |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde, **e nella dashboard dove il consumatore è l'utente finale** | ✅ sezione «Limiti Dichiarati» della spec | ⚠️ **la metà «nella dashboard» non è soddisfatta da questa feature**: il disegno riserva lo spazio, il testo è della `010b`. Vedi Complexity Tracking, prima riga |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ **nessun task di questa feature entra in una GUI**, ed è la prima feature dalla `007b` per cui è vero senza eccezioni | ✅ invariato |
| **VI. Coerenza Narrativa** | riconducibile a una domanda di business | ✅ tutte e tre: porta a schermo l'argomento che le compone | ⚠️ **con una conseguenza da dichiarare**: il report porta sette KPI su otto. Vedi Complexity Tracking, seconda riga |

**Esito**: nessuna violazione non giustificata. Due voci in Complexity Tracking; la prima è ereditata dalla `008a` e non è nuova, la seconda è prodotta da questa feature ed è la sua decisione più contestabile.

**Un punto di attenzione che il gate non intercetta, e che questa feature ha in comune con la `008a`.** I gate sono scritti per feature che producono artefatti ispezionabili. Qui il deliverable è un **vincolo su un artefatto futuro**, e non esiste modo di verificarlo se non leggendolo: nessuno script può stabilire se dieci pagine siano ordinate come un argomento o come un inventario. Il gate passa perché qualcuno lo dichiara. È la ragione per cui la revisione in contesto pulito non è una formalità di chiusura ma il presidio principale della feature, e per cui il suo perimetro va composto con cura — vedi «Il perimetro della revisione».

## Project Structure

### Documentation (this feature)

```text
specs/010a-report-disegno/
├── spec.md                          # specifica: 31 requisiti, 8 criteri, 3 storie
├── plan.md                          # questo file
├── research.md                      # Fase 0 — le nove decisioni G1-G9
├── data-model.md                    # Fase 1 — mappa delle pagine, 6 misure nuove, 4 visuali nuove
├── quickstart.md                    # Fase 1 — 2 prove eseguibili, 10 per ispezione, il censimento delle copie
├── contracts/
│   └── page-contract.md             # ★ prodotto nel blocco C, NON in questa fase
├── checklists/
│   └── requirements.md              # checklist di qualità, già verificata
├── review.md                        # revisione in contesto pulito — non ancora prodotto
└── tasks.md                         # Fase 2 — prodotto da /speckit.tasks
```

**`contracts/page-contract.md` è dichiarato qui ma non prodotto qui**, sullo stesso precedente della `008a`: la Fase 1 di `/speckit.plan` produce normalmente tutti i contratti, questo no, perché è il deliverable e ha bisogno di essere letto da solo — con l'attenzione che si dà a un disegno, non in coda a un documento di processo.

**Dove va l'esito.** In coda a [quickstart.md](./quickstart.md), come nella `008a`: le prove e il loro esito sono la stessa cosa vista prima e dopo, e separarli produrrebbe due documenti che si citano a vicenda senza che nessuno si legga da solo.

### Repository (fuori dalla cartella della feature)

```text
README.md                            # riga di stato, deliverable, prosa, Setup e Struttura
```

**È l'unico file fuori da `specs/010a-report-disegno/` che questa feature tocca.** Nessun documento sotto `docs/`, nessuno script, nessun artefatto. Se una nota in loco si rendesse necessaria per un ritrovamento, sarebbe l'unica eccezione — e i tre ritrovamenti già registrati non la richiedono, perché nessuno è una divergenza fra un valore pubblicato e il suo artefatto.

## Ordine dei blocchi

Quattro blocchi. L'ordine non è cronologico per comodità: **due dipendenze lo vincolano**, e sono entrambe presidi.

| Blocco | Che cosa produce | Dipende da | Perché in questa posizione |
|---|---|---|---|
| **A** | le decisioni `G1`-`G9` | — | `G1` fissa la direzione della corrispondenza pagina→sezione. Ogni pagina disegnata prima di `G1` andrebbe ridisegnata dopo |
| **B** | la mappa delle pagine, le 6 misure nuove, le 4 visuali nuove, la visuale non costruibile | A | **è l'input della `010b` e viene prima del contratto**, non dopo. Un elenco prodotto in coda a un documento lungo è l'elenco che si comprime quando le ore stringono, ed è precisamente quello che non va compresso |
| **C** | il contratto di pagina | A, B | è il deliverable. Consuma B invece di riprodurlo |
| **D** | censimento delle copie, prove, README, revisione, chiusura | C | il censimento precede la revisione per obbligo; la revisione precede qualunque correzione del contratto |

**Blocchi A e B sono la Fase 0 e la Fase 1**, già prodotti: [research.md](./research.md) e [data-model.md](./data-model.md). Il punto di fermata 2 cade **fra B e C**.

**Perché il punto di fermata cade lì e non dopo il contratto.** Al secondo punto di fermata la regia riceve le decisioni che chiedono conferma e il numero di pagine a cui il disegno è arrivato. Entrambe sono in B: dieci pagine, sette KPI su otto, l'issue `#21` chiusa, sei misure nuove. Portarle dopo il contratto significherebbe farle approvare insieme a settanta righe di disegno che ne discendono — cioè chiedere una conferma su una decisione già eseguita.

## Il perimetro della revisione

**Ha una difficoltà propria, e va risolta prima che la revisione parta.**

Il revisore deve poter giudicare se il disegno regge la spina dell'argomento: quindi riceve `docs/raccomandazione.md` insieme al contratto. Ma un revisore che ha letto entrambi **non può più dire se il contratto si legga da solo** — ed è la proprietà che conta per chi costruirà, che aprirà la `010b` con il contratto in mano e non con la raccomandazione.

**Le due domande sono incompatibili nella stessa sessione**, e il verbale deve dichiarare quale delle due è stata fatta verificare.

**Decisione**: si fa verificare **la prima** — se il disegno regge la spina. Il perimetro comprende quindi `docs/raccomandazione.md` e il contratto.

**Motivazione**: la seconda domanda ha un presidio alternativo e la prima no. Se il contratto non si legge da solo, la `010b` lo scopre alla prima ora di lavoro e torna a chiedere — costoso, ma recuperabile. Se il disegno non regge la spina, la `010b` costruisce dieci pagine che ripetono il difetto per cui questa feature esiste, e il costo è l'intera feature. Si fa verificare il difetto che non ha una seconda occasione.

**Che cosa questo lascia scoperto, dichiarato invece di taciuto**: nessuno verifica in questa feature che il contratto si legga da solo. È un rischio accettato e va scritto nel verbale.

## Complexity Tracking

| Violazione | Perché serve | Alternativa più semplice, e perché scartata |
|---|---|---|
| **Principio IV, metà «nella dashboard»**: i limiti non compaiono a schermo alla chiusura di questa feature | il disegno riserva lo spazio in cui il testo andrà; scriverlo qui significherebbe fare il lavoro della `010b`, che ha il proprio contratto di narrazione | scrivere il testo dentro il contratto di pagina. Scartata: fonde due decisioni che il progetto ha separato deliberatamente sulla `008a`/`008b`, e la seconda si giudica su un metro diverso — la resa a schermo, non la struttura |
| **Principio VI**: il report porta sette KPI su otto — `BQ1-K2` resta fuori | l'argomento di `docs/raccomandazione.md` non lo usa mai, e includerlo richiederebbe una pagina che nessuna sezione serve, cioè una violazione di `G1` | includerlo comunque, per completezza rispetto al framework. Scartata, ed è la scelta centrale della feature: la completezza rispetto al framework era la proprietà organizzatrice della dashboard vecchia, ed è ciò che la revisione ha respinto. **È comunque la decisione più contestabile di questo disegno e va al punto di fermata 2**, non assorbita qui |

**Nessuna delle due è nuova come classe.** La prima è ereditata dalla `008a` con lo stesso testo. La seconda è nuova come contenuto ma non come tipo: è la stessa forma di scelta — servire l'argomento invece del framework — che la regia ha già preso aprendo la `009`.
