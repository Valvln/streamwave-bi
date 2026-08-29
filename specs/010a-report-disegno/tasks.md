# Tasks: il report che porta l'argomento a schermo — disegno

**Feature**: `010a-report-disegno` | **Data**: 2026-08-29 | **Plan**: [plan.md](./plan.md)

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md), [data-model.md](./data-model.md), [quickstart.md](./quickstart.md)

**Che cosa questa lista non contiene, e va detto subito.** Nessun task apre Power BI Desktop, nessuno scrive DAX in un file di modello, nessuno tocca un `.pbix`. È la prima feature dalla `007b` per cui questo vale senza eccezioni, ed è una proprietà del perimetro, non una dimenticanza.

**I task di Fase 1 e 2 sono già eseguiti** — sono le Fasi 0 e 1 di `/speckit.plan`, i blocchi A e B del piano. Sono elencati spuntati perché la lista si legga come il registro di ciò che la feature ha fatto, non come la metà che resta.

---

## Fase 1 — Setup

- [x] T001 Aprire il branch `010a-report-disegno` da `main` aggiornato e aggiornare `.specify/feature.json` alla cartella `specs/010a-report-disegno`
- [x] T002 Scrivere la specifica in `specs/010a-report-disegno/spec.md` con le sezioni obbligatorie: domanda di business, provenienza e confidenza, limiti dichiarati
- [x] T003 Scrivere la checklist di qualità in `specs/010a-report-disegno/checklists/requirements.md` e verificarne ogni voce

**Punto di fermata 1** — dopo T003, prima del piano. ✅ superato.

---

## Fase 2 — Fondamenta: le decisioni e l'input della `010b`

**Bloccanti per tutto il resto.** `G1` fissa la direzione della corrispondenza pagina→sezione: ogni pagina disegnata prima di `G1` andrebbe ridisegnata dopo.

- [x] T004 Scrivere le nove decisioni di disegno `G1`-`G9` in `specs/010a-report-disegno/research.md`, ciascuna in forma decisione / motivazione / alternative scartate
- [x] T005 Verificare contro gli artefatti versionati quale materiale sostiene quali visuali, leggendo `reports/kpi_measures.json`, `reports/bq3_scenarios.json` e `data/curated/dim_category_mood.json` in sola lettura
- [x] T006 Scrivere la mappa delle dieci pagine in `specs/010a-report-disegno/data-model.md` §1, con per ciascuna la parte dell'argomento e la sezione di `docs/raccomandazione.md` servita
- [x] T007 Scrivere in `data-model.md` §2 l'elenco delle misure, distinguendo le dieci esistenti, le quattro dichiarate dalla `008a` e le sei nuove, ciascuna con nome, contenuto, tabelle di lettura e pagina richiedente
- [x] T008 Scrivere in `data-model.md` §3 l'elenco delle visuali, distinguendo le quattro nuove dalle quattro riusate, con le due pagine di sola prosa e la visuale che i dati non sostengono
- [x] T009 Scrivere in `data-model.md` §5 i ritrovamenti della fase, e in `quickstart.md` le dodici prove e il censimento delle affermazioni in doppia copia

**Punto di fermata 2** — dopo T009, prima del contratto. Vi si portano: il numero di pagine raggiunto, le decisioni che chiedono conferma, e i tre ritrovamenti.

---

## Fase 3 — Storia 1 (P1): chi costruirà sa che cosa costruire

**Obiettivo**: il contratto di pagina, che è il deliverable. Chi apre la `010b` non deve dedurre nulla.

**Test indipendente**: si prende il contratto senza altro materiale e si conta, pagina per pagina, quante decisioni di contenuto chi costruisce dovrebbe prendere da sé. Zero è l'esito atteso.

- [x] T010 [US1] Scrivere l'intestazione e il perimetro di `specs/010a-report-disegno/contracts/page-contract.md`: che cosa il contratto è (un vincolo, non un accertamento), che cosa non contiene deliberatamente (nessun valore trascritto, nessun testo a schermo), e che cosa non decide
- [x] T011 [US1] Scrivere la sezione 1 del contratto — la mappa delle dieci pagine con la sezione servita da ciascuna, la convenzione di conteggio dichiarata, e la regola `G1` della corrispondenza molti-a-uno
- [x] T012 [US1] Scrivere la sezione 2 del contratto — la regola che governa ogni pagina: invarianza del valore a schermo alla grana pubblicata, selezione incrociata ammessa e filtro vietato
- [x] T013 [P] [US1] Scrivere le sezioni di pagina 1, 2 e 3 del contratto — la domanda, la risposta con il verdetto congiunto di `G5`, e la pagina delle assunzioni `A1` e `A6`
- [x] T014 [P] [US1] Scrivere le sezioni di pagina 4, 5 e 6 del contratto — la prima condizione, la seconda con la visuale `V2` di `G8`, e il margine di `C2` con la visuale `V3` di `G7`
- [x] T015 [P] [US1] Scrivere le sezioni di pagina 7 e 8 del contratto — la regione e la graduatoria, con la chiusura dell'issue `#21` dichiarata secondo `G6`
- [x] T016 [P] [US1] Scrivere le sezioni di pagina 9 e 10 del contratto — gli scenari con la formulazione stretta sull'uplift e il debito della `004` dichiarato, e la pagina delle condizioni di ribaltamento
- [x] T017 [US1] Scrivere la sezione del contratto che elenca le sei misure nuove e le quattro visuali nuove, consumando `data-model.md` §2.3 e §3.1 invece di riprodurlo
- [x] T018 [US1] Scrivere la sezione del contratto che dichiara le tre verifiche dell'issue `#20` da rifare a ogni riapertura, e che l'issue resta aperta
- [x] T019 [US1] Scrivere la sezione del contratto che dichiara dove la `010b` scriverà il proprio testo, pagina per pagina, come spazio riservato e non vuoto
- [x] T020 [US1] Scrivere la sezione finale del contratto — le decisioni che chiedono conferma, sullo schema `CP` della `008a`

---

## Fase 4 — Storia 2 (P1): un decisore incontra un argomento

**Obiettivo**: verificare che la sequenza delle pagine si legga come un discorso e non come un indice.

**Test indipendente**: si legge la sola colonna «parte dell'argomento» della mappa, dall'alto in basso, senza consultare le pagine.

- [x] T021 [US2] Eseguire la prova `P1` di `quickstart.md`: leggere la sola colonna «parte dell'argomento» e verificare che l'ordine coincida con quello delle sezioni di `docs/raccomandazione.md` e non con `BQ1`→`BQ2`→`BQ3`
- [x] T022 [US2] Eseguire la prova `P5`: contare le pagine e verificare che il conteggio stia fra 8 e 12 con la convenzione dichiarata
- [x] T023 [US2] Eseguire le prove `P6`, `P7` e `P8`: la collocazione delle assunzioni `A1` e `A6` su una pagina propria, la formulazione stretta sull'uplift, il debito della `004` dichiarato dove pesa

---

## Fase 5 — Storia 3 (P2): ogni pagina dà all'occhio qualcosa

**Obiettivo**: verificare che nessuna pagina sia una griglia di schede e tabelle, e che le due pagine di sola prosa siano dichiarate con la ragione.

**Test indipendente**: si scorre l'elenco delle visuali pagina per pagina.

- [x] T024 [US3] Eseguire la prova `P4`: verificare che nessuna pagina abbia come soli elementi schede e tabelle, salvo le due dichiarate di sola prosa
- [x] T025 [US3] Verificare che ogni visuale del contratto sia sostenuta da un artefatto che contiene i valori alla grana mostrata, e che la visuale non costruibile sia dichiarata invece di essere taciuta

---

## Fase 6 — Verifica, censimento e revisione

- [x] T026 Eseguire le due prove eseguibili di `quickstart.md` §1: `scripts/check_audit_coherence.py` e la risoluzione degli identificativi di ancora citati dal contratto
- [x] T027 Eseguire le prove `P2` e `P3`: che ogni pagina dichiari le cinque voci obbligatorie, e che nessun valore compaia come cifra trascritta
- [x] T028 Eseguire il censimento delle affermazioni in doppia copia di `quickstart.md` §3, confrontando ciascuna con l'originale **prima** che la revisione cominci
- [x] T029 Compilare l'esito in coda a `quickstart.md` §4 con gli scostamenti e i ritrovamenti, scrivendolo mentre le prove vengono eseguite e non a memoria alla fine
- [ ] T030 Consegnare alla revisione in contesto pulito il perimetro composto secondo il piano — `docs/raccomandazione.md` e il contratto — dichiarando che la domanda verificata è se il disegno regga la spina, non se il contratto si legga da solo
- [ ] T031 Scrivere e committare `specs/010a-report-disegno/review.md` quando la revisione torna, **prima** di toccare il contratto, con i quattro obblighi di `CLAUDE.md`
- [ ] T032 Chiudere i soli rilievi strettamente necessari — quelli senza cui il deliverable afferma il falso o pubblica un valore che non regge — e aprire una issue per ciascun rinvio
- [ ] T033 Scrivere il blocco di chiusura in coda a `review.md`, distinguendo risolto, indebolito e rinviato, e nominando l'issue per ogni rinvio

---

## Fase 7 — Chiusura

- [ ] T034 Allineare `README.md`: riga nella tabella di stato, deliverable elencato, prosa dei deliverable estesa, `Setup` e `Struttura` allineati
- [ ] T035 Riportare alla regia l'esito: quante pagine e quale parte dell'argomento porta ciascuna, quali misure e visuali nuove la `010b` dovrà costruire, quali rilievi chiusi e quali rinviati con i numeri delle issue, e ogni divergenza fra il disegno e ciò che `docs/raccomandazione.md` afferma

---

## Dipendenze

```text
Fase 1 (T001-T003) ──► punto di fermata 1
        │
        ▼
Fase 2 (T004-T009) ──► punto di fermata 2
        │                    │
        │                    └─► le decisioni che chiedono conferma e il numero di pagine
        ▼
Fase 3 (T010-T020) ── il contratto
        │
        ├──► Fase 4 (T021-T023) ── verifica della spina
        └──► Fase 5 (T024-T025) ── verifica delle visuali
                    │
                    ▼
        Fase 6 (T026-T033) ── censimento, revisione, chiusura dei rilievi
                    │
                    ▼
        Fase 7 (T034-T035) ── README ed esito
```

**T028 precede T030 per obbligo, non per comodità.** Il censimento delle copie va eseguito prima che la revisione cominci: è il presidio che la `009` ha usato dopo il ritrovamento della chiusura della `008b`, dove un'affermazione sbagliata esisteva in due copie e il revisore ne aveva ricevuta una sola.

**T031 precede T032 per obbligo.** Il verbale si scrive e si committa quando la revisione torna, prima di toccare l'artefatto. È l'omissione della `004`, e l'ordine dei passi è l'unico presidio contro l'ammorbidimento in trascrizione.

## Esecuzione in parallelo

I quattro task marcati `[P]` — T013, T014, T015, T016 — scrivono sezioni di pagina distinte dello stesso file e non dipendono l'uno dall'altro. Dipendono tutti da T011, che fissa la mappa, e da T012, che fissa la regola che ciascuna sezione cita invece di ripetere.

Le Fasi 4 e 5 sono indipendenti fra loro e possono essere eseguite in qualunque ordine dopo la Fase 3.

## Ambito minimo

**Il contratto senza le sezioni di verifica** — T010 fino a T020 — è già consegnabile alla `010b`: contiene la mappa, le misure, le visuali e le decisioni. Ciò che manca senza le Fasi 4-6 è la garanzia che sia corretto, ed è precisamente ciò che questa feature non può comprimere: il progetto ha già visto un contratto approvato produrre dieci pagine che ripetono un difetto.

**Ciò che non è ambito minimo in nessuna circostanza**: T017, l'elenco delle misure e delle visuali nuove. È l'input su cui poggia la stima della `010b`, la feature più grande mai aperta e la sola rimasta a toccare la GUI. È la parte che si comprimerebbe per prima ed è la peggiore da comprimere.
