# Implementation Plan: il report che porta l'argomento a schermo — costruzione

**Branch**: `010b-report-costruzione` | **Date**: 2026-08-29 | **Spec**: [spec.md](spec.md)

**Input**: [spec.md](spec.md), [research.md](research.md), e il vincolo che governa tutto: [`specs/010a-report-disegno/contracts/page-contract.md`](../010a-report-disegno/contracts/page-contract.md)

## Summary

Costruire le dieci pagine che il contratto della `010a` disegna, scriverne la narrazione, e accertare che ciò che esiste a schermo coincida con ciò che gli artefatti versionati pubblicano.

**L'approccio, in una frase: si scrive prima ciò che sarà versionato, poi si apre la GUI.** Le sei misure DAX e il contratto di narrazione sono artefatti testuali; il report è un file binario che nessun controllo del repository può leggere. Il principio V lo impone — *tutto ciò che è esprimibile come artefatto testuale versionabile DEVE esserlo* — e questa feature vi aggiunge una ragione operativa: **non si scrive prosa guardando lo schermo**. Si scrive prima, si fa approvare, e poi si verifica che ci stia.

**L'ordine di costruzione è pagina per pagina, finita.** Non dieci pagine in bozza da rifinire alla fine. Se il tempo finisse, ciò che deve esistere è un sottoinsieme di pagine complete, ed è una decisione di Valerio quali cadano.

## Technical Context

**Strumento**: Power BI Desktop, sul disco di Valerio. Il `.pbix` **non è versionato**.

**Linguaggio delle misure**: DAX. Le sei nuove sono artefatti testuali e vivono in [contracts/measures.md](contracts/measures.md).

**Origine dei dati**: il modello esistente della `008a` — sette tabelle, cinque relazioni, più la tabella disconnessa degli scenari. Questa feature **aggiunge** e non ricostruisce (assunzione `A-1` della spec).

**Artefatti di verifica**: `reports/kpi_measures.json`, `reports/bq3_scenarios.json`, `reports/cleaning_report.json`, `reports/data_profile.json`, `data/curated/dim_category_mood.json`. Il confronto fra motore e valore pubblicato si fa **contro questi**, non contro la memoria.

**Controllo**: `scripts/check_audit_coherence.py`, sui documenti che questa feature pubblica o modifica.

**Testing**: nessun test automatico può leggere il `.pbix`. Le verifiche sono **prove manuali eseguibili da una persona**, sul modello delle dodici prove della `008a` (principio V).

**Scala**: dieci pagine, sei misure nuove, quattro visuali nuove più una nuova come forma, quattro riusate invariate, `114` segmenti nella graduatoria, `42` categorie nella dispersione.

**Stima**: `~8` ore, revisione e chiusura dei rilievi incluse. È la più incerta del progetto — le due feature GUI precedenti hanno sforato di quasi il doppio entrambe.

## Constitution Check

*GATE: da superare prima della Fase 0. Riverificato dopo la Fase 1.*

### Gate prima di iniziare l'implementazione

| # | Requisito | Esito | Dove |
|---|---|---|---|
| 1 | la spec dichiara a quale domanda di business risponde (VI) | **passa** | il report porta `BQ1`, `BQ2` e `BQ3`; l'ordine è quello dell'argomento e non del framework, ed è la decisione `CP-1` |
| 2 | la spec contiene i limiti dichiarati (IV) | **passa** | `FR-013`, `FR-022`, `FR-025`, e le pagine 3 e 10 che esistono per questo |
| 3 | provenienza e confidenza per ogni metrica introdotta (I) | **passa** | `FR-012`; le sei misure nuove non introducono metriche nuove — quattro leggono valori pubblicati, una compone, una converte un'unità |
| 4 | la stima è entro una giornata lavorativa (III) | **passa con riserva dichiarata** | `~8` ore è al limite superiore delle `6-7` ore del principio. La scomposizione è **già avvenuta**: la `010` è stata divisa in `010a` (disegno) e `010b` (costruzione). Se il lavoro risultasse più grande, la spec prescrive di fermarsi e riportarlo invece di comprimere |

### I sei principi

| Principio | Come questa feature vi si attiene | Dove il rispetto è a rischio |
|---|---|---|
| **I — provenienza e confidenza** | ogni valore a schermo porta le due etichette (`FR-012`); nessun numero è digitato in una visuale (`FR-003`, e le linee di riferimento come misure); i valori di `BQ3` sempre come terna (`FR-026`) | la tentazione di digitare una soglia in una visuale invece di leggerla da una misura. È la ragione per cui `M3` esiste |
| **II — riproducibilità** | il DAX è versionato in `contracts/measures.md`; nessuno script scrive in `data/raw/` o `data/processed/` (`FR-041`) | **il `.pbix` non è riproducibile da codice**, ed è il limite strutturale che l'issue `#20` registra. Questa feature lo mitiga rifacendo le tre verifiche, non lo chiude |
| **III — incrementalità** | pagine finite una alla volta; il repository resta coerente alla fine di ogni sessione | la feature attraversa più sessioni. Il vincolo si applica **alla fine di ciascuna**, non solo alla chiusura |
| **IV — trasparenza sui limiti** | è la metà «nella dashboard» che il contratto della `010a` dichiara **non soddisfatta** finché questa feature non chiude | `FR-022` è il presidio: un limite senza il proprio permesso è il difetto che ha fermato la `008b` |
| **V — confine dell'automazione** | tutti i task che toccano la GUI sono **istruzioni per una persona**; il DAX e la narrazione sono artefatti testuali versionati | un task formulato come se un agent aprisse Power BI. Non ne esistono in `tasks.md` |
| **VI — coerenza narrativa** | il report **è** il filo del discorso; è la feature che chiude l'argomento | — |

### Gate prima di considerare la feature conclusa

Verificati alla chiusura, non ora. Sono le prove di [quickstart.md](quickstart.md).

## Project Structure

### Documentation (this feature)

```text
specs/010b-report-costruzione/
├── plan.md                          # questo file
├── spec.md                          # che cosa deve esistere
├── research.md                      # la ricognizione, scritta prima della spec
├── data-model.md                    # che cosa il modello riceve
├── quickstart.md                    # le prove, e l'esito della costruzione
├── checklists/requirements.md       # qualità della spec
├── contracts/
│   ├── measures.md                  # le sei misure DAX, testo letterale
│   └── narrative-contract.md        # il testo a schermo, testo letterale
├── tasks.md                         # /speckit.tasks
└── review.md                        # il verbale della revisione in contesto pulito
```

### Che cosa questa feature tocca fuori dalla propria cartella

```text
README.md                            # tabella di stato, deliverable, prosa, Setup, Struttura (FR-033)
```

**E nient'altro.** Nessun documento di `docs/` viene modificato: `raccomandazione.md` e `roadmap.md` sono esplicitamente fuori perimetro (`FR-038`), e `kpi_operators.md` resta con la propria formulazione esclusa (`FR-042`).

**Structure Decision**: la cartella della feature segue la struttura delle nove precedenti. I due contratti stanno in `contracts/` perché sono **vincoli** e non descrizioni, sul precedente della `008a` e della `008b`.

## Le tre fasi, e i tre punti di fermata

### Fase 0 — la ricognizione *(completata)*

[research.md](research.md), scritta **prima** della spec. Ha prodotto tre accertamenti che il piano usa:

1. **il contratto si legge da solo per costruire, non per capire perché** (`R-1`) — nessuna prescrizione ambigua, tre rinvii che cadono tutti sulle giustificazioni;
2. **gli estremi dell'inviluppo sono identici sui tre assi** (`R-5`) — la scelta della coppia di assi di `V2` non cambia la forma del rettangolo;
3. **l'issue `#21` porta un accertamento contrario a `CP-3`** (`R-3`) — Power BI non offre l'evidenziazione come modalità di risposta per una dispersione né per una tabella.

### Fase 1 — che cosa sarà versionato *(prima di aprire la GUI)*

Tre artefatti testuali, in quest'ordine:

| # | Artefatto | Perché prima della GUI |
|---|---|---|
| 1 | [data-model.md](data-model.md) | dichiara che cosa il modello riceve, e distingue ciò che esiste da ciò che va scritto |
| 2 | [contracts/measures.md](contracts/measures.md) | il DAX è un artefatto testuale e il principio V impone che lo sia. Scriverlo davanti allo schermo lo lascerebbe solo dentro il file binario |
| 3 | [contracts/narrative-contract.md](contracts/narrative-contract.md) | **non si scrive prosa guardando lo schermo.** Si scrive prima, si fa approvare, poi si verifica che ci stia |

**→ Punto di fermata 3**: il contratto di narrazione è approvato **prima** che il `.pbix` venga toccato.

### Fase 2 — la costruzione *(davanti allo schermo)*

L'ordine è vincolato da tre dipendenze reali, non da preferenza:

| Passo | Che cosa | Perché in questa posizione |
|---|---|---|
| **A** | le tre verifiche del modello (issue `#20`) | **prima di leggere qualunque valore.** Un'impostazione riperduta non produce un errore: produce un valore diverso senza segnale. `S-1` è il precedente dei tre KPI sbagliati di due ordini di grandezza |
| **B** | le sei misure nuove, e il confronto di `M1`, `M4`, `M5` con le ancore | le visuali le consumano. Una visuale costruita su una misura non verificata è una visuale da rifare |
| **C** | la verifica di `CP-3` — la sincronizzazione fra le pagine 7 e 8 | **presto, non alla fine.** Esiste un accertamento precedente contrario: se non è ottenibile, l'issue `#21` resta aperta e diventa un ritrovamento. Le pagine 7 e 8 si costruiscono comunque, perché nessun valore dipende da quella sincronizzazione |
| **D** | le dieci pagine, **una alla volta e finita** | ciascuna con le proprie visuali, i propri valori, le proprie etichette, il proprio testo e le proprie interazioni disattivate |
| **E** | la navigazione persistente | dopo che le dieci pagine esistono: una barra che punta a pagine che non ci sono non è verificabile |
| **F** | le prove di [quickstart.md](quickstart.md) e l'esito | — |

**L'ordine delle pagine dentro il passo D** non segue la numerazione. Segue la dipendenza fra ciò che una pagina richiede e ciò che è già stato verificato:

1. **pagine 4, 5, 6** — le tre condizioni, che consumano `M2`-`M5` appena verificate;
2. **pagine 7, 8** — la regione, dove `CP-3` è già stata accertata al passo C;
3. **pagina 9** — gli scenari, che dipendono da `M6` e dalla tabella disconnessa;
4. **pagina 2** — il verdetto, che consuma `M1` e compone le tre condizioni: si costruisce **dopo** che le tre condizioni esistono a schermo, perché è la loro congiunzione;
5. **pagine 1, 3, 10** — la domanda e le due di sola prosa, che non consumano misure.

**Perché la pagina 2 non è la prima.** Porta la congiunzione di tre condizioni; costruirla prima che le tre esistano significherebbe verificarne il conteggio contro nulla.

## Complexity Tracking

> Compilato perché il Constitution Check porta una riserva e una deviazione strutturale.

| Violazione | Perché è necessaria | Alternativa più semplice, e perché è respinta |
|---|---|---|
| **la stima è `~8` ore contro le `6-7` del principio III** | la feature è **già** il risultato di una scomposizione: la `010` è stata divisa in disegno (`010a`, chiusa) e costruzione (`010b`). Dieci pagine finite, sei misure e una narrazione intera non si dividono ulteriormente senza produrre un artefatto incompleto a metà | **dividere in `010b` e `010c`** — per esempio le misure e cinque pagine, poi le altre cinque. Respinta perché lascerebbe su `main` un report a metà, che è precisamente ciò che il principio III vieta con il vincolo di coerenza. La mitigazione adottata è diversa e più onesta: **pagine finite una alla volta**, così che una interruzione lasci un sottoinsieme completo invece di dieci bozze |
| **il `.pbix` non è riproducibile da codice** (principio II) | è strutturale allo strumento, non una scelta di questa feature. Il file binario non è versionabile e nessun controllo del repository può leggerlo | **versionare il `.pbix`** — respinta dalla `008a`: un binario in git non è ispezionabile, e un diff su di esso non dice nulla. La mitigazione è quella registrata nell'issue `#20`: le tre impostazioni si riverificano a ogni riapertura, e l'issue **resta aperta** perché un esito positivo oggi non prova un vincolo per sempre |
| **il principio IV non è soddisfatto nella sua metà «nella dashboard» all'apertura di questa feature** | è la deviazione che il contratto della `010a` §17 registra: le fasce di testo sono riservate e vuote alla chiusura di quella feature | nessuna. **È questa feature a chiuderla**, ed è la ragione per cui esiste |

## Rischi

| Rischio | Probabilità | Che cosa lo mitiga |
|---|---|---|
| `CP-3` non è ottenibile | **alta** — esiste un accertamento precedente contrario (`R-3`) | verificarlo al passo C, presto. Nessun valore dipende da quella sincronizzazione: le pagine 7 e 8 si costruiscono comunque, e l'issue `#21` resta aperta come ritrovamento |
| una visuale non regge davanti allo schermo | media | è **previsto** dal disegno (§19), non è un difetto. Lo scostamento si annota mentre accade |
| un valore letto dal motore diverge da quello pubblicato | media — è già accaduto sulla `007b`, su tre KPI | il confronto una volta per ciascuna misura (`FR-007`), e le tre verifiche del passo A prima di leggere qualunque valore |
| la stima sfora | **alta** — entrambe le feature GUI precedenti hanno sforato di quasi il doppio | pagine finite una alla volta, così che la compressione non avvenga da sé distribuita su dieci pagine a metà. Se sfora, si riporta invece di comprimere |
| il testo a schermo ripete il difetto della `008b` | media | `FR-022` come requisito, `SC-002` come criterio contabile — *zero limiti orfani* — e la rilettura dei nove rilievi dell'issue `#29` **prima** di scrivere |

## Le quattro decisioni che tornano a Valerio

Sono quelle di §18 del contratto di pagina. Il piano non le assume acquisite, e le porta al **punto di fermata 2** insieme a questo documento.

| # | Decisione | Che cosa il piano ne fa | Stato |
|---|---|---|---|
| `CP-1` | il report porta sette KPI su otto; `BQ1-K2` resta fuori | esegue: nessuna pagina lo porta | **da confermare** |
| `CP-2` | le sei misure nuove, di cui `M2` colma un'asimmetria del framework | esegue: `contracts/measures.md` le scrive | **da confermare** |
| `CP-3` | l'issue `#21` si chiude **a condizione** che la sincronizzazione sia ottenibile senza ricalcolare valori | verifica al passo C. **Arriva con un precedente negativo**: l'issue stessa registra che Power BI non offre l'evidenziazione per una dispersione né per una tabella | **condizionata, e a rischio alto** |
| `CP-4` | il conteggio dei membri del quadrante compare, in scostamento dalla `008a` | esegue: pagina 7 lo porta | **da confermare** |

**Su `CP-3`, ciò che il piano chiede a Valerio di sapere prima di confermare.** La decisione è formulata come «si chiude a condizione che la `010b` verifichi». La ricognizione ha trovato che quella verifica ha già un esito precedente, negativo, ottenuto dalla `008a` sullo stesso strumento. Non rende `CP-3` sbagliata — un disegno diverso su due pagine invece che su una può cambiare l'esito — ma sposta la probabilità: **è più probabile che l'issue resti aperta che si chiuda.** Confermare `CP-3` significa quindi accettare che il suo esito più probabile sia un ritrovamento, non una chiusura.
