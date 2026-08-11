# Research — Feature 003: Data Cleaning & ETL

**Data**: 2026-08-11 | **Fase**: 0 (Outline & Research) | **Spec**: [spec.md](./spec.md)

La Fase 0 ha eseguito una ricognizione in sola lettura sui due file di `data/raw/` per fondare le decisioni tecniche su ciò che i dati sono, e non su ciò che il profilo riporta. La ricognizione **non è la trasformazione**: non ha prodotto artefatti persistenti, non ha scritto sotto `data/`, e nessuno dei suoi numeri entra in un documento pubblicato. Serve a sapere quali problemi la pipeline dovrà gestire prima di scriverla.

**Nota sulle sigle.** La spec usa `D1`-`D5` per le cinque **decisioni ereditate** dalle revisioni della 001 e della 002. Questo documento usa `F1`-`F8` per i **ritrovamenti** e `T1`-`T11` per le **decisioni tecniche**, per evitare la collisione.

## Ritrovamenti

### F1 — D2 regge sui dati: le tre righe senza durata sono le tre con classificazione fuori dominio

La spec lo aveva anticipato sulla base di una verifica preliminare; la ricognizione lo conferma per intero. I titoli privi di durata sono `s5542`, `s5795`, `s5814`. I titoli con classificazione per età fuori da `conventions.rating_domain` sono gli stessi tre, con valori `'74 min'`, `'84 min'`, `'66 min'`. La corrispondenza è totale in entrambe le direzioni: non esiste una riga senza durata che abbia una classificazione valida, né una riga con classificazione fuori dominio che abbia una durata.

**Conseguenza**: la regola di riparazione di D2 ha un raggio d'azione dichiarabile in anticipo — esattamente tre righe — ed è verificabile come invariante di esecuzione (T10). È ciò che la spec chiedeva per renderla difendibile.

### F2 — La grana coppia traccia-genere **non è unica** nella fonte

Ritrovamento nuovo: né la 001 né la 002 lo registrano. Il profilo stabilisce che la riga non è la traccia (`SP.id.distinct` = 89.741 su `SP.shape.rows` = 114.000) e ne conclude che esistono due granularità. La seconda di quelle due, però, non è unica nemmeno lei: **444 coppie traccia-genere compaiono più di una volta**, per **450 righe eccedenti**. Trentotto coppie compaiono due volte, sei tre volte.

Il fatto che rende la cosa gestibile: **le repliche di una stessa coppia sono identiche su tutti gli attributi**, indice di riga escluso. Nessun attributo discorda su nessuna delle 444 coppie.

**Conseguenza**: FR-011 chiede che ogni output verifichi la propria grana come invariante. Sulla grana coppia l'invariante **fallirebbe** se la pipeline si limitasse a trasportare le righe. La deduplicazione di coppia è quindi obbligatoria, ed essendo priva di perdita è anche innocua: rimuove righe interamente ridondanti, non informazione. Va comunque dichiarata e quantificata come qualunque altra decisione (FR-029), perché cambia il numero di righe rispetto a `SP.shape.rows`.

### F3 — La deduplicazione a traccia **non** è priva di perdita, e la perdita è su un solo attributo

Sulle 89.741 tracce distinte, **720 hanno repliche che discordano** — e discordano **solo** su `popularity`. Ogni altro attributo, incluse tutte le audio feature, coincide fra le repliche di una stessa traccia.

La dispersione è quasi sempre trascurabile e ha una coda: lo scarto fra valore massimo e minimo ha mediana 1 punto, media 1,71, massimo 44; tredici tracce superano i 10 punti di scarto.

**Conseguenza**: FR-018 chiede una regola deterministica che conservi un valore osservato. La scelta esiste ed è materiale solo per 720 tracce su 89.741; l'entità dell'effetto va comunque quantificata nel documento (FR-019), non solo la regola. Vedi T5.

### F4 — Il criterio di D4 è **robusto** alla trasformazione, ma le quote per genere cambiano

Due fatti da tenere separati, perché uno rassicura e l'altro obbliga.

Le quote di righe a popolarità zero per genere **cambiano su 48 dei 114 generi** dopo la deduplicazione di coppia di F2 — di poco, ma cambiano: `romance` passa da 63,60% a 61,39%, `latin` da 58,80% a 59,09%, `classical` da 39,80% a 40,94%. Sono i denominatori che si spostano, ed è il caso previsto da FR-030.

L'insieme selezionato dal criterio di D4 — quota superiore al 50% — è invece **identico prima e dopo**: `country`, `iranian`, `jazz`, `latin`, `rock`, `romance`, `soul`. Sette generi.

**Conseguenza sulla sensibilità della soglia**, che D4 obbliga a dichiarare: sul dataset trasformato il genere più vicino da sotto è `alternative` a 48,45%, cioè **1,55 punti** sotto la soglia; il più vicino da sopra è `rock` a 52,50%. Nessun genere è a un decimo di punto. Vale la pena registrare il confronto: la soglia scartata del 60% sarebbe stata **più** knife-edge, con `latin` a 59,09% e `country` poco sotto. La soglia scelta per una ragione risulta anche la più stabile delle due, il che è un argomento a posteriori e va presentato come tale, non come la ragione della scelta.

### F5 — La separazione delle due durate video è un'invariante, non un'euristica

Il campo `duration` del catalogo video ha esattamente due forme: `N min` su 6.128 righe, tutte di tipo `Movie`; `N Season` o `N Seasons` su 2.676 righe, tutte di tipo `TV Show`. Le tre righe rimanenti sono quelle di F1. Nessun film porta stagioni, nessuna serie porta minuti, nessuna forma terza esiste.

**Conseguenza**: FR-014 può essere realizzato come una verifica invece che come un tentativo. La pipeline afferma la corrispondenza fra tipo e unità e si ferma se non la trova (T10), invece di dedurre l'unità dalla stringa e sperare.

### F6 — `date_added` è una trappola di determinismo

Il campo contiene date in forma testuale inglese (`September 25, 2021`), con **88 valori che portano uno spazio iniziale**. I mesi distinti sono dodici, tutti in inglese. Dieci valori sono vuoti.

Il problema non è la normalizzazione dello spazio, che è banale. È che `datetime.strptime(valore, "%B %d, %Y")` **dipende dal locale del sistema**: funziona sotto locale C o inglese e fallisce sotto locale italiano. Una pipeline che lo usasse produrrebbe risultati diversi su macchine diverse, cioè violerebbe FR-003 in un modo che non si manifesta sulla macchina di chi la scrive.

**Conseguenza**: la conversione usa una **tabella dei mesi esplicita** nel codice. Vedi T6. È il tipo di dipendenza dall'ambiente che FR-001 vieta e che nessun test locale avrebbe scoperto.

### F7 — I campi multi-valore del catalogo video sono quattro, non uno

`listed_in` è multi-valore (42 categorie distinte, 19.323 assegnazioni, separatore virgola, nessuna categoria contiene una virgola interna: la separazione è meccanica e sicura). Ma lo sono anche `country` — 1.320 righe ne contengono più di uno — e, di fatto, `cast` e `director`.

FR-012 impone la normalizzazione del solo campo delle categorie. La ricognizione conferma che è la scelta giusta e la ragione va scritta: nessuna misura del framework 001 consuma `country`, `cast` o `director`, mentre `BQ1-K1` conta titoli per categoria ed è il caso in cui un totale ingenuo sbaglia. Normalizzare gli altri tre produrrebbe tre tabelle che nessuno legge. Vedi T7.

### F8 — Anomalie minori, tutte da contare e nessuna da correggere

- La prima colonna del catalogo musicale **non ha nome** ed è l'indice di riga `0`…`113999`, in ordine e senza salti. È un artefatto dell'esportazione della fonte, non un dato.
- Una riga del catalogo musicale ha `artists`, `album_name` e `track_name` vuoti: una traccia senza nome né autore.
- Una riga ha `duration_ms` pari a zero (`SP.duration.zero`).
- I campi `key`, `mode` e `time_signature` hanno domini piccoli e chiusi; `time_signature` include il valore `0`, che non è una metrica musicale valida.
- Il catalogo video ha due campi con un a capo incorporato nel testo, e migliaia di campi contenenti virgole: la scrittura CSV deve quotare correttamente, ed è l'unica ragione per cui non si può scrivere l'output concatenando stringhe.

**Conseguenza**: nessuno di questi casi giustifica un'eliminazione. Vengono contati e, dove pertinente, marcati (FR-023). L'indice senza nome è l'unica colonna che esce dagli output, ed esce dichiarata (FR-010, T11).

---

## Decisioni tecniche

### T1 — Sola libreria standard, output in CSV

**Decisione**: nessuna dipendenza esterna. `csv`, `json`, `hashlib`, `re` e nient'altro. Gli output di dati sono file CSV sotto `data/processed/`.

**Ragione**: è la stessa scelta della 002 (sua decisione D1) e vale qui per gli stessi motivi, più uno nuovo. I motivi vecchi: a 8.807 e 114.000 righe nulla richiede un dataframe, e la promessa «clona ed esegui» vale solo se non c'è nulla da installare. Il motivo nuovo è FR-003: il determinismo byte per byte di un CSV scritto con il modulo standard è dimostrabile riga per riga, mentre quello di un file Parquet dipende da versione della libreria, schema di compressione e metadati interni — cioè da cose che cambiano fra due macchine senza che nessuno lo decida.

**Alternative scartate**: pandas + Parquet, che sarebbe la scelta ovvia in un contesto ordinario e che qui costerebbe un ambiente da ricostruire e un determinismo sperato invece che verificato. Il blanket di `.gitignore` intercetta comunque sia `*.csv` sia `*.parquet`, quindi il formato non cambia nulla sul fronte della versionatura.

### T2 — I valori non trasformati viaggiano **verbatim**; i tipi sono dichiarati e validati

**Decisione**: un valore che nessuna decisione di trattamento tocca viene scritto nell'output esattamente com'era nella sorgente, senza passare per una conversione numerica e ritorno. I tipi di ogni campo sono dichiarati in [contracts/output-datasets.md](./contracts/output-datasets.md) e **validati** dalla pipeline, che si ferma se un valore non rispetta il tipo dichiarato.

**Ragione**: soddisfa FR-009 senza introdurre il rischio che lo renderebbe illusorio. Convertire `0.0594` in `float` e riscriverlo significa affidarsi alla rappresentazione testuale dei decimali, che è la sorgente classica di differenze fra esecuzioni e fra versioni. Trasportare la stringa elimina la classe di problema per intero. In un CSV il tipo non vive comunque nel file: vive in un contratto, e ciò che rende quel contratto vero è la validazione, non la riscrittura.

**Alternative scartate**: normalizzare tutti i numerici a una precisione fissa. Cambierebbe valori che nessuna decisione di trattamento ha deciso di cambiare, cioè produrrebbe una trasformazione non dichiarata — esattamente ciò che FR-029 vieta.

### T3 — Ordinamento degli output: ordine di sorgente, prima occorrenza

**Decisione**: ogni output conserva l'ordine in cui le righe compaiono nella sorgente. Dove una deduplicazione rimuove righe, sopravvive la **prima occorrenza**. Nella tabella titolo-categoria le categorie di un titolo compaiono nell'ordine in cui il campo le elenca.

**Ragione**: è l'ordinamento che non richiede una chiave di ordinamento e quindi non ne richiede la giustificazione. Ordinare per `show_id` darebbe `s1, s10, s100` — lessicograficamente corretto e visivamente sbagliato; ordinare per titolo introdurrebbe una dipendenza dalle regole di collazione, che è di nuovo una dipendenza dal locale (F6). L'ordine di sorgente è deterministico, ricostruibile e non scarta nulla.

### T4 — Scrittura CSV con parametri espliciti

**Decisione**: `lineterminator='\n'`, quoting minimale, codifica UTF-8 senza BOM, nessuna riga finale vuota. Intestazione presente in ogni file.

**Ragione**: i valori di default del modulo `csv` includono `\r\n` come terminatore, che produrrebbe file diversi da quelli attesi e diff rumorosi. Sono i tre o quattro parametri che decidono se FR-003 è vero, e vanno scritti invece che ereditati.

### T5 — Regola di scelta della popolarità nelle repliche discordi: il **massimo**

**Decisione**: dove le repliche di una traccia discordano su `popularity` (F3), la grana traccia conserva il **valore massimo osservato**.

**Ragione**: FR-018 impone un valore osservato e deterministico. Restano in gioco massimo, minimo e prima occorrenza; media e mediana sono escluse dal requisito perché produrrebbero un valore che nessuna riga contiene. Fra i tre, la prima occorrenza è deterministica ma arbitraria — dipende dall'ordine di esportazione della fonte, cioè da nulla di interpretabile. Il massimo è invece leggibile come enunciato: *la popolarità più alta che quella traccia ha registrato nel dataset*. L'effetto della scelta è quantificabile e piccolo: sulle 720 tracce interessate, la somma delle popolarità è 27.352 con il massimo contro 26.566 con la prima occorrenza, uno scarto di 786 punti complessivi.

**Conseguenza da dichiarare**: il massimo introduce una distorsione verso l'alto, sistematica per costruzione ancorché minima. Il documento deve dirlo, non solo dichiarare la regola: è la differenza fra dichiarare una scelta e dichiararne l'effetto (FR-019).

### T6 — `date_added` in ISO 8601 con tabella dei mesi esplicita

**Decisione**: `September 25, 2021` → `2021-09-25`. Lo spazio iniziale dei 88 valori di F6 viene rimosso. I dieci valori vuoti restano vuoti e non vengono imputati. La conversione usa una mappa dei dodici nomi di mese scritta nel codice, **mai** `strptime` con `%B`.

**Ragione**: F6. Una conversione dipendente dal locale è una violazione di FR-003 che non si manifesta sulla macchina di chi scrive la pipeline e si manifesta su quella di chi la riesegue — cioè il caso peggiore, perché rompe esattamente la promessa che la feature esiste per mantenere.

### T7 — Si normalizza solo il campo delle categorie

**Decisione**: `listed_in` produce la tabella titolo-categoria di FR-012. `country`, `cast` e `director` restano stringhe di sorgente nell'output alla grana titolo.

**Ragione**: F7. La normalizzazione ha un consumatore dichiarato — `BQ1-K1` conta titoli per categoria, ed è il caso in cui i conteggi non sono sommabili. Gli altri tre campi non alimentano alcuna misura del framework. Normalizzarli produrrebbe tre tabelle senza lettore, che è lavoro e non valore, e in una feature al limite del principio III il costo si paga su qualcos'altro.

**Da dichiarare come limite**: chi in futuro volesse contare titoli per paese incontrerà lo stesso problema di sommabilità, non risolto. Va scritto nel documento perché sia una scelta nota e non una svista ereditata.

### T8 — L'artefatto di rendicontazione riusa lo schema del profilo, con spazio di nomi disgiunto

**Decisione**: `reports/cleaning_report.json` adotta la stessa struttura di `reports/data_profile.json` — mappa `values`, record con `value`, `display`, `label`, `unit` — e usa identificativi con prefisso **`CL.`**, disgiunto dai prefissi `NF.`, `SP.` e `X.` del profilo.

**Ragione**: due artefatti con lo stesso schema e prefissi disgiunti si risolvono con un'unica mappa unita, senza ambiguità e senza che il controllo debba sapere in anticipo dove cercare un identificativo. È ciò che rende possibile T9 a costo quasi nullo. La separazione in due file è invece obbligata da FR-030: il profilo descrive `data/raw/` e mescolarvi valori post-trasformazione riaprirebbe la confusione che quel requisito esiste per chiudere.

### T9 — Il corollario (c) di D5 si realizza spostando l'onere sull'autore, non sull'euristica

**Decisione**: nel nuovo documento ogni gruppo di cifre e ogni numerale scritto in lettere deve portare **uno di due marcatori**: l'ancora a un identificativo, che il controllo risolve e confronta; oppure un marcatore esplicito di **non-misurato**, che dichiara che quel numerale non è un fatto sui dati. Tutto ciò che non porta né l'uno né l'altro fa **fallire** il controllo.

**Ragione**: è la decisione che rende D5 realizzabile dentro la stima. Riconoscere automaticamente se un numerale è «in posizione di fatto misurato» richiede di interpretare la prosa italiana, ed è precisamente la fragilità che FR-025 della 002 vietava. L'esecuzione del controllo esistente su `docs/data_audit.md` lo dimostra: emette decine di avvisi su «due letture», «tre corollari», «zero», tutti legittimi. Nessuna regola posizionale li distingue da un fatto misurato; l'autore sì, e in un istante. Il marcatore di non-misurato costa una scrittura in più a chi scrive e restituisce un controllo che fallisce invece di avvisare — cioè un controllo che qualcuno leggerà.

**Perimetro**: la regola vale per il documento prodotto da questa feature. Estenderla a `docs/data_audit.md` significherebbe rimarcare un documento già mergiato, e non entra nelle 7 ore. È un ritrovamento registrato per la regia, secondo il precedente FR-032 della 002.

### T10 — Le invarianti si verificano, non si assumono

**Decisione**: la pipeline verifica e si ferma con errore (FR-004) su: impronta dei file di origine diversa da quella in `sources` del profilo; colonna attesa assente; regola di riparazione che tocca un numero di righe diverso da tre (F1); corrispondenza tipo-unità della durata video violata (F5); grana di un output non unica sulla propria chiave (FR-011); valore che non rispetta il tipo dichiarato nel contratto (T2); valore fuori da un dominio chiuso dichiarato.

**Ragione**: sono sette affermazioni che la ricognizione ha verificato oggi su questa versione dei dati. Scritte come commenti sarebbero opinioni; scritte come controlli sono ciò che impedisce alla pipeline di riscrivere dati in silenzio quando la fonte cambia. È il vincolo che la spec pone su D2 e che qui si generalizza.

### T11 — La colonna indice senza nome esce dagli output

**Decisione**: la prima colonna del catalogo musicale (F8) non compare in alcun output. È elencata fra le esclusioni nel documento, con la ragione.

**Ragione**: è l'indice di riga dell'esportazione, non un dato della fonte. Trasportarla produrrebbe una colonna che invita a essere usata come chiave e che non lo è: dopo la deduplicazione non sarebbe nemmeno più contigua. FR-010 chiede che nessun campo sparisca in silenzio, non che ogni campo sopravviva.

---

## Cosa la Fase 0 ha cambiato rispetto alla spec

Tre cose, tutte in aggiunta e nessuna in sottrazione.

1. **F2 aggiunge una decisione di trattamento che la spec non prevedeva**: la deduplicazione della grana coppia traccia-genere. Rientra sotto FR-011 e FR-029 senza modificarli, ma va dichiarata e quantificata come le altre.
2. **F4 rafforza D4 e ne precisa l'avvertenza obbligatoria**: l'insieme dei sette generi è invariante alla trasformazione, e il genere più vicino alla soglia dista 1,55 punti. La spec chiedeva di dichiarare la sensibilità; ora se ne conosce il valore.
3. **F6 e T6 introducono un rischio di determinismo che nessun criterio di successo copriva esplicitamente**: la dipendenza dal locale. SC-001 lo intercetta solo se le due esecuzioni avvengono su locale diversi, il che non accade. Il presidio è T6 più il divieto in [quickstart.md](./quickstart.md) di introdurre conversioni dipendenti dall'ambiente.
