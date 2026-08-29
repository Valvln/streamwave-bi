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

*Questa sezione si compila quando le prove vengono eseguite, non prima.*

**Prove eseguibili**: ⬜ da eseguire

**Prove per ispezione**: ⬜ da eseguire

**Censimento delle copie**: ⬜ da eseguire

**Scostamenti fra il disegno e ciò che è stato prodotto**: ⬜

**Ritrovamenti**: tre già registrati in [data-model.md](./data-model.md) §5, da riportare nell'esito finale.
