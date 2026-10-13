"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const ROOT = path.resolve(__dirname, "..");
// Only instruction-only skills ship through the Claude Code marketplace. Handoff needs the
// bundled native addon, which the release installer provides and a git-sourced plugin cannot.
const PLUGIN_SKILLS = ["ios-design"];
const marketplace = JSON.parse(
  fs.readFileSync(path.join(ROOT, ".claude-plugin/marketplace.json"), "utf8"),
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
    [...PLUGIN_SKILLS].sort(),
  );
});

test("each plugin entry points at its skill folder with matching name and no runtime", () => {
  for (const plugin of marketplace.plugins) {
    assert.equal(plugin.source, "./skills/" + plugin.name);
    assert.deepEqual(plugin.skills, ["."]);
    assert.match(plugin.version, /^\d+\.\d+\.\d+$/);
    assert.ok(plugin.description);
    const dir = path.join(ROOT, plugin.source);
    const skill = fs.readFileSync(path.join(dir, "SKILL.md"), "utf8");
    assert.match(skill, new RegExp("^---\\nname: " + plugin.name + "\\n"));
    for (const file of walk(dir)) {
      const info = fs.lstatSync(file);
      assert.ok(!info.isSymbolicLink(), "plugin files cannot be symlinks: " + file);
      assert.ok(info.isDirectory() || file.endsWith(".md"), "unexpected plugin file: " + file);
    }
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

// Each released version records a digest of its skill folder, so changing the
// skill without bumping its version (which Claude Code needs to ship an update) fails.
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
      assert.equal(recorded, taggedDigest(tag, plugin.source), tag + " is released; bump the version instead");
    }
  }
});
