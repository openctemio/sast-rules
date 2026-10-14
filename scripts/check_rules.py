#!/usr/bin/env python3
"""Checks every rule file of the pack.

- The file declares a permitted licence in its header:
  "# SPDX-License-Identifier: MIT" or "Apache-2.0" (ALLOWED below).
- The header names where the file comes from: "# Source: https://...".
- Every rule has an id (unique across the pack), languages, message and
  severity.
- A test fixture sits next to the rule file (same name, another extension)
  and holds, for every rule of the file, at least one positive case
  ("ruleid: <id>") and one negative case ("ok: <id>"). opengrep --test
  checks that the annotations match what the rule finds.

Usage: check_rules.py [rules-dir]   (default: rules)
"""
import os
import re
import sys

import yaml

ALLOWED = {"MIT", "Apache-2.0"}
SPDX = re.compile(r"^#\s*SPDX-License-Identifier:\s*(\S+)\s*$")
RULE_EXT = (".yml", ".yaml")
SOURCE = re.compile(r"^#\s*Source:\s*(https://\S+)\s*$")


def is_rule_file(name):
    # A YAML rule's own fixture is <name>.test.yaml (opengrep --test).
    return name.endswith(RULE_EXT) and not os.path.splitext(name)[0].endswith(".test")


def header(text, pattern):
    for line in text.splitlines():
        if not line.startswith("#"):
            break
        m = pattern.match(line)
        if m:
            return m.group(1)
    return None


def fixture_of(path):
    stem = os.path.splitext(path)[0]
    d = os.path.dirname(path) or "."
    base = os.path.basename(stem)
    out = []
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        stem2 = os.path.splitext(name)[0]
        if os.path.isfile(p) and ((stem2 == base and not name.endswith(RULE_EXT)) or stem2 == base + ".test"):
            out.append(p)
    return out


PENDING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests", "negative-pending.txt")


def load_pending():
    """Imported rules whose upstream fixture has no negative case yet. The
    list only shrinks: a rule added to the pack needs both cases."""
    try:
        with open(PENDING, encoding="utf-8") as fh:
            return {l.strip() for l in fh if l.strip() and not l.startswith("#")}
    except FileNotFoundError:
        return set()


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "rules"
    errors, ids, files, rules = [], {}, 0, 0
    pending, seen_pending = load_pending(), set()
    for d, _, names in os.walk(root):
        for name in sorted(names):
            if not is_rule_file(name):
                continue
            path = os.path.join(d, name)
            files += 1
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            lic = header(text, SPDX)
            if not header(text, SOURCE):
                errors.append(f"{path}: no '# Source: https://...' header")
            if lic not in ALLOWED:
                errors.append(f"{path}: licence {lic!r} is not one of {sorted(ALLOWED)} (SPDX-License-Identifier header)")
            try:
                doc = yaml.safe_load(text) or {}
            except yaml.YAMLError as e:
                errors.append(f"{path}: not YAML: {e}")
                continue
            fixtures = fixture_of(path)
            fx = ""
            for f in fixtures:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    fx += fh.read()
            if not fixtures:
                errors.append(f"{path}: no test fixture next to it")
            for r in doc.get("rules") or []:
                rules += 1
                rid = r.get("id")
                if not rid:
                    errors.append(f"{path}: a rule without id")
                    continue
                if rid in ids:
                    errors.append(f"{path}: rule id {rid} also in {ids[rid]}")
                ids[rid] = path
                for key in ("languages", "message", "severity"):
                    if not r.get(key):
                        errors.append(f"{path}: {rid}: no {key}")
                if fixtures:
                    if not re.search(r"\bruleid:\s*(?:[\w.\-]+\s*,\s*)*" + re.escape(rid) + r"\b", fx):
                        errors.append(f"{path}: {rid}: no positive case (ruleid:) in {fixtures}")
                    has_ok = re.search(r"\bok:\s*(?:[\w.\-]+\s*,\s*)*" + re.escape(rid) + r"\b", fx)
                    if rid in pending:
                        seen_pending.add(rid)
                        if has_ok:
                            errors.append(f"{path}: {rid}: has a negative case now: remove it from tests/negative-pending.txt")
                    elif not has_ok:
                        errors.append(f"{path}: {rid}: no negative case (ok:) in {fixtures}")
    for rid in sorted(pending - seen_pending):
        errors.append(f"tests/negative-pending.txt: {rid} is not a rule of the pack: remove it")
    for e in errors:
        print(e)
    print(f"{files} rule files, {rules} rules, {len(errors)} problems", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
