# Glassmorphism Specification

## Glass Card

The primary surface component.

```
.glass-card {
  border-radius: 1rem;
  border: 1px solid hsl(var(--border) / 0.4);
  background-color: hsl(var(--card) / 0.35);      /* dark mode */
  background-color: hsl(var(--card) / 0.65);      /* light mode */
  backdrop-filter: blur(24px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);        /* dark mode */
  box-shadow: 0 8px 32px rgba(0,0,0,0.04);       /* light mode */
  transition: border-color 0.3s ease;
}
```

Hover: `border-color: hsl(var(--primary) / 0.12)`

## Glass (Generic)

For simple glass overlays.

```
.glass {
  border: 1px solid hsl(var(--border) / 0.5);
  background-color: hsl(var(--card) / 0.5);
  backdrop-filter: blur(24px);
}
```

## Shimmer Effect

For input focus state.

```
.shimmer {
  background: linear-gradient(90deg, transparent 0%, hsl(var(--primary) / 0.08) 50%, transparent 100%);
  background-size: 200% 100%;
  animation: shimmer 2s linear infinite;
}
```

## When to Use Glass

- Cards and panels
- Input containers
- Council node backgrounds (via gradient, not glass)
- Sidebar panels
- Navigation bar
