# Quickstart — le prove di validazione della feature 005

**Feature**: 005 Data Model Design | **Data**: 2026-08-18

Nove prove. Le prime sei sono eseguibili, le ultime tre sono di lettura e le esegue una persona.

**Due vincoli che valgono su tutte**, entrambi nati da difetti reali di questo progetto:

1. **nessuna prova passa per assenza di output.** Ogni prova dichiara che cosa deve **comparire**, non solo che cosa non deve. È il difetto della Prova 9 della `004`, dove un comando falliva su un clone, non produceva righe, e la prova riportava esito positivo;
2. **le prove eseguibili funzionano su un clone privo di `data/raw/`**, che è la condizione in cui il lettore esterno verifica. Nessuna riesegue una pipeline e nessuna richiede i dati di origine.

Prerequisito unico: Python 3 e una copia del repository. Nessuna dipendenza da installare.

---

## Prova 1 — Il controllo di coerenza passa su tutti i documenti

```bash
python3 scripts/check_audit_coherence.py > /tmp/chk.out 2>&1; echo "uscita: $?"
grep -c '^Documento :' /tmp/chk.out
tail -1 /tmp/chk.out
```

**Deve comparire**: `uscita: 0`, poi `4`, poi `ESITO: documenti e artefatti coerenti.`

Prima di questa feature il conteggio vale `3`: le tre sezioni sono `docs/data_audit.md`, `docs/data_cleaning.md` e `docs/bq3_scenarios.md`.

**Fallisce se**: il conteggio resta `3` — il documento nuovo non è registrato — oppure l'uscita è diversa da zero, oppure l'ultima riga non è quella attesa.

**Perché il conteggio si stampa invece di fidarsi dell'uscita**: uno script che non legge affatto il documento nuovo esce comunque con zero. L'uscita dice che ciò che è stato controllato è coerente, non che sia stato controllato tutto.

**Perché conta**: è la prova che ogni quantità di `docs/data_model.md` è legata a un artefatto che la produce, e che nessuna delle registrazioni precedenti si è rotta.

## Prova 2 — Il documento nuovo è sotto severità stretta

```bash
grep -n 'data_model.md' scripts/check_audit_coherence.py
```

**Deve comparire**: una riga che contiene `data_model.md`, `True` e `feature 005`.

**Fallisce se**: la riga non compare, oppure contiene `False` — cioè il documento è registrato ma in regime ad avvisi, che per un documento nuovo la regola di progetto vieta.

**Perché conta**: la severità è la differenza fra un controllo che elenca e uno che ferma. Registrare il documento e lasciarlo ad avvisi sarebbe conforme alla lettera e inutile nella sostanza.

## Prova 3 — Tutti e otto i KPI hanno le tre grane

```bash
for k in BQ1-K1 BQ1-K2 BQ1-K3 BQ2-K1 BQ2-K2 BQ2-K3 BQ3-K1 BQ3-K2; do
  printf '%s: %s\n' "$k" "$(grep -c "$k" docs/data_model.md)"
done
```

**Deve comparire**: otto righe, ciascuna con un conteggio **maggiore di zero**. Nessun KPI può avere conteggio `0`, nemmeno i due di BQ3, che il documento deve nominare per dichiararli fuori dal modello.

**Fallisce se**: anche una sola riga riporta `0`. Un KPI non nominato è un KPI che la `007` dovrà progettare da sé senza saperlo.

**Perché conta**: realizza `SC-001`. La copertura richiesta è 8 su 8 e questa prova la conta invece di darla per buona.

## Prova 4 — Le due note in loco esistono e il testo originale è intatto

```bash
grep -c 'Nota di correzione — 2026-08-18' docs/business_case.md
grep -c 'due granularità distinte e non intercambiabili' docs/business_case.md
grep -c 'segmento musicale (genere/mood)' docs/business_case.md
```

**Deve comparire**: `2` alla prima riga — una nota per §5.2 e una per §4 — e `1` a ciascuna delle altre due.

**Fallisce se**: la prima riporta un numero diverso da `2`, oppure una delle altre riporta `0`. Uno zero significa che il testo originale è stato **riscritto invece che annotato**, che la prassi di correzione degli artefatti già mergiati vieta: il valore originale è la traccia di ciò che quella feature aveva osservato ed è esso stesso un dato.

**Perché conta**: è la sola prova che distingue una correzione da una cancellazione, e la distinzione è il cuore della prassi.

## Prova 5 — Il README non è in drift

```bash
grep -c '005-data-model-design/review.md' README.md
grep -c 'docs/data_model.md' README.md
```

**Deve comparire**: `1` a entrambe.

**Fallisce se**: una delle due riporta `0`. Il collegamento al verbale è la parte che si dimentica più spesso — è successo sulla `003` e di nuovo sulla `004`.

**Perché conta**: il README è l'unico artefatto che ogni feature modifica e che nessuna spec possiede. Il drift vi si è ripetuto due volte, ed è la ragione per cui esiste una casella dedicata nella checklist di consegna.

## Prova 6 — Il perimetro è rispettato

```bash
grep -nE 'CALCULATE|SUMMARIZE|DIVIDE *\(|MEDIANX|\.pbix' docs/data_model.md specs/005-data-model-design/contracts/model-contract.md
echo "uscita: $?"
```

**Deve comparire**: `uscita: 1`, cioè nessuna corrispondenza.

**Fallisce se**: compare una qualunque riga, oppure `uscita: 0`. Una funzione DAX in un artefatto di questa feature è una misura in bozza, che il perimetro vieta; una menzione di `.pbix` come file prodotto è materializzazione.

**Attenzione a come si legge questa prova**: è l'unica in cui l'assenza di output è l'esito positivo, ed è quindi l'unica esposta al difetto che il vincolo 1 esclude. Per questo l'uscita del comando viene stampata: `uscita: 1` è `grep` che ha cercato e non ha trovato, mentre un errore di percorso darebbe `uscita: 2`. I due casi non vanno confusi.

## Prova 7 — Lettura in contesto pulito *(manuale)*

Si consegna a un revisore — sessione separata o subagent isolato — il **solo** `docs/data_model.md`, in una cartella priva di ogni altro artefatto del progetto. Nessuna spec, nessun piano, nessun contratto, nessuna history git.

**Le tre domande**, da porre prima che il revisore legga qualunque altra cosa:

1. che cosa è un segmento, e da dove viene?
2. su quale tabella si conta il catalogo musicale, e perché l'altra darebbe un valore diverso?
3. che cosa questo modello rende **impossibile** misurare?

**Deve comparire**: tre risposte corrette, ricavate dal solo documento.

**Fallisce se**: il revisore deve chiedere un chiarimento, oppure risponde correttamente alla terza domanda elencando solo ciò che il modello abilita. La terza è la più esposta, perché una sezione di limiti si legge volentieri come una formalità.

**Perché conta**: realizza `SC-003` e verifica `FR-002`. È anche l'unico presidio contro un fatto misurato dichiarato come non-misurato, che nessun controllo automatico può vedere.

## Prova 8 — Il verbale esiste, ed è stato scritto prima delle correzioni *(manuale)*

**Deve comparire**: `specs/005-data-model-design/review.md`, con in apertura la dichiarazione di che cosa è stato letto e cosa no, l'ancoraggio alla versione revisionata — commit e impronta del contenuto — e in coda il blocco di chiusura di chi è stato revisionato.

**Nel blocco di chiusura deve comparire**, per **ogni** rilievo, come è stato chiuso, distinguendo *risolvendolo* da *indebolendo l'affermazione*.

**Fallisce se**: il verbale è stato committato **dopo** la modifica del documento. L'ordine dei passi è l'unico presidio contro l'ammorbidimento in trascrizione, e non è verificabile leggendo il verbale: è verificabile solo dalla history.

**Perché conta**: il verbale non è il resoconto della revisione, è la revisione. Senza, restano un conteggio di rilievi che nessuno può verificare e un diff che non dice quale rilievo abbia chiuso cosa.

## Prova 9 — Il documento regge la domanda che nessuno gli ha posto *(manuale)*

Si rilegge la sezione dei limiti di `docs/data_model.md` cercando **una sola cosa**: un'affermazione su ciò che il modello rende impossibile, che il documento **non** avrebbe avuto alcun vantaggio a scrivere.

**Deve comparire**: almeno l'assenza della dimensione di calendario e l'inutilizzabilità del conteggio di righe per dimensionare un segmento. Entrambe dichiarano un limite che nessuno avrebbe notato leggendo lo schema, ed entrambe rendono più difficile, non più facile, l'uso del modello.

**Fallisce se**: ogni limite dichiarato è un limite che il lettore avrebbe comunque scoperto. Una sezione di limiti che elenca solo l'ovvio è una sezione di limiti che non è stata scritta.

**Perché conta**: il principio IV chiede che l'omissione di un limite sia trattata come un'affermazione implicita. Questa prova è l'unica che guarda ciò che **manca** invece di verificare ciò che c'è, ed è per costruzione la più debole — nessun comando la può eseguire.
