from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status() -> None:
    dog = Pet(name="Buddy", species="Dog", age=3)
    task = Task(title="Feed Buddy", duration_minutes=10, priority=5, is_required=True)
    dog.add_task(task)

    assert task.is_completed is False
    assert dog.complete_task("Feed Buddy") is True
    assert task.is_completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Buddy", species="Dog", age=3)
    initial_count = len(pet.tasks)

    pet.add_task(Task(title="Morning Walk", duration_minutes=30, priority=3, is_required=True))

    assert len(pet.tasks) == initial_count + 1


def test_sorting_correctness_chronological_order() -> None:
    scheduler = Scheduler()
    tasks = [
        Task(title="Lunch", duration_minutes=20, priority=1, is_required=False, time="12:30"),
        Task(title="Morning Walk", duration_minutes=30, priority=3, is_required=True, time="08:00"),
        Task(title="Evening Meds", duration_minutes=10, priority=5, is_required=True, time="19:15"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks, order="asc")

    assert [t.title for t in sorted_tasks] == ["Morning Walk", "Lunch", "Evening Meds"]


def test_recurrence_daily_completion_creates_next_day_task() -> None:
    today = date.today()
    tomorrow = today + timedelta(days=1)

    dog = Pet(name="Buddy", species="Dog", age=3)
    daily_task = Task(
        title="Daily Feeding",
        duration_minutes=15,
        priority=5,
        is_required=True,
        recurrence="daily",
        due_date=today.strftime("%Y-%m-%d"),
    )
    dog.add_task(daily_task)

    assert dog.complete_task("Daily Feeding") is True

    assert daily_task.is_completed is True
    assert len(dog.tasks) == 2

    new_task = dog.tasks[1]
    assert new_task.title == "Daily Feeding"
    assert new_task.is_completed is False
    assert new_task.due_date == tomorrow.strftime("%Y-%m-%d")


def test_conflict_detection_flags_duplicate_times() -> None:
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(title="Task A", duration_minutes=30, priority=2, is_required=True, time="09:00"))
    pet.add_task(Task(title="Task B", duration_minutes=30, priority=1, is_required=False, time="09:00"))

    owner = Owner(name="Sam", daily_time_available=120, pets=[pet])
    scheduler = Scheduler()

    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) >= 1
    assert "CONFLICT" in warnings[0]


def test_pet_with_no_tasks_returns_empty_schedule() -> None:
    owner = Owner(name="Sam", daily_time_available=60, pets=[Pet(name="Buddy", species="Dog", age=3)])
    scheduler = Scheduler()

    assert scheduler.schedule_by_start_time(owner) == []