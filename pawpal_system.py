from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Owner:
    name: str
    daily_time_available: int
    preferences: dict[str, Any] = field(default_factory=dict)

    def update_profile(
        self,
        name: str,
        daily_time_available: int,
        preferences: dict[str, Any],
    ) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    needs: list[str] = field(default_factory=list)

    def update_details(
        self,
        name: str,
        species: str,
        age: int,
        needs: list[str],
    ) -> None:
        pass


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: int
    is_required: bool

    def update_task(
        self,
        title: str,
        duration_minutes: int,
        priority: int,
        is_required: bool,
    ) -> None:
        pass


@dataclass
class Scheduler:
    strategy: str

    def generate_plan(
        self,
        tasks: list[CareTask],
        available_minutes: int,
        preferences: dict[str, Any],
    ) -> list[CareTask]:
        pass

    def rank_tasks(self, tasks: list[CareTask]) -> list[CareTask]:
        pass

    def explain_selection(self, task: CareTask) -> str:
        pass