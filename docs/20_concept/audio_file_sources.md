# Audio File Sources

Research and implementation guide for free, royalty-free, and open-licensed audio file providers.

Resolves [Issue #4: Explore AUDIO FILE sources](https://github.com/Funnear/agies/issues/4).

## Requirements & Compliance Matrix

| Provider | License Type | API Auth | GDPR / EU Law Compliant | Base URL / Documentation |
| --- | --- | --- | --- | --- |
| **Jamendo** | Creative Commons (CC-BY, CC-BY-SA, CC0) | Client ID (Free) | Yes (HQ in Luxembourg, EU) | [developer.jamendo.com](https://developer.jamendo.com/v3.0) |
| **Internet Archive** | Public Domain, Creative Commons | None (Open REST API) | Yes (US 501(c)(3) non-profit, no PII collected) | [archive.org/developers](https://archive.org/developers/) |
| **Freesound** | Creative Commons (CC0, CC-BY, CC-BY-NC) | API Key (Free) | Yes (Universitat Pompeu Fabra, Spain, EU) | [freesound.org/docs/api](https://freesound.org/docs/api/) |

## Architecture & Design Patterns

The `agies.audio` module follows SOLID design principles:

* **Interface Segregation (ISP):** All providers implement the lightweight abstract
  interface `BaseAudioSource` in [`src/agies/audio/base.py`](../../src/agies/audio/base.py).
* **Dependency Inversion (DIP):** The orchestrator `AudioSourcesManager` in
  [`src/agies/audio/manager.py`](../../src/agies/audio/manager.py) consumes `BaseAudioSource` abstractions.
* **Single Responsibility (SRP):** Pydantic data model `AudioTrack` in
  [`src/agies/audio/models.py`](../../src/agies/audio/models.py) unifies metadata across providers.

## Usage Example

```python
from agies.audio.manager import AudioSourcesManager
from agies.audio.archive import ArchiveOrgSource
from agies.audio.jamendo import JamendoSource
from agies.audio.freesound import FreesoundSource

# Initialize and register sources
manager = AudioSourcesManager()
manager.register(ArchiveOrgSource())
manager.register(JamendoSource(client_id="YOUR_JAMENDO_CLIENT_ID"))
manager.register(FreesoundSource(api_key="YOUR_FREESOUND_API_KEY"))

# Search across all registered providers
tracks = manager.search(query="electronic", genre="techno", limit_per_provider=5)

for track in tracks:
    print(f"[{track.provider}] {track.artist} - {track.title} ({track.license})")
    print(f"Stream: {track.stream_url}")
```
