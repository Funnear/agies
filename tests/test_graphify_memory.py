"""Unit tests for Graphify Memory & Associative Recall Engine."""

from pathlib import Path
import tempfile

from agies.memory.graphify import GraphifyMemory


def test_graphify_text_and_concept_extraction():
    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "test_memory.json"
        memory = GraphifyMemory(memory_file_path=mem_file)

        text = "David Bowie and Brian Eno recorded the iconic Berlin Trilogy at Hansa Studios experimenting with electronic synthesizer textures and ambient soundscapes."
        res = memory.graphify_text(text, session_id="session_berlin_1")

        assert res["created_nodes_count"] >= 3
        assert (
            "David Bowie" in res["extracted_concepts"]
            or "Hansa" in res["extracted_concepts"]
        )
        assert res["total_memory_nodes"] >= 4
        assert res["total_memory_edges"] >= 3

        # Test Associative Recall
        recall_res = memory.recall("Where did Bowie record in Berlin?", hops=2)
        assert recall_res["recalled_nodes_count"] >= 1
        labels = [n["label"] for n in recall_res["recalled_nodes"]]
        assert any(
            "Bowie" in lbl or "Hansa" in lbl or "Berlin" in lbl for lbl in labels
        )


def test_graphify_audio_event():
    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "test_memory.json"
        memory = GraphifyMemory(memory_file_path=mem_file)

        event = memory.graphify_audio_event(
            track_title="Autobahn Synth Track",
            artist_name="Kraftwerk",
            predicted_genre="techno",
            confidence=0.98,
            detected_bpm=132.0,
            provider="archive_org",
        )

        assert "event_id" in event
        assert "artist_id" in event

        # Recall audio event
        recall = memory.recall("Kraftwerk techno track", hops=2)
        assert recall["recalled_nodes_count"] >= 2
        labels = [n["label"] for n in recall["recalled_nodes"]]
        assert "Kraftwerk" in labels or "Techno" in labels


def test_graphify_memory_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "persistent_memory.json"

        # Create first memory instance
        mem1 = GraphifyMemory(memory_file_path=mem_file)
        mem1.graphify_text(
            "Nils Frahm records at Funkhaus Berlin using acoustic upright pianos.",
            session_id="session_1",
        )

        summary1 = mem1.get_summary()
        assert summary1["total_nodes"] >= 2
        assert mem_file.exists()

        # Reload in second memory instance
        mem2 = GraphifyMemory(memory_file_path=mem_file)
        summary2 = mem2.get_summary()
        assert summary2["total_nodes"] == summary1["total_nodes"]
        assert summary2["total_edges"] == summary1["total_edges"]

        recall_res = mem2.recall("Funkhaus", hops=1)
        assert recall_res["recalled_nodes_count"] >= 1
