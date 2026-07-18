# Reference Layout Grid

## Desktop (>1024px)

```
┌──────────────────────────────────────────────────┐
│  Nav (72px, glass, blur)                        │
├──────────────────────────────────────────────────┤
│                                                  │
│              Hero (max 900px)                    │
│              Heading 64px                        │
│              Subtitle 22px                       │
│              gap 20px                            │
│                                                  │
│              ░░░ 48px ░░░░                        │
│                                                  │
│          Council (620px diameter)                │
│                                                  │
│              ░░░ 48px ░░░░                        │
│                                                  │
│          Question Panel (900px)                  │
│          padding 28px                            │
│                                                  │
└──────────────────────────────────────────────────┘

Outer padding: 64px
Between sections: 72px
```

## Council Layout (Desktop)

```
                Sage

Guardian                     Strategist

          Council Core
          (160px diameter)

Analyst                      Ethicist

             Visionary
```

- Council container: 620px diameter
- Core: 160px diameter
- Advisor nodes: 96px diameter
- Connections: 2px stroke, 30% opacity

## Verdict Grid (Desktop)

```
┌─────────────────────┬─────────────────────────┐
│  Executive Summary  │  Confidence             │
│                     │  Wisdom                 │
│  Reasoning          │  Consensus              │
│                     │  Bias                   │
│  Transcript         │  Ethics                 │
│                     │  Recommendations        │
└─────────────────────┴─────────────────────────┘
```

- 2 columns
- Cards: glass, radius 20px
- Max width: 1280px

## Mobile (<640px)

Stack vertically, same priority order:
1. Hero
2. Council (scaled proportionally)
3. Question
4. Deliberation
5. Verdict (single column)

## Tablet (640–1024px)

Same as desktop but scale council proportionally.
