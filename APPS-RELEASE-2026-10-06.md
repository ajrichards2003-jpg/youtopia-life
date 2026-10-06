# Youtopia Life and Youtopia Ascent — release candidate

Two separately packaged apps. Version 1.0.0, build 1. Preparation and previews only; no production merge, membership purchase or store submission.

| App | Identity | Included core experience |
|---|---|---|
| Youtopia Life | com.youtopialife.app | Six complete source-linked articles, search/filter, local saved reading, Ascent, memory matching, Calm & Connect, local privacy, optional browser offline cache and bundled native content. Wider website features open externally. |
| Youtopia Ascent | com.youtopialife.ascent | Thirty questions, fresh 15-question challenge, three lifelines, protected ranks, banking, practice, missed-question review, personal best, resume, local privacy and offline game content. |

## Reproduce

From `mobile`: `npm ci` then `npm run sync`. From `mobile-ascent`: `npm ci` then `npm run sync`. Main mobile dependencies are required first because the standalone build bundles the shared native bridge. Each folder contains its own Android and iOS project. Brand assets are exported from the canonical logo and original geometric summit artwork; `tools/build_app_branding.py` refreshes native icons/splashes. Debug logging is disabled in both Capacitor configurations.

## Verification

The game test covers a complete summit, checkpoints, banking, all 30 practice questions, review, all three lifelines, second chance, resume and invalid save rejection. Both web packages and Capacitor sync pass. Offline manifest entries resolve locally. The Netlify PR 26 preview passed browser checks for question loading, source explanations, saved-run recovery, memory interaction, calm start and optional offline download. GitHub Actions run 37399454740 successfully compiled both Android debug APKs and both unsigned iOS simulator apps.

The workflow builds Android debug APKs and unsigned iOS simulator apps. These are testing artifacts, not signed store release binaries.

## Still needed for store launch

Physical-device tests; VoiceOver/TalkBack and large-text tests; developer-account and ID ownership; distribution signing; final privacy/SDK and health-content declarations; public app-specific privacy and monitored support; actual device screenshots; TestFlight/Play testing; final submission approval. Signing and developer credentials have not been supplied. The current execution host has no Android SDK or Xcode, so local native compilation is unavailable.

Neither app measures health or assigns IQ/brain-age ratings. The memory and breathing activities are recreational. Article caveats and sources remain part of the reading experience.
