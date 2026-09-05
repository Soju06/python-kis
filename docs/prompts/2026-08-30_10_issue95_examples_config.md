# 2026-08-30 - #95 예제 `--config` 기본값

## 사용자 요청

> #95 시작해줘

(선행 대화: `next-up` 3건 중 `#92` → `#95` → `#103` 순으로 정했고 `#92` 는
[PR #110](https://github.com/visualmoney/vm-stock-kis/pull/110) 으로 끝났습니다.)

## 분석

### 이슈가 적은 것

예제 7개의 `--config` 기본값이 `config.yaml` 인데 저장소 루트에 그런 파일이
없습니다. 문서는 전부 `configs/account_profiles.yaml` 을 안내합니다.

### 실제로 세어 보니 28곳

```text
default="config.yaml"                            7   사용자가 실제로 막히는 곳
os.path.join(os.getcwd(), "config.yaml")         7   두 번째 기본값
"config.yaml이 루트에 있어야 함" (docstring)       8   실행 조건 안내
나머지 문구(docstring·주석·에러 메시지)             6
                                                --
                                                28   파일 12개
```

`#75` 가 고쳤다는 `01_basic/` 에도 **문구가 4건 남아 있습니다.**
`03_advanced/02_performance_analysis.py` 는 `--config` 자체가 없는데 실행
조건에만 `config.yaml` 이 적혀 있습니다.

### 검사를 어떻게 쓸 것인가 — 여기가 핵심

이슈는 *"`--config` 의 default 가 전부 같은 값인지"* 를 제안합니다.
**그 검사는 11개가 똑같이 틀려도 통과합니다.** 오늘 세션 종료 일지가 적은
"게으르게 만든 구현"이 정확히 이 형태입니다.

라이브러리에 이미 정답이 있습니다.

```python
# src/vmkis/helpers.py:24
DEFAULT_CONFIG_PATH = "configs/account_profiles.yaml"
```

그래서 **예제의 기본값을 `create_client` 자신의 기본값과 대조**합니다.
`inspect.signature(create_client).parameters["config_path"].default` 로 꺼내면
비공개 이름을 import 하지 않고도 되고, 라이브러리가 경로를 바꾸면 검사가
따라옵니다.

## 계획

1. 28곳을 유형별로 일괄 정정 (손으로 목록을 적지 않습니다)
2. `tests/unit/test_examples_signatures.py` 에 검사 추가 —
   `create_client` 의 기본값과 대조
3. **검사기를 검사**: 한 파일만 되돌려 빨개지는지, 검사기가 0건을 보고 있지
   않은지
4. 문서(`docs/`, `README`)에도 같은 갈라짐이 있는지 확인

## 결과

28곳 + 예제 README 2곳 + `src/vmkis/types.py` 1곳을 고쳤고, 검사 5개를
넣었습니다. 노트북과 `docs/` 32곳은 범위를 넘겨 별도 이슈로 냈습니다.

일지: [2026-08-30_11_issue95_examples_config.md](../dev_logs/2026-08-30_11_issue95_examples_config.md)
