# Review and release

## Reviewable changes

1. Edit source templates, shared partials, CSS/JS or event configuration.
2. Run formatting, build, tests and checks listed in README.
3. Review source **and generated** diff. Japanese copy changes require an explicit editorial reason; baseline updates are reviewed separately from mechanical changes.
4. Check the affected desktop/mobile screens. For shared changes, include all five pages.

## Functional checks

- Hero logo moves into header; dates stay readable; menu opens/closes and Escape returns focus.
- Pause/resume controls affect snowfall, lighting and button particles; reduced-motion preference is respected.
- Calendar menu does not move adjacent photos. Google and ICS encode Dec 19–20 with exclusive ICS end Dec 21. Inspect URLs/download contents without creating an event in someone’s account.
- People opens the matching profile, closes with Escape/backdrop/close button and restores focus.
- Snowfund links retain the intended destination. Do not test by submitting a real payment.
- Pending content remains clearly pending. No invented biography, quotation or operational time is introduced.

## Publication boundary

This change does not publish, push or alter hosting/DNS. The quality workflow is read-only and has no deployment job. Current GitHub Pages delivery can continue to use committed static output. If delivery is moved to an artifact pipeline, include root HTML/CSS/JS, generated `config/event.js`, required `img/`, `partners/`, `CNAME`, `.nojekyll` and `robots.txt`; exclude development tools and local work files.

Before a release, record commit/revision, checks run, browsers/devices exercised, confirmed event details and known remaining items. Opening times and pending profiles remain editorial release inputs. Real-device Safari/Android checks and production network timing are separate from desktop browser viewport emulation.

## Rollback

Retain the prior deployed revision. Revert the specific source/configuration change, regenerate with the same locked toolchain, rerun checks and publish through the established process. Do not overwrite unrelated local changes or replace only generated HTML while leaving mismatched sources.
