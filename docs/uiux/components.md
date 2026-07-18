# Components

## UI Primitives

Located in `src/components/ui/`.

| Component | Source |
|-----------|--------|
| Button | shadcn/ui-style, `src/components/ui/button.tsx` |
| Card | shadcn/ui-style, `src/components/ui/card.tsx` |
| Badge | shadcn/ui-style, `src/components/ui/badge.tsx` |
| cn() | `src/lib/utils.ts` (clsx + tailwind-merge) |

## Domain Components

Located in `src/components/`.

| Component | Path | Description |
|-----------|------|-------------|
| Background | `background/Background.tsx` | 6-layer background system |
| GununganBg | `background/GununganBg.tsx` | SVG gunungan outline |
| FloatingParticles | `background/FloatingParticles.tsx` | Animated particles |
| CouncilChamber | `council/CouncilChamber.tsx` | Full council visualization |
| CouncilCore | `council/CouncilCore.tsx` | Center brain node |
| AdvisorNode | `council/AdvisorNode.tsx` | Individual advisor card |
| NeuralNetwork | `council/NeuralNetwork.tsx` | SVG connection lines |
| DeliberationTimeline | `deliberation/DeliberationTimeline.tsx` | 9-step animated timeline |
| VerdictDashboard | `verdict/VerdictDashboard.tsx` | Executive verdict display |
| ThemeProvider | `theme-provider.tsx` | Dark/light mode context |
| Layout | `layout.tsx` | App shell (nav + footer + background) |

## Component Rules

- Every component must look custom-designed.
- Avoid generic Card/Button defaults — customize via Tailwind.
- Use `cn()` utility for conditional classes.
- All new components must be added to this list.
