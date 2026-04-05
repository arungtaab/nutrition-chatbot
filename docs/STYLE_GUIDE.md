# Style guide — Organic editorial (“Nourish”)

The UI is meant to feel like a **small magazine or studio cookbook** sitting on a **natural, jewel-toned** spine—not clinical software and not a purple gradient SaaS hero. **Art deco** nods (brass, geometry, flank figures) stay, but the **primary read** is *organic editorial*: warm paper, soft grain, **asymmetric** type column, and **layered** surfaces.

Typography and tokens live in [frontend/src/index.css](../frontend/src/index.css). Shell layers are composed in [DecoShell.jsx](../frontend/src/components/ui/DecoShell.jsx).

## Typography (Google Fonts)

| Role | Font | Rationale |
|------|------|-----------|
| Display / wordmark | **Fraunces** | Variable optical size; distinctive editorial display without default “wellness” tropes. |
| Body / chat / long copy | **Newsreader** | True editorial serif for paragraphs and assistant messages—reads like print, not product UI. |
| UI chrome | **Figtree** | Clear small caps, chips, buttons, labels, stack strip—humanist sans, not Inter/Roboto. |

Use `font-optical-sizing: auto` on Fraunces display sizes. Keep body at comfortable **~18px** root for readability on cream panels.

## Color (natural spine + paper)

- **Jewel green** (`--deco-jewel*`) remains the **atmospheric spine** behind content.
- **Paper / cream** (`--deco-paper`, `--deco-cream`, `--deco-cream-warm`) for elevated “sheets” (features, chat dock).
- **Brass** for accents and focus; **mauve** (`--deco-mauve*`) for secondary rules and trust-band emphasis—check **contrast** when mauve or brass sits on cream (body text should stay **dark ink** on light panels).

## Memorable hook (one idea, layered)

1. **Soft smoke blobs** — blurred radial stacks (`deco-blobs`) for atmosphere; slow drift.
2. **Paper wash + grain** — `deco-paper-wash` (warm screen tint) + SVG **noise** overlay (`deco-grain`).
3. **Sunburst** — kept **subtle** (lower opacity, slower rotation) so geometry supports, not dominates.
4. **Asymmetric hero** — single left **gutter rule** (no symmetric brass frame); copy **left-aligned** with editorial inset.
5. **Layered paper cards** — stacked **box-shadows** + inset rule on feature panels (`deco-feature`).

## Section dividers

Rules are **intentionally uneven** (short rail + diamond + longer fade) so the rhythm feels editorial, not perfectly centered deco symmetry.

## Motion

- **Blob drift** and **sunburst** rotation honor **`prefers-reduced-motion: reduce`** (animations off).
- **Hero stagger** (`deco-reveal`) also disables under reduced motion (no fade-in trap).
- Keep motion **slow and sparse**—no decorative parallax spam.

## Performance

- Decorative layers use **`transform`** / **`filter`** on fixed pseudo-fullscreen elements—keep **one** blurred blob layer (already merged into a single `deco-blobs` div).
- Avoid extra canvas/WebGL; prefer **CSS** only (no new heavy deps).
- `translateZ(0)` on the blob layer encourages a stable compositor layer; don’t sprinkle `will-change` everywhere.

## Accessibility

- **Focus**: visible rings on chips, inputs, buttons (`:focus-visible`, brass/jewel tones).
- **Contrast**: primary copy on paper panels uses `--deco-cream-ink` / `--deco-muted`; verify brass-on-cream isn’t used for small text.
- **Decorative** sunburst, blobs, grain, vignette, paper wash: **`aria-hidden="true"`** on shell nodes.
- Chat flank **`<img alt="">`** when purely ornamental.
- **`SectionDecoDivider`**: `role="separator"` where used for visual section break (decorative only).

## Chat flank art

- Files: `chat-flank-left.png`, `chat-flank-right.png` in [frontend/public/illustrations/](../frontend/public/illustrations/).
- **Attribution:** Freepik — **“Designed by Freepik”** in footer ([App.jsx](../frontend/src/App.jsx)) and [ATTRIBUTION.txt](../frontend/public/illustrations/ATTRIBUTION.txt).
- **Layout:** `.deco-chat-row` — figures flank the dock; hidden on narrow viewports (about 680px and below).
