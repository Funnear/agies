"""CLI Command Runner for Weekly Autonomous Knowledge Graph & Audio Corpus Expansion."""

import argparse
import logging
from pathlib import Path
import sys

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.orchestration.weekly_expansion import WeeklyKnowledgeGraphExpander

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("agies.weekly_cli")


def main():
    parser = argparse.ArgumentParser(
        description="Run Autonomous Weekly Knowledge Graph & Audio Corpus Expansion"
    )
    parser.add_argument(
        "--audio-per-genre",
        type=int,
        default=15,
        help="Number of audio tracks to harvest per genre",
    )
    args = parser.parse_args()

    orchestrator = WeeklyKnowledgeGraphExpander()
    results = orchestrator.run_weekly_cycle(target_audio_per_genre=args.audio_per_genre)

    print("\n" + "=" * 60)
    print("      AGIES WEEKLY CONTINUOUS EXPANSION REPORT")
    print("=" * 60)
    print(f"Timestamp:              {results['cycle_timestamp']}")
    print(f"Execution Time:         {results['elapsed_seconds']}s")
    print(f"Total Graph Entities:   {results['total_nodes']} Nodes")
    print(f"Total Graph Relations:  {results['total_edges']} Edges")
    print(
        f"Audio Tracks Ingested:  {results['audio_corpus_expansion']['tracks_injected_to_graph']} Tracks"
    )
    print(
        f"Acoustic Edges Injected:{results['acoustic_enrichment']['acoustic_similarity_edges_count']} Edges"
    )
    print(f"Cypher Import Script:   {results['exported_cypher_file']}")
    print(f"Interactive Network UI: {results['exported_interactive_html']}")
    print("-" * 60)
    print("Top Predictive Breakout A&R Candidates:")
    for a in results["predictive_breakout_artists"][:4]:
        print(
            f"  * {a['artist_name']} ({a['classified_subgenre']}) -> Velocity: {a['breakout_velocity_score']} [{a['recommendation']}]"
        )
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
