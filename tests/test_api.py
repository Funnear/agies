"""Unit and Integration Tests for AGIES REST API."""

from fastapi.testclient import TestClient
from agies.api.app import app

client = TestClient(app)

VALID_KEY = "agies_test_key_123"
ADMIN_KEY = "agies_dev_master_key_999"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_unauthorized_access_without_api_key():
    response = client.get("/api/v1/graph/summary")
    assert response.status_code == 401
    assert "Missing API Key" in response.json()["detail"]


def test_forbidden_access_with_invalid_api_key():
    response = client.get(
        "/api/v1/graph/summary", headers={"X-API-Key": "invalid_key_xxx"}
    )
    assert response.status_code == 403
    assert "Invalid or revoked" in response.json()["detail"]


def test_graph_summary_endpoint():
    response = client.get("/api/v1/graph/summary", headers={"X-API-Key": VALID_KEY})
    assert response.status_code == 200
    data = response.json()
    assert "total_nodes" in data
    assert "total_edges" in data
    assert data["total_nodes"] > 30


def test_list_artists_endpoint():
    response = client.get("/api/v1/graph/artists", headers={"X-API-Key": VALID_KEY})
    assert response.status_code == 200
    artists = response.json()
    assert len(artists) > 10
    names = [a["name"] for a in artists]
    assert "Taylor Swift" in names
    assert "Drake" in names


def test_artist_ecosystem_endpoint():
    response = client.get(
        "/api/v1/graph/ecosystem/art_taylor", headers={"X-API-Key": VALID_KEY}
    )
    assert response.status_code == 200
    eco = response.json()
    assert eco["artist"]["name"] == "Taylor Swift"
    assert len(eco["labels"]) >= 1
    assert len(eco["agencies"]) >= 1


def test_analytics_power_brokers():
    response = client.get(
        "/api/v1/analytics/power-brokers?top_k=5", headers={"X-API-Key": VALID_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert "by_pagerank" in data
    assert len(data["by_pagerank"]) == 5


def test_analytics_structural_holes():
    response = client.get(
        "/api/v1/analytics/structural-holes?top_k=4", headers={"X-API-Key": VALID_KEY}
    )
    assert response.status_code == 200
    brokers = response.json()
    assert len(brokers) == 4
    assert "network_constraint" in brokers[0]


def test_analytics_predictions():
    response = client.get(
        "/api/v1/analytics/predictions?top_k=5", headers={"X-API-Key": VALID_KEY}
    )
    assert response.status_code == 200
    preds = response.json()
    assert len(preds) > 0
    assert "artist_1" in preds[0]
    assert "artist_2" in preds[0]
    assert "affinity_score" in preds[0]


def test_audio_sources_list():
    response = client.get("/api/v1/audio/sources", headers={"X-API-Key": VALID_KEY})
    assert response.status_code == 200
    sources = response.json()["available_sources"]
    assert "jamendo" in sources
    assert "archive_org" in sources
    assert "wikimedia_commons" in sources


def test_key_issuance_admin_protected():
    # Regular user cannot issue keys
    forbidden = client.post(
        "/api/v1/keys/issue",
        json={"owner": "Hacker", "tier": "admin"},
        headers={"X-API-Key": VALID_KEY},
    )
    assert forbidden.status_code == 403

    # Admin can issue keys
    success = client.post(
        "/api/v1/keys/issue",
        json={"owner": "Production Client", "tier": "pro", "rate_limit_rpm": 300},
        headers={"X-API-Key": ADMIN_KEY},
    )
    assert success.status_code == 200
    issued_key_info = success.json()
    assert issued_key_info["owner"] == "Production Client"
    assert issued_key_info["tier"] == "pro"
    new_key = issued_key_info["key"]

    # Newly issued key can access the API
    test_req = client.get("/api/v1/graph/summary", headers={"X-API-Key": new_key})
    assert test_req.status_code == 200


def test_classifier_info_endpoint():
    response = client.get(
        "/api/v1/audio/classifier/info", headers={"X-API-Key": VALID_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert "model_type" in data
    assert "supported_genres" in data
    assert "classical" in data["supported_genres"]


def test_audio_classify_endpoint():
    response = client.post(
        "/api/v1/audio/classify",
        json={
            "features": {
                "rms_energy": 0.05,
                "spectral_centroid": 950.0,
                "brightness_ratio": 0.08,
                "zero_crossing_rate": 0.03,
                "low_energy_fraction": 0.65,
                "spectral_rolloff": 2100.0,
                "spectral_flux": 0.01,
                "rhythm_regularity": 0.25,
            }
        },
        headers={"X-API-Key": VALID_KEY},
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_genre" in data
    assert "confidence" in data
    assert "probabilities" in data
    assert data["predicted_genre"] in ["classical", "ambient"]


def test_acoustic_similarity_endpoint():
    response = client.get(
        "/api/v1/graph/acoustic-similarity/art_kraftwerk?limit=3",
        headers={"X-API-Key": VALID_KEY},
    )
    assert response.status_code == 200
    data = response.json()
    assert "source_artist" in data
    assert data["source_artist"]["name"] == "Kraftwerk"
    assert "similar_artists" in data


def test_memory_graphify_and_recall_endpoints():
    # 1. Graphify text into memory
    post_res = client.post(
        "/api/v1/memory/graphify",
        json={
            "text": "Brian Eno worked extensively at Hansa Studios Berlin producing ambient and electronic music.",
            "session_id": "test_sess",
        },
        headers={"X-API-Key": VALID_KEY},
    )
    assert post_res.status_code == 200
    assert "episode_id" in post_res.json()

    # 2. Recall memory
    recall_res = client.get(
        "/api/v1/memory/recall?q=Brian+Eno+Berlin&hops=2&top_k=5",
        headers={"X-API-Key": VALID_KEY},
    )
    assert recall_res.status_code == 200
    data = recall_res.json()
    assert data["recalled_nodes_count"] >= 1

    summary_res = client.get("/api/v1/memory/summary", headers={"X-API-Key": VALID_KEY})
    assert summary_res.status_code == 200
    assert summary_res.json()["total_nodes"] >= 1


def test_emerging_artist_pathway_endpoint():
    response = client.get(
        "/api/v1/analytics/emerging-pathway?genre=techno&country=Germany&stage=bedroom_producer",
        headers={"X-API-Key": VALID_KEY},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["target_genre"] == "Techno"
    assert "distribution_stack" in data
    assert "showcase_festivals" in data
    assert "critical_traps_to_avoid" in data


def test_geo_and_genre_hierarchy_endpoints():
    # 1. Geo Hierarchy
    geo_res = client.get(
        "/api/v1/graph/hierarchy/geo?country=Germany", headers={"X-API-Key": VALID_KEY}
    )
    assert geo_res.status_code == 200
    geo_data = geo_res.json()
    assert len(geo_data) >= 1
    assert geo_data[0]["country_name"] == "Germany"
    assert len(geo_data[0]["states"]) >= 1

    # 2. Genre Hierarchy
    genre_res = client.get(
        "/api/v1/graph/hierarchy/genres", headers={"X-API-Key": VALID_KEY}
    )
    assert genre_res.status_code == 200
    genre_data = genre_res.json()
    assert len(genre_data) >= 1
    root_names = [g["root_genre_name"] for g in genre_data]
    assert any("Electronic" in r or "Hip-Hop" in r for r in root_names)


def test_city_connects_and_corridors_endpoints():
    # 1. City Connects Profile for Berlin
    city_res = client.get(
        "/api/v1/graph/city-connects/city_berlin", headers={"X-API-Key": VALID_KEY}
    )
    assert city_res.status_code == 200
    city_data = city_res.json()
    assert city_data["city_name"] == "Berlin"
    assert "studios" in city_data
    assert "record_labels" in city_data
    assert "inter_city_corridors" in city_data

    # 2. Inter-City Corridors
    corridor_res = client.get(
        "/api/v1/graph/city-corridors", headers={"X-API-Key": VALID_KEY}
    )
    assert corridor_res.status_code == 200
    corridors = corridor_res.json()
    assert len(corridors) >= 5
    corridor_names = [c["corridor_name"] for c in corridors]
    assert any("Pop" in n or "Electronic" in n for n in corridor_names)


def test_venue_endpoints():
    # 1. List Venues
    venues_res = client.get(
        "/api/v1/venues/list?city=Berlin", headers={"X-API-Key": VALID_KEY}
    )
    assert venues_res.status_code == 200
    venues = venues_res.json()
    assert len(venues) >= 2
    assert any(v["id"] == "ven_berghain" for v in venues)

    # 2. Recommend Artists for Berghain
    recs_res = client.get(
        "/api/v1/venues/recommend-artists/ven_berghain?top_k=4",
        headers={"X-API-Key": VALID_KEY},
    )
    assert recs_res.status_code == 200
    recs = recs_res.json()
    assert len(recs) >= 1
    assert recs[0]["match_score"] > 0.70

    # 3. Artist Booking Contact Card
    contact_res = client.get(
        "/api/v1/venues/contact/art_kraftwerk", headers={"X-API-Key": VALID_KEY}
    )
    assert contact_res.status_code == 200
    contact = contact_res.json()
    assert contact["artist_name"] == "Kraftwerk"
    assert "@" in contact["booking_email"]

    # 4. Dispatch Booking Inquiry
    inq_res = client.post(
        "/api/v1/venues/inquire",
        json={
            "venue_id": "ven_tresor",
            "venue_name": "Tresor Berlin",
            "artist_id": "art_kraftwerk",
            "event_date": "2026-12-05",
            "offer_fee_currency": "EUR",
            "offer_fee_amount": 5000.0,
            "set_type": "Live Set",
            "expected_attendance": 800,
            "promoter_name": "Tresor Promoter",
            "promoter_email": "booking@tresorberlin.com",
        },
        headers={"X-API-Key": VALID_KEY},
    )
    assert inq_res.status_code == 200
    receipt = inq_res.json()
    assert receipt["status"] == "dispatched"
    assert "5,000.00 EUR" in receipt["offer_fee"]
