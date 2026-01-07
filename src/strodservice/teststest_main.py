from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import unittest
from core.calc_engine import calculate_materials_with_gost

class TestCalcEngine(unittest.TestCase):
    def test_calculate_materials_with_gost(self):
        result = calculate_materials_with_gost("Термопласт", 100, 0.15)
        expected = 100 * 0.15 * 0.3  # norm = 0.3
        self.assertAlmostEqual(result, expected, places=2)

if __name__ == "__main__":
    unittest.main()