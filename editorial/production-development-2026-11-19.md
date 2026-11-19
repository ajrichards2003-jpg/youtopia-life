# Youtopia Life — Production development package (19 November 2026)

**STATUS: Editorial drafts only. Not approved for publishing. No social posts or paid activity authorised.**

## 1. The Science Within — Creatine (55–65 second premium science film)

**Editorial promise:** Separate established muscle-performance evidence from early and mixed cognitive evidence.

**Visual language:** Deep charcoal, mint molecular lighting, white typographic cards, macro 3D creatine/phosphocreatine forms, realistic muscle fibres (not medical diagrams masquerading as scans). 4:5 and 9:16 safe zones. No product or affiliate placement.

| Time | Picture | Voiceover / on-screen treatment |
|---|---|---|
| 00–05 | Smash cut: tennis grip, mitochondrion-like ATP graphic, brain silhouette. Large type: “AFTER 40?” | “What if one of sport's best-studied supplements has a second story?” |
| 05–13 | Stylised creatine/phosphocreatine molecular pathway (verify chemistry in final art) | “Creatine helps replenish energy for short, intense muscular effort.” |
| 13–23 | Macro muscle-fibre and resistance training cuts | “For high-intensity exercise and training adaptation, the evidence is strong.” [STRONG] |
| 23–34 | Transition through bloodstream to neurone illustration, visibly labelled conceptual animation | “The brain also uses energy. That has scientists asking whether creatine might help aspects of thinking.” |
| 34–45 | Abstract journal tiles, study populations and comparison bars | “Some trials and reviews suggest benefits in memory or attention. Results aren't consistent.” [EMERGING / MIXED] |
| 45–53 | Clear journal citation overlay; muted lighting | “A major European evidence assessment did not establish a general cognitive benefit.” |
| 53–61 | Brand lockup + article CTA | “The muscle story is established. The brain story is still being tested. Stay curious. Follow the evidence.” |

### Non-negotiable evidence bar
- Australian Institute of Sport: Creatine Group A performance supplement: https://www.ausport.gov.au/ais/nutrition/supplements/group_a/performance-supplements2/creatine
- 2024 adult cognition systematic review/meta-analysis: https://pubmed.ncbi.nlm.nih.gov/39070254/
- 2024 EFSA cognitive health-claim review: https://doi.org/10.2903/j.efsa.2024.9100
- October 2026 sleep-restriction pilot, null result and underpowered: https://link.springer.com/article/10.1007/s41782-026-00380-8
- 2026 sleep-deprivation systematic review: https://pubmed.ncbi.nlm.nih.gov/42261581/

**Editorial risk checks:** No implication that creatine prevents dementia or boosts IQ. No misleading “medical imaging” label for CGI. Don't turn the 40+ hook into an age-exclusive efficacy claim. Verify each original paper and citation before final render. Do not equate supplements with medical treatment.

## 2. Inside the Body — “The Night Shift” (75–90 second pilot)

**Voice and look:** Original friendly anthropomorphic organs; distinct heart (steady, optimistic), brain (overthinking but kind), muscle (warm, surprisingly thoughtful); bright sophisticated colours against soft teal studio, not a copy of another show's character designs.

| Beat | Action and dialogue |
|---|---|
| Cold open 0–10s | Brain peers at a dashboard with 200 flashing reminders. “We're meant to be RESTING. Why is everything still running?” |
| 10–26s | Heart, doing a patient little dance: “Because some of us have a night shift.” Brain: “You could have warned me.” Heart: “I've been doing it since before you could complain.” |
| 26–43s | Muscle wanders in carrying a cushion. “Excuse me, I need recovery time. Also, has anyone seen my protein?” Brain: “That isn't how protein delivery works.” |
| 43–59s | Heart indicates a glowing circulation route. “We all share the same delivery network.” Muscle: “Teamwork. I love that. Do we get jackets?” |
| 59–74s | Brain looks at night-mode panel. “Sleep helps me organise memories, too. Just don't make a contest of it.” |
| Closing 74–84s | The trio dim the lights. Heart whispers, “Still on duty.” Muscle whispers, “Still fabulous.” End card: “The body never works alone. Explore it.” |

**Science and child-safety pass:** Rest does not mean heart stops; sleep supports consolidation of some forms of memory; recovery and nutrition are more complex than a single nutrient. Keep humour G-rated, no diagnoses, and check claims with suitable sources before production.

## 3. Website and analytics QA gates

- Homepage: desktop widths 1280, 1440, 1920; verify hero text clears navigation and images, discovery pills wrap without clipping
- Mobile: 360 and 412px; menu, hero text, tap targets, accessible navigation, no horizontal overflow
- Body Explorer: whole-body overview, brain/thyroid/heart/kidneys focus, selected organ visible without shell overlay, reset restores original view, keyboard Enter/Space, info panel and responsive focus
- Analytics: Netlify edge counts are **requests**, not unique people; automated probe scans should not be counted as true visits
- PostHog: verify real project events from a test pageview before claiming unique visitors; client-side token is not a data-read credential
- Phone Pulse dashboard: authenticated read-only server-side data access required for automated refresh; never place private analytics read tokens in client-side code
- Review previews and obtain signoff before merging Body Explorer or publishing media

## 4. What remains outside this draft
Production video rendering, quality assurance on a real Android device, actual PostHog dashboard read permission, social platform follower-level analytics and final creative signoff are not validated by this document.
