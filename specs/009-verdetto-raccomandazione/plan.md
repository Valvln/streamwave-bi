# Implementation Plan: Il verdetto e la raccomandazione

**Branch**: `009-verdetto-raccomandazione` | **Date**: 2026-08-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/009-verdetto-raccomandazione/spec.md`

---

## Summary

La feature pubblica `C2` come valore ancorato, applica la regola di decisione già scritta in [`business_case.md`](../../docs/business_case.md) §3 e ne trasforma l'esito in `docs/raccomandazione.md`, il documento che risponde al board.

**L'approccio tecnico in una riga**: nessun artefatto nuovo, nessun dato nuovo, nessuno strumento nuovo — si estende `scripts/build_kpi_measures.py` con una funzione che calcola le condizioni della regola di decisione e il verdetto, e si scrive un documento che legge da lì. Tutto il peso della feature sta nella prosa e nell'argomentazione, non nel codice: le tre righe di aritmetica che servono sono un confronto, una sottrazione e una congiunzione di booleani.

**La ragione per cui il codice è così poco**: i valori esistono già tutti. `C1` e `C3` sono pubblicati dalla `007b`, `BQ1-K3` pure, i sei valori di `BQ3` dalla `004`. Questa feature non misura: **compone e conclude**. È la ragione per cui la stima assegna un'ora allo script e cinque al testo e alla revisione, ed è anche il rischio principale — una feature in cui il codice è banale invita a trattare come banale anche il resto.

---

## Technical Context

**Language/Version**: Python 3 (libreria standard soltanto, come tutti gli script del repository). Nessuna dipendenza da installare.

**Primary Dependencies**: nessuna esterna. `decimal.Decimal` con `getcontext().prec = 28` e `ROUND_HALF_UP` espliciti, già impostati in testa a `scripts/build_kpi_measures.py`.

**Storage**: file versionati. Ingressi in sola lettura: `data/processed/*.csv`, `data/curated/dim_category_mood.json`, `reports/bq3_scenarios.json`. Uscita: `reports/kpi_measures.json`, esteso e non sostituito.

**Testing**: nessun framework. Le verifiche del progetto sono tre comandi: la doppia esecuzione dello script confrontata byte per byte, `python3 scripts/check_audit_coherence.py`, e la revisione in contesto pulito — che è l'unica capace di leggere l'argomentazione, che è la sostanza di questa feature.

**Target Platform**: riga di comando, su una copia del repository. Il passo che rigenera l'artefatto richiede `data/processed/`; il controllo di coerenza no.

**Project Type**: repository di analisi documentale. Nessuna applicazione, nessun servizio, nessuna interfaccia.

**Performance Goals**: irrilevanti. Lo script attuale gira in pochi secondi su ~90.000 tracce; le voci nuove aggiungono aritmetica su valori già in memoria.

**Constraints**: determinismo assoluto — nessuna lettura dell'orologio, nessun generatore casuale, nessuna chiamata di rete; due esecuzioni consecutive producono file identici byte per byte. Nessuna scrittura in `data/`. Nessun accesso al `.pbix`, che non esiste su questa macchina.

**Scale/Scope**: un documento nuovo (~250-350 righe stimate), tre note in loco su documenti esistenti, una funzione nuova nello script, cinque-sei voci nuove nell'artefatto, una riga in `DOCUMENTS`, due righe in `convenzioni-marcatura.md`, quattro punti di aggiornamento sul README.

---

## La decisione tecnica che il piano prende, e che la spec non aveva

### V9 — Il margine si pubblica in due forme, perché la forma assoluta da sola è fuorviante

**Il rilievo che l'ha sollevata.** La regia ha osservato una tensione fra `V1` e `V3`: `V1` argomenta che la soglia `0,50` è quella giusta **e** che la scelta è inconseguente su questi dati; `V3` costruisce poi il margine come distanza fra il valore e quella soglia. Ma il margine **dipende interamente dalla soglia che `V1` ha appena dichiarato inconseguente**. Il rilievo è corretto, e i numeri lo confermano invece di attenuarlo:

| Soglia | Margine assoluto | Sovrastima richiesta, come quota del valore |
|---|---|---|
| `0,50` — maggioranza semplice | `0,3450` | `0,4083` |
| due terzi | `0,1783` | `0,2110` |
| tre quarti | `0,0950` | `0,1124` |

Fra la prima e la terza riga c'è un fattore superiore a tre. **«Inconseguente per l'esito» e «inconseguente per il margine» sono affermazioni diverse, e solo la prima è vera.**

**Le opzioni**: (a) pubblicare il solo margine assoluto rispetto a `0,50`, come `V3` lasciava intendere; (b) rinunciare al margine, tornando alla dichiarazione qualitativa che il rilievo `R19` giudica insufficiente; (c) pubblicare il margine **e** la sovrastima relativa che ne discende, dichiarando esplicitamente che entrambi sono condizionati alla soglia di `D12`; (d) pubblicare un margine per ciascuna delle tre soglie plausibili.

**La decisione**: **(c)**. L'artefatto porta due voci — il margine assoluto e la sovrastima richiesta come quota del valore pubblicato — e la prosa che le accompagna dichiara in modo non eludibile che **entrambe sono condizionate alla soglia**, con la conseguenza scritta per esteso: una soglia più severa restringerebbe il margine.

**La ragione.** (a) è ciò che il rilievo censura: presenterebbe come robustezza del verdetto una quantità che è in parte una proprietà della soglia scelta da chi scrive. (b) rinuncia al contenuto della feature. (d) moltiplicherebbe le voci ancorate per un guadagno nullo: le soglie alternative non sono decisioni del progetto e pubblicarle darebbe loro uno statuto che non hanno.

(c) mantiene l'argomento di robustezza e ne dichiara il condizionamento, che è esattamente la disciplina che questo repository applica ovunque: un numero si pubblica insieme a ciò da cui dipende. **La sovrastima relativa è la forma più difendibile delle due**, perché parla la lingua del limite che sta qualificando — `kpi_measures.md` §4.3 dice che il parallelepipedo *eccede* l'inviluppo convesso, e «di quanto la stima sarebbe gonfiata» è la domanda a cui una quota del valore risponde meglio di una differenza in punti.

**Che cosa questa decisione impone alla prosa**, ed è la parte verificabile dalla revisione: la frase che pubblica il margine deve rendere impossibili **due** letture sbagliate, non una — che il margine sia una stima dell'errore (già in `V3`), e che sia indipendente dalla soglia (nuova, e dovuta a questo rilievo).

**Dove si registra**: nella nota in loco di `kpi_operators.md` che dichiara `D12`, e in `docs/raccomandazione.md` accanto al margine. La spec resta il testo autorevole per `V1`-`V8`; `V9` è una decisione di piano e vive qui.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate di apertura (Workflow, «prima di iniziare l'implementazione»)

| | Condizione | Esito |
|---|---|---|
| 1 | la spec dichiara a quale domanda di business risponde (principio VI) | ✅ `BQ1` in via principale, con contributo dichiarato a `BQ2` e `BQ3` |
| 2 | la spec contiene «Limiti Dichiarati» compilata (principio IV) | ✅ dieci voci, inclusa «dove è esposto all'utente finale» |
| 3 | la spec contiene «Provenienza e Confidenza» per ogni metrica (principio I) | ✅ otto righe, incluse le due voci che non sono misure e sono dichiarate tali |
| 4 | la stima è entro una giornata lavorativa (principio III) | ✅ ~6 ore, sotto il limite di 6-7 |

### Principi, uno per uno

**I — Provenienza e confidenza.** Ogni valore nuovo di questa feature è `Derivato`, e ciascuno elenca le fonti a monte. La confidenza del verdetto è **media**, ereditata dal termine più debole e argomentata in `V5` invece che assunta. I valori di `BQ3` restano a confidenza bassa e compaiono **esclusivamente** come terna best/base/worst, mai isolati — è il vincolo che governa la tabella di sensibilità di `V8`, dove ogni base porta tutti e tre gli scenari.

*Il punto di attenzione, dichiarato invece che dato per scontato*: la soglia di `C2` e le basi di riferimento della tabella di sensibilità **non sono misure**. La prima è una stipulazione di chi analizza, come le soglie mediane di `C1` e `C3`; le seconde sono ipotesi di chi legge. Entrambe portano il marcatore di non-misurato, che è la forma in cui questo repository dichiara che un numero non appartiene agli artefatti.

**II — Riproducibilità totale.** Nessuna modifica manuale ad alcun file di dati. Il valore nuovo lo produce lo script, e chiunque cloni il repository lo rigenera con lo stesso comando. `data/raw/` e `data/processed/` restano in sola lettura.

*La conseguenza operativa che vale la pena scrivere*: il margine di `V3`/`V9` **non si scrive a mano nel documento**, nemmeno essendo una sottrazione fra due numeri già pubblicati. È precisamente la categoria che `D9.3` ha vietato per la North Star, e la roadmap lo ha già scritto una volta in prosa senza ancora — quella riga della roadmap è un precedente da non imitare, non una fonte da citare.

**III — Incrementalità.** ~6 ore, sotto il limite. Il repository resta coerente alla fine di ogni sessione: i punti di fermata cadono dopo `/speckit.tasks` e alla consegna della revisione, ed entrambi lasciano uno stato committabile.

**IV — Trasparenza sui limiti.** È la sostanza del deliverable, non un adempimento: due delle sei sezioni di `docs/raccomandazione.md` — «che cosa lo farebbe cambiare» e «che cosa questa raccomandazione non è» — esistono per questo principio. La riga «dove è esposto all'utente finale» ha qui una risposta reale per la prima volta nel progetto: **il documento stesso è l'esposizione all'utente finale**, non un rimando a una dashboard futura.

**V — Confine dell'automazione.** Nessun task di questa feature tocca una GUI. Il `.pbix` non viene aperto, e nessuna misura DAX viene scritta: le formule di `C1` e `C3` esistono già in `kpi_measures.md`, e `C2` non ne riceve una qui — vedi la nota sotto, in Complexity Tracking, perché è l'unica scelta che merita di essere giustificata.

**VI — Coerenza narrativa.** La feature è l'unica del progetto che serve tutte e tre le domande contemporaneamente, perché è quella che le compone. Nessun rischio di analisi narrativamente inerte: è il contrario, è la feature che chiude il filo.

### Esito

**Nessuna violazione.** Una scelta va comunque giustificata e sta in Complexity Tracking.

---

## Project Structure

### Documentation (this feature)

```text
specs/009-verdetto-raccomandazione/
├── plan.md              # questo file
├── spec.md              # il testo autorevole delle decisioni V1-V8
├── research.md          # Fase 0: le tre domande aperte e come si chiudono
├── data-model.md        # Fase 1: le voci nuove dell'artefatto, con chiave, unità, formula
├── quickstart.md        # Fase 1: come si verifica ciò che questa feature produce
├── contracts/
│   └── document-contract.md   # Fase 1: che cosa docs/raccomandazione.md deve contenere, sezione per sezione
├── checklists/
│   └── requirements.md
├── tasks.md             # Fase 2, prodotto da /speckit.tasks
└── review.md            # il verbale della revisione in contesto pulito
```

**Perché un contratto di documento, sul precedente della `008a`/`008b`.** Le due feature della dashboard hanno scritto il contenuto **prima** di aprire lo strumento, e quell'ordine ha retto anche quando il resto della `008b` non ha retto — è la parte del suo metodo che il verbale ha salvato. Qui vale la stessa logica un livello più in alto: il contratto fissa che cosa ogni sezione deve contenere e quali vincoli ereditati deve rispettare, **prima** che la prosa venga scritta, così che la stesura non possa decidere di suo di saltare un vincolo scomodo. Il contratto è anche ciò che rende verificabile, per la revisione, se una sezione manca invece di essere solo breve.

### Source Code (repository root)

```text
docs/
├── raccomandazione.md          # NUOVO — il deliverable
├── kpi_operators.md            # nota in loco in §12 + riga D12 in §10
├── kpi_measures.md             # nota di aggiunta: C2 esiste e dove vive (chiude #17)
└── convenzioni-marcatura.md    # riga in §5 (severità) + riga nella tabella di provenienza

reports/
└── kpi_measures.json           # esteso: le voci di C2, del margine e del verdetto

scripts/
├── build_kpi_measures.py       # una funzione nuova: build_decision_rule()
└── check_audit_coherence.py    # una riga in DOCUMENTS

README.md                       # riga di stato, deliverable, prosa, Setup, Struttura
```

**Structure Decision**: nessuna struttura nuova. La feature si innesta sull'impianto esistente in cinque punti, tutti già esercitati da feature precedenti: un documento sotto `docs/`, note in loco sui documenti già mergiati, voci nuove nell'artefatto delle misure, una riga in `DOCUMENTS`, l'allineamento del README. **L'unico file nuovo del repository è il deliverable.**

---

## Fase 0 — Ricerca

Vedi [research.md](research.md). Tre domande aperte, tutte chiuse su documenti già nel repository e nessuna che richieda una fonte esterna:

1. **con quale identificativo si pubblicano le voci nuove**, senza collidere con lo spazio dei nomi unito già verificato;
2. **come si scrive un numerale che non è né misurato né una soglia del progetto** — il caso delle basi di riferimento della tabella di sensibilità, che la grammatica copre ma in una categoria che va scelta;
3. **quali affermazioni della raccomandazione esistono già altrove nel repository**, perché sono le sole che possono divergere in silenzio, ed è il ritrovamento della chiusura della `008b`.

## Fase 1 — Progetto

- [data-model.md](data-model.md): le voci nuove dell'artefatto — chiave, etichetta, unità, formula esatta, cifre di presentazione — e la dichiarazione di quali valori esistenti vengono **letti** senza essere ricalcolati.
- [contracts/document-contract.md](contracts/document-contract.md): il contratto di `docs/raccomandazione.md`, sezione per sezione, con i vincoli ereditati che ciascuna deve rispettare e le formulazioni vietate con la ragione del divieto.
- [quickstart.md](quickstart.md): come si verifica, dalla doppia esecuzione al controllo di coerenza, e che cosa un esito verde **non** certifica.

### Constitution Check — seconda valutazione, dopo il progetto

Nessuna delle decisioni di Fase 1 introduce una violazione. Due punti che il progetto ha reso più stringenti invece che più lassi, e che vale la pena registrare:

- il contratto di documento vieta esplicitamente tre formulazioni — «non è scalabile», la lettura del margine come stima dell'errore, la presentazione dei segmenti come alternative disgiunte — ciascuna con la ragione. È il principio IV applicato alla scrittura, non solo alla dichiarazione dei limiti in fondo;
- il modello dati dichiara che il verdetto porta con sé la versione della tabella dei mood. È la condizione 3 delle assegnazioni dell'analista (Vincoli di Dominio e di Dato), che obbliga ogni valore pubblicato a dichiarare su quale versione è calcolato — qui applicata a un valore che dipende dalla tabella per via indiretta, attraverso `C2`.

---

## Complexity Tracking

> Nessuna violazione della constitution. La riga sotto registra una scelta che merita giustificazione perché **si scosta dalla forma che ogni KPI di questo progetto ha finora avuto**, non perché violi un principio.

| Scelta | Perché serve | Alternativa più semplice, e perché scartata |
|---|---|---|
| `C2` e il verdetto **non ricevono una formula DAX** in `docs/kpi_measures.md`, mentre `C1` e `C3` ce l'hanno | Le formule DAX di questo progetto esistono per essere incollate in un modello, e la `008a` ne ha scritte alcune proprio perché servivano a una visuale. Qui non c'è alcuna visuale da alimentare: il report nuovo è della `010a`/`010b`, che deciderà se e come portare il verdetto a schermo. Scrivere ora una formula che nessuno incollerà significherebbe pubblicare, in severità stretta, codice mai eseguito contro il motore — e la `007b` ha dimostrato che il confronto con il motore serve, perché al primo passaggio tre KPI su otto divergevano | Scriverla comunque «per simmetria»: scartata perché la simmetria sarebbe apparente. Le formule di `C1` e `C3` sono state **verificate contro il motore reale** (`E9`, `reports/kpi_engine_check.json`); una formula per `C2` scritta qui non lo sarebbe, e comparirebbe accanto a due che lo sono senza che nulla distingua i due statuti. Se la `010a` deciderà di portare il verdetto a schermo, scriverà la formula e la verificherà — che è l'ordine giusto |

---

## Rischi di questa feature, e come il piano li tiene

**Il rischio principale non è tecnico.** Il codice è banale e questo invita a trattare come banale anche il resto: il valore della feature sta in tre o quattro frasi che devono essere esatte, e sono frasi che nessun controllo automatico può verificare. Il presidio è il contratto di documento scritto prima della prosa, e la revisione in contesto pulito dopo.

**Il rischio di duplicazione**, ed è quello che la chiusura della `008b` ha scoperto sul campo: la raccomandazione ripete affermazioni che vivono già in `business_case.md`, `kpi_measures.md` e `bq3_scenarios.md`. Una divergenza fra le due copie sarebbe invisibile sia al controllo — che verifica le ancore, non le affermazioni — sia a un revisore che riceve estratti isolati. Il piano lo affronta in due punti: la ricerca di Fase 0 censisce le affermazioni duplicate una per una, e il perimetro della revisione va composto perché il revisore possa vedere entrambe le copie.

**Il rischio di compressione.** Se il lavoro sfora, la parte comprimibile è la sezione «che cosa lo farebbe cambiare» — che è la sola che distingue questo documento da un riassunto dei precedenti. La spec lo dichiara, il contratto di documento la elenca fra le sezioni obbligatorie, e la regola è: si riporta lo sforamento, non si comprime.
