# Architecture and ownership

## Static rendering

`templates/pages/*.html` + `partials/*.html` + `config/event.json` → `scripts/build.py` → root HTML and `config/event.js`.

The builder validates template keys, calculates the exclusive end of an all-day calendar event and versions CSS/JS by SHA-256 content. Output is deterministic and requires no server-side rendering at request time. The build fails on a missing local script/style or unknown token. The `--check` mode never writes files.

Shared component markers are build boundaries, not browser includes. The animated garland stays inline in the rendered page so pause states and animation timings continue to work. Page-only thank-you CSS/JS are external files for easier review. Original media are preserved; optimized images are independently versioned by their source checksum.

## Browser behavior

| Module | Responsibility |
| --- | --- |
| `site-shell.js` | Full-screen shared navigation, focus loop, background inert/scroll lock, Escape and link close |
| `motion-state.js` | One pause/reduced-motion source; temporary named suspension for overlays without changing the visitor preference |
| `snow-motion.js` | Hero snow, parallax, forest opening and warm light masks |
| `snow-logo.js` | Hero-to-header logo, tied to scrolling rather than decorative autoplay |
| `snow-atmosphere.js` | Page snowfall; coalesced layout reads and ~30fps drawing |
| `button-snow.js` | Visible-button particles; timers stopped when hidden or paused |
| `main.js` | Calendar providers, copy/share and hero boundary class |
| `people.js` | Native dialog, focus restoration, close behavior |
| `snowfund-thanks.js` | Thank-you snow accumulation; pauses offscreen/in background |

Order matters: `config/event.js` precedes `main.js`; `motion-state.js` precedes decorative consumers. Every script uses `defer`. No new production JS library was introduced. Prettier and PostCSS are development-only tools; lockfile pins their transitive dependencies.

## CSS layers

The existing cascade is retained for visual compatibility: base → page → winter treatment → shared header → shared shell → feature styles. Readable formatting, removal of obsolete particle styles and 32 shadowed declarations reduce ambiguity. Header appearance previously split across two final stylesheets now has one owner.

This is a conservative cleanup, not a claim that every legacy rule has been removed. Further pruning must include mobile, focus, open-menu, dialog, paused-motion and placeholder states. Moving a rule to a later stylesheet can change precedence even if the declaration is identical.

## Content boundaries

The site presents event information and links to external calendar/payment services. It does not confirm payments or store registrations. The thank-you animation is presentation only. Business decisions such as opening hours, contribution copy and publication of profiles remain editorial inputs, not derived facts.

`SnowMotion.setSuspended(reason, value)` stops decorative consumers while the menu or People dialog covers them. Each overlay owns its reason; closing one cannot resume another. `paused` and motion events expose the effective state; control labels retain the visitor’s preference. Page snowfall also cancels pending frames on pagehide and remeasures on pageshow.
