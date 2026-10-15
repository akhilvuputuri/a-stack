# HIG components and patterns for iOS

Distilled from the [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines) component and pattern pages (read 13 October 2026). Paraphrased; follow the linked page for exact wording.

Contents: [Navigation](#navigation) · [Presentation](#presentation) · [Content views and controls](#content-views-and-controls) · [Feedback and state](#feedback-and-state) · [Lifecycle and settings](#lifecycle-and-settings)

## Navigation

**[Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)**
- Include only the most important actions; put the rest in a More menu only if needed. Don't add a custom overflow.
- Minimize custom toolbar backgrounds and tinted controls, and reserve tint for the one primary action. Let the content inform the color and use the scroll edge effect for separation.
- Titles: short (under about 15 characters), never the app name, and may be empty when the content already identifies the screen. On iOS a large title collapses on scroll to keep people oriented.
- Use the standard Back and Close buttons with their standard symbols, not text labels saying "Back" or "Close". A custom version must look and behave the same.
- Prefer symbols without borders (for example `ellipsis`, not `ellipsis.circle`); use text for actions symbols don't express well, such as Edit.
- One primary action, styled prominent, on the trailing side. Use at most about three groups. Keep navigation and critical actions in their own groups, and separate text-labeled items from symbol items.
- Hiding toolbars temporarily for distraction-free reading is encouraged, provided a familiar gesture (tap, swipe down) reliably restores them.

**[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)**
- Use them for navigation, never actions. Keep them visible across sections (modals excepted).
- Use few tabs and avoid overflow. Never hide or disable a tab; explain empty sections instead.
- Give each tab a one-word label and a filled SF Symbol. Badges are for critical information only.
- iOS: a tab bar can minimize on scroll alongside an accessory, and a dedicated search tab sits at the trailing end. iPad: prefer `sidebarAdaptable`.

**[Search](https://developer.apple.com/design/human-interface-guidelines/search-fields)** ([Searching](https://developer.apple.com/design/human-interface-guidelines/searching))
- Use a placeholder that states the scope. Search as people type, and offer recent and suggested searches.
- Show the most relevant results first. Scope bars help when categories are clear (start broad), and tokens work for common filters.
- iOS placement: bottom toolbar when there's room (Mail, Notes); top when bottom content matters; a tab for discovery-heavy apps; inline to filter a single view.
- One search location for the whole app where possible, with the current scope always visible. Let people clear search history.
- Index content in Spotlight so it can be found without opening the app.

**[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views), [sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)**
- Use them only in regular width. Persistently highlight the selected item, show at most two hierarchy levels, and let people hide them. On iPad, start from a tab bar that can become a sidebar.

## Presentation

**[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)**
- Present modally only when there's a clear benefit. Keep the task short and give it a title.
- Avoid a modal that feels like an app within the app (one path, no buttons that look like dismiss).
- Always provide an obvious dismissal (top-toolbar button or swipe down). Confirm before discarding user content.
- Show one modal at a time.

**[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)**
- Cancel or Close sits on the leading side and Done on the trailing side. Always pair Done with Cancel or Back; never show all three.
- One sheet at a time; close the first before opening another.
- On iPhone, consider the medium detent for progressive disclosure, and include a grabber on resizable sheets (VoiceOver can use it).
- Support swipe to dismiss; if there are unsaved changes, confirm with an action sheet. Use a full-screen modal for long or complex flows.

**[Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers)**
- Use for small, related tasks only. Avoid them in compact width (iPhone portrait) and use a sheet instead.
- The arrow points to the source. Show one at a time, and don't use popovers for warnings.
- Save work when a popover closes on an outside tap.

**[Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)**
- Use alerts sparingly, and only when they're actionable. A purely informational problem (server unavailable) gets an indicator people can tap to learn more.
- No alerts for common, undoable actions, even destructive ones. Do alert for uncommon, irreversible ones.
- No alert at launch. When offline, show cached content with a nonintrusive label.
- Use an action sheet, not an alert, for choices about an action the person started.

**[Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)** (SwiftUI `confirmationDialog`)
- Short title; message only if needed. Destructive choices go first and are styled destructive; Cancel goes last.
- Anchor the sheet to its source control, and avoid scrolling.

**[Going full screen](https://developer.apple.com/design/human-interface-guidelines/going-full-screen), [status bars](https://developer.apple.com/design/human-interface-guidelines/status-bars)**
- For reading or media, temporarily hide bars and restore them with a tap or swipe. Keep essential controls easy to reveal, and resume where people left off.
- Content scrolling under the status bar must be obscured by a scroll edge effect. Never hide the status bar permanently; a tap brings it back.

## Content views and controls

**[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)**
- Use lists for text and collections for image-heavy, varied-size items.
- Keep row text succinct; long content shows as titles with a detail view.
- Navigation lists persistently highlight the selection; option lists use a checkmark.
- To drill into a row's detail, use the standard disclosure indicator; the info button is only for more information about the row.
- Use the grouped style with headers and footers for grouped data. Don't combine a section index with trailing accessories.

**[Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views)**
- Keep standard elastic scrolling, and hint that more content exists. Never nest scroll views of the same orientation.
- Consider page-by-page scrolling that overlaps by a unit such as one line of text. `.scrollTargetBehavior(.paging)` (`PagingScrollTargetBehavior`) pages by the full container with no overlap; overlap needs a custom `ScrollTargetBehavior` that subtracts it in `updateTarget`.
- Auto-scroll only as much as needed (for example, to a search hit).
- Prefer the automatic scroll edge effect style, use it only behind floating elements, and apply one per view.

**[Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)**
- Hit regions of at least 44×44 pt. Custom buttons need a pressed state.
- Use the prominent style for the most likely action, one or two per view. Distinguish options by style, not size.
- Give the primary role (Return key) only to non-destructive actions.
- For slow actions, show an activity indicator inside the button with an "-ing…" label.

**[Menus](https://developer.apple.com/design/human-interface-guidelines/menus), [context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus), [edit menus](https://developer.apple.com/design/human-interface-guidelines/edit-menus)**
- Labels are title-case verbs without articles. Add an ellipsis when more input follows.
- Put frequent items first and group related items with separators. Use submenus sparingly, one level deep and about five items. Icons go on all items in a group or on none.
- iOS menus can lead with a row of three labeled (medium) or four icon-only (small) frequent actions.
- Context menus hold the item's most relevant actions only, in about three groups at most. Hide unavailable items rather than dimming them, and put destructive items last, marked destructive.
- Every context-menu action must also be available elsewhere in the interface.
- Give context menus a preview that shows a condensed version of the item. An item has either a context menu or an edit menu, not both.
- Let people select and copy useful static text such as content, errors, and identifiers.

**[Controls](https://developer.apple.com/design/human-interface-guidelines/toggles)**
- Use switches only in list rows; elsewhere use a button that toggles.
- Segmented controls: about five segments or fewer on iPhone, equal widths, either text or images (not both), noun labels.
- Pickers for medium-to-long lists, with a pull-down button for short ones.
- Sliders run from minimum on the leading side to maximum on the trailing side. Pair them with a text field or stepper when exact values matter.

## Feedback and state

**[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)**
- Match interruption to significance. Integrate status next to what it describes (Mail shows last update and unread count in the mailbox toolbar).
- Warn only about unexpected, irreversible data loss. Confirm completion only for significant tasks.
- Explain why a command can't run.

**[Loading](https://developer.apple.com/design/human-interface-guidelines/loading), [progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators)**
- Show something immediately, and let people do other things while content loads.
- Prefer determinate progress that is honest and evenly paced, and switch from indeterminate to determinate when you can (never from spinner to bar).
- Write specific descriptions, not "Loading". Keep the indicator in a consistent place, and offer Cancel (plus Pause if cancelling loses work).
- Refresh controls complement automatic updates. Their optional title should carry value, such as when the content last updated.

**[Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)**
- Make undo predictable and visible: name the action ("Undo Archive") and show the restored result, scrolling to it if needed.
- Allow multiple undos. Integrate with `UndoManager` so shake and three-finger gestures work, and don't redefine those gestures.

**[Haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)**
- Use system patterns only for their documented meaning: notification for task outcomes, impact for physical metaphors, selection while values change.
- Be consistent, short, and sparing; match the haptic to the animation, and make haptics optional. Standard controls already play them.

**[Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)**
- Standard gestures keep their standard meaning. Custom gestures must be discoverable, easy, and never the only way to do something.
- Shortcut gestures supplement visible buttons (swipe back plus a Back button). Show when a gesture isn't available.

## Lifecycle and settings

**[Launching](https://developer.apple.com/design/human-interface-guidelines/launching)**
- Launch instantly. The launch screen matches the first screen, with no text, logo, or splash.
- Restore the previous state in detail, including scroll position.

**[Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)**
- Ideally there is none; otherwise keep it brief, interactive, and skippable. Prefer contextual tips (TipKit).
- Defer nonessential setup by choosing good defaults. Ask for permissions at first use unless the app can't work without them.
- Ask for ratings only after engagement.

**[Settings](https://developer.apple.com/design/human-interface-guidelines/settings)**
- Choose good defaults and offer few settings. Don't ask for information the system already knows (such as Dark Mode).
- Don't duplicate systemwide settings such as appearance, text size, or accessibility options.
- Task-specific options belong on the screen they affect (sort, filter, reading typography). App settings hold general, infrequently changed options.

**[Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts)**
- Require an account only for core functionality, explain the benefit on the sign-in screen, and delay sign-in as long as possible.
- Prefer Sign in with Apple or passkeys. Name the authentication method in the button, and never call it a "passcode".
- Account deletion must be possible in the app, or through a direct, discoverable link. Say when deletion completes.

**[Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking)**
- Finish user-started tasks (such as downloads) in the background, and pause attention-dependent activity when people leave.
- Send notifications sparingly, mainly to report the outcome of something the person started.
