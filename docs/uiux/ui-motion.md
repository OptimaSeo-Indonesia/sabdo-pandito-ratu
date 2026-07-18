# UI Motion

## Principles

- Animations are essential, not decorative.
- Everything must feel calm and intentional.
- Never flashy or distracting.
- Motion communicates system state.

## Animations

| Element | Animation | Duration |
|---------|-----------|----------|
| Aurora background | Slow translate | 8s infinite alternate |
| Neural lines | Dash offset flow | 1s infinite |
| Neural particles | Motion along path | 2-3s |
| Advisor node (idle) | pulseSoft | 3s infinite |
| Advisor node (active) | ping + glow | 1s |
| Advisor node (conflict) | border pulse | 1.5s |
| Council core (deliberating) | ping + spinner | 1s |
| Council core (verdict) | double ping + glow | 2s |
| Glass card hover | border-color shift | 0.3s |
| Page entry | fadeUp | 0.6s |
| Stagger children | fadeUp staggered | 0.4s + 0.05s delay |
| Progress bars | width transition | 0.5-0.8s |
| Gauge circles | stroke-dashoffset | 1s |
| Hover lift | scale/translate | 0.2s |

## Page Transitions

- Route changes: fade in 0.4s
- Deliberation steps: slide in from left 0.3s
- Verdict reveal: fade up 0.6s
