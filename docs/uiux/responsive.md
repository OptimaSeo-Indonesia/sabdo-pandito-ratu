# Responsive Design

## Mobile Priority Order

Do not simply stack cards vertically. Reorganize:

1. Hero
2. Council
3. Question
4. Live Deliberation
5. Verdict

## Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | <640px | Single column, stacked |
| Tablet | 640–1024px | 2 columns for some sections |
| Desktop | >1024px | Full layout |

## Council on Mobile

- Same hexagonal formation, scaled proportionally
- Container: `max-h-[380px]` (compact mode)
- Node icons: `h-14 w-14` (slightly smaller)
- Text: `text-[11px]` for names, `text-[9px]` for roles
- Progress bars: narrower (w-24 instead of w-28)

## Navigation on Mobile

- Desktop: horizontal links with icons
- Mobile: hamburger menu (md:hidden)
- Slide-down panel with links + theme toggle

## Session Page on Mobile

- Timeline and content stack vertically
- Council sidebar becomes collapsed or secondary
- Touch targets minimum 44px
- Bottom spacing for comfortable scrolling

## Home Page on Mobile

- Hero text scales: `text-4xl` → `text-5xl`
- Council below hero
- Input card full width
- Example prompts wrap naturally
