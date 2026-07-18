# Typography

## Font Stack

Primary: `Inter`, system-ui, sans-serif
Monospace: `JetBrains Mono`, monospace

## Font Sizes

| Element | Size | Weight |
|---------|------|--------|
| Hero title | text-4xl → sm:5xl → lg:6xl | bold (700) |
| Page title (session) | text-xl → sm:2xl | bold (700) |
| Section title | text-sm | font-medium (500) |
| Card title | text-sm | font-semibold (600) |
| Body | text-sm | normal (400) |
| Meta / labels | text-xs | medium (500) |
| Advisor name | text-[11px] → sm:text-xs | semibold (600) |
| Advisor role | text-[9px] → sm:text-[10px] | normal (400) |
| Status text | text-[9px] → sm:text-[10px] | normal (400) |
| Stats numbers | text-lg → text-2xl | bold (700) |
| Mono (sessions, ids) | text-xs | font-mono (400) |

## Hero Typography

- Hero title: Gradient text (`text-gradient` utility)
- Subtitle: text-muted-foreground, max-w-2xl
- Badge above hero: uppercase tracking-wider, text-xs

## Text Gradients

```css
.text-gradient {
  background: linear-gradient(135deg, hsl(var(--primary)), hsl(var(--primary-400)), hsl(var(--primary-600)));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```
