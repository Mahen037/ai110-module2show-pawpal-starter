import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", daily_time_available=90)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(strategy="priority_first")

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

st.markdown("## 1) Owner Profile")
with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)
    owner_time = st.number_input(
        "Daily time available (minutes)",
        min_value=0,
        max_value=24 * 60,
        value=owner.daily_time_available,
    )
    save_owner = st.form_submit_button("Save owner profile")

if save_owner:
    # Call method from pawpal_system.py
    owner.update_profile(owner_name, int(owner_time), preferences={})
    st.success("Owner profile updated.")

st.divider()

st.markdown("## 2) Add a Pet")
with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=1)
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    if not pet_name.strip():
        st.error("Pet name is required.")
    else:
        new_pet = Pet(name=pet_name.strip(), species=species, age=int(age))
        # Call method from pawpal_system.py
        owner.add_pet(new_pet)
        st.success(f"Added pet: {new_pet.name}")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("## 3) Add Tasks to a Pet")
if not owner.pets:
    st.info("Add at least one pet first.")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Choose pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    with st.form("task_form", clear_on_submit=True):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        is_required = st.checkbox("Required", value=True)
        frequency = st.number_input("Frequency per day", min_value=1, max_value=10, value=1)
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        if not task_title.strip():
            st.error("Task title is required.")
        else:
            priority_map = {"low": 1, "medium": 3, "high": 5}
            task = Task(
                title=task_title.strip(),
                duration_minutes=int(duration),
                priority=priority_map[priority_label],
                is_required=is_required,
                frequency_per_day=int(frequency),
            )
            # Call method from pawpal_system.py
            selected_pet.add_task(task)
            st.success(f"Added task to {selected_pet.name}: {task.title}")

    if selected_pet.tasks:
        st.write(f"Tasks for {selected_pet.name}:")
        st.table(
            [
                {
                    "title": t.title,
                    "duration_minutes": t.duration_minutes,
                    "priority": t.priority,
                    "required": t.is_required,
                    "frequency_per_day": t.frequency_per_day,
                    "completed": t.is_completed,
                }
                for t in selected_pet.tasks
            ]
        )
    else:
        st.info(f"No tasks for {selected_pet.name} yet.")

st.divider()

st.markdown("## 4) Generate Today's Schedule")
strategy = st.selectbox("Scheduling strategy", ["priority_first", "shortest_first"])
scheduler.strategy = strategy

if st.button("Generate schedule"):
    # Call method from pawpal_system.py
    plan = scheduler.generate_plan(owner)

    if not plan:
        st.warning("No tasks selected.")
    else:
        st.subheader("Today's Schedule")
        total = 0
        for i, task in enumerate(plan, start=1):
            st.write(
                f"{i}. {task.title} "
                f"({task.duration_minutes} min, priority={task.priority}, "
                f"{'required' if task.is_required else 'optional'})"
            )
            # Call method from pawpal_system.py
            st.caption(scheduler.explain_selection(task))
            total += task.duration_minutes

        st.success(f"Total planned time: {total} / {owner.daily_time_available} minutes")
