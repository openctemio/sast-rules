# OpenCTEM sast-rules

Static analysis rules for [opengrep](https://github.com/opengrep/opengrep), maintained by OpenCTEM. They are:

- **permissively licensed**: our own rules are MIT. Rules imported from other projects keep their MIT or Apache-2.0 licence, named in each file. Nothing here carries a non-commercial, Commons Clause or copyleft condition.
- **tested**: every rule has a fixture with cases that must match (`ruleid:`) and cases that must not (`ok:`).
- **measured**: CI reports coverage per language on pinned public benchmark repositories.
- **signed**: releases are reproducible bundles signed with cosign keyless, by this repository's release workflow.

The OpenCTEM sensor installs the latest release as its managed `semgrep-rules` content. The `ci-opengrep` image carries one release. Both verify the signature first.

## Use

```sh
opengrep scan --config rules/ --no-rewrite-rule-ids <path>
```

`--no-rewrite-rule-ids` keeps the rule ids as written here. OpenCTEM uses the rule id in a finding's identity.

## Releases and verification

Each tag `v<major>.<minor>.<patch>` publishes:

| asset | content |
|---|---|
| `sast-rules-<v>.tar.gz` | `rules/` (rule files only, no fixtures), `LICENSE`, `NOTICE`, `LICENSES/`, `VERSION`. Reproducible: sorted, mtime 0, uid/gid 0 |
| `.sha256` | its SHA-256 |
| `.sigstore.json` | cosign bundle: certificate, signature and transparency-log proof |
| `.sig`, `.pem` | the signature and certificate, separately |

Verify:

```sh
cosign verify-blob --bundle sast-rules-<v>.tar.gz.sigstore.json \
  --certificate-identity https://github.com/openctemio/sast-rules/.github/workflows/release.yml@refs/tags/v<v> \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  sast-rules-<v>.tar.gz
```

## Layout

```
rules/openctem/<language>/   our rules (MIT)
rules/gitlab/                imported from GitLab sast-rules (MIT, Apache-2.0)
rules/0xdea/                 imported from 0xdea/semgrep-rules (MIT)
rules/elttam/                imported from elttam/semgrep-rules (MIT)
bench/                       benchmark repositories, reference locations, exclusions
scripts/                     checks, coverage, bundle build, opengrep install
```

## Coverage

`bench/repos.txt` pins six public repositories: DVWA, pygoat, go-test-bench, gin, WebGoat and juice-shop.

- **Reference locations**: `bench/baseline/` lists where a broad reference rule set reported results on those commits. It holds paths and lines only, no rule text.
- **Covered**: a location counts as covered when a pack result overlaps it.
- **Exclusions**: locations that are not vulnerabilities are listed with a reason in `bench/baseline-excluded.txt`.
- **CI gate**: CI fails if a SAST language (php, python, javascript/typescript, java, go) drops below 80%.

| language | covered | reference | coverage |
|---|---|---|---|
| html | 159 | 163 | 97.5% |
| python | 70 | 72 | 97.2% |
| go | 37 | 39 | 94.9% |
| javascript / typescript | 52 | 55 | 94.5% |
| java | 41 | 49 | 83.7% |
| php | 36 | 43 | 83.7% |
| yaml (GitHub Actions) | 59 | 73 | 80.8% |
| dockerfile | 6 | 6 | 100% |

Terraform (17 reference locations) is not covered. Infrastructure as code is the `iac` capability, which runs trivy.

Run it locally: `bench/run.sh /tmp/bench --min 80 --languages php,python,javascript,java,go`.

## Adding a rule

1. Write `rules/openctem/<language>/<name>.yaml`. It starts with `# SPDX-License-Identifier: MIT` and `# Source: https://github.com/openctemio/sast-rules`, and the rule id is `openctem.<language>.<class>.<name>`.
2. Write a fixture next to it with the same name (`<name>.test.yaml` for YAML targets). It needs at least one `ruleid: <id>` case and one `ok: <id>` case.
3. Run the checks:
   ```sh
   python3 scripts/check_rules.py rules
   opengrep scan --test rules/
   bench/run.sh /tmp/bench
   ```
4. Importing from another project:
   - only MIT or Apache-2.0 files;
   - keep the upstream header and add the SPDX and Source lines;
   - run `scripts/gen_notice.py`.

   Imported rules whose upstream fixture has no `ok:` case yet are listed in `tests/negative-pending.txt`. That list may only shrink.

Never copy rules, messages or fixtures from sources under other licences (see NOTICE for what is allowed).
