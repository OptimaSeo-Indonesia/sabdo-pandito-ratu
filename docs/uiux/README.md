# Sabdo Pandito Ratu UI/UX Design System

This directory contains the complete visual identity of Sabdo Pandito Ratu.

Every UI task **MUST** start by reading this directory.

---

## Reference Files (Override Everything)

These files describe the **target** based on the approved reference image.
They **override** any existing implementation or personal design decisions.

1. `reference-ui-spec.md` — Layout & geometry
2. `reference-spacing.md` — Spacing & sizing
3. `reference-colors.md` — Color palette
4. `reference-glass.md` — Glassmorphism rules
5. `reference-motion.md` — Animation timing
6. `reference-components.md` — Every component
7. `reference-background.md` — Aurora, Gunungan, particles
8. `reference-layout-grid.md` — Grid desktop/tablet/mobile

## Implementation Files (Current State)

These files describe the **current implementation**.
Update them after implementing reference specs.

1. `philosophy.md` — Core identity and metaphor
2. `visual-language.md` — Design principles and visual direction
3. `layout-spec.md` — Grid, page structure, council positioning
4. `spacing-sizing.md` — Margins, padding, component sizes
5. `typography.md` — Font stack, sizes, weights, hierarchy
6. `colors.md` — Full color system (dark + light, advisor, connection)
7. `glassmorphism.md` — Glass effect specifications
8. `background.md` — Aurora, Gunungan, particles, neural grid
9. `components.md` — All reusable components
10. `council.md` — AI Council Chamber specification
11. `deliberation.md` — Live deliberation timeline
12. `verdict.md` — Verdict dashboard
13. `motion.md` — Animation specifications
14. `responsive.md` — Mobile and tablet adaptations

## Rules

15. `implementation-rules.md` — Mandatory implementation rules
16. `visual-qa.md` — Visual QA checklist

---

## Mandatory Instruction

Never invent a new visual language.
Never redesign existing components.
Every page must conform to this design system.

**Consistency has higher priority than creativity.**

**Reference files override everything.**
If the reference says 20px border radius and implementation says 16px — use 20px.

Before committing any UI change, run the Visual QA checklist (`visual-qa.md`).
