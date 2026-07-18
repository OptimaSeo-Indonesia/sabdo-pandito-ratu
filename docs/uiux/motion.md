# Motion Specification

## Principles

- Animations are essential, not decorative.
- Everything must feel calm and intentional.
- Never flashy or distracting.
- Motion communicates system state.

## Animation Catalog

| Element | Animation | Duration | Timing |
|---------|-----------|----------|--------|
| Aurora gradient | Slow translate | 8s | ease-in-out infinite alternate |
| Neural lines (active) | Dash offset flow | 1s | linear infinite |
| Neural particles | Motion along path | 2–3s | linear infinite |
| Advisor node (idle) | pulseSoft | 3s | ease-in-out infinite |
| Advisor node (thinking) | ping + glow | 1s | ease-out infinite |
| Advisor node (conflict) | border pulse | 1.5s | ease-in-out infinite |
| Core (deliberating) | ping + spinner | 1s | linear infinite |
| Core (verdict) | double ping | 2s | ease-in-out infinite |
| Glass card hover | border-color shift | 0.3s | ease |
| Page entry (hero) | fadeUp | 0.6s | easeOut |
| Page entry (council) | fadeUp + scale | 0.7s | easeOut, delay 0.15s |
| Page entry (input) | fadeUp | 0.6s | easeOut, delay 0.35s |
| Stagger children | fadeUp staggered | 0.4s | delay: 0.05s each |
| Progress bars | width transition | 0.5–0.8s | easeOut |
| Gauge circles | stroke-dashoffset | 1s | easeOut |
| Page transition | fade in | 0.4s | easeOut |
| Timeline steps | slide in left | 0.3s | easeOut, staggered 0.04s |
| Verdict reveal | fadeUp | 0.6s | easeOut |
| Count-up numbers | opacity + translateY | 0.6s | easeOut |

## Keyframe Definitions

```css
@keyframes pulseSoft {
  0%, 100% { opacity: 0.15; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(1.05); }
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

## Framer Motion Usage

- Use `motion.div` for entry animations
- Use `AnimatePresence` for mount/unmount transitions
- Use `initial`, `animate`, `exit` props
- Never animate layout properties (width/height) with JS — use CSS transitions
