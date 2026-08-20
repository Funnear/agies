"""Autonomous Adaptive Expansion Loop with Dynamic Convergence & Saturation Detection.

Runs continuous autonomous ingestion, web scraping, and acoustic enrichment cycles
without epoch limits until the Knowledge Graph expansion velocity flattens (plateaus) below a convergence threshold:
- Computes Growth Velocity: g(t) = (Δ|V| / |V|) + (Δ|E| / |E|)
- Detects Plateau / Saturation across consecutive steady-state epochs
- Saves convergence history logs to `data/corpus/convergence_history.json`
- Re-exports Neo4j Cypher and interactive visualizers upon final convergence.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import time
from typing import Any, Dict, List, Optional

from agies.orchestration.weekly_expansion import WeeklyKnowledgeGraphExpander

logger = logging.getLogger("agies.orchestration.convergence_expansion")


@dataclass
class ConvergenceEpoch:
    """Telemetry for a single expansion iteration epoch."""

    epoch_index: int
    timestamp: str
    elapsed_seconds: float
    total_nodes: int
    total_edges: int
    delta_nodes: int
    delta_edges: int
    growth_velocity: float
    is_converged: bool


class AdaptiveConvergenceExpander:
    """Executes recurring expansion cycles autonomously without epoch limits until graph growth flattens."""

    DEFAULT_CONVERGENCE_THRESHOLD = 0.002  # Less than 0.2% growth
    DEFAULT_PATIENCE_EPOCHS = 2  # Number of consecutive flat epochs to confirm convergence

    def __init__(
        self,
        data_dir: Optional[Path] = None,
        convergence_threshold: float = DEFAULT_CONVERGENCE_THRESHOLD,
        patience_epochs: int = DEFAULT_PATIENCE_EPOCHS,
        max_epochs: Optional[int] = None,  # None = Unlimited
    ):
        self.project_root = Path(__file__).resolve().parent.parent.parent.parent
        self.data_dir = Path(data_dir or (self.project_root / "data" / "corpus"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.convergence_threshold = convergence_threshold
        self.patience_epochs = patience_epochs
        self.max_epochs = max_epochs
        self.history_file = self.data_dir / "convergence_history.json"

    def run_until_flattened(
        self,
        initial_target_audio_per_genre: int = 15,
        delay_between_epochs_sec: float = 0.5,
    ) -> Dict[str, Any]:
        """Execute continuous expansion iterations until graph growth velocity flattens."""
        start_time = time.time()
        max_str = f"{self.max_epochs} Epochs" if self.max_epochs else "UNLIMITED (Runs until Flat)"
        logger.info(
            "=== LAUNCHING UNLIMITED EXPANSION UNTIL FLATTENED (Threshold: %.4f, Limit: %s) ===",
            self.convergence_threshold,
            max_str,
        )

        expander = WeeklyKnowledgeGraphExpander(data_dir=self.data_dir)
        epochs_history: List[ConvergenceEpoch] = []

        prev_nodes = 0
        prev_edges = 0
        consecutive_flat_epochs = 0
        final_status = "converged_and_flattened"
        epoch_idx = 0

        while True:
            epoch_idx += 1
            if self.max_epochs and epoch_idx > self.max_epochs:
                final_status = "max_epochs_reached"
                break

            epoch_start = time.time()
            target_audio = initial_target_audio_per_genre + (epoch_idx - 1) * 3

            logger.info("-> Starting Expansion Epoch #%d (Target Audio: %d)...", epoch_idx, target_audio)
            cycle_result = expander.run_weekly_cycle(target_audio_per_genre=target_audio)

            curr_nodes = cycle_result["total_nodes"]
            curr_edges = cycle_result["total_edges"]

            delta_nodes = max(0, curr_nodes - prev_nodes) if prev_nodes > 0 else curr_nodes
            delta_edges = max(0, curr_edges - prev_edges) if prev_edges > 0 else curr_edges

            if prev_nodes > 0 and prev_edges > 0:
                node_velocity = delta_nodes / prev_nodes
                edge_velocity = delta_edges / prev_edges
                growth_velocity = round(node_velocity + edge_velocity, 5)
            else:
                growth_velocity = 1.0  # Initial epoch baseline

            is_flat = (epoch_idx > 1) and (growth_velocity <= self.convergence_threshold)

            if is_flat:
                consecutive_flat_epochs += 1
                logger.info(
                    "   Epoch #%d Growth Velocity: %.5f <= Threshold %.4f (Flat Streak: %d/%d)",
                    epoch_idx,
                    growth_velocity,
                    self.convergence_threshold,
                    consecutive_flat_epochs,
                    self.patience_epochs,
                )
            else:
                consecutive_flat_epochs = 0
                logger.info(
                    "   Epoch #%d Growth Velocity: %.5f (Nodes: %d [+%d], Edges: %d [+%d])",
                    epoch_idx,
                    growth_velocity,
                    curr_nodes,
                    delta_nodes,
                    curr_edges,
                    delta_edges,
                )

            epoch_telemetry = ConvergenceEpoch(
                epoch_index=epoch_idx,
                timestamp=datetime.now(timezone.utc).isoformat(),
                elapsed_seconds=round(time.time() - epoch_start, 2),
                total_nodes=curr_nodes,
                total_edges=curr_edges,
                delta_nodes=delta_nodes,
                delta_edges=delta_edges,
                growth_velocity=growth_velocity,
                is_converged=consecutive_flat_epochs >= self.patience_epochs,
            )
            epochs_history.append(epoch_telemetry)

            # Persist live progress immediately after every epoch
            interim_summary = {
                "status": "running" if consecutive_flat_epochs < self.patience_epochs else "converged_and_flattened",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_elapsed_seconds": round(time.time() - start_time, 2),
                "total_epochs_executed": len(epochs_history),
                "final_total_nodes": curr_nodes,
                "final_total_edges": curr_edges,
                "convergence_threshold": self.convergence_threshold,
                "patience_epochs": self.patience_epochs,
                "epochs_trajectory": [asdict(e) for e in epochs_history],
            }
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(interim_summary, f, indent=2)

            prev_nodes = curr_nodes
            prev_edges = curr_edges

            if consecutive_flat_epochs >= self.patience_epochs:
                final_status = "converged_and_flattened"
                logger.info(
                    "=== CONVERGENCE ACHIEVED: Expansion curve mathematically flattened after %d epochs! ===",
                    epoch_idx,
                )
                break

            if delay_between_epochs_sec > 0:
                time.sleep(delay_between_epochs_sec)

        total_elapsed = round(time.time() - start_time, 2)

        # Save Final History to Disk
        convergence_summary = {
            "status": final_status,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_elapsed_seconds": total_elapsed,
            "total_epochs_executed": len(epochs_history),
            "final_total_nodes": prev_nodes,
            "final_total_edges": prev_edges,
            "convergence_threshold": self.convergence_threshold,
            "patience_epochs": self.patience_epochs,
            "epochs_trajectory": [asdict(e) for e in epochs_history],
        }

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(convergence_summary, f, indent=2)

        return convergence_summary
