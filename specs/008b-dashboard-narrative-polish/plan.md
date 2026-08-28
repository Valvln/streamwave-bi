# Implementation Plan: Dashboard — narrazione, limiti a schermo, rifiniture

**Branch**: `008b-dashboard-narrative-polish` | **Date**: 2026-08-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/008b-dashboard-narrative-polish/spec.md`

## Summary

La feature scrive **prosa dentro un file binario non versionato** e lascia nel repository quattro artefatti testuali: il contratto di narrazione — che porta il testo letterale di ogni blocco, scritto prima che Power BI venga riaperto — l'esito della costruzione, il contratto di pubblicabilità per la `010`, e il verbale di revisione su tutti e tre. Allinea il README e non tocca alcun documento sotto `docs/` salvo eventuali note in loco per un ritrovamento.

**È la seconda feature consecutiva il cui deliverable non è ispezionabile da uno script, e la prima il cui deliverable non è nemmeno un numero.** La `008a` portava a schermo valori: sbagliati o giusti, coincidevano o no con un artefatto, e la verifica era un confronto. Qui il deliverable è un'affermazione in prosa, per cui non esiste né ancora né artefatto che la contraddica. Ne discende l'intera forma del piano: il testo esiste **prima** nel repository e **poi** nel file, e la verifica è la lettura del primo contro il secondo.

**Il lavoro analitico è già chiuso in spec.** Le otto decisioni `N1`-`N8` sono argomentate in [spec.md](./spec.md); questo piano non le riapre, le traduce in blocchi con un ordine dichiarato e un punto di fermata in mezzo. Tre blocchi su nove non sono eseguibili da questa sessione: stanno dentro la GUI, cioè fuori dal confine del principio V.

**Che cosa questa feature chiude, e vale la pena dirlo in apertura.** La prima riga del Complexity Tracking della `008a` — il principio IV non soddisfatto nella sua metà «nella dashboard» — **si chiude qui**. È l'unica deviazione consapevole che il progetto abbia registrato con una feature nominata come rimedio, e questa è quella feature.

## Technical Context

**Linguaggio/Versione**: nessuno. Questa feature non scrive DAX, non scrive Python, non modifica alcuno script. Scrive italiano — che è il vincolo di lingua del progetto (constitution 1.0.1) e, qui, il deliverable

**Dipendenze primarie**: Power BI Desktop, a interazione **manuale** (principio V). Il modello resta quello che la `008a` ha lasciato: nessun ricaricamento è previsto, e se ne servisse uno sarebbe la conseguenza di una verifica `#20` fallita, non un passo pianificato

**Storage**: nessun artefatto nuovo sotto `reports/` o `data/`. Nessun documento nuovo sotto `docs/`, quindi **nessuna riga nuova in `DOCUMENTS` o `ARTIFACTS`** di `scripts/check_audit_coherence.py`, nessuna riga nella tabella di severità né in quella di provenienza di `docs/convenzioni-marcatura.md`. Il `.pbix` non è versionato (`FR-036`)

**Testing**: per esecuzione e per ispezione secondo [quickstart.md](./quickstart.md). Una sola prova eseguibile — `check_audit_coherence.py` verde, che qui certifica soltanto che nulla di pubblicato è stato rotto — e undici prove manuali che richiedono il `.pbix` aperto. **Una di esse è di specie nuova**: la lettura del contratto contro lo schermo, blocco per blocco, che è l'unica forma in cui una prosa a schermo si può verificare

**Piattaforma target**: Power BI Desktop, macchina di Valerio, schermo singolo in rapporto 16:9. La leggibilità del testo si giudica lì, e la leggibilità è metà del deliverable

**Tipo di progetto**: quattro documenti di feature, un contratto di lettura, un allineamento di README. Nessuna applicazione, nessuno script, nessun artefatto generato

**Obiettivi di performance**: nessuno. Questa feature non aggiunge alcuna visuale che calcoli, quindi non tocca alcun tempo di risposta. Il vincolo che ne prende il posto è lo **spazio**: quattro fasce di dimensione fissa, riservate da una feature che non sapeva quanto testo le avrebbe occupate (`N4`)

**Vincoli**: nessuna cifra in un blocco di narrazione fuori dalla lista chiusa (`N2`, `FR-016`); nessuna pagina-tooltip, nessun segnalibro, nessun pannello a scomparsa (`N3`, `FR-023`); nessuna composizione di `C1` e `C3` (`N6`, `FR-019`); nessuna raccomandazione, nessun lessico causale (`N7`, `FR-020`); nessuna visuale legata a un campo, nessun filtro, nessuna modifica al modello o al numero di pagine (`FR-024`); la verifica delle tre impostazioni di `#20` prima di ogni altra operazione (`FR-027`); ~4 ore di lavoro effettivo, **con l'ora di costruzione manuale dentro il conteggio** e non fuori (principio III)

**Scala/Ambito**: 4 pagine invariate, 4 fasce riservate da riempire, 8 KPI di cui spiegare la confidenza, 3 limiti assegnati per nome da `kpi_operators.md` §12, 4 limiti «sconsigliati» da `data_model.md` §18, 3 formulazioni escluse obbligatorie (`FR-003`), 5 issue da lasciare in stato dichiarato, 1 debito di governance da dichiarare a schermo, 1 lista chiusa di numerali, 0 misure nuove, 0 script nuovi, 0 artefatti nuovi

## Constitution Check

*GATE: da superare prima della Fase 0 e da riverificare dopo la Fase 1.*

| Principio | Gate | Pre-Fase 0 | Post-Fase 1 |
|---|---|---|---|
| **I. Provenienza e Confidenza** | ogni numero mostrato in dashboard dichiara fonte e confidenza | ✅ le etichette ci sono già dalla `008a`; questa feature aggiunge il *perché* (`N5`) e non altera alcuna classificazione | ✅ rafforzato dalla Fase 1: `N2` estende il divieto di valore senza fonte alla prosa, che è la sola superficie a schermo su cui non era ancora stato applicato |
| **II. Riproducibilità** | trasformazioni come codice versionato | ✅ nessuna trasformazione: questa feature non tocca alcun dato | ⚠️ **il `.pbix` non è rigenerabile da una copia pulita**, ereditato dalla `005` e conseguenza del principio V. Vedi Complexity Tracking |
| **III. Incrementalità** | completabile in una giornata, o scomposta | ✅ ~4 ore, come da roadmap; è la seconda metà della scomposizione della `008` decisa dalla regia il 2026-08-21 | ✅ regge — vedi «Budget e rischio». Il confine di sosta naturale è il punto di fermata 3 |
| **IV. Trasparenza sui Limiti** | la feature dichiara cosa non risponde, **e nella dashboard dove il consumatore è l'utente finale** | ✅ sezione «Limiti Dichiarati» della spec, con l'elenco di quali limiti restano comunque fuori dallo schermo e perché | ✅ **soddisfatto in entrambe le metà per la prima volta nel progetto.** È il deliverable, non un effetto collaterale: `FR-006`-`FR-015` sono la metà «nella dashboard» |
| **V. Confine dell'Automazione** | nessun task presuppone il pilotaggio di GUI | ✅ nessun task apre Power BI; i tre blocchi che vi entrano sono istruzioni eseguibili da una persona | ✅ invariato. `N1` è la sua conseguenza diretta: ciò che è esprimibile come testo versionabile **deve** esserlo, e la prosa lo è |
| **VI. Coerenza Narrativa** | riconducibile a una domanda di business | ✅ tutte e tre, come la `008a` | ✅ invariato |

**Esito**: nessuna violazione non giustificata. **Una sola** voce in Complexity Tracking, contro le due della `008a`: la prima delle due si chiude con questa feature.

**Un punto di attenzione che il gate non intercetta, e che qui è più acuto che nella `008a`.** Il gate del principio IV chiede che il limite sia dichiarato; non può chiedere che sia *comprensibile*, perché la comprensibilità non è verificabile da alcuna regola. Un blocco di testo formalmente completo e scritto in gergo passerebbe ogni gate di questo piano e mancherebbe interamente il proprio scopo. Contro questo esiste solo la revisione in contesto pulito — ed è la ragione per cui il verbale, qui, deve giudicare il testo *come lo leggerà chi non ha letto nient'altro*, non la sua conformità all'elenco degli obblighi.

## Project Structure

### Documentation (this feature)

```text
specs/008b-dashboard-narrative-polish/
├── spec.md                             # specifica approvata: 8 decisioni N1-N8, 36 requisiti, 13 criteri
├── plan.md                             # questo file
├── research.md                         # Fase 0 — le otto decisioni in formato Decisione/Motivazione/Alternative
├── data-model.md                       # Fase 1 — l'inventario degli obblighi e la loro destinazione a schermo
├── quickstart.md                       # Fase 1 — le dodici prove, e la sezione in cui l'esito verrà scritto
├── contracts/
│   ├── narrative-contract.md           # ★ prodotto nel blocco A, NON in questa fase: è il punto di fermata 3
│   └── publishability-contract.md      # ★ prodotto nel blocco D, dopo l'esito: che cosa la 010 può presupporre
├── checklists/
│   └── requirements.md                 # checklist di qualità, già verificata
├── review.md                           # revisione in contesto pulito — non ancora prodotto
└── tasks.md                            # Fase 2 — prodotto da /speckit.tasks, non da qui
```

**Nessuno dei due contratti è prodotto in questa fase, e le ragioni sono diverse.**

`narrative-contract.md` è l'oggetto del terzo punto di fermata, come `page-contract.md` lo era per la `008a`: scriverlo adesso significherebbe farlo approvare insieme al piano, cioè fondere *come si lavora* e *che cosa si scrive*. Il contratto ha bisogno di essere letto da solo, con l'attenzione che si dà a un testo destinato a un lettore, non in coda a un documento di processo.

`publishability-contract.md` è differito per una ragione che la `008a` ha imparato a proprie spese. Quella feature scrisse `dashboard-contract.md` in Fase 1 e dovette **riallinearlo all'esito reale** in coda (blocco D, T036), perché un contratto scritto prima della costruzione dichiara ciò che si intende costruire e non ciò che esiste. Un contratto che dichiara un file **pubblicabile** è ancora più esposto: scritto prima, ratificherebbe. Qui si scrive dopo l'esito, e questa riga esiste perché la scelta sia leggibile come una correzione di metodo e non come una dimenticanza di Fase 1.

**Dove va l'esito della costruzione.** In coda a `quickstart.md`, nella stessa forma della `008a`: le prove e il loro esito sono la stessa cosa vista prima e dopo, e separarle produce due documenti che si citano a vicenda senza che nessuno dei due si legga da solo.

### Source Code (repository root)

```text
README.md                            # MODIFICATO — riga di stato, deliverable, prosa dei deliverable,
                                     #   e in particolare la frase «Il file è leggibile, non pubblicabile»,
                                     #   che senza questa feature resterebbe su main come affermazione falsa

docs/*.md                            # MODIFICATO SOLO SE un ritrovamento lo impone (FR-030) — nota in loco,
                                     #   nessuna riscrittura del testo o del valore originale
```

**Nessun'altra riga.** Nessuno script nuovo o modificato, nessun artefatto nuovo, nessun documento nuovo sotto `docs/`, nessuna riga in `DOCUMENTS` o `ARTIFACTS`, nessuna modifica alla grammatica dei marcatori.

**`docs/roadmap.md` non è in questo elenco**, deliberatamente: appartiene alla regia (`CLAUDE.md`). La feature riporta; la registrazione è della regia.

**Il `.pbix` non è in questo elenco** perché non entra nel repository (`FR-036`).

**Structure Decision**: come per la `008a`, tutto ciò che sopravvive al merge vive sotto `specs/008b-dashboard-narrative-polish/`, e la cartella della feature non è materiale di lavorazione ma **l'unica traccia ispezionabile del deliverable**. Con una differenza che vale dichiarare: nella `008a` il contratto descriveva il deliverable, qui il contratto **contiene** il deliverable alla lettera. Chi legge `narrative-contract.md` ha letto la dashboard, meno l'impaginazione.

## Ordine di lavoro e punti di sosta

Nove blocchi. Tre — ★1, ★2, ★3 — sono di Valerio e stanno dentro la GUI; il piano li nomina, ne dichiara l'ordine e ne raccoglie l'esito, ma non li esegue.

| # | Blocco | Vincolo di ordine | Esito |
|---|---|---|---|
| **A** | `contracts/narrative-contract.md`: per ogni blocco, pagina e spazio di destinazione, **testo letterale**, obbligo che lo richiede, fonte documentale, formulazione esclusa dove ne esiste una vicina e sbagliata; la lista chiusa dei numerali | dopo il piano e i task | contratto completo; ogni obbligo dell'inventario di [data-model.md](./data-model.md) ha almeno un blocco |
| **⏸** | **PUNTO DI FERMATA 3** — il contratto torna a Valerio per approvazione o correzione, **prima** che Power BI venga riaperto | dopo A | contratto approvato e committato |
| **★1** | Valerio: riapre il `.pbix` e verifica le tre impostazioni dell'issue `#20` — dominio `0-1` sulle tre colonne di mood, conteggio di riga di `dim_title`, colonna di scenario di `bq3_scenarios` | dopo ⏸, **prima di qualunque altra operazione nel file** | esito dichiarato per ciascuna delle tre; se una è persa, si corregge e si dichiara come ricomparsa |
| **★2** | Valerio: inserisce i blocchi di narrazione nelle quattro fasce riservate ed esegue le rifiniture ammesse dal perimetro | dopo ★1 — **mai prima**: scrivere una narrazione corretta accanto a numeri sbagliati è il costo che `E9` ha evitato alla `007b` | testo a schermo su tutte e quattro le pagine; scostamenti annotati **mentre accadono** |
| **★3** | Valerio: legge il contratto approvato accanto allo schermo, blocco per blocco, e verifica coincidenza del testo, assenza di cifre fuori lista, assenza di composizione `C1`/`C3` | dopo ★2 | coincidenza, oppure differenza dichiarata come scostamento |
| **B** | `quickstart.md`, sezione «Esito della costruzione»: che cosa è a schermo pagina per pagina, gli scostamenti con la ragione, l'esito di ★1 e ★3, lo stato delle cinque issue, la dichiarazione di pubblicabilità contro le cinque condizioni di `N8` | dopo ★2 e ★3 | esito completo; chi legge sa che cosa la dashboard dice senza aprirla |
| **C** | note in loco su un documento di `docs/`, **solo se** un ritrovamento le impone (`FR-030`) | dopo B | zero note se nessun ritrovamento — ed è l'esito atteso, non un'omissione |
| **D** | `contracts/publishability-contract.md`: che cosa la `010` può presupporre, che cosa «pubblicabile» non significa, che cosa resta a suo carico | dopo B, **mai prima** | contratto coerente con ciò che esiste, non con ciò che si intendeva costruire |
| **E** | revisione in contesto pulito su `narrative-contract.md` e sulla sezione di esito → `review.md`, committato **prima** di qualunque correzione (i quattro obblighi di `CLAUDE.md`) | dopo D | verbale esiste ed è committato |
| **F** | chiusura dei soli rilievi strettamente necessari; gli altri come issue con numero; stato dichiarato delle cinque issue; README allineato; riesecuzione di `check_audit_coherence.py`; riporto finale | dopo E | feature conclusa |

**Il punto di massima leva è A, e per una ragione diversa dalla `008a`.** Là il contratto disegnava una struttura e l'errore intercettabile era di disegno — una visuale che non regge la forma del dato. Qui il contratto **è** il deliverable: un blocco di testo approvato è un blocco di testo pubblicato, meno la trascrizione. Il punto di fermata non intercetta un errore che costerebbe di rifare le pagine; intercetta un'affermazione sbagliata prima che diventi l'unica cosa che un lettore esterno leggerà.

**Se la giornata si spezza, il confine di sosta è ⏸**, come sulla `008a`: esistono spec, piano, task e contratto approvato, e non esiste ancora nulla che possa contraddirli. Ogni altro confine cade in mezzo a ★2, dove metà delle fasce sono piene e l'esito non è scrivibile.

**Il vincolo d'ordine da rendere esplicito è ★1 prima di ★2**, e regge sullo stesso precedente della `008a`: tre impostazioni fragili si sono già perse una volta ciascuna, e nessun controllo del repository può vederle. Costa una lettura verificarle; non verificarle costa di scrivere «questo valore misura X» sotto un numero che non misura più X.

## Budget e rischio

| Blocco | Ore | Contenuto |
|---|---|---|
| A | 1,5 | il contratto di narrazione: quattro pagine, il testo letterale di ogni blocco, obblighi, fonti, formulazioni escluse, lista chiusa |
| ★1 | 0,1 | le tre verifiche dell'issue `#20` |
| ★2 | 0,9 | costruzione manuale: inserimento dei blocchi nelle quattro fasce, rifiniture |
| ★3 | 0,1 | la lettura del contratto contro lo schermo |
| B | 0,4 | l'esito, con gli scostamenti e la dichiarazione di pubblicabilità |
| C | 0,1 | note in loco, se servono — zero se nessun ritrovamento |
| D | 0,1 | il contratto di pubblicabilità per la `010` |
| E | 0,6 | revisione in contesto pulito |
| F | 0,2 | chiusura dei rilievi necessari, issue, README, riporto |
| | **4,0** | |

**La costruzione manuale è dentro la stima**, come nella `008a` e per la stessa ragione: escluderla misurerebbe una convenzione contabile invece del lavoro.

**Il rischio maggiore è in A, ed è di registro, non di contenuto.** Un blocco può essere esatto contro ogni fonte e restare illeggibile per il destinatario dichiarato — un decisore che non ha letto nulla. È la classe di difetto che nessun gate di questo piano intercetta, perché tutti i gate verificano la conformità a un obbligo e nessuno verifica che la frase si capisca. Il presidio è la revisione in contesto pulito, e il piano le assegna esplicitamente questo metro invece della conformità.

**Il secondo rischio è che la lista chiusa di `N2` si allarghi in costruzione.** Un numero comodo — la quota di film, il conteggio dei segmenti marcati — è a portata di mano mentre si scrive, e nessuno script se ne accorgerebbe mai. Il presidio è ★3, che cerca esplicitamente cifre fuori lista, e la sua efficacia dipende dal fatto che sia eseguito come lettura e non come ricordo.

**Il terzo rischio è lo spazio.** Le quattro fasce sono state riservate dalla `008a` senza sapere quanto testo le avrebbe occupate, e la fascia di `BQ3` — che la `008a` ha dichiarato «la più alta delle quattro» — deve ospitare tre assunzioni, quattro limiti e un debito di governance. `N4` dichiara la reazione: si taglia il testo, si dichiara che cosa si è tagliato, e solo se nemmeno il minimo entra si registra uno scostamento dal disegno della `008a`.

**Il quarto rischio è la ricomparsa di una delle tre impostazioni di `#20`**, con una probabilità che nessuno conosce. Costa 0,1 ore controllarlo e costerebbe l'intera ★2 non controllarlo.

**Ciò che non è un rischio**: `check_audit_coherence.py`, che resta verde perché questa feature non tocca nulla di ciò che controlla. Il piano lo dice apertamente invece di rivendicare quel verde come una garanzia sul proprio deliverable — che è, letteralmente, la sola cosa nel repository che quel controllo non può leggere.

## Complexity Tracking

> Una violazione consapevole, ereditata e non introdotta qui. Erano due nella `008a`: la prima si chiude con questa feature.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **Principio II**: il `.pbix` non è rigenerabile da una copia pulita del repository | è la conseguenza diretta del principio V, che colloca la GUI di Power BI Desktop fuori dall'automazione, e della scelta di non versionare un file che incorpora i dati. Vale dalla `005` e non è introdotta qui | l'alternativa sarebbe versionare il `.pbix`, che porterebbe nel repository copie dei dati che `data/processed/` tiene fuori per scelta, oppure generarlo da uno script, che significa pilotare la GUI. La mitigazione è che tutto ciò che nel `.pbix` è esprimibile come testo — schema, mapping, misure DAX, il disegno delle pagine, **e ora la prosa** — è testo versionato, che è esattamente ciò che il principio V prescrive |

**La riga che si chiude, dichiarata invece di sparire.** La `008a` registrò come deviazione consapevole il principio IV non soddisfatto nella sua metà «nella dashboard», con la mitigazione che la `008b` sarebbe stata la feature successiva in roadmap e non un rinvio indefinito. Questa feature onora quella mitigazione: alla sua chiusura i limiti sono a schermo e la deviazione non esiste più. Sta scritto qui perché una deviazione che sparisce senza che nessuno dichiari dove è andata è indistinguibile da una deviazione dimenticata.
