from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from agies.api.auth import APIKeyInfo, get_api_key
from agies.audio.artist_crawler import ArtistWebsiteHarvester

router = APIRouter(prefix="/discovery", tags=["Artist & Venue Discovery"])
harvester = ArtistWebsiteHarvester()


class CrawlWebsiteRequest(BaseModel):
    """Payload to crawl an artist's website and extract audio snippets."""

    website_url: str = Field(
        ...,
        examples=["https://tychomusic.com"],
        description="Public artist website URL",
    )
    artist_name: Optional[str] = Field(
        None, examples=["Tycho"], description="Artist / Band alias"
    )
    home_city: Optional[str] = Field(
        None, examples=["San Francisco"], description="Artist home territory"
    )
    genre_hint: Optional[str] = Field(
        None, examples=["Ambient Electronic"], description="Primary subgenre"
    )


@router.post(
    "/crawl-artist-website",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Crawl an artist website, download audio snippets, and generate dual venue discovery",
)
async def crawl_artist_website(
    payload: CrawlWebsiteRequest,
    key_info: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, Any]:
    """Crawl artist website, extract audio snippets, calculate Mel-Tempograms, and compute matched venues."""
    profile = harvester.crawl_artist_website(
        website_url=payload.website_url,
        artist_name=payload.artist_name,
        home_city=payload.home_city,
        genre_hint=payload.genre_hint,
    )
    from dataclasses import asdict

    return asdict(profile)


@router.get(
    "/artist-feed",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Get verified artist website discovery feed with downloadable audio snippets",
)
async def get_artist_discovery_feed(
    key_info: APIKeyInfo = Depends(get_api_key),
) -> List[Dict[str, Any]]:
    """Retrieve pre-harvested discovery feed of artists hosting websites and audio snippets."""
    return harvester.get_discovery_feed()
