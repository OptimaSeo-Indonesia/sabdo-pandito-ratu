# Background Specification

The background consists of **6 stacked layers**.

Every page uses `<Background />` component (rendered in Layout).

## Layer 1: Dark Gradient

Solid dark background via CSS variable:
```css
background-color: hsl(var(--background));
```

## Layer 2: Aurora Gradient

Multiple radial gradients, animated translate (8s infinite alternate).

Dark mode:
```
radial-gradient(ellipse 90% 60% at 50% -20%, rgba(99,102,241,0.12), transparent)
radial-gradient(ellipse 70% 50% at 80% 30%, rgba(139,92,246,0.08), transparent)
radial-gradient(ellipse 60% 40% at 20% 60%, rgba(52,211,153,0.03), transparent)
radial-gradient(ellipse 50% 30% at 50% 80%, rgba(99,102,241,0.04), transparent)
```

Light mode: lower opacity values.

## Layer 3: Neural Dot Grid

Subtle dot grid using CSS radial-gradient background image.
```css
background-image: radial-gradient(circle at 1px 1px, hsl(var(--primary)) 0.5px, transparent 0.5px);
background-size: 60px 60px;
opacity: 0.015 (light) / 0.03 (dark);
```

## Layer 4: Gunungan SVG

Javanese cosmic tree/mountain outline.
- SVG outline only, no fill
- Stroke color: `#C9A84C` (monochrome gold)
- Stroke width: 1.5px
- Opacity: 3% (light) / 4% (dark)
- Blur: 1px
- Centered, h-[80vh], w-auto
- Behind council chamber position

## Layer 5: Floating Particles

30 dots, randomly positioned.
- Size: 1–3px
- Opacity: 0.1–0.35
- Animation: `pulseSoft` at staggered delays

## Layer 6: Radial Glow

Large radial gradient behind council.
```css
radial-gradient(circle, hsl(var(--primary)) 0%, transparent 70%)
```
- h-[60vh], w-[60vh]
- Positioned at left:50%, top:33%
- Opacity: 4% (light) / 6% (dark)

## Implementation

All layers are `pointer-events-none`, `fixed`, full viewport.
Centered in `Layout.tsx` via `<Background />` component.
