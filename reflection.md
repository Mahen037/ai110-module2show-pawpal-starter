# PawPal+ Project Reflection

## 1. System Design
Three core user actions for PawPal+:
1. Manage pet profile - 
Add/edit pet details (name, age, species, needs, owner preferences).
2. Create and manage care tasks -
Add/edit/delete tasks like feeding, walks, meds, grooming, with duration and priority.
3. Generate and view today’s plan -
Build a daily schedule based on available time and constraints, then view the ordered task list with brief reasoning.

**a. Initial design**

- Briefly describe your initial UML design.
    
    My initial UML design used four main classes: **Owner**, **Pet**, **Task**, and **Scheduler**.

- What classes did you include, and what responsibilities did you assign to each?
    - **Owner**: stores owner details, available daily time, and preferences.
    - **Pet**: stores pet profile information and care needs.
    - **Task**: represents one care task with duration, priority, and required/optional status.
    - **Scheduler**: takes tasks and constraints, ranks tasks, and generates a daily plan.

    I modeled relationships as:
    - Owner has one or more pets.
    - Pet has zero or more tasks.
    - Scheduler depends on Owner preferences and CareTask data.


**b. Design changes**

- Did your design change during implementation?

Yes, the design changed during implementation.  

- If yes, describe at least one change and why you made it.

I simplified it by removing lower-priority complexity (for example strict time windows) and focused on required features: duration, priority, and available time. This made the scheduler easier to test and made behavior more predictable for the Streamlit UI.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers these constraints:

Available daily time (minutes): hard limit; total scheduled task duration cannot exceed this.
Task priority: higher-priority tasks are scheduled first.
Required vs optional tasks: required tasks are favored over optional tasks.
Owner preferences: used as secondary ordering (for example, preferred task types or timing).


- How did you decide which constraints mattered most?

I treated time and required tasks as the highest priority because they determine feasibility and minimum care needs. Priority and preferences are then used to improve plan quality once core constraints are satisfied.



**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One tradeoff is that the scheduler may leave out lower-priority or optional tasks when time is limited.

- Why is that tradeoff reasonable for this scenario?
This is reasonable for this scenario because a realistic, executable plan is more useful than an overloaded plan that cannot be completed.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
Design brainstorming (classes, method responsibilities, tradeoffs).
Debugging (time parsing bugs, missing validations, edge-case handling).
Refactoring (cleaning scheduler methods and reducing repeated logic).
Feature extension (sorting by time, filtering, recurring tasks, conflict detection).

- What kinds of prompts or questions were most helpful?
Most helpful prompts were specific and constraint-based, for example:
“Implement sort_by_time() using HH:MM and lambda key.”
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
The suggestion initially marked tasks complete but did not fully align with how main.py was calling completion. I adjusted it so completion flows through Pet.complete_task() and verified behavior end-to-end.
- How did you evaluate or verify what the AI suggested?
Running python3 main.py after each change. Creating same-time tasks to confirm conflict warnings appear.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Sorting tasks by start time (HH:MM).
Filtering by is_completed and by pet name.
Schedule ordering by start time.
Conflict detection for overlapping tasks.
- Why were these tests important?
These tests were important because they validate core scheduling correctness and user trust: correct order, realistic warnings, and predictable behavior.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am fairly confident the scheduler works for normal use cases and the implemented constraints.
- What edge cases would you test next if you had more time?
Duplicate task names within one pet.
Recurrence + conflict interactions across multiple days.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The strongest part was building a scheduler that is both practical and readable.
I am most satisfied with adding useful real-world behavior: chronological scheduling, conflict warnings, and recurring task rollover.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Add stronger unit test coverage.
Separate scheduling strategy logic into pluggable strategy classes.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
A key lesson was that AI speeds up implementation, but quality still depends on human validation. Precise prompts, incremental testing, and checking behavior in context are essential for reliable system design.


### AI Strategy (VS Code Copilot)

**Most effective Copilot features for building the scheduler**
- **Inline code suggestions** were most effective for fast method scaffolding (`sort_by_time`, `detect_conflicts`, recurrence helpers).
- **Copilot Chat with file context** helped refine logic against actual class signatures in pawpal_system.py.
- **Test generation support** was useful for quickly drafting happy-path and edge-case tests (empty tasks, duplicate times, recurrence rollover).
- **Iterative prompt + rerun loop** (ask → edit → run `pytest`) made debugging predictable.

**One AI suggestion I rejected/modified**
- I rejected a suggestion that put task-completion flow directly in scheduling logic.
- I modified it to keep completion in `Pet.complete_task()` and let `Task` handle recurrence date rollover.
- This preserved cleaner responsibilities: `Scheduler` plans, `Pet` manages task lifecycle, `Task` owns recurrence rules.

**How separate chat sessions helped**
- I used separate sessions by phase (design, implementation, testing, packaging/reflection).
- This prevented context mixing, kept prompts focused, and reduced accidental regressions.
- It also made it easier to track decisions (UML changes vs. algorithm changes vs. UI/documentation updates).

**What I learned about being the “lead architect” with AI**
- AI accelerates coding, but architecture quality still depends on human decisions.
- I had to define boundaries, reject overreach, and verify behavior with tests.
- The main lesson: treat AI as a strong implementation partner, not the source of final design authority.