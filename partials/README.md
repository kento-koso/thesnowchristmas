# Shared HTML sources

`header.html` and `footer.html` are the common source for all five pages. `garland.html` is the homepage’s animated inline SVG.

Run `npm run build` after changing partials. Run `npm run check` to detect stale generated output. Root HTML is generated from `templates/pages/` and these partials; do not hand-edit shared blocks inside root HTML.

Tokens `{{home}}`, `{{top}}`, and `{{event.*}}` are resolved at build time. The browser receives complete static markup. See the root README for ownership and validation instructions. `partners/index.html` remains a standalone redirect and is not rendered through the shared shell.
