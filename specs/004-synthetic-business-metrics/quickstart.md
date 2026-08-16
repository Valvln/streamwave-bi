# Verifica — come si prova che questa feature funziona

**Feature**: 004 Synthetic Business Metrics · **Data**: 2026-08-16 · **Piano**: [plan.md](./plan.md)

Nessun framework di test (T9): i comportamenti verificabili sono nove e si verificano da riga di comando. Ogni prova dichiara il criterio di successo della spec che chiude.

**Prerequisiti**: Python 3 e nient'altro. Nessuna dipendenza, nessun token Kaggle, **nessuna rete**, e in particolare **nessun `data/raw/`** — se una prova qui sotto richiedesse i dati di origine, sarebbe la prova a essere sbagliata.

---

## Prova 1 — La precedenza dei fattori è nella history *(FR-011a)*

La sola prova che non si esegue: si legge.

```bash
git log --oneline --follow data/benchmarks/bq3_tier_upgrade.json
```

**Atteso**: almeno due commit. Il primo introduce i fattori della banda, il differenziale e la loro ragione; il secondo aggiunge il benchmark e la citazione.

```bash
git show <primo-commit>:data/benchmarks/bq3_tier_upgrade.json \
  | python3 -c "import json,sys; print('benchmark' in json.load(sys.stdin))"
```

**Atteso**: `False`. Nel primo commit la chiave `benchmark` **non esiste**, nemmeno vuota. Un segnaposto renderebbe indistinguibile «fissato prima» da «riempito dopo» e vanificherebbe la garanzia.

**Perché sulla chiave e non sulla parola.** La prova cercava `grep -c benchmark` e attendeva `0`. Non funziona, e la ragione è istruttiva: la prosa di `bq3_band_fixed_before` **deve** nominare il benchmark, perché il suo mestiere è dichiarare che i fattori lo precedono. Un `grep` sulla parola conta le occorrenze che dimostrano la precedenza insieme a quella che la violerebbe. FR-011a parla della chiave, e la prova ora guarda la chiave.

## Prova 2 — La citazione è completa e leggibile senza eseguire nulla *(SC-001, FR-003)*

```bash
cat data/benchmarks/bq3_tier_upgrade.json
```

**Atteso**: si leggono, senza eseguire alcuno script e senza rete, tutti e cinque gli elementi — organizzazione, titolo, data di pubblicazione, riferimento recuperabile, data di accesso — più che cosa la fonte misura, lo scarto rispetto all'uso che se ne fa, l'assunzione di trasferimento, e il registro delle fonti respinte con il motivo.

**Fallisce se**: manca uno dei cinque, oppure la fonte è indicata come «ricerche di settore» o con una formula equivalente.

## Prova 3 — La derivazione gira su una copia pulita *(SC-002, FR-017)*

```bash
git clone --branch 004-synthetic-business-metrics . /tmp/sw-clean && cd /tmp/sw-clean
ls -A data/raw/         # atteso: nessun CSV
python3 scripts/build_bq3_scenarios.py
```

**Atteso**: l'artefatto viene prodotto senza errori, con la rete staccata e senza i dataset di origine.

**Precisazione dovuta all'esecuzione integrale.** `data/raw/` su un clone **non è vuota**: contiene `.gitkeep` e il file di metadati Croissant, che [`data/README.md`](../../data/README.md) dichiara versionato come traccia di provenienza. Ciò che manca sono i due CSV, che è quanto la prova deve accertare. La formulazione precedente — «vuota o assente» — descriveva uno stato che il repository non ha mai avuto.

## Prova 4 — Doppia esecuzione, diff vuoto *(SC-002, FR-013)*

È la prova che conta più di tutte le altre messe insieme.

```bash
python3 scripts/build_bq3_scenarios.py
cp reports/bq3_scenarios.json /tmp/run1.json
python3 scripts/build_bq3_scenarios.py
diff /tmp/run1.json reports/bq3_scenarios.json && echo "DETERMINISTICO"
```

**Atteso**: `DETERMINISTICO`, diff vuoto.

**Fallisce se** l'artefatto contiene un timestamp di esecuzione. Se serve datare, si data la **fonte** — che è un fatto — non l'esecuzione, che è rumore.

## Prova 5 — Nessuna rete, nessun caso *(SC-007, FR-008, FR-013)*

```bash
grep -nE "random|seed|urllib|requests|http|socket|datetime\.now|time\(\)" scripts/build_bq3_scenarios.py
```

**Atteso**: nessuna corrispondenza.

**Perché per ispezione e non per esecuzione**: uno script può girare senza rete e contenere comunque una chiamata su un ramo mai percorso. Qui i rami non ci sono, e l'ispezione è esaustiva proprio per questo.

## Prova 6 — Il benchmark comanda tutti e sei i valori *(SC-003, FR-014)*

```bash
# si altera il solo valore del benchmark nel file dei parametri
python3 scripts/build_bq3_scenarios.py
git diff --stat reports/bq3_scenarios.json
```

**Atteso**: tutti e sei i valori cambiano, più `BQ3.band.spread_pp`. **`BQ3.band.ratio` non cambia**: con banda moltiplicativa vale `(1+k)/(1−k)` qualunque sia il benchmark, ed è una proprietà della stipulazione, non del valore adottato.

**Fallisce se** un valore resta fermo: significa che è stato scritto a mano.

```bash
git checkout data/benchmarks/bq3_tier_upgrade.json && python3 scripts/build_bq3_scenarios.py
```

## Prova 7 — L'aritmetica regge sul confine *(FR-015, F3, T5)*

Il caso costruito apposta, perché è quello che una prova casuale non troverebbe.

```bash
# benchmark temporaneo a 29 punti percentuali: worst = 14,5 · best = 58
# uplift.best = 58 x 4,00 / 100 = 2,32
python3 scripts/build_bq3_scenarios.py
```

**Atteso**: `BQ3.adoption.worst` vale **`15`**, `BQ3.adoption.best` vale `58`, `BQ3.uplift.best` vale `2,32`; ogni `display` riporta la virgola come separatore decimale.

**Perché `worst` e non `best`.** Con fattori reciproci lo scenario ottimista è un prodotto per un intero e non cade mai su un confine di arrotondamento: è il **pessimista** a caderci, perché `29 × 0,50` vale esattamente `14,5`, cioè il punto di mezzo in cui la regola dichiarata deve decidere. Le due<!--#--> insidie convergono lì, e sbagliano nello stesso verso:

- **la virgola mobile** calcola `0,29 × 0,5 × 100` come `14.499999999999998`, cioè il confine visto dal lato sbagliato, e arrotonda a **14**. È il ritrovamento F3;
- **`ROUND_HALF_EVEN`**, la modalità che `Decimal` applica se non gliene si dichiara un'altra, porta `14,5` a **14** perché il quattro è pari.

La risposta corretta è `15`, e ciascuno dei due difetti produrrebbe `14` senza presentarsi come errore: un punto percentuale su un valore pubblicato, dentro un artefatto verde.

*Prima del 2026-08-16 i fattori erano `0,50` e `1,50` e questa prova guardava `best`, dove `29 × 1,5` cadeva su `43,5`. La sostanza non cambia — cambia quale dei due estremi finisce sul confine.*

**Attenzione al ripristino**: il file dei parametri va rimesso com'era e la derivazione rieseguita, altrimenti l'artefatto resta sul valore di prova.

```bash
git checkout data/benchmarks/bq3_tier_upgrade.json && python3 scripts/build_bq3_scenarios.py
```

## Prova 8 — Il controllo di coerenza passa in severità stretta *(SC-004, FR-020)*

```bash
python3 scripts/check_audit_coherence.py
```

**Atteso**: esito verde su **tre** documenti; l'intestazione dichiara i valori dello spazio dei nomi unito su **tre** artefatti; nessuna collisione.

Due prove di alterazione, entrambe da annullare dopo:

```bash
# 1. si cambia una cifra ancorata in docs/bq3_scenarios.md
python3 scripts/check_audit_coherence.py   # atteso: ERRORE con identificativo, atteso e trovato

# 2. si aggiunge una quantita' priva di marcatore
python3 scripts/check_audit_coherence.py   # atteso: ERRORE, non avviso
```

La seconda è la prova che la severità stretta è davvero attiva sul documento nuovo. Un avviso al posto di un errore significa che la voce è entrata in `DOCUMENTS` con la severità sbagliata — e sarebbe passata inosservata, perché l'esito complessivo resterebbe verde.

```bash
python3 scripts/check_audit_coherence.py   # dopo aver annullato: verde
git checkout docs/bq3_scenarios.md
```

## Prova 9 — Il business case è cresciuto per sole aggiunte *(SC-006, FR-030)*

```bash
git diff origin/main -- docs/business_case.md
```

**Atteso**: righe `+` in §2 (`A6`), §6 (il richiamo accanto ad `A1`) e §5.5 (le due note datate). **Nessuna riga `-`** che rimuova un valore o un'affermazione preesistente.

```bash
git diff origin/main -- docs/business_case.md | grep "^-" | grep -v "^---"
```

**Atteso**: nessuna corrispondenza sostanziale.

**Perché `origin/main` e non `main`, e perché la differenza non è cosmetica.** Su un clone `main` **non esiste** come riferimento locale, e `git diff main` termina con `fatal: bad revision 'main'` senza produrre output. La catena `git diff … | grep "^-"` non trova quindi alcuna corrispondenza, e la prova **riporta esito positivo per il fallimento di git anziché per la sua conferma** — cioè il verde ottenuto non verificando nulla, che è precisamente la categoria di difetto contro cui esiste il resto di questo documento. È accaduto alla prima esecuzione integrale di questa lista.

Chi esegue queste prove nel repository di lavoro, dove `main` è un branch locale, non incontra il problema e non ha ragione di sospettarlo: è il motivo per cui la Prova 9 va eseguita sul clone almeno una volta.

E il vincolo di FR-025a e FR-027a, che è l'altro verso della stessa cura:

```bash
git diff main -- docs/business_case.md | grep "^+" | grep -E "[0-9]+[,.][0-9]+"
```

**Atteso**: nessun valore di benchmark e nessuna delle sei cifre derivate. Il differenziale di 4,00 € può comparire **solo** come rimando ad A4, dove già vive, mai riaffermato come numero nuovo.

---

## Che cosa nessuna di queste prove verifica

Vale la pena scriverlo, perché un esito verde su nove prove è persuasivo in un modo che non merita del tutto.

- **che il benchmark sia il valore giusto.** Le prove confrontano documento, artefatto e parametri fra loro. Nessuna guarda il mondo;
- **che l'assunzione di trasferimento regga.** È un'assunzione: non è verificabile con i dati di questo progetto, ed è la ragione per cui la confidenza resta `bassa`;
- **che la fonte adottata sia abbastanza vicina** a ciò per cui viene usata. Non esiste un presidio automatico su quanto adiacente sia troppo — è il motivo per cui FR-006a porta la fonte adottata, con il suo scarto, allo stesso punto di stop del fallimento;
- **che un fatto misurato non sia stato marcato come non-misurato.** Contro la dichiarazione falsa esiste la revisione in contesto pulito, non il controllo (§8 della fonte unica).

Le prime tre si presidiano con il riporto a Valerio, la quarta con la revisione. Nessuna delle quattro con uno script.
