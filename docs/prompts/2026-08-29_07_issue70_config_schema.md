# 2026-08-29 - #70 착수 + 새 설정 스키마 검토

## 사용자 요청

> #70에서 blocked 제거, #70 착수, 1. 사용자가 config.example.yaml 수정함.
> configs 폴더 생성하여 여기에 보관하는 것을 검토 token 값 은 configs/token 폴더에
> 보관을 기본값 (사용자가 config 파일 위치 지정 가능) 파일명은
> template_account_profiles.yaml 로 변경 검토 중.

`blocked` 는 #69 머지 시점에 이미 제거했습니다.

## 분석

사용자가 `config.example*.yaml` 3개를 **직접 수정**했습니다 (작업 트리 미커밋).
키 이름 변경이 아니라 **스키마 전면 재설계**입니다.

```text
config_version: 1
broker_env_<슬러그>:   live|paper|etc → base_url / ws_url / broker_id / user_agent
apps:                  자격증명 + mode + hts_id + token_path   (토큰 발급 단위)
accounts:              app 참조 + account_no + product_code + label  (원장 단위)
```

### 이것은 #70 이 아닙니다

이슈 #70 의 범위는 *"`real`/`virtual` → `live`/`paper` 개명 + 불리언 → `mode` enum"*
입니다. 새 스키마는 **다중 브로커 · 앱/계좌 분리 · 엔드포인트 주입 · 환경변수
간접 참조**를 도입합니다. 라이브러리에 **대응 개념이 없습니다.**

| 스키마가 요구하는 것 | 라이브러리 현재 |
|---|---|
| `broker_env_*.base_url` / `ws_url` | **하드코딩 상수** — `src/vmkis/__env__.py:10-14`. 주입 지점이 없습니다 (`kis.py:602`, `websocket.py:374` 가 `if virtual else` 로 고름) |
| `apps` / `accounts` 분리 | `KisAuth` 는 필드 5개 (`id`,`appkey`,`secretkey`,`account`,`virtual`). 앱 개념 없음 |
| `broker: "kis"` | 브로커 개념 자체가 없음 (KIS 전용 라이브러리) |
| `token_path` (앱별) | 기본 `~/.vmkis/` + 해시 파일명 (`kis.py:118`, `_get_hashed_token_name`) |
| `app_key_env` 간접 참조 | 없음 |

즉 **설정 파일 재설계가 아니라 새 설정 계층 + `VmKis`/`KisAuth`/도메인 해석/토큰
저장 변경**입니다.

### 초안에서 발견한 결함

1. **`config.example.real.yaml` 이 자기 규칙을 어깁니다.**
   `default_account: "kis_paper_1"` 인데 그 파일에는 `kis_paper_1` 계좌 블록이
   없습니다(`kis_live_1` 만 정의). 파일 자신이 *"🔴 필수 — 계좌 블록 중 하나를
   지정"* 이라 적어 둔 규칙 위반입니다. 스키마가 자랑하는 R29 참조 무결성이
   **잡아야 할 바로 그 종류**를 배포 템플릿이 갖고 있습니다.

2. **`VMKIS_PROFILE` 이 가리킬 대상이 없어졌습니다.**
   머리말은 여전히 *"`VMKIS_PROFILE` 로 프로필 선택"*, *"`--profile <name>`"* 이라
   적혀 있는데 새 스키마에 프로필이 없습니다. 선택 축이 `accounts.default_account`
   로 바뀌었습니다. 둘 중 하나는 거짓말입니다.

3. **`token_path` 의 기준 경로가 정의되지 않았습니다.**
   `"token/token_kis_live_1.json"` 는 상대 경로입니다. cwd 기준이면 **다른
   디렉터리에서 실행할 때마다 새 토큰 파일**이 생겨 매번 재발급하거나, 엉뚱한
   곳에 토큰이 쌓입니다. 설정 파일 기준이어야 사용자가 말한
   `configs/token/` 기본값이 성립합니다.

4. **`user_agent` 값에 따옴표가 이중입니다.**
   `config.example.real.yaml`:
   `user_agent: "'Mozilla/5.0 ... Safari/537.36'"` — YAML 이 **작은따옴표를 값에
   포함**시킵니다. 헤더에 `'Mozilla...'` 가 그대로 실려 나갑니다.

5. **`accounts` 가 스칼라 키와 블록을 한 매핑에 섞었습니다.**
   `default_account` 가 계좌 블록들과 같은 레벨이라 `default_account` 라는 이름의
   계좌를 만들 수 없고, 검증기가 이 키만 특례 처리해야 합니다.

6. **스펙 문서가 저장소에 없습니다.**
   주석이 *"스펙 §5.2 R7"*, *"§8.4 R29"* 를 인용하는데
   `git grep -rln 'R29|§8.4|broker_env_|account_profiles' -- docs/ archive/` 가
   **0건**입니다. 규칙이 설정 파일 주석에만 존재하고, 주석은 강제되지 않습니다.

## 계획

방향 확정 전까지 코드를 쓰지 않습니다. 결정이 필요한 것:

1. #70 을 **쪼갤 것인가** — 코드 쪽 개명(스키마와 무관하게 살아남음)과
   설정 스키마(새 이슈)로
2. 스펙 문서를 저장소에 들일 것인가
3. 위 결함 1~5 의 처리

## 결과

사용자 결정 4건:

| 질문 | 결정 |
|---|---|
| #70 범위 | **코드/설정 분리** — #70 은 코드 개명만, 스키마는 #75 |
| 스펙 문서 | 원본 경로를 받아 참고하되, **저장소에는 새로 최대한 단순하게** 작성 |
| 파일 배치 | `configs/`, 토큰 기본 `configs/token/`, `template_account_profiles.yaml` |
| 하위 호환 | **무시.** 별칭·경고·변환 스크립트를 넣지 않습니다 |

받은 원본은 운용 시스템(1033줄, v2.7)의 설정 스펙이었고, 그 복잡도는 **이
저장소에 없는 이유들**에서 나온 것이었습니다 — 레거시 vendor 브리지, 가구 단위
자금 배분, 다중 브로커. 대부분 옮기지 않고 3블록으로 줄였습니다.

> 사용자 추가 지시로 **참조 원본 문구는 삭제·축약**했습니다. 외부 프로젝트의
> 경로와 내부 구조가 공개 저장소 문서에 남을 이유가 없습니다.

### 산출물

| | |
|---|---|
| `docs/guidelines/CONFIG_SCHEMA.md` | 새 스키마 — 3블록, 검증 규칙 R1~R8, 토큰 경로 |
| [#75](https://github.com/visualmoney/vm-stock-kis/issues/75) | 구현 이슈. 초안 결함 5건을 전부 반영해 고침 |
| [#70](https://github.com/visualmoney/vm-stock-kis/issues/70) | 코드 개명으로 범위 축소, 제목도 변경 |
| [`draft/config-schema-v2`](https://github.com/visualmoney/vm-stock-kis/tree/draft/config-schema-v2) | 사용자 초안 보존 (main 미반영) |

초안을 브랜치로 뺀 이유는 #70 의 코드 개명이 `virtual` 을 369곳 건드리기 때문입니다.
확정되지 않은 스키마가 작업 트리에 떠 있으면 섞입니다.

### 설계에서 바꾼 것 하나

초안은 `token_path` 를 앱마다 적게 하고 *"⚠️ 앱키별로 다르게 지정해야 한다"* 라고
경고했습니다. **사용자가 지켜야 하는 불변식은 사용자가 안 지킵니다.** 두 앱이 같은
경로를 가리켜도 아무도 못 막고, 증상은 "가끔 인증이 풀린다"로 나타납니다.
`token/<app>.json` 으로 파생시켜 충돌을 구조적으로 불가능하게 했습니다.
