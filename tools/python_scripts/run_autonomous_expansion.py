#!/usr/bin/env python3
"""Run Autonomous Continuous Knowledge Graph Expansion & Exponential Growth Cycle."""

import argparse
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.orchestration.autonomous_expansion import AutonomousKnowledgeGraphExpander

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def main():
    parser = argparse.ArgumentParser(
        description="Run an autonomous knowledge graph expansion cycle."
    )
    parser.add_argument(
        "--target-audio-per-genre",
        type=int,
        default=15,
        help="Target synthetic/harvested audio tracks per musical subgenre (default: 15)",
    )
    args = parser.parse_args()

    expander = AutonomousKnowledgeGraphExpander()
    results = expander.run_autonomous_cycle(
        target_audio_per_genre=args.target_audio_per_genre
    )

    print("\n" + "=" * 60)
    print("      AGIES AUTONOMOUS CONTINUOUS EXPANSION REPORT")
    print("=" * 60)
    print(f"Timestamp:              {results['cycle_timestamp']}")
    print(f"Execution Time:         {results['elapsed_seconds']}s")
    print(f"Total Graph Entities:   {results['total_nodes']} Nodes")
    print(f"Total Graph Relations:  {results['total_edges']} Edges")
    print(
        f"Audio Tracks Ingested:  {results['audio_corpus_expansion'].get('tracks_injected_to_graph', 0)} Tracks"
    )
    print(
        f"Acoustic Edges Injected:{results['acoustic_enrichment']['classified_edges_count'] + results['acoustic_enrichment']['acoustic_similarity_edges_count']} Edges"
    )
    print(f"Cypher Import Script:   {results['exported_cypher_file']}")
    print(f"Interactive Network UI: {results['exported_interactive_html']}")
    print("-" * 60)
    print("Top Predictive Breakout A&R Candidates:")
    for c in results["predictive_breakout_artists"]:
        print(
            f"  * {c['artist_name']} ({c.get('classified_subgenre', 'Electronic')}) -> Velocity: {c.get('breakout_velocity_score', 1.0)} [{c.get('recommendation', 'Anchor')}]"
        )
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
