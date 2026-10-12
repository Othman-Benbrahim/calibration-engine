"""Tests de non-régression des métriques du calibration-engine.

Lancer :  python3 -m unittest discover -s tests -v   (depuis la racine du skill)
"""
import math
import os
import random
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import scoring  # noqa: E402


class TestScoresIndividuels(unittest.TestCase):
    def test_exemples_documentes(self):
        self.assertAlmostEqual(scoring.brier(0.65, 1), 0.1225)          # SKILL.md MODE 2
        self.assertAlmostEqual(scoring.brier(0.55, 0), 0.3025)          # format-log-externe.md
        self.assertAlmostEqual(scoring.log_loss(0.65, 1), 0.431, places=3)
        self.assertAlmostEqual(scoring.log_loss(0.55, 0), 0.799, places=3)
        self.assertAlmostEqual(scoring.log_loss(0.95, 0), 2.996, places=3)
        self.assertAlmostEqual(scoring.brier(0.95, 0), 0.9025)

    def test_moyenne_exemple(self):
        ps, os_ = [0.8, 0.8, 0.2, 0.5], [1, 0, 0, 1]
        self.assertAlmostEqual(sum(scoring.brier(p, o) for p, o in zip(ps, os_)) / 4, 0.2425)

    def test_bornes_brier(self):
        self.assertEqual(scoring.brier(1.0, 1), 0.0)
        self.assertEqual(scoring.brier(0.0, 1), 1.0)   # pire cas = 1, pas 0.5
        self.assertEqual(scoring.brier(1.0, 0), 1.0)
        self.assertEqual(scoring.brier(0.5, 0), 0.25)
        self.assertEqual(scoring.brier(0.5, 1), 0.25)

    def test_log_loss_baseline_et_infini(self):
        self.assertAlmostEqual(scoring.log_loss(0.5, 1), math.log(2))
        self.assertTrue(math.isinf(scoring.log_loss(1.0, 0)))

    def test_multiclasse(self):
        self.assertAlmostEqual(scoring.multiclass_brier([1, 0, 0], 1), 2.0)   # borne max = 2
        self.assertAlmostEqual(scoring.multiclass_brier([0.6, 0.25, 0.15], 0), 0.16 + 0.0625 + 0.0225)


class TestMurphy(unittest.TestCase):
    def test_identite_exacte_par_valeur(self):
        rnd = random.Random(42)
        ps = [round(rnd.random(), 2) for _ in range(300)]
        os_ = [1 if rnd.random() < p else 0 for p in ps]
        m = scoring.murphy(ps, os_, None)
        self.assertAlmostEqual(m["brier"], m["reliability"] - m["resolution"] + m["uncertainty"], places=12)
        self.assertAlmostEqual(m["residu_intra_bin"], 0.0, places=12)

    def test_residu_avec_bins_fixes(self):
        ps = [0.11, 0.19, 0.11, 0.19]
        os_ = [0, 1, 0, 1]
        m = scoring.murphy(ps, os_, 10)
        self.assertNotAlmostEqual(m["residu_intra_bin"], 0.0, places=6)

    def test_reliability_atteint_1(self):
        m = scoring.murphy([1.0, 1.0, 1.0], [0, 0, 0], None)
        self.assertAlmostEqual(m["reliability"], 1.0)   # borne sup = 1, pas 0.25

    def test_bornes_resolution_incertitude(self):
        m = scoring.murphy([0.0, 1.0, 0.0, 1.0], [0, 1, 0, 1], None)
        self.assertAlmostEqual(m["resolution"], 0.25)
        self.assertAlmostEqual(m["uncertainty"], 0.25)

    def test_toujours_05_calibre_seulement_si_equilibre(self):
        m = scoring.murphy([0.5] * 10, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], None)
        self.assertAlmostEqual(m["reliability"], 0.16)  # (0.5 - 0.1)², pas 0
        self.assertAlmostEqual(m["resolution"], 0.0)


class TestBins(unittest.TestCase):
    def test_bornes_des_bins(self):
        self.assertEqual(scoring.bin_index(0.0), 0)
        self.assertEqual(scoring.bin_index(0.1), 1)
        self.assertEqual(scoring.bin_index(0.7), 7)
        self.assertEqual(scoring.bin_index(0.95), 9)
        self.assertEqual(scoring.bin_index(1.0), 9)

    def test_dix_bins_couvrent_0_1(self):
        t = scoring.calibration_table([0.05, 0.97, 1.0], [0, 1, 1])
        self.assertEqual(len(t), 10)
        self.assertEqual(t[-1]["bin"], "[0.9, 1.0]")
        self.assertEqual(t[-1]["n"], 2)

    def test_sens_de_la_surconfiance(self):
        # Dire 0.20 et observer 0.30 : prévision trop extrême → sur-confiance
        self.assertTrue(scoring._reading(0.20, 0.35, 20).startswith("sur-confiance"))
        # Dire 0.80 et observer 0.65 : sur-confiance aussi
        self.assertTrue(scoring._reading(0.80, 0.65, 20).startswith("sur-confiance"))
        # Dire 0.80 et observer 0.95 : sous-confiance
        self.assertTrue(scoring._reading(0.80, 0.95, 20).startswith("sous-confiance"))


class TestRapport(unittest.TestCase):
    def test_baselines_et_bss(self):
        recs = [{"p": 0.5, "outcome": o} for o in [1, 0, 0, 0]]
        r = scoring.report(recs)
        self.assertAlmostEqual(r["brier"], 0.25)            # 0.5 donne 0.25 quel que soit l'équilibre
        self.assertAlmostEqual(r["baseline_taux_de_base"], 0.1875)
        self.assertLess(r["bss_vs_taux_de_base"], 0)        # pire que le taux de base
        self.assertEqual(r["exclues_accuracy_p_egal_0_5"], 4)

    def test_fixture_exemple(self):
        recs = scoring.load(os.path.join(HERE, "fixtures", "exemple-rapport.json"))
        r = scoring.report(recs, by=["skill_source", "domaine", "horizon"])
        self.assertEqual(r["n"], 44)
        self.assertAlmostEqual(r["brier"], 0.2032, places=4)
        for key in ("par_skill_source", "par_domaine", "par_horizon"):
            self.assertEqual(sum(v["n"] for v in r[key].values()), r["n"])
            pooled = sum(v["n"] * v["brier"] for v in r[key].values()) / r["n"]
            self.assertAlmostEqual(pooled, r["brier"], places=12)
        m = r["murphy_exact"]
        self.assertAlmostEqual(m["reliability"] - m["resolution"] + m["uncertainty"], r["brier"], places=12)


if __name__ == "__main__":
    unittest.main()
