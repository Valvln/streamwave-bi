# Verbale di revisione in contesto pulito — `T028`

**Oggetto**: `docs/raccomandazione.md`, il deliverable della feature `009`.
**Metro dichiarato dal documento stesso**: la leggibilità per il destinatario che dichiara in apertura — *un membro del board che non ha letto alcun altro documento del repository e non guarda uno schermo*, con competenza di business e non tecnica o statistica.

**Configurazione**: subagent isolato, con accesso alla sola cartella di revisione. Il revisore non ha avuto modo di sapere che il resto del repository esista.

**Nota sul perimetro, che differisce da quello delle revisioni precedenti.** Le revisioni di questo progetto hanno finora consegnato il solo artefatto. Qui il perimetro contiene **due** file, ed è una scelta dichiarata prima della revisione (`quickstart.md` §4): la chiusura della `008b` ha prodotto un ritrovamento che nessuna revisione precedente poteva fare — una frase mal contata esisteva in due copie, e la seconda stava in un documento che il revisore non aveva ricevuto. La raccomandazione è il documento più esposto a questo difetto di tutto il progetto, perché **per costruzione ripete affermazioni che vivono già altrove**. Una revisione su estratti isolati non potrebbe, per costruzione, accorgersi che due copie divergono. Il secondo file esiste per rendere possibile quel confronto, e nient'altro.

---

## 1. Che cosa è stato letto e che cosa no

*Questa sezione è la trascrizione fedele di quanto dichiarato dal revisore.*

**Letto**, integralmente e una sola volta prima di scrivere:

- `documento-da-revisionare.md` — 197 righe, dal titolo `# La raccomandazione` alla riga finale che rimanda a `specs/009-verdetto-raccomandazione/review.md`;
- `copie-autorevoli.md` — cinque estratti, siglati `A`–`E` (business case §3; scenari economici §8–§9; misure §4.3 con la nota di aggiunta della `009`; ponte tassonomia-mood §5; modello dati §18).

**Non letto**: nessun altro file del repository. Nessuna spec, nessun `plan.md`, nessun `tasks.md`, nessun verbale di revisione precedente, nessuno script (`build_kpi_measures.py`, `check_audit_coherence.py`, `build_bq3_scenarios.py`), nessun artefatto JSON (`kpi_measures.json`, `reports/`), nessuna history git, nessun tracker né issue, nessuna ricerca web. Nessun `ls`, `grep` o `find` fuori dalla cartella `revisione-009/`. Le uniche due chiamate di strumento effettuate nella sessione di revisione sono le due letture dichiarate sopra.

**Impulsi di uscita dal perimetro, avuti e non seguiti.** Elencati dal revisore perché senza di essi «contesto pulito» è un'asserzione e non un fatto verificabile.

| # | Punto del documento | Che cosa avrebbe voluto verificare | Effetto sul rilievo |
|---|---|---|---|
| I1 | §4, tabella delle terne, riga «Ricavo aggiuntivo per utente al mese»: `0,60 / 1,20 / 2,40 €` | Aprire `docs/bq3_scenarios.md` per sapere se il valore centrale `1,20 €` sia derivato dal benchmark del 30% o sia esso stesso un input indipendente. Il documento dice che «il valore centrale della terna di adozione poggia su un benchmark esterno», e tace su da dove venga la terna dell'uplift. | Rende **R4** più cauto: non posso dire che l'uplift sia privo di fonte, solo che *questa pagina* non la dichiara mentre la dichiara per l'adozione accanto. |
| I2 | §4.1, tabella «base ipotizzata» | Aprire `check_audit_coherence.py` per sapere se un valore marcato `<!--#-->` (non misurato) venga davvero solo ignorato, o se la severità stretta abbia altre implicazioni sulle nove celle aritmetiche. | Rende **R2** una constatazione sul testo, non sull'implementazione: afferma che il documento pubblica nove cifre in euro senza ancora, non che il controllo sbagli. |
| I3 | §2, `375` titoli e mediana `248,00` | Aprire `kpi_measures.json` per verificare che `KPI.BQ1K1.c1.median_of_42` sia davvero la mediana dei 42 conteggi e non di altro. | Nessuno: il documento è internamente coerente e la verifica sarebbe stata una verifica del dato, non del documento. Impulso scartato come fuori metro. |
| I4 | §4.2, «un comunicato che questo progetto cita» | Cercare l'URL del comunicato per constatare se sia ancora raggiungibile e di quale operatore si tratti. | Aggrava **R3**: proprio il fatto che il revisore non possa nemmeno sapere *chi* sia l'operatore leggendo la pagina è il rilievo. |
| I5 | §5, «la versione usata qui è la `2`» | Aprire il ponte tassonomia-mood per capire se `2` sia la versione corrente o già superata. L'estratto `D` dice «oggi 2», il che concorda; ma «oggi» è datato al momento in cui quel documento fu scritto. | Nessun rilievo autonomo: le due copie concordano. Annotato come rischio di divergenza futura in «Che cosa funziona». |
| I6 | §6 e §1, «due cataloghi pubblici» | Verificare quali siano (i nomi `netflix_categories_musical` e `SP.genre.count` nelle ancore suggeriscono fortemente le due fonti, e il revisore ha dovuto trattenersi dal confermarlo). | Alimenta **R1**: il documento non nomina mai le due fonti, e la curiosità del revisore è la prova che il lettore la avrà. |
| I7 | Riga finale, `specs/009-verdetto-raccomandazione/review.md` | Aprire il verbale che il documento stesso promette — cioè questo file. Impulso circolare, scartato immediatamente. | Nessuno. |

---

## 2. Ancoraggio della versione revisionata

- **Commit del repository al momento della revisione**: `da39020`
- **Impronta SHA-256 del documento revisionato**: `83434e006b244ad8c3152d25d31e16b1212e65e216f7e5d9e10e44941543c64b`
- **Impronta SHA-256 del file di copie autorevoli**: `308ca940b800a7d0cf93ac398b76dbee9c64e6113c9b695c3944368095dd01ff`
- Il file di copie autorevoli contiene cinque estratti letterali di documenti già mergiati, delimitati per intestazione di sezione. Il revisore non ha visto ciò che in quei documenti precede o segue gli estratti, e nessun rilievo presuppone di conoscerlo.

---

## 3. I rilievi

**Criterio di gravità, dichiarato dal revisore una volta sola e applicato uniformemente:**

- **alta** — il passaggio, letto da solo o estratto, fa concludere al destinatario qualcosa di **falso**, oppure gli nega un'informazione senza la quale non può usare ciò che legge. Include ogni frase che attribuisce a StreamWave una misura che nessuno ha fatto su StreamWave;
- **media** — il passaggio è vero ma **non decodificabile** dal destinatario dichiarato (board, nessun altro documento letto, nessuno schermo), oppure diverge da una copia autorevole in modo che indebolisce una cautela;
- **bassa** — attrito di lettura, asimmetria o imprecisione che non cambia la conclusione né induce un uso errato.

Ordinati per gravità decrescente.

---

### R1 — Le due fonti non sono mai nominate, e il limite più importante del documento diventa così non valutabile

**Gravità: alta.**

Citazione, §1 (riga 25):

> Su due cataloghi pubblici usati come sostituti — un catalogo video e un catalogo musicale — perché StreamWave non ha ceduto i propri dati a questa analisi.

E §6 (riga 172):

> al posto del suo catalogo video e del suo catalogo musicale sono stati usati due cataloghi pubblici come **sostituti**.

Il documento dichiara — correttamente, con insistenza e in tre punti diversi — che tutta l'analisi poggia su due cataloghi sostitutivi, e che l'assunzione di rappresentatività «è il limite più importante di questo documento». Poi **non dice mai quali siano quei cataloghi.** Non un nome, non un proprietario, non una scala, non una provenienza.

Che cosa non funziona, e per chi. Per il destinatario dichiarato — un membro del board, competenza di business — l'assunzione di rappresentatività è l'unica cosa su cui può esercitare un giudizio autonomo: non sa valutare una mediana o un inviluppo convesso, ma sa benissimo dire se il catalogo video di un certo operatore assomigli o no a quello della propria azienda. È l'unico giudizio che gli appartiene per competenza, e il documento glielo rende impossibile fornendogli l'etichetta astratta «due cataloghi pubblici». §5 gli chiede addirittura di considerare lo scenario «se i cataloghi sostitutivi non rappresentassero StreamWave» — cioè gli chiede di valutare la rappresentatività di due oggetti anonimi.

Aggravante di estrazione: la frase «due cataloghi pubblici usati come sostituti» estratta da sola non permette a nessuno di replicare, contestare o confermare alcunché.

**Che cosa lo chiuderebbe.** Nominare le due fonti al primo uso, in §1, con una riga ciascuna: che cosa contiene ognuna, di chi è, a che anno si ferma. Sono due incisi, non una sezione. Il documento già dedica molto più spazio a spiegare *perché* i sostituti sono un limite di quanto ne dedichi a dire *quali* siano — che è l'inversione esatta di ciò che serve a chi legge.

---

### R2 — La tabella «base ipotizzata» pubblica nove importi in euro che sono i più citabili del documento e i meno difesi

**Gravità: alta.**

Citazione, §4.1 (righe 134-138):

> | Base ipotizzata da chi legge | Pessimista | Centrale | Ottimista |
> | 500.000 abbonati | 300.000 € / mese | 600.000 € / mese | 1.200.000 € / mese |
> | 1.000.000 abbonati | 600.000 € / mese | 1.200.000 € / mese | 2.400.000 € / mese |
> | 2.000.000 abbonati | 1.200.000 € / mese | 2.400.000 € / mese | 4.800.000 € / mese |

Il documento circonda questa tabella di tre cautele consecutive e ben scritte: le basi sono ipotesi di chi legge, la lettura è condizionale («se… allora»), ogni cella eredita confidenza bassa. Il problema non è che le cautele manchino. Il problema è che **la tabella è l'unico oggetto del documento che produce cifre in euro con molti zeri**, ed è per costruzione l'oggetto che verrà estratto — copiato in una slide, letto ad alta voce, ricordato. Nessuna delle tre cautele sopravvive all'estrazione: la riga «`1.000.000 abbonati` → `1.200.000 € / mese`» estratta da sola afferma che l'offerta musicale di StreamWave varrebbe 1,2 milioni di euro al mese, che è precisamente ciò che il documento dichiara di non dire.

Il documento **sa** che accadrà. Lo scrive esplicitamente, riga 142:

> Non è un presidio: è una rinuncia, e non impedisce a valle l'operazione che scoraggia. Un totale di ricavo costruito su questi numeri e presentato senza la propria banda sarebbe un numero che nessuno ha misurato, con l'autorevolezza di uno misurato.

Qui c'è una contraddizione interna che va nominata: la copia autorevole `B` (estratto dagli scenari) usa quella stessa frase per giustificare il fatto che **quel documento non fornisce il moltiplicatore** — «qui nessuna base utenti viene quantificata, per la decisione presa nella revisione della `001`, e che l'artefatto non offre alcuna chiave per farlo». La raccomandazione conserva la frase parola per parola e **fa esattamente l'operazione che la frase esisteva per non fare**: fornisce tre moltiplicatori e ne pubblica i nove prodotti. Ha ereditato la giustificazione e abbandonato la condotta che quella giustificazione descriveva.

Che cosa non funziona, e per chi. Per il board: riceve nove cifre a sette zeri che non provengono da alcun dato e che ricorderà meglio di ogni cautela che le circonda. Per il progetto: una decisione presa in una revisione precedente (non quantificare la base) viene di fatto revocata da un documento che ne cita ancora la motivazione.

**Che cosa lo chiuderebbe.** Tre vie, in ordine di preferenza decrescente:

1. eliminare la tabella e lasciare la frase che spiega l'aritmetica («chi disponga di una stima della base moltiplichi i valori per utente; l'operazione richiede pochi secondi»). Il board sa moltiplicare;
2. tenere una sola riga a base **manifestamente convenzionale** — `100.000` o `1` abbonato — così che nessuna cella possa essere scambiata per una stima di StreamWave;
3. se la tabella resta com'è, sostituire l'intestazione di colonna «Base ipotizzata da chi legge» con qualcosa che sopravviva all'estrazione della singola riga, e ripetere il vincolo dentro ogni cella o nell'intestazione delle colonne — perché è la riga, non la tabella, l'unità che verrà estratta.

Nota di perimetro: l'impulso I2 (non seguito) riguardava se il controllo automatico tratti queste nove cifre come non-misurate. Il rilievo non dipende da quella risposta — è un rilievo sulla leggibilità, non sull'ancoraggio.

---

### R3 — Il benchmark che sostiene tutta la sezione economica è irriconoscibile: non si dice di chi sia, né quanto valga

**Gravità: alta.**

Citazione, §4.2 (righe 146 e 150):

> Il valore centrale della terna di adozione poggia su un **benchmark esterno**: una cifra pubblicata da un altro operatore, in un comunicato che questo progetto cita.
> […] Il benchmark descrive **un altro operatore, su un altro mercato, otto anni prima**.

Il documento è ammirevolmente onesto sulla fragilità di questa fonte — lo studio non è nominato, non esiste copia archiviata, l'assunzione di trasferimento non è verificabile. Ma non dice **tre cose fattuali** che chi legge non può ricostruire da nessuna parte della pagina:

1. **chi** sia l'operatore (né il nome, né il settore, né il paese: «un altro mercato» può significare un altro paese o un'altra categoria merceologica, e le due cose hanno implicazioni opposte per la trasferibilità);
2. **quale cifra** il comunicato riporti — se il 30% della terna di adozione sia la cifra del benchmark oppure una sua rielaborazione;
3. **dove** sia il comunicato, sia pure come nota.

Che cosa non funziona, e per chi. Il documento chiede al board di accettare una cifra su cui poggia l'intera sezione economica, gli spiega con cura perché quella cifra sia debole, e non gli fornisce l'unico elemento con cui potrebbe giudicare da sé se la debolezza sia tollerabile: sapere di chi si tratti. Un board che conosca il settore ha un'opinione informata su «l'operatore X ha dichiarato il 30% di adozione nel 2018»; non ne ha nessuna su «un altro operatore, su un altro mercato, otto anni prima».

C'è inoltre un'asimmetria che rende la scelta non difendibile come riservatezza: il documento non nomina neppure StreamWave con un dato proprio, quindi non c'è nulla di confidenziale da proteggere; e la copia autorevole `B` presuppone un lettore che possa «aprire il comunicato citato e constatare che riporti quella cifra». Il verbo *citare* nella copia autorevole implica un riferimento risolvibile. Nella raccomandazione «un comunicato che questo progetto cita» diventa un rimando a un altro documento per un'informazione che serve **subito**, che è precisamente ciò che §1 (riga 11) promette di non fare: «non rimanda altrove per informazioni che servono a capire le frasi che contiene».

**Che cosa lo chiuderebbe.** Una riga in §4.2 con: nome dell'operatore, cifra dichiarata, anno, e riferimento al comunicato. Tutte le cautele esistenti restano com'è.

---

### R4 — «otto anni prima» e «2018» sono in tensione con la data del documento, e non collimano

**Gravità: media.**

Citazioni. §4.2, riga 150:

> Il benchmark descrive **un altro operatore, su un altro mercato, otto anni prima**.

§5, riga 164, e §6, riga 183:

> il benchmark economico al 2018.

Il documento è datato **2026-08-29** (riga 3). Il benchmark è del **2018**. La distanza è di **otto anni** rispetto al 2026 — quindi «otto anni prima» significa *otto anni prima di oggi*, non *otto anni prima* di qualcos'altro nominato nella frase. Ma la frase in cui compare parla del benchmark rispetto a StreamWave e ai dati dell'analisi, che si fermano al **2021-2022**: rispetto a quelli la distanza è di tre o quattro anni. Il lettore che incontra «otto anni prima» in §4.2 senza aver ancora incontrato il «2018» (che compare solo in §5 e §6, più avanti) non ha alcun riferimento rispetto a cui contare otto anni.

Aggravante: la formulazione compare **due volte identica** (riga 150 e riga 175, in §6), sempre senza l'anno accanto, mentre l'anno compare due volte altrove sempre senza gli «otto anni» accanto. Le due informazioni non si incontrano mai nella stessa frase.

Che cosa non funziona, e per chi. Per il board: «otto anni prima» è un'espressione relativa senza referente esplicito, ed è per di più l'unico luogo del documento in cui un numerale in lettere qualifica un fatto misurato in modo che il lettore possa contare a mente e sbagliare.

**Che cosa lo chiuderebbe.** Scrivere in §4.2, al primo uso: «descrive un altro operatore, su un altro mercato, nel 2018 — otto anni prima di questa analisi». Poi la ripetizione in §6 può restare com'è.

---

### R5 — La riformulazione della cautela sulla banda è più larga dell'originale: sparisce «l'ampiezza non ha interpretazione probabilistica»

**Gravità: media.** (Divergenza fra copie.)

Copia autorevole `B`, estratto dagli scenari §8:

> **Il range non è un intervallo di confidenza.** Non c'è alcun «95%» dentro questi numeri, e **l'ampiezza non ha interpretazione probabilistica**. Chiedere con che probabilità il vero valore cada nella banda è una domanda a cui questo documento non risponde.

Raccomandazione, §6 (riga 181):

> La banda fra pessimista e ottimista non è un intervallo di confidenza: non c'è alcuna probabilità dentro quei numeri, e chiedere con che probabilità il valore vero vi cada è una domanda a cui questo documento non risponde.

La riformulazione conserva due delle tre affermazioni e **lascia cadere la terza**: che *l'ampiezza* della banda non abbia interpretazione probabilistica. Non è ridondante rispetto alle altre due. «Non c'è alcuna probabilità dentro quei numeri» nega che le tre cifre siano probabilità; non nega che la **distanza fra pessimista e ottimista** significhi qualcosa — ed è esattamente l'inferenza che un lettore di business fa spontaneamente («la banda è larga, quindi c'è molta incertezza; se fosse stretta, saremmo più sicuri»). L'originale la blocca esplicitamente, la riformulazione no.

Che cosa non funziona, e per chi. Per il board, che è precisamente il lettore che tratterà l'ampiezza come una misura dell'incertezza. La cautela sopravvissuta risponde a una domanda che il board non si pone; quella caduta rispondeva a quella che si pone.

**Che cosa lo chiuderebbe.** Reintegrare la clausola: «…e l'ampiezza della banda non misura quanto siamo incerti: non ha interpretazione probabilistica».

---

### R6 — «graduatoria», «mediana» e «margine»: tre termini tecnici usati senza essere sciolti al primo uso, in un documento che scioglie tutto il resto

**Gravità: media.**

Il documento ha una disciplina esplicita e ben eseguita di traduzione — «In italiano: …» apre ciascuna delle tre condizioni di §2, e funziona. Tre eccezioni le sfuggono, tutte in posizioni portanti.

**(a) «mediana»**, §2 (riga 37), primo uso:

> il numero di titoli della categoria `Music & Musicals` supera la mediana dei conteggi delle 42 categorie del catalogo. Quel conteggio vale 375 titoli contro una mediana di 248,00

La versione «in italiano» che precede dice «sta nella metà più popolata delle categorie», il che è una buona parafrasi — ma il termine *mediana* poi ricorre da solo, senza appoggio, in §3 (riga 95: «sopra la mediana per domanda e sopra la mediana per affinità») dove nessuna parafrasi lo accompagna. Il destinatario dichiarato non ha competenza statistica: *mediana* è la parola statistica per eccellenza che un non tecnico confonde con *media*, e la confusione qui non è innocua — con la media, `375` contro una media dei conteggi sarebbe un'affermazione diversa.

**(b) «margine»**, §2.4 (riga 73). Il documento introduce il concetto, lo spiega bene («è una condizione sull'errore, non una stima dell'errore»), e poi lo usa in §5 (riga 159) presupponendo la definizione. Accettabile. Ciò che non è accettabile è la **forma numerica**: `0,4083` — vedi R7.

**(c) «affinità»**, §2 (riga 55) e §3 (riga 95). Compare cinque volte e non è mai definita. Il lettore può inferire che significhi «somiglianza di carattere col catalogo video» dal contesto di C2, ma il documento non lo dice mai, e in §3 «sopra la mediana per affinità» arriva a un lettore che deve tenere insieme due mediane su due grandezze di cui una non ha nome proprio.

**Che cosa lo chiuderebbe.** Per (a): al primo uso, «la mediana — il valore che divide le categorie in due metà uguali, metà sopra e metà sotto». Per (c): un inciso al primo uso di *affinità* in §2, che è già il luogo dove il documento traduce.

---

### R7 — I numeri sono pubblicati in forma di frazione decimale a quattro cifre, che è la forma meno leggibile possibile per il destinatario dichiarato

**Gravità: media.**

Citazioni, tutte in posizione portante:

- §2 (riga 41): «La quota della categoria musicale sull'intero catalogo vale **0,0426**, cioè una frazione piccola.»
- §2 (riga 47): «vale **0,8450**, contro una soglia di maggioranza semplice fissata a **0,5000**»
- §2.4 (riga 73): «La distanza fra il valore misurato e la soglia vale **0,3450**, che è **0,4083** del valore stesso.»
- §5 (riga 159): «più di **0,4083** del proprio valore.»

Il documento pubblica **le percentuali della tabella economica in percentuale** (`15% / 30% / 60%`, riga 119) e **le quote analitiche in frazione decimale a quattro decimali**. Le due convenzioni convivono nella stessa pagina senza che nulla lo segnali. Per il board, «0,8450» richiede una conversione mentale che «84,5%» non richiede; e «0,0426, cioè una frazione piccola» chiede al lettore di fidarsi della qualificazione verbale perché la cifra non gliela comunica.

Il caso peggiore è la riga 73: **«0,3450, che è 0,4083 del valore stesso»** mette due frazioni decimali diverse — una differenza assoluta e un rapporto — nella stessa frase, entrambe a quattro decimali, entrambe senza unità, e chiede al lettore di distinguerle. È la frase che introduce il concetto centrale di §2.4, e nella forma attuale è la meno leggibile del documento.

Aggravante specifica: `0,4083` viene poi ripetuto in §5 (riga 159) come «più di 0,4083 del proprio valore», dove la locuzione «più di [una frazione] del proprio valore» è di per sé sintatticamente ostica — «più del 41% del proprio valore» sarebbe immediata.

Che cosa non funziona, e per chi. Per il board, che deve tenere a mente la soglia decisionale del documento. Il rilievo è di forma e non di sostanza — i valori sono corretti e ancorati — ma la forma è precisamente ciò su cui questo documento si gioca, perché è l'unico del progetto scritto per chi non legge gli altri.

**Che cosa lo chiuderebbe.** Non necessariamente cambiare le ancore: affiancare la lettura percentuale in prosa accanto al valore ancorato. Per esempio «vale 0,8450 — cioè poco più dell'84% del catalogo musicale». Se la convenzione di marcatura del progetto non consente due forme dello stesso valore, allora almeno uniformare la sezione economica alla stessa convenzione, così che il lettore non incontri due grammatiche numeriche.

---

### R8 — §3 promette di caratterizzare una regione e poi ne nomina un solo membro

**Gravità: media.**

Citazioni, §3 (righe 85 e 95-97):

> **La raccomandazione non è entrare da un genere.** È entrare da una **regione del catalogo musicale**, che i segmenti qui sotto servono a caratterizzare — non a delimitare.
> […] Dei 114 segmenti che l'analisi ordina, 33 si collocano contemporaneamente sopra la mediana per domanda e sopra la mediana per affinità […]. Il candidato di punta è il segmento `pop`, che occupa la posizione 1 della graduatoria […]

La sezione annuncia una regione di 33 segmenti, spiega con cura perché non vada letta come una classifica, e poi **elenca un solo segmento**: `pop`, quello in posizione 1. Gli altri 32 non sono nominati — mai, in nessun punto del documento.

L'effetto è l'opposto dichiarato. Un lettore che riceve «entrate da una regione, non da un genere» seguito da un unico nome proprio conclude che il genere sia `pop`: è l'unica cosa che può portare via dalla sezione. Il paragrafo successivo (riga 99) prova a bloccare l'inferenza — «Non dice che sia il solo da cui entrare, né che gli altri della regione siano alternative da scartare» — ma sta chiedendo al lettore di non concludere qualcosa dopo avergli fornito i materiali per concluderla e nient'altro.

Aggravante di asimmetria, e questa è la parte che rende il rilievo non solo estetico: il documento **nomina per esteso tutti e 7** i segmenti dell'esclusione (riga 103: `country`, `iranian`, `jazz`, `latin`, `rock`, `romance`, `soul`) e **uno solo dei 33** della regione raccomandata. Il lettore esce dalla sezione conoscendo sette nomi da cui *non* entrare e un nome da cui entrare. È esattamente rovesciato rispetto alla funzione della sezione, che si intitola «Con che cosa entrare».

**Che cosa lo chiuderebbe.** Elencare i 33 segmenti della regione — o, se sono troppi per la prosa, i primi cinque o dieci in graduatoria, dichiarando che l'elenco è un estratto e che la regione ne comprende 33. La cautela di riga 99 diventerebbe finalmente credibile, perché ci sarebbero più nomi fra cui non scegliere.

---

### R9 — «Sull'esito la soglia è ininfluente su questi dati» è affermato senza il valore che lo sostiene

**Gravità: media.**

Citazione, §2.4 (riga 79):

> Con una soglia di due terzi invece della maggioranza semplice varrebbe meno della metà. […] chi ritenesse che «maggioranza» debba significare qualcosa di più severo troverebbe un margine più stretto, pur trovando la stessa risposta. **Sull'esito la soglia è ininfluente su questi dati; sul margine no.**

Due affermazioni derivate qui non portano il proprio valore.

La prima, «con una soglia di due terzi […] varrebbe meno della metà», è un calcolo che il lettore può fare solo se ricostruisce a mente: il margine passerebbe da `0,8450 − 0,5000` a `0,8450 − 0,6667`, cioè da `0,3450` a circa `0,178`. Il documento afferma il risultato senza pubblicare né la soglia alternativa né il margine che ne risulta. La copia autorevole `C` (nota di aggiunta) dice la cosa più prudente e senza numeri: «Entrambe dipendono dalla soglia e si restringerebbero con una soglia più severa». La raccomandazione **quantifica** dove l'originale si limita a indicare una direzione, e lo fa senza ancora.

La seconda, «Sull'esito la soglia è ininfluente su questi dati», è più forte e più esposta. Vera per la soglia dei due terzi che la frase nomina, e vera per qualunque soglia fino a `0,8450` — ma la frase non dichiara **entro quale intervallo** l'ininfluenza valga. Estratta, «la soglia è ininfluente sull'esito» è un'affermazione universale e falsa: con una soglia del 90% l'esito cambierebbe.

Che cosa non funziona, e per chi. Per chiunque debba difendere la raccomandazione da un'obiezione metodologica sulla soglia — che è l'obiezione più prevedibile che questa analisi riceverà. Chi la difende ha una frase forte in mano e nessun numero sotto.

**Che cosa lo chiuderebbe.** Riformulare con l'estremo esplicito: «l'esito non cambierebbe con nessuna soglia fino a 0,8450, cioè fino al valore misurato stesso; cambia solo una soglia più severa di così». Questa forma è insieme più forte, più difendibile ed elimina l'ambiguità dell'estrazione.

---

### R10 — Il documento promette in apertura di non delegare, e alla riga 25 delega la propria clausola più importante

**Gravità: bassa** (per l'effetto pratico: il rinvio è interno alla stessa pagina), **ma la nomino perché è una promessa esplicita non mantenuta.**

Citazione, §1 (righe 11 e 25):

> Non richiede di aver letto alcun altro documento del progetto, **non rimanda altrove per informazioni che servono a capire le frasi che contiene** […]
> […] è il limite più importante di questo documento: **la sezione «che cosa questa raccomandazione non è» lo tratta per esteso**.

La promessa riguarda i rimandi ad *altri documenti*, e il rinvio della riga 25 è interno — dunque non è una violazione letterale. Ma è, funzionalmente, la stessa cosa: il documento identifica il proprio limite più importante e ne rimanda la trattazione a sei sezioni più avanti, in un documento dichiaratamente scritto per essere letto e citato per parti. Il lettore che legge §1 e §2 e si ferma — che è il lettore modale di una raccomandazione al board — ha ricevuto il verdetto e una menzione del limite, non il limite.

Va detto che §1 fa comunque il lavoro minimo essenziale, con la frase in grassetto della riga 25: «**Nessun numero di questa pagina è una misura fatta su StreamWave.**» Questa è la migliore frase del documento e regge da sola. Il rilievo è che sia collocata *dopo* il rinvio anziché al suo posto.

**Che cosa lo chiuderebbe.** Invertire l'ordine dentro il capoverso: prima la frase in grassetto, poi il rinvio per approfondire. Costo: zero.

---

### R11 — La sezione «Come si verifica» chiude il documento parlando a un lettore che non è quello dichiarato

**Gravità: bassa.**

Citazione, righe 187-196: il blocco `bash` con i due comandi `python3`, la nozione di «severità stretta», il rimando a `specs/009-verdetto-raccomandazione/review.md`.

Il documento dichiara in apertura (riga 11) di non presupporre «competenza tecnica». La sezione finale presuppone che il lettore sappia cosa sia un terminale, che abbia il repository clonato e che sappia interpretare «una quantità priva di ancora o di dichiarazione esplicita di non-misurato è un errore, non un avviso» — frase che contiene tre termini di gergo di progetto (*ancora*, *non-misurato*, *severità stretta*) di cui il documento ne scioglie uno solo, e solo a metà, alla riga 13 («un riferimento invisibile, verificabile con un comando»).

Non è grave: è l'ultima sezione, è chiaramente delimitata, e il paragrafo «Che cosa un esito verde certifica, e che cosa no» è ottimo e comprensibile anche a chi salta i comandi. Il rilievo è che il documento cambia destinatario senza dirlo, mentre altrove è scrupoloso nel dichiarare i propri confini.

**Che cosa lo chiuderebbe.** Una riga d'apertura di sezione: «Questa sezione è per chi voglia rifare i conti sul repository; il resto della pagina non la richiede.»

---

### R12 — «`pop` occupa la posizione 1 della graduatoria» non dichiara di quanti

**Gravità: bassa.**

Citazione, §3 (riga 97):

> Il candidato di punta è il segmento `pop`, che occupa la posizione **1** della graduatoria costruita combinando domanda e affinità con peso uguale.

«Posizione 1» è un ordinale la cui informatività dipende interamente dalla dimensione dell'insieme ordinato, e la frase non la dichiara. Il lettore può recuperarla dalla riga 95 (114 segmenti ordinati, 33 nella regione) se legge le due frasi consecutivamente, ma non se estrae la frase — ed è una frase molto estraibile, essendo l'unico nome proprio raccomandato del documento. «Primo su 114» e «primo su 33» sono affermazioni diverse, e il documento non chiarisce quale delle due sia (la graduatoria è «costruita combinando domanda e affinità», il che suggerisce che ordini tutti i 114, ma la frase è nella sottosezione «La regione», che parla dei 33).

**Che cosa lo chiuderebbe.** «occupa la posizione 1 fra i 114 segmenti ordinati» — o `33`, secondo quale sia il vero.

---

## 4. Che cosa funziona

*Elencato dal revisore perché chi corregge non lo rompa.*

- **La struttura complessiva regge il metro.** Sei sezioni in ordine: la risposta, il perché, il cosa fare, il quanto vale, il cosa la ribalterebbe, il cosa non è. È l'ordine giusto per un decisore, e ogni sezione mantiene ciò che il titolo promette.

- **La prima frase risponde.** «**Sì: l'espansione nel music streaming è coerente con il catalogo che StreamWave ha già.**» Non gira attorno, non premette cautele, e sopravvive all'estrazione — perché contiene la propria qualificazione («coerente con il catalogo», non «conveniente»). Il capoverso immediatamente successivo, «Che cosa questa risposta non dice», è il presidio corretto nella posizione corretta.

- **Il trattamento della confidenza del verdetto (§2.4) è il passaggio migliore del documento.** «Una congiunzione di condizioni non è più affidabile del suo termine meno affidabile» è comprensibile senza competenza statistica, è argomentata, e la conclusione — confidenza media, non alta — va contro l'interesse retorico di chi scrive. È il tipo di passaggio che rende credibile tutto il resto.

- **La distinzione «condizione sull'errore» / «stima dell'errore» (riga 77)** è precisa, difficile, e spiegata bene. Anticipa la lettura sbagliata esatta che un lettore farebbe. Non toccarla.

- **La qualificazione dei 7 segmenti a popolarità zero (§3, righe 103-107)** è metodologicamente irreprensibile: distingue «non misurato» da «basso», nomina tutti e sette i segmenti, e ne trae il vincolo operativo giusto («la coda della graduatoria non si legge»). È l'unico luogo del documento in cui un elenco è completo — vedi R8 per l'asimmetria che ne discende.

- **Le due qualificazioni d'unità di §4 (righe 124-126)** — tasso lordo, livello mensile a regime e non cumulato — sono fedeli alla copia autorevole `B` e la riformulazione non perde nulla. In particolare «Moltiplicarlo per dodici produrrebbe un cumulato che vale solo sotto l'assunzione che la base resti costante» rende operativa una cautela che nell'originale era più astratta: qui la raccomandazione **migliora** la fonte.

- **§5 mantiene la propria promessa** («per ciascuna è scritto che cosa succederebbe, non soltanto che esiste un rischio») e la mantiene davvero: il secondo punto arriva fino a dire che l'esito passerebbe a «sostegno parziale» e **non** a «argomento non sostenuto», che è la precisazione che un rischio dichiarato pigramente ometterebbe. La corrispondenza con la copia autorevole `A` (regola di decisione, «due su tre → sostegno parziale») è esatta.

- **Il verdetto e la regola di decisione non divergono dalla copia `A`.** «Tre condizioni su tre → l'argomento di coerenza è sostenuto: l'espansione è un'estensione del catalogo esistente» è ripreso alla lettera. La rivendicazione che il criterio sia stato fissato prima dei numeri è corretta e non sovradichiarata (la copia `A` è più esplicita nel dire che l'autore aveva ispezionato i dati; la raccomandazione non lo ripete, ma nemmeno afferma il contrario — non lo conto come divergenza perché la raccomandazione rivendica solo che la regola sia pubblica e non spostabile, che è la stessa garanzia dell'originale).

- **La stima per eccesso (§2.4, riga 65) è fedele alla copia `C`** e la traduce bene per un non tecnico: «È una scatola che contiene la regione reale ma è più grande di essa». La formula «la sovrapposizione reale è minore o uguale a 0,8450, e quanto minore questo progetto non lo misura» è riportata parola per parola dall'originale.

- **La grana dei segmenti (§3, righe 87-91) è fedele alla copia `E`**: non sommabilità, contare le righe non dimensiona un mercato, sovrapposizione per costruzione. Nessun indebolimento.

- **§6 è la sezione più forte del documento.** In particolare l'argomento per cui le due assunzioni di trasferimento restano fuori dalla scala di confidenza «per costruzione» (riga 177) — «un valore può essere impeccabile come misura e non dire nulla del soggetto a cui lo si vuole applicare» — è la formulazione più utile dell'intera pagina per un decisore, e non ha equivalente nelle copie autorevoli. È un contributo originale della `009` e va difeso.

- **Nessuna divergenza rilevata fra deliverable e copie autorevoli, salvo R5.** Il revisore dichiara di aver confrontato riga per riga le cinque copie con i passaggi corrispondenti. La sola cautela che perde un pezzo è quella sulla banda probabilistica. La riformulazione di R2 (frase su «non è scalabile») è fedele nel testo ma incoerente nella condotta — contata dentro R2, non come divergenza testuale.

- **Nota su I5**: il documento dichiara la versione `2` della tabella dei mood, coerente con la copia `D` («oggi 2»), e riporta correttamente il contratto («una revisione invalida i valori che ne dipendono invece di correggerli»). Le due copie concordano oggi. Il revisore segnala che la raccomandazione è il documento più esposto a quel contratto e il più letto da fuori: se la tabella passasse a `3`, questa pagina sarebbe la prima da invalidare e l'ultima che qualcuno penserebbe di controllare. Non è un rilievo sul testo attuale.

---

## 5. La risposta alla domanda centrale

**Sì. Un decisore che non ha letto nulla, leggendo il solo deliverable, conclude qualcosa — e ciò che conclude è in larga parte ciò che il documento vuole.** Questo documento supera il metro su cui una feature precedente del progetto è stata fermata. Non è un giudizio di cortesia: la prima frase risponde, la qualificazione «coerente ≠ redditizio» arriva subito e in forma memorizzabile, e il limite dei cataloghi sostitutivi è affermato tre volte in punti diversi con la frase «Nessun numero di questa pagina è una misura fatta su StreamWave» che regge estratta.

**Che cosa conclude, in concreto.** Che l'espansione nel music streaming è coerente col catalogo esistente; che «coerente» non significa «redditizia» e che i costi non sono stati considerati; che la conclusione poggia su dati sostitutivi e non su dati aziendali; che l'unica cosa da fare, se la raccomandazione è presa sul serio, è rifare l'analisi sui dati reali. Sono quattro conclusioni corrette e sono le quattro che il documento intende.

**Dove ciò che conclude diverge da ciò che il documento vuole**, e sono tre punti, tutti dovuti al fatto che la memoria del lettore trattiene i nomi e le cifre grandi e non trattiene le clausole che le circondano:

1. **Uscirà con «pop»** come genere da cui entrare, nonostante §3 esista per impedirlo, perché `pop` è l'unico nome proprio raccomandato in tutta la pagina mentre i sette segmenti da non leggere sono nominati tutti (R8);
2. **Uscirà con una cifra in euro a sette zeri** — quasi certamente `1.200.000 € / mese`, la cella centrale della riga centrale — nonostante tre cautele consecutive dicano che non è una stima di nulla, perché è l'unico oggetto della pagina che produca euro (R2);
3. **Non uscirà in grado di giudicare il limite che il documento stesso definisce «il più importante»**, perché per farlo dovrebbe sapere quali siano i due cataloghi sostitutivi e chi sia l'operatore del benchmark, e la pagina non lo dice mai (R1, R3).

I primi due sono difetti di **estrazione**: il documento dice la cosa giusta e la circonda male. Il terzo è un difetto di **completezza**, ed è quello che il revisore considera il più serio, perché il documento spende molte righe a spiegare al board che deve valutare un'assunzione e poi gli nega gli unici tre fatti — quali cataloghi, quale operatore, quale cifra — con cui potrebbe valutarla. Nella sua forma attuale la pagina chiede al lettore di prendere sulla fiducia proprio il punto su cui gli chiede di non fidarsi.

Nessuno dei dodici rilievi tocca il verdetto: la risposta è data, è corretta, è correttamente qualificata, e non diverge da alcuna copia autorevole.
