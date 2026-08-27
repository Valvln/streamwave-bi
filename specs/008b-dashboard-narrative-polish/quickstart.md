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

> **Sezione non ancora compilata.** Si riempie nel blocco B del piano, dopo ★2 e ★3, e le voci vanno scritte **mentre accadono** e non a memoria alla fine — è la ragione per cui ciascuna porterà la propria data.
>
> **Sarà questa sezione, non il contratto di narrazione, la fonte autorevole su ciò che esiste a schermo.** Il contratto dichiara che cosa si era deciso di scrivere; dove i due divergono, la divergenza sarà elencata qui sotto con la propria ragione.

### Che cosa è a schermo, pagina per pagina

*(da compilare — una riga per pagina: quali obblighi vi atterrano, quanti blocchi, se la fascia è bastata)*

### Gli scostamenti dal contratto approvato

> **Sezione in compilazione.** Le voci si scrivono **mentre accadono**, non a memoria alla fine (`T014`, `T019`). Alla chiusura della Fase 7 questa nota va tolta e la sezione dichiarata completa; se resterà vuota, «zero scostamenti» va scritto per esteso invece di lasciare il silenzio a significarlo.

#### `SC-1` — `BL-IN-3`, testo tagliato per pareggiare l'altezza delle fasce

**Data**: 2026-08-28 · **Pagina**: ingresso · **Blocco**: `BL-IN-3` · **Categoria**: scostamento (`F9`)

**Che cosa il contratto scrive**: il blocco apre dichiarando che accanto a ogni indicatore compare un livello, enumera i tre livelli per esteso, e chiude con due frasi — che l'etichetta non dice quanto il numero descriva StreamWave, e che anche un indicatore a confidenza alta è alto rispetto al catalogo di riferimento.

**Che cosa è stato costruito**: una versione più corta, che apre direttamente sul criterio, accorcia le tre definizioni e tiene una sola delle due frasi di chiusura.

**La ragione, dichiarata come è**: **non è una fascia insufficiente.** Le altre pagine entravano senza scorrimento, e il taglio è stato scelto per allineare l'altezza di questa fascia alle altre. È una ragione **estetica**, non di capienza, e `N4` non la prevede: `N4` disciplina il caso in cui il testo non entra. Va quindi registrata per quello che è — una decisione di uniformità presa davanti allo schermo — e non travestita da vincolo di spazio.

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

*(da compilare — `N4`: se una fascia non è bastata, che cosa è stato tolto e quale obbligo ne è rimasto scoperto o ridotto)*

### L'esito di ★1 — le tre impostazioni dell'issue `#20`

*(da compilare — una riga per impostazione: difetto assente, oppure presente, corretto e registrato come ricomparsa)*

### I ritrovamenti

*(da compilare — differenze fra ciò che un documento pubblicato afferma e ciò che si è osservato, con la nota in loco che ne discende. Zero è un esito possibile)*

### Lo stato delle cinque issue

*(da compilare — `#11`, `#17`, `#18`, `#20`, `#21`: nessuna viene chiusa da questa feature, e per ciascuna va dichiarato quale evidenza manca)*

### L'esito delle dodici prove

*(da compilare — tabella prova / chiusa da / esito, come nella `008a`. La prova 12 è condizionale: se non è stata eseguita, si dichiara che non lo è stata e perché)*

### La dichiarazione di pubblicabilità

*(da compilare — le cinque condizioni di `N8` verificate una per una, e l'elenco di ciò che «pubblicabile» non significa. È la sola sezione di questo quickstart che nessuna feature precedente ha mai avuto, e la ragione per cui il criterio è stato fissato prima di costruire invece che dopo)*
