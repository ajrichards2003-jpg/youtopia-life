# Youtopia Life — release candidate checklist

6 October 2026. Version 1.0.0 / build 1. Six complete source-linked articles, search/filter, saved reading, 30-question Ascent with practice and resume, memory matching, Calm & Connect, local privacy and offline assets. Wider website features require internet. No account, analytics or health measurements in this edition.

Web packaging and Capacitor sync pass. iOS and Android projects contain branded icons and splashes. Native compilation and physical-device QA are separate checks; never infer a passing compiler result from project generation.

Reproduce: from mobile, npm ci then npm run sync. Open ios/App/App.xcodeproj or android in the platform tools. GitHub mobile-apps workflow prepares Android debug and iOS simulator builds; neither is a signed distribution release.

Remaining: developer-account/app-ID ownership, native compiler checks, real-device and accessibility QA, final SDK/privacy declarations, public app-specific privacy policy and monitored support, signed store binaries, required beta testing, actual device screenshots, final metadata approval and store review. No purchase or submission has occurred.
