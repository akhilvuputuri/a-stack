# Writing for iOS interfaces

Distilled from the HIG pages on [Writing](https://developer.apple.com/design/human-interface-guidelines/writing), [Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion), [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts), [Menus](https://developer.apple.com/design/human-interface-guidelines/menus), [Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications), and [Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) (read 13 October 2026). Paraphrased.

## Voice and tone

- Decide the app's voice and keep a short word list so the same thing always has the same name (for example "article", "brief", "archive").
- Adjust tone to the moment: plain and serious for errors and data loss, lighter for success.
- Use few words, plain language, and active voice. Read copy aloud.
- Address people as "you". Avoid "we", which is especially unclear in errors: "Unable to load content" beats "We're having trouble…".
- Use possessives sparingly ("Favorites", not "Your Favorites").
- Avoid idioms, jargon, and casual humor; they exclude people and don't translate.
- Say "tap" on touch devices, not "click".

## Labels and capitalization

- Buttons and links are verbs that name the result ("Save", "Archive", "Retry Download"), never "Click here" and never cute ("Let's do it!").
- Choose title case or sentence case per element type and apply it everywhere. Apple's components use title case for buttons, menu items, alert buttons, notification titles, and toolbar items; complete sentences use sentence case with punctuation.
- Multi-step flows: start with "Get Started", move on with "Continue" or "Next" consistently, and finish with "Done".
- Menu items: title-case verbs without articles; add an ellipsis when more input follows; changeable labels for toggles ("Show Images"/"Hide Images").
- Settings: name the setting practically and describe what turning it on does. Link straight to a setting instead of describing where it is.
- Segmented controls take nouns. Avoid putting the app's own name in titles, actions, quick actions, or notification text; the system already shows it.

## Errors, empty states, and status

- Prevent errors first. When one happens, show it next to the problem, without blame, saying how to fix it ("Choose a password with at least 8 characters"), with no "Oops".
- If wording can't fix a common error, change the interaction.
- Empty states are temporary: give the next step and a button for it, and keep crucial information out of them.
- Alert titles are specific (never "Error" or a code) and two lines at most. Add a message only when it adds value, and don't explain the buttons.
- Alert buttons are one or two words. Use "OK" only for purely informational alerts, and always "Cancel" for cancelling.
- Progress text says what is actually happening ("Downloading 3 images", "Summarizing your notes"), not "Loading" or "Processing".
- Text-field hints show an example ("name@example.com"). Validation messages instruct ("Use only letters for your name") rather than scold ("Invalid name").
- Permission purpose strings are one specific, active, complete sentence ending in a period.

## Notifications

- Keep them concise and informative; never send several for the same thing, and don't tell people to do tasks.
- Report errors in the app (with an alert or inline), not with a notification. Keep private details out.
- Provide a short generic body for hidden previews ("New brief").
- Action buttons are short, title-case results, and never "Open". Badges count unread notifications only.

## Generative and agent-made content

- Say clearly when content was produced by AI or an agent, and never present it as written by a person.
- Note that it may contain errors, and keep sources visible. Avoid AI output where an error could cause harm.
- Put Edit, Undo, Retry, or a way to dismiss next to the generated content, and make feedback voluntary and lightweight.
