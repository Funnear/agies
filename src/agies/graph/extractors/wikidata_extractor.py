"""Wikidata SPARQL / Entity Extractor.

Extracts relationships between music artists, talent/booking agencies, record labels, and recording studios.
"""

from typing import List, Tuple
import requests
from agies.graph.extractors.base_extractor import BaseGraphExtractor
from agies.graph.schema import (
    Artist,
    BaseEntity,
    RecordLabel,
    RelationshipEdge,
    RelationshipType,
)


class WikidataExtractor(BaseGraphExtractor):
    """Wikidata SPARQL endpoint extractor for music industry relations."""

    SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

    def __init__(self, timeout: int = 20):
        super().__init__(name="wikidata")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "agies-industry-graph/0.1.0 (https://github.com/Funnear/agies)",
                "Accept": "application/sparql-results+json",
            }
        )

    def extract(
        self, query: str = "electronic", limit: int = 20
    ) -> Tuple[List[BaseEntity], List[RelationshipEdge]]:
        """Query Wikidata for musical artists and their record label / management agencies."""
        entities: List[BaseEntity] = []
        edges: List[RelationshipEdge] = []
        seen_entities = set()

        sparql_query = f"""
        SELECT ?artist ?artistLabel ?recordLabel ?recordLabelLabel ?countryLabel WHERE {{
          ?artist wdt:P31 wd:Q5;                # Instance of human
                  wdt:P106 wd:Q639669;          # Occupation: musician
                  wdt:P264 ?recordLabel.        # Record label
          OPTIONAL {{ ?artist wdt:P27 ?country. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        """

        try:
            resp = self.session.get(
                self.SPARQL_ENDPOINT,
                params={"query": sparql_query, "format": "json"},
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            return entities, edges

        bindings = data.get("results", {}).get("bindings", [])
        for b in bindings:
            art_uri = b.get("artist", {}).get("value", "")
            art_name = b.get("artistLabel", {}).get("value", "Unknown Artist")
            lbl_uri = b.get("recordLabel", {}).get("value", "")
            lbl_name = b.get("recordLabelLabel", {}).get("value", "Unknown Label")
            country = b.get("countryLabel", {}).get("value")

            art_id = f"wd_art_{art_uri.split('/')[-1]}"
            lbl_id = f"wd_lbl_{lbl_uri.split('/')[-1]}"

            if art_id not in seen_entities:
                entities.append(Artist(id=art_id, name=art_name, country=country))
                seen_entities.add(art_id)

            if lbl_id not in seen_entities:
                entities.append(RecordLabel(id=lbl_id, name=lbl_name, is_major=False))
                seen_entities.add(lbl_id)

            edges.append(
                RelationshipEdge(
                    source_id=art_id,
                    target_id=lbl_id,
                    rel_type=RelationshipType.SIGNED_TO,
                    weight=1.0,
                )
            )

        return entities, edges
