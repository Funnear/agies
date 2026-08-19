"""Generate demo interactive network graph HTML."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.graph.builder import MusicIndustryGraph
from agies.graph.extractors.synthetic_extractor import SyntheticIndustryExtractor
from agies.visualization.interactive import render_interactive_graph
from agies.analytics.patterns import MusicIndustryAnalytics


def main():
    extractor = SyntheticIndustryExtractor()
    entities, edges = extractor.extract()

    graph = MusicIndustryGraph()
    graph.ingest(entities, edges)

    analytics = MusicIndustryAnalytics(graph)
    brokers = analytics.compute_power_brokers(top_k=5)
    mobility = analytics.analyze_label_mobility()
    agency_density = analytics.analyze_agency_collaboration_density()

    print("=== Power Brokers ===")
    for b in brokers["by_pagerank"]:
        print(f"  {b['name']} ({b['entity_type']}): PageRank = {b['score']}")

    print("\n=== Label Mobility ===")
    print(f"  Migration Rate: {mobility['migration_rate_percentage']}%")

    print("\n=== Agency Collaboration Density ===")
    print(
        f"  Intra-Agency Ratio: {agency_density['intra_agency_ratio_percentage']}% ({agency_density['behavior_interpretation']})"
    )

    out_file = (
        Path(__file__).resolve().parent.parent.parent
        / "notebooks"
        / "music_industry_network.html"
    )
    render_interactive_graph(graph, output_html_path=out_file)
    print(f"\n[OK] Interactive graph saved to: {out_file}")


if __name__ == "__main__":
    main()
