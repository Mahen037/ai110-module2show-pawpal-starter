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
    
    My initial UML design used four main classes: **Owner**, **Pet**, **CareTask**, and **Scheduler**.

- What classes did you include, and what responsibilities did you assign to each?
    - **Owner**: stores owner details, available daily time, and preferences.
    - **Pet**: stores pet profile information and care needs.
    - **CareTask**: represents one care task with duration, priority, and required/optional status.
    - **Scheduler**: takes tasks and constraints, ranks tasks, and generates a daily plan.

    I modeled relationships as:
    - Owner has one or more pets.
    - Pet has zero or more care tasks.
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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
