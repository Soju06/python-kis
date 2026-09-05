# Security Policy

*[한국어](./SECURITY.md)*

VM-Stock-KIS handles **real brokerage credentials and order-placing authority** for
Korea Investment & Securities (KIS) accounts. This document explains how to report a
vulnerability, and how the library treats your credentials.

---

## Supported versions

Only the latest release receives security fixes. If you are on an older version,
upgrade first.

---

## Reporting a vulnerability

**Please do not report vulnerabilities through public issues.** Disclosing one before a
fix exists puts other users at risk.

Use GitHub's private vulnerability reporting:

**[Report a vulnerability](https://github.com/visualmoney/vm-stock-kis/security/advisories/new)**

Helpful things to include:

- A description of the issue
- Steps to reproduce (a minimal reproduction if possible)
- The impact you expect
- Affected versions

**Do not include real AppKeys, SecretKeys, account numbers, or access tokens in your
reproduction.** Redact them (e.g. `PSED321z...`) if a value is needed to explain the issue.

This is a single-maintainer project, so an immediate response is not guaranteed, but you
will get an acknowledgement **within 7 days**. Once a fix is confirmed, a patched release
is published and the advisory is made public, crediting you unless you prefer otherwise.

### Relationship to the upstream project

This repository is a fork of
[Soju06/python-kis](https://github.com/Soju06/python-kis). If a vulnerability lives in
code that predates the fork, it affects upstream too. In that case we will notify
upstream as well — you do not need to file the report twice.

---

## How credentials are stored

> **Important**: this library stores credentials and access tokens as **plaintext JSON**.
> They are not encrypted.

| What | Location | Format |
|---|---|---|
| `KisAuth.save()` | path you choose | plaintext JSON (`id`, `appkey`, `secretkey`, `account`) |
| Access token (`keep_token=True`) | `~/.vmkis/` (default) | plaintext JSON |
| `configs/account_profiles.yaml` | default config path | plaintext YAML |

The `cryptography` dependency is used **only to decrypt KIS websocket payloads**. It has
nothing to do with credentials written to disk.

Therefore:

- **Do not use `keep_token=True` on machines you do not trust** (shared PCs, shared
  servers, someone else's container).
- Restrict credential files to your own user (`chmod 600`).
- Never commit credential files. `.gitignore` covers `configs/*` (except the template)
  and leftover root names (`config.yaml`, `real_secret.json`, `virtual_secret.json`),
  but **a file saved under any other name will not be caught.**
- If you suspect exposure, **reissue your AppKey immediately** at
  [KIS Developers](https://apiportal.koreainvestment.com/). This library cannot revoke a key.

### Ways credentials can leak into logs

- **`TRACE_DETAIL_ERROR`**: setting `vmkis.__env__.TRACE_DETAIL_ERROR = True` prints the
  full request and response for any non-200 reply. **This exposes your AppKey in
  exception messages.** It defaults to `False`; do not share logs captured with it on.
- **`repr()`**: `KisKey.__repr__` masks the SecretKey as `***` but **prints the AppKey in
  full**. `KisAuth.__repr__` exposes only the account number and whether it is a virtual
  account.
- **`str(token)`**: `KisAccessToken.__str__` returns the full `Bearer <token>`. Its
  `repr()` shows only the expiry. Do not log token objects directly.

Redact these values before attaching logs to an issue.

---

## In scope

- Any path that unintentionally exposes credentials or tokens (logs, exceptions, `repr`,
  file permissions)
- Flaws in authentication or token handling (for example, a token sent to the wrong domain)
- Flaws that cause an order to be built incorrectly or routed to the wrong account
- Remote code execution or deserialization issues in response parsing
- Known vulnerabilities in dependencies that this library actually exposes

## Out of scope

- **Problems with the KIS API servers themselves** — contact
  [KIS Developers](https://apiportal.koreainvestment.com/community).
- **Your own credential leak** (committed by mistake, phishing, and so on) — reissue your
  AppKey. This is not a library vulnerability.
- **The documented design behaviour above** (plaintext storage). Proposals to improve it
  are welcome as a normal issue. If you find exposure **broader than what is documented
  here**, report it privately.
- Automated scanner output with no demonstrated impact.

---

## Repository security settings

- **Secret scanning** and **push protection** are enabled — commits containing
  credentials are blocked at push time.
- **Private vulnerability reporting** is enabled.
- CI runs the test suite and workflow linting on every pull request.

---

## Test against the virtual account first

This library can place real orders. Validate new code against a virtual trading account
(`virtual=True`) before pointing it at a live one.
