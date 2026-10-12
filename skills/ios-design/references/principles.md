# Design principles and their sources

Each entry gives the idea, the test to apply, and what to take or leave. Prefer the test over the slogan.

## Apple Human Interface Guidelines and Liquid Glass

- **Hierarchy, harmony, consistency** (the iOS 26 framing). Content leads; navigation and controls form a distinct functional layer that floats above it. Shapes follow the hardware's concentric curves. Placement and icons stay predictable across apps and platforms.
- **Clarity, deference, depth** (the earlier framing, still useful). Legible text, an interface that defers to content, and layering that explains relationships.
- **Test:** Cover the content. Is the remaining chrome sparse and recognizably iOS? Cover the chrome. Does the content still read as the point of the screen?
- **Take:** standard bars, sheets, menus, search placement, swipe actions, SF Symbols, semantic colors, title-style section headers.
- **Leave:** glass on content, custom bar backgrounds that fight the scroll edge effect, mixing text and icons within a shared toolbar group.

## Typography tradition (Bringhurst, Butterick)

- Comfortable body measure is roughly 45–75 characters per line, about 66 ideal. Line spacing around 120–145% of the font size for body text, more for long-form reading at small sizes.
- Hierarchy comes from a small set of sizes and weights, used consistently. Uppercase with tracking is for short labels only.
- **Test:** Can you name the role of every text style on screen? Do two styles differ by only a point or two?
- **Take:** Apple text styles (`.largeTitle` through `.caption2`) as the scale; serif for long-form reading when it suits the content; true italics and real quotes.
- **Leave:** fixed point sizes, more than three or four distinct styles per screen, centered long text.

## Calm technology (Amber Case)

- Use the smallest amount of attention; inform and create calm; use the periphery; work even when it fails; the right amount of technology is the minimum needed.
- **Test:** Does a healthy, idle app show anything that demands a glance? Does a failure appear where the user will notice it in time, without blocking unrelated work?
- **Take:** ambient sync/offline status, progressive disclosure of problems, graceful degradation.
- **Leave:** persistent banners for states that need no action, spinners for background work the user did not start.

## Data-ink and signal (Tufte)

- Each mark should carry information. Remove redundant and decorative marks; encode the common case as absence.
- **Test:** Remove an icon, badge, rule, or count. Did the user lose a decision they needed to make?
- **Take:** one status channel per item; exceptions in color; counts only where they change behavior.
- **Leave:** a checkmark and a colored dot and a label for the same fact.

## Less, but better (Dieter Rams)

- Good design is unobtrusive, honest, thorough down to the last detail, and as little design as possible.
- **Test:** Is anything here to look designed rather than to help? Does any copy overstate what the app knows?
- **Take:** honesty about state, restraint, polish in error and empty states as much as hero screens.
- **Leave:** ornament that ages quickly.

## Local-first software (Ink & Switch)

- Software should be fast, work offline, keep data under the user's control, and treat the network as optional. The local copy is the primary copy.
- **Test:** Turn on Airplane Mode. Does everything already on the device open instantly with no error chrome? Do edits apply immediately and reconcile later?
- **Take:** optimistic local edits, background sync, conflict and failure surfaced per item, storage made visible and controllable.
- **Leave:** blocking loaders for local reads, modal network errors, and "connect to continue" for content already on the device.

## Fluid interfaces (Apple, "Designing Fluid Interfaces", WWDC 2018)

- Motion responds to the gesture's velocity, can be interrupted and redirected, and lands where the user expects. Feedback arrives at the moment of commitment.
- **Test:** Can every animation be interrupted? Does a swipe or drag preview its outcome before committing? Is there a haptic at commit, but not on every scroll tick?
- **Take:** springs, zoom transitions from the tapped source, `sensoryFeedback`, swipe actions with full-swipe for the primary safe action, Undo.
- **Leave:** long canned animations, motion that ignores Reduce Motion, haptics as decoration.

## Progressive disclosure and recognition over recall (Nielsen Norman Group)

- Show the frequent things; put the rare things one step away; keep labels visible instead of making people remember.
- **Test:** Is the most common action reachable with one tap or one gesture from where the user is? Are rare settings out of the main flow?
- **Take:** primary action visible, secondary in a menu, settings in a sheet.
- **Leave:** burying the primary action in an overflow menu, or exposing every setting inline.

## Inclusive and accessible design

- Disability is a mismatch between a person and a design; designs that fix it often help everyone (larger text outdoors, captions on a train).
- **Test:** Use the largest accessibility text size, VoiceOver, Increase Contrast, Reduce Motion, and Reduce Transparency. Is every task still possible and clear?
- **Take:** semantic structure, combined accessibility elements for rows, custom actions mirroring swipe actions, layouts that reflow at large sizes.

## Leave out by default

- **Skeuomorphic page curls and faux paper.** Conflicts with Liquid Glass and adds motion cost. A warm page color is enough.
- **Neumorphism.** Low contrast by construction.
- **Cross-platform design systems applied verbatim** (floating action buttons, snackbars, Android navigation patterns). Use the iOS equivalent.
- **Engagement mechanics** (streaks, guilt notifications, infinite autoplay). They trade attention for metrics, which conflicts with calm and content-first apps. Add only on request.
- **Brand-first chrome** that recolors bars and controls. Express brand in content, icon, accent, and typography, not by fighting system materials.
