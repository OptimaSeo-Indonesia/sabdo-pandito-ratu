# UI Components

## Component Library

### CouncilNode
- Icon, color gradient, name, role
- Status text (thinking/done/conflict)
- Progress bar (when active)
- Glow effect (node-specific color)
- Animations: pulseSoft (idle), ping+glow (active), border-pulse (conflict)
- Responsive: scales proportionally

### CouncilCore
- Central status display
- Phase: idle → deliberating → conflict → reflecting → consensus → verdict
- Shows: title, subtitle, step progress, consensus bar, confidence, wisdom score
- Animations: spinner, ping, glow

### NeuralConnection
- SVG line between two nodes
- 7 states: idle, active, agree, debating, conflict, reflection, consensus
- Color-coded per state
- Animated dash-offset flow
- Glow filter on active lines
- Particle dot moving along path

### GlassPanel
- border: 1px solid hsl(var(--border) / 0.4)
- background: hsl(var(--card) / 0.3-0.7)
- backdrop-filter: blur(24px)
- border-radius: 1rem
- box-shadow: glass shadow
- hover: border-color shifts to primary/0.12

### DeliberationTimeline
- 9 steps with icons
- Animated progress (line fills from top)
- States: pending, in_progress, completed, failed
- Status indicators: check, spinner, dot, cross

### VerdictDashboard
- Executive intelligence summary
- Circular gauges (wisdom, confidence)
- Insight cards (consensus, conflict, ethical alignment)
- Wisdom score dimension bars
- Reasoning tree
- Recommended actions
- Alternative decisions
- Collapsible sections

### GununganBg
- SVG outline of Javanese gunungan
- Monochrome gold (#C9A84C)
- Opacity: 2-5%
- Blur: 1-2px
- Centered, no fill
- Behind council chamber

### FloatingParticles
- CSS-based particle system
- Multiple small dots
- Random positions
- pulseSoft animation at different delays
- Opacity 0.15-0.5

### AuroraBackground
- Multiple radial gradients
- Animated translate
- 8s infinite alternate
- Pointer-events: none
- Fixed positioning
