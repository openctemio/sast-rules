#!/usr/bin/env bash
# Installs the pinned opengrep release binary into $1 (default ~/.local/bin):
# checks its SHA-256 and verifies its keyless signature with cosign against
# the opengrep release workflow of exactly that version.
set -euo pipefail
OPENGREP_VERSION=1.31.0
SHA256_X86=dbbe3c2058dbe600c449a8ba22ea79a1643a6660658400090d0323a8d0d31147
SHA256_AARCH64=2b713a29a00237f85408b83002fc111db5b94c7fa8d263f0a93184a960655d9d
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
