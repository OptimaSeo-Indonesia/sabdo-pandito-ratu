# Reference UI Specification — Layout & Geometry

> This document describes the layout from the AnimaApp preview bundle.

---

## Desktop Canvas

```
┌─────────────────────────────────────────────────────────────────┐
│ ┌──────────┐  ┌─────────────────────────────────────────────┐  │
│ │          │  │  Header: Brand (56px) + User Controls       │  │
│ │ Sidebar  │  ├─────────────────────────────────────────────┤  │
│ │ 240px    │  │  ┌──────────────────────┐ ┌──────────────┐  │  │
│ │          │  │  │ Council Diagram      │ │ Deliberation  │  │  │
│ │ Nav:     │  │  │ (min-h 580px)        │ │ Progress      │  │  │
│ │ Home     │  │  │                      │ │ (380px)       │  │  │
│ │ Delib.   │  │  ├──────────────────────┤ ├──────────────┤  │  │
│ │ History  │  │  │ Question Input       │ │ Council       │  │  │
│ │ Council  │  │  │ (#070D22 card)       │ │ Status        │  │  │
│ │ Know.    │  │  └──────────────────────┘ │ (380px)       │  │  │
│ │ Analytics│  │                           └──────────────┘  │  │
│ │ Settings │  │                                               │  │
│ │ Docs     │  └─────────────────────────────────────────────┘  │
│ │          │                                                   │
│ │ Wisdom   │                                                   │
│ │ Card     │                                                   │
│ │ © 2025   │                                                   │
│ └──────────┘                                                   │
└─────────────────────────────────────────────────────────────────┘
```

- Sidebar: **240px** fixed, `bg-sidebar`
- Main content: `p-6 gap-6`
- Main grid: `1fr 380px` (left fills, right is fixed 380px)
- Page background: `#03020a` (body) / `hsl(var(--background))` (CSS)

## Sidebar

- Width: **240px**
- Background: `hsl(var(--sidebar))`
- Padding: `py-5 px-3`
- Nav items: 8 items with icons, 10px radius
- Active item: `bg-grad-active-nav` + purple border
- Bottom: Wisdom Today card, copyright

## Header

- Brand heading: **56px** font, bold, `leading-[1.05]`
- "Pandito Ratu" uses `text-gradient-brand` gradient
- Tagline: "Multi-AI Deliberation Engine" in accent color, 20px
- User profile: "Pandita Utama" with Pro badge

## Council

- Container min-height: **580px**
- Gunungan background image (absolute, top 7.4%, left -10.7%, width 32.2%)
- SVG hexagon connection lines
- Advisor positions (percentages of container):

| Advisor | Top | Left |
|---------|-----|------|
| Sage | 0% | 50% |
| Strategist | 22% | 82% |
| Guardian | 22% | 18% |
| Analyst | 62% | 18% |
| Ethicist | 62% | 82% |
| Visionary | 84% | 50% |

- Advisor node: **72px** circle, `rounded-full`, 2px colored border, radial gradient
- Council Core: **140px** circle, `rounded-full`, purple border/glow, emblem image

## Question Panel

- Background: `#070D22`
- Border: `1px solid rgba(108, 99, 255, 0.22)`
- Border radius: 16px (rounded-2xl)
- Shadow: `0 8px 32px rgba(0, 0, 0, 0.35)`
- Textarea background: `#050A1B`, rounded-[10px]
- Action buttons: `#111633` bg
- Deliberate button: gradient `#A44BFF → #6C63FF`

## Right Column (380px)

### Deliberation Progress
- Card: `bg-card`, `rounded-2xl`, purple border, shadow
- **8 steps**: Question Received, Context Analysis, Perspective Generation,
  Conflict Detection, Ethical Review, Reflection, Consensus Building, Final Verdict
- Step icons: checkmark (completed), pulsing dot (active), circle outline (pending)
- Connectors: 2px gradient lines for active, solid for done, dashed for pending

### Council Status
- Card: `bg-card`, `rounded-[18px]`, purple border, shadow
- Grid: 2 columns
- 6 advisor progress bars with colored gradients

## Verdict

- Max width: 1280px
- 2-column grid: left (summary, reasoning, transcript) + right (metrics)
- Cards: `bg-card` with purple border and shadow
- Border radius: `rounded-2xl`
