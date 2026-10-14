#!/usr/bin/env bash
# Runs the pack on every benchmark repository and prints the coverage.
#   bench/run.sh <work-dir> [coverage.py report options]
# Clones each pinned commit into <work-dir>/repos (once) and writes the
# opengrep results to <work-dir>/results.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
work="${1:?usage: bench/run.sh <work-dir> [--min PCT] [--json out.json]}"
shift
mkdir -p "$work/repos" "$work/results"
while read -r name url commit; do
  case "$name" in '' | '#'*) continue ;; esac
  dir="$work/repos/$name"
  if [ ! -d "$dir/.git" ]; then
    git init -q "$dir"
    git -C "$dir" fetch -q --depth 1 "$url" "$commit"
    git -C "$dir" checkout -q FETCH_HEAD
  fi
  [ "$(git -C "$dir" rev-parse HEAD)" = "$commit" ] || { echo "$name: not at $commit" >&2; exit 1; }
  (cd "$dir" && opengrep scan --json --output "$work/results/$name.json" --config "$root/rules" \
    --no-rewrite-rule-ids --disable-version-check --quiet --timeout 30 . >/dev/null)
done < "$root/bench/repos.txt"
python3 "$root/scripts/coverage.py" report "$work/results" "$@"
