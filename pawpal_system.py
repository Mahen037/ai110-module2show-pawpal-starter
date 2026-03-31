from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timedelta, date


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    is_required: bool
    frequency_per_day: int = 1
    is_completed: bool = False
    time: str = "00:00"  # HH:MM
    recurrence: str = "none"  # "none", "daily", "weekly"
    due_date: str = ""  # YYYY-MM-DD format, empty = today

    def update_task(
        self,
        title: str,
        duration_minutes: int,
        priority: int,
        is_required: bool,
        frequency_per_day: int | None = None,
        is_completed: bool | None = None,
        time: str | None = None,
        recurrence: str | None = None,
        due_date: str | None = None,
    ) -> None:
        if not title.strip():
            raise ValueError("title cannot be empty")
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be > 0")
        if priority < 0:
            raise ValueError("priority must be >= 0")
        if frequency_per_day is not None and frequency_per_day <= 0:
            raise ValueError("frequency_per_day must be > 0")
        if time is not None:
            self._validate_time(time)
        if recurrence is not None:
            self._validate_recurrence(recurrence)
        if due_date is not None and due_date:
            self._validate_date(due_date)

        self.title = title.strip()
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.is_required = is_required

        if frequency_per_day is not None:
            self.frequency_per_day = frequency_per_day
        if is_completed is not None:
            self.is_completed = is_completed
        if time is not None:
            self.time = time
        if recurrence is not None:
            self.recurrence = recurrence
        if due_date is not None:
            self.due_date = due_date

    @staticmethod
    def _validate_time(time: str) -> None:
        parts = time.split(":")
        if len(parts) != 2:
            raise ValueError("time must be in HH:MM format")
        if not (parts[0].isdigit() and parts[1].isdigit()):
            raise ValueError("time must be in HH:MM format")

        hour = int(parts[0])
        minute = int(parts[1])
        if hour < 0 or hour > 24 or minute < 0 or minute > 59 or (hour > 23 and minute != 0):
            raise ValueError("time must be in HH:MM format")

    @staticmethod
    def _validate_recurrence(recurrence: str) -> None:
        if recurrence not in {"none", "daily", "weekly"}:
            raise ValueError("recurrence must be 'none', 'daily', or 'weekly'")

    @staticmethod
    def _validate_date(date: str) -> None:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("due_date must be in YYYY-MM-DD format")
    

    def due_date_as_date(self) -> date:
        """Return due_date as date; empty due_date is treated as today."""
        if self.due_date:
            return datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return date.today()

    def is_due_on(self, on_date: date) -> bool:
        return self.due_date_as_date() == on_date
    

    def _mark_completed(self) -> Task | None:
        """Mark task as completed and return a new recurring task if applicable."""
        self.is_completed = True

        if self.recurrence == "none":
            return None

        next_due_date = self._calculate_next_due_date()
        new_task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            is_required=self.is_required,
            frequency_per_day=self.frequency_per_day,
            is_completed=False,
            time=self.time,
            recurrence=self.recurrence,
            due_date=next_due_date,
        )
        return new_task

    def _calculate_next_due_date(self) -> str:
        """Calculate next due date based on recurrence pattern."""
        current_date = datetime.strptime(self.due_date, "%Y-%m-%d") if self.due_date else datetime.now()

        if self.recurrence == "daily":
            next_date = current_date + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_date = current_date + timedelta(weeks=1)
        else:
            next_date = current_date

        return next_date.strftime("%Y-%m-%d")

    def mark_incomplete(self) -> None:
        self.is_completed = False

    def get_end_time(self) -> str:
        """Calculate end time based on start time and duration."""
        hours, minutes = map(int, self.time.split(":"))
        total_minutes = hours * 60 + minutes + self.duration_minutes
        end_hour = (total_minutes // 60) % 24
        end_minute = total_minutes % 60
        return f"{end_hour:02d}:{end_minute:02d}"

    def time_to_minutes(self) -> int:
        """Convert HH:MM to total minutes since midnight."""
        hours, minutes = map(int, self.time.split(":"))
        return hours * 60 + minutes


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

    def complete_task(self, title: str) -> bool:
        """Mark a task complete and auto-add next occurrence if recurring."""
        for i, task in enumerate(self.tasks):
            if task.title == title:
                next_task = task._mark_completed()
                if next_task:
                    self.tasks.append(next_task)
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
    strategy: str = "priority_first"  # or shortest_first


    def _pending_tasks_for_day(self, owner: Owner, on_date: date | None = None) -> list[Task]:
        target = on_date or date.today()
        return [
            t for t in owner.get_all_tasks()
            if (not t.is_completed) and t.is_due_on(target)
        ]

    def generate_plan(self, owner: Owner, on_date: date | None = None) -> list[Task]:
        available = owner.daily_time_available
        if available < 0:
            raise ValueError("owner.daily_time_available must be >= 0")

        tasks = self._pending_tasks_for_day(owner, on_date)
        expanded_tasks: list[Task] = []
        for task in tasks:
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

        return sorted(
            tasks,
            key=lambda t: (
                0 if t.is_required else 1,
                -t.priority,
                t.duration_minutes,
                t.title.lower(),
            ),
        )

    def sort_by_time(self, tasks: list[Task], order: str = "asc") -> list[Task]:
        """Sort tasks by Task.time in HH:MM format."""
        if order not in {"asc", "desc"}:
            raise ValueError("order must be 'asc' or 'desc'")

        for task in tasks:
            Task._validate_time(task.time)

        return sorted(
            tasks,
            key=lambda t: (t.time_to_minutes(), t.duration_minutes),
            reverse=(order == "desc"),
        )

    def filter_tasks(
        self,
        owner: Owner,
        is_completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter tasks by completion status and/or pet name."""
        results: list[Task] = []
        pet_name_normalized = pet_name.strip().lower() if pet_name is not None else None

        for pet in owner.pets:
            if pet_name_normalized is not None and pet.name.lower() != pet_name_normalized:
                continue

            for task in pet.tasks:
                if is_completed is not None and task.is_completed != is_completed:
                    continue
                results.append(task)

        return results

    def detect_conflicts(self, owner: Owner, on_date: date | None = None) -> list[str]:
        warnings: list[str] = []
        pending_tasks = self._pending_tasks_for_day(owner, on_date)

        for i in range(len(pending_tasks)):
            for j in range(i + 1, len(pending_tasks)):
                task1 = pending_tasks[i]
                task2 = pending_tasks[j]
                if self._tasks_overlap(task1, task2):
                    warnings.append(
                        f"⚠️  CONFLICT: '{task1.title}' ({task1.time}-{task1.get_end_time()}) "
                        f"overlaps with '{task2.title}' ({task2.time}-{task2.get_end_time()})"
                    )
        return warnings

    def _tasks_overlap(self, task1: Task, task2: Task) -> bool:
        """Check if two tasks have overlapping time slots."""
        task1_start = task1.time_to_minutes()
        task1_end = task1_start + task1.duration_minutes

        task2_start = task2.time_to_minutes()
        task2_end = task2_start + task2.duration_minutes

        # Overlap occurs if one task starts before the other ends
        return not (task1_end <= task2_start or task2_end <= task1_start)

    def schedule_by_start_time(self, owner: Owner, on_date: date | None = None) -> list[tuple[str, Task]]:
        target = on_date or date.today()
        scheduled: list[tuple[str, Task]] = []

        for pet in owner.pets:
            for task in pet.tasks:
                if (not task.is_completed) and task.is_due_on(target):
                    scheduled.append((pet.name, task))

        scheduled.sort(key=lambda x: x[1].time_to_minutes())
        return scheduled

    def explain_selection(self, task: Task) -> str:
        status = "required" if task.is_required else "optional"
        completion = "completed" if task.is_completed else "pending"
        recurrence_str = f", recurrence={task.recurrence}" if task.recurrence != "none" else ""
        return (
            f"Task '{task.title}' is {status}, priority={task.priority}, "
            f"duration={task.duration_minutes}m, frequency={task.frequency_per_day}/day, "
            f"status={completion}{recurrence_str}."
        )