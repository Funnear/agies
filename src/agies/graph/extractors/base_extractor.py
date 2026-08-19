"""Abstract Base Extractor for Music Industry Knowledge Graph."""

from abc import ABC, abstractmethod
from typing import Tuple, List
from agies.graph.schema import BaseEntity, RelationshipEdge


class BaseGraphExtractor(ABC):
    """Abstract interface for extracting music industry entities and relationships."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def extract(
        self, query: str = "", limit: int = 50
    ) -> Tuple[List[BaseEntity], List[RelationshipEdge]]:
        """Extract a set of entities and their connecting relationship edges.

        Returns:
            Tuple of (entities_list, relationship_edges_list)
        """
        pass
