# Verdict Dashboard

## Layout

Executive intelligence dashboard with collapsible sections.

## Sections

1. **Executive Summary** — Decision headline + gauges
2. **Final Verdict** — Decision text, confidence badge
3. **Wisdom Score** — Circular gauge + dimension bars
4. **Confidence** — Percentage display
5. **Consensus Level** — Progress bar
6. **Conflict Score** — Count + details
7. **Ethical Alignment** — Principle evaluation cards
8. **Recommended Actions** — Bullet list
9. **Alternative Decisions** — Secondary list
10. **Reasoning Tree** — Expandable tree visualization
11. **Debate Transcript** — Full deliberation report (collapsible)

## Gauges

Circular SVG gauges with:
- stroke-dashoffset animation (1s duration)
- Score text centered
- Label below

## Insight Cards

Small glass cards with:
- Icon in colored gradient circle
- Value (large bold number)
- Label (small muted text)
- Entrance animation: fadeUp staggered

## Wisdom Score Dimensions

Horizontal bars for:
- Evidence Quality
- Perspective Diversity
- Ethical Alignment
- Long-Term Impact
- Uncertainty Handling
- Reversibility

Each bar animates width from 0 to score value.

## Reasoning Tree

Vertical tree with branches:
- Question → Evidence → Assumptions → Conflicts → Reflection → Consensus → Decision
- Each branch expandable
- Dots on timeline connecting branches
