"""Behavioral & Predictive Analytics API Router."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query

from agies.api.auth import APIKeyInfo, get_api_key
from agies.api.routes.graph import _graph_instance
from agies.analytics.patterns import MusicIndustryAnalytics
from agies.analytics.advanced import AdvancedIndustryAnalytics

router = APIRouter(prefix="/analytics", tags=["Behavioral & Predictive Analytics"])

_analytics = MusicIndustryAnalytics(_graph_instance)
_adv_analytics = AdvancedIndustryAnalytics(_graph_instance)


@router.get("/power-brokers", summary="Get top power brokers & gatekeepers")
async def get_power_brokers(
    top_k: int = Query(10, ge=1, le=50),
    key: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, List[Dict[str, Any]]]:
    """Retrieve top power brokers by PageRank and Betweenness Centrality."""
    return _analytics.compute_power_brokers(top_k=top_k)


@router.get(
    "/ecosystems", summary="Detect creative sub-communities & production cliques"
)
async def get_creative_ecosystems(
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Detect modularity-based creative ecosystems and genre cliques."""
    return _analytics.detect_creative_ecosystems()


@router.get(
    "/label-mobility", summary="Analyze artist label loyalty vs. migration churn"
)
async def get_label_mobility(
    key: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, Any]:
    """Retrieve label migration rate, loyal artists, and historical label hopping events."""
    return _analytics.analyze_label_mobility()


@router.get("/studio-reliance", summary="Get Studio & Producer Reliance Index (SPRI)")
async def get_studio_reliance(
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Calculate sonic concentration index for artists."""
    return _analytics.compute_studio_reliance()


@router.get("/structural-holes", summary="Analyze Burt's network constraint & brokers")
async def get_structural_holes(
    top_k: int = Query(8, ge=1, le=30),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Identify key brokers spanning structural gaps between creative communities."""
    return _adv_analytics.analyze_structural_holes(top_k=top_k)


@router.get("/predictions", summary="Predict upcoming musical collaborations")
async def get_collaboration_predictions(
    top_k: int = Query(10, ge=1, le=50),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Forecast future artist-artist collaboration likelihood using link prediction algorithms."""
    return _adv_analytics.predict_future_collaborations(top_k=top_k)


@router.get(
    "/emerging-pathway",
    summary="Get personalized micro-pathways for starting musicians",
)
async def get_emerging_artist_pathway(
    genre: str = Query("techno", description="Musical genre or subgenre"),
    country: str = Query("Germany", description="Target region or home market"),
    stage: str = Query(
        "bedroom_producer",
        description="Career stage: bedroom_producer, local_gigging, breakthrough_ready",
    ),
    key: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, Any]:
    """Provide tailored micro-pathways, distribution stacks, showcase festivals, and acoustic targets for an emerging artist."""
    from agies.analytics.emerging_artist_pathways import EmergingArtistAdvisor

    advisor = EmergingArtistAdvisor()
    return advisor.generate_pathway_playbook(
        genre=genre, country=country, career_stage=stage
    )
