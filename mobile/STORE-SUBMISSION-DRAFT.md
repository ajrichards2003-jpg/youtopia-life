# Youtopia Life — store submission draft

**Status:** working draft for review. This file does not represent an Apple App Store or Google Play submission, approval, age rating, privacy declaration or developer-account purchase.

**Current code basis:** `preview-youtopia-app-oct6`, reviewed 6 October 2026 (Australia/Sydney).

## Product positioning

**App name:** Youtopia Life  
**Subtitle / short description:** Evidence-led health discovery, reading and play  
**Bundle / application ID:** `com.youtopialife.app` — ownership and availability still require verification in the relevant developer accounts.

### Promotional text

Explore evidence-led stories about sleep, recovery, nutrition and emerging health ideas. Save articles on your device, read an optional offline collection and test your knowledge in Youtopia Ascent.

### Short description

Discover health evidence, save articles locally and climb Youtopia Ascent.

### Full description

Youtopia Life is an evidence-led discovery app for people curious about health, human potential and emerging ideas.

Read complete source-linked articles inside the app, search by topic and save useful stories to a reading list stored on your device. Optional offline reading downloads the included library so it remains available without a connection.

Youtopia Ascent is a 15-question health-and-evidence challenge with five progress ranks and source-linked explanations. Its ranks reflect game progress only. They are not an IQ score, brain-age estimate, diagnosis or clinical assessment.

The first release includes:

- Six complete source-linked evidence articles.
- Topic search and filters.
- A device-local saved-reading list.
- Optional offline reading.
- Youtopia Ascent.
- Links to the wider Youtopia Life website.

Youtopia Life is educational. It does not diagnose, treat or prevent disease, replace professional medical advice, or measure health data.

### Keywords for review

health education, wellness evidence, sleep, recovery, nutrition, longevity, science, reading, quiz

Do not add disease-treatment, clinical, diagnostic, anti-ageing guarantee or unsupported performance keywords.

## Store URLs

| Field | Proposed value | Gate |
| --- | --- | --- |
| Privacy policy | https://youtopialife.com/privacy/ | Recheck live page against the final native build and declarations. |
| Support | https://youtopialife.com/contact/ | Confirm monitored support route and response owner. |
| Marketing | https://youtopialife.com/app/ | Do not use until the app page is approved and public. |

## Current data inventory

This inventory is based on the current source code and must be rechecked after the final native build and dependency review.

| Data or capability | Current behaviour | Store declaration note |
| --- | --- | --- |
| Account | No app account or sign-in. | Do not claim account deletion is available or required. |
| Health data | The app does not request, import or measure health data. | Reassess before adding wearables, HealthKit, Health Connect or personalised health features. |
| Analytics / advertising | No app analytics or advertising code is intentionally included. | Verify compiled binaries and all SDK dependency reports before selecting “no data collected.” |
| Saved reading | Article IDs are stored locally on the device. | Device-local preference; not transmitted by the app. |
| Ascent progress | Best progress is stored locally on the device. | Device-local game state; not transmitted by the app. |
| Offline library | Only after the user enables it, a service worker/native web cache stores included app files and images locally. | Explain in privacy/support copy; linked websites remain online. |
| External links | Website, source, privacy and support links open outside the app. | Destination sites have separate data practices; confirm native browser handling. |
| Notifications, contacts, camera, microphone, location | Not used by the current release. | Do not add permissions unless the product requirement and declaration are reviewed. |

## Preliminary classification notes

- Educational health and wellness content, not a medical device.
- No simulated gambling or real-money rewards.
- Ascent ranks describe quiz progress and must remain clearly non-clinical.
- The final Apple age-rating questionnaire and Google content-rating questionnaire must be completed from the actual release build. Do not advertise a rating before the stores assign or confirm it.
- Review all article language, linked destinations and imagery for the selected age audience before submission.

## App-review notes draft

Youtopia Life provides a self-contained evidence library, device-local saved reading, optional offline access and a 15-question educational challenge. No login is required.

To test:

1. Open **Learn**, search for “sleep” and open an article.
2. Save the article, then confirm it appears under **Saved**.
3. Open settings and enable offline reading; verify the status message.
4. Open **Play**, start Youtopia Ascent and complete several questions.
5. External source and website links should open in the system browser.

The app does not request health data, diagnose conditions, provide personalised treatment or assign IQ/brain-age scores.

## Screenshot plan

Capture from the final release candidate only, with no mock data presented as a real measurement.

1. Discover — hero and evidence-led positioning.
2. Learn — article library and search.
3. Reader — source links, uncertainty and editorial responsibility visible.
4. Saved — device-local reading list.
5. Ascent — question screen with non-clinical rank language.
6. Explore — wider Youtopia features, clearly identified as external.

Prepare required iPhone/iPad and Android phone/tablet sizes only after confirming the final supported-device list and current store specifications.

## Release-candidate QA gates

### Functional

- [ ] Fresh install and update install both tested.
- [ ] Discover, Learn, Play, Saved and Explore navigation tested.
- [ ] Search, topic filtering, article modal, save/unsave and focus return tested.
- [ ] Ascent complete, incorrect-answer, lifeline, checkpoint and bank paths tested.
- [ ] Offline reading tested after explicit opt-in and again after app restart.
- [ ] External links use the system browser and back navigation returns safely.
- [ ] iOS gesture/back behaviour and Android hardware/software back behaviour tested.
- [ ] No stale files remain after a clean production build.

### Accessibility and presentation

- [ ] VoiceOver and TalkBack labels/order tested.
- [ ] Dynamic/large text tested without clipping.
- [ ] Reduced motion, contrast and visible focus tested.
- [ ] Small phone, large phone and tablet safe areas tested in portrait and landscape.
- [ ] Final Youtopia app icon and splash assets use the canonical licensed artwork.
- [ ] No default Capacitor icons, splash images or test identifiers remain.

### Privacy, safety and compliance

- [ ] Compiled dependency/SDK inventory matches the privacy declarations.
- [ ] No debug logging is enabled in the release build.
- [ ] Privacy, support and external-link disclosures match actual behaviour.
- [ ] All six articles receive final evidence, source, rights and editorial review.
- [ ] No medical, diagnostic, treatment or guaranteed-outcome wording is introduced in metadata or screenshots.
- [ ] App Store Review Guidelines, Play policies and health-content declarations are rechecked immediately before submission.

### Distribution

- [ ] Bundle ID ownership confirmed.
- [ ] Version/build numbers and release signing configured.
- [ ] Apple and Google developer-account ownership and costs approved by Adam before purchase.
- [ ] TestFlight and Play testing requirements confirmed for the account type.
- [ ] Device beta feedback recorded and blocking defects resolved.
- [ ] Final screenshots, descriptions, age/content questionnaires and reviewer notes approved.
- [ ] Submission remains a separate explicit approval step.

## Known release blockers

1. Default native platform icons and splash screens still need replacement with canonical Youtopia artwork.
2. Native iOS and Android binaries have not been compiled, signed or tested on physical devices.
3. Developer-account ownership, bundle-ID availability, membership costs and signing authority are unverified.
4. Final privacy/data-safety answers require compiled-SDK verification.
5. Store screenshots and final metadata require the approved release candidate.
6. App submission has not been authorised or performed.
