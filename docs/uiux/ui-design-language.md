# Sabdo Pandito Ratu UI Design Bible

> This document defines the permanent visual identity, design language, and user experience principles for Sabdo Pandito Ratu.
>
> Every UI implementation MUST follow this specification.
>
> Never invent a different visual style.
>
> Every new page and component must conform to this design system.

---

## Core Philosophy

Sabdo Pandito Ratu is NOT a chatbot.

Sabdo Pandito Ratu is NOT a landing page.

Sabdo Pandito Ratu is NOT an admin dashboard.

Sabdo Pandito Ratu is a **Multi-AI Deliberation Engine**.

Users should feel they are interacting with an intelligent council of AI advisors that think, deliberate, challenge assumptions, detect conflicts, reflect, and collaboratively produce transparent decisions.

The interface itself should communicate intelligence before the user even asks a question.

---

## Design Principles

The UI must communicate:
- Wisdom
- Transparency
- Intelligence
- Trust
- Fairness
- Deliberation
- Reflection
- Premium Quality
- Calmness
- Precision

Avoid:
- Bootstrap appearance
- Generic SaaS landing pages
- ChatGPT clone
- Material Design defaults
- CRUD dashboards
- Marketing-heavy layouts
- Generic AI chat interfaces

---

## Visual Inspiration

Inspired by: Linear, Raycast, Vercel, OpenAI, Arc Browser.

But should never become a visual copy. Sabdo Pandito Ratu must establish its own visual identity.

---

## Visual Language

**Theme:** AI Operating System

**Mood:** Premium, Futuristic, Elegant, Calm, Intelligent, Transparent

**Keywords:** Glass, Glow, Neural, Council, Deliberation, Motion, Wisdom

---

## Page Structure

**Forbidden:**
1. Hero
2. Textarea
3. Feature Cards
4. Footer

**Instead:**
1. Hero
2. AI Council Visualization
3. Question Panel
4. Live Deliberation
5. Verdict Dashboard

The AI Council must always be the visual centerpiece.

---

## Background Layers

The background must consist of multiple visual layers:

1. Dark gradient (near-black → deep navy)
2. Aurora gradient (radial glows)
3. Subtle neural network pattern
4. Gunungan outline — SVG, outline only, monochrome gold, opacity 2-5%, slight blur, no fill
5. Floating particles
6. Soft radial glow around council

The Gunungan is symbolic. Users should discover it naturally.

---

## AI Council Layout

```
                Sage

Guardian                     Strategist

          Council Core

Analyst                      Ethicist

             Visionary
```

The advisors form a hexagonal neural network. Every advisor connects to the center. Connections animate continuously.

---

## Council Core States

- Idle: "Council Ready · Awaiting Question"
- Running: "Consensus Building..." / "Analyzing Perspectives..." / "Reflecting..."
- Finished: "Verdict Ready · Confidence 94% · Wisdom Score 91"

---

## Neural Connection Colors

| State | Color |
|-------|-------|
| Agreement | Blue glow |
| Conflict | Amber glow |
| Reflection | Purple pulse |
| Consensus | White pulse |
| Idle | Dim indigo |

---

## Colors

Dark mode: Near black, deep navy, indigo, electric blue, violet, cyan accent
Light mode: Soft white, light gray, soft blue gradient, frosted glass, subtle shadows

---

## Motion

Use: glow pulse, node breathing, animated neural lines, timeline progression, soft hover lift, smooth transitions, progress animations, counter animations, aurora movement.

Avoid flashy animations. Everything calm and intentional.

---

## Component Library

Create reusable: CouncilNode, CouncilCore, NeuralConnection, GlassPanel, GlowButton, VerdictCard, Timeline, ScoreGauge, ReasoningTree, BackgroundGrid, AuroraBackground, FloatingParticles

---

## Mobile Priority

1. Hero
2. Council
3. Question
4. Live Deliberation
5. Verdict

Council must remain visually central on mobile.

---

## Acceptance Criteria

Complete only if:
- Not a chatbot
- Not a SaaS landing page
- AI Council is visual centerpiece
- Deliberation visible in real time
- Users observe advisors think, disagree, reflect, reach consensus
- Feels like AI Operating System, not a website
- Gunungan appears only as subtle symbolic inspiration
- Every page follows same design language

---

## Documentation Structure

```
docs/uiux/
├── ui-design-language.md    (this file)
├── ui-philosophy.md
├── ui-layout.md
├── ui-colors.md
├── ui-motion.md
└── ui-components.md
```

---

## Mandatory Instruction

For every UI task: Follow the design language and UI specifications in `/docs`. Do not invent a different visual style. All new components, layouts, animations, colors, and interactions must conform to the existing design system. Consistency is mandatory across the entire application.
