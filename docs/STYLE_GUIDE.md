# Style guide — Chrome Pantry v1

Y2K chrome on a dark base; grunge only as a **light global background texture**. Do not introduce new palettes per screen.

## Typography (Google Fonts)

| Role | Font | Weights | Variable |
|------|------|---------|----------|
| Headings | Chakra Petch | 600, 700 | `--font-display` |
| Body / chat | IBM Plex Sans | 400, 500, 600 | `--font-body` |
| Errors / meta | IBM Plex Mono | 400, 500 | `--font-mono` |

- H1: Chakra Petch 700, `letter-spacing: -0.02em`, avoid long ALL CAPS.
- Chat body: IBM Plex Sans, minimum 16px on small viewports.

## Color tokens

| Token | Hex |
|-------|-----|
| `--bg-deep` | `#070714` |
| `--bg-surface` | `#0f1024` |
| `--bg-elevated` | `#16183a` |
| `--border-subtle` | `#2a2d5c` |
| `--border-chrome` | `#5b5fc7` |
| `--text-primary` | `#f3f4f8` |
| `--text-muted` | `#9aa3b2` |
| `--accent` | `#5eead4` |
| `--accent-hot` | `#f0abfc` |
| `--danger` | `#fb7185` |
| `--warning` | `#fcd34d` |
| `--accent-chrome` | `#818cf8` |

**Gradient wash (header only):** `135deg`, `#5eead4` → `#6366f1` → `#f0abfc` at ≤ 12% opacity.

## Shape

- `--radius-card`: 14px
- `--radius-pill`: 999px

**Card shadow:** `0 8px 28px rgba(0,0,0,0.45)`, `inset 0 1px 0 rgba(255,255,255,0.06)`.

**Focus:** `outline: 2px solid var(--accent-chrome); outline-offset: 2px`.

## Texture

Single noise layer on `#root` or `body::before`, opacity 0.035–0.06, `pointer-events: none`, `mix-blend-mode: soft-light`.

## Motion

150–220ms, `cubic-bezier(0.2, 0.9, 0.2, 1)`. Honor `prefers-reduced-motion`.

## Components

- **Header:** “Food Planner” + muted tagline; optional `✦` accent in `--accent-hot`.
- **Assistant messages:** elevated card, left border 4px `var(--accent)`.
- **User messages:** elevated, aligned end.
- **Send button:** background `var(--accent)`, label `#052e2a`.

Reference implementation: [frontend/src/index.css](frontend/src/index.css).
