# Feature Specification: Data Audit & Profiling

**Feature Branch**: `002-data-audit-profiling`

**Created**: 2026-08-08

**Status**: Draft

**Input**: User description: "Data Audit & Profiling — profilo riproducibile dei due dataset reali. La 001 cita numerosi fatti sui dati (completezza, identificativi distinti, struttura del campionamento, concentrazione degli zeri) che esistono solo come prosa: nessuno script li rigenera. È il rilievo R8. Il rilievo R11 chiede quante e quali categorie del catalogo video compongano `BQ1-K1`, la North Star. La feature produce (1) uno script Python deterministico e rieseguibile che legge `data/raw/` in sola lettura, (2) un artefatto di soli numeri leggibile da macchina e versionato, unica fonte di verità del profiling, (3) un documento di audit in italiano che interpreta il profilo. Il documento cita i numeri, non li possiede, e la divergenza fra prosa e numeri deve essere rilevabile da un comando eseguibile. La feature descrive i dati, non li corregge né li giudica."

*(Il prompt di consegna integrale è più esteso di questa sintesi. Ogni vincolo che conteneva compare qui sotto come requisito, criterio di successo o limite dichiarato: questa spec è il testo autorevole, non il prompt.)*

## Rapporto con la feature 001

Due precisazioni servono a chi legge le due spec in sequenza.

**Il divieto di numeri della 001 era locale.** FR-016 della 001 vietava numeri di risultato nel proprio deliverable, perché quel documento definiva il metro e un metro non può contenere misure. Questa feature produce quasi soltanto numeri osservati, e non è una contraddizione: il divieto valeva per `docs/business_case.md`, non è un principio generale del progetto. Ciò che vale sempre è il principio I — ogni numero dichiara fonte e confidenza — che questa spec applica in pieno.

**Questa feature chiude due voci di debito della 001, non tutte.** Chiude il rilievo **R8** (provenienza dei numeri sui dati citati nel business case) e la parte osservativa del rilievo **R11** (quante e quali categorie del catalogo video hanno contenuto musicale dichiarato). Non chiude la parte testuale di R11 — l'allineamento di §3 del business case, che descrive quattro tipologie di contenuto dove la misura ne legge una sola etichetta: la roadmap lo assegna al debito testuale, non a questa feature. Vedi FR-032.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chiunque può rigenerare i numeri invece di crederci (Priority: P1)

Una persona che clona il repository, ricostruisce `data/raw/` con `scripts/download_data.sh` e lancia un solo comando ottiene un artefatto di soli numeri che descrive i due dataset. L'artefatto è versionato: chi **non** ha il token Kaggle lo trova comunque nel repository e può leggerlo, confrontarlo, citarlo. Nessun numero sui dati reali resta affidato alla parola dell'analista.

**Why this priority**: è il rilievo R8 e il principio II. Un profilo che vive solo nell'esecuzione non è verificabile da chi non ha i dati; un numero che vive solo in prosa non è verificabile da nessuno. Una feature che si fermasse qui avrebbe già prodotto l'artefatto che manca al progetto: il documento di US2 lo interpreta, ma senza l'artefatto non ha nulla da interpretare.

**Independent Test**: si esegue lo script due volte di seguito e si confrontano i due artefatti; si cerca poi nell'artefatto ciascuno dei valori che la 001 cita in prosa. La storia è superata se le due esecuzioni coincidono e se ogni valore dell'inventario di FR-018 è presente e identificabile.

**Acceptance Scenarios**:

1. **Given** una copia del repository con `data/raw/` ricostruito, **When** si esegue lo script di profiling, **Then** viene prodotto un artefatto di soli numeri e `data/raw/` risulta immutato (nessun file aggiunto, modificato o rimosso).
2. **Given** lo stesso `data/raw/`, **When** lo script viene eseguito due volte, **Then** i due artefatti sono identici byte per byte.
3. **Given** l'artefatto prodotto, **When** si cerca uno qualunque dei valori che la 001 cita in prosa, **Then** lo si trova associato a un identificativo stabile che il documento di audit e le feature successive possono citare.
4. **Given** una copia del repository **senza** `data/raw/`, **When** si guarda sotto controllo di versione, **Then** l'artefatto è presente e leggibile, e `git check-ignore` non lo intercetta.
5. **Given** l'artefatto prodotto, **When** si cerca il censimento delle categorie del catalogo video, **Then** vi si trovano **tutte** le categorie con il numero di titoli distinti di ciascuna, senza alcuna selezione a monte.
6. **Given** `data/raw/` incompleto o una colonna attesa assente, **When** si esegue lo script, **Then** lo script si ferma con un errore che nomina il file o la colonna mancante, e **non** produce un artefatto parziale.

---

### User Story 2 - Chi legge capisce cosa i dati permettono e cosa impediscono (Priority: P2)

Un lettore apre il documento di audit e in una lettura capisce com'è fatto ciascuno dei due dataset, quali sono i suoi punti fragili, e cosa questo vincola per le feature a valle: quali misure del framework 001 hanno i campi che le alimentano, quali granularità sono obbligate, dove un totale ingenuo sbaglierebbe. Ogni numero che legge è marcato e rimanda all'artefatto di US1.

**Why this priority**: l'artefatto da solo non si legge. È l'interpretazione a trasformare un profilo in una decisione informata a valle, ed è il documento — non il file di numeri — ciò che una feature successiva consulta prima di scrivere una riga. Dipende da US1 perché ogni sua affermazione numerica deve poter puntare a un identificativo che esiste.

**Independent Test**: si consegna il solo documento a un lettore che non ha visto i dati e gli si chiede di dire, per due misure del framework 001 scelte a caso, se i campi che servono esistono, e di indicare due fragilità dei dataset con il numero che le sostiene. Se ci riesce, la storia è superata.

**Acceptance Scenarios**:

1. **Given** il documento di audit, **When** lo si legge, **Then** ogni valore proveniente dal profilo è marcato in modo riconoscibile e risolvibile su un identificativo dell'artefatto; nessun valore del profilo compare in prosa non marcato.
2. **Given** il documento di audit, **When** si cerca una qualunque delle otto misure del framework 001, **Then** si trova detto se i campi che la alimentano esistono nei dati e con quale completezza — come constatazione sui campi, non come giudizio sull'idoneità della misura.
3. **Given** il documento di audit, **When** si cerca la risposta a R11, **Then** si trova **quante e quali** categorie del catalogo video hanno contenuto musicale dichiarato, il criterio con cui sono state riconosciute, e cosa l'esito comporta per la confidenza di `BQ1-K1`.
4. **Given** il documento di audit, **When** si cercano i limiti, **Then** si trovano dichiarati la copertura temporale, il fatto che il profilo descrive i dataset e non i mercati, e le inferenze da evitare elencate nella sezione "Limiti Dichiarati" di questa spec.
5. **Given** il documento di audit, **When** vi si cerca un valore di KPI o una risposta anche parziale a BQ1, BQ2 o BQ3, **Then** non se ne trova alcuno.

---

### User Story 3 - Prosa e numeri non possono divergere in silenzio (Priority: P3)

Chi modifica il documento di audit — oggi o fra tre feature — non può lasciare al suo interno un numero che il profilo non conferma più senza che qualcuno se ne accorga. Un comando eseguibile confronta ogni valore marcato nel documento con l'artefatto e fallisce se trova una divergenza, dicendo quale.

**Why this priority**: è lo stesso rischio che la 001 si era vietata con FR-005b, qui fra due file invece che fra due sezioni. Vale P3 perché è uno strato di protezione su artefatti già prodotti da US1 e US2, ma senza di esso l'ibrido documento-più-artefatto è solo un modo più elaborato di avere due copie destinate a divergere.

**Independent Test**: si altera un singolo valore marcato nel documento e si esegue il comando. La storia è superata se il comando fallisce e indica quale valore non torna.

**Acceptance Scenarios**:

1. **Given** documento e artefatto coerenti, **When** si esegue il comando di coerenza, **Then** termina con esito positivo.
2. **Given** un solo valore marcato alterato nel documento, **When** si esegue il comando, **Then** termina con esito negativo e nomina il valore divergente, il valore atteso e quello trovato.
3. **Given** un valore marcato che rimanda a un identificativo inesistente nell'artefatto, **When** si esegue il comando, **Then** termina con esito negativo e nomina il riferimento non risolvibile.
4. **Given** una copia del repository **senza** `data/raw/`, **When** si esegue il comando di coerenza, **Then** funziona ugualmente, perché confronta due artefatti entrambi versionati.

---

### Edge Cases

- **Un valore rigenerato non coincide con quello citato nella 001.** È un ritrovamento, non un incidente da assorbire in silenzio. Va registrato nel documento di audit con il valore vecchio, quello nuovo e l'ipotesi sulla causa, e l'artefatto della 001 in cui compariva va corretto con una nota. Vedi FR-030 e FR-031.
- **Il censimento trova più di una categoria a contenuto musicale dichiarato.** L'esito ribalta il presupposto su cui `BQ1-K1` regge la confidenza alta: selezionare fra più categorie **è** una mappatura. Questa feature registra il ritrovamento e ne dichiara la conseguenza, ma **non** ridefinisce la North Star — quella decisione richiede un contesto che questa feature non ha. Vedi FR-021.
- **Un campo categorico ha cardinalità troppo alta per essere enumerato** (titoli, registi, descrizioni). Il profilo riporta la cardinalità e i valori più frequenti, non l'elenco completo, e dichiara la soglia oltre la quale ha smesso di enumerare. Le categorie del catalogo video sono l'eccezione: lì l'enumerazione completa è il punto (FR-020).
- **Un campo è multi-valore** (l'elenco di categorie di un titolo video). Conteggi diversi sullo stesso campo sono entrambi corretti a granularità diverse. Il profilo dichiara quale granularità produce ciascun conteggio invece di sceglierne una in silenzio: è la stessa trappola che nella 001 ha prodotto la nota metodologica di §5.2.
- **Una variabile numerica contiene valori degeneri** (durate a zero, popolarità a zero, anni fuori dominio). Il profilo li conta e li segnala come osservazione. Non li corregge, non li esclude e non decide se vadano trattati: è la feature 003.
- **`data/raw/` non è ricostruibile** perché manca il token Kaggle. Lo script si ferma con un messaggio che rimanda a `scripts/download_data.sh`. Il documento di audit e il comando di coerenza restano comunque leggibili e eseguibili, perché entrambi poggiano su artefatti versionati.

## Requirements *(mandatory)*

### Lo script di profiling

- **FR-001**: La feature MUST produrre uno script Python versionato nel repository, eseguibile con un solo comando e senza alcun input manuale, interattivo o dipendente dall'ambiente di chi lo lancia.
- **FR-002**: Lo script MUST leggere esclusivamente i file sotto `data/raw/` e MUST NOT scrivervi. Al termine dell'esecuzione il contenuto di `data/raw/` MUST risultare immutato.
- **FR-003**: Lo script MUST essere deterministico: due esecuzioni sugli stessi file di origine producono un artefatto identico byte per byte. Sono quindi vietati timestamp di esecuzione, ordinamenti non stabili e campionamenti casuali all'interno dell'artefatto.
- **FR-004**: Se un file di origine manca, o se una colonna attesa è assente o cambia nome, lo script MUST fermarsi con un errore che nomina il file o la colonna, e MUST NOT produrre un artefatto parziale. Un profilo silenziosamente incompleto è peggio di nessun profilo.
- **FR-005**: Lo script MUST registrare nell'artefatto, per ciascun file di origine, nome, dimensione in byte e un'impronta del contenuto, così che due profili possano essere confrontati sapendo se descrivono gli stessi dati.

### L'artefatto di profilo

- **FR-006**: La feature MUST produrre un artefatto di **soli numeri**, in un formato strutturato leggibile da macchina, che è l'**unica fonte di verità** di ogni valore prodotto dal profiling.
- **FR-007**: L'artefatto MUST essere versionato in git. MUST essere collocato in una posizione effettivamente tracciata: non sotto `data/interim/` o `data/processed/`, e senza un'estensione intercettata dal blanket di `.gitignore`. La verifica è meccanica: `git check-ignore` sul percorso dell'artefatto non deve restituirlo.
- **FR-008**: Ogni valore dell'artefatto MUST avere un identificativo stabile e univoco, citabile dal documento di audit e dalle feature successive. Stabile significa che l'identificativo non cambia quando cambia il valore.
- **FR-009**: Ogni valore dell'artefatto MUST dichiarare l'unità in cui è espresso e la granularità su cui è calcolato, dove entrambe non siano univoche.
- **FR-010**: L'artefatto MUST NOT contenere prosa interpretativa, commento o giudizio. L'interpretazione vive nel documento di audit.
- **FR-011**: L'artefatto MUST essere rigenerato dallo script, mai modificato a mano. Se un valore è sbagliato si corregge lo script (principio II).

### Copertura del profilo

Per **entrambi** i dataset, l'artefatto MUST riportare:

- **FR-012**: dimensioni — numero di righe, numero e nome dei campi, tipo osservato di ciascun campo.
- **FR-013**: completezza per campo — conteggio e quota di valori mancanti, con la definizione dichiarata di cosa conta come mancante (assente, stringa vuota, segnaposto).
- **FR-014**: cardinalità dei campi categorici. Per i campi a bassa cardinalità, l'enumerazione completa dei valori con la frequenza di ciascuno; per quelli ad alta cardinalità, la sola cardinalità più i valori più frequenti, dichiarando la soglia che separa i due trattamenti.
- **FR-015**: duplicazione degli identificativi — righe totali, identificativi distinti, quanti identificativi compaiono più di una volta e con quale molteplicità.
- **FR-016**: struttura del campionamento — la distribuzione delle righe lungo la dimensione che governa il campione, in forma che renda visibile se il campione è bilanciato per costruzione.
- **FR-017**: distribuzioni delle variabili numeriche, con misure di **posizione** (minimo, quartili, mediana, massimo, media) e di **dispersione**, e conteggio dei valori sentinella o degeneri: zeri, valori costanti, valori fuori dal dominio dichiarato dalla fonte.
- **FR-018**: per i campi **multi-valore**, il profilo MUST riportare i conteggi in entrambe le granularità pertinenti — il campo come stringa e il campo come insieme di valori atomici — dichiarando per ciascun conteggio quale delle due lo produce.
- **FR-019**: nessun campo dei due dataset può essere escluso in silenzio. I campi non profilati MUST essere elencati con la ragione dell'esclusione.

### Rigenerazione dei valori della 001

- **FR-020**: L'artefatto MUST contenere, con identificativo proprio, ciascun valore dell'inventario qui sotto. È l'elenco puntuale dei numeri che la 001 cita in prosa e che oggi nessuno script rigenera.

| # | Valore citato nella 001 | Dove compare |
|---|---|---|
| V01 | titoli del catalogo video: totale, film, serie | `research.md` inventario |
| V02 | quota di valori mancanti per ciascun campo del catalogo video (tutti i campi elencati, non solo quelli citati) | `research.md` tabella completezza |
| V03 | numero di categorie distinte del catalogo video | `research.md` inventario |
| V04 | numero di valori distinti della classificazione per età | `research.md` inventario |
| V05 | righe del catalogo musicale e numero di generi | `research.md` inventario |
| V06 | identificativi di traccia distinti, identificativi ripetuti, quota di righe ripetute | `research.md` R2 |
| V07 | numero di tracce per genere (verifica del bilanciamento del campione) | `research.md` R1 |
| V08 | durata mediana di una traccia | `research.md` inventario |
| V09 | film con durata valorizzata, durata mediana, minimo e massimo | `research.md` R3 |
| V10 | quota di tracce con indice di popolarità pari a zero, complessiva | `research.md` R5 |
| V11 | quota di tracce a popolarità zero **per genere**, e verifica che nessun genere sia interamente a zero | `research.md` R5 |
| V12 | numero di generi musicali con corrispondenza lessicale nelle categorie video, e quali | `research.md` R4 |
| V13 | entità della sovrastima di un totale di catalogo calcolato senza deduplicare | `business_case.md` §5.2 |
| V14 | completezza e dominio dei campi che alimentano gli assi di mood | `research.md` inventario |

- **FR-021**: L'artefatto MUST riportare il **censimento completo** delle categorie del catalogo video: tutte le categorie, con il numero di titoli distinti di ciascuna, senza alcuna selezione a monte. Il documento di audit MUST poi dichiarare **quante e quali** hanno contenuto musicale dichiarato, con il criterio di riconoscimento esplicito, e registrare la conseguenza: una sola categoria significa che `BQ1-K1` non compie alcuna selezione e la confidenza alta regge; più di una significa che la selezione è una mappatura e che la confidenza alta della North Star è da rivedere. La feature registra la conseguenza e **non** ridefinisce la North Star.
- **FR-022**: Il valore V12 MUST dichiarare la regola di confronto applicata (normalizzazione, esattezza del confronto). Il documento MUST dichiarare che quel valore descrive i **vocabolari di etichette** dei due cataloghi, non la corrispondenza dei contenuti: la 001 ha già escluso il matching lessicale come piano di confronto (decisione D1), e questo valore non lo riabilita.

### Il documento di audit

- **FR-023**: La feature MUST produrre un documento di audit in italiano, come singolo file Markdown, leggibile senza strumenti diversi da un lettore Markdown.
- **FR-024**: Il documento **cita** i numeri, non li possiede: ogni valore proveniente dal profilo MUST essere marcato in modo riconoscibile e MUST rimandare all'identificativo del valore nell'artefatto. Nessun valore del profilo può comparire in prosa non marcato.
- **FR-025**: La marcatura MUST essere leggibile da macchina e non ambigua. Il controllo di coerenza NON DEVE poggiare sull'estrazione euristica di "tutti i numeri" dalla prosa italiana: è fragile e produrrebbe falsi allarmi su date, riferimenti a sezioni e sigle.
- **FR-026**: Il documento MUST interpretare il profilo: per ciascun ritrovamento rilevante dichiara **cosa vincola a valle** — quale granularità è obbligata, dove un totale ingenuo sbaglierebbe, quale fragilità un KPI erediterà.
- **FR-027**: Il documento MUST dichiarare, per ciascuna delle otto misure del framework 001, se i campi che la alimentano esistono nei dati e con quale completezza. È una **constatazione sui campi**, non un giudizio sull'idoneità della misura: dire che un campo esiste ed è completo non è dire che la misura è buona.
- **FR-028**: Il documento MUST contenere le sezioni obbligatorie richieste dai principi I e IV: provenienza e confidenza di ciò che riporta, e limiti dichiarati. I limiti viaggiano con il documento, non solo con questa spec.
- **FR-029**: Il documento MUST contenere una nota breve che spiega perché è pieno di numeri mentre `docs/business_case.md` dichiara di non contenerne: il divieto della 001 era locale a quel documento. Chi legge i due in sequenza non deve inciamparci.

### Divergenze rispetto alla 001

- **FR-030**: Ogni valore rigenerato che **non coincide** con il corrispondente citato nella 001 MUST essere registrato nel documento di audit, in una sezione dedicata, con: il valore citato nella 001, il valore rigenerato, dove il primo compariva, e l'ipotesi sulla causa della divergenza.
- **FR-031**: Per ciascuna divergenza registrata, l'artefatto della 001 in cui il valore compare MUST essere corretto con una nota datata che riporta il valore corretto e la ragione del cambiamento. Il valore originale NON DEVE sparire senza traccia: lasciare un numero sbagliato in un documento già mergiato è peggio che modificarlo, ma cancellarlo senza dirlo è peggio di entrambi.
- **FR-032**: La feature MUST NOT correggere il disallineamento descrittivo di §3 di `docs/business_case.md` rilevato da R11 — le quattro tipologie di contenuto contro l'unica etichetta che la misura legge. È debito testuale assegnato altrove dalla roadmap. Se il censimento lo conferma, questa feature lo registra come ritrovamento e si ferma lì.

### Il controllo di coerenza

- **FR-033**: La feature MUST produrre un **comando eseguibile** che confronta ogni valore marcato nel documento di audit con il corrispondente valore dell'artefatto e segnala le divergenze. La sua esistenza è un requisito; come sia realizzato è una decisione di implementazione.
- **FR-034**: Il comando MUST terminare con stato di errore quando trova almeno una divergenza, e MUST nominare il valore divergente, quello atteso e quello trovato. Un controllo che segnala senza fallire è un controllo che verrà ignorato.
- **FR-035**: Il comando MUST segnalare come errore anche un riferimento non risolvibile: un valore marcato nel documento che punta a un identificativo assente dall'artefatto.
- **FR-036**: Il comando MUST poter essere eseguito **senza** `data/raw/`, perché confronta due artefatti entrambi versionati. Non deve rieseguire il profiling per verificare la coerenza.

### Perimetro — cosa la feature non fa

- **FR-037**: La feature MUST NOT produrre dataset puliti, deduplicati o comunque trasformati in modo persistente. Pulizia ed ETL sono la feature 003.
- **FR-038**: La feature MUST NOT decidere il trattamento delle tracce a popolarità zero (divergenza 6 della revisione 001). Le conta, le localizza e si ferma: la decisione è della feature 003.
- **FR-039**: La feature MUST NOT calcolare alcun KPI del framework 001, né produrre risposte anche parziali a BQ1, BQ2 o BQ3.
- **FR-040**: La feature MUST NOT emettere giudizi sull'idoneità dei dati che la 001 non abbia già stabilito. Descrive, non giudica.

### Key Entities

- **Sorgente**: un file di `data/raw/`. Attributi: nome, dimensione, impronta del contenuto. Serve a stabilire se due profili descrivono gli stessi dati.
- **Valore di profilo**: un singolo numero osservato. Attributi: identificativo stabile, valore, unità, dataset e campo di riferimento, granularità di calcolo. È l'unità che il documento cita e che il controllo di coerenza verifica.
- **Campo**: una colonna di un dataset. Attributi: nome, tipo osservato, completezza, cardinalità, se è multi-valore.
- **Categoria del catalogo video**: un'etichetta della classificazione della fonte. Attributi: nome, numero di titoli distinti, se ha contenuto musicale dichiarato. Il censimento le comprende tutte.
- **Ritrovamento**: un fatto osservato che vincola il lavoro a valle. Attributi: enunciato, valori di profilo che lo sostengono, conseguenza dichiarata. Vive nel documento, poggia sull'artefatto.
- **Divergenza**: uno scarto fra un valore citato nella 001 e il corrispondente rigenerato. Attributi: valore citato, valore rigenerato, artefatto in cui compariva, ipotesi sulla causa, nota di correzione applicata.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Due esecuzioni consecutive dello script sullo stesso `data/raw/` producono artefatti identici byte per byte.
- **SC-002**: Dopo l'esecuzione dello script, `data/raw/` è immutato: zero file aggiunti, modificati o rimossi.
- **SC-003**: Il 100% dei quattordici valori dell'inventario di FR-020 è presente nell'artefatto con un identificativo proprio.
- **SC-004**: Il 100% dei campi di entrambi i dataset è profilato oppure elencato fra le esclusioni con la relativa ragione; zero campi omessi in silenzio.
- **SC-005**: Il 100% dei valori provenienti dal profilo che compaiono nel documento di audit è marcato e risolvibile su un identificativo dell'artefatto; zero valori del profilo in prosa non marcata.
- **SC-006**: Il comando di coerenza, eseguito su una copia pulita del repository **priva** di `data/raw/`, termina con esito positivo. Alterando un singolo valore marcato nel documento, termina con esito negativo e nomina quel valore.
- **SC-007**: Chi clona il repository senza token Kaggle può risalire da qualunque numero del documento di audit al valore corrispondente nell'artefatto versionato, senza eseguire nulla.
- **SC-008**: L'artefatto contiene il numero di categorie del catalogo video a contenuto musicale dichiarato e il conteggio di titoli distinti di ciascuna categoria del censimento; il documento dichiara il criterio di riconoscimento applicato e la conseguenza per la confidenza di `BQ1-K1`.
- **SC-009**: Per tutte e otto le misure del framework 001 il documento dice se i campi che le alimentano esistono nei dati e con quale completezza.
- **SC-010**: Il 100% delle divergenze rilevate rispetto ai valori citati nella 001 è registrato nel documento e ha una nota corrispondente nell'artefatto della 001 interessato; zero divergenze rilevate e non registrate.
- **SC-011**: Zero valori di KPI e zero risposte anche parziali a BQ1, BQ2 o BQ3 compaiono negli artefatti prodotti: una rilettura mirata non trova né misure del framework né affermazioni sull'opportunità dell'espansione.
- **SC-012**: L'artefatto non è intercettato da `.gitignore`, verificato meccanicamente sul percorso.

## Assumptions

Le assunzioni che seguono sono default ragionevoli adottati dove il prompt di consegna non vincolava. Sono decisioni di collocazione e di perimetro, non di implementazione: il come resta a `/speckit.plan`.

- **Collocazione dell'artefatto**: sotto `reports/`, che `.gitignore` lascia libero salvo le figure PNG. Il formato è strutturato e leggibile da macchina; la scelta puntuale del formato è demandata al piano, con il vincolo di FR-007 (non intercettabile dal blanket su `*.csv`, `*.parquet`, `*.xlsx` e sui formati di database).
- **Collocazione del documento di audit**: `docs/`, accanto a `docs/business_case.md`, perché è un artefatto di lettura e non un artefatto di feature.
- **Collocazione dello script**: `scripts/`, accanto a `scripts/download_data.sh`.
- **Nessuna figura, nessun grafico**: il profilo è testuale. Le figure PNG sono peraltro escluse da git sotto `reports/figures/`, e produrle qui aggiungerebbe un artefatto non versionato al centro di una feature che esiste per rendere tutto verificabile.
- **Dimensione dei dati**: circa 8.800 righe da un lato e 114.000 dall'altro. Nessun vincolo di memoria o di prestazioni entra nel perimetro; qualunque strumento ordinario è adeguato.
- **I due dataset sono quelli dichiarati dalla constitution** e non ne vengono aggiunti altri. Le fonti ammesse sono fissate lì.
- **Il documento di audit non è sottoposto a revisione in contesto pulito.** La 001 lo ha fatto e ne è venuta gran parte del valore critico del progetto, ma la roadmap non pianifica una revisione qui e il costo non rientra nella stima. Resta un debito dichiarato, non un'omissione.
- **Rischio di stima dichiarato**: la stima è di ~4 ore. Il pezzo più esposto a crescere è il controllo di coerenza di FR-033: un meccanismo di marcatura generale costa più di quanto la feature vale. Se in fase di piano dovesse gonfiarsi, il ripiego dichiarato è la forma più semplice che soddisfa FR-033-FR-036 — marcatori espliciti nel documento, risoluzione diretta sull'identificativo, nessuna estrazione generale di numeri dalla prosa — e non l'abbandono del requisito.

## Domanda di Business *(obbligatoria — Constitution, principio VI)*

- **Domanda servita**: BQ1, BQ2 e BQ3 — tutte e tre.
- **Contributo**: feature **fondativa e strumentale**. Non risponde a nessuna delle tre domande e non ne calcola alcun KPI: stabilisce **quali misure del framework 001 sono davvero costruibili sui dati disponibili**, verificando per ciascuna che i campi che la alimentano esistano e siano abbastanza completi. Contribuisce a BQ1 stabilendo se il catalogo video espone davvero un'unica etichetta di contenuto musicale — da cui dipende la confidenza della North Star `BQ1-K1` — e se i campi di durata e di mood reggono i confronti che `BQ1-K2` e `BQ1-K3` presuppongono. Contribuisce a BQ2 misurando la struttura del campionamento e la concentrazione degli zeri di popolarità, che sono le due fragilità su cui poggiano `BQ2-K1` e i KPI che ne derivano. Contribuisce a BQ3 per esclusione, confermando che nessun campo comportamentale o economico esiste nei dati reali e che l'intera terza domanda resta necessariamente sintetica.

## Provenienza e Confidenza dei Dati *(obbligatoria — Constitution, principio I)*

Ogni valore prodotto da questa feature è **osservato direttamente sui dati reali**, senza mappature né assunzioni interposte: confidenza **alta** per il criterio D5 della 001, formato a valore puntuale.

| Famiglia di valori | Fonte | Confidenza | Criterio di attribuzione | Formato di presentazione |
|---|---|---|---|---|
| Dimensioni e completezza dei campi | Netflix (reale), Spotify (reale) | alta | conteggio diretto sul file di origine, nessuna interpretazione | valore puntuale |
| Cardinalità e frequenze dei campi categorici | Netflix (reale), Spotify (reale) | alta | enumerazione diretta dei valori presenti | valore puntuale |
| Duplicazione degli identificativi | Spotify (reale) | alta | confronto fra righe totali e identificativi distinti | valore puntuale |
| Struttura del campionamento | Spotify (reale) | alta | conteggio delle righe per genere, osservato | valore puntuale |
| Distribuzioni delle variabili numeriche | Netflix (reale), Spotify (reale) | alta | statistiche descrittive calcolate sui valori osservati | valore puntuale |
| Valori sentinella e degeneri | Netflix (reale), Spotify (reale) | alta | conteggio dei valori che ricadono nella condizione dichiarata | valore puntuale |
| Censimento delle categorie del catalogo video | Netflix (reale) | alta | lettura delle etichette assegnate dalla fonte, senza selezione | valore puntuale |
| Corrispondenza lessicale fra i nomi di genere (V12) | Derivato (Netflix + Spotify) | alta | la regola di confronto è dichiarata e meccanica; il valore descrive i **vocabolari di etichette**, non la corrispondenza dei contenuti | valore puntuale con nota |

**Assunzioni dietro i dati sintetici**: nessun dato sintetico viene generato in questa feature.

**Cosa questa scala non misura.** Vale per intero la distinzione introdotta in `docs/business_case.md` §6 dopo il rilievo R1: la confidenza qualifica la solidità di un numero **rispetto al dataset da cui è calcolato**, non la sua trasferibilità a StreamWave. Fra le due si interpone l'assunzione A1 — il catalogo Netflix rappresenta il catalogo di StreamWave, il dataset Spotify il mercato musicale accessibile — che resta fuori dalla scala per costruzione, perché si applica identica a tutti i valori. Un profilo a confidenza alta è alta **sul dataset**: che il dataset descriva StreamWave dipende interamente da A1, che con i dati disponibili non è verificabile. Il documento di audit deve dirlo, non solo questa spec.

## Limiti Dichiarati *(obbligatoria — Constitution, principio IV)*

- **Copertura del dato**: catalogo video fermo al **2021**, catalogo musicale fermo al **2022**. Il profilo è una fotografia a quelle date. Nessuna sua osservazione dice qualcosa su dinamiche successive, né sull'evoluzione dei consumi musicali degli ultimi anni.
- **Non risponde a**: nessuna delle tre domande di business. Non contiene KPI, stime né raccomandazioni. Chi cercasse qui una risposta su BQ1, BQ2 o BQ3 non la troverà.
- **Non risponde a**: come i dati vadano puliti, deduplicati o trasformati. Il profilo constata, non corregge: è la feature 003.
- **Non risponde a**: se le tracce a popolarità zero vadano incluse, escluse o riportate a parte. Le conta e le localizza; la decisione è della feature 003 (divergenza 6 della revisione 001).
- **Non risponde a**: se i dati siano idonei allo scopo del progetto, oltre a quanto la 001 ha già stabilito. Descrivere un dataset non è approvarlo.
- **Il profilo descrive i dataset, non i mercati che rappresentano.** Ogni numero riguarda un catalogo pubblico specifico. Che quel catalogo rappresenti il mercato video o il mercato musicale è l'assunzione A1 della 001, che resta indimostrata.
- **Inferenza da evitare — la distribuzione del campione non è la distribuzione del mercato.** Il catalogo musicale contiene per costruzione lo stesso numero di tracce per ogni genere (ritrovamento R1 della 001: 1.000 tracce per genere). Contare le righe di un genere misura il campionamento, non la sua importanza di mercato. Qualunque lettura del profilo che dimensioni un segmento contando tracce è sbagliata prima di essere calcolata.
- **Inferenza da evitare — completezza non è correttezza.** Un campo valorizzato al 100% è un campo senza valori mancanti, non un campo con valori giusti. Il profilo misura la presenza del dato, non la sua veridicità: non ha modo di sapere se una durata dichiarata sia quella reale o se un genere sia attribuito correttamente.
- **Inferenza da evitare — la corrispondenza lessicale dei nomi di genere non è corrispondenza di contenuto.** V12 conta quante etichette coincidono come stringhe. La 001 ha già escluso il matching lessicale come piano di confronto fra i due cataloghi (decisione D1), e il valore rigenerato qui non lo riabilita: lo documenta.
- **Dove è esposto all'utente finale**: il documento di audit porta con sé la propria sezione di limiti. Non vivono solo in questa spec: viaggiano con l'artefatto che si legge.
