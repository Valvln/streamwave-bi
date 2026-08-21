# Contratto: cosa `007b` può presupporre leggendo `docs/kpi_operators.md`

**Feature**: 007a-kpi-operators | **Data**: 2026-08-21

Non è un'interfaccia software — questa feature non espone API, CLI o schemi di scambio dati. È il contratto di lettura fra due feature in sequenza: cosa `007b` (implementazione DAX) può dare per garantito leggendo `docs/kpi_operators.md` senza dover riaprire alcuna revisione precedente (SC-006), e cosa resta invece a suo carico.

## Cosa il documento garantisce

1. **Un operatore completo per ciascuno dei sei KPI di `BQ1`/`BQ2`** (`BQ1-K1`, `BQ1-K2`, `BQ1-K3`, `BQ2-K1`, `BQ2-K2`, `BQ2-K3`): formula, grana, provenienza dal modello dati, confidenza ereditata, limiti dichiarati — sufficienti a scrivere la misura DAX senza decisioni analitiche residue (FR-001–FR-013b, SC-001, SC-006).
2. **Nessuna decisione analitica implicita.** Le nove decisioni (D1-D9) coprono per intero le sette lacune ereditate più le due voci minori; `007b` non deve scegliere fra letture alternative di alcuna scheda di `business_case.md` §5.5.
3. **Ogni numero citato è un input, non un risultato.** `007b` non trova in questo documento alcun valore dei KPI (FR-019, SC-002) — solo dati già ancorati da feature precedenti, usati come esempio per argomentare un operatore.
4. **La confidenza di ciascun KPI è quella già fissata da `business_case.md` §5.4**, mai promossa (FR-015, SC-005) — `007b` eredita la stessa classificazione senza doverla riverificare.
5. **I limiti strutturali introdotti dagli operatori stessi sono dichiarati esplicitamente** (D1: stima per eccesso; D2: distanza non interpretabile in assoluto) — `007b` non li scopre a implementazione avvenuta.

## Cosa il documento non garantisce, e resta a carico di `007b`

1. **Che l'operatore sia esprimibile in DAX senza adattamento.** Un limite del linguaggio che rendesse un operatore non implementabile come definito è un ritrovamento della `007b`, da registrare con nota in loco su `docs/kpi_operators.md` (Assumptions di spec.md) — non una libertà di deviare in silenzio.
2. **Che i valori risultanti siano corretti.** Un operatore ben argomentato riduce l'arbitrarietà della formula, non l'incertezza del risultato (Limiti Dichiarati di spec.md) — la verifica contro un motore reale resta compito della `007b` e della sua propria revisione.
3. **Che la versione 2 della tabella dei mood (dopo la chiusura di `CF-1`) non richieda un adattamento.** Gli operatori presuppongono solo la stabilità degli assi e degli estremi ancorati, non dei valori delle celle — `007b` applica gli stessi operatori alla versione 2 senza tornare a `007a`, ma deve verificare che gli estremi non siano anch'essi cambiati (Assumptions di spec.md).
4. **Il conteggio dei titoli per categoria (C1, D9.2) e qualunque altro conteggio che questa feature dichiara come "non oggi pubblicato".** `007b` li produce; `007a` fornisce solo l'operatore con cui calcolarli.

## Come si verifica che il contratto è rispettato

Le due direzioni si verificano diversamente: che `007a` abbia scritto un documento completo si verifica con [quickstart.md](../quickstart.md); che `007b` lo abbia letto correttamente si verifica quando quella feature aprirà la propria spec e dichiarerà, KPI per KPI, quale voce di `docs/kpi_operators.md` implementa — non è verificabile da questa feature, che si ferma alla pubblicazione del documento.
