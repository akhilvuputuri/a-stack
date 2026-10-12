# Reading, library, and offline-first patterns

For apps whose value is the content: readers, read-later libraries, news, documentation, podcasts, notes. Adapt rather than copy; the user's product decisions win.

## Library and list screens

- **The title is the row.** Give it the strongest text style and the most space. Use a text style that scales, such as `.font(.title3.weight(.semibold))`, `.font(.system(.title3, design: .serif))` when the app already uses serif, or `Font.custom(name, size:, relativeTo:)`; never a fixed `size:` alone.
- **Metadata is quiet and short.** One secondary line: source, author, reading time or time remaining. Strip `www.`; prefer a site name over an uppercased hostname when available. Use uppercase tracking only for very short labels.
- **One status channel per row.** Pick the single fact that changes what the user will do (unread, partly read, unavailable offline, failed). Show the normal state as nothing. A small symbol or a thin progress line is enough; avoid stacking checkmarks, colored dots, and labels.
- **Disclosure chevrons are optional** in plain content lists where the whole row obviously opens content. Removing them returns width to titles. Keep them in settings-style lists.
- **Avoid truncating titles** when possible: allow three or four lines, and let row height grow at large text sizes.
- **Exceptions live where they will be seen without taking over.** A failed import is a per-item fact or a compact entry point (toolbar badge, section at the end, or a row in a secondary screen). Avoid permanent strips at the top of the main list for non-urgent states.
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
- Present Undo in a bottom bar region that coexists with bottom search and toolbars (`.safeAreaBar(edge: .bottom)` on iOS 26). Let it auto-dismiss and remain reachable to VoiceOver.

## Reader screen

- **Immersion.** Let bars recede while reading: hide the navigation bar and bottom toolbar on downward scroll or on tap, and bring them back on upward scroll or tap. Respect Reduce Motion with fades instead of slides.
- **Primary actions near the thumb.** Typography, finish/archive, and share belong in a bottom toolbar or at the end of the article, not only in an overflow menu. Put a clear "Done" or "Archive" affordance at the end of the text where reading ends.
- **Typography controls** open from an `Aa` button as a popover or small sheet with live preview: size, theme, font (one serif, one sans), and optionally line spacing and width. Changes apply immediately without losing position.
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
- Color: inject theme tokens as CSS custom properties from the same source as native colors so native chrome and HTML match exactly.

## Themes and color

- Define colors once, as tokens: asset-catalog colors with Any, Dark, and High Contrast variants, or a small `ShapeStyle`/environment theme type. Avoid comparing a stored theme string in every view.
- A paper/sepia theme is a set of tokens (page, elevated surface, primary ink, secondary ink, accent, separator), each verified for contrast: at least 4.5:1 for body text and secondary text that must be read, at least 3:1 for large text (18 pt and up, or 14 pt and up if bold) and essential icons. Secondary text on warm paper often fails; check it.
- A themed `List` or `Form` paints its own background; use `.scrollContentBackground(.hidden)` with the theme's page color, and `.listRowBackground` for the surface token.
- Keep surfaces on one page color when possible. Two nearly identical background tones side by side (header strip versus list) look like a seam.
- Status colors: use system green, orange, and red sparingly; on a warm theme, consider desaturated variants that still pass contrast. Do not rely on color alone; pair with a symbol or text for VoiceOver and color-blind users.
- Bars stay system glass; the page color shows through them.

## Offline and sync communication

- Local content opens instantly with no network chrome. Sync and downloads run in the background and report ambiently (a small toolbar indicator, pull-to-refresh, or a status line in settings).
- Distinguish per-item truths precisely: saved on server, downloading, readable offline, readable with missing images, failed. Show only the ones that need attention in the main list; show all of them in detail or diagnostics.
- Failures carry a recovery action (Retry) and a short reason. Retry never discards an existing readable copy.
- Storage is visible and controllable: total used, per-item size where useful, remove download.
- Background refresh timing is chosen by iOS; copy should say "may refresh" rather than promising a schedule.

## Onboarding and sign-in

- One sentence of value, then the form. Use `textContentType` for autofill and passkeys or Sign in with Apple when the backend supports them.
- Developer-only fields (custom server URL) belong behind an "Advanced" disclosure when ordinary users will see the screen.
