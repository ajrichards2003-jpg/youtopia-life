# Youtopia Ascent + Vital Rush — launch preparation

7 October 2026. These are the two active games. The broader Youtopia Life app is on hold. Preview first; neither a production website merge nor an app-store submission has happened in this update.

| App | Source | Native project | Proposed package/bundle ID |
|---|---|---|---|
| Ascent | ascent-app | mobile-ascent | com.youtopialife.ascent |
| Vital Rush | vital-rush | mobile-vital-rush | com.youtopialife.vitalrush |

Both are version 1.0.0/build 1. Confirm identity ownership and available build numbers in the developer accounts. Do not change a registered app's signing identity. Launch pricing proposed: free, no ads or purchases. No new paid tool, account enrolment or charge has been initiated.

## Product readiness
Ascent: 90 source-linked questions; 30 per audience, ten per tier; fresh 15-question climbs; three lifelines; separate local progress; missed-question review; practice replay preserves its mode; browser offline support; bundled native content.

Rush: original three-lane runner; food-powered fictional growth; shields; research points; fair obstacle rows; daily route; 35-second non-penalising practice; gentle pace; saved motion/pace preferences; local bests and earned suits; optional sound; pause/lifecycle handling; privacy and confirmed reset; browser offline downloads; separate portrait iOS/Android wrapper and original icon/splash assets.

Code and browser checks are evidence of functionality, not an independent content review or physical-device result. Rush requires sight despite keyboard/status support; test real usability. Neither game promises health outcomes, IQ ratings or download rankings.

## Launch sequence
1. Approve the current preview and final public privacy/support pages. Publish only the two games and their supporting pages after approval. The inherited broader-app changes in the preview branch must not be included in a production merge while that app is paused; prepare a games-only production change set first.
2. Confirm Apple Developer/App Store Connect and Play Console account status/type, Apple Team ID, and app ID availability. Account owners handle enrolment, payments, identity checks and legal agreements themselves. Credentials/private keys must stay out of chat/repository.
3. Build and test on an actual iPhone and Android device. Record exact build SHA, OS, device, expected/observed results and defects in DEVICE-TEST-RESULTS.csv. Test a small phone and tablet, airplane-mode first launch, background/return, Android back, touch/swipes, pause, storage retention/reset and accessibility. For Ascent, test all audience modes/lifelines/resume/outbound gates. For Rush, complete practice, regular/daily runs, jump versus wall, shields/Glow, unlocks, resize/orientation and app switching. Capture actual release-candidate screenshots.
4. Use existing registered signing credentials or generate/register an upload identity through the owner's approved tooling. `node tools/build_android_release.mjs mobile-ascent` and `node tools/build_android_release.mjs mobile-vital-rush` require four private signing environment variables. Both yield signed AAB/APK only when configured correctly. On macOS, sync/open each iOS project, select the owner's Team, test on device, archive/validate and upload to App Store Connect. Debug APKs and unsigned simulator apps are not store releases.
5. Start Play internal testing and TestFlight. Complete audience/content-rating, privacy/Data Safety, SDK inventory, support, export-compliance and relevant health-app declarations from the final build. Check whether the actual Play account requires the new-personal-account closed test: currently 12 continuously opted-in testers for 14 days before applying for production access. Do not invent tester participation or launch dates.
6. Resolve beta feedback. Approve final metadata/assets, then submit both for review. Approve the rollout once the stores accept them. Launch announcements should use real store links only after they exist.

## Store package
- mobile-ascent/STORE-SUBMISSION-DRAFT.md: Ascent copy, review notes and screenshot subjects.
- mobile-vital-rush/STORE-SUBMISSION-DRAFT.md: Rush copy, review notes and screenshot subjects.
- ascent-app/privacy.html and vital-rush/privacy.html: in-app/public policy candidates.
- vital-rush/icon-1024.png and native icon/splash resources: original Rush art.
- MOBILE-SIGNING-AND-DEVICE-TESTING.md and tools/build_android_release.mjs: signing workflow.
- DEVICE-TEST-RESULTS.csv: physical-device evidence, currently NOT TESTED.

## Remaining facts
Developer-account access/enrolment/type, Team ID, ID ownership, devices, real signing material, device evidence, public policy publication, verified support inbox, final ratings/privacy declarations, store screenshots and beta/store review are not confirmed. No store submission is possible to claim until those steps occur. Web preview links are not App Store/TestFlight/Play listing links.

## Current official references (checked 7 October 2026)
- Apple review, metadata, privacy and Kids category: https://developer.apple.com/app-store/review/guidelines/
- Google new personal-account tests: https://support.google.com/googleplay/android-developer/answer/14151465
- Capacitor native setup: https://capacitorjs.com/docs/getting-started
