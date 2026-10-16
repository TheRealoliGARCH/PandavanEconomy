"""Original five-state absorbing Markov model.

State order: Peace, Experiment, War, Stagnation, Absorb.
Published parameter meanings: a = Peace -> Absorb; e allocates non-absorbing
Peace transitions to Experiment; p = Experiment -> War; q = War -> Peace;
h = Stagnation -> Peace.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
from numpy.typing import NDArray

STATES = ("Peace", "Experiment", "War", "Stagnation", "Absorb")
TRANSIENT_STATES = STATES[:-1]
DEFAULT_PARAMETERS = {"a": 0.05, "e": 0.70, "p": 0.40, "q": 0.60, "h": 0.30}


@dataclass(frozen=True)
class ChainMetrics:
    """Quantities derived from the four transient states."""

    transient_matrix: NDArray[np.float64]
    absorption_vector: NDArray[np.float64]
    fundamental_matrix: NDArray[np.float64]
    absorption_probabilities: NDArray[np.float64]
    expected_absorption_times: NDArray[np.float64]


def _validate_parameters(parameters: Mapping[str, float]) -> dict[str, float]:
    required = set(DEFAULT_PARAMETERS)
    if set(parameters) != required:
        missing = sorted(required - set(parameters))
        extra = sorted(set(parameters) - required)
        raise ValueError(f"Expected parameters {sorted(required)}; missing={missing}, extra={extra}")
    values = {key: float(value) for key, value in parameters.items()}
    for key, value in values.items():
        if not np.isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError(f"Parameter {key!r} must be finite and in [0, 1].")
    return values


def transition_matrix(parameters: Mapping[str, float] | None = None) -> NDArray[np.float64]:
    """Return the published 5x5 row-stochastic transition matrix."""
    pars = _validate_parameters(DEFAULT_PARAMETERS if parameters is None else parameters)
    a, e, p, q, h = (pars[key] for key in ("a", "e", "p", "q", "h"))
    return np.array(
        [
            [0.0, e * (1.0 - a), 0.0, (1.0 - e) * (1.0 - a), a],
            [1.0 - p, 0.0, p, 0.0, 0.0],
            [q, 0.0, 1.0 - q, 0.0, 0.0],
            [h, 1.0 - h, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0],
        ], dtype=float
    )


def absorbing_chain_metrics(parameters: Mapping[str, float] | None = None) -> ChainMetrics:
    """Calculate N, absorption probabilities, and expected times.

    Raises ValueError if this parameterization does not define a finite-mean
    absorbing chain with eventual absorption probability one.
    """
    matrix = transition_matrix(parameters)
    q_matrix = matrix[:4, :4]
    r_vector = matrix[:4, 4]
    system = np.eye(4) - q_matrix
    try:
        fundamental = np.linalg.solve(system, np.eye(4))
        times = np.linalg.solve(system, np.ones(4))
    except np.linalg.LinAlgError as exc:
        raise ValueError("The transient system is not a finite-mean absorbing chain.") from exc
    absorption = fundamental @ r_vector
    if not np.allclose(absorption, np.ones(4), atol=1e-9, rtol=1e-9):
        raise ValueError("The selected parameters do not imply eventual absorption with probability one.")
    if not np.all(np.isfinite(times)) or np.any(times < 0):
        raise ValueError("Expected absorption times are not finite and nonnegative.")
    return ChainMetrics(q_matrix, r_vector, fundamental, absorption, times)


def finite_horizon_absorption_probability(
    horizon: int,
    initial_state: str = "Peace",
    parameters: Mapping[str, float] | None = None,
) -> float:
    """Probability of entering Absorb within `horizon` transitions.

    Starting in Absorb is intentionally excluded because this function defines
    risk from one of the four transient states.
    """
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError("horizon must be a nonnegative integer")
    if initial_state not in TRANSIENT_STATES:
        raise ValueError(f"initial_state must be one of {TRANSIENT_STATES}")
    matrix = transition_matrix(parameters)
    q_matrix = matrix[:4, :4]
    index = TRANSIENT_STATES.index(initial_state)
    survival = float(np.linalg.matrix_power(q_matrix, horizon)[index, :].sum())
    risk = 1.0 - survival
    if -1e-12 <= risk < 0.0:
        risk = 0.0
    if 1.0 < risk <= 1.0 + 1e-12:
        risk = 1.0
    if not 0.0 <= risk <= 1.0:
        raise ArithmeticError("Computed absorption probability lies outside [0, 1].")
    return risk


def baseline_report() -> dict[str, object]:
    """Compact baseline report, with outputs for the default parameters."""
    metrics = absorbing_chain_metrics()
    return {
        "states": list(STATES),
        "parameters": dict(DEFAULT_PARAMETERS),
        "transition_matrix": transition_matrix().tolist(),
        "absorption_probabilities": metrics.absorption_probabilities.tolist(),
        "expected_absorption_times": metrics.expected_absorption_times.tolist(),
        "finite_horizon_risk_from_peace": {
            str(h): finite_horizon_absorption_probability(h) for h in (5, 10, 20, 50)
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(baseline_report(), indent=2))
