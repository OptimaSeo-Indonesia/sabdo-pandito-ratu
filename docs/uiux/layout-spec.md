# Layout Specification

## Page Structure (Forbidden)

This layout is **forbidden**:
1. Hero
2. Textarea
3. Feature Cards
4. Footer

## Page Structure (Mandatory)

This layout is **mandatory**:
1. Hero
2. AI Council Visualization
3. Question Panel
4. Live Deliberation
5. Verdict Dashboard

The AI Council must always be the visual centerpiece.

---

## Council Layout (Desktop)

```
                Sage
              (top-center)

    Guardian                Strategist
   (top-left)              (top-right)

          Council Core
            (center)

    Analyst                 Ethicist
  (bottom-left)          (bottom-right)

             Visionary
           (bottom-center)
```

Position percentages (relative to container):
- Sage: `left: 50%, top: 8%`
- Guardian: `left: 16%, top: 27%`
- Strategist: `left: 84%, top: 27%`
- Core: `left: 50%, top: 48%`
- Analyst: `left: 16%, top: 67%`
- Ethicist: `left: 84%, top: 67%`
- Visionary: `left: 50%, top: 85%`

## Grid

| Page | Container | Columns |
|------|-----------|---------|
| Home | max-w-7xl, centered | Single column |
| Session | max-w-7xl | 5-col (3 left + 2 right sidebar) |
| Sessions (History) | max-w-5xl | Single column |

## Z-Index Stacking

| Layer | Z-Index |
|-------|---------|
| Background (aurora, gunungan, particles) | 0 (fixed) |
| Page content | 10 (relative) |
| Nav | 50 (sticky) |
| Modals / overlays | 100 |
