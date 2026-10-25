# Asset provenance register

Reviewed 25 October 2026. This is an operational release-control record, not legal advice.

Use this register for every locally hosted film, audio track, generated visual, supplier asset and merchandise print file. An asset is not production-ready merely because it exists in the repository, ChatGPT Library, a review pack or a previous preview.

## Release statuses

- **Approved** — source, owner/licensor, permitted use and evidence location are documented.
- **Editorial only** — permitted for the stated editorial context but not advertising, merchandise or paid promotion.
- **Pending** — evidence or usage scope is incomplete; keep out of production campaigns.
- **Blocked** — misidentified, unlicensed or otherwise unsuitable; do not use.

## Current high-risk groups

| Asset group | Current status | Required evidence | Release rule |
| --- | --- | --- | --- |
| Locally hosted Youtopia films | Mixed — see individual records | Original footage or image source, render/project file, music source and releases where applicable | Only the exact channels recorded below are cleared; every other film remains Pending |
| Locally hosted audio | Pending | Generator/service account or composer, creation date, applicable terms or licence receipt, original export | Do not use in production until rights and permitted commercial scope are recorded |
| Generated campaign artwork | Pending | Generating tool/account, prompt or project record, original export, identity/brand review | Preview only until resemblance, logo, person and commercial-use checks pass |
| Ring AIR and other supplier media | Pending supplier scope | Written supplier permission or programme terms covering website, organic social and paid use separately | Links and original Youtopia editorial explanation may proceed; supplier media cannot be assumed reusable |
| Collection 01 artwork and mock-ups | Pending | Original design source, trade-mark/name clearance, final print file, mock-up licence and physical sample approval | Keep noindex and non-transactional; no sale or public launch |
| Unsplash editorial imagery | Editorial only | Photographer/page URL or image ID retained in source; current Unsplash licence | Do not sell as a standalone asset or imply endorsement |
| Wikimedia Commons portraits | Editorial only | Exact file, author, individual licence, attribution and adaptation/crop disclosure | Recheck before advertising, merchandise or reuse outside the documented page |
| Embedded YouTube material | Editorial only | Original URL and embed-only use | Do not download, edit, rehost or use clips in advertising without permission |

## Per-asset records

| File or URL | Asset type | Source/creator | Created/acquired | Licence or permission | Permitted channels | Restrictions/expiry | Evidence location | Reviewer/date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/social/journal-launch/sleep-reel.mp4` | 21-second silent vertical editorial Reel | Youtopia render from `assets/guide-sleep.jpg`; source photo Ahmed Nishaath, Unsplash ID `photo-1761957883290-c37d9ce7c5d2` | Render committed 17 October 2026 | Unsplash free licence recorded in `CONTENT_RIGHTS.md`; original Youtopia typography/render; no audio | Website preview, organic social and Story cut | Editorial sleep context only; no paid advertising, merchandise, endorsement implication or music addition without a new review | `tools/build_journal_growth.py`; commit `0758bb0`; `CONTENT_RIGHTS.md` | Automated evidence review / 23 October 2026 | Editorial only — still requires final visual/brand approval before scheduling |
| `assets/social/journal-launch/creatine-reel.mp4` | 21-second silent vertical editorial Reel | Youtopia render from `assets/nutrition/training-campaign.webp` | Render committed 17 October 2026 | Render script and silent export verified; original generation/account evidence for source image not recorded | Preview only | Do not schedule, advertise or repurpose until the source image's generation record and commercial-use scope are preserved | `tools/build_journal_growth.py`; commit `0758bb0` | Automated evidence review / 23 October 2026 | Pending |
| `assets/social/journal-launch/clocks-reel.mp4` | 21-second silent vertical editorial Reel | Youtopia render from `assets/research-watch/epigenetic-clocks.webp` | Render committed 17 October 2026 | Render script and silent export verified; original generation/account evidence for source image not recorded | Preview only | Do not schedule, advertise or repurpose until the source image's generation record and commercial-use scope are preserved | `tools/build_journal_growth.py`; commit `0758bb0` | Automated evidence review / 23 October 2026 | Pending |
| `youtopia_cinematic_v3.mp4` | Finished cinematic campaign film stored outside the repository | Remi/Picasso collaboration; production inputs not yet documented in this register | 24 October 2026 | Music, stock/generative footage and tool/project evidence not yet preserved | Private review only | Do not publish, schedule, advertise or repurpose until every visual, voice and music component is cleared | ChatGPT Library asset and source production project to be linked | Automated intake / 25 October 2026 | Pending |
| `Youtopia-Life-Reel-Follow-And-Explore.mp4` | Social campaign Reel stored outside the repository | Youtopia campaign production; detailed source sheet not yet attached | Latest known version 5, reviewed 25 October 2026 | Supplier/product media, music and generated-scene scope not yet recorded per component | Private review only | Affiliate disclosure does not itself clear supplier footage or music | ChatGPT Library asset and campaign source pack to be linked | Automated intake / 25 October 2026 | Pending |
| `Youtopia-Life-Updated-Campaign-Pack.zip` | Campaign source/review archive | Youtopia campaign production | Latest known version 7, reviewed 25 October 2026 | Archive existence is not permission; individual included assets require records | Private production/review | Do not treat the pack as a blanket licence or as proof that included media is scheduled or published | ChatGPT Library archive; component manifest required | Automated intake / 25 October 2026 | Pending |

## Mandatory checks

1. Confirm the exact file or URL, not only a general supplier or platform name.
2. Separate ownership of the visual/footage from music, font, logo, likeness and product-packaging rights.
3. Preserve the original export, project file, permission email or licence receipt.
4. Record channel scope separately: website, organic social, paid advertising and merchandise are not interchangeable.
5. Confirm named people and clubs from authentic supplied media; do not use generated or guessed faces.
6. Recheck time-limited or programme-specific permissions before reuse.
7. Keep pending assets out of scheduled posts, advertisements, store listings and production deploys.
8. Record affiliate disclosure separately from media permission; one does not substitute for the other.

## Release gate

A release using locally hosted or externally stored campaign media passes this gate only when every included asset has an individual **Approved** or appropriate **Editorial only** record and the visible preview has been checked. Missing evidence is treated as pending, not as permission.
