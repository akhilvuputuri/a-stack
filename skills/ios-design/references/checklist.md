# Verification matrix

Run the rows that apply to the change. Record each as observed, not run (with reason), or not applicable. Use synthetic or demo data in any screenshot that leaves the machine.

| Area | Check |
| --- | --- |
| Build | Project builds for the deployment target and for the latest SDK; newer APIs are availability-gated with a working fallback. |
| Tests | Existing unit and UI tests pass; accessibility identifiers used by UI tests are unchanged. |
| Appearance | Light, Dark, each custom theme, and System; switching themes while a sheet is open. |
| Text size | Default, largest standard (xxxLarge), and largest accessibility size (AX5), plus Bold Text. No clipped or overlapping text; no more truncation at AX sizes than at xxxLarge; rows grow; inline items stack; toolbars still fit. |
| Contrast | At default settings, in every theme: text below 18 pt (below 14 pt if bold) meets 4.5:1; larger text and essential icons meet 3:1. This follows WCAG AA, which is stricter than Apple's HIG table for small bold text. Then recheck with Increase Contrast on. |
| Materials | Reduce Transparency on, alone and together with Increase Contrast and Dark Mode; custom glass and overlays stay legible. Liquid Glass clear and tinted appearance preferences. |
| Motion | Reduce Motion on; transitions fall back to fades; nothing essential relies on animation. |
| VoiceOver | Logical reading order; rows read as one element with a useful summary; icon buttons labeled; swipe actions present in the Actions rotor (no duplicates); state changes announced when relevant. |
| Touch | Targets at least 44×44 pt; swipe and context-menu actions match and are also reachable elsewhere in the UI; destructive actions are confirmed or undoable; every gesture has a visible alternative. |
| Other input | Voice Control can name every control (visible labels match accessibility labels); Full Keyboard Access reaches every action; no UI disappears on a timer before people can act. |
| Language | A right-to-left pseudolanguage and a long-string pseudolanguage (Xcode scheme options) keep layouts intact; paragraphs align by their own language. |
| States | Empty, loading, partial, failed, offline (Airplane Mode, with no alert at launch), signed out, very long titles, missing author or image; state restores after relaunch, including scroll position. |
| Layout | Smallest supported iPhone, largest iPhone, landscape where supported, and iPad if the app runs there. Content clears bottom search and toolbars. |
| Feedback | Haptics fire once at commitment; no haptic on scroll or passive updates. |

Simulator settings: Settings > Accessibility > Display & Text Size (Bold Text, Larger Text, Increase Contrast, Reduce Transparency), Motion > Reduce Motion; Display & Brightness > Liquid Glass for Clear or Tinted (iOS 26.1 and later). Xcode's Environment Overrides and Accessibility Inspector cover most of these quickly. SwiftUI previews can pin `\.dynamicTypeSize`, `\.colorScheme`, and `\.legibilityWeight` for fast iteration, but confirm in the simulator.
