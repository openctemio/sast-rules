#!/usr/bin/env python3
"""Coverage of the pack on the benchmark repositories.

bench/repos.txt pins each repository (name, URL, commit). bench/baseline/
<name>.json holds the locations (path, lines, language) of the results a
reference rule set gave on that commit; it holds no rule text. A baseline
location counts as covered when a pack result in the same file overlaps
its lines (TOLERANCE lines either side). Locations listed, with a reason,
in bench/baseline-excluded.txt are not vulnerabilities and are left out.

  coverage.py baseline   <name> <reference-results.json>   write a baseline
  coverage.py report     <results-dir> [--min PCT] [--json out.json]

results-dir holds <name>.json, opengrep --json output of the pack.
--min fails when a language (with at least MIN_SAMPLES baseline locations)
is below PCT; --languages a,b limits that gate to those languages.
"""
import json
import os
import sys

TOLERANCE = 2
MIN_SAMPLES = 10
HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(HERE, "..", "bench")

LANG = {
    ".php": "php", ".py": "python", ".java": "java", ".go": "go", ".rb": "ruby",
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "javascript", ".tsx": "javascript", ".cs": "csharp", ".scala": "scala", ".kt": "kotlin",
    ".c": "c", ".h": "c", ".cpp": "c", ".html": "html", ".htm": "html",
    ".yml": "yaml", ".yaml": "yaml", ".json": "json", ".tf": "terraform", ".sh": "bash",
}


def language(path):
    base = os.path.basename(path)
    if base.lower().startswith("dockerfile") or base.endswith(".dockerfile"):
        return "dockerfile"
    return LANG.get(os.path.splitext(base)[1].lower(), "other")


def locations(results):
    out = []
    for r in results.get("results", []):
        p = r["path"]
        out.append({"path": p, "start": r["start"]["line"], "end": r["end"]["line"], "language": language(p)})
    return out


def cmd_baseline(name, ref):
    with open(ref, encoding="utf-8") as fh:
        locs = locations(json.load(fh))
    uniq = sorted({(l["path"], l["start"], l["end"], l["language"]) for l in locs})
    doc = [{"path": p, "start": s, "end": e, "language": lang} for p, s, e, lang in uniq]
    os.makedirs(os.path.join(BENCH, "baseline"), exist_ok=True)
    with open(os.path.join(BENCH, "baseline", name + ".json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    print(f"{name}: {len(doc)} locations")


def repos():
    out = []
    with open(os.path.join(BENCH, "repos.txt"), encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                out.append(line.split()[0])
    return out


def excluded():
    """bench/baseline-excluded.txt: baseline locations that are not
    vulnerabilities (with the reason), left out of the denominator."""
    out = set()
    try:
        with open(os.path.join(BENCH, "baseline-excluded.txt"), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    name, path, start = line.split()[:3]
                    out.add((name, path, int(start)))
    except FileNotFoundError:
        pass
    return out


def cmd_report(results_dir, min_pct=None, json_out=None, gate_langs=None):
    per_lang = {}
    per_repo = {}
    skip = excluded()
    for name in repos():
        with open(os.path.join(BENCH, "baseline", name + ".json"), encoding="utf-8") as fh:
            base = json.load(fh)
        with open(os.path.join(results_dir, name + ".json"), encoding="utf-8") as fh:
            pack = locations(json.load(fh))
        by_file = {}
        for p in pack:
            by_file.setdefault(p["path"], []).append(p)
        hit = 0
        base = [b for b in base if (name, b["path"], b["start"]) not in skip]
        for b in base:
            covered = any(p["start"] <= b["end"] + TOLERANCE and p["end"] >= b["start"] - TOLERANCE
                          for p in by_file.get(b["path"], []))
            t = per_lang.setdefault(b["language"], [0, 0])
            t[1] += 1
            if covered:
                t[0] += 1
                hit += 1
        per_repo[name] = {"covered": hit, "baseline": len(base), "pack_results": len(pack)}
    rows = []
    print("| language | covered | baseline | coverage |")
    print("|---|---|---|---|")
    failed = []
    for lang in sorted(per_lang, key=lambda k: -per_lang[k][1]):
        c, n = per_lang[lang]
        pct = 100.0 * c / n if n else 0.0
        rows.append({"language": lang, "covered": c, "baseline": n, "coverage": round(pct, 1)})
        print(f"| {lang} | {c} | {n} | {pct:.1f}% |")
        gated = gate_langs is None or lang in gate_langs
        if min_pct is not None and gated and n >= MIN_SAMPLES and pct < min_pct:
            failed.append(lang)
    print()
    print("| repository | covered | baseline | pack results |")
    print("|---|---|---|---|")
    for name, r in per_repo.items():
        print(f"| {name} | {r['covered']} | {r['baseline']} | {r['pack_results']} |")
    if json_out:
        with open(json_out, "w", encoding="utf-8") as fh:
            json.dump({"languages": rows, "repositories": per_repo}, fh, indent=1)
    if failed:
        print(f"\nbelow {min_pct}%: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


def main():
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "baseline":
        cmd_baseline(a[1], a[2])
        return 0
    if len(a) >= 2 and a[0] == "report":
        min_pct = float(a[a.index("--min") + 1]) if "--min" in a else None
        json_out = a[a.index("--json") + 1] if "--json" in a else None
        langs = set(a[a.index("--languages") + 1].split(",")) if "--languages" in a else None
        return cmd_report(a[1], min_pct, json_out, langs)
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
