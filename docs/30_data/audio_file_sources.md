# Audio File Sources

Research and implementation guide for free, royalty-free, and open-licensed audio file providers.

Resolves [Issue #4: Explore AUDIO FILE sources](https://github.com/Funnear/agies/issues/4).

## Requirements & Compliance Matrix

| Provider | License Type | API Key Required? | Available Audio Formats | GDPR / EU Law Compliant | Base URL / Documentation |
| --- | --- | --- | --- | --- | --- |
| **Jamendo** | Creative Commons (CC-BY, CC-BY-SA, CC0) | **Yes** (Free Client ID) | MP3 (128k / 320k), OGG, FLAC | Yes (HQ in Luxembourg, EU) | [developer.jamendo.com](https://developer.jamendo.com/v3.0) |
| **Internet Archive** | Public Domain, Creative Commons | **No** (Open REST API) | MP3, FLAC, OGG, WAV, AIFF | Yes (US 501(c)(3) non-profit, no PII collected) | [archive.org/developers](https://archive.org/developers/) |
| **Freesound** | Creative Commons (CC0, CC-BY, CC-BY-NC) | **Yes** (Free API Key) | WAV, MP3, OGG, FLAC, AIFF | Yes (Universitat Pompeu Fabra, Spain, EU) | [freesound.org/docs/api](https://freesound.org/docs/api/) |

## Search Options & Format Filtering per Provider

Each provider supports query parameters and format constraints:

* **Jamendo:**
  * **Search parameters:** Full-text search (`search`), tags/genres (`tags`), duration
    (`durationbetween`), order (`order`), vocal/instrumental (`vocalinstrumental`).
  * **Format filter:** Format is specified via `audioformat` (`mp31` for MP3 128k, `mp32` for
    MP3 VBR, `ogg`, `flac`).
* **Internet Archive (`archive.org`):**
  * **Search parameters:** Lucene queries across fields (`title:`, `creator:`, `subject:`,
    `date:`, `collection:`).
  * **Format filter:** Filter audio containers via `format:` (e.g. `format:"VBR MP3"`,
    `format:"FLAC"`, `format:"Waveform Audio"`).
* **Freesound:**
  * **Search parameters:** Text queries (`query`), tags (`tag`), duration filter
    (`duration:[min TO max]`), sample rate (`samplerate:[min TO max]`), channels (`channels:`).
  * **Format filter:** Filter via `type:` in the filter string (e.g. `type:wav`, `type:mp3`,
    `type:flac`, `type:ogg`).

## Provider Registration & API Key Instructions

### 1. Jamendo API (Client ID)

1. Create a free account at [jamendo.com](https://www.jamendo.com).
2. Go to the [Jamendo Developer Portal](https://devportal.jamendo.com/).
3. Click **Create an App** and fill in your project application details.
4. Copy the generated **Client ID**.
5. Set `JAMENDO_CLIENT_ID=<your_client_id>` in your local `.env` file.

### 2. Freesound API (API Key)

1. Create a free account at [freesound.org](https://freesound.org).
2. Visit the [Freesound API Keys Page](https://freesound.org/apiv2/apply/).
3. Fill out the application form requesting API credentials for educational / OSS use.
4. Copy the assigned **Client Secret / API Token**.
5. Set `FREESOUND_API_KEY=<your_api_key>` in your local `.env` file.

> **Important:** Client IDs and API keys must be loaded from local `.env` files (or environment
> variables) and should never be hardcoded into Python source files or Jupyter notebooks.

## Architecture & Design Patterns

The `agies.audio` module follows SOLID design principles:

* **Interface Segregation (ISP):** All providers implement the lightweight abstract
  interface `BaseAudioProvider` in
  [`src/agies/audio/base_audio_provider.py`](../../src/agies/audio/base_audio_provider.py).
* **Dependency Inversion (DIP):** The search service `AudioSearchService` in
  [`src/agies/audio/search_service.py`](../../src/agies/audio/search_service.py) consumes
  `BaseAudioProvider` abstractions.
* **Single Responsibility (SRP):** The `AudioTrack` model in
  [`src/agies/audio/model_audio_track_metadata.py`](../../src/agies/audio/model_audio_track_metadata.py)
  unifies metadata across providers.
* **Domain Exception Handling:** Network and API errors are caught and converted into domain-level
  `AudioProviderError` subclasses (`AudioProviderConnectionError`,
  `AudioProviderAuthenticationError`, etc.).

## Usage Example

```python
from agies.audio.provider_archive_org import ProviderArchiveOrg
from agies.audio.provider_freesound import ProviderFreesound
from agies.audio.provider_jamendo import ProviderJamendo
from agies.audio.search_service import AudioSearchService

# Initialize search service
service = AudioSearchService()

# Register providers (API keys loaded from environment / .env)
service.register(ProviderArchiveOrg())
service.register(ProviderJamendo(client_id="YOUR_JAMENDO_CLIENT_ID"))
service.register(ProviderFreesound(api_key="YOUR_FREESOUND_API_KEY"))

# Search across all registered providers
tracks = service.search(query="ambient", genre="electronic", limit_per_provider=5)

for track in tracks:
    print(f"[{track.provider}] {track.artist} - {track.title} ({track.license})")
    print(f"Format: {track.audio_file_format} | Stream: {track.stream_url}")
```
