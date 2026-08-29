# Come si verifica ciò che questa feature produce

Tre verifiche meccaniche e una che nessuna macchina può fare. L'ultima è quella che conta di più, ed è la ragione per cui questa pagina la elenca invece di fermarsi ai comandi.

---

## Prerequisiti

| Verifica | Richiede `data/raw/` | Richiede `data/processed/` | Richiede una licenza Power BI |
|---|---|---|---|
| 1 — rigenerazione dell'artefatto | no | **sì** | no |
| 2 — determinismo | no | **sì** | no |
| 3 — coerenza delle ancore | no | no | no |
| 4 — revisione in contesto pulito | no | no | no |

Chi clona il repository senza i dati di origine esegue la **3** e la **4**: sono le due che verificano che i numeri dei documenti non siano stati scritti a mano. Per la **1** e la **2** servono i dataset trasformati, che si ricostruiscono con `scripts/download_data.sh` e `scripts/build_datasets.py`.

---

## 1. La catena rigenera l'artefatto

```bash
python3 scripts/build_kpi_measures.py
```

**Esito atteso**: lo script stampa il numero di valori scritti e l'elenco delle voci non-per-segmento, ora comprensivo delle sei voci nuove.

**Che cosa guardare oltre all'uscita zero:**

- `KPI.BQ1K3.c2.threshold`, `.c2.satisfied`, `.c2.margin`, `.c2.margin_share_of_value` esistono;
- `KPI.verdict.conditions_satisfied` e `KPI.verdict.all_satisfied` esistono;
- la convenzione `kpi_decision_rule` è presente fra le altre sei;
- **nessun valore preesistente è cambiato.** È la verifica che conta di più in questo passo: la feature aggiunge, non modifica. Un valore che si muove è un ritrovamento da dichiarare, non un aggiornamento da accettare.

Il confronto con lo stato precedente si fa così, prima di rigenerare:

```bash
git stash list >/dev/null  # promemoria: l'artefatto è versionato, quindi
git diff --stat reports/kpi_measures.json
```

Un diff che tocca **solo** righe aggiunte è l'esito atteso. Un diff che modifica una riga esistente va investigato prima di procedere.

---

## 2. Il determinismo

```bash
python3 scripts/build_kpi_measures.py
sha256sum reports/kpi_measures.json    # su macOS: shasum -a 256
python3 scripts/build_kpi_measures.py
sha256sum reports/kpi_measures.json
```

**Esito atteso**: le due impronte coincidono. Nessuna lettura dell'orologio, nessun generatore casuale, nessuna chiamata di rete: due esecuzioni consecutive producono un file identico byte per byte.

**Che cosa questo garantisce, e che cosa no.** Garantisce che il file non contenga rumore di esecuzione. Non garantisce che i valori siano giusti: uno script deterministico sbaglia in modo deterministico.

---

## 3. La coerenza fra documenti e artefatti

```bash
python3 scripts/check_audit_coherence.py
```

**Esito atteso**: stato 0, con otto documenti scanditi — i sette esistenti più `docs/raccomandazione.md` — di cui sette in severità stretta.

**Che cosa l'esito verde certifica**: che ogni numero ancorato coincide con il valore dell'artefatto che lo produce, che nessun riferimento è irrisolvibile, che nessun marcatore è malformato, e che le categorie della tabella dei mood coincidono ancora con quelle del catalogo video.

**Che cosa non certifica**, ed è dichiarato in `convenzioni-marcatura.md` §8:

- non si accorge di un'affermazione che **avrebbe dovuto** essere ancorata;
- non impedisce che un fatto misurato venga marcato come non-misurato;
- **non vede le quantità espresse per frazione o ordinale in lettere** — «la metà», «la maggioranza», «un terzo». In questo documento quella zona è più larga del solito, perché la maggioranza è il concetto su cui `C2` è definita;
- non verifica alcuna argomentazione, che è la sostanza del deliverable.

---

## 4. La revisione in contesto pulito

Non è un comando ed è la verifica principale.

**L'oggetto**: `docs/raccomandazione.md`, che è il documento che un lettore esterno riceverà.

**Il perimetro**, e qui c'è una differenza rispetto alle revisioni precedenti che va composta con cura. Le revisioni di questo progetto hanno finora consegnato **il solo artefatto**, ed è ciò che rende la lettura pulita. Qui il ritrovamento della chiusura della `008b` impone un'aggiunta: una revisione su estratti isolati **non può per costruzione** vedere che un'affermazione esiste in due copie divergenti. La raccomandazione ripete per progetto affermazioni che vivono già in `business_case.md`, `kpi_measures.md` e `bq3_scenarios.md`.

Il perimetro va quindi composto in modo che il revisore possa confrontare le copie, e il verbale deve dichiarare **che cosa ha ricevuto e che cosa no** — è il secondo dei quattro obblighi di `CLAUDE.md`, e qui serve più che altrove perché il perimetro non è quello consueto.

**Che cosa la revisione deve poter dire**, oltre ai rilievi: se un decisore che non ha letto nulla, leggendo il solo deliverable, **conclude qualcosa**. È il metro che la `008b` si era data e su cui è stata fermata.

**La regola di chiusura** (2026-08-22): si chiudono dentro la feature **solo** i rilievi senza cui il deliverable afferma il falso o pubblica un valore che non regge. Tutto il resto va sul tracker con un numero, e il blocco di chiusura lo dichiara come rinvio distinguendolo da *risolto* e da *indebolito*.

---

## 5. Che cosa questa feature non permette di verificare

- **Che il verdetto sia vero per StreamWave.** Poggia su cataloghi proxy, e l'assunzione `A1` non è verificabile con i dati disponibili. L'ancora garantisce l'origine di un numero, non la sua verità;
- **che la sovrapposizione reale sia vicina alla stima.** Il margine dice quanto la stima dovrebbe sbagliare perché la conclusione cambi, non quanto sbagli;
- **che il benchmark di `BQ3` regga.** La verifica esterna consiste nell'aprire il comunicato citato, e resta fuori dalla portata di qualunque comando di questo repository (`bq3_scenarios.md` §9);
- **che le formule `C1` e `C3` diano nel motore DAX gli stessi valori.** Quello è il confronto `E9` della `007b`, già eseguito e congelato in `reports/kpi_engine_check.json`. Questa feature non lo rifà e non ne aggiunge uno per `C2`, che non riceve una formula DAX — la ragione sta in Complexity Tracking del piano.
