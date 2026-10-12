# Reading, library, and offline-first patterns

For apps whose value is the content: readers, read-later libraries, news, documentation, podcasts, notes. Adapt rather than copy; the user's product decisions win.

## Library and list screens

- **The title is the row.** Give it the strongest text style and the most space. Use a text style that scales, such as `.font(.title3.weight(.semibold))`, `.font(.system(.title3, design: .serif))` when the app already uses serif, or `Font.custom(name, size:, relativeTo:)`; never a fixed `size:` alone.
- **Metadata is quiet and short.** One secondary line: source, author, reading time or time remaining. Strip `www.`; prefer a site name over an uppercased hostname when available. Use uppercase tracking only for very short labels.
- **One status channel per row.** Pick the single fact that changes what the user will do (unread, partly read, unavailable offline, failed). Show the normal state as nothing. A small symbol or a thin progress line is enough; avoid stacking checkmarks, colored dots, and labels.
- **Keep the standard disclosure indicator** on rows that drill into detail; the HIG's [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables) page prescribes it for navigation. Reduce noise elsewhere (status marks, metadata) rather than removing the system indicator.
- **Avoid truncating titles** when possible: allow three or four lines, and let row height grow at large text sizes.
- **Exceptions live where they will be seen without taking over.** A failed import is a per-item fact or a compact entry point (a toolbar item, a section at the end, or a row in a secondary screen). Avoid permanent strips at the top of the main list for non-urgent states. Mail's toolbar status (last update, unread count) is the HIG's model for ambient status.
- **Counts earn their place** only when they change behavior (for example, an unread badge). "9 items" rarely does.
- **Search** sits at the bottom on iPhone. Scope it with `.searchScopes` for library versus archive rather than separate modes, when that matches the model.
- **Collections and filters**: a toolbar menu or `.searchScopes`, not a persistent filter row, unless filtering is the main task.
- **Empty states** use `ContentUnavailableView` with one action that resolves them.

## Triage gestures and menus

- Give the most frequent safe action (archive, mark read) the full swipe. One common layout puts it on the leading edge and keeps destructive actions on the trailing edge without full swipe; Mail instead puts Archive on the trailing full swipe. Choose one and keep it consistent, but never let a full swipe destroy data without Undo or confirmation.
- Destructive actions should be reversible (Undo) or confirmed. Prefer Undo when the operation can actually be reversed; a full-swipe delete with neither is a P0.
- Give every row a `.contextMenu` with the same top actions as its swipe actions, and a preview where helpful.
- Confirm in VoiceOver that swipe actions appear in the Actions rotor. Add `.accessibilityAction(named:)` only for actions that are missing, to avoid duplicates.
- Add `.sensoryFeedback(.success, trigger:)` or similar at commitment, not on every state change.
- Present Undo in a bottom bar region that coexists with bottom search and toolbars (`.safeAreaBar(edge: .bottom)` on iOS 26). Don't make it vanish on a timer; the HIG asks to minimize time-boxed UI. Keep it until the next action or an explicit dismissal, and name the action ("Undo Archive"). Register the change with `UndoManager` so shake-to-undo also works, and show the restored item.

## Reader screen

- **Immersion.** Let bars recede while reading: hide the navigation bar and bottom toolbar on downward scroll or on tap, and bring them back on upward scroll or tap. Respect Reduce Motion with fades instead of slides. Keep text scrolling beneath the status bar obscured by a scroll edge effect, and let a tap restore anything hidden. The HIG allows hiding the status bar temporarily for full-screen media; for reading, keeping it visible is a reasonable stricter default.
- **Paging (optional).** Some readers prefer page-by-page scrolling that overlaps by one line; offer it as a choice, not a replacement for continuous scrolling. System `.paging` has no overlap; use a custom `ScrollTargetBehavior`, or for a `WKWebView` article, scroll programmatically by the viewport height minus one line.
- **Primary actions near the thumb.** Typography, finish/archive, and share belong in a bottom toolbar or at the end of the article, not only in an overflow menu. Put a clear "Done" or "Archive" affordance at the end of the text where reading ends.
- **Typography controls** open from an `Aa` button, kept on the reading screen because the HIG puts task-specific options where they apply. On iPhone use a sheet at the medium detent with a grabber (popovers are discouraged in compact width); in regular width a popover is fine. Offer size, reading theme, font (one serif, one sans), and optionally line spacing and width. Changes apply live without losing position.
- **Progress.** A thin progress indicator, time remaining, and an exact restore of reading position. Never reset position after theme or size changes.
- **Transitions.** `.navigationTransition(.zoom(sourceID:in:))` with `.matchedTransitionSource(id:in:)` from the tapped row ties the list to the article.

## Web-view typography

When articles render in `WKWebView`:

- Measure: `max-width: 34em` to 38em for body text, with comfortable side padding from the safe area (`env(safe-area-inset-*)` plus a margin; these insets are 0 unless the document's viewport meta includes `viewport-fit=cover`).
- Leading: `line-height` 1.5–1.65 for body; tighter (1.15–1.25) for headings.
- System fonts: `font-family: ui-serif` for Apple's serif (New York), `-apple-system, system-ui` for SF. These match native text better than Georgia or Helvetica.
- Dynamic Type: `font: -apple-system-body` scales with the user's text size. It is a shorthand that resets `font-family` and `line-height`, so declare it first and override family and leading after it. If the app also offers its own size control, apply it as a multiplier on top of the system size rather than ignoring the accessibility setting.
- Refinement: `hyphens: auto` (plus `-webkit-hyphens: auto` for older WebKit) with a correct `lang` attribute, `text-wrap: pretty` for paragraphs where supported, `hanging-punctuation: first`, and `font-variant-numeric: oldstyle-nums proportional-nums` in serif body text.
- Images: `max-width: 100%; height: auto;` with a light rounded radius; captions in a smaller secondary style.
- Color: inject theme tokens as CSS custom properties from the same source as the native reading surface (page, ink, link), so native views drawn on the page and the HTML match exactly. System bars are glass over that page, not separately colored.
- Direction: set `lang` and `dir="auto"` on article content so right-to-left articles align by their own language.
- Accessibility: keep real heading elements so the VoiceOver rotor can jump between sections; give images alt text from the source where available.

## Themes and color

- Reading themes (paper, sepia, night) style the reading surface. Outside the reader, chrome follows the system light/dark setting; the HIG discourages app-specific appearance settings. Inside the reader, the chosen theme sets the screen's interface style by its luminance (paper and sepia light, night dark), so bars, sheets, and HTML agree. With "Match System" (the default), the theme follows the system.
- Scope that style to the reader:
  - **SwiftUI:** apply `.environment(\.colorScheme, themeScheme)` to the reader's view and `.toolbarColorScheme(themeScheme, for: .navigationBar, .bottomBar)` for its bars.
  - **Sheets opened from the reader:** apply `.preferredColorScheme(themeScheme)` inside the sheet's content, where it affects only that sheet.
  - **UIKit:** set `overrideUserInterfaceStyle` on the reader's own view controller.
  - **Pitfall:** don't put `.preferredColorScheme` on a view pushed inside a `NavigationStack`, and don't set `overrideUserInterfaceStyle` on the window or root controller. Both restyle the whole window, library included, and can persist after going back.
- Define colors once, as tokens: asset-catalog colors with Any, Dark, and High Contrast variants, or a small `ShapeStyle`/environment theme type. Avoid comparing a stored theme string in every view.
- A paper/sepia theme is a set of tokens (page, elevated surface, primary ink, secondary ink, accent, separator), each verified for contrast: at least 4.5:1 for body text and secondary text that must be read, at least 3:1 for large text (18 pt and up, or 14 pt and up if bold) and essential icons. Secondary text on warm paper often fails; check it.
- A themed `List` or `Form` paints its own background; use `.scrollContentBackground(.hidden)` with the theme's page color, and `.listRowBackground` for the surface token.
- Keep surfaces on one page color when possible. Two nearly identical background tones side by side (header strip versus list) look like a seam.
- Status colors: use system green, orange, and red sparingly; on a warm theme, consider desaturated variants that still pass contrast. Do not rely on color alone; pair with a symbol or text for VoiceOver and color-blind users.
- Bars stay system glass; the page color shows through them.

## Offline and sync communication

- Local content opens instantly with no network chrome. Never show an alert at launch for being offline; show cached content with a quiet label. Sync and downloads run in the background and report ambiently (a toolbar status in the style of Mail, pull-to-refresh whose title shows the last update time, or a status line in settings).
- Distinguish per-item truths precisely: saved on server, downloading, readable offline, readable with missing images, failed. Show only the ones that need attention in the main list; show all of them in detail or diagnostics.
- Failures carry a recovery action (Retry) and a short reason. Retry never discards an existing readable copy.
- Storage is visible and controllable: total used, per-item size where useful, remove download.
- Background refresh timing is chosen by iOS; copy should say "may refresh" rather than promising a schedule.

## Agent- and AI-made content

- Label content an assistant or model produced, wherever it appears (row, header, share). Keep sources visible, note that it may contain errors, and never present it as written by a person.
- Offer Retry or Delete next to it, and don't let generated content take destructive actions without confirmation.

## System integration

- Index saved items in Spotlight (title, source, author) so they open from system search.
- A Home Screen quick action ("Continue Reading", with the title as subtitle) and a widget ("Up next", with a deep link to the item) fit reading apps; show last-updated time when the widget may be stale.
- App Shortcuts: "Save link to <App>", "Continue reading in <App>".
- The share extension should save in a single tap and report progress in the main app, not through notifications.

## Onboarding and sign-in

- One sentence of value (why an account is needed), then the form. Delay sign-in if any part of the app can work without it. Use `textContentType` for autofill and passkeys or Sign in with Apple when the backend supports them.
- Developer-only fields (custom server URL) belong behind an "Advanced" disclosure when ordinary users will see the screen.
