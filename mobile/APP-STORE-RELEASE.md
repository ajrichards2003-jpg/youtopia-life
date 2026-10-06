# Youtopia Life app release checklist

Initial preview: six complete source-linked evidence articles, searchable topics, local saved reading, Ascent, and links to the wider Youtopia world. No analytics, account, health measurement or medical assessment. Offline caching is opt-in. Saved reading stays on this device.

## Build status
Web build passed. Capacitor iOS (Swift Package Manager) and Android projects generated successfully. Native binaries have not been compiled, signed or tested on devices. Default platform icons and splash screens must be replaced before release.

## Reproduce
From mobile: npm ci; npm run sync. Open ios/App/App.xcodeproj in Xcode or android in Android Studio. Build tools, supported OS versions and signing must be verified against current Capacitor requirements.

## Before store submission
- Confirm ownership of bundle ID com.youtopialife.app and developer account organisation details. Apple and Google developer memberships may require payment.
- Replace default icons/splash assets with licensed Youtopia branding; check all image/content rights.
- Test real iPhone and Android devices: navigation, back button, safe areas, accessibility, article modals, saving, source links, game completion and airplane-mode reading. Check small screens, large text and performance.
- Keep meaningful app functionality beyond website links; Apple minimum-functionality review is not guaranteed by using Capacitor.
- Finalise privacy policy and support URLs, App Privacy/Data Safety declarations and any applicable Google health-app declaration. Declare actual SDK/network behaviour accurately. Reassess before adding analytics, AI, accounts or health data.
- Prepare age rating, screenshots, description and review notes explaining educational purpose, evidence caveats and the non-clinical Ascent ranks.
- Confirm current Play testing requirements for the account type; newer personal accounts can require a closed test before production access.
- Complete TestFlight/Play testing, signing, release configuration and store review. No app-store submission or approval has happened.

Official references: https://developer.apple.com/app-store/review/guidelines/ ; https://capacitorjs.com/docs/ios ; https://capacitorjs.com/docs/android ; https://support.google.com/googleplay/android-developer/
