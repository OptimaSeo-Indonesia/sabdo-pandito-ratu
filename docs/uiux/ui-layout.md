# UI Layout

## Page Structure

Every page follows this hierarchy:

1. **Hero** — centered title + subtitle
2. **AI Council** — hexagonal neural visualization
3. **Question Panel** — glass panel input (secondary)
4. **Live Deliberation** — animated timeline + advisor activity
5. **Verdict Dashboard** — executive intelligence cards

## Council Layout (Desktop)

```
                Sage
              (top-center)

Guardian                     Strategist
(top-left)                  (top-right)

          Council Core
            (center)

Analyst                      Ethicist
(bottom-left)              (bottom-right)

             Visionary
           (bottom-center)
```

## Council Layout (Mobile)

Same hexagonal formation, scaled proportionally. Council remains visually central.

## Grid

Home page: single column, centered, max-w-7xl.
Session page: 5-column grid (3 cols content + 2 cols council sidebar).
History page: single column, max-w-5xl.
