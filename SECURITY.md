# Security policy

## Supported versions

Only the latest release of `kuchka` receives security fixes.

## Reporting a vulnerability

Please report a vulnerability privately, through GitHub's
[private vulnerability reporting](https://github.com/Dimonade/kuchka/security/advisories/new),
and not as a public issue.

A useful report names the affected version, gives a minimal reproduction, and
describes the impact. A first answer comes within seven days. A fix is released
as a new version, and the report is credited unless you prefer otherwise.

## What counts

`kuchka` is a pure-Python library without network or file access, so the reports
that matter are about untrusted input: parsing a string, converting a number, or
any path where a small input makes the library consume unbounded time or memory.
The size limits on exact numeric input are in `kuchka.internal.limits`.

`pickle` of untrusted data is unsafe for any library and is not a supported way
to receive values; see
[Copying, pickling, and persistence](docs/concepts/persistence.md).

## Release provenance

Releases are published from GitHub Actions with PyPI trusted publishing, and each
file carries a
[PyPI attestation](https://docs.pypi.org/attestations/) that names the repository and
workflow that built it. Verify a downloaded file with:

```bash
uvx pypi-attestations verify pypi --repository https://github.com/Dimonade/kuchka \
  pypi:kuchka-<version>-py3-none-any.whl
```
