"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const ROOT = path.resolve(__dirname, "..");
// Only instruction-only skills ship through the Claude Code marketplace. Handoff needs the
// bundled native addon, which the release installer provides and a git-sourced plugin cannot.
const PLUGIN_SKILLS = ["ios-design"];
const marketplace = JSON.parse(
  fs.readFileSync(path.join(ROOT, ".claude-plugin/marketplace.json"), "utf8"),
);
function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
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
