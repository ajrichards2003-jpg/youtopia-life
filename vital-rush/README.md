# Youtopia Vital Rush

Original browser arcade prototype. Open `index.html` through an HTTP server or the draft deploy preview. No build step or external assets are required. Desktop arrows/A/D and Space/Up; touch swipes and the visible buttons. Escape pauses. Switching away pauses automatically.

## Implemented
Three lanes; progressively faster runs; at least two unobstructed lanes in every row; jumpable low hurdles and tall walls; three lives; foods/protein-themed collectibles; ten-food Glow Rush with fictional growth and doubled pickup points; one-hit shields; peptide-inspired research tokens that award points without being consumed; repeatable local-date daily routes; gentle pace; sound toggle; less motion; local personal bests and two food-earned suits.

No accounts, analytics, ads, purchases, online leaderboard or external game dependencies. Scores and unlocks are local to the browser and are not synchronised. Clearing browser data removes them. Date changes select a new daily route. This version has no service worker or native wrapper yet. Canvas play has keyboard controls and status announcements but is not fully playable without sight.

## Validation
`node tests/vital-rush-check.cjs` verifies deterministic courses, fair obstacle generation, controls, pause, hurdle/wall distinction, shields, food growth, doubled points and end state. `node tests/ascent-check.cjs` verifies the separately maintained Ascent edition.

## Release development
This is a playable prototype, not an App Store submission or a download-ranking forecast. First validate whether people understand the controls, choose to retry and enjoy the growth mechanic. Test on physical iPhones and Android devices, tune portrait field of view and jump timing, and gather feedback before adding content, native packaging, store assets or monetisation. No download forecast is supported yet.
