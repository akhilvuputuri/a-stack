# Liquid Glass and iOS 26 conventions

Summarized from Apple's "Adopting Liquid Glass" overview and the Human Interface Guidelines (Materials, Color, Toolbars, Scroll views) as of the iOS 26 SDK. Component rules beyond glass live in [HIG components](hig-components.md). Confirm every API against the project's SDK before relying on it, and gate with `#available(iOS 26, *)` when the deployment target is lower.

## Layers

- Liquid Glass is the functional layer: bars, tab bars, toolbars, sidebars, sheets, popovers, menus, and a few important custom controls. Content sits beneath it.
- Never apply glass to list rows, cards, article bodies, or images. Glass on glass (stacked glass elements) reduces legibility. The content layer uses standard materials (`.ultraThinMaterial` through `.thickMaterial`) when it needs separation. Sliders and toggles in content may show glass only while being used.
- Regular glass suits text-heavy elements (alerts, sidebars, popovers). Clear glass is only for controls over rich media; add a dark dimming layer of about 35% when that media is bright.
- Standard components adopt the material automatically when built with the current SDK. Start by rebuilding and looking before writing custom code.

## Bars and backgrounds

- Remove custom backgrounds from `NavigationStack` bars, toolbars, tab bars, and split views. Calls such as `.toolbarBackground(color, for: .navigationBar)` or `UINavigationBarAppearance` fills interfere with the glass and the scroll edge effect. Let a custom page color show through instead.
- System bars apply a scroll edge effect so content scrolling beneath stays legible. A custom bar placed with `safeAreaInset` does not get it; use `.safeAreaBar(edge:)` so the system can apply the effect. Tune with `.scrollEdgeEffectStyle(_:for:)` only when necessary.
- `.backgroundExtensionEffect()` mirrors and blurs adjacent content beneath sidebars and inspectors on iPad and Mac.

## Toolbars

- Group related items that share a background; separate unrelated groups with `ToolbarSpacer(.fixed)` (or a flexible spacer). Do not mix text and icons inside one shared group.
- Prefer standard SF Symbols for common actions, and always give icon-only items an accessibility label.
- Remove a whole item (`if condition { ToolbarItem { … } }` inside the toolbar builder) rather than hiding its content, which leaves an empty glass capsule. `ToolbarContent.hidden(_:)` is unavailable on iOS in the iOS 26.2 SDK.
- Give a toolbar at most one primary action (Done, Submit), styled prominent, on the trailing side: `.confirmationAction` placement in sheets, `UIBarButtonItem.Style.prominent` in UIKit, or `.buttonStyle(.glassProminent)` for a custom button. Confirm the rendered style in the simulator.
- Use symbols without borders (`ellipsis`, not `ellipsis.circle`); the glass capsule already provides the container. Keep the standard Back and Close buttons.
- Aim for at most three toolbar groups.
- Bottom toolbars (`.bottomBar`) suit reading and editing screens where actions belong near the thumb.

## Search

- On iPhone, `.searchable` on a navigation container places search at the bottom for reach.
- When search is secondary, `.searchToolbarBehavior(.minimize)` collapses it into a toolbar button. `DefaultToolbarItem(kind: .search, placement: .bottomBar)` positions it explicitly among other bottom items.
- In a `TabView`, mark the search tab with `Tab(role: .search)` so it separates and morphs into a field.

## Tabs

- `.tabBarMinimizeBehavior(.onScrollDown)` lets the tab bar recede while reading.
- `.tabViewBottomAccessory { … }` hosts persistent mini-players or status above the tab bar.
- `.tabViewStyle(.sidebarAdaptable)` turns tabs into a sidebar on iPad.

## Controls and custom glass

- Prefer `.buttonStyle(.glass)` and `.buttonStyle(.glassProminent)` to hand-built glass.
- For custom elements use `.glassEffect(_:in:)` with `Glass.regular` (optionally `.tint(_:)` and `.interactive()`), sparingly. Combine neighbors in a `GlassEffectContainer` for performance and morphing; use `.glassEffectID(_:in:)` for morph transitions.
- Shapes should be concentric with their container: `ConcentricRectangle` or `.rect(corners:isUniform:)`.
- Tint controls lightly. A custom accent color needs light, dark, and increased-contrast variants.

## Sheets, menus, dialogs

- Sheets are inset with larger corner radii at partial detents and become more opaque at full height. Remove custom sheet or popover backgrounds; check content near the rounder corners.
- `confirmationDialog` anchors to its source control. Attach it to the button that triggers it.
- Menus show icons for common actions. The top actions of a context menu should match that item's swipe actions.

## Lists and forms

- Rows and sections have more padding and larger corner radii. Do not hard-code row heights.
- Section headers use title-style capitalization; the system no longer uppercases them. Update header strings.
- Use `Form` with `.formStyle(.grouped)` to inherit platform metrics.

## Accessibility settings to test

Reduce Transparency, Increase Contrast, Reduce Motion, the user's Liquid Glass appearance preference (clear or tinted), Bold Text, and the largest accessibility text sizes. System components adapt; custom glass, colors, and animations must be checked by hand. Read `\.accessibilityReduceTransparency`, `\.accessibilityReduceMotion`, and `\.colorSchemeContrast` in custom views.

## Icons

App icons use layered artwork composed in Icon Composer, with default, dark, clear, and tinted variants. Prefer simple, solid, overlapping shapes and let the system apply highlights and blur.
