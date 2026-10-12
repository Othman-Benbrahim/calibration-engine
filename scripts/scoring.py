#!/usr/bin/env python3
"""
scoring.py — Scores de prévision déterministes pour le skill calibration-engine.

Le LLM ne calcule pas les scores agrégés « de tête » : il appelle ce script.
Bibliothèque standard uniquement.

Entrée : un fichier JSON (liste d'objets) ou CSV avec au minimum les colonnes
  p        probabilité annoncée pour l'événement (0 ≤ p ≤ 1)
  outcome  1 si l'événement s'est produit, 0 sinon
et, en option : id, skill_source, domaine, horizon_jours.

Usage :
  python3 scripts/scoring.py single --p 0.65 --outcome 1
  python3 scripts/scoring.py report predictions.json [--bins 10] [--by skill_source domaine]
  python3 scripts/scoring.py multiclass --probs 0.6 0.25 0.15 --realized 0

Conventions :
  - Brier binaire  BS = (p − o)² ∈ [0, 1] ; toujours dire 0.5 donne 0.25.
  - Log loss en logarithme naturel ; toujours dire 0.5 donne ln 2 ≈ 0.693.
  - Bins de calibration : [0.0, 0.1), [0.1, 0.2), …, [0.9, 1.0] (le dernier inclut 1.0).
  - Décomposition de Murphy (1973) : BS = REL − RES + UNC. Elle est EXACTE quand
    les prévisions sont regroupées par valeur distincte ; avec des bins de largeur
    fixe, un terme résiduel intra-bin apparaît (rapporté séparément).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Record = Dict[str, object]


# ---------------------------------------------------------------------------
# Scores individuels
# ---------------------------------------------------------------------------


def _check(p: float, o: int) -> None:
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"probabilité hors de [0, 1] : {p}")
    if o not in (0, 1):
        raise ValueError(f"outcome doit valoir 0 ou 1 : {o}")


def brier(p: float, o: int) -> float:
    _check(p, o)
    return (p - o) ** 2


def log_loss(p: float, o: int) -> float:
    """Log loss en nats. Infini si l'on annonce 0 ou 1 et que l'on se trompe."""
    _check(p, o)
    q = p if o == 1 else 1.0 - p
    return math.inf if q == 0 else -math.log(q)


def multiclass_brier(probs: Sequence[float], realized: int) -> float:
    """Brier multi-classes (somme sur les classes) ∈ [0, 2]."""
    if abs(sum(probs) - 1.0) > 0.01:
        raise ValueError(f"les probabilités somment à {sum(probs):.4f} ≠ 1")
    if not 0 <= realized < len(probs):
        raise ValueError("indice de la classe réalisée invalide")
    return sum((f - (1.0 if j == realized else 0.0)) ** 2 for j, f in enumerate(probs))


# ---------------------------------------------------------------------------
# Agrégats
# ---------------------------------------------------------------------------


def bin_index(p: float, n_bins: int = 10) -> int:
    """Indice de bin pour des bins de largeur 1/n_bins ; p = 1.0 tombe dans le dernier."""
    return min(int(round(p * n_bins, 9)), n_bins - 1)  # round : évite 0.7*10 = 6.999…


def calibration_table(ps: Sequence[float], os_: Sequence[int], n_bins: int = 10) -> List[Dict[str, object]]:
    groups: Dict[int, List[Tuple[float, int]]] = defaultdict(list)
    for p, o in zip(ps, os_):
        groups[bin_index(p, n_bins)].append((p, o))
    rows = []
    for k in range(n_bins):
        lo, hi = k / n_bins, (k + 1) / n_bins
        g = groups.get(k, [])
        row: Dict[str, object] = {"bin": f"[{lo:.1f}, {hi:.1f}{']' if k == n_bins - 1 else ')'}", "n": len(g)}
        if g:
            fbar = sum(p for p, _ in g) / len(g)
            obar = sum(o for _, o in g) / len(g)
            row.update({"p_moyenne": fbar, "frequence_observee": obar, "ecart": obar - fbar,
                        "lecture": _reading(fbar, obar, len(g))})
        rows.append(row)
    return rows


def _reading(fbar: float, obar: float, n: int, tol: float = 0.10) -> str:
    if n < 5:
        return "effectif trop faible"
    gap = obar - fbar
    if abs(gap) <= tol:
        return "cohérent"
    # Sur-confiance = prévisions trop extrêmes : la fréquence observée est plus
    # proche de 0.5 que la probabilité annoncée.
    if abs(obar - 0.5) < abs(fbar - 0.5):
        return "sur-confiance (prévisions trop extrêmes)"
    return "sous-confiance (prévisions pas assez tranchées)"


def murphy(ps: Sequence[float], os_: Sequence[int], n_bins: Optional[int] = None) -> Dict[str, float]:
    """Décomposition de Murphy (1973).

    n_bins=None : regroupement par valeur de prévision distincte → identité exacte.
    n_bins=k    : bins de largeur fixe → BS = REL − RES + UNC + résidu intra-bin.
    """
    n = len(ps)
    if n == 0:
        raise ValueError("aucune prédiction")
    obar = sum(os_) / n
    groups: Dict[object, List[Tuple[float, int]]] = defaultdict(list)
    for p, o in zip(ps, os_):
        key = p if n_bins is None else bin_index(p, n_bins)
        groups[key].append((p, o))
    rel = res = 0.0
    for g in groups.values():
        nk = len(g)
        fk = sum(p for p, _ in g) / nk
        ok = sum(o for _, o in g) / nk
        rel += nk * (fk - ok) ** 2
        res += nk * (ok - obar) ** 2
    rel /= n
    res /= n
    unc = obar * (1.0 - obar)
    bs = sum(brier(p, o) for p, o in zip(ps, os_)) / n
    return {"brier": bs, "reliability": rel, "resolution": res, "uncertainty": unc,
            "residu_intra_bin": bs - (rel - res + unc)}


def report(records: Sequence[Record], n_bins: int = 10,
           by: Sequence[str] = ()) -> Dict[str, object]:
    ps = [float(r["p"]) for r in records]
    os_ = [int(r["outcome"]) for r in records]
    for p, o in zip(ps, os_):
        _check(p, o)
    n = len(ps)
    if n == 0:
        raise ValueError("aucune prédiction résolue")
    bs = sum(brier(p, o) for p, o in zip(ps, os_)) / n
    ll = sum(log_loss(p, o) for p, o in zip(ps, os_)) / n
    obar = sum(os_) / n
    clim = obar * (1.0 - obar)
    decided = [(p, o) for p, o in zip(ps, os_) if p != 0.5]
    acc = (sum(1 for p, o in decided if (p > 0.5) == (o == 1)) / len(decided)) if decided else None

    out: Dict[str, object] = {
        "n": n,
        "avertissement": _sample_warning(n),
        "brier": bs,
        "log_loss": ll,
        "taux_de_base": obar,
        "baseline_toujours_0_5": 0.25,
        "baseline_taux_de_base": clim,
        "bss_vs_0_5": 1.0 - bs / 0.25,
        "bss_vs_taux_de_base": (1.0 - bs / clim) if clim > 0 else None,
        "sharpness": sum((p - 0.5) ** 2 for p in ps) / n,
        "accuracy_seuil_0_5": acc,
        "exclues_accuracy_p_egal_0_5": n - len(decided),
        "murphy_exact": murphy(ps, os_, None),
        "murphy_bins": murphy(ps, os_, n_bins),
        "calibration": calibration_table(ps, os_, n_bins),
    }
    for key in by:
        groups: Dict[str, List[Record]] = defaultdict(list)
        for r in records:
            groups[str(r.get(key, "inconnu"))].append(r)
        out[f"par_{key}"] = {
            g: {"n": len(rs), "brier": sum(brier(float(r["p"]), int(r["outcome"])) for r in rs) / len(rs),
                "avertissement": _sample_warning(len(rs))}
            for g, rs in sorted(groups.items())
        }
    return out


def _sample_warning(n: int) -> Optional[str]:
    if n < 10:
        return "n < 10 : score brut seulement, aucune conclusion de calibration"
    if n < 30:
        return "n < 30 : échantillon insuffisant pour une calibration robuste"
    return None


# ---------------------------------------------------------------------------
# Entrées / sorties
# ---------------------------------------------------------------------------


def load(path: str) -> List[Record]:
    if path.endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("le JSON doit être une liste d'objets {p, outcome, ...}")
    return data


def _default(o):
    if isinstance(o, float) and math.isinf(o):
        return "inf"
    raise TypeError


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("single")
    s.add_argument("--p", type=float, required=True)
    s.add_argument("--outcome", type=int, required=True)
    r = sub.add_parser("report")
    r.add_argument("path")
    r.add_argument("--bins", type=int, default=10)
    r.add_argument("--by", nargs="*", default=[])
    m = sub.add_parser("multiclass")
    m.add_argument("--probs", type=float, nargs="+", required=True)
    m.add_argument("--realized", type=int, required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "single":
            res = {"brier": brier(args.p, args.outcome), "log_loss": log_loss(args.p, args.outcome)}
        elif args.cmd == "report":
            res = report(load(args.path), args.bins, args.by)
        else:
            res = {"brier_multiclasse": multiclass_brier(args.probs, args.realized), "plage": "[0, 2]"}
    except (ValueError, KeyError) as exc:
        print(json.dumps({"erreur": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=2, default=_default))
    return 0


if __name__ == "__main__":
    sys.exit(main())
