"""Music Industry Knowledge Graph API Router."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from agies.api.auth import APIKeyInfo, get_api_key
from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.micro_corpus import MicroEcosystemCorpusExtractor
from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder
from agies.graph.city_connects import CityIndustryConnectsEnricher
from agies.graph.enrichment import AcousticGraphEnricher

router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])

# Shared graph instance initialized with global corpus, micro pathways, geo hierarchy, and acoustic enrichment
_graph_instance = MusicIndustryGraph()
_corpus_extractor = GlobalMusicIndustryCorpusExtractor()
_c_entities, _c_edges = _corpus_extractor.extract()
_graph_instance.ingest(_c_entities, _c_edges)

_micro_extractor = MicroEcosystemCorpusExtractor()
_m_entities, _m_edges = _micro_extractor.extract()
_graph_instance.ingest(_m_entities, _m_edges)

_geo_builder = GeoTaxonomyHierarchyBuilder()
_g_entities, _g_edges = _geo_builder.build_hierarchy()
_graph_instance.ingest(_g_entities, _g_edges)

_city_enricher = CityIndustryConnectsEnricher()
_city_enricher.enrich_city_connects(_graph_instance)

_enricher = AcousticGraphEnricher()
_enricher.enrich_graph(_graph_instance)


@router.get("/summary", summary="Get knowledge graph summary statistics")
async def get_graph_summary(key: APIKeyInfo = Depends(get_api_key)) -> Dict[str, Any]:
    """Retrieve node counts, relationship totals, and entity breakdown."""
    return _graph_instance.summary()


@router.get("/artists", summary="List artists in the knowledge graph")
async def list_artists(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    classified_subgenre: Optional[str] = Query(
        None, description="Filter by classified subgenre (arXiv:2110.08862)"
    ),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Get list of all artist nodes with their genres, acoustic subgenres, and metadata."""
    artist_ids = _graph_instance.get_artists()
    artists = []
    for aid in artist_ids:
        data = _graph_instance.graph.nodes[aid]
        if genre and genre.lower() not in [g.lower() for g in data.get("genres", [])]:
            continue
        if (
            classified_subgenre
            and data.get("classified_subgenre", "").lower()
            != classified_subgenre.lower()
        ):
            continue
        artists.append({"id": aid, **data})
    return artists


@router.get("/ecosystem/{artist_id}", summary="Get full artist ecosystem profile")
async def get_artist_ecosystem(
    artist_id: str,
    key: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, Any]:
    """Retrieve full ecosystem profile (labels, agencies, studios, producers, collaborators) for a given artist."""
    try:
        return _graph_instance.get_artist_ecosystem(artist_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Artist '{artist_id}' not found in knowledge graph.",
        )


@router.get(
    "/acoustic-similarity/{artist_id}", summary="Get acoustically similar artists"
)
async def get_acoustic_similarity(
    artist_id: str,
    limit: int = Query(5, ge=1, le=20, description="Max similar artists to return"),
    key: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, Any]:
    """Find acoustically similar artists based on Mel-Spectrogram & Tempogram cosine similarity (arXiv:2110.08862)."""
    graph = _graph_instance.graph
    if artist_id not in graph:
        raise HTTPException(
            status_code=404,
            detail=f"Artist '{artist_id}' not found in knowledge graph.",
        )

    artist_data = graph.nodes[artist_id]
    similar_peers = []

    for u, v, d in graph.edges(artist_id, data=True):
        if d.get("rel_type") == "ACOUSTIC_SIMILARITY":
            peer_id = v if u == artist_id else u
            peer_data = graph.nodes.get(peer_id, {})
            similar_peers.append(
                {
                    "artist_id": peer_id,
                    "name": peer_data.get("name", peer_id),
                    "acoustic_similarity_score": d.get("weight", 0.0),
                    "classified_subgenre": peer_data.get("classified_subgenre"),
                    "detected_bpm": peer_data.get("detected_bpm"),
                }
            )

    similar_peers.sort(key=lambda x: x["acoustic_similarity_score"], reverse=True)
    return {
        "source_artist": {
            "id": artist_id,
            "name": artist_data.get("name", artist_id),
            "classified_subgenre": artist_data.get("classified_subgenre"),
            "detected_bpm": artist_data.get("detected_bpm"),
        },
        "similar_artists": similar_peers[:limit],
    }


@router.get(
    "/hierarchy/geo",
    summary="Get hierarchical Geo-Spatial breakdown (Country -> State -> City -> District)",
)
async def get_geo_hierarchy(
    country: Optional[str] = Query(
        None,
        description="Filter by Country name (e.g. Germany, United Kingdom, United States)",
    ),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Retrieve multi-level nested Geo-Spatial hierarchy."""
    graph = _graph_instance.graph
    countries = [
        {"id": n, **d}
        for n, d in graph.nodes(data=True)
        if d.get("attributes", {}).get("category") == "Country"
    ]
    if country:
        countries = [
            c for c in countries if country.lower() in c.get("name", "").lower()
        ]

    result = []
    for c in countries:
        cid = c["id"]
        # Find states
        states = []
        for u, v, d in graph.edges(data=True):
            if (
                v == cid
                and d.get("metadata", {}).get("hierarchy") == "state_to_country"
            ):
                state_data = graph.nodes[u]
                # Find cities
                cities = []
                for cu, cv, cd in graph.edges(data=True):
                    if (
                        cv == u
                        and cd.get("metadata", {}).get("hierarchy") == "city_to_state"
                    ):
                        city_data = graph.nodes[cu]
                        # Find districts
                        districts = [
                            {"id": du, "name": graph.nodes[du].get("name", du)}
                            for du, dv, dd in graph.edges(data=True)
                            if dv == cu
                            and dd.get("metadata", {}).get("hierarchy")
                            == "district_to_city"
                        ]
                        cities.append(
                            {
                                "id": cu,
                                "name": city_data.get("name", cu),
                                "districts": districts,
                            }
                        )
                states.append(
                    {"id": u, "name": state_data.get("name", u), "cities": cities}
                )
        result.append(
            {"country_id": cid, "country_name": c.get("name"), "states": states}
        )
    return result


@router.get("/hierarchy/genres", summary="Get hierarchical Genre & Subgenre Taxonomy")
async def get_genre_hierarchy(
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Retrieve Root Genres -> Subgenres -> Micro-Genres taxonomy tree."""
    graph = _graph_instance.graph
    root_genres = [
        {"id": n, "name": d.get("name", n)}
        for n, d in graph.nodes(data=True)
        if d.get("attributes", {}).get("taxonomy_level") == "Root Genre"
    ]
    tree = []
    for rg in root_genres:
        rid = rg["id"]
        subgenres = []
        for u, v, d in graph.edges(data=True):
            if (
                v == rid
                and d.get("metadata", {}).get("hierarchy") == "subgenre_to_parent"
            ):
                sub_data = graph.nodes[u]
                # Find micro-genres
                micro_genres = [
                    {"id": mu, "name": graph.nodes[mu].get("name", mu)}
                    for mu, mv, md in graph.edges(data=True)
                    if mv == u
                    and md.get("metadata", {}).get("hierarchy") == "subgenre_to_parent"
                ]
                subgenres.append(
                    {
                        "id": u,
                        "name": sub_data.get("name", u),
                        "micro_genres": micro_genres,
                    }
                )
        tree.append(
            {
                "root_genre_id": rid,
                "root_genre_name": rg["name"],
                "subgenres": subgenres,
            }
        )
    return tree


@router.get(
    "/city-connects/{city_id}",
    summary="Get city-level industry infrastructure and anchors",
)
async def get_city_industry_connects(
    city_id: str,
    key: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, Any]:
    """Retrieve all artists, studios, labels, producers, festivals, and corridors anchored to a city."""
    try:
        return _city_enricher.get_city_profile(_graph_instance, city_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/city-corridors",
    summary="Get top global inter-city creative and business corridors",
)
async def list_inter_city_corridors(
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Retrieve global inter-city creative trade highways (e.g. Stockholm <-> LA, Berlin <-> London)."""
    corridors = []
    for c1, c2, corridor_name, weight in _city_enricher.INTER_CITY_CORRIDORS:
        name1 = _graph_instance.graph.nodes.get(c1, {}).get("name", c1)
        name2 = _graph_instance.graph.nodes.get(c2, {}).get("name", c2)
        corridors.append(
            {
                "city_1": name1,
                "city_2": name2,
                "corridor_name": corridor_name,
                "corridor_strength": weight,
            }
        )
    return corridors
