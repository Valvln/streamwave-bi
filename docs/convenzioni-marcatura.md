# Convenzioni di marcatura dei valori

Definizione normativa della grammatica con cui i documenti di questo progetto legano ogni numero pubblicato all'artefatto che lo produce, e di ciò che `scripts/check_audit_coherence.py` garantisce verificandola.

Questo file è la **fonte unica**. Prima del 2026-08-15 la grammatica viveva in due contratti di feature — `specs/002-data-audit-profiling/contracts/profile-artifact.md` §4 per le prime tre forme, `specs/003-data-cleaning-etl/contracts/output-datasets.md` §3 per la quarta e per la severità. Entrambi rinviano ora qui: la chiave di lettura di un documento pubblicato non può stare in una cartella di lavorazione che il lettore non ha ragione di aprire.

**Questo documento non è sottoposto al controllo**, e la ragione è che non contiene fatti misurati sui dati: i numerali che vi compaiono descrivono la grammatica, non i cataloghi. È l'unica eccezione, ed è dichiarata qui perché non sia una svista.

---

## 1. Forma

Il marcatore è un commento HTML, invisibile in qualunque lettore Markdown, e segue il testo che marca **senza spazio interposto**.

```
<testo-display><!--@<identificativo>-->
```

Come si scrive:

```markdown
Il catalogo video contiene 8.807<!--@NF.shape.rows--> titoli, di cui
6.131<!--@NF.type.movie--> film e 2.676<!--@NF.type.tvshow--> serie.
```

Come si legge:

> Il catalogo video contiene 8.807 titoli, di cui 6.131 film e 2.676 serie.

## 2. Le quattro forme

Le prime tre nascono con la feature 002 — la prima con il contratto, le altre due dopo che una revisione indipendente ha dimostrato che una marcatura limitata alle cifre lasciava scoperta proprio la zona in cui gli errori passano, le affermazioni derivate scritte a mano. La quarta nasce con la 003.

| Forma | Come si scrive | Che cosa dichiara, e come viene verificata |
|---|---|---|
| **cifre** | `8.807<!--@NF.shape.rows-->` | è un valore di un artefatto; confronto carattere per carattere con `display` |
| **numerale in lettere** | `dodici<!--@X.claims_001.coincide-->` | come sopra; il numerale è convertito e confrontato con `value` |
| **letterale** | `` `Music & Musicals`<!--@catalogs.netflix_categories_musical--> `` | il letterale è membro dell'elenco indicato |
| **non-misurato** | `Le due<!--#--> letture` | il numero **non è un valore di questi artefatti**, e chi scrive lo dichiara |

I numerali in lettere riconosciuti arrivano fino a *venti*: oltre, e per qualunque misura, si scrive in cifre.

### La forma di non-misurato

`<!--#-->` non asserisce nulla sul valore. Dichiara che chi scrive **ha considerato** quel numerale e afferma che non appartiene agli artefatti. Copre quattro categorie:

- i **numerali di struttura del discorso** — «le due letture», «tre corollari» — che non sono quantità misurate;
- le **soglie**, che sono stipulazioni di chi analizza e non osservazioni sui dati. Dove una soglia ha un valore registrato fra le convenzioni di un artefatto la si **ancora** invece di marcarla: ancorare è sempre più forte che dichiarare;
- i **fatti dichiarati altrove** — per esempio la copertura temporale delle fonti, che vive nella constitution — ma solo dove lo sono davvero. Un numero ancorabile che non viene ancorato è il caso peggiore di questa categoria;
- i **fatti non verificabili**, come un'affermazione sulla storia di un'esecuzione passata. Qui il marcatore è formalmente corretto ma dice meno di quanto serve: **la prosa deve dichiarare che il fatto non è verificabile**, perché il marcatore da solo non lo distingue da un numerale retorico.

Un solo marcatore copre tutti e quattro i casi. La distinzione fra «non misurabile» e «misurato altrove» resta un onere della prosa e non diventa una quinta forma: un lettore la coglie meglio da una frase italiana che da un simbolo in più.

## 3. Dove si risolvono gli identificativi

Il controllo unisce in un unico spazio dei nomi le mappe `values` di tutti gli artefatti versionati — oggi `reports/data_profile.json`, `reports/cleaning_report.json`, `reports/bq3_scenarios.json` e `data/curated/dim_category_mood.json` — e **verifica** che l'unione non abbia collisioni invece di assumerlo. Restano risolvibili anche `catalogs.<chiave>` e `conventions.<chiave>` di ciascun artefatto, con semantica di appartenenza: il testo marcato deve essere membro dell'elenco.

## 4. Regole

1. il testo che precede immediatamente il marcatore — un letterale fra apici inversi, oppure la sequenza senza spazi fino al primo spazio o all'inizio di riga — deve corrispondere secondo la forma usata;
2. un identificativo può essere marcato più volte nello stesso documento;
3. il marcatore funziona ovunque, in prosa come in cella di tabella;
4. un marcatore che vive **dentro** un frammento di codice in linea è sintassi mostrata come esempio, non un'ancora, e non viene verificato: un documento deve poter documentare il proprio meccanismo senza attivarlo;
5. non esistono altre forme. Una quantità priva di marcatore non è un valore di artefatto e il controllo non la confronta.

Due vincoli di scrittura discendono dalla regola 1 e sono costati entrambi un difetto reale:

- **il marcatore non deve essere separato dal valore da altra formattazione.** `**421<!--@ID-->**` fa catturare `**421` e il confronto fallisce: un numero ancorato non si scrive in grassetto;
- **una sostituzione automatica non deve poter entrare in un identificativo.** Un marcatore finito dentro un'ancora la spezza e il valore si degrada in silenzio a dichiarazione di non-misurato. Il controllo oggi fallisce su entrambi i sintomi — un'apertura di commento dentro il valore catturato, una chiusura di commento rimasta nel testo — ma la guardia esiste perché il difetto è già accaduto.

## 5. Che cosa il controllo verifica, e con quale severità

| Condizione | Esito |
|---|---|
| il testo prima del marcatore corrisponde secondo la sua forma | passa |
| il testo prima del marcatore **non** corrisponde | errore: riporta identificativo, atteso e trovato |
| il marcatore punta a un identificativo assente dagli spazi dei nomi | errore: riporta il riferimento non risolvibile |
| un riferimento a `catalogs`/`conventions` è usato su un valore non fra apici inversi | errore |
| il valore catturato contiene un'apertura di commento, o resta una chiusura nel testo | errore: il marcatore è malformato |
| una cifra o un numerale non è adiacente ad alcun marcatore | **dipende dal documento**, vedi sotto |

L'ultima riga è l'unica che varia. La severità è dichiarata per documento in `DOCUMENTS`, dentro lo script:

| Documento | Quantità priva di marcatore |
|---|---|
| `docs/data_audit.md` (002) | avviso |
| `docs/data_cleaning.md` (003) | **errore** |
| `docs/bq3_scenarios.md` (004) | **errore** |
| `docs/data_model.md` (005) | **errore** |
| `docs/content_taxonomy_bridge.md` (006) | **errore** |

> **Nota in loco — 2026-08-20, feature `006`.** Le due righe finali sono state aggiunte insieme. Quella della `005` **mancava**: `docs/data_model.md` era entrato in `DOCUMENTS` sotto severità stretta con la feature 005, e questa tabella non lo registrava — un drift scoperto dalla `006` mentre aggiungeva il proprio documento, non un rilievo di revisione. Il testo precedente non viene riscritto altrove: l'omissione era una riga assente, e la correzione è la riga presente. La conseguenza per chi legge è che fra il merge della `005` e questa data la tabella dichiarava tre documenti verificati mentre lo script ne verificava quattro; la fonte autorevole restava e resta `DOCUMENTS`.

È il corollario (c) della regola di §7, ed è tutta la differenza fra un controllo che elenca e uno che ferma. **La severità stretta vale per i documenti nuovi e non è retroattiva**: applicarla al documento della 002 richiederebbe di rimarcare un artefatto già mergiato, ed è un ritrovamento registrato per la regia, non un lavoro che una feature successiva assorbe di nascosto.

Il controllo legge **solo** documenti e artefatti versionati: non richiede `data/raw/` e non riesegue alcuna pipeline.

**Una verifica che non riguarda la marcatura.** Dalla feature 006 lo stesso script porta anche un presidio sui **dati** degli artefatti, eseguito prima di leggere qualunque documento: l'insieme delle categorie coperte da `data/curated/dim_category_mood.json` deve coincidere con il catalogo delle categorie video di `reports/cleaning_report.json`, e una divergenza è un errore. Sta qui, e non fra le righe della tabella, perché non è una condizione sulla grammatica: è un vincolo di coerenza fra due artefatti, che condivide con la marcatura solo il comando che lo esegue. Chi cerca in questa pagina la lista completa di ciò che l'esito verde certifica deve contare anche quello.

## 6. Le esclusioni strutturali

Alcune classi di cifre non richiedono marcatore perché sono riferimenti e non quantità: sigle di KPI, requisiti, criteri, storie e task; rilievi, decisioni, ritrovamenti, voci di inventario e assunzioni; numeri di feature, date, versioni, riferimenti di sezione, numeri di divergenza dei verbali, nomi di standard, numerazione degli elenchi ordinati Markdown, codice in linea, bersagli dei link, intestazioni e blocchi di codice.

**L'elenco normativo è quello dichiarato in `scripts/check_audit_coherence.py`**, ed è questa la forma definitiva, non un ripiego: una esclusione vive dove viene applicata, altrimenti le due copie divergono e nessuna delle due è vera. Un documento che dichiara la propria copertura ne nomina le classi — come fa §2 di [`data_cleaning.md`](data_cleaning.md) — e rinvia allo script per la lista.

Restano fuori dal vocabolario dei numerali le quantità espresse per frazione o ordinale in lettere — «un quinto», «la metà», «un decimo di punto». Il controllo non le riconosce: sono presidiate a mano, e questa riga esiste perché chi legge sappia dove il presidio è umano.

## 7. Le affermazioni derivate sono esse stesse valori

Regola di progetto, nata come decisione D5 della feature 003.

> Un confronto, una graduatoria, un rapporto o una differenza costruiti su valori misurati sono essi stessi valori misurati. O esistono nell'artefatto con un identificativo proprio e vengono ancorati come qualunque altro numero, o non si scrivono. Non esiste la categoria intermedia dell'affermazione che «si ricava dai numeri già pubblicati e quindi non ha bisogno di fonte».

Tre corollari:

- **(a)** superlativi, ordinali e moltiplicatori riferiti a fatti misurati sono ammessi solo se ancorati;
- **(b)** i numerali scritti in lettere sono vietati per qualunque fatto misurato;
- **(c)** il controllo **fallisce** — non avvisa — su un numerale non ancorato in posizione di fatto misurato.

Il corollario (c) è realizzabile solo spostando l'onere su chi scrive: ogni numerale porta o l'ancora o il marcatore di non-misurato. Far indovinare al controllo se un numerale sia un fatto è l'euristica sulla prosa italiana che la 002 aveva già vietato.

**La seconda forma di §2 e il corollario (b) convivono, e la convivenza va dichiarata.** Il controllo continua ad accettare il numerale in lettere ancorato perché lo usa il documento della 002; i documenti nuovi non lo usano, perché (b) è la regola più severa. La forma **non** viene rimossa dalla grammatica: rimuoverla romperebbe un artefatto già mergiato per guadagnare una semplificazione che nessuno sta chiedendo.

## 8. Il confine della garanzia

Il controllo verifica ciò che è ancorato. **Non può accorgersi di un'affermazione che *avrebbe dovuto* essere ancorata**, né impedire che un fatto misurato venga marcato come non-misurato: contro la dichiarazione falsa esiste la revisione in contesto pulito, non il controllo. Un esito verde certifica le ancore, non l'intero documento — e questa frase è qui perché la sua assenza è già costata tre affermazioni errate sfuggite a un controllo che dichiarava tutto coerente.

Ciò che il marcatore elimina è la categoria dell'omissione distratta. Non elimina la categoria della menzogna.

---

## Provenienza

| Data | Feature | Che cosa ha stabilito |
|---|---|---|
| 2026-08-08 | 002 | la forma del marcatore, l'ancora a cifre, i due spazi dei nomi di appartenenza, il confine della garanzia |
| 2026-08-09 | 002 | il numerale in lettere e il letterale, dopo la revisione in contesto pulito |
| 2026-08-11 | 003 | il marcatore di non-misurato, la severità per documento, l'unione degli spazi dei nomi con verifica delle collisioni |
| 2026-08-15 | 003 | consolidamento in questo file; le due guardie sui marcatori malformati; la convivenza fra la seconda forma e il corollario (b); un solo marcatore per i quattro casi di non-misurato; lo script come elenco normativo delle esclusioni |
| 2026-08-16 | 004 | il terzo artefatto nello spazio dei nomi unito e il terzo documento in severità stretta; l'elenco degli artefatti dichiarato una volta sola nello script, dopo che era duplicato fra la lettura e l'intestazione stampata |
| 2026-08-20 | 006 | il quarto artefatto (`data/curated/dim_category_mood.json`, il primo fuori da `reports/`) e il quinto documento in severità stretta; il presidio sulla tassonomia delle categorie, che è un controllo sui **dati** degli artefatti e non sulla marcatura dei documenti; il recupero della riga di severità della `005`, mai registrata qui |

**Una nota su ciò che la grammatica non esclude, scoperta scrivendo il documento della 004.** Le sigle di requisito con **suffisso letterale** — `FR-011a`, `FR-017a` — non rientrano nell'esclusione strutturale, che si chiude su un confine di parola dopo le cifre e non lo trova quando segue una lettera. In severità stretta la sigla viene quindi segnalata come quantità priva di marcatore. Non è un difetto da correggere allargando il criterio: le sigle si scrivono fra apici inversi, come già si fa per gli identificativi tecnici, e il caso si chiude senza toccare l'espressione. Sta qui perché il prossimo che lo incontra non lo prenda per un errore del controllo.
