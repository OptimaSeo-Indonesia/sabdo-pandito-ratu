# AI Council

## Layout

Six advisors in hexagonal sacred geometry formation around a central core.

See `layout-spec.md` for exact position percentages.

## Advisor States

| State | Visual |
|-------|--------|
| idle | Soft pulse animation (3s cycle), dim opacity |
| thinking | Ping ring + glow expansion + progress bar (node-specific color) |
| conflict | Red border pulse animation |
| done | Static, success color |

## Status Labels

Idle: "Awaiting query", "Standing by", "Prepared", "Ready"
Thinking: per-advisor phrases (e.g. "Evaluating ethics", "Scanning risks")

## Neural Connection States

| State | Color | Animation |
|-------|-------|-----------|
| idle | Dim indigo | None |
| active | Blue | Dash-offset flow, glow |
| agree | Emerald | Dash-offset flow |
| debating | Amber | Dash-offset flow |
| conflict | Rose | Glow pulse |
| reflection | Violet | Slow pulse |
| consensus | Indigo | Static, dim |

## Council Phase Flow

```
idle → deliberating → conflict → reflecting → consensus → verdict
```

Each phase changes:
- Core display (title, subtitle, progress bar)
- Connection line colors
- Advisor node animations
- Center glow color

## Core Display

| Phase | Title | Subtitle |
|-------|-------|----------|
| idle | Council Ready | 6 Advisors · Transparency Enabled |
| deliberating | Deliberating | Step X/9 |
| conflict | Conflict Detected | X Conflicts Active |
| reflecting | Reflecting | Synthesizing insights |
| consensus | Building Consensus | Consensus X% |
| verdict | Verdict Ready | Confidence X% · Wisdom X |
