# Feature Specification: il report che porta l'argomento a schermo — disegno

**Feature Branch**: `010a-report-disegno`

**Created**: 2026-08-29

**Status**: Draft

**Input**: User description: "Disegno del report a 8-12 pagine che sostituisce la dashboard a quattro pagine, portando a schermo l'argomento di docs/raccomandazione.md nell'ordine in cui quel documento lo espone: la domanda, la risposta, perché regge, con che cosa entrare, quanto vale, che cosa lo ribalterebbe, che cosa non si può concludere. Il deliverable è specs/010a-report-disegno/contracts/page-contract.md, sul modello del contratto della 008a. La feature non apre Power BI, non costruisce visuali, non scrive DAX, non scrive il testo a schermo: dichiara che cosa deve esistere e lo consegna alla 010b."

## Perché questa feature esiste

La dashboard a quattro pagine della `008` è stata revisionata in contesto pulito e ha ricevuto un no sul metro che si era data: «un decisore che non conclude niente non ha usato la dashboard — l'ha archiviata». Il difetto non era il testo a schermo, era l'impaginazione: **quattro pagine, una per domanda di business, sono un inventario di misure**. Un inventario non porta a una conclusione perché non è ordinato come un argomento — è ordinato come un framework.

La `009` ha scritto l'argomento che mancava: [`docs/raccomandazione.md`](../../docs/raccomandazione.md), revisionato in contesto pulito e approvato sullo stesso metro. Questa feature **non lo riscrive**: lo impagina. È la spina del report, ed è la ragione per cui la feature esiste.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — chi costruirà il report sa che cosa costruire (Priority: P1)

Chi apre la `010b` riceve un documento che, per ciascuna pagina, dice quale parte dell'argomento porta, quali valori compaiono con l'identificativo dell'ancora, quali misure DAX servono distinguendo le esistenti dalle nuove, quali visuali con tipo e assi, e che cosa la pagina non offre. Non deve dedurre nulla, non deve rileggere `docs/raccomandazione.md` per capire quale numero va dove, e non deve inventare una visuale dove i dati non la sostengono.

**Why this priority**: è il deliverable. La `010b` è la feature più grande mai aperta in questo progetto e la sola rimasta a toccare la GUI: la sua stima poggia sull'elenco di ciò che va costruito. Un elenco vago la fa sforare.

**Independent Test**: si prende il contratto senza altro materiale e si conta, pagina per pagina, quante decisioni chi costruisce dovrebbe prendere da sé. Zero decisioni di contenuto è l'esito atteso; le decisioni di forma — colori, caratteri, dimensioni — sono dichiarate come non decise.

**Acceptance Scenarios**:

1. **Given** il contratto di pagina, **When** chi costruisce cerca quali misure DAX deve scrivere ex novo, **Then** le trova in un elenco separato da quelle già esistenti, ciascuna con il proprio nome, ciò che calcola e la pagina che la richiede.
2. **Given** il contratto di pagina, **When** chi costruisce cerca quale valore va in una data posizione a schermo, **Then** trova l'identificativo dell'ancora verso `reports/`, non un numero trascritto.
3. **Given** una pagina che il contratto descrive, **When** chi costruisce cerca che cosa quella pagina non deve offrire, **Then** trova la voce «interazioni non offerte, e perché» con la ragione di ciascuna esclusione.

---

### User Story 2 — un decisore che scorre le pagine incontra un argomento (Priority: P1)

Chi apre il report e scorre le pagine in sequenza incontra, in quest'ordine: la domanda, la risposta, perché la risposta regge, che cosa fare, quanto vale, che cosa la ribalterebbe, che cosa non si può concludere. Non incontra un indice di KPI, e non deve ricomporre l'argomento da sé.

**Why this priority**: è il metro su cui la dashboard precedente ha ricevuto un no, ed è l'unica ragione per cui questa feature esiste. Vale P1 insieme alla prima storia perché le due sono la stessa cosa vista da due lati: il contratto è utile solo se ciò che descrive è un argomento.

**Independent Test**: si legge la sola colonna «che parte dell'argomento porta» della mappa delle pagine, dall'alto in basso, e si verifica che la sequenza sia leggibile come un discorso senza consultare le pagine.

**Acceptance Scenarios**:

1. **Given** la mappa delle pagine, **When** la si legge in sequenza, **Then** l'ordine coincide con l'ordine delle sezioni di `docs/raccomandazione.md` e non con l'ordine `BQ1`→`BQ2`→`BQ3` del framework di KPI.
2. **Given** una pagina qualunque del disegno, **When** si cerca a quale sezione della raccomandazione corrisponde, **Then** la corrispondenza è dichiarata puntualmente, non lasciata all'inferenza.
3. **Given** il report a schermo, **When** un decisore si ferma dopo la pagina della risposta, **Then** ha comunque ricevuto la risposta e il criterio con cui è stata data — la sequenza non richiede di arrivare in fondo per concludere qualcosa.

---

### User Story 3 — ogni pagina dà all'occhio qualcosa da guardare (Priority: P2)

Ogni pagina del disegno porta almeno un elemento visivo che comunica, o è una pagina di sola prosa dichiarata come tale. Nessuna pagina è una griglia di schede numeriche affiancate a una tabella.

**Why this priority**: è un vincolo esplicito della regia e il secondo difetto della dashboard precedente. Vale P2 e non P1 perché una pagina povera di grafica ma corretta è un difetto di comunicazione; una pagina che porta la parte sbagliata dell'argomento è un difetto di struttura, e il secondo si ripara solo ridisegnando.

**Independent Test**: si scorre l'elenco delle visuali pagina per pagina e si verifica che nessuna pagina abbia come soli elementi schede e tabelle, salvo dove il disegno dichiara la pagina come di sola prosa e ne dà la ragione.

**Acceptance Scenarios**:

1. **Given** una pagina del disegno, **When** se ne elencano le visuali, **Then** o esiste almeno una visuale con una geometria che porta informazione, oppure la pagina è dichiarata di sola prosa con la ragione.
2. **Given** una visuale che il disegno richiede, **When** si verifica quale artefatto la alimenta, **Then** l'artefatto esiste e contiene i valori alla grana che la visuale mostra; dove non li contiene, il disegno lo dichiara invece di assumere la visuale costruibile.

---

### Edge Cases

- **Che cosa succede se il disegno arriva a più di 12 o a meno di 8 pagine.** La feature si ferma al secondo punto di fermata e riporta il numero raggiunto: è una decisione di Valerio, non una da assorbire comprimendo o gonfiando le pagine.
- **Che cosa succede se una visuale richiede valori a una grana che nessun artefatto pubblica.** La visuale non entra nel contratto: si dichiara che i dati non la sostengono e si sceglie una forma che i dati sostengono. Inventare la visuale sarebbe pubblicare una geometria che afferma ciò che nessun valore contiene.
- **Che cosa succede se il disegno trova un difetto in `docs/raccomandazione.md`.** È un ritrovamento: si dichiara e si porta alla regia. Quel documento è stato revisionato in contesto pulito e questa feature non lo modifica.
- **Che cosa succede se un'affermazione del contratto esiste già in `docs/raccomandazione.md` o nel contratto della `008a`.** Va censita prima della revisione e verificata contro l'originale: è il presidio che la `009` ha usato dopo il ritrovamento della chiusura della `008b`, dove un'affermazione sbagliata esisteva in due copie e il revisore ne aveva ricevuta una sola.
- **Che cosa succede alle tre impostazioni fragili del `.pbix`** (issue `#20`). Il file non è versionato e questa feature non lo apre: il contratto dichiara che chi costruisce le rifà, e l'issue resta aperta.

## Requirements *(mandatory)*

### Functional Requirements

**Il deliverable e la sua natura**

- **FR-001**: il deliverable è `specs/010a-report-disegno/contracts/page-contract.md`, scritto **prima** che Power BI Desktop venga aperto, sul modello strutturale del contratto della `008a`.
- **FR-002**: il contratto è un **vincolo, non un accertamento**: dichiara che cosa deve esistere. Nessuna sua riga descrive lo stato di un file che questa sessione non ha aperto — e questa sessione non apre il `.pbix`, che non è versionato.
- **FR-003**: il contratto **non trascrive alcun valore di KPI**. I valori si citano per identificativo di ancora verso `reports/`, mai come cifra: una seconda copia di un valore è una copia che può divergere senza che nulla lo segnali.
- **FR-004**: il contratto non contiene il testo a schermo. Dichiara **dove** la `010b` scriverà, perché quella feature non debba ridisegnare le pagine per farvi entrare il proprio testo.

**La spina dell'argomento**

- **FR-005**: l'ordine delle pagine è l'ordine dell'argomento di `docs/raccomandazione.md`, non l'ordine del framework di KPI. Un lettore che scorre in sequenza incontra: la domanda, la risposta, perché la risposta regge, che cosa fare, quanto vale, che cosa la ribalterebbe, che cosa non si può concludere.
- **FR-006**: per ciascuna pagina il contratto dichiara **a quale sezione di `docs/raccomandazione.md` corrisponde**, puntualmente.
- **FR-007**: il report ha fra 8 e 12 pagine. Il contratto dichiara se la pagina iniziale e quella finale sono comprese nel conteggio. Se il disegno esce dalla forchetta, la feature si ferma e lo riporta invece di comprimere o gonfiare.

**Che cosa ogni pagina dichiara**

- **FR-008**: per ciascuna pagina il contratto dichiara **quale parte dell'argomento porta**.
- **FR-009**: per ciascuna pagina il contratto elenca **quali valori compaiono**, ciascuno con l'identificativo dell'ancora verso `reports/`.
- **FR-010**: per ciascuna pagina il contratto elenca **quali misure DAX servono**, distinguendo quelle che esistono già da quelle da creare.
- **FR-011**: per ciascuna pagina il contratto elenca **quali visuali**, con il tipo e ciò che va sugli assi.
- **FR-012**: per ciascuna pagina il contratto dichiara **che cosa la pagina non offre e perché**, sul modello delle voci «interazioni non offerte» del contratto della `008a`.
- **FR-013**: ogni pagina porta almeno un elemento visivo che comunica, **oppure** è dichiarata di sola prosa con la ragione per cui quel passaggio dell'argomento non porta numeri. Una pagina di sola prosa non va riempita di grafica per giustificarne l'esistenza.

**L'input della `010b`**

- **FR-014**: il contratto produce un elenco delle **misure nuove** che il disegno richiede, separato da quelle esistenti, con per ciascuna: il nome, che cosa calcola, la pagina che la richiede, e da quali tabelle del modello legge.
- **FR-015**: il contratto produce un elenco delle **visuali nuove** che il disegno richiede rispetto a quelle della dashboard a quattro pagine, con l'indicazione di quali fra esse riusano materiale già costruito.
- **FR-016**: il contratto dichiara quali visuali il disegno **avrebbe voluto** e i dati non sostengono, con la ragione. Una visuale non costruibile dichiarata è un vincolo per chi costruisce; una taciuta è un'ora persa davanti allo schermo.

**Provenienza, confidenza e limiti a schermo**

- **FR-017**: ogni valore a schermo porta la propria etichetta di fonte e confidenza nella forma di `business_case.md` §5.4. Vale su ogni pagina, senza eccezioni.
- **FR-018**: il contratto dichiara **dove le assunzioni A1 e A6 compaiono a schermo**. `docs/raccomandazione.md` le tratta in una sezione propria perché sopravvivano all'estrazione di una frase: una pagina che le relega in nota a piè di schermo perde quella proprietà, e il disegno deve dire dove stanno.
- **FR-019**: dove i numeri di `BQ3` compaiono, il contratto dichiara che **il debito della `004` sulla verificabilità del benchmark è aperto**.
- **FR-020**: sull'uplift il contratto usa la **formulazione stretta** di `bq3_scenarios.md` §8, la stessa che `docs/raccomandazione.md` §4 adotta — qui nessuna base viene quantificata e nessun artefatto offre una chiave per farlo — e **non** la formulazione «non è scalabile», che quel documento dichiara falsa (issue `#26`).
- **FR-021**: i tre valori di scenario di `BQ3` si presentano **sempre come terna**, mai come valore isolato, su qualunque pagina compaiano.

**Il debito ereditato**

- **FR-022**: il contratto dichiara che chi costruirà rifà le **tre verifiche del modello** dell'issue `#20`, che il `.pbix` non versionato può riperdere a ogni riapertura. Questa feature non chiude e non tocca quell'issue.
- **FR-023**: il disegno decide se l'issue `#21` — dispersione e graduatoria di `BQ2` che non si evidenziano a vicenda — viene riproposta o chiusa nel report nuovo, e lo dichiara nel contratto.
- **FR-024**: l'issue `#28` si chiude solo insieme alla `010b`: questa feature ne porta l'impaginazione, non la resa a schermo. Il fatto va dichiarato nell'esito.

**Il presidio contro le copie divergenti**

- **FR-025**: prima della revisione, la feature **censisce** le affermazioni del contratto che vivono già in `docs/raccomandazione.md` o nel contratto della `008a`, e verifica che le copie non divergano. È il presidio che la `009` ha usato dopo il ritrovamento della chiusura della `008b`.

**Il perimetro**

- **FR-026**: la feature non apre Power BI Desktop per alcuna ragione, non costruisce visuali, non scrive DAX in un file di modello, non tocca un `.pbix`. Tutto ciò è della `010b`.
- **FR-027**: la feature non scrive il testo a schermo, che ha il proprio contratto di narrazione nella `010b`.
- **FR-028**: la feature non ricalcola alcun KPI e non riapre alcun operatore fissato. Una divergenza incontrata è un **ritrovamento** da dichiarare con nota in loco.
- **FR-029**: la feature non modifica `docs/raccomandazione.md`, `docs/roadmap.md`, né chiude alcuna issue aperta. Non scrive in `data/raw/` né in `data/processed/`.

**Chiusura**

- **FR-030**: la feature chiude il proprio drift sul [README](../../README.md): riga nella tabella di stato, deliverable elencato, prosa dei deliverable estesa, `Setup` e `Struttura` allineati.
- **FR-031**: la revisione in contesto pulito produce `specs/010a-report-disegno/review.md` con i quattro obblighi di `CLAUDE.md`. Il perimetro della revisione dichiara **quale delle due domande** viene fatta verificare — se il disegno regge la spina dell'argomento, oppure se il contratto si legge da solo — perché un revisore che ha letto entrambi i documenti non può più rispondere alla seconda.

### Key Entities

- **Pagina**: l'unità del disegno. Porta una parte dell'argomento, un insieme di valori ancorati, un insieme di visuali, un insieme di interazioni non offerte, e uno spazio riservato al testo della `010b`.
- **Valore a schermo**: un numero pubblicato da un artefatto sotto `reports/` o `data/curated/`, citato nel contratto per identificativo di ancora e mai per cifra, con etichetta di fonte e confidenza.
- **Misura**: un'espressione DAX. O esiste già ed è pubblicata da `docs/kpi_measures.md`, o è nuova e questa feature la specifica senza scriverla.
- **Visuale**: un elemento grafico con un tipo, ciò che va sugli assi, e l'artefatto che la alimenta alla grana a cui la mostra.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: la sequenza delle pagine, letta dalla sola colonna «che parte dell'argomento porta», si legge come un discorso e coincide con l'ordine delle sezioni di `docs/raccomandazione.md`.
- **SC-002**: ogni pagina del contratto dichiara tutte e cinque le voci di `FR-008`…`FR-012`. Nessuna pagina ne omette una.
- **SC-003**: ogni valore citato dal contratto porta un identificativo di ancora risolvibile contro un artefatto versionato. Nessun valore compare come cifra trascritta.
- **SC-004**: l'elenco delle misure nuove e delle visuali nuove è sufficiente perché chi apre la `010b` cominci a costruire senza tornare a chiedere: ogni voce ha nome, contenuto e pagina richiedente.
- **SC-005**: nessuna pagina ha come soli elementi schede e tabelle, salvo quelle dichiarate di sola prosa con la ragione.
- **SC-006**: il numero di pagine sta fra 8 e 12, con il conteggio dichiarato; oppure la feature si è fermata al secondo punto di fermata e lo ha riportato.
- **SC-007**: il censimento di `FR-025` non trova alcuna divergenza fra le copie, oppure ne trova e le dichiara come ritrovamento.
- **SC-008**: la revisione in contesto pulito ha prodotto il verbale, e il blocco di chiusura distingue i rilievi risolti, indeboliti e rinviati, nominando l'issue per ogni rinvio.

## Assumptions

- **Il `.pbix` a quattro pagine non viene aperto.** Non è versionato, vive sul disco di Valerio, e questa feature non può ispezionarlo. Ogni affermazione sul suo contenuto sarebbe un accertamento che questa sessione non può fare: il contratto dichiara vincoli, e la `010b` accerterà.
- **Il modello dati resta quello di `docs/data_model.md`**, con le estensioni che il contratto della `008a` ha già dichiarato — le due soglie di `F7`, le due misure companion di `CP-1`, la tabella disconnessa degli scenari di `CP-2`. Se il disegno nuovo richiede altre estensioni, le dichiara come tali.
- **Il report nuovo sostituisce la dashboard a quattro pagine**, non la affianca. La roadmap lo dichiara: il `.pbix` a quattro pagine non è pubblicabile e la `010b` lo sostituisce.
- **La forma delle etichette di fonte e confidenza** è quella di `business_case.md` §5.4, già adottata dal contratto della `008a`. Questa feature non la ridefinisce.
- **`docs/raccomandazione.md` è corretto.** È stato revisionato in contesto pulito e approvato. Questa feature lo impagina; se vi trovasse un difetto, è un ritrovamento per la regia.

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: tutte e tre — BQ1, BQ2, BQ3 — perché il report porta a schermo l'argomento che le compone in una risposta unica.
- **Contributo**: la risposta esiste già, pubblicata da `docs/raccomandazione.md`. Ciò che manca è la sua forma a schermo: questa feature la disegna, e senza di essa la risposta resta in un documento che il board leggerebbe soltanto se qualcuno gliela portasse. È la metà mancante di ciò che la revisione della `008b` ha respinto — il no non riguardava i numeri, riguardava l'impaginazione — e senza questo passaggio l'issue `#28` non si chiude.

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

**Questa feature non introduce alcuna metrica nuova e non produce alcun valore.** Disegna dove i valori già pubblicati compaiono a schermo. La tabella elenca quindi ciò che il disegno **porta a schermo**, con la fonte e la confidenza che quei valori hanno già, invariate.

| Metrica | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| `BQ1-K1` `music_adjacent_catalog_share` 🎯 | Netflix (reale) | alta | la classificazione è assegnata dalla fonte e viene solo letta | valore singolo |
| `BQ1-K2` `format_duration_gap` | Derivato (Netflix + Spotify) | alta | entrambi i termini osservati, confronto aritmetico | valore singolo, con segno |
| `BQ1-K3` `mood_profile_overlap` | Derivato (Netflix + Spotify) | media | poggia sulla mappatura interpretativa di `dim_category_mood` | valore singolo con nota |
| `BQ2-K1` `segment_demand_index` | Spotify (reale) | media | indice della fonte di cui il progetto non controlla la costruzione | un valore per segmento, con la quota di zeri accanto |
| `BQ2-K2` `segment_catalog_affinity` | Derivato (Netflix + Spotify) | media | stessa mappatura interpretativa di `BQ1-K3` | un valore per segmento |
| `BQ2-K3` `segment_entry_priority` | Derivato (`BQ2-K1` + `BQ2-K2`) | media | eredita la confidenza dei due termini che compone | punteggio, quadrante, posizione |
| `BQ3-K1` `premium_tier_adoption_rate` | Benchmark (esterno) per il centrale, Sintetico per la costruzione degli scenari | bassa | il centrale è un benchmark trasferito, non una misura sul progetto | **terna**, mai valore isolato |
| `BQ3-K2` `arpu_uplift` | Derivato (`BQ3-K1` + prezzi di A4) | bassa | eredita la confidenza del termine che compone | **terna**, mai valore isolato |
| verdetto congiunto — condizioni soddisfatte | Derivato (`C1` + `C2` + `C3`) | media | una congiunzione non è più affidabile del suo termine meno affidabile | conteggio su tre, con le tre condizioni accanto |

**Assunzioni dietro i dati sintetici**: nessun dato sintetico è prodotto da questa feature. Quelli che il disegno porta a schermo sono i sei valori di scenario di `BQ3`, generati dalla `004` e congelati in `reports/bq3_scenarios.json`, con le assunzioni dichiarate in `docs/bq3_scenarios.md`. Il debito della `004` sulla verificabilità del benchmark che li ancora **resta aperto**, ed è una decisione di governance che questa feature non prende: il contratto dichiara che è aperto dove quei numeri compaiono.

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Non risponde a**: che aspetto avrà il report costruito. Questa feature disegna un vincolo; ciò che esisterà lo accerterà la `010b`, e in caso di divergenza fra il disegno e il costruito la fonte autorevole è l'esito della `010b`, non questo contratto.
- **Non risponde a**: se una visuale regge davanti allo schermo. È l'unica cosa che un disegno a tavolino non può verificare, ed è la ragione per cui gli scostamenti sono previsti dal disegno invece di essere trattati come difetti.
- **Non risponde a**: se il testo a schermo comunicherà. Il testo è della `010b`, che ha il proprio contratto di narrazione; questa feature riserva lo spazio in cui andrà.
- **Inferenza da evitare**: che un report ordinato come un argomento sia per ciò stesso convincente. L'ordine è condizione necessaria — è ciò che mancava e che ha fatto respingere la dashboard precedente — e non è condizione sufficiente. La resa a schermo può ancora fallire, e la `010b` è dove si vede.
- **Inferenza da evitare**: che questa feature chiuda l'issue `#28`. Ne chiude l'impaginazione. La resa a schermo è della `010b`, e l'issue si chiude solo insieme a quella.
- **Copertura del dato**: catalogo video fermo al 2021, catalogo musicale al 2022, benchmark economico al 2018. Il disegno non aggiunge dati e non estende alcuna copertura: porta a schermo i medesimi valori con i medesimi limiti.
- **Dove è esposto all'utente finale**: il contratto dichiara, pagina per pagina, dove ciascun limite compare a schermo. Le assunzioni A1 e A6 hanno una collocazione dichiarata per obbligo di `FR-018`, e non stanno in nota a piè di schermo.
