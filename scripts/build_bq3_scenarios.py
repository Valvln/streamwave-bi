#!/usr/bin/env python3
"""Derivazione dei parametri di scenario della terza domanda di business.

Legge `data/benchmarks/bq3_tier_upgrade.json` -- curato a mano, versionato, mai
riscritto da questo script -- e produce `reports/bq3_scenarios.json`, che
contiene sei valori di scenario piu' due affermazioni derivate.

Che cosa questo script **non** e': un generatore. Non esiste alcuna estrazione
casuale, e non e' una semplificazione ma una conseguenza. La base utenti di
StreamWave non e' quantificata (divergenza 9 della revisione 001), quindi non
esiste alcun N da cui estrarre; nessun consumatore a valle legge righe; e una
banda dichiarata come fiducia dell'analista non guadagna nulla a essere
campionata. La derivazione e' percio' deterministica per costruzione: nessun
generatore casuale, nessuna lettura dell'orologio, nessun contatto con l'esterno
(FR-013, FR-008). Due esecuzioni consecutive producono file identici.

L'aritmetica sta tutta in `decimal.Decimal` e mai in virgola mobile. Non e'
pedanteria: `0,29 x 1,5` in virgola mobile vale `0.43499999999999994`, cioe' il
confine di arrotondamento visto dal lato sbagliato, e produrrebbe una cifra
sbagliata dentro un artefatto verde (ritrovamento F3 di research.md).

I numeri escono come **stringhe**, come entrano. Un consumatore che li rilegga
non deve poter reintrodurre per disattenzione il difetto che l'ingresso evita.

Uso:
    python3 scripts/build_bq3_scenarios.py
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PARAMS = REPO / "data" / "benchmarks" / "bq3_tier_upgrade.json"
OUT = REPO / "reports" / "bq3_scenarios.json"

SCHEMA_VERSION = 1

RATE_UNIT = "punti percentuali della base"
MONEY_UNIT = "euro per utente al mese"

SCENARIOS = ("worst", "base", "best")
SCENARIO_LABEL = {
    "worst": "scenario pessimista",
    "base": "scenario centrale",
    "best": "scenario ottimista",
}

# La regola di arrotondamento e' dichiarata qui e ripubblicata fra le
# convenzioni dell'artefatto: chi rifa' il conto a mano deve sapere quale
# regola applicare senza aprire questo file (FR-015, decisione T5).
ROUNDING_RULE = (
    "ROUND_HALF_UP, dichiarato esplicitamente e non la modalita' predefinita di "
    "decimal.Decimal, che e' ROUND_HALF_EVEN. Due famiglie di valori. I tassi in "
    "punti percentuali -- BQ3.adoption.* e BQ3.band.spread_pp -- si pubblicano "
    "alle cifre significative del benchmark, al piu' due. Gli importi in euro -- "
    "BQ3.uplift.* -- si pubblicano a due posizioni decimali fisse, che sono la "
    "convenzione con cui si scrive una valuta e non una pretesa di precisione: la "
    "precisione effettiva degli importi resta quella del benchmark, cioe' due "
    "cifre significative, e 1,20 EUR non va letto come una conoscenza a tre. "
    "BQ3.band.ratio non discende dal benchmark ed e' esatto per costruzione. "
    "Tutta l'aritmetica in decimal.Decimal, mai in virgola mobile."
)


# ===========================================================================
# Lettura dei parametri
# ===========================================================================

def read_parameters() -> dict:
    """Legge il file dei parametri. Non lo scrive e non lo riscrive mai."""
    if not PARAMS.exists():
        raise SystemExit(
            f"ERRORE: file dei parametri mancante: {PARAMS.relative_to(REPO)}\n"
            f"        E' versionato e curato a mano: non viene rigenerato da "
            f"alcuno script, e su una copia pulita deve semplicemente esserci."
        )
    params = json.loads(PARAMS.read_text(encoding="utf-8"))
    for block in ("band", "price", "benchmark"):
        if block not in params:
            raise SystemExit(
                f"ERRORE: blocco «{block}» assente dal file dei parametri.\n"
                f"        La derivazione non ha i propri ingressi e si ferma."
            )
    return params


# ===========================================================================
# Arrotondamento e presentazione
# ===========================================================================

def to_significant(value: Decimal, digits: int) -> Decimal:
    """Arrotonda a un numero di cifre significative, con ROUND_HALF_UP."""
    if value == 0:
        return Decimal(0)
    exponent = value.adjusted()
    quantum = Decimal(1).scaleb(exponent - digits + 1)
    rounded = value.quantize(quantum, rounding=ROUND_HALF_UP)
    # Un arrotondamento puo' guadagnare una cifra: 9,95 a due cifre da' 10,0,
    # che ne porta tre. In quel caso si riquantizza sull'esponente nuovo.
    if rounded.adjusted() != exponent:
        quantum = Decimal(1).scaleb(rounded.adjusted() - digits + 1)
        rounded = value.quantize(quantum, rounding=ROUND_HALF_UP)
    return rounded


def to_money(value: Decimal) -> Decimal:
    """Porta un importo a due posizioni decimali fisse, con ROUND_HALF_UP."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def strip_zeros(value: Decimal) -> Decimal:
    """Toglie gli zeri decimali non significativi senza passare a notazione
    esponenziale, che `normalize()` da solo introdurrebbe su 30 -> 3E+1."""
    stripped = value.normalize()
    if stripped.as_tuple().exponent > 0:
        stripped = stripped.quantize(Decimal(1))
    return stripped


def display_of(value: Decimal) -> str:
    """Formattazione esplicita con la virgola decimale italiana.

    Mai una funzione dipendente dal locale: sulla macchina di chi sviluppa
    darebbe il risultato giusto per caso (vincolo ereditato da F6 della 003).
    """
    return format(value, "f").replace(".", ",")


# ===========================================================================
# La guardia dell'intervallo (FR-016)
# ===========================================================================

def guard_rate(name: str, value: Decimal, factor_high: Decimal) -> None:
    """Ferma la derivazione se un tasso cade fuori da 0-100.

    Il messaggio **instrada l'uscita** invece di limitarsi a fermare: chi lo
    incontra lo incontra a commit gia' fatti, e non deve essere costretto a
    dedurre da solo che l'uscita esiste (T19 dei task).
    """
    if Decimal(0) <= value <= Decimal(100):
        return
    ceiling = to_significant(Decimal(100) / factor_high, 4)
    raise SystemExit(
        f"ERRORE: {name} vale {value} e cade fuori dall'intervallo 0-100.\n"
        f"        La derivazione si ferma e non scrive alcun artefatto: meglio\n"
        f"        nessun file che un file parziale (FR-016).\n"
        f"\n"
        f"        Perche' accade. Lo scenario ottimista vale benchmark per "
        f"{factor_high}, quindi\n"
        f"        esce da 0-100 per qualunque benchmark oltre il {display_of(ceiling)}%. "
        f"I fattori della\n"
        f"        banda sono fissati prima della ricognizione (FR-011a), quindi "
        f"questa\n"
        f"        incompatibilita' e' scopribile solo qui, a commit gia' fatti.\n"
        f"\n"
        f"        L'uscita esiste gia' dentro FR-011a: i fattori possono cambiare "
        f"dopo la\n"
        f"        ricognizione, purche' il cambiamento sia **dichiarato con la "
        f"propria\n"
        f"        ragione** in data/benchmarks/bq3_tier_upgrade.json, sotto "
        f"bq3_band_fixed_before.\n"
        f"        Non applicarlo in silenzio: la banda e' l'unico numero libero "
        f"della feature,\n"
        f"        ed e' la sola cosa che nessun controllo di questo progetto puo' "
        f"presidiare."
    )


# ===========================================================================
# La catena di derivazione
# ===========================================================================

def derive(params: dict) -> dict:
    """Gli otto valori, tutti discendenti dai tre ingressi.

    Nessun ramo, nessun caso speciale, nessun valore scritto a mano: cambiare
    il benchmark e rieseguire li muove tutti (FR-014). L'unica eccezione e'
    `band.ratio`, che dipende dai soli fattori e vale (1+k)/(1-k) qualunque sia
    il benchmark -- ed e' una proprieta' della stipulazione, non del valore.
    """
    factor_low = Decimal(params["band"]["bq3_band_factor_low"])
    factor_high = Decimal(params["band"]["bq3_band_factor_high"])
    price_delta = Decimal(params["price"]["bq3_price_delta_eur"])
    benchmark = Decimal(params["benchmark"]["bq3_benchmark_value"])
    digits = int(params["benchmark"]["bq3_benchmark_significant_digits"])

    exact_adoption = {
        "worst": benchmark * factor_low,
        "base": benchmark,
        "best": benchmark * factor_high,
    }
    for scenario in SCENARIOS:
        guard_rate(f"BQ3.adoption.{scenario}", exact_adoption[scenario], factor_high)

    exact_uplift = {
        scenario: exact_adoption[scenario] * price_delta / Decimal(100)
        for scenario in SCENARIOS
    }

    # Le due affermazioni derivate esistono perche' un confronto costruito su
    # valori misurati e' esso stesso un valore misurato: o ha un identificativo
    # proprio, o non si scrive (FR-031, regola D5 del metodo di progetto).
    # Si calcolano sui valori **esatti** e non su quelli gia' arrotondati: il
    # rapporto e' esatto per costruzione e arrotondare prima lo sporcherebbe.
    exact_spread = exact_adoption["best"] - exact_adoption["worst"]
    exact_ratio = exact_adoption["best"] / exact_adoption["worst"]

    values: dict = {}
    for scenario in SCENARIOS:
        rate = to_significant(exact_adoption[scenario], digits)
        values[f"BQ3.adoption.{scenario}"] = {
            "display": display_of(rate),
            "value": str(rate),
            "label": f"tasso di adozione del tier premium, {SCENARIO_LABEL[scenario]}",
            "unit": RATE_UNIT,
            "scenario": scenario,
        }
        money = to_money(exact_uplift[scenario])
        values[f"BQ3.uplift.{scenario}"] = {
            "display": display_of(money),
            "value": str(money),
            "label": (
                "variazione del ricavo medio per utente, "
                f"{SCENARIO_LABEL[scenario]}"
            ),
            "unit": MONEY_UNIT,
            "scenario": scenario,
        }

    spread = to_significant(exact_spread, digits)
    values["BQ3.band.spread_pp"] = {
        "display": display_of(spread),
        "value": str(spread),
        "label": "ampiezza della banda di adozione, fra scenario ottimista e pessimista",
        "unit": "punti percentuali",
    }

    ratio = strip_zeros(exact_ratio.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    values["BQ3.band.ratio"] = {
        "display": display_of(ratio),
        "value": str(ratio),
        "label": (
            "rapporto fra scenario ottimista e pessimista; dipende dai soli "
            "fattori della banda e non dal benchmark"
        ),
        "unit": "rapporto",
    }
    return values


# ===========================================================================
# Scrittura dell'artefatto
# ===========================================================================

def fingerprint(path: Path) -> dict:
    """Impronta del file dei parametri: l'artefatto dichiara da quale versione
    dell'ingresso discende, senza doverne ricopiare il contenuto."""
    payload = path.read_bytes()
    return {
        "file": str(path.relative_to(REPO)),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }


def build_artifact(params: dict, values: dict) -> dict:
    # Tutte le chiavi di `conventions` portano il prefisso `bq3_`. Lo spazio dei
    # nomi e' **piatto** e condiviso fra artefatti, e `rounding_decimals` e' gia'
    # occupato da un'altra feature con contenuto diverso: una convenzione senza
    # prefisso collide, nel caso migliore rumorosamente (ritrovamento F2).
    return {
        "conventions": {
            "bq3_band_factor_low": params["band"]["bq3_band_factor_low"],
            "bq3_band_factor_high": params["band"]["bq3_band_factor_high"],
            "bq3_band_meaning": params["band"]["bq3_band_meaning"],
            "bq3_band_fixed_before": params["band"]["bq3_band_fixed_before"],
            "bq3_price_delta_eur": params["price"]["bq3_price_delta_eur"],
            "bq3_rounding": ROUNDING_RULE,
        },
        "schema_version": SCHEMA_VERSION,
        "sources": [fingerprint(PARAMS)],
        "values": values,
    }


def write_artifact(artifact: dict) -> None:
    # Nessuna marca temporale di esecuzione: se serve datare, si data la fonte,
    # che e' un fatto, non l'esecuzione, che e' rumore. E' la condizione perche'
    # due esecuzioni consecutive diano un diff vuoto (FR-013).
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(artifact, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> None:
    params = read_parameters()
    values = derive(params)
    write_artifact(build_artifact(params, values))
    print(f"Scritto {OUT.relative_to(REPO)}: {len(values)} valori.")
    for vid in sorted(values):
        entry = values[vid]
        print(f"  {vid:<24} {entry['display']:>6}  {entry['unit']}")


if __name__ == "__main__":
    main()
