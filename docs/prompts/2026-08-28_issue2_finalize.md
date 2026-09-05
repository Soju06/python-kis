# 2026-08-28 - Issue #2 마무리 (뉴스레터 기록물 분리 + 죽은 링크 정정)

## 사용자 요청

> <https://github.com/visualmoney/vm-stock-kis/issues/2>, 이슈 2번 진행 승인,
> read @CLAUDE.md

작업 중 추가로 받은 지시:

> root에 archive 폴더 생성하고 archive/docs 폴더 생성 허용

> new_letter 관련 처리 archive폴더 docs 또는 src scripts 등 python file 보관용

확인받은 결정:

| 항목 | 결정 |
|---|---|
| `docs/NEWSLETTER_TEMPLATE.md` | 기록물로 분리 + 서식 신설 |
| 보관 위치 | 저장소 루트 `archive/`, 종류별 하위 폴더 (`docs`/`src`/`scripts`) |
| 커밋 6 (`v3.0.0` 태그 + PyPI 배포) | **이번 세션 범위 밖.** 저장소 정리까지만 |

## 착수 시점 실측

이슈 본문은 착수 전 조사 기준이고, 그 뒤 PR #4·#6·#8·#9·#10·#11 이 머지됐다.
실제 상태를 먼저 확인했다.

| 이슈의 항목 | 실제 |
|---|---|
| 커밋 1~5 | ✅ 완료 (PR #4·#6·#8) |
| GitHub Environment `pypi` / `testpypi` | ✅ 둘 다 존재 |
| TestPyPI `v3.0.0rc1` 선행 업로드 | ✅ 업로드됨, publish 잡 success |
| `__author__` 업스트림 잔존 | ✅ PR #11에서 배포 메타데이터 파생으로 해결 |
| `MIGRATION_GUIDE.md`의 v2.x 표기 소실 | ✅ 커밋 4에서 복원 |
| PyPI `vm-stock-kis` | 아직 404 (미배포) |
| 커밋 6 `v3.0.0` 태그 | ❌ 미실행 |
| `docs/NEWSLETTER_TEMPLATE.md` | ❌ 옛 이름 잔존 — 이번 작업 대상 |

## 분석

- **작업 범위**: 문서 + 린트/빌드 제외 설정. 라이브러리 코드 변경 없음
- **영향 받는 모듈**: 없음 (`src/vmkis/**` 무변경)
- **예상 시간**: 1시간

## 계획

1. `docs/NEWSLETTER_TEMPLATE.md` → `archive/docs/2025-12_NEWSLETTER.md` 로 분리,
   맨 위에 동결 안내 추가
2. 같은 자리에 실제 빈 서식을 새로 작성 (`vmkis`/`VmKis` 기준)
3. `archive/README.md` — 보관 기준·구조·규칙 명문화
4. `archive/` 를 markdownlint·ruff 제외 경로에 추가
5. 완료 기준 grep 재실행 중 발견되는 잔재 정리
6. 전체 검증 → 개발 일지 → 커밋 → PR

## 결과

완료. 상세는 [개발 일지](../dev_logs/2026-08-28_issue2_finalize.md) 참조.

계획에 없었으나 5번에서 **존재하지 않는 저장소를 가리키는 링크 19곳**을
발견해 함께 고쳤다 (`QuantumOmega` 7곳, `yourusername` 12곳).

커밋 6은 사용자 결정에 따라 남겨 둔다.
