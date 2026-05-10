"""
simulation.py — Slotted ALOHA Protocol Simulator

Standalone module exposing simulate_slotted_aloha().
Can be imported directly or run as a script for a quick demo.
"""

import random


def simulate_slotted_aloha(num_slots: int, n: int, p_0: float, logging: bool = False) -> float:
    """
    Simulate a modified slotted ALOHA protocol with adaptive backoff.

    Each node starts with transmission probability p_0. On collision, the
    colliding node halves its probability. After 4 consecutive collisions
    without success, the node resets its probability back to p_0 (drop-and-reset).

    Parameters
    ----------
    num_slots : int
        Total number of time slots to simulate.
    n : int
        Number of nodes in the network.
    p_0 : float
        Base transmission probability in [0, 1). Each node is initialized
        to this value and resets to it after a successful transmission or
        after 4 consecutive collisions.
    logging : bool, optional
        If True, prints per-node state every 10 slots. Default is False.

    Returns
    -------
    float
        Channel efficiency = successful_slots / num_slots.

    Notes
    -----
    A node transmits in a given slot if a uniform random draw r in [0, 1)
    satisfies r < p_i. Using strict less-than (<) avoids a degenerate case
    where p_0 = 0 would still trigger transmission under <=.
    """
    # Per-node counters
    idle_cnt = [0] * n
    tx_cnt = [0] * n
    succ_cnt = [0] * n
    drop_cnt = [0] * n

    # Adaptive state
    prev_prob = [p_0] * n          # current transmission probability per node
    collisions_per_node = [0] * n  # consecutive collision counter per node

    success_slots = 0

    if logging:
        print(f"Simulation: {num_slots} slots | {n} nodes | p_0 = {p_0}")
        print("-" * 60)

    for slot in range(num_slots):
        who_transmits = []
        node_state = []

        for i in range(n):
            if random.random() < prev_prob[i]:
                who_transmits.append(i)
                node_state.append("tx")
                tx_cnt[i] += 1
            else:
                node_state.append("idle")
                idle_cnt[i] += 1

        senders = len(who_transmits)

        if senders == 0:
            slot_status = "idle"
        elif senders == 1:
            slot_status = "success"
            success_slots += 1
        else:
            slot_status = "collision"

        if slot_status == "success":
            winner = who_transmits[0]
            prev_prob[winner] = p_0
            succ_cnt[winner] += 1
            collisions_per_node[winner] = 0

        elif slot_status == "collision":
            for i in who_transmits:
                collisions_per_node[i] += 1
                if collisions_per_node[i] >= 4:
                    # Drop-and-reset after 4 consecutive collisions
                    prev_prob[i] = p_0
                    collisions_per_node[i] = 0
                    drop_cnt[i] += 1
                else:
                    prev_prob[i] /= 2

        if logging and slot % 10 == 0:
            print(f"Slot {slot:>4}: {slot_status}")
            for i in range(n):
                print(
                    f"  node {i}: {node_state[i]:>4} | "
                    f"p={prev_prob[i]:.4f} | "
                    f"idle={idle_cnt[i]:>4} | "
                    f"tx={tx_cnt[i]:>4} | "
                    f"succ={succ_cnt[i]:>4} | "
                    f"drops={drop_cnt[i]}"
                )

    efficiency = success_slots / num_slots

    if logging:
        print("-" * 60)
        print(f"Result: n={n}, p_0={p_0}, efficiency={efficiency:.4f}")

    return efficiency


if __name__ == "__main__":
    # Quick demo
    random.seed(42)
    for n in [1, 5, 10, 20]:
        p_opt = 1 / n if n > 0 else 1.0
        eff = simulate_slotted_aloha(num_slots=100_000, n=n, p_0=round(p_opt, 2))
        print(f"n={n:>3}, p_0={p_opt:.2f} -> efficiency={eff:.4f}")
