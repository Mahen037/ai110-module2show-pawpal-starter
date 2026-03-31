from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # Create owner
    owner = Owner(name="Mahendra", daily_time_available=90)

    # Create pets
    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Luna", species="Cat", age=2)

    # Add tasks (different durations)
    dog.add_task(Task(title="Morning Walk", duration_minutes=35, priority=3, is_required=True))
    dog.add_task(Task(title="Feed Buddy", duration_minutes=10, priority=5, is_required=True))
    dog.add_task(Task(title="Bath Buddy", duration_minutes=10, priority=5, is_required=True))
    cat.add_task(Task(title="Play Time", duration_minutes=20, priority=2, is_required=False))
    cat.add_task(Task(title="Clean Litter Box", duration_minutes=15, priority=4, is_required=True))
    cat.add_task(Task(title="Feed Luna", duration_minutes=5, priority=4, is_required=True))

    # Attach pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Build schedule
    scheduler = Scheduler(strategy="priority_first")
    plan = scheduler.generate_plan(owner)

    # Print schedule
    print("Today's Schedule")
    print("-" * 20)

    total = 0
    for i, task in enumerate(plan, start=1):
        print(
            f"{i}. {task.title} "
            f"({task.duration_minutes} min, priority={task.priority}, "
            f"{'required' if task.is_required else 'optional'})"
        )
        total += task.duration_minutes

    print("-" * 20)
    print(f"Total planned time: {total} min")
    print(f"Time available: {owner.daily_time_available} min")


if __name__ == "__main__":
    main()