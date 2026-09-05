# 2026-08-30 - README 배지 개발 일지

## 요청받은 것이 이미 있었습니다

"CI 상태 배지를 추가할 수 있는지" — `README.md:3` 에 이미 있었고 지금도
`passing` 을 돌려줍니다.

```console
$ curl -s -o /dev/null -w "%{http_code}\n" ".../ci.yml/badge.svg"
200
```

없다고 보고 하나 더 넣었으면 같은 배지가 둘이 됐습니다.

## 라이선스가 왜 안 보이느냐는 질문 — 세 곳을 각각 쟀습니다

| 어디 | 무엇이 나오나 |
|---|---|
| GitHub API | `{"key":"mit","spdx_id":"MIT"}` — **인식하고 있습니다** |
| PyPI JSON | `license_expression: 'MIT'`, `license: None`, License 분류자 0개 |
| shields.io `pypi/l/` | **`license: MIT`** — 동작합니다 |

### 중간에 틀린 결론을 냈습니다

PyPI 프로젝트 페이지를 받아 `MIT` 를 세었더니 **0회**였습니다. 여기서
*"분류자가 없어서 PyPI 가 렌더링을 못 한다"* 고 결론지을 뻔했습니다.

`attrs` 로 대조해 보고 틀린 것을 알았습니다.

```text
vm-stock-kis: MIT=0  len=3036
attrs:        MIT=0  len=3036     ← attrs 가 라이선스를 안 보여줄 리 없습니다
packaging:    Apache=1 len=127552
```

**`len=3036` 이 셋 중 둘에서 똑같습니다.** 페이지가 아니라 차단 응답이었고,
제가 센 것은 그 차단 페이지였습니다. 뚫린 `packaging` 을 보면 PyPI 는
분류자 없이 `license_expression` 을 그대로 렌더링합니다.

```html
<div class="sidebar-section__data-block">
<p>
Apache-2.0 OR BSD-2-Clause
```

> **같은 길이의 응답 둘은 내용이 아니라 차단입니다.** 대조군을 하나 넣지
> 않았으면 없는 결함을 고치고 있었을 것입니다.

## 배지에 값을 박지 않았습니다

처음 설계는 이랬습니다.

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENCE)
```

`badge/...` 형태는 **문자열을 URL 에 박는 것**입니다. `pyproject.toml` 만
바뀌면 배지가 거짓말을 시작하고 아무 검사도 안 걸립니다. CLAUDE.md 가 금지한
"손으로 적지 않는 것" 그대로입니다.

재 보니 `pypi/l/vm-stock-kis` 가 이미 `license: MIT` 를 돌려줍니다 —
`license = "MIT"` 가 `License-Expression` 으로 나가고 있기 때문입니다.
그래서 그쪽으로 바꿨습니다. **적을 값이 없으면 어긋날 일도 없습니다.**

손으로 적은 값은 **패키지 이름 하나**만 남았고, 그것이 틀리면 배지 셋이
동시에 404 가 되므로 거기에 검사를 겁니다.

## 되돌려 확인

| 무엇을 되돌렸나 | 결과 |
|---|---|
| 배지의 패키지 이름을 `vmkis` 로 | 1건 실패 — 어느 URL 이 빠졌는지 이름을 찍습니다 |
| 라이선스를 `badge/license-MIT-blue` 로 | **2건 실패** — 이름 검사 + "값을 박았다" 검사 |
| README 경로를 `READ.md` 로 | 4건 전부 error |

두 번째의 두 번째 검사가 이 파일의 핵심입니다. 값을 박는 형태가 **다시
생기지 않게** 막습니다.

## 손대지 않은 것

**커버리지 배지.** CI 가 `coverage.xml` 을 만들지만 codecov 같은 외부
서비스로 올리지 않아 배지가 읽을 곳이 없습니다. 계정 연결과
`CODECOV_TOKEN` 은 제가 할 수 없어 이슈로 남기지 않고 사용자에게
선택지로 제시했습니다.

**`License ::` 분류자.** PyPI 가 `license_expression` 을 직접 읽으므로
필요 없고, PEP 639 는 분류자와 병기하는 것을 오히려 권하지 않습니다.

## 변경 파일

- `README.md` — 배지 3개 추가 (PyPI 버전 · Python · License)
- `tests/unit/test_readme_badges.py` (신규) — 검사 4건

## 테스트 결과

```text
uv run pytest -m 'not requires_api and not performance'
  1212 passed, 7 skipped, 47 deselected in 32.60s
```
