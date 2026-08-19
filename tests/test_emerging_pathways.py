"""Unit tests for Emerging Artist Pathways & Micro-Insights Engine."""

from agies.analytics.emerging_artist_pathways import EmergingArtistAdvisor
from agies.graph.micro_corpus import MicroEcosystemCorpusExtractor


def test_micro_ecosystem_corpus_extraction():
    extractor = MicroEcosystemCorpusExtractor()
    entities, edges = extractor.extract()

    assert len(entities) >= 20
    assert len(edges) >= 20

    # Check for DIY platforms, curation gateways, showcase festivals
    entity_names = [e.name for e in entities]
    assert any("Bandcamp" in n for n in entity_names)
    assert any("COLORSxSTUDIOS" in n or "Boiler Room" in n for n in entity_names)
    assert any(
        "Reeperbahn Festival" in n or "The Great Escape" in n for n in entity_names
    )


def test_emerging_artist_advisor_playbook():
    advisor = EmergingArtistAdvisor()
    playbook = advisor.generate_pathway_playbook(
        genre="techno", country="Germany", career_stage="bedroom_producer"
    )

    assert playbook["target_genre"] == "Techno"
    assert playbook["target_region"] == "Germany"
    assert len(playbook["distribution_stack"]) >= 2
    assert len(playbook["curation_gateways"]) >= 2
    assert len(playbook["step_by_step_roadmap"]) == 4
    assert len(playbook["critical_traps_to_avoid"]) >= 1
    assert "GEMA" in playbook["rights_organization"]
