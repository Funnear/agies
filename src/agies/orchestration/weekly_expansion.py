"""Backward compatibility wrapper for AutonomousKnowledgeGraphExpander."""

from agies.orchestration.autonomous_expansion import (
    AutonomousKnowledgeGraphExpander,
    WeeklyKnowledgeGraphExpander,
)

__all__ = ["AutonomousKnowledgeGraphExpander", "WeeklyKnowledgeGraphExpander"]
