# Slotted ALOHA Protocol Simulator

A simulation of a **modified slotted ALOHA** protocol with adaptive backoff, implemented in Python. The project evaluates channel efficiency across varying node counts and transmission probabilities, and validates simulation results against theoretical predictions.

## Overview

Slotted ALOHA is a random-access MAC protocol where time is divided into discrete slots and nodes may only begin transmission at slot boundaries. This implementation extends the classic model with:

- **Exponential backoff on collision**: each colliding node halves its transmission probability (`p_i /= 2`)
- **Drop-and-reset after 4 consecutive collisions**: avoids indefinite backoff starvation
- **Per-node state tracking**: idle count, transmission count, success count, drop count

## Repository Structure

```
slotted-aloha/
├── simulation.ipynb          # Main notebook: implementation, verification, evaluation
├── simulation.py             # Standalone importable module (extracted core function)
├── theoretical_efficiency.pkl  # Precomputed theoretical efficiency values (required for Task 3 plots)
├── requirements.txt          # Python dependencies
└── README.md
```

## Protocol Details

Each node `i` maintains a transmission probability `p_i`, initialized to `p_0`.

**Per slot, each node independently:**
1. Draws a random number `r ∈ [0, 1)`
2. Transmits if `r < p_i`

**Slot outcome:**
| Senders | Outcome | State update |
|---------|---------|--------------|
| 0 | Idle | No change |
| 1 | **Success** | Winner resets `p_i = p_0` |
| ≥ 2 | **Collision** | Each collider: `p_i /= 2`; if 4th consecutive collision → reset `p_i = p_0`, increment drop count |

**Efficiency** is defined as:

```
efficiency = successful_slots / total_slots
```

## Results

Simulation results (solid lines) are compared against theoretical values (circle markers) across 7 node counts (`n = 1, 2, 5, 10, 20, 50, 100`) and a range of `p_0` values from 0.01 to 1.0, each over 100,000 slots.

Key observations:
- For `n = 1`, efficiency peaks near `p_0 = 1.0` (no competition)
- For large `n`, optimal `p_0` shifts toward smaller values; high `p_0` causes saturation
- Simulation closely tracks theoretical curves, validating the implementation

## Usage

### Run the notebook

```bash
jupyter notebook simulation.ipynb
```

### Import the simulator directly

```python
from simulation import simulate_slotted_aloha

efficiency = simulate_slotted_aloha(
    num_slots=100000,
    n=10,
    p_0=0.1
)
print(f"Efficiency: {efficiency:.4f}")
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_slots` | `int` | Number of time slots to simulate |
| `n` | `int` | Number of nodes in the network |
| `p_0` | `float` | Base transmission probability `[0, 1)` |
| `logging` | `bool` | Print per-slot state every 10 slots (default: `False`) |

## Requirements

- Python 3.8+
- See `requirements.txt`

## Background

This project was completed as part of **CSCI 333 — Computer Networks** at Nazarbayev University. The theoretical efficiency values are derived from the standard slotted ALOHA throughput formula:

$$S = n \cdot p \cdot (1 - p)^{n-1}$$

where `n` is the number of nodes and `p` is the transmission probability.
