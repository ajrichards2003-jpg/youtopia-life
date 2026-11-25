# Youtopia Life — five-workstream delivery review
Date: 17 November 2026 · Prepared for review only · No production deployment

## 1. Analytics — partially connected, verification required
- Netlify production site: `c5dbb66c-397a-4579-b8ca-a92a1e05e438`, primary URL https://youtopialife.com.
- The public site served `/assets/posthog-boot.js` (23 requests), `/assets/analytics.js` (22) and `/assets/analytics-consent.js` (21) in the observed 24-hour Netlify window. **File requests do not prove ingestion.**
- Source shows cookieless PostHog, DNT handling, UTM capture and `affiliate_click`, `form_submit`, `video_play`, `cta_click` event instrumentation.
- Check in the authenticated PostHog project: live `$pageview` and each custom event, source dimensions, and that consent/privacy copy matches actual behavior. No PostHog event counts were accessible in this review.
- Buffer read-only data (18 October to 17 November; refreshed 16 Nov): Youtopia Life 13 posts / 80 impressions / 69 reach / 6 reactions / 1 click; Biohacker Australia 11 posts / 30 impressions / 25 reach / 1 reaction / 0 clicks. These are Buffer posts' metrics, not full page reach.
- Buffer's three channels are connected: Youtopia Life, Biohacker Australia and Cardinia Tigers. Metricool brand ID 7082151 reported no network connected; Youtopia Australia social metrics remain unavailable.
- Next test: one controlled link click with a known UTM and a known Awin `clickref`, then reconcile PostHog and Awin reporting; do not purchase anything.

### Connected-source verification — 17 November 2026 (Australia/Sydney)
- Netlify project state was successfully read: the primary site is `https://youtopialife.com`, the current production deploy reports `ready/current`, and Forms is enabled.
- Netlify form summaries currently report: first-collection-interest 1, merch-interest 0, youtopia-contact 4, wallpaper-signup 0, youtopia-weekly 1 and youtopia-signup 1.
- The summary endpoint showed newer `last_submission_at` timestamps for youtopia-contact and youtopia-weekly, but the actual submission-record read did **not** contain new records at those times. The newest retrieved contact record remains the 27 October 2026 affiliate-partnership enquiry; the only retrieved weekly record remains the 28 September 2026 consented signup.
- Therefore no new contact or newsletter growth is claimed from those summary timestamps. Do not expose submitter email addresses in reports. Recheck the actual records before reporting any future increase.
- The connected Buffer organization `My organization` still contains three connected, unlocked Facebook pages: Youtopia Life, Biohacker Australia and Cardinia Tigers Junior Football Club. Connection status alone is not page-level analytics and does not prove publication.

## 2. Body Explorer — improvement in this branch
- Existing model has nine keyboard-selectable SVG organs, viewBox zoom and a back-to-whole-body control.
- Added organ-specific **related reading** links using existing first-party evidence/guide pages. The page labels these as learning topics, not personal diagnoses.
- Still outstanding: anatomical artwork upgrade, visual validation of organ alignment and scale, real Safari/Android interaction tests. A schematic SVG is not a medically precise 3D model.
- Accessibility check: keyboard select, selected-state, focus visibility, screen-reader announcement and return-to-body operation.

## 3. Website QA — findings
- Production homepage and shop both resolve and contain sections for research, Pulse, products and affiliate disclosure.
- `/body/` returned 503 to a crawler test (may be transient, not proof of failure for browsers). Retest from a browser/device.
- Observed Netlify 404 examples include `/wp-content/plugins/super-forms/uploads/php/index.php`, `/ai.txt`, `/llms.txt`, unrelated `/product_content_*.html` and `/UpFiles/...` paths. They suggest external scanning/crawler requests, not necessarily broken site navigation. Review internal URL errors separately before applying fixes.
- Complete cross-device QA at 390px/430px mobile, tablet and desktop. Verify carousel, Body Explorer, all CTA destinations, newsletter forms and purchase-link rel/disclosures.

## 4. Affiliate links and revenue — verification required
- `scripts/check-affiliates.py` guards Awin publisher 3106417, clickrefs and sponsor attributes; currently its confirmed merchant list only contains Ultrahuman (merchant ID 69428).
- The production affiliate-disclosure page still lists Ultrahuman only. PR #63 proposes a six-partner disclosure, but that list must not be merged until the current Awin approvals and destinations are verified.
- The public shop's primary visible partner directory remains Ultrahuman-led; other product/editorial work in open branches must not be treated as proof of an active affiliate relationship.
- Confirm active merchant IDs, approval conditions and AU storefront destinations directly against Awin; do not infer approval from a website listing.
- In an authorised Awin session collect clicks, tracked sales, confirmed commission and pending commission for a shared date range. No verified sales/commission count available in this pass.

## 5. Content and video workflow
- Retain the evidence-first labels Strong / Promising / Experimental, clear product disclosures, original source links and no unsupported health claims.
- Prepare the Dire Wolf/Pulse film, wearable and product edits for review only; verify footage/image licensing, captions and mobile crops.
- Continue the existing Facebook posting pause. No new social publishing, paid media, partner outreach or deployments without Adam's explicit approval.
- Use Remi's `docs/remi-affiliate-handover/START-HERE.md` return format for device QA, asset masters, approvals and video drafts.

## Open pull-request release map — verified 17 November 2026
| PR | Workstream | Current state | Gate |
|---|---|---|---|
| #68 | Body Explorer reading links + review | Draft, mergeable | Real-device/accessibility QA, anatomical review, Adam approval |
| #67 | Media provenance release gate | Draft, mergeable | Adam approval; documentation only, no media clearance granted |
| #66 | BiVACOR hero + thylacine Pulse | Open, mergeable | Preview QA, editorial approval, coordinate with #64 |
| #64 | Mobile hero fit | Draft, mergeable | Physical iPhone/Android/tablet and accessibility-text QA; Adam approval |
| #63 | Affiliate disclosure | Draft, mergeable | Current Awin partner verification and Adam confirmation |
| #57 | Colostrum evidence guide | Draft, mergeable | Supplier/label/ARTG-affiliate/claims checks and editorial approval |
| #54, #49, #45, #32 | Older product/design/community/game previews | Open but non-mergeable against current main | Rebuild only if still wanted; do not merge stale branches |

## Acceptance criteria for the five checklist tasks
1. Analytics: PostHog live event receipt verified; Netlify, Buffer and Metricool/Australia sources documented; daily/weekly reporting reproducible.
2. Explorer: selecting each organ zooms to its anatomical position, educational links work and approved anatomically reviewed imagery renders on mobile.
3. Site QA: critical links, forms and conversions pass real-device and automated checks; 404 anomalies classified.
4. Affiliates: merchant approval and outbound links reconciled, disclosure/attribution tested, first verified revenue numbers captured (or explicitly zero).
5. Content: licensed, evidence-reviewed previews and one approved content/video workflow with a no-publish safeguard.

## Release control
This document and Body Explorer improvement are on a review branch only. Do not merge or deploy without Adam's approval.
