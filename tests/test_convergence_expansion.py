"""Unit tests for Adaptive Convergence Expansion Loop."""

from agies.orchestration.convergence_expansion import AdaptiveConvergenceExpander


def test_convergence_expander(tmp_path):
    expander = AdaptiveConvergenceExpander(
        data_dir=tmp_path / "corpus",
        convergence_threshold=0.05,
        patience_epochs=1,
        max_epochs=3,
    )

    results = expander.run_until_flattened(
        initial_target_audio_per_genre=5,
        delay_between_epochs_sec=0.01,
    )

    assert results["total_epochs_executed"] >= 1
    assert results["final_total_nodes"] > 0
    assert results["final_total_edges"] > 0
    assert (tmp_path / "corpus" / "convergence_history.json").exists()
