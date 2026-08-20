# Verifica — come si prova che questa feature funziona

**Feature**: 006 Content Taxonomy Bridge · **Data**: 2026-08-20 · **Piano**: [plan.md](./plan.md)

Nessun framework di test (T6, research.md): la maggior parte dei comportamenti verificabili è procedurale — precedenza in history, indipendenza dichiarata, copertura — non aritmetica. Dieci prove, ciascuna dichiara il criterio di successo che chiude.

**Prerequisiti**: Python 3 e nient'altro. Nessuna rete, nessun `data/raw/`: il controllo di coerenza e la lettura degli artefatti curati non li richiedono.

---

## Prova 1 — Il criterio precede ogni valore *(SC-001, US1)*

```bash
git log --oneline --follow docs/mood_assignment_criteria.md
git log --oneline --follow data/curated/dim_category_mood_proposal.json
git log --oneline --follow data/curated/dim_category_mood.json
```

**Atteso**: il primo commit del criterio precede, per timestamp e per posizione in history, il primo commit di entrambi gli altri due file.

```bash
git show <primo-commit-del-criterio>:docs/mood_assignment_criteria.md \
  | grep -E "0[.,][0-9]|1[.,]0" 
```

**Atteso**: nessun valore numerico riconducibile a una cella della tabella — solo gli identificativi `SP.num.*` di ancoraggio (F3, research.md), che non sono valori della tabella di questa feature.

## Prova 2 — Il criterio ancora gli estremi a osservazioni reali, non a titoli *(FR-002, FR-003, FR-004)*

```bash
cat docs/mood_assignment_criteria.md
```

**Atteso**: per ciascuno dei tre assi, un esempio all'estremo basso e uno all'estremo alto, citando gli identificativi `SP.num.energy.min/.max`, `SP.num.valence.min/.max`, `SP.num.danceability.min/.max` o le statistiche aggregate di `reports/data_profile.json`. **Fallisce se** un esempio nomina un titolo, una trama o un cast specifico.

## Prova 3 — La proposta è di un unico modello, invocato manualmente *(SC-005, US2)*

```bash
cat data/curated/dim_category_mood_proposal.json | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(d['model'], d['invoked_at'], len(d['rows']))"

grep -rniE "openai|anthropic|api[._-]?key|requests\.(get|post)|urllib\.request" scripts/
```

**Atteso**: la prima riga stampa modello, data e `42`. La seconda non trova corrispondenze: nessuno script del repository invoca un servizio LLM.

## Prova 4 — Chi verifica non è chi ha ottenuto la proposta *(FR-008, US3)*

```bash
python3 -c "
import json
d = json.load(open('data/curated/dim_category_mood.json'))
print('verificato da:', d['verification']['verified_by'])
print('spostamenti:', d['verification']['changes_count'])
"
```

**Atteso**: `verified_by` è dichiarato e distinto da chi ha ottenuto la proposta (verificabile confrontando con la history git dei due commit). Se `changes_count` è `0`, il campo `zero_changes_note` è presente e lo dichiara come ritrovamento, non come conferma (User Story 3, scenario 3).

## Prova 5 — La tabella copre le 42 categorie, sulla scala corretta *(SC-004, US4)*

```bash
python3 -c "
import json
mood = json.load(open('data/curated/dim_category_mood.json'))
cleaning = json.load(open('reports/cleaning_report.json'))
cats = set(mood['catalogs']['mood_categories'])
expected = set(cleaning['catalogs']['netflix_categories_normalized'])
print('copertura:', len(cats), '/', len(expected))
print('mancanti:', expected - cats)
print('in eccesso:', cats - expected)
for vid, payload in mood['values'].items():
    if vid.startswith('MOOD.category.'):
        v = float(payload['value'])
        assert 0.0 <= v <= 1.0, vid
print('tutti i valori in 0-1: OK')
"
```

**Atteso**: copertura `42/42` (o una differenza dichiarata esplicitamente nel documento pubblicato), nessun valore fuori da `0-1`.

## Prova 6 — Il campo `version` esiste ed è coerente con il numero di correzioni *(FR-015, D5)*

```bash
python3 -c "
import json
d = json.load(open('data/curated/dim_category_mood.json'))
print('version:', d['version'])
assert isinstance(d['version'], int) and d['version'] >= 1
"
```

**Atteso**: intero, a partire da `1`.

## Prova 7 — Il controllo di coerenza fallisce se la tassonomia diverge *(D6, FR-019 — la prova che chiude R2)*

```bash
python3 scripts/check_audit_coherence.py    # atteso: verde prima dell'alterazione

python3 -c "
import json
p = 'data/curated/dim_category_mood.json'
d = json.load(open(p))
d['catalogs']['mood_categories'].pop()   # rimuove una categoria dalla tabella
open(p, 'w').write(json.dumps(d))
"
python3 scripts/check_audit_coherence.py    # atteso: ERRORE — la copertura non coincide con catalogs.netflix_categories_normalized

git checkout data/curated/dim_category_mood.json
python3 scripts/check_audit_coherence.py    # atteso: verde di nuovo
```

**Atteso**: la seconda esecuzione **fallisce** — uscita diversa da zero, non un avviso. È la prova diretta che il presidio della divergenza 5 della `002` è un controllo che ferma, non un promemoria: nessuno deve ricordarsi di eseguirlo, basta che giri.

## Prova 8 — Il controllo passa in severità stretta su cinque documenti e quattro artefatti *(SC-006, FR-023)*

```bash
python3 scripts/check_audit_coherence.py
```

**Atteso**: l'intestazione dichiara **quattro** artefatti uniti; l'esito è verde su **cinque** documenti, incluso `docs/content_taxonomy_bridge.md` in severità stretta.

Due prove di alterazione, entrambe da annullare dopo:

```bash
# 1. si altera una cifra ancorata nel documento pubblicato
python3 scripts/check_audit_coherence.py   # atteso: ERRORE, identificativo/atteso/trovato

# 2. si aggiunge un numero privo di marcatore nel documento pubblicato
python3 scripts/check_audit_coherence.py   # atteso: ERRORE, non avviso — è severità stretta fin dalla nascita
git checkout docs/content_taxonomy_bridge.md
```

## Prova 9 — Nessun attributo di record individuale *(SC-007, FR-020, D7)*

```bash
grep -rn "dim_title\|title_name\|cast\b\|synopsis\|description" \
  docs/mood_assignment_criteria.md \
  docs/content_taxonomy_bridge.md \
  data/curated/dim_category_mood.json \
  data/curated/dim_category_mood_proposal.json
```

**Atteso**: nessuna corrispondenza sostanziale — l'unica occorrenza ammissibile è nella prosa che *dichiara* la regola stessa (per esempio D7 citata nel documento pubblicato), non l'uso della regola violata.

## Prova 10 — Nessuna promozione di confidenza, nessuna etichetta `Benchmark (esterno)` *(SC-005, D3, D4)*

```bash
grep -n "confidenza\|Benchmark (esterno)\|alta" docs/content_taxonomy_bridge.md
```

**Atteso**: ogni menzione della confidenza dei tre KPI dice `media`; nessuna occorrenza di `Benchmark (esterno)` come fonte di questa tabella.

---

## Che cosa nessuna di queste prove verifica

- **che il giudizio dell'analista sia corretto.** Nessuna prova qui valuta se un profilo di mood assegnato a una categoria sia "giusto": è un giudizio, non una misura (Limiti Dichiarati della spec), e la sola difesa possibile è il processo — criterio prima, verifica indipendente, conteggio pubblico — non uno script;
- **che il criterio sia stato scritto senza aver già visto la proposta in mente.** La Prova 1 verifica l'**ordine dei commit**, non lo stato psicologico di chi scrive. È lo stesso limite dichiarato dalla `004` su `bq3_band_fixed_before`: la garanzia vale contro la variante più comune del difetto, non contro tutte;
- **che la revisione in contesto pulito del documento pubblicato (D9.2) sia avvenuta correttamente.** Quella si verifica leggendo `specs/006-content-taxonomy-bridge/review.md`, non da riga di comando — è la Prova implicita nell'User Story 5, non ripetuta qui perché il suo criterio di successo è già in SC-003.
