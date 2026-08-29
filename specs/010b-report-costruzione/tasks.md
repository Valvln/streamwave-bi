# Tasks: il report che porta l'argomento a schermo — costruzione

**Feature**: `010b-report-costruzione` | **Data**: 2026-08-29

**Input**: [plan.md](plan.md), [spec.md](spec.md), [data-model.md](data-model.md), [contracts/measures.md](contracts/measures.md), [research.md](research.md), [quickstart.md](quickstart.md)

**Il vincolo che governa tutto**: [`specs/010a-report-disegno/contracts/page-contract.md`](../010a-report-disegno/contracts/page-contract.md)

---

## Come leggere questi task

**Tutti i task che toccano Power BI sono istruzioni per una persona.** Il principio V lo impone: *nessun task può presupporre che un agent pilota quelle GUI*. Dove un task dice «costruire», chi costruisce è Valerio davanti allo schermo.

**Le pagine si costruiscono finite, una alla volta.** Non dieci pagine in bozza da rifinire alla fine. Se il tempo finisse, ciò che deve esistere è un **sottoinsieme di pagine complete**, e la decisione su quali cadano è di Valerio.

**Gli scostamenti si annotano mentre accadono**, nella sezione di esito di [quickstart.md](quickstart.md). Uno scostamento ricostruito a memoria alla fine è una razionalizzazione.

---

## Fase 1 — Ciò che sarà versionato *(prima di aprire Power BI)*

**Obiettivo**: produrre gli artefatti testuali, perché il principio V chiede che tutto ciò che è esprimibile come testo lo sia, e perché **non si scrive prosa guardando lo schermo**.

- [x] T001 Scrivere la ricognizione in `specs/010b-report-costruzione/research.md`, verificando per primo se il contratto di pagina si legge senza `docs/raccomandazione.md` accanto
- [x] T002 Scrivere la spec in `specs/010b-report-costruzione/spec.md` con i limiti dichiarati e il perimetro
- [x] T003 Scrivere il piano in `specs/010b-report-costruzione/plan.md` con il Constitution Check e il Complexity Tracking
- [x] T004 [P] Scrivere `specs/010b-report-costruzione/data-model.md`: che cosa il modello riceve, e che cosa vi si trova già
- [x] T005 [P] Scrivere `specs/010b-report-costruzione/contracts/measures.md`: il DAX letterale delle sei misure nuove e delle tre della `008a` da riscrivere se mancano
- [x] T006 Scrivere le sedici prove in `specs/010b-report-costruzione/quickstart.md`, prima di costruire

**→ PUNTO DI FERMATA 2.** Piano e task tornano a Valerio insieme alle quattro decisioni di §18 del contratto di pagina. **Non si costruisce senza che siano stati visti.**

---

## Fase 2 — La narrazione *(ancora prima di aprire Power BI)*

**Obiettivo**: il testo letterale a schermo, scritto **prima** che il file venga toccato, sul precedente della `008b` — che su questo aveva ragione, ed è la parte del suo lavoro sopravvissuta alla revisione.

- [x] T007 Rileggere i nove rilievi dell'issue [`#29`](https://github.com/Valvln/streamwave-bi/issues/29) come catalogo dei modi in cui la prima narrazione ha fallito, e i nove punti che il §4 di quel verbale dichiara **funzionanti**
- [x] T008 Scrivere la Parte I di `specs/010b-report-costruzione/contracts/narrative-contract.md`: il destinatario, la lista chiusa dei numerali, il registro, e le formulazioni escluse
- [x] T009 [P] Scrivere i blocchi delle pagine 1, 2 e 3 in `contracts/narrative-contract.md`
- [x] T010 [P] Scrivere i blocchi delle pagine 4, 5 e 6 in `contracts/narrative-contract.md`
- [x] T011 [P] Scrivere i blocchi delle pagine 7, 8 e 9 in `contracts/narrative-contract.md`
- [x] T012 [P] Scrivere i blocchi della pagina 10 in `contracts/narrative-contract.md`
- [x] T013 Verificare su `contracts/narrative-contract.md` che **ogni limite abbia accanto ciò che si può concludere nonostante quel limite** (`FR-022`, `SC-002`, issue [`#28`](https://github.com/Valvln/streamwave-bi/issues/28)) — è il conteggio dei limiti orfani, e l'esito atteso è zero
- [x] T014 Verificare su `contracts/narrative-contract.md` che il testo non usi la formulazione «l'uplift non è scalabile» (`FR-024`, issue [`#26`](https://github.com/Valvln/streamwave-bi/issues/26) e [`#31`](https://github.com/Valvln/streamwave-bi/issues/31)) e che i valori di `BQ3` compaiano sempre come terna (`FR-026`)
- [x] T015 Verificare su `contracts/narrative-contract.md` che il debito della `004` sulla verificabilità del benchmark sia dichiarato dove i numeri di `BQ3` compaiono (`FR-025`)

**→ PUNTO DI FERMATA 3.** Il contratto di narrazione è approvato **prima** che il `.pbix` venga toccato.

---

## Fase 3 — Il modello *(davanti allo schermo)*

**Obiettivo**: che ogni misura esista e porti il valore che l'artefatto pubblica, **prima** che qualunque visuale la consumi. Una visuale costruita su una misura non verificata è una visuale da rifare.

- [ ] T016 ★ Aprire il `.pbix` e riverificare le tre impostazioni dell'issue [`#20`](https://github.com/Valvln/streamwave-bi/issues/20), **leggendo l'issue e non una copia**, prima di leggere qualunque valore (prova 1)
- [ ] T017 Verificare che le tre misure della `008a` — le due soglie del quadrante e `c3_high_high_exists` — siano nel modello; se mancano, riscriverle dal testo di `contracts/measures.md` §3 (prova 3)
- [ ] T018 Scrivere `c2_threshold` (`M3`) nel modello, dal testo di `contracts/measures.md` §2.3
- [ ] T019 Scrivere `c2_overlap_above_threshold` (`M2`) nel modello, dal testo di `contracts/measures.md` §2.2
- [ ] T020 Scrivere `c2_margin` (`M4`) nel modello, dal testo di `contracts/measures.md` §2.4
- [ ] T021 Scrivere `c2_margin_share_of_value` (`M5`) nel modello, dal testo di `contracts/measures.md` §2.5
- [ ] T022 Scrivere `verdict_conditions_satisfied` (`M1`) nel modello, dal testo di `contracts/measures.md` §2.1
- [ ] T023 Scrivere `arpu_uplift_per_100k` (`M6`) nel modello, dal testo di `contracts/measures.md` §2.6; se una colonna calcolata risultasse più semplice, è equivalente e **va dichiarato nell'esito**
- [ ] T024 Scrivere `quadrant_members_count` nel modello, dal testo di `contracts/measures.md` §3.3 — è la decisione `CP-4`
- [ ] T025 ★ Confrontare **una volta** la lettura dal motore di ciascuna delle sei misure con il `display` della propria ancora (prova 2). **Una divergenza è un ritrovamento**, da annotare subito nella sezione di esito di `quickstart.md`
- [ ] T026 Verificare che `bq3_scenarios` porti i sei valori senza alcuna relazione con il resto del modello (`FR-029`, prova 4)
- [ ] T027 ★ Verificare `CP-3`: se la selezione si sincronizzi fra le pagine 7 e 8 come **evidenziazione e senza ricalcolare valori** (prova 5). Se ottenibile, rispondere anche all'issue [`#33`](https://github.com/Valvln/streamwave-bi/issues/33) — la riga si evidenzia dov'è, o si porta in vista? Se non ottenibile, l'issue [`#21`](https://github.com/Valvln/streamwave-bi/issues/21) **resta aperta** e diventa un ritrovamento
- [ ] T028 Annotare in `quickstart.md` l'esito di T025 e T027, **mentre accade**

---

## Fase 4 — Le pagine delle tre condizioni *(US1, US2)*

**Obiettivo**: le tre condizioni esistono a schermo, ciascuna con la propria forma. Sono la premessa della pagina 2, che le compone.

**Test indipendente**: si aprono le pagine 4, 5 e 6 e per ciascuna si verifica che porti il valore ancorato, le etichette, il testo, e nessuna delle interazioni vietate.

- [ ] T029 [US1] Costruire la pagina 4 «La prima condizione»: distribuzione delle `42` categorie video ordinata, con la categoria musicale marcata e la mediana come **linea di riferimento letta da misura**; la scheda della North Star riusata invariata; i valori con le etichette; il testo della fascia dal contratto di narrazione
- [ ] T030 [US1] Disattivare sulla pagina 4 tutte le interazioni di §6.1 del contratto di pagina — in particolare **qualunque filtro di categoria video** (issue `#18`), il filtro sul tipo di titolo, il filtro di anno e il drill-down verso i titoli
- [ ] T031 [US1] Costruire la pagina 5 «La seconda condizione»: `V2`, dispersione delle `42` categorie su due dei tre assi di mood con l'inviluppo come rettangolo; la scheda della quota di tracce; i valori con le etichette; il testo della fascia
- [ ] T032 [US1] Dichiarare a schermo sulla pagina 5 l'**asse escluso** e la versione della tabella di mood (`conventions.kpi_mood_table_version`) — `FR-016`
- [ ] T033 [US1] Disattivare sulla pagina 5 tutte le interazioni di §7.1 — in particolare **qualunque filtro di categoria video**, dove il difetto sarebbe *visibile e ingannevole insieme*
- [ ] T034 [US1] Costruire la pagina 6 «Quanto dovrebbe sbagliare»: `V3`, barra orizzontale su asse `0-1` **assoluto**, con il valore misurato, la soglia come riferimento e la distanza etichettata; il margine relativo accanto; il testo della fascia
- [ ] T035 [US1] Verificare che la pagina 6 non porti **alcuna barra di errore, intervallo o banda** attorno al valore, e che la soglia sia marcata come **stipulazione** e non come misura
- [ ] T036 [US1] Disattivare sulla pagina 6 lo slicer che muove la soglia e qualunque filtro (§8.1)

---

## Fase 5 — Le pagine della regione *(US1, US2)*

**Obiettivo**: la regione di ingresso e ciò che contiene, con i presidi che impediscono al disegno di affermare una graduatoria di alternative.

**Test indipendente**: si aprono le pagine 7 e 8 e si verifica che i segmenti a domanda non misurata siano marcati nella dispersione e **fuori ordinamento** nella tabella.

- [ ] T037 [US1] Costruire la pagina 7 «La regione di ingresso»: dispersione dei `114` segmenti riusata **invariata**, con le due linee di riferimento **lette da misura**; l'indicatore booleano di `C3`; il conteggio dei membri del quadrante (`CP-4`); i valori con le etichette; il testo della fascia
- [ ] T038 [US1] Verificare che le tre marcature della dispersione — quadrante, domanda non misurata, resto — restino **distinguibili fra loro** (`FR-017`, §19 del contratto di pagina: è l'unica eccezione al «i colori sono di chi costruisce»)
- [ ] T039 [US1] Disattivare sulla pagina 7 tutte le interazioni di §9.1 — in particolare qualunque filtro su `dim_track` o `fact_track_segment`, che sposterebbe la mediana della domanda
- [ ] T040 [US1] Costruire la pagina 8 «Che cosa la regione contiene»: graduatoria riusata **invariata**, con le sette colonne nell'ordine di §10.1 e la **quota di zeri immediatamente adiacente alla domanda**; il testo della fascia
- [ ] T041 [US1] Costruire sulla pagina 8 il secondo blocco dei sette segmenti a domanda non misurata: **senza colonna di posizione**, ordinato alfabeticamente, con tutte le altre colonne (`FR-018`, §10.2)
- [ ] T042 [US1] Verificare che sulla pagina 8 **nessuna riga sia evidenziata come prima** e che la posizione non riceva rilievo grafico rispetto alle altre colonne (§10.1)
- [ ] T043 [US1] Disattivare sulla pagina 8 tutte le interazioni di §10.4 — in particolare il filtro «prime N posizioni», la possibilità di nascondere la quota di zeri, e l'ordinamento secondario che spareggia i pari merito

---

## Fase 6 — La pagina degli scenari *(US1, US2)*

- [ ] T044 [US1] Costruire la pagina 9 «Quanto vale»: la terna degli scenari riusata **invariata**, due righe e tre colonne più unità; `V4`, la tabella del fattore di conversione con l'unità in intestazione; il testo della fascia
- [ ] T045 [US1] Verificare che nessun valore di `BQ3` compaia **isolato**, nemmeno in una frase di sintesi (`FR-026`), e che nessuna visuale moltiplichi l'uplift per una base utenti
- [ ] T046 [US1] Disattivare sulla pagina 9 lo slicer di scenario che riduce a uno, il campo in cui digitare la base, e **qualunque selezione incrociata con il resto del report** (§11.1)

---

## Fase 7 — La pagina del verdetto *(US1, US2)*

**Perché non è la prima.** Porta la congiunzione di tre condizioni: costruirla prima che le tre esistano significherebbe verificarne il conteggio contro nulla.

- [ ] T047 [US1] Costruire la pagina 2 «La risposta»: `V1`, visuale di stato a tre elementi con il conteggio al centro e le tre condizioni **dentro** l'esito, non accanto; l'esito booleano del verdetto; il testo della fascia
- [ ] T048 [US1] Verificare che la pagina 2 porti **una sola etichetta** di fonte e confidenza, quella del verdetto — `Fonte: Derivato (C1 + C2 + C3) · Confidenza: media` — e che le tre condizioni portino la propria confidenza **dentro** la visuale, subordinata (§4)
- [ ] T049 [US1] Disattivare sulla pagina 2 qualunque filtro e la selezione di una condizione che isola le altre; ammettere il drill-through verso le pagine delle condizioni **come navigazione**, non come filtro (§4.1)

---

## Fase 8 — Le pagine di prosa e la domanda *(US1, US2)*

**Obiettivo**: le tre pagine che non consumano misure. Non sono un vuoto da riempire: ciò che devono dare all'occhio è **struttura**.

- [ ] T050 [US1] Costruire la pagina 1 «La domanda»: il diagramma delle tre condizioni **come struttura senza esiti**; gli elementi di navigazione; il testo della fascia
- [ ] T051 [US1] Verificare che la pagina 1 **non porti alcun valore** e che il diagramma porti i **nomi** delle tre condizioni e non i loro esiti (§3)
- [ ] T052 [US1] Costruire la pagina 3 «Su che cosa poggia»: l'articolazione dei due cataloghi sostitutivi contro i due che il progetto non ha, come **struttura visibile**; i due valori di numerosità con le etichette; `A1` e `A6` con la loro **differenza di portata** mantenuta visibile; il testo, che è l'intera pagina
- [ ] T053 [US1] Costruire la pagina 10 «Che cosa lo ribalterebbe»: l'articolazione **condizione → conseguenza**, una per riga; i limiti dichiarati; il richiamo di `A1` e `A6` **per esteso e non per etichetta** (§12); il valore dell'anno più recente del catalogo video con la propria ancora
- [ ] T054 [US1] Verificare che gli altri due anni — catalogo musicale e benchmark — siano marcati come **non misurati**, e che la differenza di statuto fra i tre non sia appiattita (§12)
- [ ] T055 [US1] Verificare che le pagine 3 e 10 **non abbiano ricevuto alcuna visuale** (`FR-013`, prova 11) — in particolare **nessuna barra dei rischi ordinata per gravità** a pagina 10

---

## Fase 9 — La navigazione *(US1)*

- [ ] T056 [US1] Costruire la barra di navigazione **persistente su tutte e dieci le pagine**, con l'elemento della pagina corrente marcato, le etichette uguali ai titoli di §1, e l'ordine delle dieci pagine visibile
- [ ] T057 [US1] Verificare che da ciascuna pagina si raggiunga ogni altra con **un solo passaggio**, tramite elementi interni al report e non tramite il riquadro delle schede di Power BI (prova 13, `SC-004`)

---

## Fase 10 — Le verifiche finali *(US2, US3)*

- [ ] T058 [US2] Eseguire la prova 7: ogni valore a schermo coincide con il `display` della propria ancora. Ogni divergenza è un **ritrovamento** da dichiarare con nota in loco
- [ ] T059 [US2] Eseguire la prova 8: nessun numero è digitato in una visuale — la mediana di pagina 4, la soglia di pagina 6, le due soglie di pagina 7, i bordi dell'inviluppo di pagina 5 sono **misure lette dal modello**
- [ ] T060 [US2] Eseguire la prova 9: ogni valore porta le due etichette, su ogni pagina, con l'unica eccezione dichiarata della pagina 2
- [ ] T061 [US2] Eseguire la prova 10: nessuna interazione produce una grana non pubblicata, e **nessuna pagina espone un filtro di categoria video** (`FR-030`, issue `#18`)
- [ ] T062 [US2] Eseguire la prova 12: la visuale di §15 **non è stata costruita**
- [ ] T063 [US3] Eseguire la prova 14: il testo a schermo coincide con il contratto di narrazione. Dove diverge, prevale ciò che è a schermo e **lo scostamento si dichiara**
- [ ] T064 [US1] Eseguire la prova 15 a schermo: **zero limiti orfani** (`SC-002`, issue `#28`)

---

## Fase 11 — L'esito, il repository, la revisione

- [ ] T065 Completare la sezione «Esito della costruzione» di `specs/010b-report-costruzione/quickstart.md`: quali pagine esistono e in quale stato, gli scostamenti ciascuno con la propria ragione, i ritrovamenti, l'esito delle quattro decisioni di §18, lo stato delle issue, l'esito delle sedici prove
- [ ] T066 Dichiarare nell'esito **se il contratto di pagina si è letto da solo**, riportando quanto `research.md` `R-1` ha accertato — è la verifica che nessuno aveva fatto prima di questa feature
- [ ] T067 [P] Aggiornare `README.md`: riga nella tabella di stato, deliverable elencato, prosa dei deliverable estesa, `Setup` e `Struttura` allineati (`FR-033`). **Non c'è alcun automatismo**
- [ ] T068 [P] Eseguire `python3 scripts/check_audit_coherence.py` e verificare che sia verde sui documenti che questa feature pubblica o modifica (prova 16)
- [ ] T069 Comporre il perimetro della revisione in contesto pulito, dichiarando **quale domanda si fa verificare**. La difficoltà è strutturale e va detta: il revisore **non potrà vedere il report**, perché il `.pbix` non è versionato. Ciò che riceve è il contratto di narrazione e l'esito
- [ ] T070 Eseguire la revisione in contesto pulito e trascriverne il verbale **integralmente**, non parafrasato, in `specs/010b-report-costruzione/review.md`, con i quattro obblighi di [CLAUDE.md](../../CLAUDE.md)
- [ ] T071 Proporre a Valerio quali rilievi chiudere e quali rinviare, applicando la soglia dello *strettamente necessario*: il deliverable, senza quella correzione, afferma il falso o pubblica un valore che non regge. **Decide Valerio**
- [ ] T072 Scrivere il blocco di chiusura in coda a `review.md`, distinguendo per ciascun rilievo *risolto*, *indebolito* e *rinviato*, e nominando l'issue per ogni rinvio

---

## Dipendenze

```
Fase 1 (artefatti testuali)
   └─→ PUNTO DI FERMATA 2 ─→ Fase 2 (narrazione)
          └─→ PUNTO DI FERMATA 3 ─→ Fase 3 (modello)
                 ├─ T016 ★ prima di qualunque lettura di valore
                 ├─ T025 ★ prima di qualunque visuale
                 └─ T027 ★ presto: cambia ciò che si dichiara, non ciò che si costruisce
                        └─→ Fase 4 (pagine 4, 5, 6)
                               └─→ Fase 5 (pagine 7, 8)
                                      └─→ Fase 6 (pagina 9)
                                             └─→ Fase 7 (pagina 2) — dopo che le tre condizioni esistono
                                                    └─→ Fase 8 (pagine 1, 3, 10)
                                                           └─→ Fase 9 (navigazione) — dopo che le dieci pagine esistono
                                                                  └─→ Fase 10 (verifiche)
                                                                         └─→ Fase 11 (esito, README, revisione)
```

**Le tre dipendenze reali, che non sono preferenze**:

1. **T016 prima di tutto** — un'impostazione riperduta produce un valore diverso **senza segnale**;
2. **T025 prima delle visuali** — una visuale costruita su una misura non verificata è una visuale da rifare;
3. **la pagina 2 dopo le pagine 4, 5, 6** — porta la loro congiunzione.

**Che cosa è parallelizzabile**: i blocchi di narrazione (T009-T012), perché toccano parti diverse dello stesso documento e nessuno dipende dall'altro; e T067-T068, che toccano file diversi.

**Che cosa non lo è, malgrado sembri**: le pagine. Ciascuna si costruisce **finita** prima di passare alla successiva, ed è il presidio contro la compressione distribuita su dieci pagine rifinite a metà.

---

## Strategia di consegna

**Se il tempo bastasse per tutto**: le undici fasi nell'ordine.

**Se il tempo non bastasse** — ed è lo scenario più probabile, dato che entrambe le feature GUI precedenti hanno sforato di quasi il doppio — **la compressione non avviene da sé**. Si riporta a Valerio, e la decisione su che cosa cade è sua.

**Ciò che non deve accadere in nessun caso**: dieci pagine rifinite a metà. Un sottoinsieme di pagine complete è un deliverable; dieci bozze non lo sono.

**L'ordine in cui il valore si accumula**, se servisse a decidere che cosa tenere:

| Sottoinsieme | Che cosa porta |
|---|---|
| Fasi 1-3 | il modello verificato e la narrazione versionata. **Il contratto di narrazione è già un deliverable**: è il testo che un lettore esterno può giudicare |
| + Fasi 4, 7 | le tre condizioni e il verdetto: l'argomento minimo, cioè la risposta e il perché regge |
| + Fasi 5, 6 | la regione e gli scenari: che cosa fare e quanto vale |
| + Fase 8 | i limiti e la premessa sui proxy — **senza cui il principio IV non è soddisfatto** |
| + Fasi 9-11 | la navigazione, le verifiche, la revisione |

**La quarta riga non è rinunciabile a cuor leggero.** Un report che porta la risposta e non i limiti è precisamente l'artefatto che questo progetto ha passato nove feature a non produrre.
