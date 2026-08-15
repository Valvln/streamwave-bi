# Come si lavora in questo repository

Contratto operativo per qualunque sessione di agent che lavori su StreamWave BI. Non descrive il progetto — quello lo fanno il [README](README.md) e la [constitution](.specify/memory/constitution.md) — ma **come le sessioni si dividono il lavoro e cosa la toolchain non fa da sola**.

Regola generale, da cui discendono quasi tutte le altre: **se una cosa non è scritta, non accade.** Non dare per scontato che un hook, un automatismo o una convenzione implicita se ne occupi.

## I documenti che governano il lavoro

| Documento | Cosa stabilisce | Chi lo modifica |
|---|---|---|
| [`.specify/memory/constitution.md`](.specify/memory/constitution.md) | i sei principi non negoziabili e i due gate di feature | solo per emendamento formale, con Sync Impact Report e bump di versione |
| [`docs/roadmap.md`](docs/roadmap.md) | ordine delle feature, stime in ore, dipendenze, debito aperto, rischi | la sessione di regia |
| `specs/NNN-nome/spec.md` | cosa la feature attiva deve fare e cosa non deve fare | la sessione esecutiva, tramite `/speckit.specify` |
| `specs/NNN-nome/review.md` | verbale di revisione, dove esiste | una sessione di revisione in contesto pulito |
| [`docs/convenzioni-marcatura.md`](docs/convenzioni-marcatura.md) | la grammatica con cui ogni numero pubblicato è legato all'artefatto che lo produce, e che cosa il controllo garantisce | la feature che estende la grammatica, con nota in coda alla tabella di provenienza |

La constitution prevale su tutto. Questo file non ne ripete i principi né i gate: li presuppone. In caso di conflitto fra le due, vince la constitution e questo file va corretto.

## Ruoli delle sessioni

**Sessione di regia.** Conosce la roadmap e l'esito atteso dell'intero progetto. Il suo output è **testo**: il contenuto delle spec e i prompt di consegna. Revisiona ciò che torna indietro, presidia i gate, misura lo scostamento fra stime e timestamp git.

La regia **non esegue**: non apre branch, non invoca i comandi `/speckit.*`, non crea gli artefatti sotto `specs/`. Le uniche eccezioni sono gli artefatti di governance che le appartengono — `docs/roadmap.md` e gli emendamenti alla constitution — che scrive direttamente e propone al commit.

**Sessione esecutiva.** Riceve un prompt di consegna ed esegue: apre il branch, invoca i comandi, scrive i file, implementa. Si ferma dove il prompt le dice di fermarsi e riporta cosa ha prodotto.

**Sessione di revisione.** Riceve **solo** l'artefatto da revisionare, senza spec, senza piano, senza history git. È l'unica configurazione in cui la revisione dice qualcosa: un revisore che ha visto costruire il documento non può più leggerlo come lo leggerà chi lo riceve. Vedi [`specs/001-business-case-kpi/review.md`](specs/001-business-case-kpi/review.md) come precedente.

Il confine esiste perché una regia che esegue perde il punto di vista esterno da cui revisiona, e i due ruoli collassano in uno.

## Cosa la toolchain non fa da sola

**L'apertura del branch.** Il repository non ha `.specify/extensions.yml` e non ha quindi alcun hook `before_specify`. Spec Kit **non crea il branch**. Chi esegue lo apre a mano, da `main` aggiornato, prima di invocare qualunque comando — e lo chiama come la cartella della feature (`002-data-audit-profiling` ↔ `specs/002-data-audit-profiling`).

**L'aggiornamento del puntatore di feature.** `.specify/feature.json` indica la cartella attiva ai comandi a valle. Va aggiornato quando se ne apre una nuova. La numerazione è `sequential` (`.specify/init-options.json`): la prossima cartella è il numero successivo all'ultimo presente in `specs/`.

**I commit.** Nessun commit viene eseguito di iniziativa, mai. Si propongono messaggio e contenuto, decide Valerio. Vale anche per `git add`, `push`, apertura di PR e merge: sono azioni sue.

**La protezione di `data/raw/`.** È in sola lettura per il principio II e non è versionata. Nessuno script vi scrive dentro. Chi clona il repository la ricostruisce con `scripts/download_data.sh` e un token Kaggle.

## Punti di stop del flusso

Il flusso è `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`. Due fermate obbligatorie, non quattro:

1. **dopo `/speckit.specify`** — la spec torna in revisione prima di diventare un piano. È il punto di massima leva: un errore di perimetro qui si propaga a piano, task e implementazione moltiplicato;
2. **dopo `/speckit.tasks`** — piano e task si possono produrre di seguito, ma non si implementa senza che siano stati visti.

Fuori da queste due, la sessione esecutiva procede senza chiedere conferma a ogni passo.

## Correzione degli artefatti già mergiati

Quando una feature scopre che un artefatto già mergiato contiene un valore errato o un'affermazione ambigua, la correzione è una **nota in loco**: non un'errata separata, non una riscrittura silenziosa.

1. **Il valore originale resta.** Non si cancella e non si sovrascrive: è la traccia di ciò che quella feature aveva osservato, ed è essa stessa un dato.
2. **La nota sta accanto al testo che corregge**, non in fondo al documento né in un file a parte. Chi legge quel passaggio deve incontrare la correzione lì, anche se ci è arrivato da un link diretto.
3. **La nota dichiara**: data, feature che l'ha prodotta, valore o affermazione precedente, valore corretto, causa della divergenza, e la fonte verificabile da cui il nuovo valore proviene.

Se l'affermazione originale è **ambigua e non sbagliata**, non va riscritta. La nota riporta le letture possibili con i rispettivi valori e obbliga chi la cita a valle a dichiarare quale adotta: scegliere al posto di chi ha scritto è una decisione, e spetta a chi ha il contesto per prenderla.

Non tutto ciò che è sbagliato si corregge nel momento in cui lo si trova. Se il difetto è già assegnato a un'altra feature o al debito testuale della roadmap, la feature che lo incontra lo registra come ritrovamento e si ferma lì — precedente: FR-032 della 002.

**Perché in loco e non un'errata.** È una scelta di metodo, non una constatazione, e va difesa come tale: un'errata separata lascia intatto il documento originale ma pretende che chi legge ne conosca l'esistenza; una nota in loco sporca il documento ma raggiunge chiunque legga il passaggio. Per artefatti destinati a essere letti da fuori — che è ciò che questo progetto produce — vince la seconda.

Il precedente esecutivo è il commit `c011103` sulla feature 001. Le correzioni si propongono come commit `fix:` separati, come qualunque altra modifica.

## Le affermazioni derivate sono esse stesse valori

Regola di progetto, nata come decisione **D5 della feature 003** e valida da qui in avanti per ogni documento che pubblichi misure. La feature che l'ha prodotta si è deliberatamente fermata prima di scriverla qui: portarla dagli artefatti di una feature al metodo del progetto è atto di governance, e appartiene alla regia.

> Un confronto, una graduatoria, un rapporto o una differenza costruiti su valori misurati **sono essi stessi valori misurati**. O esistono nell'artefatto con un identificativo proprio e vengono ancorati come qualunque altro numero, o non si scrivono. Non esiste la categoria intermedia dell'affermazione che «si ricava dai numeri già pubblicati e quindi non ha bisogno di fonte».
>
> Tre corollari:
> **(a)** superlativi, ordinali e moltiplicatori riferiti a fatti misurati sono ammessi solo se ancorati a un valore che li sostiene;
> **(b)** i numerali scritti in lettere sono vietati per qualunque fatto misurato;
> **(c)** il controllo di coerenza **fallisce** — non avvisa — su un numerale non ancorato in posizione di fatto misurato.

**Perché è una regola e non un consiglio.** Le tre affermazioni errate che la revisione della 002 ha trovato nel documento di audit erano tutte e tre affermazioni derivate: «il secondo campo più incompleto», «tre delle sei corrispondenze», «un dominio quattro volte più ricco». Nessun valore le conteneva, nessun controllo le verificava, ed erano passate sotto un esito verde. È la zona in cui gli errori si concentrano, perché è l'unica in cui chi scrive calcola a mente.

**Il corollario (c) si realizza spostando l'onere su chi scrive**, non facendo indovinare al controllo se un numerale sia un fatto: ogni numerale porta o l'ancora o il marcatore di non-misurato. L'euristica sulla prosa italiana è vietata dalla 002 e resta vietata.

**Due precisazioni che vanno con la regola**, entrambe dovute al rilievo R7 della revisione della 003:

- **il corollario (b) e la forma «numerale in lettere ancorato» convivono.** Il controllo continua ad accettare quella forma perché la usa il documento della 002; i documenti nuovi non la usano, perché (b) è la regola più severa. La forma non viene rimossa dalla grammatica: rimuoverla romperebbe un artefatto già mergiato per guadagnare una semplificazione che nessuno sta chiedendo;
- **un fatto misurato non deve mai portare il marcatore di non-misurato.** È una dichiarazione materialmente falsa, ed è la categoria che il controllo non può presidiare: contro di essa esiste solo la revisione in contesto pulito.

**La severità stretta di (c) non è retroattiva**: vale per i documenti nuovi ed è dichiarata per documento dentro `scripts/check_audit_coherence.py`. Il documento della 002 resta sotto il regime ad avvisi finché il debito registrato in roadmap non lo chiude.

La grammatica dei marcatori, le esclusioni strutturali e il confine della garanzia stanno in [`docs/convenzioni-marcatura.md`](docs/convenzioni-marcatura.md), che è la fonte unica: un documento pubblicato non delega la propria chiave di lettura a una cartella sotto `specs/`, che il lettore esterno non ha ragione di aprire.

## Convenzioni

- **Lingua**: prosa in italiano, sempre. Identificativi tecnici in inglese: KPI, misure DAX, colonne, tabelle, file, cartelle, branch. Il progetto non verrà tradotto — non scrivere nulla in inglese "per sicurezza".
- **Commit**: in italiano, imperativo, con prefisso convenzionale (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`). La history è parte dell'artefatto da portfolio.
- **Unità di stima**: una giornata lavorativa è **6-7 ore di lavoro effettivo**, non un giorno di calendario (constitution v1.0.2, principio III). Le stime della roadmap sono in ore. Una feature può attraversare più giorni; deve però lasciare il repository coerente **alla fine di ogni sessione**.
- **Nessun numero senza fonte**: ogni valore pubblicato dichiara provenienza e confidenza (principio I). Un numero che compare solo in prosa, senza uno script che lo rigeneri, è un debito — è il rilievo R8 della feature 001.

## Checklist di consegna di un prompt

Vincola la regia, non chi esegue. Un prompt è consegnabile solo se:

- [ ] dichiara **quale branch aprire** e da quale base;
- [ ] dichiara **dove la sessione si ferma** e cosa riporta;
- [ ] dichiara la **stima in ore** e cosa fare se il lavoro sembra più grande — la scomposizione si decide prima di aprire la feature, non dopo;
- [ ] dichiara il **debito ereditato** da feature precedenti, con riferimento puntuale al rilievo o alla divergenza, non con un rimando generico;
- [ ] dichiara il **perimetro**: cosa la feature non fa e a quale feature quel pezzo spetta;
- [ ] richiama le **sezioni obbligatorie** della spec — domanda di business, provenienza e confidenza, limiti dichiarati;
- [ ] **non presuppone alcun automatismo.** Se non è scritto, non accade.
