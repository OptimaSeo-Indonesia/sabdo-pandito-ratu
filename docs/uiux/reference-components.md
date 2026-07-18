# Reference Components (AnimaApp bundle)

## Navigation (Sidebar)

| Element | Value |
|---------|-------|
| Width | 240px |
| Background | `hsl(var(--sidebar))` |
| Items | Home, Deliberations, History, Council, Knowledge, Analytics, Settings, Documentation |
| Active style | `bg-grad-active-nav` + `border rgba(108,99,255,0.55)` |
| Inactive style | `text-muted` `hover:bg-[rgba(108,99,255,0.06)]` |
| Bottom | Wisdom Today card + copyright |

## Council Core

| Element | Value |
|---------|-------|
| Diameter | 140px |
| Style | Circle, radial gradient, `1.5px rgba(108,99,255,0.5)` border |
| Contains | Emblem image ("Council Core"), text "Balance • Wisdom • Truth" |
| Button | "Ajukan Question" with gradient `#A44BFF → #6C63FF` |

## Advisor Nodes

| Element | Value |
|---------|-------|
| Diameter | 72px |
| Style | Circle, `rounded-full`, `2px solid {color}80` |
| Background | `radial-gradient(circle at 40% 35%, {glow} 0%, rgba(3,7,22,0.9) 70%)` |
| Contains | Icon (32px), Name, Role, Green "Ready" dot |
| Colors | Sage=#A855F7, Strategist=#3B82F6, Guardian=#F59E0B, Analyst=#10B981, Visionary=#3B82F6, Ethicist=#EC4899 |

## Question Panel

| Element | Value |
|---------|-------|
| Background | `#070D22` |
| Border | `1px solid rgba(108, 99, 255, 0.22)` |
| Radius | 16px (rounded-2xl) |
| Title | "Submit a Question to the Council" |
| Textarea | `#050A1B` bg, max 2000 chars, placeholder text |
| Buttons | Upload Context, Voice Input, Suggestions (all `#111633` bg) |
| Toggle | Dry Run switch (`#1A1F36` track, `#6C63FF` active) |
| Submit | "Deliberate" gradient button `#A44BFF → #6C63FF` |

## Deliberation Pipeline

| Element | Value |
|---------|-------|
| Container | `bg-card rounded-2xl` with purple border |
| Steps | 8 |
| Status icons | Checkmark (done), pulsing dot (active), circle (pending) |
| Connectors | 2px gradient/solid/dashed lines |
| Live badge | Green pulsing dot |

## Council Status

| Element | Value |
|---------|-------|
| Container | `bg-card rounded-[18px]` with purple border |
| Grid | 2 columns |
| Items | 6 advisor cards with icon, name, description, progress bar |
| Bar gradients | Per-advisor colored gradients |
| Labels | Percentage shown to right of bar |

## Verdict Grid

| Element | Value |
|---------|-------|
| Width | 1280px max |
| Columns | 2 |
| Left | Executive Summary, Reasoning, Transcript (collapsible) |
| Right | Confidence, Wisdom, Consensus, Bias, Ethics, Recommendations |
| Cards | `bg-card` with purple border and shadow |
