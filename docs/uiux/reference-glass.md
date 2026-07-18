# Reference Card & Border Styles (AnimaApp bundle)

## Card Style (Default)

```css
.card-ref {
  background: hsl(var(--card));
  border: 1px solid rgba(108, 99, 255, 0.22);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}
```

## Card Variants

| Element | Border Radius | Customization |
|---------|---------------|---------------|
| Deliberation Progress | `rounded-2xl` (16px) | Default card |
| Council Status | `rounded-[18px]` | Default card |
| Question Panel | `rounded-2xl` (16px) | `#070D22` bg, `rgba(108,99,255,0.22)` border |
| Sidebar Wisdom | `rounded-2xl` (16px) | `bg-card`, `rgba(108,99,255,0.22)` border |
| Advisor node | `rounded-full` | 72px circle, 2px colored border |
| Council Core | `rounded-full` | 140px circle, `1.5px rgba(108,99,255,0.5)` border |
| Nav item (active) | `rounded-[10px]` | `bg-grad-active-nav`, `rgba(108,99,255,0.55)` border |
| Action buttons | `rounded-[10px]` | `#111633` bg, `rgba(255,255,255,0.08)` border |

## Borders

| Element | Border |
|---------|--------|
| Cards | `1px solid rgba(108, 99, 255, 0.22)` |
| Textarea | `1px solid rgba(108, 99, 255, 0.16)` |
| Actions | `1px solid rgba(255, 255, 255, 0.08)` |
| Active nav | `1px solid rgba(108, 99, 255, 0.55)` |
| Council Core | `1.5px solid rgba(108, 99, 255, 0.5)` |
| Advisor | `2px solid {color}80` |
| Pending step | `rgba(255, 255, 255, 0.12)` |

## Shadows

| Element | Shadow |
|---------|--------|
| Cards | `0 8px 32px rgba(0, 0, 0, 0.35)` |
| Deliberate button | `0 8px 24px rgba(108, 99, 255, 0.35)` |
| Advisor nodes | `0 0 20px {color}4D, 0 0 40px {color}4D` |
| Council Core | `0 0 30px rgba(108,99,255,0.35), 0 0 60px rgba(108,99,255,0.15)` |
| In-progress step | `0 0 12px rgba(108, 99, 255, 0.6)` |
| Ajukan Question | `0 2px 8px rgba(108, 99, 255, 0.4)` |
