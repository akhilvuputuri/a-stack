"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const ROOT = path.resolve(__dirname, "..");
// Only instruction-only plugins ship through the plugin marketplaces. Each lives at
// plugins/<name>/skills/<skill>/SKILL.md, the layout Claude Code, Codex and `npx skills`
// all discover. Handoff needs the bundled native addon, which only the release installer
// provides, so it stays in skills/ and is hidden from `npx skills`.
// Each plugin's exact skill inventory. Only workflow carries the Claude SessionStart hook.
const PLUGIN_SKILLS = {
  "ios-design": ["ios-design"],
  workflow: ["adopt", "experiment", "incident", "independent-review", "journal", "preflight", "ship"],
};
const PLUGINS = Object.keys(PLUGIN_SKILLS);
const HOOK_PLUGINS = ["workflow"];
const HANDOFF_SKILLS = ["publish-handoff", "resume-handoff"];
const marketplace = JSON.parse(
  fs.readFileSync(path.join(ROOT, ".claude-plugin/marketplace.json"), "utf8"),
);
const codexMarketplace = JSON.parse(
  fs.readFileSync(path.join(ROOT, ".agents/plugins/marketplace.json"), "utf8"),
);
function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === ".DS_Store") continue; // Finder metadata; git-ignored and never shipped.
    const full = path.join(dir, entry.name);
    out.push(full);
    if (entry.isDirectory()) walk(full, out);
  }
  return out;
}

test("marketplace lists exactly the allowlisted instruction-only skills", () => {
  assert.equal(marketplace.name, "a-stack");
  assert.ok(marketplace.owner && marketplace.owner.name);
  assert.deepEqual(
    marketplace.plugins.map((plugin) => plugin.name).sort(),
    [...PLUGINS].sort(),
  );
});

function assertInstructionOnly(dir, allowed) {
  for (const file of walk(dir)) {
    const info = fs.lstatSync(file);
    assert.ok(!info.isSymbolicLink(), "plugin files cannot be symlinks: " + file);
    const relative = path.relative(dir, file).split(path.sep).join("/");
    assert.ok(
      info.isDirectory() || file.endsWith(".md") || allowed.includes(relative),
      "unexpected plugin file: " + file,
    );
  }
}

// Skill frontmatter can declare hooks, tools and other behavior that runs when the skill
// is invoked. Marketplace skills are instructions only, so allow exactly name and description.
function frontmatter(text, name) {
  const match = /^---\n([\s\S]*?)\n---\n/.exec(text);
  assert.ok(match, name + ": SKILL.md needs frontmatter");
  return match[1];
}
function assertPlainFrontmatter(text, name) {
  const keys = frontmatter(text, name).split("\n").map((line) => line.split(":")[0]);
  assert.deepEqual(keys, ["name", "description"], name + ": frontmatter may hold only name and description");
}
function skillNames(dir) {
  return fs
    .readdirSync(path.join(dir, "skills"), { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);
}

// Claude Code caps SessionStart hook output at 10,000 characters; beyond that the core
// rules would be replaced by a file path and a 2,000-character preview.
const HOOK_OUTPUT_LIMIT = 10000;

test("each plugin holds named instruction-only skills under plugins/<name>/skills", () => {
  for (const plugin of marketplace.plugins) {
    assert.equal(plugin.source, "./plugins/" + plugin.name);
    assert.equal(plugin.skills, undefined, "plugins use the default skills/ scan");
    assert.match(plugin.version, /^\d+\.\d+\.\d+$/);
    assert.ok(plugin.description);
    const dir = path.join(ROOT, plugin.source);
    const hasHook = HOOK_PLUGINS.includes(plugin.name);
    assert.equal(fs.existsSync(path.join(dir, "hooks")), hasHook, plugin.name + ": unexpected hooks/");
    assertInstructionOnly(dir, [
      ".codex-plugin/plugin.json",
      ...(hasHook ? ["hooks/hooks.json", ".codex-plugin/hooks.json"] : []),
    ]);
    const names = skillNames(dir);
    assert.deepEqual(names.sort(), [...PLUGIN_SKILLS[plugin.name]].sort(), plugin.name + ": skill inventory");
    for (const name of names) {
      const skill = fs.readFileSync(path.join(dir, "skills", name, "SKILL.md"), "utf8");
      assert.match(skill, new RegExp("^---\\nname: " + name + "\\ndescription: \\S"));
      assertPlainFrontmatter(skill, name);
    }
    if (!hasHook) {
      assert.ok(!fs.existsSync(path.join(dir, "CORE.md")), plugin.name + ": CORE.md without its hook");
      continue;
    }
    const core = fs.readFileSync(path.join(dir, "CORE.md"), "utf8");
    assert.ok(core.length < HOOK_OUTPUT_LIMIT, "CORE.md must stay under the hook output cap");
    for (const name of names) assert.ok(core.includes("`" + name + "`"), "CORE.md must list " + name);
    const hooks = JSON.parse(fs.readFileSync(path.join(dir, "hooks/hooks.json"), "utf8"));
    assert.deepEqual(hooks, {
      hooks: {
        SessionStart: [
          { hooks: [{ type: "command", command: "cat", args: ["${CLAUDE_PLUGIN_ROOT}/CORE.md"] }] },
        ],
      },
    });
  }
});

test("the Codex marketplace and manifests mirror the Claude marketplace", () => {
  assert.equal(codexMarketplace.name, marketplace.name);
  assert.deepEqual(
    codexMarketplace.plugins.map((p) => p.name).sort(),
    marketplace.plugins.map((p) => p.name).sort(),
  );
  for (const plugin of marketplace.plugins) {
    const entry = codexMarketplace.plugins.find((p) => p.name === plugin.name);
    assert.deepEqual(entry.source, { source: "local", path: plugin.source });
    assert.equal(entry.version, plugin.version);
    assert.equal(entry.description, plugin.description);
    assert.ok(entry.policy && entry.policy.installation && entry.policy.authentication && entry.category);
    const manifest = JSON.parse(
      fs.readFileSync(path.join(ROOT, plugin.source, ".codex-plugin/plugin.json"), "utf8"),
    );
    assert.equal(manifest.name, plugin.name);
    assert.equal(manifest.version, plugin.version);
    assert.equal(manifest.description, plugin.description);
    assert.equal(manifest.skills, "./skills/");
    // Codex discovers hooks/hooks.json unless the manifest names hooks explicitly, and it
    // drops the Claude hook's args. Point Codex at an explicit empty hooks file instead.
    if (HOOK_PLUGINS.includes(plugin.name)) {
      assert.equal(manifest.hooks, "./.codex-plugin/hooks.json");
      const codexHooks = JSON.parse(
        fs.readFileSync(path.join(ROOT, plugin.source, ".codex-plugin/hooks.json"), "utf8"),
      );
      assert.deepEqual(codexHooks, { hooks: {} });
    } else {
      assert.equal(manifest.hooks, undefined);
    }
  }
});

test("skills/ holds only Handoff, hidden from `npx skills` discovery", () => {
  const names = fs
    .readdirSync(path.join(ROOT, "skills"), { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);
  assert.deepEqual(names.sort(), [...HANDOFF_SKILLS].sort());
  for (const name of HANDOFF_SKILLS) {
    const skill = fs.readFileSync(path.join(ROOT, "skills", name, "SKILL.md"), "utf8");
    assert.match(frontmatter(skill, name), /\nmetadata:\n  internal: true$/);
  }
});

test("README pins the tag that matches each plugin version", () => {
  const readme = fs.readFileSync(path.join(ROOT, "README.md"), "utf8");
  for (const plugin of marketplace.plugins) {
    const tag = plugin.name + "--v" + plugin.version;
    const pinned = [...readme.matchAll(new RegExp(plugin.name + "--v[0-9]+\\.[0-9]+\\.[0-9]+", "g"))].map((m) => m[0]);
    assert.ok(pinned.length > 0, "README must pin " + tag);
    assert.deepEqual([...new Set(pinned)], [tag]);
  }
});

// Each released version records a digest of its plugin folder, so changing the
// plugin without bumping its version (which Claude Code needs to ship an update) fails.
function digest(dir) {
  const hash = crypto.createHash("sha256");
  for (const file of walk(dir).filter((f) => fs.lstatSync(f).isFile()).sort()) {
    hash.update(path.relative(dir, file).split(path.sep).join("/") + "\0");
    hash.update(fs.readFileSync(file));
    hash.update("\0");
  }
  return hash.digest("hex");
}

test("each plugin's content matches the digest recorded for its version", () => {
  const releases = JSON.parse(
    fs.readFileSync(path.join(ROOT, ".claude-plugin/releases.json"), "utf8"),
  );
  for (const plugin of marketplace.plugins) {
    const recorded = releases[plugin.name] || {};
    const actual = digest(path.join(ROOT, plugin.source));
    assert.equal(
      recorded[plugin.version],
      actual,
      plugin.name + " changed: bump its version and record " + actual + " for it",
    );
  }
});

// Released versions are immutable: once <name>--v<version> is tagged, its recorded digest
// must match the tagged files. Untagged (unreleased) versions may still change.
// Reads raw blobs with cat-file, so no repository-configured filters or hooks run.
function git(args) {
  const result = spawnSync("git", ["-c", "core.fsmonitor=false", ...args], {
    cwd: ROOT,
    encoding: "buffer",
    maxBuffer: 64 * 1024 * 1024,
  });
  return result.status === 0 ? result.stdout : null;
}
function taggedDigest(tag, source) {
  const prefix = source.replace(/^\.\//, "");
  const listing = git(["ls-tree", "-r", "-z", tag, "--", prefix]);
  if (listing === null) return null;
  const files = listing
    .toString("utf8")
    .split("\0")
    .filter(Boolean)
    .map((line) => {
      const [meta, file] = line.split("\t");
      return { type: meta.split(" ")[1], file };
    });
  assert.ok(files.every((entry) => entry.type === "blob"), tag + " contains non-file entries");
  const hash = crypto.createHash("sha256");
  for (const { file } of files.sort((a, b) => (a.file < b.file ? -1 : a.file > b.file ? 1 : 0))) {
    hash.update(path.posix.relative(prefix, file) + "\0");
    hash.update(git(["cat-file", "blob", tag + ":" + file]));
    hash.update("\0");
  }
  return hash.digest("hex");
}

test("released versions keep the digest of their tagged content", (t) => {
  if (git(["rev-parse", "--is-inside-work-tree"]) === null) return t.skip("not a git checkout");
  const releases = JSON.parse(
    fs.readFileSync(path.join(ROOT, ".claude-plugin/releases.json"), "utf8"),
  );
  for (const plugin of marketplace.plugins) {
    for (const [version, recorded] of Object.entries(releases[plugin.name] || {})) {
      const tag = plugin.name + "--v" + version;
      if (git(["rev-parse", "-q", "--verify", "refs/tags/" + tag]) === null) continue;
      // A plugin may move between releases, so use the source recorded at the tag itself.
      const tagged = JSON.parse(git(["cat-file", "blob", tag + ":.claude-plugin/marketplace.json"]).toString("utf8"));
      const entry = tagged.plugins.find((p) => p.name === plugin.name);
      assert.ok(entry, tag + " exists but its marketplace does not list " + plugin.name);
      const source = entry.source;
      assert.equal(recorded, taggedDigest(tag, source), tag + " is released; bump the version instead");
    }
  }
});
