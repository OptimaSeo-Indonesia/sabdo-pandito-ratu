# Reference Glassmorphism Rules

## Glass Style (Default)

```css
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  box-shadow: /* very soft */;
}
```

## Glass Card

- Background: `rgba(255,255,255,0.05)`
- Backdrop blur: **18px**
- Border: `1px solid rgba(255,255,255,0.08)`
- Border radius: **20px**
- Shadow: very soft, minimal

## Glass Variants

| Element | Customization |
|---------|---------------|
| Nav | Transparent glass, blur |
| Question panel | Default glass, padding 28px |
| Verdict cards | Default glass, radius 20px |
| Advisor nodes | Glass with color gradient overlay |

## When NOT to Use Glass

- Advisor node icons: use solid color gradient instead
- Core node: use glass + glow
- Background layers: no glass (they're behind content)
