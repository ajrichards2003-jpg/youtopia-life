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
| EINSTAR | New creative-technology feature page `/products/einstar/`, shop spotlight and directory; 2 tracked links | **Joined 30 Oct 2026** per founder's Awin screenshots; advertiser **105805**, publisher **3106417**; standard **6%** valid-order commission, **90-day** cookie; tiered KOL 8% / 10% requires eligibility and monthly sales | Verify live redirected destination, relevant Australian storefront/shipping, product imagery rights and checkout; do not confuse Awin US performance data with Youtopia results. |
| iHerb | **Paused at founder's explicit request, 1 Nov 2026**. No purchase links or public promotion in reviewed site pages. | Historical acceptance recorded, but campaign excluded from this release. | Do not feature or add any iHerb links until explicitly reactivated. |
| Therabody, Myprotein, Bulletproof, WHOOP, Oura, Eight Sleep | In pipeline/planning, not verified publisher campaigns | No approved tracked-link status verified | Keep as prospects, not live partners. |

## Release gates

- Confirm every program through the relevant publisher dashboard; a merchant-id URL in HTML is not proof of acceptance.
- Verify Awin publisher `3106417`, merchant IDs, query encoding, `rel="sponsored noopener"`, local link paths, disclosures, destination and checkout.
- Keep iHerb paused until separately approved. Keep supplements editorially evidence-led and avoid medicine-like or paediatric promotional claims. Bovine colostrum is still in separate draft PR #57 pending scientific citations and editorial checks.
- Remove stale percentage-discount copy anywhere on the site, including unpublished store pages and old launch documents; only promote an offer visible in the account.
- Confirm rights and commercial permission for partner imagery and third-party videos.
- Test carousel, keyboard navigation, playback closure, responsive views, founder asset and search/analytics before production.
- Production main is **not** updated by this review branch. No investor-facing revenue or conversion results are inferred from code.


## Founder photographs — verified source (1 November 2026)
The homepage founder feature now uses the user's **original photographic reference files** from the separately maintained `Adam Richards / Reference Uploads` folder on Drive. These are not derived from the `AI Founder & Lifestyle` folder. Included full-size original PNGs:
- `assets/founder-adam-original-formal.png` — original supplied formal portrait
- `assets/founder-adam-original-blue-shirt.png` — original supplied casual blue-shirt photo
- `assets/founder-adam-ecoflow-event.png` — original supplied event photo (low resolution)

Each photo is displayed unchanged, and a click opens the matching original file (native browser zoom). The previously displayed illustrative `adam-founder-editorial-v3.webp` collage has been removed from the homepage founder section, but retained in the repository for history/other approved review work. No AI face regeneration, identity retouch or fabricated results are used in this founder feature. Verify user approves public use of all three originals and note that originals were taken at different times.
