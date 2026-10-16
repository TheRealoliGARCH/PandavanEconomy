import numpy as np
import pytest

from pandavan_economy.baseline import (
    DEFAULT_PARAMETERS,
    STATES,
    absorbing_chain_metrics,
    finite_horizon_absorption_probability,
    transition_matrix,
)


def test_transition_matrix_is_stochastic():
    matrix = transition_matrix()
    assert matrix.shape == (5, 5)
    assert np.all(matrix >= 0.0)
    assert np.allclose(matrix.sum(axis=1), 1.0)
    assert np.allclose(matrix[4], [0, 0, 0, 0, 1])


def test_default_fundamental_matrix_matches_paper_table():
    fundamental = absorbing_chain_metrics().fundamental_matrix
    expected = np.array([
        [20.0, 17.29, 11.5266666667, 5.70],
        [20.0, 18.29, 12.1933333333, 5.70],
        [20.0, 17.29, 13.1933333333, 5.70],
        [20.0, 17.99, 11.9933333333, 6.70],
    ])
    assert np.allclose(fundamental, expected, atol=1e-8)


def test_absorption_probabilities_are_one_for_default_parameters():
    assert np.allclose(absorbing_chain_metrics().absorption_probabilities, np.ones(4))


def test_expected_absorption_times_match_paper_table():
    times = absorbing_chain_metrics().expected_absorption_times
    expected = [54.5166666667, 56.1833333333, 56.1833333333, 56.6833333333]
    assert np.allclose(times, expected, atol=1e-7)


@pytest.mark.parametrize("horizon", [0, 1, 5, 10, 20, 50])
def test_finite_horizon_risk_is_valid_and_non_decreasing(horizon):
    risk = finite_horizon_absorption_probability(horizon)
    assert 0.0 <= risk <= 1.0
    if horizon > 0:
        assert risk >= finite_horizon_absorption_probability(horizon - 1) - 1e-12


def test_finite_horizon_risk_at_zero_is_zero():
    assert finite_horizon_absorption_probability(0) == pytest.approx(0.0)


def test_invalid_parameter_value_is_rejected():
    params = dict(DEFAULT_PARAMETERS)
    params["a"] = -0.1
    with pytest.raises(ValueError):
        transition_matrix(params)


def test_wrong_parameter_keys_are_rejected():
    with pytest.raises(ValueError):
        transition_matrix({"a": 0.05})


def test_non_absorbing_parameterization_is_rejected_for_metrics():
    params = dict(DEFAULT_PARAMETERS)
    params["a"] = 0.0
    with pytest.raises(ValueError, match="eventual absorption"):
        absorbing_chain_metrics(params)


def test_state_order_is_stable():
    assert STATES == ("Peace", "Experiment", "War", "Stagnation", "Absorb")


def test_known_finite_horizon_risk_baseline():
    risks = [finite_horizon_absorption_probability(h) for h in (5, 10, 20)]
    assert np.allclose(risks, [0.1055, 0.1828, 0.3184], atol=5e-4)
