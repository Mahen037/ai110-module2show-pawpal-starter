from pawpal_system import Pet, Task


def test_task_completion_changes_status() -> None:
    task = Task(title="Feed Buddy", duration_minutes=10, priority=5, is_required=True)
    assert task.is_completed is False

    task.mark_completed()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Buddy", species="Dog", age=3)
    initial_count = len(pet.tasks)

    pet.add_task(Task(title="Morning Walk", duration_minutes=30, priority=3, is_required=True))

    assert len(pet.tasks) == initial_count + 1