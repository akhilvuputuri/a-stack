// Synthetic fixture for ios-design skill evaluations. Not a real app; not built by tests.
// Deployment target for evaluation: iOS 17.0, built with the iOS 26 SDK.
import SwiftUI

struct Episode: Identifiable {
  let id: UUID
  var show: String
  var title: String
  var minutes: Int
  var played: Double  // 0...1
  var downloaded: Bool
  var failed: String?
}

struct EpisodeLibrary: View {
  @State var episodes: [Episode]
  @State private var query = ""
  @State private var syncing = false
  @AppStorage("theme") private var theme = "light"

  var body: some View {
    NavigationStack {
      VStack(spacing: 0) {
        if episodes.contains(where: { $0.failed != nil }) {
          HStack {
            Image(systemName: "exclamationmark.triangle.fill").foregroundColor(.red)
            Text("Some downloads failed").font(.system(size: 12))
            Spacer()
          }.padding(8).background(Color.yellow)
        }
        HStack {
          Text("\(episodes.count) episodes").font(.system(size: 12))
          Spacer()
          if syncing { ProgressView() }
        }.padding(.horizontal)
        List {
          ForEach(episodes) { episode in
            NavigationLink {
              Text(episode.title)
            } label: {
              VStack(alignment: .leading, spacing: 4) {
                HStack {
                  Text(episode.show.uppercased()).font(.system(size: 10)).foregroundColor(.gray)
                  Spacer()
                  if episode.played == 1 { Image(systemName: "checkmark") }
                  if episode.downloaded {
                    Image(systemName: "arrow.down.circle.fill").foregroundColor(.green)
                  }
                  Image(systemName: "ellipsis")
                    .onTapGesture { /* show options */ }
                }
                Text(episode.title).font(.system(size: 21, weight: .semibold)).lineLimit(1)
                Text("\(episode.minutes) min").font(.system(size: 11)).foregroundColor(.gray)
              }
              .padding()
              .glassEffect(.regular, in: .rect(cornerRadius: 16))
            }
            .swipeActions(edge: .trailing, allowsFullSwipe: true) {
              Button(role: .destructive) {
                episodes.removeAll { $0.id == episode.id }
              } label: {
                Image(systemName: "trash")
              }
            }
          }
        }
        .listStyle(.plain)
        .background(theme == "sepia" ? Color(red: 0.96, green: 0.94, blue: 0.89) : .white)
      }
      .navigationTitle("Library")
      .toolbarBackground(theme == "sepia" ? Color(red: 0.95, green: 0.92, blue: 0.86) : .white, for: .navigationBar)
      .toolbarBackground(.visible, for: .navigationBar)
      .searchable(text: $query)
      .toolbar {
        ToolbarItem(placement: .topBarTrailing) {
          Button { syncing = true } label: { Image(systemName: "arrow.clockwise") }
        }
        ToolbarItem(placement: .topBarTrailing) {
          Button("Edit") {}
        }
      }
      .task {
        syncing = true
        episodes = []
        try? await Task.sleep(for: .seconds(2))
        syncing = false
      }
    }
  }
}
