# Editing rules for contributors and AI

## Preserve the approved site
- Keep the blue/white winter palette, one central tree, opening branches, slowly breathing lights and snowfall.
- Preserve Japanese copy unless the user explicitly changes it. Do not invent profiles, testimonials, event hours or published form backends. Pending material uses deliberate blank placeholders.
- Event dates: December 19–20, 2026. The user identified v89 as the latest supplied KV. Check asset provenance before replacing exports; do not infer a source version from a renamed image.
- Venue: selectable `at` text + supplied MEGURO MARC SVG wordmark. Do not recreate brand logos as text.
- Buttons have a shared softly squared shape. People dialogs intentionally have rounded blue borders. Keep the introduction calendar menu outside document flow so adjacent photos do not move.

## Source ownership
- Edit HTML in `templates/pages/`; edit shared shell in `partials/`. Root HTML and `config/event.js` are generated, never the editing source.
- Edit event metadata in `config/event.json`; run `npm run build` afterwards.
- Shared header appearance lives in `snow-header.css`; shared footer and action shape live in `site-shell.css`. Page-specific changes should be scoped to that page.
- Preserve CSS order and media-query boundaries. Do not blindly merge separated rules or remove styles solely because they are unused in one viewport/state.
- `motion-state.js` owns pause/reduced-motion state. Effects subscribe to `snow-motion-change`. Cancel timers/frames while offscreen or hidden where applicable.
- `snow-decor.js`, `img/models/` and the Blender export script are retained for future reuse and are not loaded by the current pages.

## Validation and delivery
- Run `npm run format`, `npm run build`, `npm run format:check`, `npm test`, `npm run check` after changes.
- Visually check affected pages at desktop and mobile widths and test affected interactions. Use the configured browser tooling; do not substitute synthetic screenshots for actual rendered UI.
- Re-run page checks after edits to shared components. Compare with the existing design, not only with passing assertions.
- Do not reset unrelated working-tree changes. Do not publish, change DNS, submit forms, contact third parties or perform payments unless the user authorizes that scope.
- No need to add Storybook or migrate frameworks for this site. Avoid new production dependencies without a concrete need.
