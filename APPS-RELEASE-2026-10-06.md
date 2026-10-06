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

## Family modes — 6 October 2026
Kids (suggested 7–12): 15 general discovery questions, mistakes continue. Teen (13–17): 15 science, reasoning and online-safety questions. Adult (18+): 30 health/evidence questions. Separate local scores and saved runs; no birth date, account, chat, advertising, purchases or health measurements. Default is Kids; modes are reading-level choices, not verified ages. Outbound navigation has a random grown-up multiplication check. This is a navigation barrier, not verified parental consent or identity.

Store audience declarations must include children and teens. Review Google Play Families requirements. Apple Kids category selection and age-band presentation need final account-owner review; do not use child-directed store metadata while declaring an adult-only audience. Verify all outbound paths and native back navigation on devices. A guardian should review Kids usability; independent clinical review is not claimed.

## Final family release-candidate verification
Commit a4b27680d4f22cdc798eb66cb69f00791477f536: GitHub Actions run 37400807367 passed all four Android/iOS simulator jobs. Automated game checks pass Adult paths, both youth question sets, gentle Kids completion, separate youth bests/saves, practice and resume. Both cache inventories include family navigation code. Browser checks verified Kids/Teen selection, 15-question youth practice, a Kids mistake continuing, source navigation prompting, incorrect grown-up answer staying inside the game and cancellation. Preview deployment passed.

Account-owner next steps: connect existing Apple Developer/App Store Connect and Google Play Console accounts; confirm the two bundle/package IDs belong to Youtopia; use distribution signing credentials through the platform secret store, never in repository or chat; install on real Android/iPhone devices for offline, large text, screen-reader and child usability checks; approve app-specific public privacy/support pages; complete truthful audience/rating/privacy declarations; take real-device screenshots; upload signed release builds to beta tracks and satisfy any account-specific testing requirements before submission. No signed release, beta distribution or store submission has occurred.
