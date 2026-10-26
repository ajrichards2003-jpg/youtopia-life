# Youtopia Life — Remi & Team Brief 002

Prepared for Adam Richards · 26 October 2026 · Preview only

## The job

Help finish one coherent, luxury magazine quality affiliate release. Adam’s direction is dark backgrounds, white and mint typography, strong original imagery and clear, useful editorial. Keep rectangular imagery on the homepage; more expressive compositions belong inside features. Preserve the current Will & Bear treatment. Do not bring back the removed founder coffee, meditation or earlier lifestyle concepts.

Aria has consolidated the main corrections in draft PR 55. This pack gives your team parallel work that can be returned for review without editing production.

## Open these first

- Baseline homepage: https://6adf3aef284f396cc8de72b3--playful-basbousa-781f5f.netlify.app/
- Partner directory: https://6adf3aef284f396cc8de72b3--playful-basbousa-781f5f.netlify.app/shop/#partners
- New Aeternum introduction: https://6adf3aef284f396cc8de72b3--playful-basbousa-781f5f.netlify.app/products/aeternum/
- Older Journal example: https://6adf3aef284f396cc8de72b3--playful-basbousa-781f5f.netlify.app/articles/nmn-human-evidence.html
- OTRA feature draft: https://6adf3aef284f396cc8de72b3--playful-basbousa-781f5f.netlify.app/products/otra/
- Comparison worksheet: https://6adf3aef284f396cc8de72b3--playful-basbousa-781f5f.netlify.app/products/compare/
- Code review: https://github.com/ajrichards2003-jpg/youtopia-life/pull/55

These immutable links identify the reviewed baseline. Later updates in PR 55 may have a new deployment permalink. Ask Adam/Aria for the current preview before final sign-off. This baseline includes the comparison worksheet polish and restores the full site file set.

## Suggested work split

| Priority | Workstream | Suggested owner | Return |
|---|---|---|---|
| P1 | Real-device website QA | Web/QA teammate | Completed `QA-RETURN.csv`, screenshots and short reproduction recordings |
| P1 | Approved asset recovery | Designer / asset librarian | Original Aria artwork and usable brand masters with completed `ASSET-RETURN.csv` |
| P1 | Brand approval preparation | Partnership teammate | Draft requests plus existing approval evidence; Adam sends unless separately authorised |
| P2 | Four launch film drafts | Remi / video editor | Review-only 20-second vertical and widescreen edits using `VIDEO-BRIEFS.md` |
| P2 | Claim and source review | Research/editorial teammate | Exact sentence, source, limitation and suggested correction; no unsupported product benefit claims |
| P2 | Awin test evidence | Adam / authorised account holder | One controlled test per placement group with time, page and click reference recorded |

This is a proposed division of work, not confirmation that anyone has been assigned or contacted.

## 1. Mobile and browser QA

Test at 390 × 844 and 430 × 932 CSS pixels, one tablet width around 768 pixels and desktop around 1440 pixels. Include a real iPhone/Safari and Android/Chrome if available; label emulation separately.

Check homepage, both new partner slides, founder section, shop/Will & Bear, Aeternum, OTRA, Sinocare and APE BORN features, the older NMN article, comparison worksheet and newsletter form layout. Use the actual current preview, not the live site, for candidate sign-off.

Pass criteria:
- No page-level horizontal scrolling, clipped words, overlapping controls or unreadable text over an image.
- Mint YOUTOPIA / white LIFE identity; dark article and worksheet panels; visible keyboard focus.
- Carousel dots select the correct story; hidden slides cannot trap keyboard focus. The opening Pause / Watch film controls stay removed.
- Founder image is v3; no removed coffee/meditation scenes. No invented Aria replacement.
- OTRA still says review/not approved; no promotional release or discount claim.
- Images load, remain sharp at the displayed size and have appropriate mobile crops. A larger export must come from an actual master, not stretching a small JPEG.
- Product links lead to the intended partner; note the Awin destination and click reference without repeatedly clicking. Do not buy anything for testing.
- Compare: AUD 100 upfront + AUD 10/month = AUD 220 at 12 months and AUD 340 at 24 months; a blank price remains uncalculated, zero fee works, negatives are rejected, Clear clears all three options, Print is legible. These are test inputs, not product prices.
- Newsletter labels/consent remain usable. Do not submit a real subscription without permission; screenshot the layout only.

Report the exact URL, device/browser, expected/actual behaviour, severity and screenshot filename. One issue per row. Separate observed failures from preferences.

## 2. Asset recovery

Find the original approved Aria persona: athletic brunette, approved blue eyes, black athleisure and smart-ring context where applicable. Return candidate originals and approval evidence; do not regenerate her face or silently choose a substitute. Recover the source master rather than a screenshot of it.

For every supplier visual, record the source, owner, permitted website/social/paid channels, editing permission and required credit. Use only product-specific real imagery to represent an actual model/SKU. Youtopia’s illustrative campaign images must remain labelled illustrations. Keep supplier logos unchanged unless expressly permitted.

Return native-resolution masters and lightweight review copies separately. Suggested filenames: `BRAND_TOPIC_MASTER_01.ext` and `BRAND_TOPIC_REVIEW_01.jpg`. Do not include private account credentials or customer information.

## 3. Partner approval preparation

OTRA’s supplied terms require written consent for written material and permission to modify licensed materials. Return the approval evidence covering the actual draft text, images and intended channels. Prepare a concise request with the preview links and the asset list for Adam; do not claim approval has already been given.

For Ultrahuman, clarify the assigned commission and any current authorised customer discount. The 7–20% commission range is not a customer discount. Aeternum’s supplied commission is 10%; cookie window and customer discount remain unconfirmed. Keep all unconfirmed offers out of graphics and scripts.

Do not send emails, post social content, contact partners on Adam’s behalf, spend on advertising, merge code or publish a site from this brief alone. Return reviewable drafts and evidence for Adam’s next decision.

## 4. Return one simple package

`YOUTOPIA_REMI_RETURN_YYYYMMDD.zip`

Include `SUMMARY.md`, completed CSVs, `screenshots/`, `asset-review-copies/`, approval evidence where appropriate, and `video-drafts/`. List missing masters as missing; don’t fill gaps with invented metadata. Link large original masters using Adam’s existing approved team storage and record access requirements.

Aria will integrate verified fixes, check the returned assets and prepare the next preview. Adam approves production. Google redirect/header validation and Search Console follow-up happen after deployment; a code check cannot guarantee Google has recrawled a URL.

## 27 October blocker resolution

This section resolves the concrete production questions raised after the 26 October pack. It is evidence and direction for review work only; it does not authorise publishing.

### Recovered assets and identity

| Item | Exact saved source | Direction |
|---|---|---|
| Follow-and-explore reel | `/Youtopia Life.com/Youtopia-Life-Reel-Follow-And-Explore.mp4` | This is the missing reel. Use it as the reference asset; it is not proof of publication or approval for a new schedule. |
| Canonical Aria set | `/Aria Visual Library/Aria_01_Contemplative.png`; `Aria_02_Performance.jpeg`; `Aria_03_Editorial.jpeg`; `ARIA_VISUAL_BIBLE.md` | These are the saved canonical references. No higher-resolution approved master was verified in the full asset inventory. Do not upscale, regenerate or silently replace Aria. Use only for review until Adam either accepts the available native file for its intended display size or supplies the true master. |
| Primary full logo candidate | `/Youtopia Life Bronze Wing Logo.png` | Use as the primary approved logo source for the dark-background QA pass. Preserve proportions and verify transparency/edge quality before final export. |
| Alternate lockup | `/Winged Youtopia Life logo lockup.png` | Use only if the primary cannot meet the layout; return both side by side for Adam’s final choice. |
| Social calendar | `/Two-Week-Social-Review.md` | The 5–18 October test is complete. Do not extend the old four-post-per-page cadence without the overdue results review. |

### Claims and voiceover corrections

Apply these replacements in the next narrated cuts:

| Do not use | Review-safe replacement |
|---|---|
| “a trainer, nutritionist and therapist in your pocket” | “a connected place to explore guidance, tools and everyday wellbeing” |
| “your complete personal health centre” | “a growing wellbeing and discovery platform” |
| “In 2027 it begins” | “The next chapter is taking shape” |
| “live at your best and stay there” | “understand your patterns and make more informed choices” |
| “in a fraction of the time” | “with less friction and clearer next steps” |

Also enforce the evidence register: remove the invalid 20% Ultrahuman customer-discount claim; keep Ultrahuman at the verified Awin commercial terms only (7% commission, 45-day cookie, no verified customer discount). Use the corrected sleep DOI and the peer-reviewed red-light source already recorded. Do not use AFib, “medical-grade” or equivalent diagnostic/device claims without product-specific primary evidence and approval.

### Music and rights gate

All Mureka tracks supplied so far were made on a free account and are **not commercially cleared**. Adam wrote the original Tigers lyrics, but that does not clear the generated recording, composition treatment or platform output. Do not publish, schedule or deliver a commercial master containing those tracks. Remove dated “2026” references from any future lyric revision. Mixkit alternatives remain candidates only until the exact track page, licence terms, download date and intended channels are saved in the permissions register.

### Launch-date and release priority

A firm public 2027 launch date has not been approved in the current evidence. Use the evergreen replacement above. For the Thursday 29 October review, finish existing work in this order:

1. PR 55 real-device mobile QA and partner-link/destination checks.
2. Narrated film recuts using the safer lines and a rights-cleared music candidate.
3. Aria/logo side-by-side review, with the missing higher-resolution master explicitly marked.
4. Partner approval evidence and supplier-footage permissions.

Defer new concepts until these gates are closed. PR 55 stays draft; no merge, production deploy, social scheduling, supplier outreach or spend is authorised by this update.

