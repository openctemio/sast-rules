#!/usr/bin/env bash
# Installs the pinned opengrep release binary into $1 (default ~/.local/bin):
# checks its SHA-256 and verifies its keyless signature with cosign against
# the opengrep release workflow of exactly that version.
set -euo pipefail
OPENGREP_VERSION=1.30.2
SHA256_X86=a66aa3278457f02b287b985a45b6762aebcaba5000f2689245fd1ed86d1456c7
SHA256_AARCH64=90acea5df4b733083f388d4feeb250ca802f671b33d1f222653d1e571dd2b0d8
dest="${1:-$HOME/.local/bin}"
case "$(uname -m)" in
  x86_64) arch=x86; sum="$SHA256_X86" ;;
  aarch64 | arm64) arch=aarch64; sum="$SHA256_AARCH64" ;;
  *) echo "unsupported architecture $(uname -m)" >&2; exit 1 ;;
esac
f="opengrep_manylinux_${arch}"
base="https://github.com/opengrep/opengrep/releases/download/v${OPENGREP_VERSION}"
tmp="$(mktemp -d)"
trap 'rm -rf -- "${tmp:?}"' EXIT
for x in "" .cert .sig; do curl -fsSL -o "$tmp/$f$x" "$base/$f$x"; done
echo "$sum  $tmp/$f" | sha256sum -c -
cosign verify-blob --cert "$tmp/$f.cert" --signature "$tmp/$f.sig" \
  --certificate-identity "https://github.com/opengrep/opengrep/.github/workflows/rolling-release.yml@refs/heads/release-v${OPENGREP_VERSION}" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com "$tmp/$f"
mkdir -p "$dest"
install -m 0755 "$tmp/$f" "$dest/opengrep"
"$dest/opengrep" --version
