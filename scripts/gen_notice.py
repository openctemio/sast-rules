#!/usr/bin/env python3
"""Writes NOTICE: every file under rules/ that was imported from another
project, with its licence, source and copyright line, plus the licence
texts of each upstream.

  gen_notice.py          rewrite NOTICE
  gen_notice.py --check  fail when NOTICE is not current
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
RULES = os.path.join(ROOT, "rules")
OWN = "openctem"

UPSTREAMS = {
    "gitlab": ("GitLab sast-rules", "https://gitlab.com/gitlab-org/security-products/sast-rules",
               "MIT (rules marked MIT), Apache-2.0 (rules derived from gosec and bandit); Copyright (c) 2011-present GitLab Inc."),
    "0xdea": ("0xdea semgrep-rules", "https://github.com/0xdea/semgrep-rules", "MIT; Copyright (c) 2022 raptor"),
    "elttam": ("elttam semgrep-rules", "https://github.com/elttam/semgrep-rules", "MIT; Copyright (c) 2020 Semgrep (as stated in the upstream LICENSE)"),
}

SPDX = re.compile(r"^(?:#|//)\s*SPDX-License-Identifier:\s*(\S+)")
SOURCE = re.compile(r"^#\s*Source:\s*(\S+)")
LICENCE_LINE = re.compile(r"^(?:#|//|<!--)\s*License:\s*(.+?)\s*(?:-->)?$")


def head(path, n=12):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return [next(fh, "").rstrip("\n") for _ in range(n)]


def entries():
    rules, fixtures = [], []
    for d, _, names in sorted(os.walk(RULES)):
        rel_dir = os.path.relpath(d, RULES)
        top = rel_dir.split(os.sep)[0]
        if top in (OWN, "."):
            continue
        for name in sorted(names):
            path = os.path.join(d, name)
            rel = os.path.relpath(path, ROOT)
            lines = head(path)
            if name.endswith((".yml", ".yaml")) and not os.path.splitext(name)[0].endswith(".test"):
                spdx = next((m.group(1) for m in map(SPDX.match, lines) if m), "?")
                src = next((m.group(1) for m in map(SOURCE.match, lines) if m), "?")
                lic = next((m.group(1) for m in map(LICENCE_LINE.match, lines) if m), "")
                rules.append((rel, spdx, src, lic))
            else:
                lic = next((m.group(1) for m in map(LICENCE_LINE.match, lines) if m), "")
                fixtures.append((rel, lic))
    return rules, fixtures


def render():
    rules, fixtures = entries()
    out = [
        "OpenCTEM sast-rules",
        "Copyright (c) 2026 OpenCTEM contributors. Licensed under the MIT licence (LICENSE).",
        "",
        "This repository includes files imported from the projects below. Each",
        "imported rule file keeps its upstream licence (SPDX-License-Identifier",
        "header) and names the upstream file it comes from (Source header). The",
        "only change to an imported rule file is the addition of those two header",
        "lines. Licence texts: LICENSES/ (MIT texts are in each upstream's",
        "repository and reproduced below by copyright line).",
        "",
        "Upstream projects",
        "-----------------",
    ]
    for key, (name, url, lic) in UPSTREAMS.items():
        out.append(f"- {name} ({url}): {lic}")
    out += [
        "",
        "Test fixtures (files next to a rule, used only by opengrep --test) keep",
        "their upstream licence line. Fixtures marked LGPL-3.0 (from find-sec-bugs",
        "and security-code-scan, via GitLab sast-rules) are licensed under",
        "LGPL-3.0 (LICENSES/LGPL-3.0-only.txt, LICENSES/GPL-3.0-only.txt). Release",
        "bundles contain rule files only, never fixtures.",
        "",
        "MIT licence text (applies to every file marked MIT below, with the",
        "copyright holder named for its upstream):",
        "",
    ]
    with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as fh:
        mit = fh.read().split("\n\n", 2)[2].split("\n\nRules under")[0]
    out += [mit, "", "Imported rule files", "-------------------"]
    for rel, spdx, src, lic in rules:
        out.append(f"{rel}")
        out.append(f"  licence: {spdx}" + (f" ({lic})" if lic else ""))
        out.append(f"  source:  {src}")
    out += ["", "Imported test fixtures with a licence other than MIT", "----------------------------------------------------"]
    for rel, lic in fixtures:
        if lic and not lic.startswith("MIT"):
            out.append(f"{rel}: {lic}")
    return "\n".join(out) + "\n"


def main():
    text = render()
    path = os.path.join(ROOT, "NOTICE")
    if "--check" in sys.argv:
        try:
            with open(path, encoding="utf-8") as fh:
                if fh.read() == text:
                    return 0
        except FileNotFoundError:
            pass
        print("NOTICE is not current: run scripts/gen_notice.py", file=sys.stderr)
        return 1
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
