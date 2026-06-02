[中文](./manifesto.md)

# Why VibeSkills Exists

I did not start this project because I thought the world needed a bigger manifesto.

If anything, it was the opposite.
I kept seeing too many genuinely good things already out there.

There are excellent skills, plugins, workflows, agent projects, and working methods. Each of them solves part of the problem. But once you try to use them in real work, the same friction appears again and again: they are scattered, they overlap, they conflict, and the burden falls back on the user.

You still end up asking:

- which thing should I use right now
- what should happen first
- which components are going to fight each other
- how do I stop the model from skipping the boring but necessary steps
- how do I verify the result
- how do I leave enough evidence so this does not become unreadable later

I did not want to solve that from scratch every time.

So the project slowly became an integration effort: collecting skills, projects, plugins, pitfalls, workflow norms, safety boundaries, verification habits, and maintenance lessons into one more coherent system.

It is not trying to prove some grand theory.
It is trying to make AI easier to use, steadier in practice, and less likely to drag people into a black box.

## What It Does Not Want To Become

`VibeSkills` does not want to become any of these things:

- a repository that keeps piling on features without improving usability
- a system that uses terminology and complexity to simulate depth
- a black-box agent demo that treats prompt tricks as reliability
- an ecosystem where the user still absorbs all the cost of choosing, validating, and recovering

If a system looks smart but has no boundaries, no verification, no evidence trail, and no rollback surface, I do not think it is trustworthy.

## What It Tries To Protect

### 1. People should not have to memorize a complicated skill ecosystem

Users should not have to remember which exact skill, project, or plugin should be activated in every situation.
A good system should absorb more of that choice cost.

### 2. AI should follow the right process, not just move fast

Many failures are not capability failures. They are workflow failures.
That is why I care more about “clarify first, execute second, verify third” than “start doing things immediately.”

### 3. Integration matters more than accumulation

The point of this project is not to keep collecting more things.
The point is to integrate the useful things so they can work together more naturally.

### 4. Traceability, boundaries, and rollback matter more than looking clever

I do not want AI work to end with one line that says “done.”
Requirements, plans, verification, and cleanup should leave a trail whenever possible, otherwise the system will not survive long-term maintenance.

### 5. Honesty matters more than pretending to be fully ready

If host plugins, MCP surfaces, secrets, or environment prerequisites are still missing, the system should say so plainly instead of pretending everything is already complete.

## Finally

`VibeSkills` is not an attempt to overstate itself.

It comes from a very practical desire: when I am surrounded by more and more strong but scattered AI capabilities, I want someone to do the hard integration work first so starting is easier, working is steadier, and the number of unnecessary mistakes goes down.

If this project can do that, then it is already worth building.
