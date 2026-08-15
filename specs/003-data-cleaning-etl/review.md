# Revisione in contesto pulito — `docs/data_cleaning.md`

**Data**: 2026-08-11
**Oggetto**: `docs/data_cleaning.md` (feature 003 — Data Cleaning & ETL)
**Natura della revisione**: contesto pulito. Chi scrive non ha partecipato alla stesura del documento, non ne conosce le decisioni preparatorie e non ha potuto chiedere chiarimenti. Il documento è stato letto come lo leggerà chi lo riceve.

## Cosa è stato letto, e cosa no

**Letto**, nell'ordine:

1. `docs/data_cleaning.md`, per intero, una volta, senza tornare indietro e senza aprire altro (Prova 1);
2. `reports/data_profile.json` e `reports/cleaning_report.json`, solo dopo la Prova 1 e solo per verificare la tracciabilità dei valori;
3. `scripts/check_audit_coherence.py`, letto per intero. **Va dichiarato**: la lettura non era prevista come obbligatoria, ma è diventata necessaria per verificare le garanzie che §2 enuncia sul proprio meccanismo di controllo. Senza leggerlo non era possibile stabilire se quelle garanzie fossero vere *come enunciate*, che è ciò che la Prova 2 richiede. Il documento delega la propria chiave di lettura a un file che non pubblica;
4. `python3 scripts/check_audit_coherence.py`, eseguito. **Il suo esito non è stato preso per buono**: la risoluzione delle ancore, il confronto con gli artefatti, il conteggio degli avvisi, le identità aritmetiche di §5, il conteggio dei generi di §7 e la sensibilità della soglia sono stati riscritti e rieseguiti in modo indipendente, con codice proprio. Dove i due risultati coincidono lo si dice; dove il controllo tace su qualcosa che avrebbe dovuto vedere, lo si dice altrettanto.

**Non letto**, per vincolo di perimetro: nulla sotto `specs/` (di quella cartella è stata verificata solo l'esistenza, per sapere dove scrivere questo verbale), `CLAUDE.md`, `README.md`, la constitution, `docs/roadmap.md`, `docs/business_case.md`, `docs/data_audit.md`. Nessun comando `git`. `scripts/build_datasets.py` non è stato aperto: non è servito.

**Tre punti in cui il documento ha costretto a voler uscire dal perimetro.** Sono registrati qui perché il fatto stesso è un ritrovamento, e tornano come divergenze in fondo:

- §2 rimanda a `specs/003-data-cleaning-etl/contracts/output-datasets.md` §3 per la definizione delle quattro forme di marcatura. La chiave di lettura del documento sta fuori dal documento, in una cartella di lavorazione che il lettore esterno non ha ragione di aprire;
- D3 dichiara che una nota in loco «va apposta in §5.2 del business case, ed è debito di questa feature». Non è verificabile senza aprire `docs/business_case.md`. Il documento afferma un debito proprio senza dire se sia stato saldato;
- §11 parla di avvisi sul documento di audit. Il numero dichiarato non coincide con quello che il controllo emette oggi (rilievo R2), e capire perché richiederebbe di aprire `docs/data_audit.md`.

## Esito complessivo

**Il documento non è ancora presentabile a un board, ma non per le ragioni che di solito rendono impresentabile un documento di questo tipo.**

L'impianto argomentativo è solido e in più punti notevole. Le nove decisioni sono dichiarate una per una con ragione, effetto misurato e osservazione di appoggio; §9 e §10 sono fra le sezioni meglio scritte che si possano leggere su un artefatto di pulizia dati, perché distinguono la confidenza *rispetto al dataset* dalla trasferibilità *al committente* e lo dicono a chiare lettere; D5 è una regola di metodo che vale più della feature che l'ha prodotta; §8 chiude la porta alla sommabilità dei conteggi con una precisione che raramente si trova.

**E la verifica indipendente conferma la parte che più conta**: tutte e **99** le ancore ben formate risolvono nell'unione dei due artefatti e coincidono carattere per carattere con il valore registrato — zero riferimenti mancanti, zero divergenze. Tutte le identità aritmetiche interne tornano: 1.002 + 22 + 6 = 1.030; 114.000 − 450 = 113.550; 26,53%, 20,97% e 13,95% si ricalcolano esattamente dai valori ancorati; 8.797 + 10 = 8.807; le liste registrate hanno esattamente la lunghezza che il testo dichiara (22, 6, 7, 3). I conteggi di §5 sui generi (78 e 48) e l'affermazione di §7 sull'insieme identico prima e dopo la trasformazione sono stati riprodotti da zero e risultano esatti. Questo è lavoro fatto bene e va detto con la stessa precisione con cui si segnala un difetto.

Il problema è altrove, ed è più serio: **il documento fonda la propria credibilità su un meccanismo di controllo, descrive quel meccanismo con garanzie più forti di quelle che offre, e il meccanismo fallisce in silenzio proprio sul numero di testa della prima decisione.** Cinque ancore sono corrotte: nel Markdown reso il lettore trova `15.844.rows.after-->` al posto di un valore, e il controllo non se ne accorge perché le declassa a «non misurato» invece di fallire. Accanto a questo, un numero pubblicato in §11 è contraddetto dal comando che il documento stesso invita a eseguire.

Per un artefatto la cui tesi è «chi legge può non fidarsi di me, ma può verificare», un meccanismo di verifica che sbaglia in silenzio non è un difetto fra gli altri: è il difetto. I rilievi R1, R2 e R3 vanno chiusi prima di qualunque presentazione. Gli altri sono correggibili con interventi circoscritti.

---

## Prova 1 — Comprensione

Una sola lettura integrale, senza ritorni indietro e senza aprire nient'altro. Le risposte che seguono sono state formulate a documento chiuso.

### Che cosa fa questa feature ai dati, e perché

Prende due dataset pubblici — un catalogo video e un catalogo musicale — e ne produce quattro file trasformati, che non entrano nel repository. Il *perché* passa con chiarezza fin da §1, ed è la parte meglio riuscita del documento: gli output non si versionano, si versiona la pipeline; quindi ciò che va versionato è la **dichiarazione delle decisioni**, non i dati. Il documento capisce di essere l'unico strumento con cui una decisione di trattamento diventa contestabile da chi i dati non li ha. È un'ottima ragione d'essere, esposta in due paragrafi.

### Quali decisioni dichiara di aver preso

Nove, in due gruppi: cinque ereditate dalle revisioni precedenti (popolarità zero conservata e marcata; riparazione di uno scivolamento di colonna su tre titoli; totali di catalogo sulla grana traccia; soglia al 50% per i generi a forte concentrazione di zeri; le affermazioni derivate come valori da ancorare) e quattro emerse dalla ricognizione (deduplicazione della coppia traccia-genere; massimo osservato sulle popolarità discordi; conversione delle date con mappa esplicita dei mesi; normalizzazione di un solo campo multi-valore su quattro).

**La più discutibile, a lettura chiusa, è D2** — la riparazione dello scivolamento di colonna. Non perché sia mal argomentata: è argomentata meglio di tutte le altre, con un vincolo sul raggio d'azione che la rende difendibile e una confidenza dichiarata «media» in §9. È discutibile perché è l'unico punto in cui la feature **scrive un valore in un campo in cui la fonte non l'aveva messo**, cioè fa esattamente la cosa che tutto il resto del documento si vieta. Il documento lo sa e lo dice; resta il punto su cui un board tornerà per primo.

**La seconda più discutibile è D4**, e per una ragione che alla prima lettura è rimasta come un'increspatura: la soglia del 50% è motivata dal comportamento della **mediana** («se più della metà delle righe vale zero, il valore centrale è zero»), e nello stesso paragrafo il documento spiega che le mediane per genere non si possono calcolare qui perché appartengono alla feature 005. La soglia è dunque giustificata da una misura che la feature dichiara fuori dal proprio perimetro. L'argomento resta valido — è una proprietà della definizione di mediana, non una stima — ma la tensione è reale e il documento non la scioglie.

### Che cosa dichiara esplicitamente di non fare

§10 è esplicito e ben costruito: nessuna delle tre domande di business, nessun KPI, nessuna stima, nessuna raccomandazione; nessun modello dati (è la 005); nessuna definizione di «segmento»; nessuna scelta di quale grana musicale una misura debba usare, salvo il vincolo di D3 sui totali. Aggiunge quattro «inferenze da evitare», fra cui la migliore del documento: *un dataset pulito non è un dataset rappresentativo*.

### Riesce a spiegare perché esiste?

**Sì, e meglio della media.** §1 risponde alla domanda in due paragrafi senza retorica, e §10 chiude il cerchio dichiarando il compromesso invece di attenuarlo («Chi ha i dati confronta le impronte; chi non li ha si affida a tre artefatti leggibili invece che a un file che non può aprire. È un compromesso, e va dichiarato invece che attenuato»). Su questo il documento non ha nulla da farsi perdonare.

### Punti rimasti oscuri alla prima lettura

Sono la parte più utile della prova e vanno registrati come sono venuti.

1. **Il testo rotto nelle tabelle.** In §4 e in §5 l'occhio inciampa su `.rows.after-->`, `.count-->`, `.pct-->` dove ci si aspetta un numero. Alla prima lettura è sembrato un refuso di rendering. È il rilievo R1, ed è la cosa più grave del documento.
2. **La numerazione di §4 collide con quella delle sezioni.** Le sottosezioni si chiamano «6», «7», «8», «9» e convivono con le sezioni §5, §6, §7, §8. Dentro la sottosezione «7» si legge «Vedi §6 del documento»: per capire dove andare si è dovuti tornare all'indice mentale. È R10.
3. **«Cinque sono quelle ereditate»** non si è lasciato far tornare con la tabella sottostante. Ci si è dovuti fermare a contare. È R8.
4. **Che cosa sia esattamente il «criterio stretto»** di §5 non è rimasto chiaro: si capisce che 78 e 48 differiscono per la precisione del confronto, non si capisce da dove venga la differenza. La verifica ha poi mostrato che la spiegazione data non è la causa reale. È R5.
5. **«Un margine di alcuni punti in entrambe le direzioni»** (§7) è rimasto come affermazione da controllare: è l'unico punto del documento in cui una quantità viene descritta a parole invece che data. È R4.
6. **Il conteggio degli avvisi in §11** (53, e prima 54) è rimasto come l'unico numero che il lettore può controllare in tre secondi eseguendo il comando. È R2.

---

## Prova 2 — Verificabilità dei numeri

Il confronto è stato riscritto in proprio: risoluzione delle ancore contro l'unione dei due JSON, confronto del testo con il campo `display`, verifica di appartenenza per i letterali, ricalcolo delle identità aritmetiche, ricostruzione da zero dei conteggi per genere.

### Ciò che regge

- **99 ancore ben formate su 99 risolvono e coincidono.** Zero riferimenti inesistenti, zero divergenze di forma. Il confronto carattere per carattere con `display` funziona come dichiarato.
- **Tutte le identità aritmetiche interne tornano.** Il conto di §5 (1.002 + 22 + 6 = 1.030) è esatto; il blocco `denominators` contiene esattamente 421 voci, quante ne dichiara `CL.meta.profile_values.changed`; le quote ricalcolate dai valori ancorati restituiscono i display pubblicati alla cifra dichiarata.
- **Le liste hanno la lunghezza che il testo afferma**: 22 valori senza controparte, 6 fuori perimetro, 7 generi, 3 titoli riparati, e `netflix_rating_blanked_values` è vuota come richiede lo `0` di §5.
- **L'affermazione di §7 sull'insieme identico prima e dopo la trasformazione è vera.** Ricalcolando le quote sui due stati, l'insieme dei generi oltre il 50% è lo stesso: `country, iranian, jazz, latin, rock, romance, soul`.
- **I conteggi 78 e 48 di §5 si riproducono esattamente** con i due criteri che il documento descrive. Il difetto di quel passaggio non è nei numeri, è nella spiegazione (R5).
- **La corrispondenza di D2 regge sugli artefatti**: tre durate mancanti, tre classificazioni fuori dominio, tre titoli riparati e una regola che richiede entrambe le condizioni. L'affermazione «la corrispondenza è totale in entrambe le direzioni» è sostenuta dai valori pubblicati.

### Ciò che non regge

Tutto il dettaglio sta nei rilievi. In sintesi, rispetto alle quattro domande della prova:

- **valori non ancorati che avrebbero dovuto esserlo**: «un quinto», «la metà», «un decimo di punto», «un punto e mezzo» (R3); i margini della soglia scartata (R4); l'appartenenza dei tre titoli riparati a un unico artista (R6);
- **affermazioni derivate che nessun valore sostiene**: la comparazione di stabilità fra le due soglie in §7 (R4) — che viola la regola D5 enunciata dal documento stesso;
- **identità aritmetiche interne che non tornano**: nessuna. Tutte verificate, tutte esatte;
- **affermazioni marcate «non misurate» che sono fatti sui dati**: il 2021 della copertura video, che è `NF.num.release_year.max` nel profilo (R11); il conteggio degli avvisi di §11, che è l'output diretto del controllo ed è anche sbagliato (R2); e in forma minore i numerali in lettere che duplicano fatti già ancorati altrove (R7).

### Le garanzie di §2, verificate come enunciate

La prova chiedeva di verificare le garanzie **come enunciate**, non se siano vere in generale. Esito, garanzia per garanzia:

| Garanzia di §2 | Vera come enunciata? |
|---|---|
| «Ogni numero porta un marcatore **invisibile nel Markdown reso**» | **No.** In tre righe il marcatore è visibile: il lettore vede `.rows.after-->`, `.count-->`, `.pct-->` (R1) |
| «il controllo … **fallisce** se trova … un riferimento inesistente» | **Solo per riferimenti ben formati.** Un identificativo malformato non fa fallire nulla: viene declassato a «non misurato» in silenzio (R1) |
| «Ogni cifra e ogni numerale del documento» | **No.** Il controllo ha classi di esclusione non dichiarate e un vocabolario di numerali limitato a *zero–venti* (R3) |
| «Nessuna quantità può comparire senza che chi scrive abbia dichiarato se sia un valore misurato o no» | **No**, come sopra: quattro quantità in lettere compaiono senza alcun marcatore |
| «una dichiarazione falsa di non-misurato … contro questo esiste la revisione in contesto pulito» | **Vera, ed è servita**: R2 e R11 sono esattamente questo caso |

L'ultima riga merita una nota di merito. §2 dichiara in anticipo che il controllo non può intercettare una dichiarazione falsa di non-misurato e che l'unico presidio è la revisione in contesto pulito. Questa revisione ne ha trovate due. **La previsione del documento su di sé era corretta**, ed è un punto a suo favore: aveva indicato con precisione dove sarebbe stato debole.

---

## Prova 3 — Tenuta del perimetro

Il perimetro dichiarato in §10 è, nel complesso, **rispettato con disciplina non comune**. Il documento resiste a dire che cosa significhino i suoi numeri per il business, non anticipa la definizione di segmento, non tocca il segno della differenza di `BQ1-K2`, e in D5 arriva a rifiutare esplicitamente di portare la propria regola in `CLAUDE.md` perché «è atto di governance e non appartiene a questa feature». È il tipo di autolimitazione che un board nota.

I punti in cui il perimetro cede sono pochi e circoscritti.

**Giudizi travestiti da constatazioni.** §6 dice che «lo scarto fra le repliche discordi è **quasi sempre trascurabile**» e che la distorsione è «sistematica per costruzione **ancorché minima**». *Trascurabile* e *minima* sono valutazioni su una distribuzione, e la stessa sezione dichiara quattordici righe più sotto di aver **deliberatamente rinunciato a misurare la dispersione** per non introdurre una misura di posizione fuori perimetro. Il documento si vieta la misura e ne pubblica comunque la conclusione. È R9.

**Asimmetria di enfasi.** §7 argomenta la stabilità della soglia adottata dando i due margini in entrambe le direzioni, e liquida la soglia scartata riportando **solo** il lato che la penalizza. Il calcolo indipendente mostra che con il 60% un genere sarebbe rimasto fuori per 0,9091 punti *e* un altro sarebbe rimasto dentro per 1,0611: il documento cita il primo e tace il secondo. È R4, e la sua gravità sta nel fatto che l'omissione va tutta nella stessa direzione.

**Un'inferenza sulla fonte presentata come fatto.** §D2 afferma che i tre titoli sono «la **firma** di un errore di caricamento su un lotto omogeneo». È una conclusione sul processo editoriale di un terzo, non un'osservazione sui dati, ed è enunciata all'indicativo. Il documento la usa poi per sostenere l'ammissibilità della riparazione. La formulazione onesta esiste già poche righe dopo — «rende l'ipotesi … più solida della sola coincidenza numerica» — e andrebbe usata in entrambi i punti. Confluisce in R6.

**Numeri che sono esiti di analisi anziché descrizioni.** §5 presenta «421 valori non valgono più» e «78 generi su 114 cambiano» come descrizioni del dato trasformato. Il secondo è in buona parte l'esito del **modo in cui si è scelto di confrontare** due artefatti memorizzati a precisioni diverse (R5). Non è una descrizione: è un risultato di metodo, e va etichettato come tale.

**Prescrizioni ad altre feature.** D1 impone un obbligo alla feature 007 e a `BQ2-K1`; D3 chiude l'intercambiabilità delle grane per «ogni totale di catalogo musicale». Sono decisioni di questa feature, dichiarate come tali e coerenti con il suo mandato, e **non** vengono contate come sconfinamento — ma vale la pena registrarle: sono il punto in cui un documento di pulizia dati vincola il lavoro analitico a valle, e chi le riceve deve sapere che le sta ricevendo.

**Rilettura valutativa complessiva**: fuori dai punti sopra, gli aggettivi valutativi del documento sono quasi tutti riferiti a **decisioni di metodo** («difendibile», «irreversibile», «meccanico», «arbitrario») e non ai dati. È la distinzione giusta ed è tenuta con costanza.

---

## Rilievi

### R1 — Cinque ancore sono corrotte, il documento reso mostra testo rotto al posto dei numeri, e il controllo non se ne accorge

**Dove.** Righe 130, 201 e 202. Gli identificativi sono `CL.SP.zero<!--#-->.rows.after`, `SP.pop.zero<!--#-->.count`, `CL.SP.recalc.pop.zero<!--#-->.count`, `SP.pop.zero<!--#-->.pct`, `CL.SP.recalc.pop.zero<!--#-->.pct`. La causa è evidente: una sostituzione globale della parola *zero* con `zero<!--#-->` ha colpito anche le occorrenze di «zero» **dentro** gli identificativi delle ancore.

**Cosa non va.** Tre conseguenze distinte, in ordine di gravità crescente.

1. **Il documento reso è rotto.** Un commento HTML termina al primo `-->`. Il lettore che apre il Markdown su GitHub non vede un'ancora invisibile: vede

   | | riga | ciò che il lettore vede |
   |---|---|---|
   | §4, decisione 1 | 130 | `15.844.rows.after--> righe` |
   | §5, righe a popolarità zero | 201 | `16.020.count-->` e `15.844.count-->` |
   | §5, quota di righe a popolarità zero | 202 | `14,05%.pct-->` e `13,95%.pct-->` |

   Verificato simulando lo stripping dei commenti come lo esegue un parser reale (`<!--` fino al **primo** `-->`).

2. **Cinque valori hanno perso l'ancora in silenzio.** La grammatica del marcatore non ammette `<` nell'identificativo: il motore ripiega sull'alternativa e riconosce il `<!--#-->` interno come **marcatore di non-misurato**, con `display` uguale a `15.844<!--@CL.SP.zero`. I cinque numeri risultano quindi *dichiarati non misurati*. Fra questi c'è **15.844, il numero di testa di D1**, che nel corpo della sezione (riga 47) è invece correttamente ancorato: lo stesso valore è ancorato in un punto e dichiarato non misurato in un altro.

3. **Il controllo passa.** `ESITO: documenti e artefatti coerenti.` Il documento afferma in §2 che il controllo «fallisce se trova … un riferimento inesistente». Un riferimento *malformato* non è previsto da quella garanzia, e non fallisce: degrada. Il conteggio stesso lo mostra — il controllo dichiara 190 marcatori di cui 91 non misurati; le ancore realmente ben formate sono 99, e cinque delle 91 «dichiarazioni di non-misurato» sono ancore rotte che nessuno ha dichiarato.

**Perché conta.** Il documento chiede di essere creduto sulla base di un meccanismo: ogni numero è ancorato, un comando verifica, il comando fallisce se qualcosa non torna. Qui il meccanismo fallisce in silenzio, e fallisce **in modo visibile al lettore** — chi apre il documento vede `15.844.rows.after-->` prima ancora di aver deciso se fidarsi. Per un artefatto da portfolio è il difetto peggiore possibile: non mina un numero, mina la garanzia. E lo fa in una feature il cui contributo di metodo (D5) è proprio *rendere impossibile che un numero passi senza dichiarazione*.

**Correzione proposta.** Ripristinare i cinque identificativi (`CL.SP.zero.rows.after`, `SP.pop.zero.count`, `CL.SP.recalc.pop.zero.count`, `SP.pop.zero.pct`, `CL.SP.recalc.pop.zero.pct`) e — perché non si ripeta — far **fallire** il controllo su ogni sequenza `<!--` che compaia dentro il `display` catturato da un marcatore, oltre che su ogni `-->` residuo nel testo dopo l'estrazione. Sono due righe di guardia, e sono esattamente il caso che la grammatica attuale non copre.

---

### R2 — §11 pubblica un conteggio di avvisi che il comando del documento contraddice

**Dove.** §11, righe 305 e 307: «sono 53 le occorrenze oggi segnalate come avvisi» e «gli avvisi passano da 54 a 53, mentre marcatori ed esito restano invariati».

**Cosa non va.** Eseguendo `python3 scripts/check_audit_coherence.py` oggi, gli avvisi sul documento di audit sono **59**. Il conteggio è stato verificato in modo indipendente contando le righe di avviso emesse, non fidandosi dell'intestazione: 59. Il documento ne dichiara 53.

Entrambi i numeri — 53 e 54 — portano il marcatore di non-misurato. È coerente con la lettera di §2, che definisce quel marcatore come «il numero **non è un valore di questi artefatti**». Ma è precisamente il caso che §2 stessa indica come non presidiabile dal controllo, ed è anche il caso in cui la lettera della definizione tradisce il nome del marcatore: 53 non è un numero non misurato, è un numero **misurabile in tre secondi** da chiunque, che si dà il caso non stia nei due JSON.

**Perché conta.** È l'unico numero del documento che un lettore scettico può falsificare senza avere i dati di origine, senza token Kaggle e senza leggere nulla: gli basta eseguire il comando che il documento stesso gli mette davanti in §2. Se il primo numero che qualcuno prova a verificare è sbagliato, nessuna delle 99 ancore corrette recupera la fiducia persa. E il rilievo si aggrava per il contesto: la frase in cui il numero sbagliato compare è quella in cui la feature racconta di **aver corretto un difetto del controllo**.

**Correzione proposta.** Due strade, e vanno decise insieme (vedi divergenza 2). La minima: rigenerare i conteggi e riscriverli. La corretta: registrare l'esito del controllo — marcatori, avvisi, esito, per documento — come valori nel rendiconto, ancorarli, e sottrarre così alla prosa l'unica classe di numeri che si degrada da sola a ogni modifica dei documenti.

---

### R3 — La garanzia di copertura di §2 è più ampia di quella che il controllo offre, e le esclusioni non sono dichiarate

**Dove.** §2: «**Che cosa il controllo copre.** Ogni cifra e ogni numerale del documento. Nessuna quantità può comparire senza che chi scrive abbia dichiarato se sia un valore misurato o no».

**Cosa non va.** L'enunciato è falso in due modi, entrambi verificati in proprio.

*Primo: il controllo ha classi di esclusione che il documento non nomina.* Sono sigle strutturali (`BQ\d`, `FR-\d+`, `[RDFVA]\d+`, numeri di feature, date, versioni, **`ISO \d+`**), riferimenti di sezione, numerazione degli elenchi ordinati, codice in linea, bersagli dei link, intestazioni e blocchi di codice. Sono scelte tutte ragionevoli e tutte **motivate per iscritto dentro lo script**, che osserva giustamente che «una esclusione non scritta è una esclusione che nessuno può contestare». Il punto è che sono scritte **solo lì**. Il documento pubblicato afferma copertura totale. Effetto concreto: l'`8601` di «forma ISO 8601» (righe 137 e 238) non porta marcatore, e non lo porta perché è escluso — non perché sia stato dichiarato.

*Secondo: il vocabolario dei numerali si ferma a «venti».* Ne conseguono quattro quantità che compaiono nel documento **prive di qualunque marcatore** e invisibili al controllo:

| Riga | Testo | Perché è una quantità |
|---|---|---|
| 79, 85 | «sovrastima di circa **un quinto**» | è il 20%, ed è il fulcro dell'intera argomentazione aritmetica di D3 |
| 97 | «se più della **metà** delle righe di un genere vale zero» | è il 50%, ed **è la definizione della soglia di D4** |
| 228 | «Nessun genere sta a **un decimo di punto** dal confine» | è 0,1 punti percentuali |
| 230 | «un genere sarebbe rimasto fuori per meno di **un punto e mezzo**» | è 1,5 punti percentuali |

Le prime due sono difendibili come citazioni o come glosse di valori ancorati lì accanto. Le ultime due no: sono quantità nuove, portanti, e nessun valore le sostiene (vedi R4).

**Perché conta.** Un board non contesta che un controllo abbia esclusioni: le esclusioni sono normali e queste sono ben scelte. Contesta che siano state taciute mentre si dichiarava copertura totale. La differenza fra «copriamo tutto» e «copriamo tutto tranne queste sette classi, ed ecco perché» è la differenza fra un'affermazione che si può smontare in dieci minuti e una che regge.

**Correzione proposta.** Riscrivere il primo capoverso di «Che cosa il controllo copre» come: *«Ogni cifra e ogni numerale in lettere fino a venti che non appartenga a una delle classi strutturali escluse — sigle del framework, riferimenti di sezione, date, versioni, numerazione di elenchi, codice in linea e bersagli dei link — elencate in `scripts/check_audit_coherence.py`.»* E aggiungere alle esclusioni note del secondo capoverso una quinta voce: le quantità espresse con ordinali o frazioni in lettere (*un quinto*, *la metà*, *un decimo*, *un punto e mezzo*), che il vocabolario non riconosce e che vanno quindi presidiate a mano.

---

### R4 — L'argomento di sensibilità di §7 poggia su numeri che non esistono negli artefatti, e riporta un solo lato del confronto

**Dove.** §7, riga 230: «La soglia scartata del 60% sarebbe stata più esposta: con quella, un genere sarebbe rimasto fuori per meno di un punto e mezzo. Che la soglia scelta per una ragione risulti anche **la più stabile delle due** è una circostanza favorevole verificata a posteriori». E riga 228: «attorno alla soglia c'è un margine di **alcuni punti** in entrambe le direzioni».

**Cosa non va.** Tre problemi sovrapposti.

*Il confronto non è ancorato.* «Meno di un punto e mezzo» e «la più stabile delle due» sono un rapporto e un superlativo costruiti su fatti misurati. Nessun valore degli artefatti li sostiene: esistono `CL.SP.zero.high_genres.nearest_below` e `nearest_above` per la soglia **adottata**, e nulla per la soglia **scartata**. È letteralmente il caso che D5 vieta, con le parole di D5: *«un confronto … costruito su valori misurati è esso stesso un valore misurato. O esiste nell'artefatto con un identificativo proprio … o non si scrive»*, e il corollario (a): *«superlativi … e moltiplicatori riferiti a fatti misurati sono ammessi solo se ancorati a un valore che li sostiene»*. Il documento infrange la propria regola nella sezione immediatamente successiva a quella in cui la enuncia.

*Il confronto è riportato a un lato solo.* Ricalcolando le quote sul dato trasformato:

| Soglia | genere più vicino da sotto (escluso) | margine | genere più vicino da sopra (incluso) | margine |
|---|---|---:|---|---:|
| 50% (adottata) | `alternative` 48,4484% | 1,5516 | `rock` 52,50% | 2,50 |
| 60% (scartata) | `latin` 59,0909% | **0,9091** | `soul` 61,0611% | **1,0611** |

Il documento cita di questa tabella una sola cella: lo 0,9091 della soglia scartata. Tace che con il 60% un genere sarebbe stato **incluso** per appena 1,0611 punti — cioè che l'esposizione è simmetrica — mentre per la soglia adottata dà entrambi i lati. La conclusione «la più stabile delle due» resta **vera** (1,5516 > 0,9091), ma è dimostrata al lettore con metà dei dati, e la metà mancante è quella sfavorevole.

*«Alcuni punti» sovradichiara.* Il margine inferiore è **1,55** punti. «Alcuni punti» suggerisce al lettore italiano un'ampiezza maggiore. Ed è una quantità espressa a parole al posto di una sottrazione che si poteva scrivere.

**Perché conta.** §7 è la sezione che deve convincere che la soglia non è arbitraria, cioè il punto di massima esposizione della feature: D4 è l'unica decisione che introduce una stipulazione nei dati, ed è dichiarata a confidenza **media** in §9. Che proprio lì il documento chieda di essere creduto sulla parola, dopo aver scritto la regola che vieta di chiedere di essere creduti sulla parola, è il rilievo che un revisore ostile userebbe per primo.

**Correzione proposta.** Registrare nel rendiconto i due margini della soglia scartata (`CL.SP.zero.high_genres.nearest_below_60` e `nearest_above_60`), ancorarli, e riscrivere il capoverso dando **entrambi** i lati di entrambe le soglie — la conclusione regge lo stesso e regge meglio. Sostituire «un margine di alcuni punti» con i due valori: «un margine di 1,55 punti sotto e 2,50 sopra».

---

### R5 — §5 spiega il divario 78/48 con una causa che non è la causa reale

**Dove.** §5: «Il confronto avviene sul valore, non sulla forma con cui lo si scrive: dei 78 generi che cambiano, solo su 48 la differenza è visibile anche alla **seconda cifra decimale**. Sugli altri il valore si sposta **oltre**».

**Cosa non va.** I due conteggi sono esatti — riprodotti da zero: 78 e 48. La spiegazione no. Ricostruendo i valori:

- il **profilo** memorizza tutte e 114 le quote per genere con **una** cifra decimale (`jazz` = 68.1, `romance` = 63.6, `alternative` = 48.5);
- il **rendiconto** le memorizza con **fino a quattro** (`jazz` = 68.1682, `romance` = 61.3938, `alternative` = 48.4484).

Il «criterio stretto» confronta dunque numeri calcolati a precisioni diverse, e per costruzione li trova quasi sempre diversi. Verificato: **60 dei 78 generi «cambiati» tornano identici** una volta che il valore trasformato è arrotondato all'unica cifra decimale con cui il profilo lo aveva memorizzato. Solo **3 generi** si spostano di più di mezzo punto (`romance` −2,21; `classical` +1,14; `dance` −1,02).

La frase «sugli altri il valore si sposta oltre [la seconda cifra decimale]» descrive quindi un movimento nei dati che in gran parte **non c'è**: c'è un disallineamento di precisione fra due artefatti. E «visibile anche alla seconda cifra decimale» chiede al lettore di guardare una cifra decimale che il profilo non ha mai registrato.

Va detto che l'effetto non contamina in modo altrettanto grave il numero di testa della sezione: sui 421 valori del blocco `denominators`, quelli che tornano identici alla precisione con cui il profilo li aveva memorizzati sono **65**. Il 421 resta quindi in massima parte reale. È la famiglia per genere — quella che il documento sceglie di commentare per esteso — a essere dominata dall'artefatto di precisione.

**Perché conta.** §5 si apre dichiarandosi «la sezione che protegge dal citare un numero del profilo credendo che descriva il dato trasformato». È la sezione che si assume il compito di impedire un fraintendimento, e in un suo passaggio lo produce: chi legge esce credendo che 78 generi su 114 si siano mossi per effetto della deduplicazione, mentre i generi che si muovono in modo apprezzabile sono 3. Il documento poi mette in guardia — «chi confrontasse le tabelle stampate ne conterebbe 48» — ma indirizza l'avvertenza al lettore invece che alla causa.

**Correzione proposta.** Sostituire la spiegazione con quella vera, che è più interessante e non costa nulla: *«Il profilo memorizza queste quote con una sola cifra decimale, il rendiconto con quattro: il criterio stretto le trova quindi quasi sempre diverse. Dei 78 generi, 60 tornano identici una volta arrotondati alla precisione del profilo, e solo 3 si spostano di più di mezzo punto.»* Va inoltre deciso se il criterio stretto sia quello giusto da pubblicare (divergenza 1).

---

### R6 — L'argomento che regge D2 poggia su un fatto che nessun artefatto registra

**Dove.** §D2, riga 57: «Sono tre special di stand-up **dello stesso artista**. Non è un caso sparso: è la **firma** di un errore di caricamento su un lotto omogeneo, e rende l'ipotesi dello scivolamento di colonna più solida della sola coincidenza numerica».

**Cosa non va.** Che i tre titoli `s5542`, `s5795`, `s5814` siano special di stand-up e che appartengano a un unico artista **non è verificabile da nessun artefatto versionato**. Cercato: nessun catalogo del profilo o del rendiconto registra tipo, regista o interprete dei tre titoli; l'unica traccia è la lista degli identificativi. Chi non possiede `data/raw/` non ha modo di controllare, e chi lo possiede deve andarselo a cercare a mano.

È un'omissione più seria di un'ancora mancante qualsiasi, perché quella frase è **portante**. Il documento la usa esplicitamente per elevare la riparazione da coincidenza numerica a inferenza motivata, e §9 vi appoggia la riga a confidenza media («l'attribuzione al campo durata è un'inferenza — meccanica, verificabile e circoscritta»). Se la premessa dell'omogeneità del lotto non è verificabile, la parte dell'inferenza che va oltre l'aritmetica non lo è.

Si aggiunge il registro: «è la firma di un errore di caricamento» è una conclusione sul processo editoriale della fonte, enunciata all'indicativo come se fosse un'osservazione. La formulazione corretta il documento ce l'ha già, dodici parole dopo: «rende l'ipotesi … più solida».

Nota minore ma della stessa famiglia: «Sono **tre** special» porta il marcatore di non-misurato, mentre lo stesso 3 è ancorato due volte nella stessa sezione (`NF.duration.missing`, `CL.NF.duration.repaired.rows`).

**Perché conta.** D2 è la decisione più esposta della feature — l'unica in cui la pipeline scrive un valore dove la fonte non l'aveva messo. È anche quella meglio difesa: il vincolo sul raggio d'azione, la separazione delle due funzioni, la doppia corrispondenza. Tutta questa difesa converge su un unico fatto qualitativo che il lettore deve accettare senza poterlo controllare. È il punto debole di un argomento per il resto forte, ed è facile da chiudere.

**Correzione proposta.** Registrare nel rendiconto un catalogo dei titoli riparati con tipo e artista — tre righe di dati — e ancorare l'affermazione. In assenza, riscrivere: *«I tre titoli appartengono, nei dati di origine, a un lotto omogeneo per tipo e interprete: è compatibile con un errore di caricamento e rende l'ipotesi dello scivolamento più solida della sola coincidenza numerica.»* Ed espungere «è la firma di».

---

### R7 — §2 e D5 dettano due regole incompatibili sui numerali scritti in lettere

**Dove.** §2, seconda riga della tabella delle forme: «**numerale in lettere ancorato** | come sopra, per i numeri che in prosa si scrivono a parole» — cioè: un numerale in lettere può essere un fatto misurato, purché ancorato. §D5, corollario (b): «i numerali scritti in lettere sono **vietati per qualunque fatto misurato**».

**Cosa non va.** Le due regole non possono valere insieme. Il controllo implementa la prima (accetta i numerali in lettere ancorati e li confronta con `value`); il documento pratica la seconda, e il conteggio lo mostra: **0 marcatori in lettere** su 190. Una forma su quattro delle forme che §2 dichiara al lettore non viene mai usata.

Il costo non è teorico. Poiché la forma «ancorata in lettere» è di fatto abbandonata, ogni volta che il documento deve scrivere in prosa un fatto già ancorato altrove lo marca **non misurato**, il che è falso per definizione. Casi: «la riparazione di D2 svuota **tre** valori» e «i **tre** fuori dominio» (§5, righe 195-196), «normalizzarli produrrebbe **tre** tabelle senza lettore» (§4, riga 166 — dove lo stesso 3 è ancorato a `CL.NF.multivalue.fields_not_normalized` sulla stessa riga), «Sono **tre** special» (§D2). E «1 campo su **4**» (§4, riga 138), dove il 4 è la somma di due valori ancorati.

**Perché conta.** Il lettore che voglia usare questa notazione — ed è dichiaratamente proposta come regola generale del progetto — riceve due istruzioni opposte a quattro sezioni di distanza, e ne vede praticata solo una. Peggio: la pratica corrente produce, come effetto collaterale, una serie di dichiarazioni di non-misurato **materialmente false**, che è esattamente la categoria che §2 indica come non presidiabile dal controllo e affidata a questa revisione.

**Correzione proposta.** Decidere quale regola valga (divergenza 4). Se vince (b), rimuovere la seconda riga dalla tabella di §2 e dalla docstring dello script, e riscrivere in cifre ancorate le occorrenze elencate sopra. Se vince §2, usare la forma dove serve. In entrambi i casi un fatto misurato non deve mai portare il marcatore di non-misurato.

---

### R8 — «Cinque sono quelle ereditate» non si lascia far tornare con la tabella

**Dove.** §4, riga 126: «Nove decisioni sono applicate ai dati. Cinque sono quelle ereditate di §3; quattro sono emerse dalla ricognizione».

**Cosa non va.** Il lettore va alla tabella per verificare e trova che la colonna «Origine» delle prime cinque righe riporta D1, **D2, D2**, D3, D4. Cinque righe, ma **quattro** decisioni ereditate distinte: D2 ne occupa due, e **D5 non compare affatto**. La corrispondenza «cinque decisioni ereditate → cinque righe» che la frase promette non esiste.

La ragione è comprensibile a posteriori — D2 produce due operazioni distinte, che il documento tiene giustamente separate; D5 è una regola documentale e non un trattamento applicato ai dati — ma non è scritta da nessuna parte, e il titolo della sezione («Le nove decisioni **di trattamento**») rende l'assenza di D5 corretta e la frase che la precede sbagliata.

**Perché conta.** È il primo controllo che chiunque esegue: la sezione promette un'aritmetica (5 + 4 = 9) e la offre in una tabella che non la mostra. Costa trenta secondi e un'increspatura di fiducia, in una sezione che avrebbe dovuto costare zero.

**Correzione proposta.** *«Nove decisioni sono applicate ai dati. Cinque discendono dalle decisioni ereditate di §3 — D2 ne produce due, perché la riparazione e il controllo di dominio restano operazioni distinte, e D5 non compare qui perché è una regola sui documenti, non un trattamento dei dati; quattro sono emerse dalla ricognizione.»*

---

### R9 — §6 pubblica una valutazione della dispersione dopo aver dichiarato di non averla misurata

**Dove.** §6, riga 216: «Lo scarto fra le repliche discordi è **quasi sempre trascurabile** e ha una coda». Riga 218: distorsione «sistematica per costruzione **ancorché minima**». Riga 220: «**Perché non si è misurata la dispersione** … è esclusa per non introdurre in questo artefatto una misura di posizione che il perimetro della feature tiene fuori».

**Cosa non va.** *Trascurabile* e *minima* sono affermazioni sulla forma della distribuzione degli scarti. Il documento ne dispone di due sole osservazioni — 13 tracce oltre i dieci punti, massimo 44 — e dichiara quattro righe più sotto di aver rinunciato di proposito a misurare la dispersione. Le due cose non stanno insieme: o la dispersione non è misurata, e allora non se ne pubblica il giudizio; o il giudizio si pubblica, e allora poggia su una misura che va dichiarata.

I due dati disponibili, per inciso, la sostengono solo in parte: 13 tracce su 720 è l'1,8%, ed è un'informazione sulla **coda**, non sul centro. Nulla nel documento dice quanto valga lo scarto tipico.

**Perché conta.** §6 è la sezione che il documento costruisce per dichiarare una perdita invece di nasconderla, e lo fa con la frase giusta: «dichiararlo senza quantificarlo non sarebbe dichiararlo». Poi lo qualifica con due aggettivi non quantificati. È il tipo di scivolamento che un board coglie subito, perché entrambi gli aggettivi tirano nella direzione che conviene a chi scrive.

**Correzione proposta.** Espungere *trascurabile* e *minima*, e lasciar parlare i due valori ancorati: *«Lo scarto fra le repliche discordi ha una coda corta: 13 tracce su 720 superano i dieci punti, e il massimo osservato è 44. La dispersione non è misurata — sarebbe una misura di posizione, che il perimetro della feature tiene fuori — e non se ne pubblica quindi alcuna caratterizzazione.»* Onesto, e più forte.

---

### R10 — La numerazione delle sottosezioni di §4 collide con quella delle sezioni

**Dove.** §4 contiene le sottosezioni `### 6`, `### 7`, `### 8`, `### 9`, che sono i numeri di riga della tabella delle decisioni. Il documento ha anche le sezioni §5, §6, §7, §8, §9.

**Cosa non va.** Nella sottosezione **7** («La deduplicazione a traccia non è priva di perdita») si legge «Vedi **§6** del documento per la quantificazione», dove §6 è la sezione di primo livello «La perdita della deduplicazione». Nella stessa pagina convivono quindi un «7» che è una decisione e un «§7» che è una sezione sulla soglia dei generi, un «6» che è una decisione e un «§6» che è la sezione sulla perdita. D4 rimanda a «§7» intendendo la sezione. Il documento se ne accorge — da qui quel «del documento» aggiunto a mano — e vi rimedia con una glossa invece che con la numerazione.

**Perché conta.** Chi cita questo artefatto a valle citerà «§7» o «la 7» e produrrà riferimenti ambigui che nessuno potrà risolvere senza riaprire il file. È il difetto meno grave dell'elenco e il più economico da chiudere.

**Correzione proposta.** Rinominare le sottosezioni con il prefisso della decisione — `### Decisione 6 — …` — oppure numerarle `### 4.6`.

---

### R11 — La copertura temporale è dichiarata non misurata, ma il 2021 è un valore del profilo

**Dove.** §2, terzo trattino di «Che cosa il controllo non copre»: «La copertura temporale dei due cataloghi — 2021 e 2022 — è stabilita dalla constitution fra le fonti dati ammesse, **non è un valore di questi artefatti**, e porta il marcatore di non-misurato con la fonte citata in prosa». Ripreso in §10.

**Cosa non va.** Per il catalogo video l'affermazione è falsa: `NF.num.release_year.max` vale **2021** nel profilo della 002, ed è esattamente il fatto che la prosa asserisce. Un valore ancorabile esiste e non è stato ancorato, in un capoverso che serve a spiegare **perché** non lo si può ancorare. Per il catalogo musicale la ricerca non ha trovato alcun valore corrispondente al 2022: lì l'affermazione regge.

Le due metà della frase sono quindi asimmetriche, e la frase le tratta come una cosa sola.

**Perché conta.** È il caso di scuola che §2 dichiara di non poter presidiare — una dichiarazione di non-misurato apposta a un fatto che negli artefatti c'è. Che compaia proprio nell'esempio scelto per illustrare il confine della copertura lo rende più visibile, non meno: è il paragrafo che un lettore attento controlla per primo, perché è quello in cui il documento definisce i propri limiti.

**Correzione proposta.** Ancorare il 2021 a `NF.num.release_year.max` e riformulare il trattino distinguendo i due casi: *«Per il catalogo video l'anno di riferimento è anche un valore del profilo, ed è ancorato; per quello musicale non lo è, ed è stabilito dalla constitution fra le fonti dati ammesse.»* Se il 2021 della prosa intende una copertura diversa dall'anno massimo di produzione — per esempio la data di ultimo inserimento — la differenza va detta, perché il lettore non ha modo di indovinarla.

---

### R12 — Due righe usano accenti traslitterati in un documento che altrove non lo fa

**Dove.** Righe 47 e 71, entrambe capoversi «**L'effetto**»: «Nessuna riga **e'** rimossa per il valore di **popolarita'**: **e'** verificato come invariante»; «Nessuna riga **e'** eliminata».

**Cosa non va.** Sono le uniche due righe del documento con accenti resi come apostrofo ASCII. Ovunque altrove il testo usa `è`, `popolarità`, `perché` correttamente. La provenienza è trasparente — quelle due frasi vengono da stringhe di codice o di rendiconto, dove la traslitterazione è la convenzione — ma il documento è prosa destinata a un lettore esterno.

**Perché conta.** È il difetto meno grave del verbale e si segnala solo perché l'artefatto è destinato a un portfolio pubblico: due `e'` in mezzo a un testo altrimenti tipograficamente pulito sono la cosa che un lettore nota senza saper dire perché, e capitano nei capoversi «L'effetto», cioè quelli che il lettore frettoloso legge per primi.

**Correzione proposta.** `è`, `popolarità`.

---

### R13 — «Alla prima esecuzione ne ha fermati sei» non è verificabile e invita a una lettura sbagliata

**Dove.** §5, riga 187, subito dopo la tabella del conto dei valori del profilo: «Senza quell'invariante l'affermazione sarebbe vera soltanto per i valori che qualcuno si fosse ricordato di confrontare … Alla prima esecuzione ne ha fermati **sei**».

**Cosa non va.** È un'affermazione sulla storia di un'esecuzione passata della pipeline. Nessun artefatto la registra e nessuna riesecuzione può riprodurla: è vera o falsa senza che il lettore disponga di alcun mezzo per stabilirlo. Il marcatore di non-misurato è qui formalmente corretto, e proprio per questo mostra il limite del marcatore: dichiara «non è un valore di questi artefatti» dove il lettore avrebbe bisogno di leggere «non è verificabile».

Si aggiunge una collisione infelice: due righe più sopra la tabella riporta **6** valori «fuori perimetro». Un lettore in scorrimento lega naturalmente i due sei, che non hanno nulla a che vedere l'uno con l'altro.

**Perché conta.** L'aneddoto serve — dimostra che l'invariante non è decorativo — ma è collocato dove diventa indistinguibile dai numeri verificabili che lo circondano, in una sezione tutta costruita su un conto che torna.

**Correzione proposta.** O registrarlo (un contatore nel rendiconto), o marcarlo come aneddoto e allontanarlo dal 6 della tabella: *«Alla sua prima esecuzione l'invariante ha effettivamente fermato la pipeline su valori dimenticati; il conto attuale è quello della tabella.»*

---

## Divergenze da chiarire

Punti su cui va presa una decisione che questo documento non poteva prendere da solo. Sono formulati come domande perché la risposta richiede un contesto che una revisione in contesto pulito non ha.

**1. Quale precisione governa il confronto fra profilo e rendiconto.** Il profilo memorizza a una cifra decimale ciò che il rendiconto memorizza a quattro (R5). Il «criterio stretto» confronta i due numeri come sono, e produce 78 generi cambiati dove i generi realmente mossi in modo apprezzabile sono 3. Vanno decise due cose insieme: se il confronto debba avvenire alla **precisione minore fra le due** — con conseguente ricalcolo di 421 e di 78 — e se il profilo della 002 abbia un difetto di precisione da registrare come ritrovamento. La decisione cambia numeri pubblicati in §5 e nel blocco `denominators`, e non spetta a chi revisiona.

**2. Che cosa significa il marcatore di non-misurato.** Il nome dice «non misurato»; la definizione di §2 dice «non è un valore di questi artefatti». Sono cose diverse, e nello spazio fra le due cadono almeno tre casi trovati da questa revisione: il 2021 della copertura, che è un valore del profilo (R11); il 53 degli avvisi, che è l'output diretto e riproducibile del controllo (R2); il «sei» dell'invariante, che non è verificabile in alcun modo (R13). Vanno distinte due categorie — *non misurabile* e *misurato altrove* — o va estesa la nozione di artefatto per assorbire i numeri che il controllo stesso produce. La seconda strada chiuderebbe R2 alla radice.

**3. Se le esclusioni del controllo debbano essere pubblicate nel documento.** Oggi sono motivate con cura dentro lo script e taciute in §2, che dichiara copertura totale (R3). Poiché la copertura è ciò su cui il documento fonda la propria credibilità, chi ha il contesto deve decidere se pubblicare l'elenco delle esclusioni, se restringere l'enunciato, o entrambe le cose.

**4. Se valga il corollario (b) di D5 o la seconda forma di §2.** Sono incompatibili (R7). La scelta ha un costo asimmetrico: (b) è più severo e più semplice da rispettare, ma obbliga a scrivere in cifre numeri che in prosa italiana si scrivono a parole. La seconda forma è più elegante e non viene usata nemmeno una volta. Decidere significa anche decidere se rimuovere una forma dalla grammatica del controllo.

**5. Se il fatto che regge D2 debba diventare un dato.** L'omogeneità del lotto dei tre titoli è oggi un'affermazione qualitativa portante e non verificabile (R6). Registrarla nel rendiconto è economico, ma significa pubblicare attributi di titoli individuali — tipo e interprete — in un artefatto che finora contiene solo aggregati e identificativi. È una scelta sul perimetro degli artefatti, non sulla singola frase.

**6. Se la nota in loco su §5.2 del business case sia stata apposta.** D3 la dichiara «debito di questa feature». Il documento non dice se sia stata saldata, e verificarlo è fuori dal perimetro di questa revisione. Va accertato prima di considerare chiusa la feature: D3 è l'unica decisione che impone una modifica a un artefatto già mergiato.

**7. Se la chiave di lettura debba stare nel documento.** §2 rimanda a `specs/003-data-cleaning-etl/contracts/output-datasets.md` §3 per la definizione normativa delle quattro forme di marcatura. Un lettore esterno — che è il destinatario dichiarato di questo artefatto — non ha ragione di aprire una cartella di lavorazione, e §2 da sola non basta a ricostruire la grammatica (per esempio: che i numerali in lettere siano riconosciuti solo fino a *venti* non si evince da nessuna parte). Va deciso se la parte normativa vada trasferita nel documento o in `docs/`.

**8. Quanti avvisi produce oggi il controllo sul documento di audit, e perché il numero è cambiato.** §11 dichiara 53; il comando ne emette 59 (R2). Stabilire se il documento di audit sia stato modificato dopo la stesura, se il controllo sia cambiato, o se il conteggio fosse sbagliato in partenza richiede di aprire `docs/data_audit.md` e la storia del repository, entrambi fuori dal perimetro di questa revisione. Va accertato da chi ha quel contesto, perché la risposta decide se R2 sia un refuso o un difetto di processo.

---

## Nota di verifica della sessione revisionata — 2026-08-11

*Aggiunta in coda dalla sessione che ha scritto il documento revisionato. Il verbale sopra **non è stato modificato**: un revisore indipendente che venisse riscritto da chi ha revisionato smetterebbe di essere indipendente. Questa nota registra l'esito della verifica dei rilievi e le decisioni che alcuni hanno richiesto oltre la correzione.*

**Tutti e tredici i rilievi sono stati verificati e chiusi.** Nessuno è caduto: ogni fatto asserito dal verbale è risultato esatto, incluso il conteggio delle ancore ben formate e i due margini della soglia scartata, ricalcolati in modo indipendente.

**R1 è il rilievo che giustifica da solo la revisione.** La causa è stata confermata: una sostituzione automatica della parola *zero* con il marcatore di non-misurato aveva colpito anche le occorrenze dentro cinque identificativi. La correzione è duplice. Le cinque ancore sono state ripristinate; ma soprattutto il controllo ora **fallisce** su entrambi i sintomi — un'apertura di commento dentro il valore catturato, e una chiusura di commento rimasta nel testo dopo l'estrazione dei marcatori. Le due guardie sono state provate reintroducendo il difetto: lo intercettano. Il rilievo mostrava che il meccanismo falliva in silenzio proprio dove la sua garanzia contava, ed era vero.

**R5 ha corretto una spiegazione sbagliata con una diagnosi che si è rivelata ancora più netta di quella proposta.** Il verbale attribuiva il divario 78/48 a un disallineamento di precisione fra i due artefatti. È esatto, e la causa di quel disallineamento è strutturale: nel catalogo di origine ogni genere ha **esattamente 1.000 righe**, quindi la quota di zeri ha una sola cifra decimale per costruzione. Il documento ora lo dice, e pubblica i due valori che misurano quanta parte del divario sia apparente — 60 generi tornano identici alla precisione del profilo, 3 si spostano di oltre mezzo punto.

**Quattro rilievi hanno richiesto nuovi valori nel rendiconto**, perché la correzione non era riscrivere una frase ma renderla verificabile: i due margini della soglia scartata (R4), i due conteggi sulla precisione (R5), i nomi dei tre titoli riparati (R6). La regola D5 non ammetteva altra strada — un confronto o una graduatoria o hanno un identificativo o non si scrivono — e il verbale ha avuto ragione a contestare che il documento la violasse nella sezione immediatamente successiva a quella in cui la enuncia.

**R2 è stato chiuso rimuovendo il numero invece di aggiornarlo.** Il verbale offriva due strade e ne indicava una come corretta: registrare l'esito del controllo fra i valori. Non è percorribile senza circolarità, perché il rendiconto è prodotto dalla pipeline e il controllo legge il rendiconto. Il documento non pubblica più alcun conteggio di avvisi e rimanda al comando, spiegando perché: un numero che si degrada a ogni modifica dei documenti non va messo in prosa. La causa del divario 53/59 è accertata ed è la divergenza 8 del verbale: le note di adozione che questa stessa feature ha aggiunto al documento di audit hanno introdotto altri avvisi.

**Le divergenze 6 e 8 sono chiuse.** La nota in loco su §5.2 del business case **è stata apposta**, e il documento ora lo dichiara invece di annunciare un debito. Il diff verso `main` dei due artefatti mergiati contiene solo righe aggiunte: zero rimosse, zero modificate.

**Un rilievo del verbale vale oltre questa feature.** L'osservazione di R7 — che §2 e il corollario (b) di D5 dettavano due regole incompatibili sui numerali in lettere, e che la pratica corrente produceva dichiarazioni di non-misurato materialmente false — tocca la regola che la feature propone al progetto intero. La riconciliazione adottata è dichiarata in §2: il controllo accetta la forma perché la usa il documento della 002, questo documento non la usa perché segue la regola più severa. Chi porterà D5 in `CLAUDE.md` deve portarci anche questa precisazione.

**Sulle tre uscite dal perimetro registrate dal revisore.** Sono legittime e tutte e tre utili. La lettura dello script di controllo, in particolare, non era prevista e si è resa necessaria perché il documento delegava la propria chiave di lettura a un file di lavorazione: è la divergenza 7, e resta aperta per la regia.
