# Quickstart: verifica della narrazione e delle rifiniture della `008b`

**Feature**: 008b-dashboard-narrative-polish | **Data**: 2026-08-27

Dodici prove, in ordine di esecuzione. **Una sola è eseguibile da chi ha clonato il repository**; le altre undici richiedono il `.pbix` aperto e non saranno mai automatizzabili — è il principio V, non una lacuna di questo documento. Il loro esito è un'osservazione umana, dichiarata come tale nella sezione finale, sulla stessa forma già usata da `E9` della `007b` e dalle dodici prove della `008a`.

**Che cosa distingue queste prove da quelle della `008a`.** Là si confrontavano numeri: una prova aveva un esito binario che chiunque, con il file aperto, avrebbe replicato. Qui **sette prove su dodici confrontano un testo con un altro testo**, e una — la prova 4 — verifica un'esaustività. Sono verifiche di lettura, non di misura, e vale la pena dirlo prima che qualcuno legga un esito verde come se avesse la stessa forza di quello della `007b`.

## Prerequisiti

- Il `.pbix` nello stato in cui la `008a` lo ha lasciato: quattro pagine, otto KPI a schermo, quattordici misure, otto tabelle, cinque relazioni, quattro fasce vuote riservate.
- `data/processed/` presente, nel caso una verifica della prova 2 imponga un ricaricamento.
- Il contratto di narrazione [approvato](./contracts/narrative-contract.md) e committato.
- L'inventario degli obblighi di [data-model.md](./data-model.md) §3, che è la lista contro cui la prova 4 si esegue.

---

## Le dodici prove

### 1 — Nulla di pubblicato è stato rotto *(eseguibile)*

```bash
python3 scripts/check_audit_coherence.py
```

Atteso: **esito verde**, invariato rispetto al merge della `008a` — sette documenti, sei artefatti. Questa feature non aggiunge documenti né artefatti.

**Che cosa questo verde certifica, e che cosa no.** Certifica che le note in loco eventualmente scritte nel blocco C non hanno rotto alcuna ancora. **Non dice nulla sul deliverable**, e qui meno che mai: il deliverable è prosa dentro un file binario, cioè la sola cosa nel repository che quel controllo non può leggere per costruzione.

### 2 — Le tre impostazioni fragili dell'issue `#20` *(manuale, ★1 — prima di ogni altra cosa nel file)*

Tre ispezioni, da eseguire **prima** che venga scritto un solo blocco di testo.

| Impostazione | Che cosa ispezionare | Atteso |
|---|---|---|
| tipizzazione delle colonne di mood (issue `#11`) | `energy`, `valence`, `danceability` di `dim_track` | valori nel dominio `0-1`. Un valore nell'ordine delle centinaia è la ricomparsa del difetto che `E9` trovò nella `007b` |
| lettura dei CSV sull'origine di `dim_title` | il conteggio di riga di `dim_title` | coincide con quello che la `008a` ha lasciato dopo la correzione a `QuoteStyle.Csv`. Un conteggio maggiore è la ricomparsa del difetto di caricamento |
| colonna di scenario di `bq3_scenarios` | le colonne della tabella disconnessa | la colonna che nomina lo scenario è presente. Senza di essa i sei valori sono sei numeri senza l'etichetta che dice a quale ipotesi ciascuno appartiene |

Se una delle tre è persa: **la narrazione si ferma**, la correzione precede, il fatto si dichiara nell'esito come ricomparsa, e si esegue la prova 12.

### 3 — La struttura della `008a` è invariata *(manuale)*

Atteso: **quattro** pagine, **otto** tabelle, **cinque** relazioni, **quattordici** misure, e nessun filtro né slicer su alcuna pagina. Nessuna visuale legata a un campo è stata aggiunta.

È la prova del perimetro (`FR-024`): questa feature aggiunge caselle di testo e forme, e ogni altra differenza rispetto a ciò che la `008a` ha lasciato è un ritrovamento o uno scostamento, mai una libertà.

### 4 — Ogni obbligo ha almeno un blocco, e ogni blocco serve un obbligo *(manuale, ★3)*

Percorrere l'inventario di [data-model.md](./data-model.md) §3 riga per riga e trovare, per ciascun `OB`, il blocco a schermo che lo soddisfa. Poi percorrere i blocchi a schermo e trovare, per ciascuno, l'obbligo che lo richiede.

Atteso: **corrispondenza in entrambe le direzioni**. Un obbligo senza blocco è una dimenticanza e si chiude prima del riporto. Un blocco senza obbligo è testo che qualcuno ha voluto scrivere, e in una feature governata dal principio IV va giustificato nell'esito o rimosso.

### 5 — Il testo a schermo coincide con il contratto approvato *(manuale, ★3)*

Leggere il contratto accanto allo schermo, blocco per blocco.

Atteso: **coincidenza alla lettera**. Una differenza è uno **scostamento** e si dichiara con la propria ragione; non si corregge in silenzio né sul contratto, che è stato approvato, né a schermo, che è ciò che il lettore vedrà.

### 6 — Nessuna cifra fuori dalla lista chiusa *(manuale, ★3)*

Percorrere ogni blocco cercando le cifre.

Atteso: nessuna, salvo le voci della lista chiusa dichiarata nel contratto. Una cifra in più è una violazione di `N2` e si toglie prima del riporto — **non** si sana verificando che coincida con il valore pubblicato, perché la coincidenza di oggi non è la proprietà che `N2` richiede.

Atteso inoltre: dove i due anni di copertura compaiono, il loro statuto è distinto — osservato sul lato video, dichiarato dalla fonte sul lato musicale (`FR-018`).

### 7 — Nessuna composizione della regola di decisione *(manuale)*

Atteso: `C1` compare su `BQ1` e `C3` su `BQ2`, ciascuna nominata **da sola**, ciascuna accompagnata dalla dichiarazione che da sola non decide. **Nessuna pagina** conta le condizioni, nomina `C2`, usa un ordinale o una frazione riferiti a esse, o pubblica un esito complessivo.

È il presidio contro un verdetto che nessuno ha misurato, ereditato da `F6` della `008a` ed esteso alla prosa da `N6`.

### 8 — Nessuna conclusione, nessuna causa, nessuna persona *(manuale)*

Atteso: nessun blocco formula una raccomandazione, un verdetto o una previsione; nessun lessico causale su una relazione fra attributi di catalogo; nessun superlativo o ordinale riferito a un fatto misurato non visibile a schermo; nessuna affermazione sul comportamento delle persone.

**Il caso che va cercato per primo** è la parola «domanda», che è a schermo dalla `008a` e che una prosa distratta trasforma in un comportamento osservato. Sulla pagina `BQ2` deve essere dichiarato che nomina un indice della fonte (`OB-33`).

### 9 — Le tre formulazioni escluse non compaiono *(manuale)*

Atteso: a schermo non compaiono, in nessuna forma,

- «differenza fra la durata del catalogo video e quella del catalogo musicale» o qualunque variante che sottintenda i due cataloghi interi (`OB-09`);
- «domanda bassa» riferita ai segmenti marcati (`OB-14`);
- «l'uplift non è scalabile» o qualunque variante che presenti come impossibile un'operazione che è soltanto non fornita (`OB-31`).

Sono le tre formulazioni più comode delle rispettive corrette, e la terza è dichiarata **falsa** alla lettera da `bq3_scenarios.md` §8.

### 10 — Il testo è sempre visibile *(manuale)*

Atteso: nessuna pagina-tooltip, nessun segnalibro, nessun pannello a scomparsa, nessun pulsante che scopra o nasconda un blocco. Nessun limite dichiarato è raggiungibile solo con un'azione dell'utente.

Atteso inoltre: le pagine restano **quattro** — una pagina-tooltip sarebbe la quinta, anche se nascosta.

### 11 — Le sigle sono sciolte dove compaiono *(manuale)*

Atteso: ogni sigla che il testo di questa feature usa è sciolta sulla stessa pagina. Non copre le sigle già a schermo dalla `008a` sulle quali questa feature non scrive; copre quelle che i blocchi introducono.

### 12 — I valori a schermo coincidono ancora con i pubblicati *(manuale, condizionale)*

**Si esegue solo se la prova 2 ha imposto una correzione.** Per ciascuno degli otto KPI, confrontare il valore letto a schermo con quello di `docs/kpi_measures.md` alla stessa grana.

Atteso: coincidenza. Una divergenza è un **ritrovamento**: si dichiara con nota in loco sul documento della `007b`, senza riscrivere il valore originale né correggere lo schermo in silenzio.

**Se la prova 2 è passata su tutte e tre le voci, questa prova non si esegue**, e la sua non esecuzione si dichiara — non si finge un esito che nessuno ha osservato.

---

## Esito della costruzione

**Costruzione eseguita fra il 2026-08-27 e il 2026-08-28.** Le voci degli scostamenti sono state scritte mentre accadevano, ciascuna con la propria data; le sezioni di sintesi sono state compilate a chiusura, nella Fase 7.

**Questa sezione, non il contratto di narrazione, è la fonte autorevole su ciò che esiste a schermo.** Il contratto dichiara che cosa si era deciso di scrivere; dove i due divergono, la divergenza è elencata qui sotto con la propria ragione (`F9` della `008a`, ereditata).

### Che cosa è a schermo, pagina per pagina

| Pagina | Obblighi atterrati | Blocchi | La fascia è bastata? |
|---|---|---|---|
| **Ingresso** | `OB-01`-`OB-04` | quattro: `BL-IN-1`, `BL-IN-2`, `BL-IN-3` nella fascia sotto la scheda della North Star; `BL-IN-4` nella striscia a piè di pagina | **no**, e la reazione è stata doppia: `BL-IN-3` è stato accorciato (`SC-1`) e il testo residuo scorre (`SC-3`) |
| **`BQ1`** | `OB-05`-`OB-12`, `OB-35` | nove: `BL-Q1-1`, `BL-Q1-1b`, `BL-Q1-2`, `BL-Q1-3` sull'area della metrica di riferimento; `BL-Q1-4`, `BL-Q1-5` sulla differenza di durata; `BL-Q1-6`, `BL-Q1-7`, `BL-Q1-8` sulla sovrapposizione | **no**, il testo scorre (`SC-3`). Nessun blocco tagliato |
| **`BQ2`** | `OB-13`-`OB-23`, `OB-33` | dieci: `BL-Q2-1` … `BL-Q2-10` | **no**, il testo scorre (`SC-3`). Nessun blocco tagliato, nemmeno i tagliabili `BL-Q2-9` e `BL-Q2-5` |
| **`BQ3`** | `OB-24`-`OB-32` | nove: `BL-Q3-1` … `BL-Q3-9` | **no**, il testo scorre (`SC-3`). Nessun blocco tagliato, `BL-Q3-9` compreso |

`OB-34` è trasversale e non ha blocco proprio: è servito dagli scioglimenti di `C1` in `BL-Q1-3` e di `C3` in `BL-Q2-8`, che sono le uniche sigle introdotte da questa feature.

**Trentadue blocchi, trentacinque obblighi, quattro pagine — le stesse quattro che la `008a` ha lasciato.** Nessuna pagina è stata aggiunta, nessuna visuale legata a un campo, nessun filtro, nessuna modifica al modello.

**L'ordine di taglio previsto dal contratto non è mai stato usato**, ed è il fatto che spiega `SC-3`: davanti a fasce insufficienti si è scelto di tenere il testo intero e accettare lo scorrimento, invece di tagliare come `N4` prescriveva.

### Gli scostamenti dal contratto approvato

> **Sezione in compilazione.** Le voci si scrivono **mentre accadono**, non a memoria alla fine (`T014`, `T019`). Alla chiusura della Fase 7 questa nota va tolta e la sezione dichiarata completa; se resterà vuota, «zero scostamenti» va scritto per esteso invece di lasciare il silenzio a significarlo.

#### `SC-1` — `BL-IN-3`, testo tagliato per pareggiare l'altezza delle fasce

**Data**: 2026-08-28 · **Pagina**: ingresso · **Blocco**: `BL-IN-3` · **Categoria**: scostamento (`F9`)

**Che cosa il contratto scrive**: il blocco apre dichiarando che accanto a ogni indicatore compare un livello, enumera i tre livelli per esteso, e chiude con due frasi — che l'etichetta non dice quanto il numero descriva StreamWave, e che anche un indicatore a confidenza alta è alto rispetto al catalogo di riferimento.

**Che cosa è stato costruito**: una versione più corta, che apre direttamente sul criterio, accorcia le tre definizioni e tiene una sola delle due frasi di chiusura.

**La ragione, dichiarata come è**: **non è una fascia insufficiente.** Le altre pagine entravano senza scorrimento, e il taglio è stato scelto per allineare l'altezza di questa fascia alle altre. È una ragione **estetica**, non di capienza, e `N4` non la prevede: `N4` disciplina il caso in cui il testo non entra. Va quindi registrata per quello che è — una decisione di uniformità presa davanti allo schermo — e non travestita da vincolo di spazio.

> **Nota in loco — 2026-08-29, feature `008b`. La premessa di questa ragione è contraddetta dallo stesso documento.**
>
> **Affermazione precedente**: *«Le altre pagine entravano senza scorrimento»*.
>
> **Affermazione corretta**: **non entravano.** La tabella «Che cosa è a schermo, pagina per pagina», venti righe più sopra, dichiara per `BQ1`, `BQ2` e `BQ3` — tutte e tre — *«no, il testo scorre (`SC-3`)»*, e `SC-3` porta in intestazione **Pagine: tutte e quattro**. Nessuna delle altre pagine entrava senza scorrimento.
>
> **Le due letture possibili, e questa nota non sceglie fra loro** perché chi scrive oggi non ha modo di stabilire quale sia vera:
> - **`SC-1` fu scritto prima che si scoprisse lo scorrimento delle altre pagine e non è stato rivisto.** In questa lettura la ragione era vera nel momento in cui è stata scritta ed è falsa adesso — ed è, va detto, l'effetto rovesciato della disciplina del «si scrive mentre accade», che questo documento adotta proprio per non ricostruire a memoria;
> - **la ragione registrata non è quella vera.** In questa lettura il taglio ha avuto un'altra causa, e l'uniformità estetica è una ricostruzione a posteriori.
>
> **In nessuna delle due letture il taglio resta motivato**, ed è il taglio che ha portato via l'enunciato generale di `OB-03`. Chi cita questo passaggio a valle dichiari quale lettura adotta.
>
> **Che cosa questa nota non tocca**: la ragione resta dichiarata come **estetica** e non travestita da vincolo di spazio. Il revisore registra quel gesto fra ciò che funziona e non va perso chiudendo il rilievo: la premessa è sbagliata, l'onestà con cui la ragione è stata nominata no. Sono due cose diverse, e questa nota corregge la prima.
>
> **Da notare, in tensione con la nota**: la tabella «Che cosa è a schermo» attribuisce il taglio alla capienza — *«no, e la reazione è stata doppia: `BL-IN-3` è stato accorciato (`SC-1`)»* — cioè esattamente alla ragione che `SC-1` nega con enfasi. Anche la tabella e lo scostamento dicono due cose diverse sullo stesso fatto.
>
> **Fonte verificabile**: [`review.md`](./review.md), rilievo `R5` punto (a), che confronta questo passaggio con la tabella delle pagine e con l'intestazione di `SC-3`.

**Che cosa il taglio è costato, oltre a quanto già registrato in §13.1 del contratto**:

- cade *«Questa etichetta non dice quanto il numero descriva StreamWave»*, che era l'enunciato generale; resta il caso particolare che lo esemplifica. `OB-03` è servito, e la sua seconda metà — che la scala non misura la trasferibilità — è ora affidata a un esempio invece che a una regola;
- cade *«senza corrispondenze costruite né ipotesi interposte»* dalla definizione di *alta*, cioè il contrappunto che rendeva leggibili *media* e *bassa*;
- cade *«e per questo si presenta sempre come intervallo, mai come valore singolo»*, che il contratto aveva già spostato su `BL-Q3-1`: nessuna perdita ulteriore.

**Un difetto di trascrizione dentro lo scostamento, che non è parte dello scostamento.** La riga di *bassa* è stata inserita troncata:

```text
Bassa: il numero dipende da ipotesi che i dati disponibili .
```

La frase si interrompe a metà e non afferma nulla. **Va riparata a schermo prima di chiudere `T013`**, e la riparazione non riapre il contratto: è la stessa versione accorciata, completata. Testo da inserire:

```text
Bassa: il numero dipende da ipotesi non verificabili con i dati disponibili.
```

Manca inoltre il punto finale all'ultima frase del blocco.

#### `SC-2` — `BQ1`, etichetta di confidenza di `BQ1-K2` errata a schermo

**Data**: 2026-08-28 · **Pagina**: `BQ1` · **Categoria**: scostamento dal contratto di pagina della `008a`, non ritrovamento

**Che cosa è stato trovato**: l'etichetta di `BQ1-K2` riportava `Derivato (Netflix + Spotify) · Confidenza: media`.

**Che cosa dicono gli artefatti**: `business_case.md` §5.4, `kpi_operators.md` §11 e il contratto di pagina della `008a` §1.1 dichiarano tutti e tre **alta**, e la scala di `business_case.md` §6 lo conferma per costruzione — due durate osservate e una sottrazione, senza mappature interposte. La fonte era corretta, la confidenza no.

**Perché non è un ritrovamento**: `F9` della `008a` chiama ritrovamento la differenza fra un valore letto a schermo e il valore pubblicato, e impone la nota in loco. Qui **nessun documento pubblicato sbaglia**: sbaglia la trascrizione a schermo, ed è la categoria che si corregge nel file e si dichiara qui. Nessuna nota in loco è dovuta.

**Perché si chiude subito e non si rinvia**: senza la correzione il file pubblica un'etichetta che contraddice tre artefatti, accanto al blocco `BL-Q1-4` che spiega perché quella confidenza è alta. È la soglia dello *strettamente necessario* — il deliverable, senza la correzione, afferma il falso.

**Che cosa questo dice sul presidio**: l'errore è nato in una trascrizione manuale di un'etichetta, cioè nell'unica classe di contenuto che la `008a` aveva portato a schermo senza che alcuno script potesse rileggerla. La prova 3 di questo quickstart verifica la struttura e la prova 12 i valori; **nessuna delle dodici prove verifica le etichette**, ed è una lacuna del disegno di questa feature, trovata perché un blocco di narrazione le stava accanto e la contraddiceva. È il tipo di riscontro che la prova 5 produce per caso e non per costruzione.

#### `SC-3` — Le fasce non mostrano il testo in un pezzo solo: le caselle scorrono

**Data**: 2026-08-28 · **Pagine**: tutte e quattro · **Categoria**: scostamento, e conformità parziale a `FR-023`

**Che cosa è stato costruito**: tutti i blocchi del contratto sono a schermo, su tutte e quattro le pagine, e nessuno è stato tagliato per farvi entrare. Nessuna fascia però li mostra **interi in un colpo d'occhio**: le caselle di testo eccedono lo spazio e la parte in eccesso si raggiunge scorrendo.

**Perché non è il caso previsto da `N4`**: `N4` prescrive di tagliare il testo quando la fascia non basta, e di dichiarare il taglio. Qui non si è tagliato — si è scelto di tenere il testo intero accettando lo scorrimento. È la decisione opposta a quella che `N4` prevede, presa davanti allo schermo, e va registrata come tale invece di essere assorbita.

**Che cosa questo fa a `FR-023`.** Il requisito ha due metà. La prima — nessuna pagina-tooltip, nessun segnalibro, nessun pannello a scomparsa — è **rispettata**: nessuno dei tre esiste. La seconda dice *«nessun limite dichiarato DEVE essere raggiungibile solo con un'azione dell'utente»*, e lo scorrimento è un'azione dell'utente. Su quella metà la conformità è **parziale**.

**La differenza che rende lo scorrimento meno grave dei tre divieti, e che non la annulla.** L'argomento di `N3` è che *«un limite raggiungibile con un clic si legge solo se qualcuno sospetta che esista»*. Una barra di scorrimento non ha quel difetto: **dichiara la propria esistenza**, e chi vede il testo tagliato a metà sa che continua. Un segnalibro no, una pagina-tooltip nemmeno. Resta che chi non scorre non legge, e la seconda metà di un blocco è precisamente dove il contratto ha già registrato — §13.1 — che sta la parte prescrittiva.

**Che cosa questo non tocca**: la dichiarazione di pubblicabilità. Le cinque condizioni di `N8` nominano `N2`, `N6` e `N7`, non `N3`. Il criterio è stato fissato prima di costruire e non si allarga adesso; il contratto di pubblicabilità del blocco D dovrà però **elencare lo scorrimento fra ciò che «pubblicabile» non garantisce**, o prometterebbe una leggibilità che il file non ha.

**Che cosa resta aperto, e dove**: l'autore dichiara di voler valutare pagine dedicate alla prosa fra una pagina-grafico e l'altra, con le sole note indispensabili accanto alle misure. Comporta di riaprire il numero di pagine, che la `008a` chiude a quattro, ed è quindi fuori dal perimetro di questa feature. È registrata come issue `#27`, senza alcuna decisione presa.

### Che cosa è stato tagliato, e perché

**Un solo blocco è stato tagliato in costruzione: `BL-IN-3`.** Il taglio è documentato in `SC-1`, con la sua ragione — allineare l'altezza delle fasce, non una fascia insufficiente — e con ciò che è costato: `OB-03` resta servito, ma la sua seconda metà, che la scala non misura la trasferibilità, è ora affidata a un esempio invece che a un enunciato.

**Nessun altro blocco è stato tagliato**, su nessuna delle quattro pagine, `BL-Q2-9` e `BL-Q2-5` compresi — che erano i due che il contratto designava come primi da sacrificare. Dove il testo non entrava si è scelto lo scorrimento (`SC-3`).

**Un taglio diverso, avvenuto prima e non qui.** I nove obblighi che il contratto elenca in §13.1 come «soddisfatti in parte» non sono tagli di costruzione: sono accorciamenti decisi in **revisione del contratto**, prima che il file venisse riaperto, e stanno lì con il proprio dettaglio. La distinzione conta per chi legge: un accorciamento in revisione è passato per un'approvazione, un taglio in costruzione no.

### L'esito di ★1 — le tre impostazioni dell'issue `#20`

Verificate il 2026-08-28, **prima di ogni scrittura nel file**, nell'ordine prescritto (`T010`, prova 2).

| Impostazione | Esito |
|---|---|
| dominio `0-1` su `energy`, `valence`, `danceability` di `dim_track` (issue `#11`) | **difetto assente** — i valori sono nel dominio atteso |
| conteggio di riga di `dim_title` | **difetto assente** — coincide con quello lasciato dalla `008a` dopo la correzione a `QuoteStyle.Csv` |
| colonna di scenario su `bq3_scenarios` | **difetto assente** — la colonna è presente |

**Nessuna ricomparsa, nessuna correzione, e quindi la prova 12 non è stata eseguita** — vedi la tabella delle prove.

**Che cosa questo esito dimostra, e che cosa no.** Dimostra che le tre impostazioni hanno retto **questa** riapertura. Non dimostra che non possano riperdersi alla prossima, che è precisamente ciò che l'issue `#20` dichiara, e la ragione per cui resta aperta.

### I ritrovamenti

**Zero**, ed è dichiarato per esteso invece di essere lasciato al silenzio. Nessuna differenza è stata trovata fra un valore letto a schermo e il valore pubblicato dal documento della `007b`. **Nessuna nota in loco è dovuta** su alcun documento di `docs/` (`T033`).

**Due cose che potrebbero sembrare ritrovamenti e non lo sono**, e vale la pena dire perché:

- **`SC-2`**, l'etichetta di confidenza di `BQ1-K2` che a schermo diceva `media`. `F9` della `008a` chiama ritrovamento la differenza fra un valore letto a schermo e il valore pubblicato: qui nessun documento pubblicato sbaglia — sbagliava la trascrizione. Corretta nel file, dichiarata come scostamento;
- **l'issue `#26`**, la formulazione esclusa dentro il contratto di pagina della `008a` §8. Riguarda un documento di disegno sotto `specs/`, non un valore pubblicato, e la decisione di non scrivere una nota in loco è registrata al §14 del contratto di narrazione.

### Lo stato delle cinque issue, e le due aperte da questa feature

**Nessuna delle cinque è chiusa da questa feature**, come il perimetro prescrive (`FR-031`).

| Issue | Stato | Quale evidenza manca per chiuderla |
|---|---|---|
| `#11` — tipizzazione delle colonne di mood | **aperta** | è assorbita da `#20` e non è chiudibile finché il `.pbix` non è versionato. La verifica di ★1 vale per una riapertura, non per tutte |
| `#17` — `C2` non è mai stata nominata, né il terzo vincolo di `kpi_operators.md` §12 | **aperta** | `C2` non esiste come valore ancorato in alcun artefatto. Questa feature non lo pubblica e non ne discute il valore: dichiara soltanto, su `BL-Q1-3` e `BL-Q2-8`, che l'esito congiunto non è a schermo — vero indipendentemente da quante condizioni esistano |
| `#18` — `mood_profile_overlap` senza `ALL` | **aperta** | la formula non è stata toccata. Questa feature dimostra che il difetto non si manifesta, perché nessuna pagina offre un filtro di categoria (`FR-026`); non dimostra che non esista |
| `#20` — le tre impostazioni fragili | **aperta** | è strutturale: nasce dal fatto che il `.pbix` non è versionato e nessun controllo del repository entra nel modello. L'esito di ★1 la conferma invece di chiuderla |
| `#21` — dispersione e graduatoria non si evidenziano | **aperta** | il vincolo dello strumento non è risolto. `BL-Q2-9` **dichiara** a schermo che le due visuali non si filtrano, il che non la riapre e non la chiude |

**Due issue nuove**, entrambe aperte da questa feature e nessuna delle due chiusa qui:

| Issue | Che cosa registra |
|---|---|
| `#26` | il contratto di pagina della `008a` §8 usa la formulazione che `bq3_scenarios.md` §8 dichiara falsa. Nessun valore ne dipende |
| `#27` | la considerazione dell'autore su pagine dedicate alla prosa fra una pagina-grafico e l'altra, conseguenza di `SC-3`. Comporta di riaprire il numero di pagine e nessuna decisione è presa |

### L'esito delle dodici prove

| # | Prova | Chiusa da | Esito |
|---|---|---|---|
| 1 | nulla di pubblicato è stato rotto *(eseguibile)* | `T039` | **verde** — vedi la nota sotto la tabella |
| 2 | le tre impostazioni fragili di `#20` ★1 | `T010` | **passata** su tutte e tre le voci, nessuna ricomparsa |
| 3 | la struttura della `008a` è invariata | `T026` | **passata** — quattro pagine, otto tabelle, cinque relazioni, quattordici misure, nessun filtro né slicer, nessuna visuale legata a un campo aggiunta |
| 4 | esaustività in entrambe le direzioni ★3 | `T020` | **passata** — ogni obbligo ha almeno un blocco, ogni blocco serve almeno un obbligo. Nessun obbligo scoperto, nessun blocco senza obbligo |
| 5 | fedeltà alla lettera al contratto ★3 | `T021` | **passata con uno scostamento già dichiarato**: `BL-IN-3` non coincide alla lettera, ed è `SC-1`. Nessun'altra differenza |
| 6 | nessuna cifra fuori dalla lista chiusa ★3 | `T022` | **passata** — `2021` e `2022` solo su `BL-IN-4`, nessun'altra cifra su alcun blocco |
| 7 | nessuna composizione della regola di decisione | `T023` | **passata** — `C1` su `BQ1` e `C3` su `BQ2`, ciascuna da sola, nessun conteggio, `C2` mai nominata, nessun esito complessivo |
| 8 | nessuna conclusione, nessuna causa, nessuna persona | `T024` | **passata** — la parola «domanda» è dichiarata su `BQ2` come indice della fonte (`BL-Q2-10`) |
| 9 | le tre formulazioni escluse non compaiono | `T025` | **passata** — nessuna delle tre, in nessuna variante |
| 10 | il testo è sempre visibile | `T026` | **passata in parte**: nessuna pagina-tooltip, nessun segnalibro, nessun pannello, le pagine restano quattro. Il testo però **scorre**, ed è `SC-3` |
| 11 | le sigle sono sciolte dove compaiono | `T027` | **passata** — `C1` e `C3` sono le uniche introdotte da questa feature, entrambe sciolte sulla propria pagina |
| 12 | i valori a schermo coincidono ancora con i pubblicati *(condizionale)* | — | **non eseguita** |

**Perché la prova 12 non è stata eseguita.** Si esegue solo se la prova 2 impone una correzione, e la prova 2 è passata su tutte e tre le voci. Nessuna correzione è servita, quindi nessun valore è stato toccato e non c'era nulla da riconfrontare. **La non esecuzione è dichiarata invece che sostituita da un esito che nessuno ha osservato**, come il quickstart prescriveva prima di cominciare.

**Le due prove che non sono verdi piene, dette come sono.** La 5 e la 10 hanno ciascuna uno scostamento già registrato — `SC-1` e `SC-3` — e sarebbe stato più comodo scriverle «passate» rimandando alla sezione degli scostamenti. Sono marcate qui perché una tabella di prove tutte verdi accanto a una sezione con tre scostamenti è una tabella che si legge senza leggere l'altra.

**Che cosa il verde della prova 1 certifica, e che cosa no.** Certifica che nessuna ancora dei sette documenti pubblicati è stata rotta. **Non dice nulla del deliverable di questa feature**, che è prosa dentro un file binario non versionato — la sola cosa del repository che quel controllo non può leggere per costruzione. Sette prove su dodici hanno confrontato un testo con un altro testo, e il loro esito è un'osservazione umana.

### La dichiarazione di pubblicabilità

Il criterio è stato fissato in `N8`, **prima** che il file venisse riaperto. Non si allarga adesso, e non si restringe: si verifica.

| # | Condizione di `N8` | Esito | Dove si verifica |
|---|---|---|---|
| 1 | le tre assenze del contratto di dashboard `008a` punto 1 sono colmate — limiti dichiarati, assunzione strutturale dei proxy, narrazione | **verificata** | l'assunzione dei proxy è `BL-IN-1` sulla pagina di ingresso; i limiti sono su tutte e quattro le pagine; la narrazione esiste, ed è questo esito a dire dove |
| 2 | il *perché* di ogni livello di confidenza è a schermo, per tutti e otto i KPI | **verificata** | `BL-Q1-1`, `BL-Q1-4`, `BL-Q1-6` su `BQ1`; `BL-Q2-1`, `BL-Q2-3`, `BL-Q2-5` su `BQ2`; `BL-Q3-1` copre entrambi i KPI di `BQ3`. Per `BQ1-K1`, che compare su due pagine, la ragione sta una volta sola su `BQ1` (`N5`) |
| 3 | i limiti che `kpi_operators.md` §12 e `data_model.md` §18 assegnano esplicitamente a questa feature sono a schermo, in forma leggibile da un non tecnico | **verificata sulla lettera, contestabile sulla sostanza** — vedi sotto | tutti a schermo; tre di essi dicono meno di quanto la fonte prescrive (§13.1 del contratto) |
| 4 | nessun blocco viola `N2`, `N6` o `N7` | **verificata** | prove 6, 7 e 8, tutte passate |
| 5 | le tre impostazioni dell'issue `#20` sono state riverificate all'apertura e il loro esito è dichiarato | **verificata** | prova 2, passata su tutte e tre; l'esito è dichiarato nella sezione ★1 |

**La condizione 3 va guardata da vicino, perché è l'unica su cui due letture oneste divergono.** Alla lettera chiede che quei limiti siano *a schermo, in forma leggibile da un non tecnico*: lo sono tutti, e la prova 4 lo ha verificato in entrambe le direzioni. Su una lettura più stretta — che ciascuno sia portato **per intero** — non è soddisfatta: `OB-11` e `OB-19`, due dei tre limiti che `kpi_operators.md` §12 assegna per nome a questa feature, e `OB-20`, della categoria *sconsigliato* di `data_model.md` §18, dicono meno di quanto la fonte prescrive. Il dettaglio di che cosa manca è nella §13.1 del contratto di narrazione.

**La dichiarazione poggia sulla lettura letterale, e questo è il punto su cui va contestata se qualcuno la contesta.** È scritto qui e non nascosto perché la revisione in contesto pulito lo incontri: se un revisore che non ha letto la §13.1 trova quei tre blocchi insufficienti leggendo solo lo schermo, la dichiarazione va rivista.

> ## Il `.pbix` è pubblicabile
>
> **Dal 2026-08-28.** È la prima volta che questo progetto lo afferma, e sostituisce l'affermazione della `008a` — *«Il file è leggibile, non pubblicabile»* — che senza questa feature sarebbe rimasta su `main` come dichiarazione falsa.
>
> **La ragione, in una riga**: un file che espone otto numeri con la propria fonte, la propria confidenza, la ragione di quella confidenza e i limiti che ne governano la lettura può essere mostrato a chi non ha letto nulla di questo repository senza che ne tragga una conclusione che i dati non sostengono.

> **Nota in loco — 2026-08-29, feature `008b`. La dichiarazione qui sopra è ritirata.**
>
> **Affermazione precedente**: il `.pbix` è pubblicabile dal 2026-08-28, per la ragione in una riga riportata nella scatola.
>
> **Affermazione corretta**: il `.pbix` **non è dichiarato pubblicabile**. L'affermazione della `008a` — *«Il file è leggibile, non pubblicabile»* — **non è stata sostituita** e resta vera. Tutto ciò che precede questa nota resta un accertamento vero su che cosa esiste a schermo: cade la conclusione, non l'osservazione.
>
> **Causa della divergenza**: la revisione in contesto pulito su contratto ed esito è tornata con venticinque rilievi e un giudizio negativo sul metro che questa feature si era data — la leggibilità per un decisore che non ha letto alcun documento del repository. Due dei rilievi colpiscono la dichiarazione direttamente:
> - **`R6`** — la *ragione in una riga* promette che il lettore non tragga conclusioni non sostenute, mentre il quinto trattino dell'elenco qui sotto dichiara che chi non scorre non legge la parte prescrittiva. Le due frasi non possono essere vere insieme;
> - **`R5b`** — la riga di *bassa* della legenda di confidenza è a schermo **troncata** (`SC-1`), e su quella legenda poggia la lettura di tutti e otto i numeri del file. Un file con una frase rotta sulla prima pagina non è pubblicabile il giorno in cui lo si dichiara.
>
> Il contratto di pubblicabilità nomina, alla propria §4, **la revisione in contesto pulito come il primo dei tre presidi** su cui la garanzia poggia. Il presidio ha risposto no.
>
> **Che cosa non è caduto: il criterio.** `N8` era stato fissato **prima** di costruire, le sue cinque condizioni sono state verificate una per una e nessuna è stata allargata dopo — il revisore lo dichiara per primo (*«non la contesto sul criterio»*). Quello che è caduto è **la misura, non il metro**.
>
> **Perché la riga tronca non è stata riparata**: il 2026-08-28 la regia ha deciso che la dashboard a quattro pagine è **superata**. Non viene rifinita, viene sostituita da un report a 8-12 pagine disegnato lungo la spina di una raccomandazione che il progetto non ha ancora scritto (`009`, `010a`, `010b`). Power BI Desktop non è stato riaperto: la riga tronca si dichiara, non si ripara.
>
> **Fonte verificabile**: [`review.md`](./review.md) — rilievi `R5b` e `R6`, §5 «Giudizio complessivo sul metro dichiarato», e il blocco di chiusura in coda al verbale.

**Che cosa «pubblicabile» non significa**, con la stessa precisione, perché è la metà su cui un lettore esterno si può ingannare:

- **non** significa pubblicato. Il `.pbix` resta un file locale non versionato, e nessuna pubblicazione sul servizio è nel perimetro di alcuna feature di questo progetto;
- **non** significa che le issue aperte siano chiuse. `#11`, `#17`, `#18`, `#20`, `#21` restano aperte, `#26` e `#27` si aggiungono, e `#20` in particolare dichiara che tre impostazioni possono riperdersi a ogni riapertura;
- **non** significa che il debito della `004` sulla verificabilità del benchmark sia risolto. Non lo è, e `BL-Q3-9` lo dice a schermo invece di nasconderlo — che è precisamente ciò che rende il file pubblicabile invece di impedirlo;
- **non** significa che i numeri descrivano StreamWave. Non lo fanno, e `BL-IN-1` lo dice per primo;
- **non** significa che tutto il testo si legga in un colpo d'occhio. Le caselle scorrono (`SC-3`): il testo è tutto presente e nessun blocco è nascosto dietro un clic, ma chi non scorre non legge la seconda metà di un blocco — che è dove sta la parte prescrittiva.

**Chi garantisce che tutto questo sia vero.** Tre presidi umani e nessuno script: la revisione in contesto pulito che questo esito riceverà, le undici prove manuali di lettura, e la disciplina con cui gli scostamenti sono stati scritti mentre accadevano. `scripts/check_audit_coherence.py` non entra nel `.pbix` e non legge `specs/`: il suo verde riguarda i sette documenti pubblicati, e nient'altro.

> **Nota in loco — 2026-08-29, feature `008b`. Il conteggio delle prove è sbagliato, e il primo presidio ha risposto no.**
>
> **Affermazione precedente**: *«le undici prove manuali di lettura»*.
>
> **Affermazione corretta**: le prove manuali effettivamente eseguite sono **dieci**. Delle dodici prove della tabella qui sopra, la 1 è **eseguibile** — è `check_audit_coherence.py`, che la frase stessa esclude dai presidi — e la 12 è dichiarata **non eseguita**.
>
> **Causa della divergenza**: un conteggio a memoria in una sezione di sintesi, e nel punto in cui il documento elenca ciò che garantisce la pubblicabilità. Il numero include una prova che il documento dichiara, quattro righe più sopra, di non aver eseguito.
>
> **Sul primo presidio**: la revisione in contesto pulito che questo esito «riceverà» l'ha ricevuta, ed è tornata con un no. La dichiarazione di pubblicabilità che questa frase sostiene è **ritirata** — vedi la nota sopra la scatola.
>
> **Fonte verificabile**: la tabella «L'esito delle dodici prove» qui sopra, e il rilievo `R18` caso 4 di [`review.md`](./review.md).
