"""Unit tests for Geo-Spatial and Musical Taxonomy Hierarchy."""

from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder


def test_geo_taxonomy_hierarchy_construction():
    builder = GeoTaxonomyHierarchyBuilder()
    entities, edges = builder.build_hierarchy()

    assert len(entities) >= 50
    assert len(edges) >= 50

    # Test Country -> State -> City -> District
    entity_ids = {e.id for e in entities}
    assert "geo_de" in entity_ids
    assert "state_de_be" in entity_ids
    assert "city_berlin" in entity_ids
    assert "distr_fhain_xberg" in entity_ids

    # Test Musical Taxonomy
    assert "tax_electronic" in entity_ids
    assert "tax_techno" in entity_ids
    assert "tax_industrial_techno" in entity_ids
    assert "tax_hiphop" in entity_ids
    assert "tax_westcoast_gfunk" in entity_ids


def test_hierarchy_relationships():
    builder = GeoTaxonomyHierarchyBuilder()
    _, edges = builder.build_hierarchy()

    # Verify state-to-country and district-to-city hierarchy edges
    hierarchies = {e.metadata.get("hierarchy") for e in edges if e.metadata}
    assert "state_to_country" in hierarchies
    assert "city_to_state" in hierarchies
    assert "district_to_city" in hierarchies
    assert "subgenre_to_parent" in hierarchies
