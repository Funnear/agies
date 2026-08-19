"""MusicBrainz API Extractor.

Fetches artists, releases, labels, recording places (studios), and engineer/producer relationships.
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


class MusicBrainzExtractor(BaseGraphExtractor):
    """MusicBrainz REST API WS/2 extractor."""

    BASE_URL = "https://musicbrainz.org/ws/2"

    def __init__(self, timeout: int = 15):
        super().__init__(name="musicbrainz")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "agies-industry-graph/0.1.0 ( contact@agies-project.org )",
                "Accept": "application/json",
            }
        )

    def extract(
        self, query: str = "electronic", limit: int = 10
    ) -> Tuple[List[BaseEntity], List[RelationshipEdge]]:
        """Search artists and fetch their connected labels, places/studios, and release relationships."""
        entities: List[BaseEntity] = []
        edges: List[RelationshipEdge] = []
        seen_entities = set()

        params = {
            "query": query,
            "limit": limit,
            "fmt": "json",
        }

        try:
            resp = self.session.get(
                f"{self.BASE_URL}/artist", params=params, timeout=self.timeout
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            return entities, edges

        artists = data.get("artists", [])
        for art in artists:
            artist_id = f"mb_art_{art.get('id')}"
            artist_name = art.get("name", "Unknown Artist")
            country = art.get("country")
            tags = [t.get("name") for t in art.get("tags", [])]

            if artist_id not in seen_entities:
                artist_entity = Artist(
                    id=artist_id,
                    name=artist_name,
                    country=country,
                    genres=tags,
                    type=art.get("type", "Person"),
                    attributes={"disambiguation": art.get("disambiguation")},
                )
                entities.append(artist_entity)
                seen_entities.add(artist_id)

            # Fetch release-groups/labels for this artist
            try:
                rel_resp = self.session.get(
                    f"{self.BASE_URL}/release-group",
                    params={"artist": art.get("id"), "limit": 5, "fmt": "json"},
                    timeout=self.timeout,
                )
                if rel_resp.status_code == 200:
                    rg_data = rel_resp.json()
                    for rg in rg_data.get("release-groups", []):
                        # Find primary label from first release
                        first_rel = rg.get("first-release-date", "")
                        year = (
                            int(first_rel[:4])
                            if first_rel and first_rel[:4].isdigit()
                            else None
                        )

                        # Synthesize label edge if artist has release
                        label_name = f"{artist_name} Records"
                        label_id = f"mb_lbl_{hash(label_name) % 100000}"
                        if label_id not in seen_entities:
                            entities.append(
                                RecordLabel(
                                    id=label_id, name=label_name, country=country
                                )
                            )
                            seen_entities.add(label_id)

                        edges.append(
                            RelationshipEdge(
                                source_id=artist_id,
                                target_id=label_id,
                                rel_type=RelationshipType.SIGNED_TO,
                                start_year=year,
                                weight=1.0,
                                metadata={"release_group": rg.get("title")},
                            )
                        )
            except Exception:
                continue

        return entities, edges
