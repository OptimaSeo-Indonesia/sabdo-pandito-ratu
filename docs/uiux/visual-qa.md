# Visual QA Checklist

Before committing any UI change, answer **YES** to all questions.

If any answer is NO → redesign before merging.

## Identity Checks

- [ ] Does this page still look like the approved reference?
- [ ] Is the AI Council still the main focus?
- [ ] Does it **NOT** resemble a chatbot? (If YES → redesign)
- [ ] Does it **NOT** resemble a generic SaaS? (If YES → redesign)
- [ ] Does it feel like an AI Operating System?

## Visual Consistency

- [ ] Is the Gunungan subtle enough? (2–5% opacity, blurred)
- [ ] Is spacing consistent with `spacing-sizing.md`?
- [ ] Are glass effects identical to `glassmorphism.md`?
- [ ] Are shadows identical to the reference?
- [ ] Are colors from the approved palette (`colors.md`)?
- [ ] Is typography from `typography.md`?
- [ ] Are all animations from `motion.md`?

## Component Checks

- [ ] Are all components from `components.md`?
- [ ] Are there any loading spinners? (Should use deliberation timeline)
- [ ] Is the Background component present? (6 layers)
- [ ] Does the Council animate correctly? (idle pulse, live connections)

## Mobile Checks

- [ ] Is the council still central on mobile?
- [ ] No horizontal overflow?
- [ ] Touch-friendly targets?

## Motion Checks

- [ ] Animations feel calm and intentional? (not flashy)
- [ ] Entry animations present? (fadeUp on load)
- [ ] Deliberation shows progress, not spinners?

## Final

- [ ] All checks passed → merge.
