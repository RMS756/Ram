"""Chapter 3 Eq. 3.4 calibration fit — NLL on the labels (SC-4 alternative).

SC-4 (UNRESOLVED): Chapter 3 fits (gamma_1, gamma_0) by minimising the negative
log-likelihood of the *labels* on out-of-fold logits (Guo et al., 2017), whereas
the frozen implementation (``PlattLogitCalibrator``) fits against Platt's
smoothed targets. Both are provided so the pilot can report both; neither is
adopted here.

The map, the gamma_1 > 0 check and the runtime transform are inherited
unchanged from ``PlattLogitCalibrator``; only the fitting targets differ.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from rem.algorithms.calibration.platt import MonotonicityViolationError, PlattLogitCalibrator
from rem.algorithms.detection.ridge_logistic import sigmoid

__all__ = ["LabelNLLLogitCalibrator"]


class LabelNLLLogitCalibrator(PlattLogitCalibrator):
    """p = sigmoid(gamma_1 s + gamma_0), fitted by NLL on y_i (Chapter 3 Eq. 3.4)."""

    name = "platt_logit_label_nll"

    def fit(self, logits: Sequence[float], labels: Sequence[int]) -> "LabelNLLLogitCalibrator":
        scores = np.asarray(logits, dtype=float)
        y = np.asarray(labels, dtype=float)
        if scores.shape[0] != y.shape[0] or scores.shape[0] == 0:
            raise ValueError("logits and labels must be non-empty and equally long.")
        if set(np.unique(y)) - {0.0, 1.0}:
            raise ValueError("Labels must be 0 or 1.")
        if y.min() == y.max():
            raise ValueError("The calibration split must contain both classes.")
        design = np.column_stack([np.ones_like(scores), scores])
        theta = np.zeros(2)
        self._converged = False
        for _ in range(self.max_iterations):
            p = sigmoid(design @ theta)
            grad = design.T @ (p - y)
            w = p * (1.0 - p)
            hess = (design.T * w) @ design + 1e-12 * np.eye(2)
            step = np.linalg.solve(hess, grad)
            # Damped Newton: halve the step until the NLL does not increase, so
            # (quasi-)separable calibration sets do not diverge.
            nll0 = _nll(design, y, theta)
            scale = 1.0
            while scale > 1e-8 and _nll(design, y, theta - scale * step) > nll0 + 1e-12:
                scale *= 0.5
            theta = theta - scale * step
            if np.max(np.abs(scale * step)) < self.tolerance:
                self._converged = True
                break
        g0, g1 = float(theta[0]), float(theta[1])
        if not g1 > 0.0:
            raise MonotonicityViolationError(
                f"{self.name} fitted gamma_1 = {g1:.6g} (not positive); calibration rejected "
                "for this fit (Chapter 3 Sec. 3.7.2 property 1)."
            )
        self._gamma_0, self._gamma_1 = g0, g1
        return self


def _nll(design: np.ndarray, y: np.ndarray, theta: np.ndarray) -> float:
    s = design @ theta
    return float(np.sum(np.logaddexp(0.0, s) - y * s))
