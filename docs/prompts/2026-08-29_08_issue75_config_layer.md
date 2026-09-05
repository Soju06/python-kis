# 2026-08-29 - #75 설정 계층 구현

## 사용자 요청

> 1. #75 착수

## 분석

스키마는 [CONFIG_SCHEMA.md](../guidelines/CONFIG_SCHEMA.md) 에 확정돼 있습니다.
여기서는 **구현 배치**만 정합니다.

### 새 모듈을 만듭니다

`helpers.py` 는 "초보자용 설정 헬퍼"입니다. 새 스키마는 3블록 파싱 + 규칙 9개 +
토큰 경로 해석 + 엔드포인트 해석이라 helpers 에 넣으면 그 성격이 사라집니다.

`src/vmkis/config.py` 를 만들고 `helpers.create_client` 가 그것을 씁니다.
import-linter 계약 2개(`utils` 상위 금지, `client -> api` 금지)에 걸리지 않습니다.

### `user_agent` / `endpoints` 배선까지 합니다

`VmKis.__init__` 은 `@overload` 5개(`kis.py:103,148,207,249,302`) + 실구현
1개(`kis.py:359`) 라 인자 2개 추가가 시그니처 6곳을 건드립니다. #70 이 곧 같은
시그니처를 다시 쓸 예정이라 미루고 싶은 유혹이 있지만, **파싱만 하고 안 읽는
키를 내보내는 것**은 CONFIG_SCHEMA.md 가 스스로 금지한 것입니다.

> 설정 항목을 추가할 때는 "이 라이브러리가 그 값으로 무엇을 하는가"에 답해야 합니다.

배선 지점은 3곳입니다.

```text
kis.py:463                  session.headers.update({"User-Agent": USER_AGENT})
kis.py:602                  urljoin(REAL_DOMAIN if domain == "real" else VIRTUAL_DOMAIN, path)
client/websocket.py:374     WEBSOCKET_VIRTUAL_DOMAIN if self.virtual else WEBSOCKET_REAL_DOMAIN
```

웹소켓은 `KisWebsocketClient.kis: "VmKis"` 로 이미 객체를 들고 있어 새 배선이
필요 없습니다.

### `KisAuth` 는 쪼개지 않습니다

필드 5개(`id`,`appkey`,`secretkey`,`account`,`virtual`)뿐이라 새 스키마와 1:1 이
아닙니다. 설정 계층이 **번역**합니다.

```text
apps.<app>.hts_id                     -> KisAuth.id
apps.<app>.app_key / app_secret       -> KisAuth.appkey / secretkey
accounts.<acct>.account_no + product_code -> KisAuth.account  ("00000000-01")
apps.<app>.mode == "paper"            -> KisAuth.virtual
```

### 하위 호환 없음

`load_config` 와 `_validate_profile`(#69)을 **삭제**합니다. 별칭도 경고도 두지
않습니다. 옛 파일은 `version` 키가 없어 R1 에서 걸립니다.

## 계획

1. `src/vmkis/config.py` — 3블록 파싱, R1~R9, 토큰/엔드포인트/UA 해석
2. `helpers.py` — `create_client` 를 새 계층 위로. `load_config`/`_validate_profile` 제거
3. `VmKis` — `user_agent` / `endpoints` 인자 (시그니처 6곳) + 배선 3곳
4. `template_account_profiles.yaml` 신설, `config.example*.yaml` 3개 삭제
5. `.gitignore` — `configs/`
6. 예제 4개, `docs/user/`
7. 테스트 — R1~R9 각각. **되돌려 확인**

## 결과

계획 7단계를 전부 수행했습니다. 작업 중 사용자 지시로 두 가지가 바뀌었습니다.

| 지시 | 반영 |
|---|---|
| 템플릿을 `configs/` 안에 두면? | 옮겼습니다. **토큰 안전성 때문에** 그게 맞습니다 (아래) |
| 앱·계좌 이름에 `app_`/`acc_` 접두사 | 적용. 두 이름공간이 눈으로 구분됩니다 |

### 템플릿 위치가 스타일 문제가 아니었습니다

루트에 두면 사용자가 제자리에서 채웠을 때 토큰이 `./token/`(저장소 루트)에
떨어지고 **그건 `.gitignore` 에 없습니다.** `configs/` 안에 두면 `configs/token/`
으로 가서 자동으로 무시됩니다.

그 과정에서 `.gitignore` 동작 하나를 실측했습니다 — `configs/` 로 디렉터리째
제외하면 git 이 안으로 내려가지 않아 `!` 예외가 통하지 않습니다. `configs/*`
여야 합니다.

### 계획에 없던 발견

영문 문서가 **한 번도 맞은 적이 없는 API** 를 적고 있었습니다
(`VmKis(app_key=, app_secret=, account_number=, server=)` — 네 인자 모두 없음).
설정에 직결된 곳은 정정했고 나머지는
[#78](https://github.com/visualmoney/vm-stock-kis/issues/78) 로 남겼습니다.

```console
uv run pytest -m 'not requires_api'    1088 passed, 8 skipped
coverage                               91.79% (게이트 90), config.py 100%
되돌려 확인                            R2·R6·R9 무력화 시 7건 실패
```

상세는 [개발 일지](../dev_logs/2026-08-29_08_issue75_config_layer.md).
