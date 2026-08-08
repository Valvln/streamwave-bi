# Research — Feature 002: Data Audit & Profiling

**Data**: 2026-08-08 | **Fase**: 0 (Outline & Research) | **Spec**: [spec.md](./spec.md)

La Fase 0 ha eseguito una ricognizione in sola lettura sui due file di `data/raw/` per fondare le decisioni tecniche su ciò che i dati sono davvero, e non su ciò che la 001 riporta. La ricognizione **non è il profiling**: non ha prodotto artefatti persistenti e i suoi numeri non entrano in nessun documento. Serve a sapere quali problemi lo script dovrà saper gestire prima di scriverlo.

## Ritrovamenti

### F1 — R11 ha una risposta, ed è quella che la roadmap anticipava

Il catalogo video espone **una sola** categoria a contenuto musicale dichiarato: `Music & Musicals`, su 42 categorie distinte. Nessun'altra etichetta contiene un riferimento a musica, concerti o canto.

**Conseguenza**: `BQ1-K1` non compie alcuna selezione fra categorie, quindi non c'è mappatura interpretativa e la **confidenza alta della North Star regge**. Il ritrovamento va comunque prodotto dallo script e non asserito: finché il numero non esce da un artefatto versionato, il principio II non è soddisfatto. La feature registra l'esito; il disallineamento testuale di §3 del business case resta debito testuale (FR-032).

### F2 — "Sovrastima di circa un quinto" è ambiguo, e le due letture danno numeri diversi

`business_case.md` §5.2 afferma che un totale di catalogo calcolato senza deduplicare "sovrastima di circa un quinto". La frase ammette due letture aritmetiche:

| Lettura | Formula | Valore |
|---|---|---|
| quota di righe che sono ripetizioni | (righe − identificativi distinti) / righe | ≈ 21% |
| di quanto il totale non deduplicato eccede quello corretto | (righe − distinti) / distinti | ≈ 27% |

"Un quinto" è corretto sotto la prima lettura e sbagliato sotto la seconda, che è però quella che la parola "sovrastima" suggerisce più naturalmente: si sovrastima **rispetto al valore giusto**, cioè rispetto al denominatore deduplicato.

**Conseguenza**: l'artefatto espone **entrambe** le quantità con identificativi distinti, e il documento di audit dichiara quale delle due §5.2 intendeva. È il primo candidato divergenza di FR-030, e mostra perché la feature serve: la prosa non era falsa, era sotto-determinata.

### F3 — Il conteggio delle corrispondenze lessicali dipende interamente dalla regola di confronto

`research.md` della 001 (R4) dichiara 6 generi musicali con corrispondenza lessicale nelle categorie video: `anime`, `british`, `children`, `comedy`, `kids`, `spanish`. Una regola di confronto per token esatti sulle etichette ne trova **4**: `kids` e `spanish` non emergono perché vivono dentro `Kids' TV` e `Spanish-Language TV Shows`, dove l'apostrofo e il trattino spezzano il token.

**Conseguenza**: il valore non esiste senza la sua regola. FR-022 lo prevede già; la Fase 0 conferma che non è una formalità. L'artefatto dichiara la regola applicata, e se sotto quella regola il conteggio non è 6, è una divergenza da registrare — non un numero da forzare finché non torna.

### F4 — Il catalogo video contiene tre valori in un campo sbagliato

Il campo della classificazione per età contiene 18 valori distinti, ma tre di essi sono durate (`74 min`, `84 min`, `66 min`), una per riga: un evidente scivolamento di campo nella fonte. I valori di classificazione legittimi sono 14, più il valore vuoto.

**Conseguenza**: "18 valori" è vero come cardinalità osservata e fuorviante come descrizione del dominio. Il profilo riporta la cardinalità grezza **e** i valori fuori dominio, separatamente. È il caso che dà sostanza al limite dichiarato "completezza non è correttezza": quei tre campi sono valorizzati al 100% e sbagliati.

### F5 — La 001 profilava 9 campi su 12, e il catalogo musicale ha una colonna senza nome

Il catalogo video ha **12** campi; `research.md` della 001 ne documentava 9 (mancano l'identificativo, il titolo e il cast — quest'ultimo con 825 valori mancanti, il secondo campo più incompleto dopo il regista). Il catalogo musicale espone **21** campi, il primo dei quali è **privo di nome**: è l'indice di riga della fonte, sopravvissuto all'esportazione.

**Conseguenza**: FR-019 (nessun campo escluso in silenzio) rende il profilo di questa feature più ampio di ciò che rigenera. La colonna senza nome va profilata e dichiarata per quello che è, non ignorata perché scomoda.

### F6 — Esistono valori degeneri oltre a quelli che la 001 cita

Oltre alla massa di zeri nell'indice di popolarità, già nota, la ricognizione ha trovato una traccia con durata dichiarata pari a zero e tre titoli video privi di durata. Sono pochi, e proprio per questo sparirebbero senza un profilo che li conta.

## Decisioni

### D1 — Solo libreria standard: niente pandas, niente ambiente virtuale

**Decisione**: lo script usa esclusivamente la libreria standard di Python (`csv`, `statistics`, `hashlib`, `json`). Nessuna dipendenza esterna, nessun `requirements.txt`, nessun ambiente virtuale introdotto da questa feature.

**Rationale**: tre ragioni convergenti.

1. **Riproducibilità (principio II)**: la promessa "chiunque cloni il repository può rigenerare" vale davvero solo se non c'è nulla da installare. Con la sola libreria standard, `python3 scripts/profile_data.py` funziona ovunque esista Python 3.
2. **Determinismo (FR-003)**: pandas cambia rappresentazione e comportamento dei float fra versioni minori, e `describe()` non garantisce stabilità di formato nel tempo. Con `statistics` e una regola di arrotondamento dichiarata, il determinismo è dimostrabile invece che sperato.
3. **Scala**: 8.807 e 114.000 righe. Non c'è alcun problema che una libreria di dataframe risolverebbe.

**Alternative scartate**: pandas più `requirements.txt` — introduce un chore di ambiente dentro una feature da 4 ore e un rischio di determinismo, per un vantaggio nullo a questa scala; `polars` — stesso costo, stesso rischio, meno diffuso.

**Nota per la 003**: questa decisione non vincola le feature successive. L'ETL della 003 lavorerà su join e trasformazioni, dove un dataframe si ripaga; quello sarà il momento di introdurre la dipendenza e l'ambiente, con la sua chore dichiarata.

### D2 — L'artefatto è un unico file JSON sotto `reports/`

**Decisione**: `reports/data_profile.json`, un solo file.

**Rationale**: JSON è leggibile da macchina senza dipendenze, leggibile da persona quando serve, e diffabile riga per riga in una pull request — che è ciò che rende visibile il cambiamento di un numero fra due esecuzioni. `reports/` è l'unica cartella che `.gitignore` lascia libera (salvo le figure PNG), verificato meccanicamente con `git check-ignore`. Un solo file perché l'artefatto è dichiarato "unica fonte di verità" (FR-006): spezzarlo in più file crea la domanda "quale dei due vale" che la feature esiste per eliminare.

**Alternative scartate**: CSV — intercettato dal blanket di `.gitignore` e incapace di rappresentare una struttura annidata; YAML — richiederebbe una dipendenza per essere riletto dal controllo di coerenza; un file per dataset — moltiplica le fonti di verità.

### D3 — Ogni valore porta con sé la propria forma di visualizzazione

**Decisione**: ogni valore dell'artefatto è un record che contiene sia il valore numerico grezzo sia una stringa `display` già formattata secondo le convenzioni italiane del progetto (separatore di migliaia `.`, decimale `,`, unità dove pertinente). Il documento di audit scrive **esattamente** la stringa `display`.

**Rationale**: è la decisione che rende banale il controllo di coerenza. Confrontare due stringhe identiche non richiede di interpretare la formattazione italiana dei numeri, di sapere se `14,1` vada confrontato con `0,141` o con `14,1`, o di indovinare quanti decimali l'autore ha usato. La formattazione vive in un solo posto — lo script — ed è quindi automaticamente uniforme in tutto il documento.

Se serve una seconda forma dello stesso numero (la quota come percentuale e come frazione), è un secondo valore con un proprio identificativo, non una riformulazione a mano.

**Alternative scartate**: confronto numerico con normalizzazione della locale — richiede un parser di numeri italiani nel controllo, cioè esattamente la fragilità che FR-025 vieta; tolleranza numerica configurabile — introduce la domanda "quanto scarto è accettabile" in una feature il cui punto è che non ce ne sia.

### D4 — La marcatura è un commento HTML subito dopo il valore

**Decisione**: la sintassi è `valore<!--@ID-->`, con il commento immediatamente adiacente al valore, senza spazio. Esempio: `8.807<!--@NF.shape.rows-->`.

**Rationale**: un commento HTML è invisibile in qualunque lettore Markdown, quindi il documento resta leggibile senza strumenti (FR-023) e senza rumore visivo; è al tempo stesso un delimitatore non ambiguo per una macchina. L'adiacenza risolve il problema di FR-025: il controllo non cerca "tutti i numeri del documento", cerca il testo che precede immediatamente un marcatore noto. Non ci sono falsi positivi su date, numeri di sezione o sigle, perché nulla di ciò che non è marcato viene mai letto.

**Alternative scartate**: documento generato da template — garantirebbe la coerenza per costruzione, ma renderebbe il deliverable un artefatto generato, mentre la spec chiede un documento scritto per essere letto; inoltre creerebbe due file dove uno solo è quello giusto da modificare, che è un footgun peggiore del problema risolto. Sintassi di attributo `{#id}` — non è Markdown standard e comparirebbe come testo in molti lettori.

### D5 — Regole di determinismo, dichiarate ed esplicite

**Decisione**: il determinismo di FR-003 è garantito da quattro regole vincolanti per lo script:

1. **Nessun timestamp di esecuzione** nell'artefatto. La provenienza è data dall'impronta dei file di origine (FR-005), non dall'ora in cui si è premuto invio.
2. **Ordinamento stabile ed esplicito** di ogni collezione: chiavi ordinate alfabeticamente in serializzazione, elenchi di categorie e generi ordinati per un criterio dichiarato e senza pareggi ambigui.
3. **Arrotondamento dichiarato**: ogni valore non intero è arrotondato a un numero fisso di decimali prima della serializzazione, così che nessuna differenza di rappresentazione in virgola mobile possa affiorare nel file.
4. **Nessun campionamento, nessun ordine di iterazione dipendente dall'ambiente**.

**Rationale**: il determinismo non è una proprietà che si ottiene per caso; è la somma di quattro decisioni ognuna delle quali, se omessa, lo rompe in silenzio. Dichiararle qui le rende verificabili in fase di revisione del codice, invece che solo osservabili eseguendo due volte.

### D6 — Le affermazioni della 001 sono codificate e confrontate automaticamente

**Decisione**: i valori che la 001 cita in prosa sono codificati come tabella di riferimento versionata insieme allo script, ciascuno con l'indicazione di dove compare. Lo script confronta ogni valore rigenerato con l'affermazione corrispondente ed emette nell'artefatto un blocco di divergenze.

**Rationale**: FR-030 impone di registrare ogni divergenza. Farlo a occhio su una quarantina di numeri sparsi fra due documenti è il modo tipico in cui una divergenza sfugge — ed è proprio ciò che questa feature esiste per impedire. Un confronto automatico rende il ritrovamento un output dello script anziché un atto di attenzione. F2 e F3 sono già due candidati noti.

**Alternative scartate**: confronto manuale in fase di scrittura del documento — non riproducibile e non rieseguibile quando i dati di origine venissero riscaricati; file di riferimento separato sotto `specs/` — uno script che legge la propria configurazione dalla cartella di una spec confonde due piani che il repository tiene distinti.

### D7 — Questa feature produce `contracts/`, a differenza della 001

**Decisione**: viene prodotto `contracts/profile-artifact.md`, che fissa la forma del record di valore, la convenzione di denominazione degli identificativi e la grammatica della marcatura.

**Rationale**: la 001 rifiutò `contracts/` (sua decisione D6) perché il contratto *era* il documento, e duplicarne lo schema avrebbe creato due definizioni destinate a divergere. Qui la situazione è rovesciata su due punti. Primo, il consumatore del contratto è **una persona che scrive marcatori a mano** nel documento di audit: ha bisogno di un posto dove guardare che non sia il codice sorgente dello script. Secondo, la divergenza fra contratto e implementazione non è affidata all'attenzione, perché il controllo di coerenza fallisce se la grammatica non è rispettata — la garanzia meccanica che alla 001 mancava. Il contratto serve anche alle feature successive, che citeranno identificativi di questo artefatto senza volerne riaprire lo script.

### D8 — Il divieto di valori non marcati è presidiato da un avviso, non da un errore

**Decisione**: il controllo di coerenza fallisce (stato di errore) su due condizioni: un valore marcato che non coincide con l'artefatto, e un riferimento non risolvibile. Emette invece un **avviso non bloccante** per i gruppi di cifre presenti nel documento e non adiacenti ad alcun marcatore, come lista da vagliare a occhio.

**Rationale**: SC-005 chiede che nessun valore del profilo compaia non marcato. La direzione inversa — riconoscere che un numero *sarebbe dovuto* essere marcato — richiederebbe di distinguere in prosa italiana un valore di profilo da una data, da un riferimento a una sezione o da un numero di rilievo. È esattamente l'estrazione euristica che FR-025 vieta, e trasformarla in un gate produrrebbe fallimenti falsi che porterebbero a disattivare il controllo. L'avviso dà alla revisione l'elenco su cui guardare senza pretendere di decidere al posto suo.

**Onestà sul limite**: SC-005 resta quindi verificato da una lettura assistita, non da un comando. È dichiarato qui e ripreso in [quickstart.md](./quickstart.md); non è un requisito eluso, è un requisito il cui controllo automatico completo costerebbe più della feature intera.

### D9 — Convenzioni di profilazione, fissate una volta

**Decisione**: quattro convenzioni valgono per tutto il profilo e sono dichiarate nell'artefatto stesso.

| Convenzione | Regola |
|---|---|
| **valore mancante** | campo assente, stringa vuota o composta di soli spazi. Non si inferiscono segnaposto (`N/A`, `unknown`): se ne esistono, sono riportati come valori osservati e segnalati fra i valori fuori dominio |
| **cardinalità alta** | oltre una soglia dichiarata di valori distinti, si riportano cardinalità e valori più frequenti anziché l'enumerazione completa. Le categorie del catalogo video sono esenti: lì l'enumerazione completa è il punto (FR-021) |
| **campo multi-valore** | l'elenco di categorie di un titolo video è profilato sia come stringa intera sia come insieme di etichette atomiche, con conteggi distinti e granularità dichiarata (FR-018) |
| **dispersione** | scarto interquartile e deviazione standard campionaria, entrambi riportati: il primo perché robusto agli zeri di popolarità, la seconda perché è ciò che il lettore si aspetta |

**Rationale**: sono le quattro scelte che, lasciate implicite, rendono due profili non confrontabili pur essendo entrambi "corretti". Dichiararle nell'artefatto le rende parte del dato, non del codice.

## Nota di impatto sulla spec

Nessuna. Le decisioni di Fase 0 stanno tutte dentro il perimetro dei requisiti approvati; F2 e F3 anticipano divergenze che FR-030 già prevede, e F4 e F5 allargano il profilo entro quanto FR-019 già imponeva. La spec non va modificata.
