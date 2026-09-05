# 2026-08-27 - Issue #2 이름 변경 및 src 레이아웃 전환

## 사용자 요청

> 작업 시작 승인, #3 이후 커밋 하고 #2 작업 진행

이후 확인한 결정 사항:

* 산문 브랜딩 `Python-KIS` → **`VM-Stock-KIS`**
* 이번 세션 범위: **커밋 1~2** (이름 변경 + src 레이아웃, 패키징)

대상 이슈: [visualmoney/vm-stock-kis#2](https://github.com/visualmoney/vm-stock-kis/issues/2)

## 착수 시점 실측 — 이슈 본문 이후 이미 끝난 항목

이슈 본문은 uv 전환 PR(#4) 이전에 작성되었다. 착수 전 실제 상태를 확인한 결과
아래 항목은 이미 완료되어 있었다.

| 항목 | 이슈 본문 | 실제 |
|---|---|---|
| 빌드 백엔드 | Poetry | ✅ 이미 uv + hatchling + hatch-vcs |
| `requires-python` | `>=3.10` / `^3.11` 혼재 | ✅ 이미 `>=3.10`으로 통일 |
| `[project.urls]` `"Original Project"` | 없음 | ✅ 이미 있음 |
| `authors` TOML 구문 오류 | 파싱 불가 | ✅ 이미 복구 |
| `py.typed` | 없음 | ✅ 이미 있음 |
| `.coveragerc` / `poetry.lock` | 삭제 필요 | ✅ 이미 삭제 |
| git 태그 | 하나도 없음 | ✅ `v2.1.6` 존재 |
| `.pre-commit-config.yaml` 중복 | black·isort 중복 | ✅ 이슈 #3에서 정리 |

따라서 남은 핵심은 **이름 변경 + src 레이아웃 + 그에 딸린 패키징 경로**였다.

## 미완료였던 항목

* flat 레이아웃 (`pykis/`)
* 배포명 `python-kis`, 모듈명 `pykis`, 클래스명 `PyKis`
* `__env__.py`의 `__url__` 업스트림 잔존, `except Exception`, `"2.1.6+dev"` 하드코딩
* `.python-version`, `CHANGELOG.md`, `dependabot.yml` 부재

## 계획

1. `git mv pykis src/vmkis`
2. 이슈가 제시한 sed 스윕 (업스트림 URL sentinel 보호)
3. 스윕이 놓치는 지점 수동 수정
4. 호환 shim 3종 + 테스트
5. 패키징 경로 갱신, 재검증

## 결과

완료. 상세는 [개발 일지](../dev_logs/2026-08-27_issue2_rename_vmkis.md) 참조.

```text
959 passed, 8 skipped, 17 deselected — Python 3.10 / 3.13
Total coverage 90.67% (게이트 90)
```
