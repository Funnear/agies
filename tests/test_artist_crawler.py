"""Unit tests for Artist Website Harvester & Dual Discovery Engine."""

from fastapi.testclient import TestClient
import pytest

from agies.api.app import create_app
from agies.audio.artist_crawler import ArtistWebsiteHarvester


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_artist_website_harvester_seed_feed():
    harvester = ArtistWebsiteHarvester()
    feed = harvester.get_discovery_feed()
    assert len(feed) >= 4
    for artist in feed:
        assert "artist_name" in artist
        assert "website_url" in artist
        assert len(artist["audio_snippets"]) >= 1
        assert len(artist["matched_venues"]) >= 1
        assert artist["audio_snippets"][0]["is_downloaded"] is True


def test_crawl_artist_website_direct():
    harvester = ArtistWebsiteHarvester()
    profile = harvester.crawl_artist_website(
        website_url="https://tychomusic.com",
        artist_name="Tycho",
        home_city="San Francisco",
        genre_hint="house",
    )
    assert profile.artist_name == "Tycho"
    assert len(profile.audio_snippets) >= 2
    assert profile.acoustic_signature["classified_subgenre"] == "house"
    assert len(profile.matched_venues) >= 1
    assert profile.matched_venues[0]["acoustic_fit_score"] > 70.0


def test_discovery_api_endpoints(client):
    headers = {"X-API-Key": "agies_test_key_123"}

    # 1. Get discovery feed
    res = client.get("/api/v1/discovery/artist-feed", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 4
    assert "nils-frahm" in [a["artist_slug"] for a in data]

    # 2. Crawl artist website
    payload = {
        "website_url": "https://bicepmusic.com",
        "artist_name": "BICEP",
        "home_city": "London",
        "genre_hint": "techno",
    }
    res_crawl = client.post(
        "/api/v1/discovery/crawl-artist-website", json=payload, headers=headers
    )
    assert res_crawl.status_code == 200
    crawl_data = res_crawl.json()
    assert crawl_data["artist_name"] == "BICEP"
    assert len(crawl_data["audio_snippets"]) >= 2
    assert len(crawl_data["matched_venues"]) >= 1
