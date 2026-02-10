from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALC_DIR = ROOT / "calculator_implementations"
EVAL_DIR = ROOT / "evaluation"

# Ensure calculator and evaluation modules can be imported by their local names.
for path in (str(CALC_DIR), str(EVAL_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)


def assert_close(actual, expected, tol: float = 1e-6):
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        f"Expected {expected}, got {actual}"
    )
