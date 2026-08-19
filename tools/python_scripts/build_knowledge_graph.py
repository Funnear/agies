"""Knowledge Graph Collection & Behavioral Pattern Pipeline.

Ingests data from open APIs (MusicBrainz, Wikidata) and curated industry datasets,
constructs the Music Industry Knowledge Graph, executes standard and advanced behavioral pattern analytics,
and exports graph artifacts, link predictions, and interactive visualizers.
"""

from pathlib import Path
import json
import logging
import sys
import networkx as nx

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.graph.builder import MusicIndustryGraph
from agies.graph.extractors.musicbrainz_extractor import MusicBrainzExtractor
from agies.graph.extractors.wikidata_extractor import WikidataExtractor
from agies.graph.extractors.synthetic_extractor import SyntheticIndustryExtractor
from agies.analytics.patterns import MusicIndustryAnalytics
from agies.analytics.advanced import AdvancedIndustryAnalytics
from agies.visualization.interactive import render_interactive_graph

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("agies.pipeline")


def main():
    logger.info("=== Starting Music Industry Knowledge Graph Construction Pipeline ===")

    project_root = Path(__file__).resolve().parent.parent.parent
    data_dir = project_root / "data"
    notebooks_dir = project_root / "notebooks"
    data_dir.mkdir(parents=True, exist_ok=True)
    notebooks_dir.mkdir(parents=True, exist_ok=True)

    industry_graph = MusicIndustryGraph()

    # 1. Ingest Baseline Ecosystem
    logger.info(
        "Ingesting industry ecosystem baseline (Major/Indie labels, top agencies, legendary studios, super-producers)..."
    )
    synthetic_extractor = SyntheticIndustryExtractor(seed=42)
    syn_entities, syn_edges = synthetic_extractor.extract()
    industry_graph.ingest(syn_entities, syn_edges)
    logger.info(
        f"Ingested {len(syn_entities)} entities and {len(syn_edges)} relationships from baseline."
    )

    # 2. Ingest Live MusicBrainz Data
    logger.info(
        "Querying MusicBrainz live API for electronic and rock artist relationships..."
    )
    try:
        mb_extractor = MusicBrainzExtractor(timeout=10)
        mb_entities, mb_edges = mb_extractor.extract(query="electronic", limit=8)
        if mb_entities:
            industry_graph.ingest(mb_entities, mb_edges)
            logger.info(
                f"Ingested {len(mb_entities)} entities and {len(mb_edges)} edges from MusicBrainz."
            )
    except Exception as e:
        logger.warning(f"MusicBrainz ingestion notice: {e}")

    # 3. Ingest Live Wikidata Data
    logger.info("Querying Wikidata SPARQL endpoint for artist-label-agency mappings...")
    try:
        wd_extractor = WikidataExtractor(timeout=10)
        wd_entities, wd_edges = wd_extractor.extract(limit=10)
        if wd_entities:
            industry_graph.ingest(wd_entities, wd_edges)
            logger.info(
                f"Ingested {len(wd_entities)} entities and {len(wd_edges)} edges from Wikidata."
            )
    except Exception as e:
        logger.warning(f"Wikidata ingestion notice: {e}")

    # Graph Summary
    summary = industry_graph.summary()
    logger.info("=== Graph Summary ===")
    logger.info(f"Total Entity Nodes: {summary['total_nodes']}")
    logger.info(f"Total Relationship Edges: {summary['total_edges']}")

    # 4. Standard Behavioral Pattern Analytics
    logger.info("=== Executing Behavioral Pattern Analytics Suite ===")
    analytics = MusicIndustryAnalytics(industry_graph)
    power_brokers = analytics.compute_power_brokers(top_k=10)
    ecosystems = analytics.detect_creative_ecosystems()
    mobility = analytics.analyze_label_mobility()
    studio_reliance = analytics.compute_studio_reliance()
    agency_density = analytics.analyze_agency_collaboration_density()

    # 5. Advanced Analytics & Link Predictions
    logger.info(
        "=== Executing Advanced Network Analytics & Predictive Intelligence ==="
    )
    adv_analytics = AdvancedIndustryAnalytics(industry_graph)
    structural_holes = adv_analytics.analyze_structural_holes(top_k=8)
    k_core = adv_analytics.compute_k_core_decomposition()
    predicted_collabs = adv_analytics.predict_future_collaborations(top_k=10)
    era_evolution = adv_analytics.analyze_era_evolution()

    logger.info("Top Structural Hole Brokers (Burt's Constraint):")
    for sh in structural_holes[:3]:
        logger.info(
            f"  - [{sh['entity_type'].upper()}] {sh['name']} (Constraint: {sh['network_constraint']}, {sh['brokerage_potential']})"
        )

    logger.info("Top Predicted Upcoming Collaborations (Link Prediction):")
    for pc in predicted_collabs[:4]:
        logger.info(
            f"  - {pc['artist_1']} x {pc['artist_2']} (Affinity: {pc['affinity_score']}, Likelihood: {pc['likelihood']}, Shared Genres: {pc['shared_genres']})"
        )

    # 6. Export Graph & Reports
    json_path = data_dir / "music_industry_knowledge_graph.json"
    industry_graph.export_json(json_path)

    graphml_path = data_dir / "music_industry_knowledge_graph.graphml"
    try:
        g_export = nx.MultiDiGraph()
        for n, d in industry_graph.graph.nodes(data=True):
            clean_d = {
                k: ("" if v is None else str(v) if isinstance(v, (list, dict)) else v)
                for k, v in d.items()
            }
            g_export.add_node(n, **clean_d)
        for u, v, k, d in industry_graph.graph.edges(keys=True, data=True):
            clean_d = {
                k_: (
                    ""
                    if v_ is None
                    else str(v_) if isinstance(v_, (list, dict)) else v_
                )
                for k_, v_ in d.items()
            }
            g_export.add_edge(u, v, key=k, **clean_d)
        nx.write_graphml(g_export, str(graphml_path))
    except Exception as e:
        logger.warning(f"GraphML export notice: {e}")

    report_data = {
        "summary": summary,
        "power_brokers": power_brokers,
        "creative_ecosystems": ecosystems,
        "label_mobility": mobility,
        "studio_reliance": studio_reliance,
        "agency_collaboration_dynamics": agency_density,
        "structural_holes": structural_holes,
        "k_core_decomposition": k_core,
        "predicted_collaborations": predicted_collabs,
        "era_evolution": era_evolution,
    }
    report_json_path = data_dir / "behavioral_patterns_report.json"
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    # 7. Generate Interactive Pyvis Network Visualizers
    html_output_notebooks = notebooks_dir / "music_industry_network.html"
    html_output_data = data_dir / "music_industry_network.html"

    render_interactive_graph(
        industry_graph,
        output_html_path=html_output_notebooks,
        heading="Music Industry Knowledge Graph & Predictive Ecosystem",
    )
    render_interactive_graph(
        industry_graph,
        output_html_path=html_output_data,
        heading="Music Industry Knowledge Graph & Predictive Ecosystem",
    )
    logger.info(f"Updated Interactive Visualizers at {html_output_notebooks}")
    logger.info("=== Pipeline Execution Complete Successfully! ===")


if __name__ == "__main__":
    main()
