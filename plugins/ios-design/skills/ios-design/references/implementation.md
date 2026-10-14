# Implementation and verification notes

Field notes from applying this skill end to end in a SwiftUI reading app (iOS 17 target, built with the iOS 26.3 SDK locally and Xcode 16.4 in CI), October 2026. Each note was observed in that project unless marked otherwise; re-verify on your own targets. The HIG references say what to build; this file covers how it tended to break.

## SDK, CI and availability

- `#available` gates the runtime, not the compiler. An API that only exists in a newer SDK (for example `safeAreaBar`, `Button(role: .close)`, `ToolbarSpacer`) fails to compile wherever an older Xcode builds, such as a CI runner on Xcode 16.4. Wrap such code in `#if compiler(>=6.2)` and `#available(iOS 26.0, *)`, and put the fallback in both the `#else` branch and the `else` of `if #available`. The compiler version stands in for the SDK (Swift 6.2 ships with Xcode 26, 6.1 with Xcode 16.4); it is not an SDK check. Check the CI runner's Xcode before adopting new APIs.
- Icon Composer `.icon` files need Xcode 26 to build. An asset-catalog icon builds from Xcode 16, with dark and tinted variants declared as `"appearances": [{"appearance": "luminosity", "value": "dark"}]` and `"appearances": [{"appearance": "luminosity", "value": "tinted"}]`. Keep the layer sources for a later `.icon`.

## Contrast as code

- Keep theme colors in one token type (page, surface, ink, secondary ink, link, accent, warning, separator), each with an Increase Contrast variant. Native views and any article HTML read the same tokens; inject them into HTML as CSS custom properties.
- Enforce contrast with a unit test, not a one-off audit. WCAG 2.x relative luminance:

  ```swift
  func luminance(_ hex: UInt32) -> Double {
    [hex >> 16 & 0xff, hex >> 8 & 0xff, hex & 0xff].map { channel -> Double in
      let c = Double(channel) / 255
      return c <= 0.03928 ? c / 12.92 : pow((c + 0.055) / 1.055, 2.4)
    }.enumerated().map { [0.2126, 0.7152, 0.0722][$0] * $1 }.reduce(0, +)
  }
  func contrast(_ a: UInt32, _ b: UInt32) -> Double {
    let (x, y) = (luminance(a), luminance(b))
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)
  }
  // Assert contrast(ink, page) >= 4.5 for every ink and variant, on every page and surface.
  ```

- Typical failures found this way: secondary text on a warm sepia page (about 2.5:1), a light-mode link blue `#4685c5` on white (3.87:1), and the system secondary label on white (about 3.4:1) when used for text that must be read.

## Web-view reading

- Scale a pixel size from the reader's setting so it stacks on Dynamic Type and the default stays unchanged: `UIFontMetrics(forTextStyle: .body).scaledValue(for: setting, compatibleWith: UITraitCollection(preferredContentSizeCategory: UIContentSizeCategory(dynamicTypeSize)))`. Read `\.dynamicTypeSize` from the environment so changes re-render.
- Bold Text reaches web content through the system text styles (`font: -apple-system-body`). A page that sets its own font sizes and families doesn't get it; map `\.legibilityWeight == .bold` to a body `font-weight` (600 for New York).
- At accessibility sizes, shrink in-article heading sizes toward the body (for example 1.3, 1.2 and 1.1em); otherwise long words in headings break mid-word.
- `hyphens: auto` does nothing without `<html lang>`. The language comes from the source page, so validate it (a BCP 47 pattern such as `^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8}){0,3}$`) before writing it into markup.
- Put every input that changes the injected presentation (scaled size, theme, contrast, legibility weight, header) into one `Equatable` value, re-present when it changes, and restore the reading position only after the scroll view's content size reflects the new layout.

## Bars that recede while reading

- Let the article ignore the vertical safe area and pad its content by the bar insets measured while the bars are visible, so hiding them never moves the text.
- When the bars are hidden, cover the status bar area with the page color; a full-screen overlay sized from the measured top inset worked where a zero-height view with `ignoresSafeArea` did not.
- Never hide the bars while VoiceOver or Switch Control is running; observe their status-change notifications and add a Magic Tap that shows the bars.
- Delay the tap-to-toggle (about 0.3 s) and cancel it on link activation or a second tap; skip it when the tap stops a fling. Otherwise link taps also toggle the bars.
- With Reduce Motion on, don't hide the bars on scroll at all; a tap still toggles them without animation.
- Observed on iOS 26.3: the interactive edge swipe-back still works with the navigation bar hidden.

## SwiftUI pitfalls

- `swipeActions` with `Button(role: .destructive)` removes the row as soon as it is tapped. If the action opens a confirmation, cancelling leaves the row missing. Use a plain button with `.tint(.red)` and keep the destructive role inside the confirmation.
- A `confirmationDialog(presenting:)` captures the item when it opens. Re-read current state when the user confirms, because a sync may have changed it meanwhile.
- `fullScreenCover(item:)` cannot present while a sheet is up, and the route stays set, so later opens of the same item are ignored. Route opens through a request that dismisses open sheets first, then presents.
- Replacing a `NavigationLink` row with a `Button` (for example to present full screen) drops the disclosure chevron; add it back as a decorative, `accessibilityHidden` image.
- Pure helpers on a `@MainActor` type that tests or other actors call should be `nonisolated`.

## Theme scope: an owner's choice

- Observed (October 2026): with reading themes scoped to the reader as `content-apps.md` describes, the owner found it inconsistent that only the reader followed the theme, and asked for the chosen theme across the whole app, with System as the default. Applying it app-wide meant styling every presentation root (the root view and each sheet), because the app overrode the UIKit interface style per presenting controller and derived its color tokens from each presentation's own `colorScheme`.

## Delete, Archive and Trash

- A safe pattern that owners asked for: Delete moves the item to a Trash screen that is separate from Archive, with an Undo bar and shake to undo and no confirmation (it is reversible). In Trash, Restore is the easy action; Delete Permanently and Empty Trash are confirmed. Purge after a stated period (30 days), and say so in the Trash footer.
- Keep trashed items out of search, Spotlight, widgets, Continue Reading and automatic downloads, but keep any existing download until the purge so restoring is instant. Saving the same link again restores the item; an idempotent retry of an earlier request should not.
- Show the Undo bar only while that item is still trashed; it may be restored elsewhere.
- Server and sync: a purge or a schema mismatch makes the server reject queued edits. Never let one rejected edit stop the library from syncing; drop it only on the server's own "item not found", keep it otherwise, and tell the user when it persists. Deploy the backend before an app build that sends new fields.

## System integration plumbing

- A widget reads a small `Codable` snapshot written to the App Group's `UserDefaults`; it never opens the app's database. Reload the timeline only when the snapshot changes.
- Route deep links, Home Screen quick actions, Spotlight (`onContinueUserActivity(CSSearchableItemActionType)`) and App Intents through one `open(id)` that waits a bounded time for a cold launch to load data.
- A quick action that launches the app arrives in `application(_:configurationForConnecting:options:)` as `options.shortcutItem`; one used while the app runs arrives in `windowScene(_:performActionFor:completionHandler:)`, so set a scene delegate class.
- Spotlight indexing that deletes and then re-indexes needs a generation check, or a sign-out during indexing re-adds the library. Persist the index signature so cold launches don't re-index everything.
- Clear the index, widget snapshot, quick actions and any "last opened" record on sign-out and account deletion. Mark widget titles `privacySensitive()`.
- Privacy manifest: App Group `UserDefaults` needs reason `1C8F.1` in addition to `CA92.1`.

## App icons and naming

- A script that renders the icon can silently produce a blank image (AppKit cannot draw into a 3-channel bitmap, so one shipped solid black). Render with CoreGraphics into an opaque RGB context. In CI, check that every icon variant is 1024×1024 and not blank (more than a couple of distinct colors), and that the default (Any) icon has no alpha. The dark variant may use a transparent background, which the system fills.
- The Home Screen icon style (light, dark, tinted, clear) is a separate setting from the system appearance, and there is no `simctl` command for it. Switch it from the Home Screen's Edit > Customize, in the simulator or on a device.
- Naming: screen candidates with an exact-title App Store search (the public iTunes Search API, `entity=software`) and check existing websites and domains, since a same-space web product can exist without an iOS app. Names are limited to 30 characters (App Review guidelines 2.3.7 and 4.1). Shortlists go stale quickly. A trademark search is the owner's call.

## Simulator verification

- With more than one simulator booted, `booted` can target either; pass the device UDID to every `simctl` command.
- Use a separate preview bundle identifier and a launch-argument synthetic data store. Tapping the app icon launches without launch arguments, and other local builds with the same synthetic data can also answer Spotlight results.
- `xcrun simctl ui <udid> content_size accessibility-extra-extra-extra-large`, `increase_contrast enabled` and `appearance dark` switch states quickly. `defaults write` does not reach a sandboxed app's preferences; change in-app settings through the UI.
- Screenshots can show the previous frame after a tap; take another before concluding. Wrap `simctl io screenshot` in a time limit, since it can hang on an unresponsive simulator.
- There is no `simctl ui` option for Bold Text or shake. Use the simulator's Settings (Accessibility > Display & Text Size > Bold Text), Xcode's Environment Overrides, or Device > Shake (⌃⌘Z), and also cover them in tests (for example `.environment(\.legibilityWeight, .bold)` on a hosted view).
