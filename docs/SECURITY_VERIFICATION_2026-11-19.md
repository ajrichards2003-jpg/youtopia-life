# Youtopia Life security verification — updated 22 November 2026

**Status: materially improved, but not a penetration-test sign-off.** Changes remain isolated in draft PR #74; nothing has been merged or published from this branch.

## Completed and verified

### Production deploy
- Netlify project `c5dbb66c-397a-4579-b8ca-a92a1e05e438` reports production deploy `6afe48b814858c41a7b1a76d` ready and published from main commit `154be29688f295177de647aeabe58811ff2c05a2` on 19 November 2026.
- The deploy validation report scanned 5,317 files and reported no standard or enhanced secret-scan matches.
- The deployed `ask-youtopia` function exposes only `/api/ask-youtopia` and Netlify reports the configured sliding-window limit of 20 requests per 60 seconds, aggregated by IP and domain.
- Draft PR #74 now gives every Ask Youtopia JSON response explicit no-store, CSP deny-all, same-origin resource, no-referrer, nosniff, frame-deny and noindex headers; the regression check fails if these controls are removed.
- Deploy Preview `6b00da04683df2378d64e63b` built successfully from commit `9ce69e204da9f1d44628c09e212098f808b6cd39`. A direct preview read verified the expected function headers and a 405 response to GET.
- Controlled preview-only rejection checks returned 415 for non-JSON content, 403 for a disallowed origin and 413 for a 2,050-byte body. No production requests or authenticated AI calls were made.
- Netlify processed 73 redirect rules and one static header rule without deployment errors.
- A direct production header read on 22 November verified `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()`, CSP report-only, and HSTS with `max-age=2592000` on the homepage. The 30-day HSTS policy does not currently include `includeSubDomains` or `preload`.

### Public-only site
- Netlify publishes `public-site` via `python3 scripts/build-public.py`, not the repository root.
- The build script allowlists public root files and public extensions and excludes operational folders, hidden files, source maps and configuration formats.
- On 20 November 2026, direct browser checks of `/.env`, `/README.md`, `/netlify.toml`, `/docs/test.md`, `/.git/config` and `/wp-admin/` all rendered Youtopia's not-found page. None displayed the requested file or sensitive content.
- On 22 November, direct HTTP reads confirmed final `404` responses with HTML bodies for `/.env`, `/README.md`, `/netlify.toml` and `/wp-admin/`. The live `/api/ask-youtopia` route returned the intended `405` JSON response to GET.

### Security regression and dependencies
- Security-regression workflow run `44838556736` passed at the current PR head after the lockfile, dependency-audit and function-header regression steps were added.
- Draft PR #74 adds `package-lock.json`, resolving `@netlify/identity` 2.0.1, `@netlify/blobs` 9.1.6 and `openai` 7.61.0 for reproducible installs.
- A fresh `npm audit --audit-level=high --omit=dev` against that generated lockfile on 20 November 2026 found 0 known vulnerabilities.
- The PR workflow uses Node 24, installs locked production dependencies with lifecycle scripts disabled, and fails on high or critical npm audit findings before running the existing public-build checks.
- Dependabot PR #73 proposes the separate major `@netlify/blobs` 9.1.6 → 11.1.9 upgrade. It remains unmerged and needs compatibility testing; the draft security PR does not silently adopt it.

### Existing source controls
- `scripts/check-security.py` asserts the public-only build, response-header configuration, one canonical AI endpoint, platform rate limiting, allowed origins, maximum body size, authenticated users and a daily per-user quota.
- `netlify.toml` contains deny rules for common private-file and WordPress scanner paths.
- The AI function rejects non-POST methods, non-JSON content, oversized bodies, malformed JSON, disallowed origins, unauthenticated users, blank or overlong questions, and requests beyond the per-user daily quota.
- Error responses do not expose exception details.

### Account security
- Adam reported completing GitHub two-factor authentication on 20 November 2026 and receiving recovery codes.
- Recovery codes must remain outside the repository, PR comments and ChatGPT. Store them in an established password manager or encrypted offline recovery location.

## Still outstanding
- **HTTP headers:** current production static headers and the preview function headers are now directly verified. The stronger function headers remain preview-only until an approved merge/deploy. Review CSP reports before enforcement. Treat any future HSTS increase, `includeSubDomains` or `preload` as a deliberate domain-wide decision; do not enable them blindly.
- **CSP:** keep report-only until violations are reviewed; do not switch to enforcement blindly.
- **AI endpoint:** disallowed-origin, oversized-body, content-type and method rejection are verified on the preview. Authenticated quota behaviour and malformed/unauthenticated request paths remain for a separately approved controlled test; do not stress-test production.
- **Forms:** verify spam/bot protection in Netlify and use only a clearly labelled controlled test with approval.
- **Access:** owner still needs to verify Netlify MFA, GitHub/Netlify collaborator least privilege, branch protection/required checks, deploy permissions, and API-token scope/rotation.
- **Dependencies:** test Dependabot PR #73's major Blobs upgrade before any merge.
- **External:** obtain a scoped passive vulnerability assessment if stronger assurance is required; do not run intrusive scans without authorization.

## Release gate
Do not claim the site is “fully secure” or “Fort Knox.” Merge PR #74 only after review acceptance. Production deployment remains a separate deliberate decision.

## Decisions for Adam
1. Keep the GitHub recovery codes in a trusted password manager or encrypted offline backup; do not attach them here.
2. Confirm Netlify MFA and review who has repository and deploy access.
3. Decide whether PR #74 should be merged.
