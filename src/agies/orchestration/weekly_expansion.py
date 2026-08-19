"""Weekly Continuous Expansion & Exponential Growth Orchestration Engine.

Orchestrates all 6 core expansion axes in an automated weekly cycle:
1. Live Open Data Ingestion (MusicBrainz, Wikidata, Discogs, Showcase Circuits)
2. Hierarchical Geo & Grassroots Micro-Ecosystem Ingestion
3. Exponential Audio Corpus Harvesting & Acoustic Feature Extraction (arXiv:2110.08862)
4. Knowledge Graph Acoustic Enrichment (Subgenre classification & cosine similarity)
5. Graph Machine Learning (Node2Vec structural embeddings & Predictive A&R)
6. Enterprise Graph Exporters (Neo4j Cypher, GraphML, JSON, and Interactive HTML)
"""

from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import time
from typing import Any, Dict, Optional

from agies.analytics.gnn_predictive import GNNPredictiveAREngine
from agies.audio.growth import ExponentialAudioCorpusEngine
from agies.graph.builder import MusicIndustryGraph
from agies.graph.city_connects import CityIndustryConnectsEnricher
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.density import GraphDensityInclusionEngine
from agies.graph.enrichment import AcousticGraphEnricher
from agies.graph.exporters.neo4j_exporter import Neo4jGraphExporter
from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder
from agies.graph.ingestion import (
    DiscogsBeatportConnector,
    ShowcaseFestivalsConnector,
    WikidataSPARQLConnector,
)
from agies.graph.micro_corpus import MicroEcosystemCorpusExtractor
from agies.visualization.interactive import render_interactive_graph

logger = logging.getLogger("agies.orchestration.weekly_expansion")


class WeeklyKnowledgeGraphExpander:
    """Master orchestrator for continuous weekly knowledge graph and audio corpus expansion."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.project_root = Path(__file__).resolve().parent.parent.parent.parent
        self.data_dir = Path(data_dir or (self.project_root / "data" / "corpus"))
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def run_weekly_cycle(self, target_audio_per_genre: int = 15) -> Dict[str, Any]:
        """Execute complete continuous expansion cycle."""
        start_time = time.time()
        cycle_timestamp = datetime.now(timezone.utc).isoformat()
        logger.info(
            "=== STARTING WEEKLY AUTONOMOUS EXPANSION CYCLE (%s) ===", cycle_timestamp
        )

        industry_graph = MusicIndustryGraph()

        # Step 1: Ingest Global Core Corpus
        logger.info("-> 1/6 Ingesting Global Core Multi-Continental Corpus...")
        c_ext = GlobalMusicIndustryCorpusExtractor()
        c_ent, c_edg = c_ext.extract()
        industry_graph.ingest(c_ent, c_edg)

        # Step 2: Ingest Micro-Ecosystem Pathways & Geo/Genre Hierarchy
        logger.info("-> 2/6 Ingesting Micro-Ecosystems and Geo/Genre Hierarchies...")
        m_ext = MicroEcosystemCorpusExtractor()
        m_ent, m_edg = m_ext.extract()
        industry_graph.ingest(m_ent, m_edg)

        geo_b = GeoTaxonomyHierarchyBuilder()
        g_ent, g_edg = geo_b.build_hierarchy()
        industry_graph.ingest(g_ent, g_edg)

        city_enr = CityIndustryConnectsEnricher()
        city_enr.enrich_city_connects(industry_graph)

        # Step 3: Ingest Live Data Connectors
        logger.info(
            "-> 3/6 Ingesting Live Data Connectors (MusicBrainz, Wikidata, Discogs, Festivals)..."
        )
        for connector in [
            WikidataSPARQLConnector(),
            DiscogsBeatportConnector(),
            ShowcaseFestivalsConnector(),
        ]:
            try:
                for fn_name in [
                    "fetch_historic_studios",
                    "fetch_electronic_subgenre_releases",
                    "fetch_showcase_circuits",
                ]:
                    if hasattr(connector, fn_name):
                        ent, edg = getattr(connector, fn_name)()
                        industry_graph.ingest(ent, edg)
            except Exception as e:
                logger.warning("Connector step notice: %s", e)

        # Step 4: Exponential Audio Corpus Growth & Feature Extraction
        logger.info(
            "-> 4/6 Exponentially Growing Audio Corpus & Mel-Tempogram Classification..."
        )
        audio_engine = ExponentialAudioCorpusEngine()
        audio_results = audio_engine.expand_audio_corpus(
            industry_graph, target_tracks_per_genre=target_audio_per_genre
        )

        # Step 5: Deep Mel-Tempogram Graph Enrichment
        logger.info(
            "-> 5/6 Running Deep Mel-Tempogram Acoustic Enrichment (arXiv:2110.08862)..."
        )
        enricher = AcousticGraphEnricher()
        enrichment_results = enricher.enrich_graph(industry_graph)

        # Step 5.5: Multi-Dimensional Graph Density & Structural Inclusion
        logger.info(
            "-> Ingesting Multi-Dimensional Inclusion Closures & Hardware Synthesizer Gear..."
        )
        density_engine = GraphDensityInclusionEngine()
        density_results = density_engine.enrich_density(industry_graph)

        # Step 6: Graph Machine Learning (Node2Vec & Predictive A&R)
        logger.info(
            "-> 6/6 Computing Graph ML Embeddings & Predictive A&R Forecasts..."
        )
        gnn_engine = GNNPredictiveAREngine()
        gnn_engine.fit_embeddings(industry_graph)
        breakout_artists = gnn_engine.predict_breakout_ar_candidates(
            industry_graph, top_k=6
        )

        # Step 7: Multi-Format Exports (Cypher, GraphML, JSON, HTML)
        logger.info(
            "-> Generating Enterprise Graph Database Artifacts & Visualizations..."
        )
        neo4j_exporter = Neo4jGraphExporter(output_dir=self.data_dir)
        cypher_file = neo4j_exporter.export_cypher(industry_graph)

        summary = industry_graph.summary()
        graph_json_path = self.data_dir / "music_industry_corpus.json"
        nodes_data = [{"id": n, **d} for n, d in industry_graph.graph.nodes(data=True)]
        edges_data = [
            {"source": u, "target": v, **d}
            for u, v, d in industry_graph.graph.edges(data=True)
        ]
        graph_dict = {"nodes": nodes_data, "edges": edges_data, "summary": summary}
        with open(graph_json_path, "w", encoding="utf-8") as f:
            json.dump(graph_dict, f, indent=2)

        html_path = self.data_dir / "corpus_interactive_network.html"
        render_interactive_graph(industry_graph, str(html_path))

        elapsed = round(time.time() - start_time, 2)
        logger.info(
            "=== WEEKLY EXPANSION COMPLETE IN %.2fs: %d Nodes | %d Edges ===",
            elapsed,
            summary["total_nodes"],
            summary["total_edges"],
        )

        return {
            "cycle_timestamp": cycle_timestamp,
            "elapsed_seconds": elapsed,
            "total_nodes": summary["total_nodes"],
            "total_edges": summary["total_edges"],
            "audio_corpus_expansion": audio_results,
            "acoustic_enrichment": enrichment_results,
            "density_inclusion": density_results,
            "predictive_breakout_artists": breakout_artists,
            "exported_cypher_file": str(cypher_file),
            "exported_json_file": str(graph_json_path),
            "exported_interactive_html": str(html_path),
        }
