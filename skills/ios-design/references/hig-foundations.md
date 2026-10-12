# HIG foundations for iOS

Distilled from Apple's [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines) (read in full on 13 October 2026). Paraphrased; follow the linked page when a decision depends on exact wording. Numbers are Apple's unless marked otherwise.

## Apple's design principles

[Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) names eight principles. Use them as review questions:

| Principle | Ask |
| --- | --- |
| Purpose | Is the app's most important job obviously the best part of the experience? |
| Agency | Can people get straight to the content, skip guided flows, and recover from mistakes? |
| Responsibility | Is it clear what the app does with data and why each permission is needed? |
| Familiarity | Does it reuse patterns people know, consistently, with clear feedback? |
| Flexibility | Does it work across text sizes, inputs (touch, voice, keyboard), and configurations without losing place? |
| Simplicity | Does every element earn its place? Apple notes that simplicity is not the same as minimalism. |
| Craft | Are the error, empty, and settings screens as considered as the hero screen? |
| Delight | Does the feeling match the purpose (calm for reading), without decoration getting in the way? |

[Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios): limit onscreen controls and keep secondary actions one step away; adapt to orientation, Dark Mode, and Dynamic Type; put frequent controls in the middle or bottom of the screen, within thumb reach; support swipe-back and swipe actions on rows.

## Accessibility

[Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover):

- Text should enlarge to at least 200 percent. iOS text, system or custom font, defaults to 17 pt with an 11 pt minimum; go larger for thin weights.
- Contrast: Apple's table (used by Accessibility Inspector) asks 4.5:1 up to 17 pt, 3:1 at 18 pt and above, and 3:1 for bold text at any size. This skill is stricter than Apple in two ways. It applies WCAG AA's bold rule (3:1 only from 14 pt bold), and it requires the thresholds at default settings in every theme. Apple accepts an Increase Contrast variant as a fallback; here that variant is an extra check. Check light and dark.
- Controls: 44×44 pt default, 28×28 pt absolute minimum. Leave about 12 pt around bezeled controls and about 24 pt around borderless ones.
- Never rely on color alone. Offer an onscreen alternative to every gesture (a swipe-to-dismiss also gets a button).
- Avoid UI that disappears on a timer; prefer explicit dismissal so slower readers and assistive-technology users are not rushed.
- Reduce Motion: cut automatic and repeating animation, tighten springs, track gestures directly, avoid animating depth and blur, and replace sliding transitions with fades.
- VoiceOver: descriptive labels on every key element; describe meaningful images and hide decorative ones; give each screen a unique title and real headings; group related elements (image with caption); announce layout changes; support the rotor for headings and links.
- Also support Voice Control (visible labels match accessibility labels), Full Keyboard Access, Switch Control, and Bold Text. Assistive Access apps reduce to core tasks, one interaction per screen.

## Color and Dark Mode

[Color](https://developer.apple.com/design/human-interface-guidelines/color), [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode):

- One meaning per color. If the accent marks interactivity, don't also use it for static text.
- Every custom color needs light, dark, and increased-contrast variants (asset catalog color sets). Provide light and dark even for single-appearance apps, because Liquid Glass adapts to them.
- Use semantic colors for their stated purpose: `systemBackground`/`secondarySystemBackground`/`tertiarySystemBackground` for plain layouts, the `systemGroupedBackground` set for grouped lists, and `label` through `quaternaryLabel`, `placeholderText`, `separator`, and `link` for foreground. Don't hard-code their values; they change between releases.
- Dark Mode is not an inversion. In iOS, sheets and popovers switch from base to elevated backgrounds automatically; custom backgrounds lose that depth cue.
- For custom foreground/background pairs, Apple suggests aiming for 7:1, especially for small text. 4.5:1 is the floor for body-size text; large text and essential icons follow the 3:1 rule above.
- Avoid an app-specific light/dark appearance setting; people expect the system choice to apply. Reading or media apps may offer content themes (paper, sepia) for the reading surface; elsewhere chrome follows the system appearance. See [content apps](content-apps.md) for how a reader screen reconciles the two.
- Soften bright white images in Dark Mode. Test in sunlight and dim rooms; reading apps can set `UIWhitePointAdaptivityStyle` to control True Tone adaptation.
- On Liquid Glass, color is for emphasis only: tint the background of a primary action (as prominent buttons do), not several controls. Over colorful content keep bars monochrome; over monochrome content the brand accent works well.

## Typography and Dynamic Type

[Typography](https://developer.apple.com/design/human-interface-guidelines/typography):

- Prefer Regular, Medium, Semibold, or Bold; avoid Ultralight, Thin, and Light at small sizes. Use few typefaces.
- System families: SF Pro (and Rounded) and New York (`Font.Design.serif`). Never embed system fonts. Custom fonts must implement Dynamic Type and Bold Text.
- Built-in text styles combine size, weight, and leading. Use the bold trait for an extra level, loose leading for long passages, tight leading only for one- or two-line rows (never for three or more lines).
- When text grows, prioritize content: titles of tabs and chrome need not scale as much as the article.
- At large sizes: avoid truncation (show as much at AX sizes as at the largest standard size), stack inline items (glyphs, timestamps) below text, reduce columns, keep primary elements at the top. Use `dynamicTypeSize.isAccessibilitySize` to switch layouts.

iOS text styles as size/leading in points, at the default (Large), largest standard (xxxLarge), and largest accessibility (AX5) settings:

| Style | Default | xxxLarge | AX5 |
| --- | --- | --- | --- |
| Large Title | 34/41 | 40/48 | 60/70 |
| Title 1 | 28/34 | 34/41 | 58/68 |
| Title 2 | 22/28 | 28/34 | 56/66 |
| Title 3 | 20/25 | 26/32 | 55/65 |
| Headline (semibold) | 17/22 | 23/29 | 53/62 |
| Body | 17/22 | 23/29 | 53/62 |
| Callout | 16/21 | 22/28 | 51/60 |
| Subheadline | 15/20 | 21/28 | 49/58 |
| Footnote | 13/18 | 19/24 | 44/52 |
| Caption 1 | 12/16 | 18/23 | 43/51 |
| Caption 2 | 11/13 | 17/22 | 40/48 |

The system tracks text automatically in apps; New York tracking matters only for mockups and HTML (0 at 15 pt, about −0.07 pt at 17 pt, about −0.2 pt at 20 pt).

## Layout

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout):

- Order by importance, top-to-bottom and leading-to-trailing. Align to scan; indent to subordinate; group with space, containers, or separators. Use progressive disclosure.
- Separate controls from content with Liquid Glass and the scroll edge effect, not solid or semi-opaque fills under controls. Extend full-screen backgrounds under bars.
- Choose layout by size class, not by device or orientation, and consider every combination (iPad windows resize freely). Keep functionality the same across sizes; larger spaces may show more (tab bar to sidebar).
- Respect safe areas, margins, and the readable content guide. Dynamic Type may require stacking adjacent views and growing rows.

## Materials and motion

[Materials](https://developer.apple.com/design/human-interface-guidelines/materials), [Motion](https://developer.apple.com/design/human-interface-guidelines/motion):

- Liquid Glass is for the functional layer only; the content layer uses standard materials (ultraThin, thin, regular, thick) chosen by meaning, with vibrant label/fill colors on top. Sliders and toggles in content may show glass only while active.
- Regular glass for text-heavy elements; clear glass only over rich media, with a 35% dark dimming layer when the media is bright.
- Motion must have a purpose, never be the only signal, follow the gesture's direction, stay brief, be cancelable, and be avoided on frequent interactions with custom elements.

## Icons and images

[Icons](https://developer.apple.com/design/human-interface-guidelines/icons), [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols), [Images](https://developer.apple.com/design/human-interface-guidelines/images):

- Interface icons: one simple concept, consistent weight and detail with each other and with adjacent text, optically centered, vector, labeled for VoiceOver.
- SF Symbols: match text weight; use scale for emphasis; outline beside text and in toolbars, fill in tab bars and swipe actions, slash for unavailable, enclosed for small sizes. Check availability for the deployment target. Symbol animations (bounce, pulse, replace, draw) should communicate, not decorate. SF Symbols and look-alikes may not be used in app icons or logos.
- Bitmaps at @2x and @3x with an embedded color profile; test on devices.

## Inclusion and privacy

[Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy), [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left):

- Plain language; address people as "you"; no idioms or casual humor that may not translate; gender-neutral copy and figures; disability is a spectrum and may be temporary or situational.
- Request only needed data, at the moment of need, with a specific one-sentence purpose string. A pre-permission screen has one "Continue" button and never imitates the system alert. Store secrets in the keychain; prefer passkeys or Sign in with Apple.
- Right to left: system components flip. Align multi-line paragraphs by their own language (in HTML, `dir="auto"` plus `lang`), flip progress and navigation, not real directions, logos, or digits.
