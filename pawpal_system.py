from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    is_required: bool
    frequency_per_day: int = 1
    is_completed: bool = False

    def update_task(
        self,
        title: str,
        duration_minutes: int,
        priority: int,
        is_required: bool,
        frequency_per_day: int | None = None,
        is_completed: bool | None = None,
    ) -> None:
        """_summary_

        Args:
            title (str): _description_
            duration_minutes (int): _description_
            priority (int): _description_
            is_required (bool): _description_
            frequency_per_day (int | None, optional): _description_. Defaults to None.
            is_completed (bool | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        if not title.strip():
            raise ValueError("title cannot be empty")
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be > 0")
        if priority < 0:
            raise ValueError("priority must be >= 0")
        if frequency_per_day is not None and frequency_per_day <= 0:
            raise ValueError("frequency_per_day must be > 0")

        self.title = title.strip()
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.is_required = is_required

        if frequency_per_day is not None:
            self.frequency_per_day = frequency_per_day
        if is_completed is not None:
            self.is_completed = is_completed

    def mark_completed(self) -> None:
        self.is_completed = True

    def mark_incomplete(self) -> None:
        self.is_completed = False


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def update_details(self, name: str, species: str, age: int, tasks: list[Task]) -> None:
        if not name.strip():
            raise ValueError("name cannot be empty")
        if not species.strip():
            raise ValueError("species cannot be empty")
        if age < 0:
            raise ValueError("age must be >= 0")

        self.name = name.strip()
        self.species = species.strip()
        self.age = age
        self.tasks = list(tasks)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, title: str) -> bool:
        for i, task in enumerate(self.tasks):
            if task.title == title:
                self.tasks.pop(i)
                return True
        return False


@dataclass
class Owner:
    name: str
    daily_time_available: int
    pets: list[Pet] = field(default_factory=list)

    def update_profile(self, name: str, daily_time_available: int, preferences: dict[str, Any]) -> None:
        if not name.strip():
            raise ValueError("name cannot be empty")
        if daily_time_available < 0:
            raise ValueError("daily_time_available must be >= 0")

        self.name = name.strip()
        self.daily_time_available = daily_time_available

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        for i, pet in enumerate(self.pets):
            if pet.name == pet_name:
                self.pets.pop(i)
                return True
        return False

    def get_all_tasks(self) -> list[Task]:
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Scheduler:
    strategy: str = "priority_first" # or shortest_first

    def generate_plan(self, owner: Owner) -> list[Task]:
        """_summary_

        Args:
            owner (Owner): _description_

        Raises:
            ValueError: _description_

        Returns:
            list[Task]: _description_
        """
        available = owner.daily_time_available
        if available < 0:
            raise ValueError("owner.daily_time_available must be >= 0")

    

        tasks = owner.get_all_tasks()
        # Expand by frequency: a task with frequency_per_day=3 appears 3 times.
        expanded_tasks: list[Task] = []
        for task in tasks:
            if task.is_completed:
                continue
            expanded_tasks.extend([task] * task.frequency_per_day)


        ranked = self.rank_tasks(expanded_tasks)

        plan: list[Task] = []
        used_minutes = 0

        for task in ranked:
            if used_minutes + task.duration_minutes <= available:
                plan.append(task)
                used_minutes += task.duration_minutes

        return plan

    def rank_tasks(self, tasks: list[Task]) -> list[Task]:
        """_summary_

        Args:
            tasks (list[Task]): _description_

        Returns:
            list[Task]: _description_
        """
        if self.strategy == "shortest_first":
            return sorted(
                tasks,
                key=lambda t: (
                    0 if t.is_required else 1,
                    t.duration_minutes,
                    -t.priority,
                    t.title.lower(),
                ),
            )

        # default: priority_first
        return sorted(
            tasks,
            key=lambda t: (
                0 if t.is_required else 1,
                -t.priority,
                t.duration_minutes,
                t.title.lower(),
            ),
        )

    def explain_selection(self, task: Task) -> str:
        """_summary_

        Args:
            task (Task): _description_

        Returns:
            str: _description_
        """
        status = "required" if task.is_required else "optional"
        completion = "completed" if task.is_completed else "pending"
        return (
            f"Task '{task.title}' is {status}, priority={task.priority}, "
            f"duration={task.duration_minutes}m, frequency={task.frequency_per_day}/day, status={completion}."
        )