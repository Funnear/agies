"""Unit tests for Music Industry Knowledge Graph."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.extractors.synthetic_extractor import SyntheticIndustryExtractor
from agies.graph.schema import (
    Artist,
    RecordLabel,
    RelationshipEdge,
    RelationshipType,
    Studio,
)


def test_graph_add_and_query():
    graph = MusicIndustryGraph()

    artist = Artist(id="art_1", name="Aurora Pulse", genres=["Synthpop"])
    label = RecordLabel(id="lbl_1", name="Neon Records", is_major=False)
    studio = Studio(id="std_1", name="Starlight Sound", city="Berlin")

    graph.add_entity(artist)
    graph.add_entity(label)
    graph.add_entity(studio)

    graph.add_relationship(
        RelationshipEdge(
            source_id="art_1",
            target_id="lbl_1",
            rel_type=RelationshipType.SIGNED_TO,
            start_year=2022,
        )
    )
    graph.add_relationship(
        RelationshipEdge(
            source_id="art_1",
            target_id="std_1",
            rel_type=RelationshipType.RECORDED_AT,
        )
    )

    assert len(graph.get_artists()) == 1
    assert len(graph.get_labels()) == 1
    assert len(graph.get_studios()) == 1

    ecosystem = graph.get_artist_ecosystem("art_1")
    assert ecosystem["artist"]["name"] == "Aurora Pulse"
    assert len(ecosystem["labels"]) == 1
    assert ecosystem["labels"][0]["name"] == "Neon Records"
    assert len(ecosystem["studios"]) == 1
    assert ecosystem["studios"][0]["name"] == "Starlight Sound"


def test_synthetic_extractor_ingestion():
    extractor = SyntheticIndustryExtractor()
    entities, edges = extractor.extract()

    graph = MusicIndustryGraph()
    graph.ingest(entities, edges)

    summary = graph.summary()
    assert summary["total_nodes"] > 30
    assert summary["total_edges"] > 40
    assert summary["nodes_by_type"]["artist"] >= 15
    assert summary["nodes_by_type"]["record_label"] >= 10
    assert summary["nodes_by_type"]["agency"] >= 5
    assert summary["nodes_by_type"]["studio"] >= 5


def test_global_corpus_extractor():
    from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor

    extractor = GlobalMusicIndustryCorpusExtractor()
    entities, edges = extractor.extract()

    graph = MusicIndustryGraph()
    graph.ingest(entities, edges)

    summary = graph.summary()
    assert summary["total_nodes"] >= 80
    assert summary["total_edges"] >= 100
    assert summary["nodes_by_type"]["artist"] >= 30
    assert summary["nodes_by_type"]["record_label"] >= 20
    assert summary["nodes_by_type"]["studio"] >= 10
    assert summary["nodes_by_type"]["producer"] >= 10
