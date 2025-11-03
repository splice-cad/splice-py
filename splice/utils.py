"""
Utility functions for harness operations.
"""

from typing import Set, Optional
from .types import ComponentType, get_designator_prefix


class DesignatorGenerator:
    """
    Generates unique designators for components based on their type and category.

    Maintains counters for each designator prefix to ensure uniqueness.
    """

    def __init__(self) -> None:
        self._counters: dict[str, int] = {}
        self._used_designators: Set[str] = set()

    def generate(
        self, kind: ComponentType, category: Optional[str] = None, custom: Optional[str] = None
    ) -> str:
        """
        Generate a unique designator for a component.

        Args:
            kind: The component type
            category: Optional category for specialized components
            custom: Optional custom designator to use instead of auto-generation

        Returns:
            A unique designator string (e.g., "X1", "W2", "F1")

        Raises:
            ValueError: If the custom designator is already in use
        """
        # If custom designator provided, validate and use it
        if custom:
            if custom in self._used_designators:
                raise ValueError(f"Designator '{custom}' is already in use")
            self._used_designators.add(custom)
            return custom

        # Get prefix based on kind and category
        prefix = get_designator_prefix(kind, category)

        # Get next number for this prefix
        if prefix not in self._counters:
            self._counters[prefix] = 0

        # Find next available number
        while True:
            self._counters[prefix] += 1
            designator = f"{prefix}{self._counters[prefix]}"
            if designator not in self._used_designators:
                self._used_designators.add(designator)
                return designator

    def register(self, designator: str) -> None:
        """
        Register a designator as used without generating it.

        Useful for importing existing harnesses.

        Args:
            designator: The designator to register

        Raises:
            ValueError: If the designator is already registered
        """
        if designator in self._used_designators:
            raise ValueError(f"Designator '{designator}' is already registered")
        self._used_designators.add(designator)

    def is_used(self, designator: str) -> bool:
        """Check if a designator is already in use."""
        return designator in self._used_designators

    def reset(self) -> None:
        """Reset all counters and used designators."""
        self._counters.clear()
        self._used_designators.clear()
