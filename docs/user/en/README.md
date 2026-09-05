# vm-stock-kis (English)

A Python client for the **Korea Investment & Securities (한국투자증권) Open Trading
API**. Domestic and overseas **cash equities only** — no futures, options, bonds,
or ELW.

> **The documentation for this project is written in Korean.** This page is the
> only English document, and it is deliberately kept short. See
> [Why only this page](#why-only-this-page).

## Install

```bash
pip install vm-stock-kis
```

## Before you write any code

Copy the template and fill it in — do not edit the template in place.

```bash
cp configs/template_account_profiles.yaml configs/account_profiles.yaml
```

**A live app registration is required even if you only trade on paper.** Quote
TRs do not exist on the paper domain, so a quote request from a paper account
still goes to the live domain and uses the live app key. If your config lists
only a paper app, `create_client()` stops and tells you what to add.
([#87](https://github.com/visualmoney/vm-stock-kis/issues/87))

```python
from vmkis import create_client

kis = create_client()          # reads configs/account_profiles.yaml
print(kis.stock("005930").quote())
```

Quotes you receive are for **your own use only**. Redistributing them to third
parties or wrapping them in an external service is prohibited (customer terms
art. 5③) and can get the API account suspended. Read the current terms on
[KIS Developers](https://apiportal.koreainvestment.com/) — this page does not
copy the full text. Korean detail:
[USER_GUIDE](../USER_GUIDE.md#시세-조회).

## Where to go next

Korean, but the code blocks read the same in any language:

| Document | What it covers |
|---|---|
| [QUICKSTART](../../../QUICKSTART.md) | Install to first quote, with a full config example |
| [docs/INDEX](../../INDEX.md) | Index of every document in this repository |
| [docs/FAQ](../../FAQ.md) | Frequently asked questions |
| [docs/user/EXTENDING_API](../EXTENDING_API.md) | Calling unsupported TRs through `fetch()` |
| [SECURITY](../../../SECURITY.en.md) | **English.** How credentials are handled, how to report a vulnerability |
| [CHANGELOG](../../../CHANGELOG.md) | Version history |

Runnable code needs no translation: [`examples/`](../../../examples/).

## Why only this page

English versions of QUICKSTART and FAQ used to live here. They fell behind the
Korean originals and started giving wrong instructions — the English QUICKSTART
never received the live-app requirement above, and the English FAQ still taught
argument names that had been removed. A translation nobody updates is worse than
no translation, because a reader cannot tell it is stale.

They are frozen at [`archive/docs/user/en/`](../../../archive/docs/user/en/).

English coverage may grow again later. What each level would contain is written
down in advance so the scope is not re-invented under pressure — see
[#104](https://github.com/visualmoney/vm-stock-kis/issues/104). **When to move is
a decision, not a rule**, and no condition triggers it automatically.

**Issues and pull requests in English are welcome.**
