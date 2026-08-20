"""Unit tests for Deep Genre Taxonomy and Lineage Expansion Engine."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.genre_expansion import DeepGenreTaxonomyExpander


def test_genre_taxonomy_expansion():
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    initial_nodes = len(graph.graph.nodes)

    expander = DeepGenreTaxonomyExpander()
    stats = expander.expand_genre_taxonomies(graph)

    assert stats["micro_genres_added"] >= 10
    assert stats["artist_genre_bindings_added"] >= 5
    assert len(graph.graph.nodes) > initial_nodes

    # Check key micro-genres
    assert "subg_industrial_techno" in graph.graph
    assert "subg_melodic_techno" in graph.graph
    assert "subg_amapiano" in graph.graph
    assert "subg_afro_house" in graph.graph
    assert "subg_goa_trance" in graph.graph
    assert "subg_jungle_dnb" in graph.graph
    assert "subg_deep_dubstep" in graph.graph
    assert "subg_desi_hip_hop" in graph.graph
    assert "subg_flamenco_nuevo" in graph.graph

    # Check genre attributes
    amapiano_node = graph.graph.nodes["subg_amapiano"]
    assert amapiano_node["attributes"]["macro_genre"] == "House"
    assert "Soweto" in amapiano_node["attributes"]["cultural_origin"]
