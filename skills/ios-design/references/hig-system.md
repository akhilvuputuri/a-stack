# App icon, branding, and system integration

Distilled from the HIG pages on [App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons), [Branding](https://developer.apple.com/design/human-interface-guidelines/branding), [Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets), [Home Screen quick actions](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions), [App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts), [Siri](https://developer.apple.com/design/human-interface-guidelines/siri), [Searching](https://developer.apple.com/design/human-interface-guidelines/searching), [Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views), and [Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications) (read 13 October 2026). Paraphrased.

## App icon

- **Layers.** Build a background layer plus one or more foreground layers, and compose them in Icon Composer. The system adds the Liquid Glass highlights, refraction, shadows, and masking, so supply square, unmasked layers.
- **Artwork.**
  - Give foreground shapes crisp edges, with no feathering.
  - Vary opacity across layers to create depth.
  - Use a solid-color or gradient background.
  - Prefer vector layers (SVG or PDF); outline any text.
- **Design.**
  - Build the icon around one concept in a few filled, overlapping shapes, centered within Apple's grid, without filling the canvas.
  - Prefer illustration to photographs.
  - Avoid thin lines and sharp corners.
  - Don't reproduce UI or screenshots, Apple hardware, or SF Symbols (or look-alikes); SF Symbols may not be used in icons or logos.
  - Leave text out unless it is essential, and never add words like "Read" or "New".
- **Effects.** Don't bake in highlights, shadows, bevels, blur, or glow.
- **Appearances.**
  - Default, dark, clear, and tinted versions keep the same core features. Base the dark version on the light one; colored backgrounds give the best contrast in dark.
  - Alternate icons need their own dark, clear, and tinted versions.
  - Color spaces: sRGB, Gray Gamma 2.2, Display P3.
- **Check.** Verify the icon at small sizes (Settings, Spotlight, notifications) and in every appearance, switched with Home Screen Edit > Customize in the simulator or on a device. Generated icons can come out blank; check the files in CI and look at the real Home Screen ([Implementation notes](implementation.md#app-icons-and-naming)).

## Branding

- Express the brand through voice, a restrained accent color (primary actions, status, the selected tab), and optionally a legible custom font for headlines with system fonts for body text. Consider carrying brand color in the content layer, beneath the glass.
- Use familiar components, and let branding defer to content.
- Don't repeat the logo through the app, don't turn the launch screen into branding (onboarding may carry it), and keep Apple trademarks out of the name and images.
- Names: screen candidates against the App Store and the web before choosing; see [Implementation notes](implementation.md#app-icons-and-naming).

## Widgets

- **Purpose.** Offer one idea tied to the app's main purpose, with content that changes during the day and deep links into the right item. Don't replicate the app icon.
- **Sizes and branding.** Offer only the sizes that add value. Branding stays subtle; a small logo goes top-right, and only when content comes from several sources.
- **Freshness.** Show "last updated" when people may check more often than the widget can refresh. Don't hide stale data behind placeholders.
- **Interaction.** Buttons and toggles handle simple related actions; avoid layouts that look like the app.
- **Specifications.**
  - Margins are 16 pt (11 pt for tight groups).
  - Use `ContainerRelativeShape` for corners.
  - Use system text styles at 11 pt or larger, and never rasterize text. Dynamic Type applies from Large to AX5.
- **Rendering modes.** Support full color (light and dark), accented (`widgetAccentable` groups), and vibrant (Lock Screen; use opaque grayscale).
- **Gallery.** Use a realistic preview, placeholder shapes while loading, and a description that starts with a verb ("Pick up where you left off").

## Quick actions, App Shortcuts, Siri, Spotlight

- **Home Screen quick actions:**
  - Offer up to four, with at least one useful one, using SF Symbols (no emoji) and short titles that name the result.
  - Add an optional subtitle with live context (such as an unread count), and update actions only in predictable ways.
- **App Shortcuts:**
  - Use App Intents, up to ten, available at install, for the most common tasks.
  - Allow at most one optional parameter, and ask a follow-up question when information is missing.
  - Phrases are brief and include the app name.
  - Surface them with `SiriTipView`, and make responses complete in audio alone.
  - For common domains, consider app schemas for Apple Intelligence.
- **Siri:** use familiar terms for content, keep responses concise and device-independent, leave out the app name, and never advertise.
- **Spotlight:** index content with descriptive metadata so it can be found without opening the app. Favor personally relevant items (recent, favorites).

## Share sheet and extensions

- Don't duplicate system activities. Custom actions take a short verb title without the product name and an SF Symbol, and irrelevant activities are excluded.
- A share extension should finish in as few steps as possible (one tap is ideal), with no extra modals.
- Long work continues in the background, and the main app shows its status.
- Notify only about problems, not routine completion.

## Notifications and badges

- **Urgency.** Use interruption levels honestly: passive (read at leisure), active (default), time sensitive (now or within an hour), and critical (requires an entitlement).
- **Badges.** Badges count unread notifications only. They are never the sole signal and always stay current.
- **Marketing.** Marketing notifications need explicit opt-in and in-app controls, and are never time sensitive.
- **Foreground.** When the app is in the foreground, insert new content quietly instead of notifying.
