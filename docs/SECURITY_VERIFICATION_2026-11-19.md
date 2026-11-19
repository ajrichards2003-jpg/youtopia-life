# Youtopia Life security verification — 19 November 2026

**Status: partial verification; not a penetration-test sign-off.** No production configuration changed in this review.

## Confirmed from current main source
- Netlify publishes `public-site` via `python3 scripts/build-public.py`, not repository root.
- The build script allowlists public root files and public extensions, excludes operational folders, hidden files, source maps and configuration formats.
- `scripts/check-security.py` asserts the public-only build, response-header configuration, one canonical AI endpoint, rate limits, allowed origins, maximum body size, user verification and daily quota.
- `.github/workflows/security-regression.yml` runs security checks on pull requests and pushes to main.
- `netlify.toml` contains deny rules for common private-file and WordPress scanner paths.
- Netlify project API reports the current production deploy ready/current and Forms enabled.

## Checks NOT yet passed
- **Live HTTP**: externally request `/`, `/.env`, `/README.md`, `/netlify.toml`, `/docs/test.md`, `/.git/config`, `/wp-admin/`; verify protected paths do not return sensitive bytes, not merely a status code. Check headers including HSTS, nosniff, frame options, referrer and permissions policies. Review CSP report-only telemetry before enforcement. Live test attempt from the execution environment failed at DNS resolution; no result claimed.
- **CI**: inspect latest security-regression workflow run and its conclusion for the deployed commit, plus branch protection/required checks.
- **Dependencies**: review Dependabot PRs and run a dependency vulnerability audit in CI; test major upgrades before merging.
- **AI endpoint**: exercise allowed/disallowed origins, oversized JSON, malformed bodies, burst requests and unauthenticated requests using controlled low-volume tests. Do not stress-test production.
- **Forms**: inspect Netlify spam filtering and bot protection; perform one controlled test only with approval and distinguish it from genuine leads.
- **Access**: owner must verify MFA/passkeys, recovery options, least-privilege collaborators, Netlify deploy permissions, GitHub repository settings and API-token scope/rotation. Never paste credentials into a PR.
- **External**: scoped passive vulnerability assessment and remediation verification, not an intrusive scan without authorization.

## Release gate
Do not claim “fully secure” or “Fort Knox” until the live checks, CI, access controls, and dependency review are recorded with dates. Do not publish or merge this document automatically. An HTTP 404 on a random WordPress path is not by itself evidence of a successful attack.

## Decision for Adam
Authorize a later production deployment only if a tested code change is necessary; account-level MFA and permissions require owner review. This document requests no secrets or passwords.
