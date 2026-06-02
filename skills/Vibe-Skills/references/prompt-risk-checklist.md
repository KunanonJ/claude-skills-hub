# Prompt Risk Checklist

Use this risk checklist when a prompt candidate is going to be suggested, injected, or reused inside VCO.

## Injection and Instruction Collision

1. Check for upstream prompt injection markers.
2. Check for hidden “ignore previous instructions” phrasing.
3. Check for role override attempts.
4. Check for policy override attempts.
5. Check for nested assistant/user simulation that changes authority.
6. Check for conflicting instruction priorities.
7. Check for ambiguous “do whatever is best” language.
8. Check for unverifiable implicit assumptions.

## Data Leakage and Privacy

9. Check for secret disclosure requests.
10. Check for token/API key placeholders leaking into examples.
11. Check for copying raw confidential text into prompt templates.
12. Check for unnecessary personal data retention.
13. Check for prompt candidates that memorize sensitive context.
14. Check for raw prompt excerpts in telemetry.
15. Check for accidental persistence of security-sensitive data.
16. Check for open-ended logging instructions.

## Tool Safety

17. Check whether tools are clearly bounded.
18. Check whether tool stop conditions are explicit.
19. Check whether tool side effects are described.
20. Check whether unsafe tool escalation is possible.
21. Check whether the prompt asks to bypass confirmation.
22. Check whether destructive actions are framed as defaults.
23. Check whether tool outputs are trusted without validation.
24. Check whether retries could loop indefinitely.

## Output Reliability

25. Check whether output schema is explicit.
26. Check whether evaluation criteria are explicit.
27. Check whether evidence is required where needed.
28. Check whether confidence / uncertainty is represented.
29. Check whether the prompt overpromises certainty.
30. Check whether the prompt suppresses necessary caveats.
31. Check whether the prompt encourages filler over evidence.
32. Check whether the prompt rewards verbosity without validation.

## Context Pressure

33. Check whether examples are bloating the context window.
34. Check whether repeated constraints can be compressed.
35. Check whether chain-of-thought exposure is unnecessary.
36. Check whether prompt assets duplicate existing assets.
37. Check whether multiple overlays are colliding.
38. Check whether prompt refinement changed the original user goal.
39. Check whether ambiguity should be escalated to confirmation.
40. Check whether the prompt candidate should remain advice-only.
41. Check whether rollback guidance is explicit whenever prompt output could trigger side effects.
