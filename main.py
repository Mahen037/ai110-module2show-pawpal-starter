from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime


def main() -> None:
    # Create owner
    owner = Owner(name="Mahendra", daily_time_available=90)

    # Create pets
    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Luna", species="Cat", age=2)

    # Add tasks intentionally out of chronological order
    dog.add_task(Task(title="Morning Walk", duration_minutes=35, priority=3, is_required=True, time="07:30"))
    dog.add_task(Task(title="Feed Buddy", duration_minutes=10, priority=5, is_required=True, time="06:45"))
    dog.add_task(Task(title="Bath Buddy", duration_minutes=10, priority=5, is_required=True, time="19:00"))

    cat.add_task(Task(title="Play Time", duration_minutes=20, priority=2, is_required=False, time="08:15", recurrence="daily"))
    cat.add_task(Task(title="Clean Litter Box", duration_minutes=15, priority=4, is_required=True, time="06:30"))
    cat.add_task(Task(title="Feed Luna", duration_minutes=5, priority=4, is_required=True, time="06:40"))

    # Add conflicting tasks (same start time for Buddy and Luna)
    dog.add_task(Task(title="Grooming", duration_minutes=25, priority=2, is_required=False, time="08:15"))

    # Mark one task complete to test filtering
    cat.complete_task("Play Time")  # instead of cat.tasks[0]._mark_completed()

    # Attach pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(strategy="priority_first")

    # 1) Sorted by time
    print("All Tasks (Sorted by Time)")
    print("-" * 50)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks(), order="asc")
    for i, task in enumerate(sorted_tasks, start=1):
        status_icon = "✓" if task.is_completed else "○"
        print(
            f"{i}. {status_icon} {task.time}-{task.get_end_time()} | {task.title} "
            f"({task.duration_minutes} min, priority={task.priority})"
        )

    # 2) Schedule by start time (chronological order)
    print("\n\nSchedule by Start Time")
    print("-" * 50)
    scheduled = scheduler.schedule_by_start_time(owner)
    for i, (pet_name, task) in enumerate(scheduled, start=1):
        print(
            f"{i}. {task.time}-{task.get_end_time()} | {pet_name.upper()}: {task.title} "
            f"({task.duration_minutes} min)"
        )

    # 3) Detect conflicts
    print("\n\nConflict Detection")
    print("-" * 50)
    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("✅ No scheduling conflicts detected!")

    # 4) Filter by completion status
    print("\n\nPending Tasks Only")
    print("-" * 50)
    pending_tasks = scheduler.filter_tasks(owner, is_completed=False)
    for i, task in enumerate(scheduler.sort_by_time(pending_tasks), start=1):
        print(f"{i}. {task.time} - {task.title}")

    # 5) Filter by pet name
    print("\n\nBuddy's Tasks")
    print("-" * 50)
    buddy_tasks = scheduler.filter_tasks(owner, pet_name="Buddy")
    for i, task in enumerate(scheduler.sort_by_time(buddy_tasks), start=1):
        status = "✓" if task.is_completed else "○"
        print(f"{i}. {status} {task.time}-{task.get_end_time()} | {task.title}")

    # 6) Generate plan
    plan = scheduler.generate_plan(owner)
    print("\n\nToday's Schedule (Generated Plan)")
    print("-" * 50)
    total = 0
    for i, task in enumerate(plan, start=1):
        print(
            f"{i}. {task.title} "
            f"({task.duration_minutes} min, priority={task.priority}, "
            f"{'required' if task.is_required else 'optional'})"
        )
        total += task.duration_minutes

    print("-" * 50)
    print(f"Total planned time: {total} min")
    print(f"Time available: {owner.daily_time_available} min")


if __name__ == "__main__":
    main()