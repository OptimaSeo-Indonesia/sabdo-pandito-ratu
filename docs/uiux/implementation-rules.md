# Implementation Rules

## Before Implementing Any Page

Read the following files **in order**. Do not skip.

1. `README.md`
2. `philosophy.md`
3. `visual-language.md`
4. `reference-spec.md`
5. `layout-spec.md`
6. `components.md`
7. `council.md`
8. `deliberation.md`
9. `verdict.md`
10. `motion.md`
11. `implementation-rules.md`
12. `visual-qa.md`

## Mandatory Rules

1. **Do not invent a new visual language.**
   Follow the design system exactly.

2. **Do not redesign existing components.**
   Use the components listed in `components.md`. If a component doesn't exist, create it following the patterns in this directory.

3. **Do not change spacing.**
   Use values from `spacing-sizing.md`.

4. **Do not change the color palette.**
   Use values from `colors.md`. Never add new colors.

5. **Do not create another visual hierarchy.**
   Follow `layout-spec.md` page structure.

6. **Consistency has higher priority than creativity.**
   If something doesn't match the design system, fix it.

7. **If unsure, follow the reference image instead of making assumptions.**
   `reference-spec.md` overrides personal design decisions.

8. **Every new component must be documented.**
   Add to `components.md`.

9. **Before committing, run Visual QA checklist.**
   See `visual-qa.md`.

10. **Never add a loading spinner.**
    Use the deliberation timeline instead.

11. **The AI Council is always the visual centerpiece.**
    Never bury it below other content.

12. **Background layers are mandatory.**
    Always use `<Background />` component via Layout.
