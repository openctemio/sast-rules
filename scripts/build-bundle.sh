#!/usr/bin/env bash
# Builds a reproducible rules bundle: rule files only (no test fixtures),
# with LICENSE, NOTICE, LICENSES/ and VERSION.
#   build-bundle.sh <version> <out-dir>
set -euo pipefail
version="${1:?usage: build-bundle.sh <version> <out-dir>}"
out="${2:?usage: build-bundle.sh <version> <out-dir>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
stage="$(mktemp -d)"
trap 'rm -rf -- "${stage:?}"' EXIT
name="sast-rules-$version"
mkdir -p "$stage/$name" "$out"
(cd "$root" && find rules -type f \( -name '*.yml' -o -name '*.yaml' \) ! -name '*.test.yaml' ! -name '*.test.yml' -print0 |
  xargs -0 -I{} install -D -m 0644 {} "$stage/$name/{}")
cp -R "$root/LICENSE" "$root/NOTICE" "$root/LICENSES" "$stage/$name/"
echo "$version" > "$stage/$name/VERSION"
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -C "$stage" -cf - "$name" | gzip -n -9 > "$out/$name.tar.gz"
(cd "$out" && sha256sum "$name.tar.gz" > "$name.tar.gz.sha256")
echo "$out/$name.tar.gz: $(find "$stage/$name/rules" -type f | wc -l) rule files"
