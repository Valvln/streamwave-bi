# Come si verifica questa feature

**Feature**: `010a-report-disegno` | **Data**: 2026-08-29

Questa feature produce **testo**: un contratto di disegno e i documenti che lo sostengono. Non tocca dati, non tocca script, non apre Power BI. Ne discende che quasi nulla di ciò che va verificato è verificabile da un comando — e questo documento dice quali sono le due eccezioni e quali sono le prove che restano umane.

---

## 1. Le prove eseguibili

**Sono due, ed è onesto dichiarare che certificano poco.**

```bash
python3 scripts/check_audit_coherence.py
```

**Che cosa certifica**: che nessuno dei documenti pubblicati sotto `docs/` sia stato rotto da questa feature. Questa feature non ne modifica nessuno, quindi l'esito verde certifica **un'assenza di danno, non una presenza di qualità**. Va eseguito comunque, perché un esito rosso significherebbe che qualcosa è stato toccato senza che nessuno se ne accorgesse.

**Che cosa non certifica**: nulla del contratto di pagina. Il controllo legge i documenti dichiarati in `DOCUMENTS`, che vivono sotto `docs/`; il contratto vive sotto `specs/` e non vi entra — come non vi entrava quello della `008a`.

```bash
python3 -c "import json; d=json.load(open('reports/kpi_measures.json'))['values']; \
  [print(k, d[k]['display']) for k in sorted(d) if k in ('KPI.verdict.conditions_satisfied','KPI.BQ1K3.c2.margin','KPI.BQ1K3.c2.margin_share_of_value','KPI.BQ1K3.c2.threshold','KPI.BQ2K3.threshold.demand','KPI.BQ2K3.threshold.affinity')]"
```

**Che cosa certifica**: che ogni identificativo di ancora citato dal contratto per le misure nuove `M1`, `M3`, `M4` ed `M5` sia risolvibile contro l'artefatto. È il presidio contro l'ancora inventata — un identificativo plausibile che non esiste, che nessun controllo di questa feature intercetterebbe altrimenti.

---

## 2. Le prove per ispezione

Ciascuna è un'osservazione umana, e va dichiarata come tale nell'esito. L'esito si scrive **mentre si verifica**, non a memoria alla fine.

| # | Prova | Come si esegue | Esito atteso |
|---|---|---|---|
| `P1` | l'ordine è quello dell'argomento | si legge la sola colonna «parte dell'argomento» della mappa, dall'alto in basso | si legge come un discorso; l'ordine coincide con quello delle sezioni di `docs/raccomandazione.md` e non con `BQ1`→`BQ2`→`BQ3` |
| `P2` | ogni pagina dichiara le cinque voci | si scorre ciascuna sezione di pagina del contratto cercando: parte dell'argomento, valori con ancora, misure distinte fra esistenti e nuove, visuali con tipo e assi, interazioni non offerte | nessuna pagina ne omette una |
| `P3` | nessun valore è trascritto | si cerca nel contratto qualunque cifra che non sia un numero di pagina, una sigla o un riferimento di sezione | nessuna cifra in posizione di valore misurato; tutti i valori compaiono come identificativo di ancora |
| `P4` | ogni pagina dà all'occhio qualcosa | si scorre l'elenco delle visuali pagina per pagina | nessuna pagina ha come soli elementi schede e tabelle, salvo le due dichiarate di sola prosa con la ragione |
| `P5` | il conteggio delle pagine | si contano le righe della mappa | dieci, con la convenzione dichiarata; dentro la forchetta 8-12 |
| `P6` | le assunzioni `A1` e `A6` hanno una collocazione | si cerca dove il contratto le colloca | su una pagina propria, non in nota a piè di schermo |
| `P7` | la formulazione sull'uplift | si cerca nel contratto la stringa «scalabile» | compare solo nella forma stretta di `bq3_scenarios.md` §8; mai «non è scalabile» come affermazione propria |
| `P8` | il debito della `004` è dichiarato dove pesa | si cerca la pagina degli scenari | dichiara che il debito sulla verificabilità del benchmark è aperto |
| `P9` | le tre verifiche dell'issue `#20` | si cerca il richiamo nel contratto | dichiarato che chi costruisce le rifà; l'issue resta aperta |
| `P10` | il censimento delle copie | si esegue la tabella di §3 | nessuna divergenza, oppure divergenze dichiarate come ritrovamento |

---

## 3. Il censimento delle affermazioni in doppia copia

**È la prova `P10`, e ha una sezione propria perché è il presidio che la `009` ha usato dopo il ritrovamento della chiusura della `008b`** — dove un'affermazione sbagliata esisteva in due copie e il revisore ne aveva ricevuta una sola.

Il contratto di pagina ripete necessariamente alcune affermazioni che vivono già altrove. Ciascuna va confrontata con l'originale **prima** che la revisione cominci.

| Affermazione | Vive già in | Nel contratto compare | Verifica |
|---|---|---|---|
| la formulazione stretta sull'uplift | `bq3_scenarios.md` §8; `docs/raccomandazione.md` §4 | pagina 9 | le due copie originali coincidono fra loro, e il contratto usa la stessa |
| il divieto di scheda singola per `BQ3` | contratto `008a` §6; constitution, principio I | pagina 9 | invariato |
| la lettura dei segmenti a domanda non misurata | `kpi_measures.md` §5.3; `docs/raccomandazione.md` §3; contratto `008a` §5.1 | pagina 8 | le tre copie coincidono |
| che i segmenti non si sommano | `data_model.md` §18; `docs/raccomandazione.md` §3 | pagina 8 | le due copie coincidono |
| la confidenza del verdetto non è la media delle tre | `docs/raccomandazione.md` §2 | pagina 2, e §4 di `data-model.md` | copia unica nel contratto, coincidente con l'originale |
| «stima per eccesso» per `BQ1-K3` | `kpi_measures.md` §4.3; `docs/raccomandazione.md` §2 | pagine 5 e 6 | le due copie coincidono |
| il margine è una condizione sull'errore, non una stima | `docs/raccomandazione.md` §2 | pagina 6 | copia unica nel contratto |

**Che cosa si fa se due copie divergono**: è un ritrovamento e si dichiara. Non si corregge `docs/raccomandazione.md`, che è fuori perimetro; non si sceglie silenziosamente la formulazione che piace di più.

---

## 4. Esito della verifica

*Compilata il 2026-08-29, mentre le prove venivano eseguite.*

### Prove eseguibili

| Prova | Esito |
|---|---|
| `check_audit_coherence.py` | ✅ verde — «documenti e artefatti coerenti». Certifica un'assenza di danno: questa feature non tocca alcun documento sotto `docs/` |
| risoluzione degli identificativi di ancora | ✅ ogni ancora citata dal contratto risolve contro un artefatto versionato, comprese le tre aggiunte durante la correzione di `P3` (`CL.NF.category.distinct`, `SP.genre.count`, `MOOD.coverage.rows`) e le due con segnaposto (`KPI.BQ2K1.<segmento>.*`, `MOOD.category.<categoria>.<asse>`) |

### Prove per ispezione

| Prova | Esito |
|---|---|
| `P1` — l'ordine è quello dell'argomento | ✅ la colonna «parte dell'argomento» si legge come un discorso; l'ordine coincide con le sezioni di `raccomandazione.md` |
| `P2` — le cinque voci per pagina | ✅ tutte e dieci le pagine dichiarano parte dell'argomento, sezione servita, valori con ancora, visuali o struttura, interazioni non offerte |
| `P3` — nessun valore trascritto | ⚠️ **quattro violazioni trovate e corrette**, vedi sotto |
| `P4` — ogni pagina dà qualcosa all'occhio | ✅ otto pagine con visuale, due di sola prosa dichiarate con la ragione |
| `P5` — il conteggio delle pagine | ✅ dieci, iniziale compresa, dentro la forchetta |
| `P6` — collocazione di `A1` e `A6` | ✅ pagina 3, propria, richiamate a pagina 9 e 10 e mai introdotte in nota |
| `P7` — la formulazione sull'uplift | ✅ «scalabile» compare una volta sola, nella forma che dichiara **falsa** la formulazione esclusa |
| `P8` — il debito della `004` | ✅ dichiarato aperto a pagina 9, dove i numeri di `BQ3` compaiono |
| `P9` — le tre verifiche dell'issue `#20` | ✅ dichiarate a §13.4; l'issue resta aperta e non viene toccata |
| `P10` — il censimento delle copie | ⚠️ **una divergenza trovata e corretta**, vedi sotto |

### Che cosa `P3` ha trovato

Il contratto dichiarava in apertura di non trascrivere alcun valore, **e ne trascriveva quattro**: il numero di categorie video, il numero di segmenti, il conteggio di titoli della categoria musicale, il numero di tracce del catalogo musicale, più il margine relativo in forma arrotondata.

Corretti sostituendo ciascuno con la propria ancora o con una formulazione non numerica. È il difetto che `FR-003` esiste per impedire, ed è passato sotto la prima stesura: la prova che lo ha trovato è meccanica, e senza di essa sarebbe arrivato alla revisione.

**Una cifra resta nel documento**, il fattore `100.000` di §11. Non è un fatto misurato ma un'**unità dichiarata** — la stessa categoria delle soglie nella grammatica dei marcatori — e `raccomandazione.md` §4 la marca infatti come non-misurata. La sua permanenza è dichiarata in apertura del contratto perché non venga letta come una svista.

### Che cosa `P10` ha trovato

Le sette affermazioni in doppia copia sono state confrontate con i rispettivi originali. **Sei coincidono.** La settima divergeva, e la divergenza era **interna ai documenti di questa feature**:

- `raccomandazione.md` §2 scrive che una congiunzione non è più affidabile del suo **termine meno affidabile**;
- `research.md` `G5` e `data-model.md` §4 scrivevano «termine **più debole**».

Sono sinonimi e nessuna delle due afferma il falso. È comunque una divergenza: l'originale usa una formulazione sola, e due riscritture ne introducevano una seconda che a valle si sarebbe potuta citare come se fosse la sua. Allineate entrambe alla formulazione dell'originale.

**È il caso per cui il censimento esiste**, ed è la prima volta che intercetta qualcosa: sulla `009` aveva confermato sette copie su sette.

### Scostamenti fra il disegno e ciò che è stato prodotto

**Uno**, dichiarato nel contratto a §9 e in `CP-4`: il conteggio dei membri del quadrante compare a schermo, mentre il contratto della `008a` §5.3 dichiarava esplicitamente che non doveva comparire. Non è una correzione di quel contratto — è una decisione diversa in un disegno diverso, dove l'argomento usa quel conteggio come esito della terza condizione.

### Ritrovamenti

I tre di [data-model.md](./data-model.md) §5, invariati:

1. nessun profilo di mood per segmento musicale è pubblicato come valore ancorato;
2. `C2` è l'unica delle tre condizioni senza una companion booleana pubblicata;
3. il report porta sette KPI su otto.

**Nessuno richiede una nota in loco**: nessuno è una divergenza fra un valore pubblicato e il suo artefatto.

**Nessuna divergenza è stata trovata fra il disegno e ciò che `docs/raccomandazione.md` afferma.**

### La revisione in contesto pulito

Eseguita il 2026-08-29 da un subagent isolato, con il perimetro composto secondo [plan.md](./plan.md). Verbale in [review.md](./review.md).

**Esito sulla domanda**: il disegno regge la spina dell'argomento, «sostanzialmente e non solo formalmente».

**Otto rilievi**: tre sostanziali (`R1`, `R2`, `R3`), cinque minori. Cinque chiusi dentro la feature per decisione della regia — che ha allargato la soglia rispetto alla proposta di questa sessione, includendo `R3` — e tre rinviati alle issue [`#32`](https://github.com/Valvln/streamwave-bi/issues/32), [`#33`](https://github.com/Valvln/streamwave-bi/issues/33), [`#34`](https://github.com/Valvln/streamwave-bi/issues/34).

**Che cosa la chiusura di `R1` ha cambiato nel disegno**, ed è la modifica più sostanziale che la revisione ha prodotto: i segmenti a domanda non misurata **escono dall'ordinamento della graduatoria** invece di occuparne la coda. Era la terza opzione che il contratto non aveva considerato, fra troncare la coda e ordinare tutto.

**Verifiche rieseguite dopo le correzioni**: controllo di coerenza verde, `P2` invariata su tutte e dieci le pagine, tutti i rimandi interni risolvono.
