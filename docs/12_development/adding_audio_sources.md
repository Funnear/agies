# Adding New Audio Data Sources (Developer Guide)

As a sole contributor, the **`AudioDataSource`** abstraction is designed for maximum developer ergonomics: zero-boilerplate, automatic local disk caching, rate-limit backoff, retries, and a pluggable `@register_source` decorator.

---

## 1. Minimal Example: Creating a New Source in 10 Lines

To add any new audio source (e.g. Bandcamp, SoundCloud, ccMixter, Musopen, Spotify previews, internal audio repository), simply inherit from `AudioDataSource` and implement `_fetch_tracks()`:

```python
from agies import AudioDataSource, register_source, AudioFilter, AudioTrack, LicenseInfo

@register_source("my_sound_source", aliases=["mysound"])
class MySoundDataSource(AudioDataSource):
    source_name = "my_sound_source"
    BASE_URL = "https://api.example.com/v1"

    def _fetch_tracks(self, audio_filter: AudioFilter) -> list[AudioTrack]:
        # 1. Automatic caching, retry backoff, and rate-limiting are handled by _request_with_retry
        data = self._request_with_retry(
            method="GET",
            url=f"{self.BASE_URL}/search",
            params={"q": audio_filter.query, "limit": audio_filter.limit}
        )

        # 2. Map provider JSON to normalized AudioTrack
        tracks = []
        for item in data.get("items", []):
            tracks.append(AudioTrack(
                id=str(item["id"]),
                provider=self.source_name,
                title=item["title"],
                artist=item.get("artist", "Unknown"),
                duration_seconds=item.get("duration"),
                stream_url=item.get("preview_mp3_url"),
                download_url=item.get("download_url"),
                license=LicenseInfo(name="CC-BY 4.0", is_commercial_allowed=True),
            ))
        return tracks
```

---

## 2. Using Your New Source Instantly

Once decorated with `@register_source`, your provider is automatically available across the entire AGIES ecosystem:

```python
import agies

# Direct query via factory
source = agies.get_audio_source("my_sound_source")
tracks = source.search(query="ambient synth", limit=5)

# Download track with automatic filename sanitization & streaming chunks
downloaded_path = source.download_track(tracks[0], destination_dir="./my_audio")

# Or list all available sources
print(agies.AudioSourceRegistry.list_available_sources())
# ['archive_org', 'freesound', 'jamendo', 'my_sound_source']
```

---

## 3. Built-in Features for Sole Maintainers

| Feature | How It Works |
| :--- | :--- |
| **Auto-Caching** | Responses are cached locally to `~/.cache/agies/audio/<source>/` to avoid hitting API rate limits during rapid prototyping and test iterations. |
| **Exponential Backoff** | Handles temporary 429/500 network hiccups automatically. |
| **Safe Downloading** | Sanitizes track titles into valid filesystem filenames, streams in chunks to conserve memory, and avoids re-downloading existing files. |
| **Batch Downloads** | `source.download_batch(tracks, destination_dir="./downloads")`. |
