# 2026-08-30 - README 배지

## 사용자 요청

> README.md 파일 ci 상태를 표시를 추가할 수 있는지?

이어서:

> MIR or Apache 2.0으로 라이센스가 표시 되지 않는 이유는

## 분석

### CI 배지는 이미 있었습니다

`README.md:3` 입니다. 확인해 보니 실제로 `passing` 을 돌려줍니다.

```console
$ curl -s ".../actions/workflows/ci.yml/badge.svg" | grep -o "passing"
passing
```

**요청받은 것이 이미 있을 때는 그것을 먼저 말해야 합니다.** 없다고 보고
하나 더 넣으면 같은 배지가 둘이 됩니다.

### 없는 것은 다른 배지들

근거가 저장소에 이미 있습니다 — `pyproject.toml` 의 `license = "MIT"`,
`requires-python = ">=3.10"`, 그리고 PyPI 에 `vm-stock-kis 0.1.0`.

커버리지 배지는 **지금은 불가능**합니다. CI 가 `coverage.xml` 을 만들지만
codecov 같은 외부 서비스로 올리지 않아 배지가 읽을 곳이 없습니다.

### 라이선스 표시 질문

세 곳을 각각 확인했습니다. 결론은 **어디서도 문제가 없다**는 것입니다.

## 계획

1. PyPI 버전 · Python · License 배지 추가. **값을 손으로 적지 않는 형태로**
2. 손으로 적은 값이 남으면 그것을 대조하는 검사
3. 되돌려 확인

## 결과

배지 3개를 넣고 검사 4건을 붙였습니다. 라이선스는 처음에
`badge/license-MIT-blue` 로 박으려 했다가 `pypi/l/` 이 실제로 동작하는 것을
확인하고 바꿨습니다 — **적을 값이 없으면 어긋날 일도 없습니다.**

일지: [2026-08-30_12_readme_badges.md](../dev_logs/2026-08-30_12_readme_badges.md)
