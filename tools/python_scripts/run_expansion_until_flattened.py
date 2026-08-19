#!/usr/bin/env python3
"""Run Autonomous Knowledge Graph Expansion until Graph Growth Velocity Flattens."""

import argparse
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.orchestration.convergence_expansion import AdaptiveConvergenceExpander

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def main():
    parser = argparse.ArgumentParser(
        description="Run continuous autonomous expansion cycles until the knowledge graph flattens."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.002,
        help="Growth velocity threshold (default: 0.002 = 0.2%)",
    )
    parser.add_argument(
        "--patience",
        type=int,
        default=2,
        help="Consecutive flat epochs needed to declare convergence (default: 2)",
    )
    parser.add_argument(
        "--max-epochs",
        type=int,
        default=10,
        help="Maximum expansion epochs before terminating (default: 10)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay in seconds between epochs (default: 0.2s)",
    )

    args = parser.parse_args()

    expander = AdaptiveConvergenceExpander(
        convergence_threshold=args.threshold,
        patience_epochs=args.patience,
        max_epochs=args.max_epochs,
    )

    results = expander.run_until_flattened(
        delay_between_epochs_sec=args.delay,
    )

    print("\n" + "=" * 60)
    print("      AGIES CONVERGENCE EXPANSION TRAJECTORY REPORT")
    print("=" * 60)
    print(f"Status:                 {results['status'].upper()}")
    print(f"Total Elapsed Time:     {results['total_elapsed_seconds']}s")
    print(f"Total Epochs Run:       {results['total_epochs_executed']}")
    print(f"Final Graph Nodes:      {results['final_total_nodes']} Nodes")
    print(f"Final Graph Relations:  {results['final_total_edges']} Edges")
    print(f"Convergence Threshold:  {results['convergence_threshold']}")
    print("-" * 60)
    print("Epoch Trajectory History:")
    for ep in results["epochs_trajectory"]:
        flat_badge = " [FLAT / CONVERGED]" if ep["is_converged"] else ""
        print(
            f"  * Epoch {ep['epoch_index']}: {ep['total_nodes']} Nodes (+{ep['delta_nodes']}), "
            f"{ep['total_edges']} Edges (+{ep['delta_edges']}) | Velocity: {ep['growth_velocity']}{flat_badge}"
        )
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
