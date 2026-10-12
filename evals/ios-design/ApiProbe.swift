// Compile probe for APIs named in skills/ios-design/references. Typecheck only; not shipped.
// xcrun swiftc -typecheck -sdk "$(xcrun --sdk iphonesimulator --show-sdk-path)" \
//   -target arm64-apple-ios26.0-simulator evals/ios-design/ApiProbe.swift
import SwiftUI
struct Probe: View {
  @Namespace var ns
  @State var q = ""
  @State var flag = false
  @Environment(\.accessibilityReduceTransparency) var rt
  @Environment(\.accessibilityReduceMotion) var rm
  @Environment(\.colorSchemeContrast) var contrast
  @Environment(\.legibilityWeight) var lw
  var body: some View {
    TabView {
      Tab("Library", systemImage: "books.vertical") {
        NavigationStack {
          List {
            Text("Row").font(.system(.title3, design: .serif, weight: .semibold))
              .font(.custom("Georgia", size: 20, relativeTo: .body))
              .matchedTransitionSource(id: "a", in: ns)
              .accessibilityAction(named: "Archive") {}
              .contextMenu { Button("Archive") {} }
              .swipeActions(edge: .leading, allowsFullSwipe: true) { Button("Archive") {} }
            NavigationLink("x") { Text("d").navigationTransition(.zoom(sourceID: "a", in: ns)) }
          }
          .formStyle(.grouped)
          .scrollEdgeEffectStyle(.soft, for: .top)
          .safeAreaBar(edge: .bottom) { Text("Undo") }
          .searchable(text: $q)
          .searchScopes($q) { Text("All").tag("") }
          .searchToolbarBehavior(.minimize)
          .sensoryFeedback(.success, trigger: flag)
          .toolbar {
            if !flag { ToolbarItem(placement: .topBarTrailing) { Button("A") {} } }
            ToolbarSpacer(.fixed, placement: .topBarTrailing)
            ToolbarItem(placement: .confirmationAction) { Button("Done") {} }
            DefaultToolbarItem(kind: .search, placement: .bottomBar)
          }
          .toolbarVisibility(.hidden, for: .navigationBar)
        }
      }
      Tab(role: .search) { Text("Search") }
    }
    .tabBarMinimizeBehavior(.onScrollDown)
    .tabViewBottomAccessory { Text("Now playing") }
    .tabViewStyle(.sidebarAdaptable)
    .overlay {
      GlassEffectContainer {
        Button("G") {}.buttonStyle(.glass)
        Button("P") {}.buttonStyle(.glassProminent)
        Text("c").glassEffect(.regular.tint(.orange).interactive(), in: .rect(cornerRadius: 12))
          .glassEffectID("c", in: ns)
        ConcentricRectangle()
        Rectangle().fill(.clear).clipShape(.rect(corners: .concentric, isUniform: true))
        Color.clear.backgroundExtensionEffect()
        ContentUnavailableView("Empty", systemImage: "book")
      }
    }
    .confirmationDialog("Delete?", isPresented: $flag) { Button("Delete", role: .destructive) {} }
  }
}
