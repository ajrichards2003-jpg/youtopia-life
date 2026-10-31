# Partner and affiliate integration audit — 1 November 2026

Scope: inspected source in `preview/nov2026-hero-founders-partners`, which inherits the consolidated release review from 26 October. This is a code audit, **not** an Awin dashboard, contractual approval or successful live purchase test.

| Partner | Source-code coverage | Merchant ID / commercial status | Follow-up |
|---|---|---|---|
| Ultrahuman Ring AIR | Homepage highlight, product page and tracked publisher links | Awin merchant 69428, publisher 3106417. Dashboard commission previously checked at 7%; **do not advertise a 20% customer discount**. | Recheck every homepage deep link, current offer/cookie and mobile checkout. |
| Sinocare | Homepage highlight, product page, Journal article and tracked Awin links | Merchant 114180, publisher 3106417; approval reported by founder. | Product images, labelling, AU fulfilment and click attribution QA. |
| APE BORN Fitness | Homepage highlight, product page, Journal article and tracked Awin links | Merchant 59683, publisher 3106417; approval reported by founder. | Link destinations, product-evidence context, AU fulfilment and mobile QA. |
| Aeternum | Product page, article cross-link and shop directory; tracked Awin links | Merchant 82371, publisher 3106417; approval reported by founder. | Confirm offer/cookie and brand claims. |
| OTRA Eyewear | Product page and editorial page, Awin links; deliberately **noindex** | Merchant 96299, publisher 3106417; approval reported by founder. | Brand copy and creative sign-off before making public/indexable. |
| Will & Bear | Shop feature with tracked Awin links in source | Merchant 119813, publisher 3106417; **approval and permission not independently verified**. | Confirm current account approval, creative/terms and link status. |
| iHerb | **Not integrated with a verified tracked purchase link** in reviewed pages | Founder reported acceptance on 3 Oct 2026. | Obtain the account-issued affiliate destination, verify eligibility/permissions, curate compliant AU products before adding. |
| Therabody, Myprotein, Bulletproof, WHOOP, Oura, Eight Sleep | In pipeline/planning, not verified publisher campaigns | No approved tracked-link status verified | Keep as prospects, not live partners. |

## Release gates

- Confirm every program through the relevant publisher dashboard; a merchant-id URL in HTML is not proof of acceptance.
- Verify Awin publisher `3106417`, merchant IDs, query encoding, `rel="sponsored noopener"`, local link paths, disclosures, destination and checkout.
- Keep supplements editorially evidence-led and avoid medicine-like or paediatric promotional claims. Bovine colostrum is still in separate draft PR #57 pending scientific citations and editorial checks.
- Remove stale percentage-discount copy anywhere on the site, including unpublished store pages and old launch documents; only promote an offer visible in the account.
- Confirm rights and commercial permission for partner imagery and third-party videos.
- Test carousel, keyboard navigation, playback closure, responsive views, founder asset and search/analytics before production.
- Production main is **not** updated by this review branch. No investor-facing revenue or conversion results are inferred from code.
