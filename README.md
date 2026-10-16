# Pandavan Economy

A research repository for the Pandavan Economy framework: a five-state absorbing Markov chain, finite-horizon absorption-risk optimization, and a reciprocal-exchange network layer.

## Research integrity

This repository separates three layers:

1. **Original model:** Peace, Experiment, War, Stagnation, and Absorb, with the published five-parameter transition matrix.
2. **Computational validation:** matrix invariants, fundamental matrix, absorption probabilities, and absorption-time calculations.
3. **Extensions:** policy-controlled transition probabilities and network coupling. These are hypotheses and implementation experiments, not established empirical findings.

Absorb is an absorbing state by definition. No intervention may transition out of Absorb.

## Start here

Requirements: Python 3.10 or later, NumPy, pytest.

```bash
python -m pip install -e ".[dev]"
pytest
python -m pandavan_economy.baseline
```

## Model

State order is `(Peace, Experiment, War, Stagnation, Absorb)`. The original transition matrix is

```text
P = [[0, e(1-a), 0, (1-e)(1-a), a],
     [1-p, 0, p, 0, 0],
     [q, 0, 1-q, 0, 0],
     [h, 1-h, 0, 0, 0],
     [0, 0, 0, 0, 1]]
```

For transient submatrix `Q`, the fundamental matrix is `N = (I - Q)^(-1)`. Finite-horizon absorption probability from transient state `i` is

```text
Pr(T_A <= H | Q_0=i) = 1 - e_i^T Q^H 1
```

The code uses a linear solve rather than explicitly calculating a matrix inverse when possible.

## Reproducibility and scope

- The five-parameter model is validated independently of the extension.
- Synthetic intervention results, if later added, must be labeled as model-generated rather than empirical.
- No real-world intervention effectiveness is claimed without a defined dataset and a credible identification strategy.
- The Genuine Nations sampling frame should be versioned separately from time-varying economic and rating data. A roster is not empirical validation of the classification.
- The network layer distinguishes reciprocal connection from equal bidirectional flow.

See `docs/RESEARCH_PROTOCOL.md` for the proposed workflow.
