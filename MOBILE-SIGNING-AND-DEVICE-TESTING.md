# Youtopia mobile release: signing, devices and submission

6 October 2026. Code and build preparation complete; credentials, signed distribution builds, real-device results and store submissions are pending. Android debug APKs and iOS simulator apps from Actions run 37400807367 passed compilation. Simulator apps cannot be installed on an iPhone. Debug APKs are device-test builds, not Play release bundles.

## Account facts needed

Confirm existing Apple Developer Program/App Store Connect and Google Play Console accounts, individual/organisation status, Google account creation date, Apple Team ID, app ID ownership, and available Android/iPhone devices. Account enrollment, legal agreements, payment and identity verification must be completed by the owner. Do not send passwords or private signing material in chat or commit them.

| App | Bundle/package ID | Android test artifact |
|---|---|---|
| Youtopia Life | com.youtopialife.app | mobile-android-debug |
| Youtopia Ascent | com.youtopialife.ascent | mobile-ascent-android-debug |

Download test artifacts through the signed-in repository Actions page: https://github.com/ajrichards2003-jpg/youtopia-life/actions/runs/37400807367 . Record the tested build SHA and device/OS. Install only on a device whose owner agrees to testing. Do not change store app IDs after registration.

## Android distribution signing

Reuse an existing registered upload key if one exists. Otherwise the account owner creates and backs up a new upload keystore through Android Studio: Build > Generate Signed Bundle / APK. Keep it in a private location outside the repository and store its passwords in a password manager. Prefer Google Play App Signing; upload keys and app signing keys have different roles. Never replace a registered signing identity arbitrarily.

Both Android projects read these environment variables: YOUTOPIA_UPLOAD_STORE_FILE (absolute path), YOUTOPIA_UPLOAD_STORE_PASSWORD, YOUTOPIA_UPLOAD_KEY_ALIAS, YOUTOPIA_UPLOAD_KEY_PASSWORD. Populate them privately through the local secure environment or approved build secret store. Do not put secret values in shell history, logs, committed config or chat. The release helper refuses to run without all four. Partial Gradle signing configuration also fails rather than silently producing an unsigned release.

Install main mobile dependencies first, then the selected app dependencies. On a machine with Node 22, Java 21 and the Android SDK, run `node tools/build_android_release.mjs mobile` and then the same command with `mobile-ascent` using that app's correct upload identity. Outputs: `<app>/android/app/build/outputs/bundle/release/app-release.aab` and `<app>/android/app/build/outputs/apk/release/app-release.apk`. Verify the AAB certificate with jarsigner and the APK with the Android SDK apksigner. Check the registered upload certificate fingerprint, package ID, version code and supported SDKs. No secret values are printed by the helper. Build failure means no release is ready.

Upload the signed AAB to each app's Play internal test first. Use the Play-delivered build on devices before proceeding to a closed test or production. For personal accounts created after 13 November 2023, Google currently requires at least 12 continuously opted-in closed testers for 14 days before applying for production access; internal tests do not replace this requirement. Check the actual account dashboard.

## Apple signing and TestFlight

On a Mac with supported Xcode: run the selected app's npm sync, open `<app>/ios/App/App.xcodeproj`, select target App > Signing & Capabilities, choose the owner's Apple Team and confirm the exact Bundle Identifier. Use automatic signing with the authorized account or an approved existing signing system. Select a connected physical iPhone for development testing. Select a generic iOS device for Product > Archive, validate and distribute through App Store Connect. Never upload an unsigned simulator app as an iPhone build.

Create matching app records in App Store Connect, upload archives and complete export-compliance answers from the actual build. Start with internal TestFlight; external testers may require beta review. Keep both app records, builds and release notes separate. Distribution certificates/profiles stay in the owner's Keychain or approved secret store; none have been created here.

## Device acceptance

Use DEVICE-TEST-RESULTS.csv to record actual outcomes. Every row begins NOT TESTED. At minimum: a compact Android phone, the owner's foldable if available, a compact iPhone and larger iPhone/iPad if supported. Check fresh install, first launch offline in airplane mode, every question mode, lifelines and results, separate mode saves, force-close/resume, parent-gate wrong/cancel/correct and alternative clicks, Android back, source return, TalkBack/VoiceOver, large text, portrait/landscape, small-screen clipping and reinstall/update behavior. Main app: all articles/images, search, saved reading, memory matching, breathing pause/background handling and privacy. Parent/guardian-supervised youth usability checks should verify reading and navigation; do not collect children's identity or health information.

A pass requires a named device/build, steps and observed result. Compilation and browser checks do not count as physical-device results. Fix critical failures, rebuild and rerun only affected paths plus core smoke tests. Capture store screenshots from the actual native release candidate, without preview overlays.

## Submission sequence

1. Confirm app names, identities, account ownership, territory choices and pricing with the owner.
2. Publish approved app-specific privacy policies and verify monitored support routes.
3. Finish real-device and accessibility acceptance; record final signed build fingerprints and version numbers.
4. Complete accurate store audience, age rating, privacy/Data Safety, SDK and health-content declarations. Ascent includes children and teens; do not declare it adult-only. Apple Kids-category treatment and regional age-assurance requirements require account-specific review.
5. Upload signed builds to beta tracks; resolve automated pre-launch reports and tester feedback. Satisfy account-specific testing requirements.
6. Finalize existing store-copy drafts, real-device screenshots and reviewer instructions. Set controlled/manual release where available.
7. Submit each app for review and track the actual review result. Store review and production access are not guaranteed or claimed complete.

Official sources checked 6 October 2026:
- https://developer.android.com/studio/publish/app-signing
- https://support.google.com/googleplay/android-developer/answer/14151465?hl=en
- https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/
- https://developer.apple.com/kids/
- https://support.google.com/googleplay/android-developer/answer/9867159?hl=en
