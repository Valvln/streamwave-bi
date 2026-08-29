# Ricerca — Fase 0

Tre domande aperte dal piano, tutte chiuse su documenti e artefatti già nel repository. **Nessuna richiede una fonte esterna, e nessuna riapre una decisione già presa**: dove la risposta esisteva, questa fase la trova e la cita invece di ricostruirla.

---

## R-1 — Con quale identificativo si pubblicano le voci nuove

**La domanda.** `reports/kpi_measures.json` entra in uno spazio dei nomi **unito** con altri cinque artefatti, e `scripts/check_audit_coherence.py` verifica che l'unione non abbia collisioni invece di assumerlo (`convenzioni-marcatura.md` §3). Le chiavi nuove devono quindi essere scelte, non improvvisate.

**Che cosa lo schema esistente stabilisce già.** Le chiavi dell'artefatto hanno la forma `KPI.<sigla><KPI>.<sottodominio>.<voce>`, e il sottodominio esiste dove un gruppo di voci risponde a una domanda propria:

| Precedente già nell'artefatto | Che cosa raggruppa |
|---|---|
| `KPI.BQ1K1.c1.above_median`, `.c1.median_of_42`, `.c1.category_count.music_musicals` | la condizione `C1`, con la soglia e i due termini del confronto |
| `KPI.BQ1K1.north_star_invariance.*` | una verifica a sé, con esito, differenza e i due conteggi confrontati |
| `KPI.BQ1K3.bound.<asse>.<estremo>` | gli estremi degli assi di mood |

**La decisione**: `C2` prende il sottodominio `c2` sotto la sigla del KPI che la misura, esattamente come `c1` sta sotto `BQ1K1`; il verdetto, che non appartiene ad alcun singolo KPI, prende un sottodominio proprio sotto il prefisso `KPI.`.

- `KPI.BQ1K3.c2.threshold` — la soglia di maggioranza
- `KPI.BQ1K3.c2.satisfied` — l'esito booleano
- `KPI.BQ1K3.c2.margin` — il margine assoluto
- `KPI.BQ1K3.c2.margin_share_of_value` — la sovrastima richiesta come quota del valore (`V9`)
- `KPI.verdict.conditions_satisfied` — quante delle tre condizioni sono soddisfatte
- `KPI.verdict.all_satisfied` — l'esito della congiunzione

**Perché `C2` sta sotto `BQ1K3` e non sotto un prefisso proprio.** Perché `C1` sta sotto `BQ1K1`. La regola di decisione non è un KPI: è una lettura di tre KPI, e ciascuna condizione vive sotto la misura che la determina. Metterla altrove obbligherebbe chi cerca «dove sta `C2`» a sapere che le tre condizioni sorelle vivono in tre posti con tre criteri diversi.

**Perché il verdetto no.** Non è determinato da alcun KPI singolo: metterlo sotto uno dei tre lo attribuirebbe a quello, e la scelta di quale sarebbe arbitraria. `KPI.verdict.*` è un sottodominio nuovo dentro un prefisso già verificato — non introduce alcuna radice nuova nello spazio dei nomi unito, quindi non tocca il rischio di collisione che il controllo presidia.

**Verifica eseguita**: nessuna delle sei chiavi esiste oggi in alcuno dei sei artefatti; il prefisso `KPI.` è già di proprietà esclusiva di `reports/kpi_measures.json`.

---

## R-2 — Come si marca un numerale che non è misurato e non è una soglia del progetto

**La domanda.** La tabella di sensibilità di `V8` contiene basi di riferimento — valori di abbonati stipulati per illustrare l'aritmetica. Non sono misure, non sono soglie di analisi, e non sono fatti dichiarati altrove. La grammatica di `convenzioni-marcatura.md` deve coprirli, o la decisione `V8` non è realizzabile in un documento a severità stretta.

**Che cosa la grammatica dice.** Il marcatore di non-misurato `<!--#-->` non asserisce nulla sul valore: dichiara che chi scrive **ha considerato** quel numerale e afferma che non appartiene agli artefatti. Copre quattro categorie (§2): numerali di struttura del discorso; **soglie, che sono stipulazioni di chi analizza e non osservazioni sui dati**; fatti dichiarati altrove; fatti non verificabili.

**La decisione**: le basi di riferimento ricadono nella **seconda** categoria, con una precisazione che la prosa deve portare — sono stipulazioni **di chi legge**, non di chi analizza. La forma del marcatore è la stessa; ciò che cambia è l'onere della prosa, che deve dire di chi è l'ipotesi.

**Perché la distinzione non diventa una quinta forma.** §2 lo stabilisce già per un caso analogo: «un solo marcatore copre tutti e quattro i casi. La distinzione fra "non misurabile" e "misurato altrove" resta un onere della prosa e non diventa una quinta forma: un lettore la coglie meglio da una frase italiana che da un simbolo in più». Introdurre una forma nuova per questa feature romperebbe una grammatica stabile da sei feature per un guadagno che una frase ottiene meglio.

**Il vincolo che ne discende, e che il contratto di documento recepisce**: la tabella di sensibilità non può limitarsi a marcare. Deve dichiarare in prosa, accanto alla tabella, che le basi sono un'illustrazione parametrica e che **il moltiplicatore lo mette chi legge** — perché il marcatore, da solo, non distingue una stipulazione di chi scrive da una di chi legge, ed è precisamente la distinzione che qui conta.

**Un secondo esito, sulle quantità che il controllo non vede.** §6 dichiara che frazioni e ordinali in lettere — «un quinto», «la metà» — non sono riconosciuti: «sono presidiate a mano, e questa riga esiste perché chi legge sappia dove il presidio è umano». La raccomandazione parlerà di maggioranza e di metà: **quelle espressioni non saranno segnalate dal controllo**, e la loro correttezza dipende interamente dalla revisione. È un limite noto della verifica, da dichiarare nel quickstart invece di scoprirlo dopo.

---

## R-3 — Quali affermazioni la raccomandazione ripete, e dove vivono già

**La domanda, e perché è la più importante delle tre.** La chiusura della `008b` ha prodotto un ritrovamento che nessuna revisione precedente poteva fare: una frase mal contata esisteva in **due copie**, e la seconda stava in un documento che il revisore non aveva ricevuto. Non è un rilievo mancato, è una conseguenza del perimetro. La raccomandazione è il documento più esposto a questo difetto di tutto il progetto, perché **per costruzione ripete affermazioni che vivono già altrove**: è il suo scopo.

**Il censimento**, eseguito sui documenti pubblicati e non a memoria:

| Affermazione | Dove vive già | Copie |
|---|---|---|
| il tasso di `BQ3-K1` è **lordo**, le disdette sono escluse | `business_case.md` §5.5 (scheda `BQ3-K1`), `bq3_scenarios.md` §8, `kpi_operators.md` §8, `kpi_measures.md` §8 | 4 |
| l'uplift è un **livello mensile a regime**, non un cumulato | `business_case.md` §5.5 (scheda `BQ3-K2`), `bq3_scenarios.md` §8, `kpi_operators.md` §9, `kpi_measures.md` §8 | 4 |
| l'uplift non si moltiplica per una base che il progetto non quantifica | `bq3_scenarios.md` §8, `kpi_operators.md` §9, `kpi_measures.md` §8 | 3 |
| i valori di `BQ3` si presentano **sempre** come intervallo, mai isolati | `business_case.md` §6 e §7, `bq3_scenarios.md` §5, `kpi_operators.md` §8, `kpi_measures.md` §8 | 4 |
| `mood_profile_overlap` è una **stima per eccesso** | `kpi_operators.md` §4 e §12, `kpi_measures.md` §4.3 | 3 |
| il contratto di versione: una revisione della tabella dei mood **invalida** il valore | `content_taxonomy_bridge.md` §5, `kpi_operators.md` §4 e §7, `kpi_measures.md` §4.1 e §7 | 4 |
| i 7 segmenti `is_high_zero_genre` portano domanda **non misurata dalla fonte** | `kpi_operators.md` §5.1, `kpi_measures.md` §5.3 e §7.4 | 3 |
| i segmenti si sovrappongono; contare le righe non li dimensiona | `business_case.md` §5.2, `data_model.md` §18, `kpi_operators.md` §5.2, `kpi_measures.md` §5.4 | 4 |
| la lettura dell'esito «tre su tre» | `business_case.md` §3 | 1 |
| `A1` e `A6` restano fuori dalla scala di confidenza | `business_case.md` §2 e §6 | 2 |

**La divergenza già presente, trovata da questo censimento.** `kpi_operators.md` §9 scrive che l'uplift **«non è scalabile»**. `bq3_scenarios.md` §8 dichiara che quella formulazione **è falsa**: «il valore *è* scalabile, chiunque disponga di una stima di abbonati lo moltiplica in pochi secondi», e la formulazione corretta è più stretta — *qui nessuna base viene quantificata e l'artefatto non offre alcuna chiave; non è un presidio, è una rinuncia*.

Le due copie divergono, e nessun controllo può accorgersene. È lo stesso difetto già registrato come issue [`#26`](https://github.com/Valvln/streamwave-bi/issues/26) sul contratto di pagina della `008a`.

**Che cosa questa feature ne fa**, e la scelta va dichiarata perché è un rinvio: **non la corregge**. Correggere `kpi_operators.md` §9 significherebbe aggiungere una nota in loco a un documento già mergiato per un difetto che questa feature non introduce e che il suo deliverable non rende falso — e la regola del 2026-08-22 riserva le chiusure in-branch ai rilievi senza cui il deliverable afferma il falso. La feature **registra il ritrovamento** come issue nuova sul tracker, e si limita a non ripetere l'errore: `docs/raccomandazione.md` usa la formulazione stretta, come `V8` prescrive.

*Che questo sia un ritrovamento e non un rilievo di revisione va detto*: nessuno lo ha sollevato, è emerso censendo le copie. La forma in cui si registra è quella dei ritrovamenti — issue con riferimento puntuale — non quella dei rilievi.

**Le due conseguenze operative del censimento:**

1. **il contratto di documento cita, per ogni affermazione ereditata, la copia autorevole** che la raccomandazione deve seguire. Dove esistono più copie e una è più stretta, vince la più stretta: per l'uplift è `bq3_scenarios.md` §8;
2. **il perimetro della revisione deve contenere le copie**, non solo il deliverable. È l'unico modo perché il revisore possa vedere una divergenza; su estratti isolati non lo potrebbe per costruzione. Il verbale dichiarerà che cosa gli è stato dato, come i quattro obblighi impongono.

---

## Che cosa questa fase non ha risolto, e non doveva

- **il valore del margine** non è oggetto di ricerca: è aritmetica sui valori pubblicati, e lo calcola lo script. Nessun numero di questa fase entra in alcun documento;
- **la soglia di `C2`** è fissata dalla spec (`V1`), non da qui;
- **la struttura del report della `010a`** è fuori perimetro, anche dove questa feature ne determina il contenuto.
