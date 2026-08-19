"""Build and export the complete Multi-Country Global Music Industry Knowledge Graph Corpus.

Executes country-by-country modeling, cross-border network analysis, and global pattern mining.
"""

from pathlib import Path
import json
import logging
import sys
from typing import Dict
import networkx as nx

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.extractors.musicbrainz_extractor import MusicBrainzExtractor
from agies.graph.extractors.wikidata_extractor import WikidataExtractor
from agies.analytics.patterns import MusicIndustryAnalytics
from agies.analytics.advanced import AdvancedIndustryAnalytics
from agies.analytics.global_patterns import GlobalPatternAnalyzer
from agies.visualization.interactive import render_interactive_graph

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("agies.corpus_pipeline")


def main():
    logger.info(
        "=== Building Global Multi-Country Music Industry Knowledge Graph Corpus ==="
    )

    project_root = Path(__file__).resolve().parent.parent.parent
    corpus_dir = project_root / "data" / "corpus"
    corpus_dir.mkdir(parents=True, exist_ok=True)

    industry_graph = MusicIndustryGraph()

    # 1. Ingest Multi-Country Global Corpus
    logger.info(
        "Ingesting Global Music Industry Corpus across 11+ Nations (Germany, UK, USA, Japan, S.Korea, France, Sweden, Jamaica, Nigeria, Brazil, Canada)..."
    )
    corpus_extractor = GlobalMusicIndustryCorpusExtractor()
    corpus_entities, corpus_edges = corpus_extractor.extract()
    industry_graph.ingest(corpus_entities, corpus_edges)
    logger.info(
        f"Ingested {len(corpus_entities)} entities and {len(corpus_edges)} relationships from Global Corpus."
    )

    # Ingest Micro-Ecosystem Corpus for Emerging Musicians
    from agies.graph.micro_corpus import MicroEcosystemCorpusExtractor

    micro_extractor = MicroEcosystemCorpusExtractor()
    micro_entities, micro_edges = micro_extractor.extract()
    industry_graph.ingest(micro_entities, micro_edges)
    logger.info(
        f"Ingested {len(micro_entities)} grassroots entities and {len(micro_edges)} stepping-stone relationships from Micro-Ecosystem."
    )

    # Ingest Hierarchical Geo-Spatial & Genre Taxonomy
    from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder

    geo_builder = GeoTaxonomyHierarchyBuilder()
    geo_entities, geo_edges = geo_builder.build_hierarchy()
    industry_graph.ingest(geo_entities, geo_edges)
    logger.info(
        f"Ingested {len(geo_entities)} hierarchical geo/genre entities and {len(geo_edges)} taxonomic edges."
    )

    # Ingest City-Level Industry Connects & Inter-City Corridors
    from agies.graph.city_connects import CityIndustryConnectsEnricher

    city_enricher = CityIndustryConnectsEnricher()
    city_results = city_enricher.enrich_city_connects(industry_graph)
    logger.info(
        f"Injected {city_results['city_anchors_added']} city infrastructure anchors and {city_results['inter_city_corridors_added']} inter-city corridors."
    )

    # 2. Ingest Live Open API Data (MusicBrainz & Wikidata)
    try:
        mb_extractor = MusicBrainzExtractor(timeout=8)
        mb_entities, mb_edges = mb_extractor.extract(query="electronic", limit=10)
        if mb_entities:
            industry_graph.ingest(mb_entities, mb_edges)
            logger.info(
                f"Ingested {len(mb_entities)} entities and {len(mb_edges)} relationships from MusicBrainz."
            )
    except Exception as e:
        logger.warning(f"MusicBrainz ingestion notice: {e}")

    try:
        wd_extractor = WikidataExtractor(timeout=8)
        wd_entities, wd_edges = wd_extractor.extract(limit=10)
        if wd_entities:
            industry_graph.ingest(wd_entities, wd_edges)
            logger.info(
                f"Ingested {len(wd_entities)} entities and {len(wd_edges)} relationships from Wikidata."
            )
    except Exception as e:
        logger.warning(f"Wikidata ingestion notice: {e}")

    # 3. Acoustic Knowledge Graph Enrichment (arXiv:2110.08862 Mel-Tempogram Classifier)
    logger.info(
        "=== 3. Enriching Knowledge Graph with Deep Mel-Tempogram Acoustic Intelligence ==="
    )
    from agies.graph.enrichment import AcousticGraphEnricher

    enricher = AcousticGraphEnricher()
    enrichment_results = enricher.enrich_graph(industry_graph)
    logger.info(
        "Enrichment Complete: %d artists acoustically classified, %d genre taxonomy nodes, %d acoustic similarity edges added.",
        enrichment_results["enriched_artists_count"],
        enrichment_results["added_genre_nodes_count"],
        enrichment_results["acoustic_similarity_edges_count"],
    )

    summary = industry_graph.summary()
    logger.info("=== Final Global Corpus Statistics ===")
    logger.info(f"Total Nodes: {summary['total_nodes']}")
    logger.info(f"Total Edges: {summary['total_edges']}")
    logger.info(f"Nodes by Type: {summary['nodes_by_type']}")
    logger.info(f"Edges by Relationship: {summary['edges_by_relationship']}")

    # 3. Standard & Advanced Network Analytics
    logger.info("=== Running Network Analytics Suite ===")
    analytics = MusicIndustryAnalytics(industry_graph)
    adv_analytics = AdvancedIndustryAnalytics(industry_graph)
    global_analytics = GlobalPatternAnalyzer(industry_graph)

    power_brokers = analytics.compute_power_brokers(top_k=15)
    ecosystems = analytics.detect_creative_ecosystems()
    mobility = analytics.analyze_label_mobility()
    studio_reliance = analytics.compute_studio_reliance()
    agency_density = analytics.analyze_agency_collaboration_density()
    structural_holes = adv_analytics.analyze_structural_holes(top_k=15)
    k_core = adv_analytics.compute_k_core_decomposition()
    predicted_collabs = adv_analytics.predict_future_collaborations(top_k=15)

    # 4. Global Macro Patterns & Cross-Border Flows
    logger.info("=== Mining Global Macro Patterns & Trade Flows ===")
    cross_border_flows = global_analytics.analyze_cross_border_flows()
    producer_export_leverage = global_analytics.analyze_producer_export_leverage()
    global_macro_patterns = global_analytics.spot_emerging_global_patterns()

    logger.info(
        f"Global De-Anglicization Index: {global_macro_patterns['de_anglicization_index_percentage']}% non-Anglo presence."
    )
    logger.info("Top Cross-Border Corridors:")
    for corr in cross_border_flows["top_cross_border_corridors"][:5]:
        logger.info(
            f"  - {corr['corridor']}: {corr['collaboration_count']} international collabs"
        )

    logger.info("Top Producer Export Hubs:")
    for pe in producer_export_leverage[:4]:
        logger.info(
            f"  - {pe['country']}: {pe['export_leverage_ratio']}% foreign export ratio ({pe['archetype']})"
        )

    # 5. Persist Entities Catalog & Knowledge Graph
    catalog: Dict[str, list] = {}
    for nid, data in industry_graph.graph.nodes(data=True):
        etype = data.get("entity_type", "other")
        catalog.setdefault(etype, []).append({"id": nid, **data})

    with open(corpus_dir / "entities_catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    industry_graph.export_json(corpus_dir / "music_industry_corpus.json")

    # GraphML Export
    graphml_path = corpus_dir / "music_industry_corpus.graphml"
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
        logger.warning(f"GraphML notice: {e}")

    # Save Cross-Border Flows JSON
    with open(
        corpus_dir / "global_cross_border_flows.json", "w", encoding="utf-8"
    ) as f:
        json.dump(cross_border_flows, f, indent=2)

    # Save Combined Analytics & Patterns Report JSON
    full_report = {
        "summary": summary,
        "global_macro_patterns": global_macro_patterns,
        "cross_border_flows": cross_border_flows,
        "producer_export_leverage": producer_export_leverage,
        "power_brokers": power_brokers,
        "creative_ecosystems": ecosystems,
        "label_mobility": mobility,
        "studio_reliance": studio_reliance,
        "agency_collaboration_dynamics": agency_density,
        "structural_holes": structural_holes,
        "k_core_decomposition": k_core,
        "predicted_collaborations": predicted_collabs,
    }
    with open(
        corpus_dir / "corpus_behavioral_patterns.json", "w", encoding="utf-8"
    ) as f:
        json.dump(full_report, f, indent=2)

    # 6. Generate Global Patterns Markdown Report
    report_md_path = corpus_dir / "global_music_patterns_report.md"
    generate_markdown_report(
        report_md_path,
        summary,
        global_macro_patterns,
        cross_border_flows,
        producer_export_leverage,
        predicted_collabs,
    )
    logger.info(f"Saved Global Patterns Report to {report_md_path}")

    # 7. Render Interactive Physics Graph Visualizer
    html_path = corpus_dir / "corpus_interactive_network.html"
    render_interactive_graph(
        industry_graph,
        output_html_path=html_path,
        heading="Global Music Industry Multi-Country Knowledge Graph & Emergent Macro Patterns",
    )
    logger.info(f"Rendered Interactive Visualizer at {html_path}")
    logger.info("=== Full Pipeline Completed Successfully! ===")


def generate_markdown_report(
    path: Path, summary, macro_patterns, cross_border, producer_leverage, predictions
):
    """Format and save a detailed Markdown report on emerging global patterns."""
    content = f"""# Global Music Industry Knowledge Graph: Multi-Country Analysis & Emerging Patterns

> **Corpus Scope**: {summary['total_nodes']} Entities, {summary['total_edges']} Relationships  
> **Territories Analyzed**: Germany, UK, USA, Japan, South Korea, France, Sweden, Jamaica, Nigeria, Brazil, Canada  

---

## 1. Global Corpus Architecture

| Entity Type | Total Nodes | Key Representatives |
| :--- | :--- | :--- |
| **Artists** | {summary['nodes_by_type'].get('artist', 0)} | Kraftwerk, BTS, Taylor Swift, Drake, Daft Punk, Burna Boy, Bad Bunny, Ryuichi Sakamoto |
| **Record Labels** | {summary['nodes_by_type'].get('record_label', 0)} | BMG, Deutsche Grammophon, UMG, SME, WMG, Beggars, HYBE, Mavin, Som Livre |
| **Recording Studios** | {summary['nodes_by_type'].get('studio', 0)} | Hansa (Berlin), Funkhaus (Berlin), Abbey Road (London), Electric Lady (NYC), Tuff Gong (Kingston) |
| **Producers** | {summary['nodes_by_type'].get('producer', 0)} | Max Martin, Brian Eno, Hans Zimmer, Rick Rubin, Dr. Dre, Tainy, Don Jazzy, Ludwig Göransson |
| **Talent Agencies** | {summary['nodes_by_type'].get('agency', 0)} | WME, CAA, UTA, Wasserman, Primary Talent, Roc Nation |

---

## 2. Emerging Global Macro Patterns

"""
    for p in macro_patterns.get("macro_patterns", []):
        content += f"""### [{p['pattern_id']}] {p['title']}
- **Core Finding**: {p['insight']}
- **Empirical Metric**: {p['evidence_metric']}

"""

    content += """---

## 3. National Industrial Models & Ecosystem Archetypes

| Territory | Industrial Archetype | Structural Mechanism |
| :--- | :--- | :--- |
"""
    for country, data in macro_patterns.get(
        "national_industrial_archetypes", {}
    ).items():
        content += (
            f"| **{country}** | `{data['model_name']}` | {data['characteristics']} |\n"
        )

    content += """
---

## 4. Producer Export Leverage (Sonic Architecture Imbalance)

Which countries act as **net exporters** of musical architecture to the rest of the world?

| Country | Producer Count | Export Ratio | Archetype | Key Global Clients |
| :--- | :--- | :--- | :--- | :--- |
"""
    for pe in producer_leverage:
        clients = ", ".join(pe["foreign_clients_sample"]) or "Domestic Focused"
        content += f"| **{pe['country']}** | {pe['producers_count']} | `{pe['export_leverage_ratio']}%` | {pe['archetype']} | {clients} |\n"

    content += """
---

## 5. Cross-Border Collaboration Corridors

Top international collaboration highways identified in the graph:

| International Corridor | Collaboration Weight / Frequency |
| :--- | :--- |
"""
    for c in cross_border.get("top_cross_border_corridors", []):
        content += (
            f"| **{c['corridor']}** | `{c['collaboration_count']} major releases` |\n"
        )

    content += """
---

## 6. Machine-Learned Forecasts: Emergent Cross-Border Collaborations

Top predicted upcoming international partnerships (Adamic-Adar & Jaccard neighborhood affinity):

| Artist 1 | Artist 2 | Affinity Score | Likelihood |
| :--- | :--- | :--- | :--- |
"""
    for pred in predictions[:8]:
        content += f"| **{pred['artist_1']}** | **{pred['artist_2']}** | `{pred['affinity_score']}` | {pred['likelihood']} |\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
