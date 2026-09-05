# 문서 인덱스

**최종 업데이트**: 2026-09-05

이 저장소의 문서 목록입니다. **여기 적힌 경로는 전부 실재합니다** —
새 문서를 만들거나 옮기면 이 파일도 함께 고쳐 주세요.

> 이 파일은 2026-08-28에 다시 썼습니다. 그전에는 링크 28곳이 **작성자 PC의
> 절대경로**(그것도 포크 이전 디렉터리명)를 가리켜 GitHub 에서 전부 죽어
> 있었고, 디렉터리 트리 블록도 깨져 있었습니다
> ([#29](https://github.com/visualmoney/vm-stock-kis/issues/29)).

---

## 처음 오셨다면

| 문서 | 내용 |
|---|---|
| [README](../README.md) | 프로젝트 소개, 설치, 튜토리얼 링크 |
| [QUICKSTART](../QUICKSTART.md) | 설치부터 첫 조회까지 |
| [FAQ](FAQ.md) | 자주 묻는 질문 |
| [SIMPLEKIS_GUIDE](SIMPLEKIS_GUIDE.md) | 초보자용 간소화 인터페이스 |

## 사용자 문서

| 문서 | 내용 |
|---|---|
| [user/USER_GUIDE](user/USER_GUIDE.md) | 기능별 사용법 |
| [user/EXTENDING_API](user/EXTENDING_API.md) | **미지원 TR 을 `fetch()` 로 호출하기.** 이 라이브러리는 주식 현물만 구현합니다 |
| [MIGRATION_GUIDE](MIGRATION_GUIDE.md) | `python-kis` 2.x → `vm-stock-kis` 0.0.1 이름 변경 대응 |
| [../CHANGELOG](../CHANGELOG.md) | 변경 이력 |
| [../SECURITY](../SECURITY.md) ([English](../SECURITY.en.md)) | 자격증명 취급 방식, 취약점 신고 |

### English

| 문서 | 내용 |
|---|---|
| [user/en/README](user/en/README.md) | 영문 문서는 **이 한 장뿐**입니다 |
| [../SECURITY.en](../SECURITY.en.md) | 자격증명 취급 방식, 취약점 신고 |

> **영문 user guide 분기는 닫혀 있습니다**([#104](https://github.com/visualmoney/vm-stock-kis/issues/104)).
> 번역본이 원본을 못 따라와 틀린 안내를 하고 있었기 때문입니다 — 옛 영문
> QUICKSTART 는 `#87` 의 실전 앱 요건이 없었고, 옛 영문 FAQ 는 `#70` 이 없앤
> 이름을 가르쳤습니다. **아무도 갱신하지 않는 번역은 번역이 없는 것보다
> 나쁩니다.** 다시 늘릴 때의 **범위**는 `#104` 에 단계로 적어 두었습니다 —
> **조건은 없습니다. 옮길지는 그때 판단합니다.**

## 개발자 문서

| 문서 | 내용 |
|---|---|
| [architecture/ARCHITECTURE](architecture/ARCHITECTURE.md) | 허브-스포크 **만** 모듈 구조. 얇은 파사드 · `fetch()`. **불변식** |
| [generated/API_REFERENCE](generated/API_REFERENCE.md) | 공개 모듈 docstring 덤프. 손으로 고치지 말고 `uv run python scripts/generate_api_reference.py` |
| [developer/DEVELOPER_GUIDE](developer/DEVELOPER_GUIDE.md) | 개발 환경, 코드 구조 |
| [developer/VERSIONING](developer/VERSIONING.md) | git 태그 기반 버저닝, **태그 표기 규칙** |
| [../CONTRIBUTING](../CONTRIBUTING.md) | 기여 절차, 브랜치·커밋 관례 |
| [../AGENTS](../AGENTS.md) | 에이전트 불변식 (Cursor). 세부는 `.cursor/rules/`, `.cursor/skills/` |

## 규칙 및 가이드라인 (`guidelines/`)

| 문서 | 내용 |
|---|---|
| [API_STABILITY_POLICY](guidelines/API_STABILITY_POLICY.md) | 버전 정책, 호환성 보장 범위, Deprecation 절차 |
| [CONFIG_SCHEMA](guidelines/CONFIG_SCHEMA.md) | 설정 파일 구조와 검증 규칙 |
| [PYPI_RELEASE](guidelines/PYPI_RELEASE.md) | 배포 준비와 절차 |
| [DEVELOPER_SETUP](guidelines/DEVELOPER_SETUP.md) | 개발 환경 구축 |
| [GUIDELINES_001_TEST_WRITING](guidelines/GUIDELINES_001_TEST_WRITING.md) | 테스트 작성 표준 |
| [AGENT_WORKFLOW_RULES](guidelines/AGENT_WORKFLOW_RULES.md) | AI 에이전트 작업 규칙 |
| [REGIONAL_GUIDES](guidelines/REGIONAL_GUIDES.md) | 지역별 설정 |
| [PLANTUML_SETUP](guidelines/PLANTUML_SETUP.md) | 다이어그램 도구 |

## 기록물 — 당시 상태로 동결

**아래는 갱신하지 않습니다.** 옛 이름(`pykis` / `PyKis`)과 죽은 링크가 남아
있어도 그대로 둡니다. 그것이 당시 서술입니다.

| 위치 | 내용 |
|---|---|
| [`dev_logs/`](dev_logs/) | 개발 일지 (날짜별) |
| [`prompts/`](prompts/) | 사용자 요청 원본 |
| [`reports/`](reports/) | 분석·완료 보고서 |
| [`reports/archive/`](reports/archive/) | 대체된 옛 보고서 |
| [`../archive/`](../archive/README.md) | 저장소 루트의 동결 보관소 — 보관 기준은 여기 |

**Discussions 는 쓰지 않습니다.** 2025-12-20 에 켠 뒤 8개월간 게시물이 자동
생성 환영글 1건뿐이어서 2026-08-28 에 껐습니다. 설정 가이드는
[`../archive/docs/guidelines/2025-12-20_GITHUB_DISCUSSIONS_SETUP.md`](../archive/docs/guidelines/2025-12-20_GITHUB_DISCUSSIONS_SETUP.md)
에 있습니다. **창구는 GitHub Issues 하나입니다.**

### 읽을 만한 최신 보고서

| 문서 | 내용 |
|---|---|
| [reports/2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR](reports/2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR.md) | 공식 샘플과의 비교. API 커버리지 격차, 확장 전략 |
| [reports/2026-08-30_DOCS_AUDIT](reports/2026-08-30_DOCS_AUDIT.md) | 마크다운 전수 조사. `#108` 문서 정리군의 근거 |
| [reports/2026-08-30_EN_DOCS_STAGES](reports/2026-08-30_EN_DOCS_STAGES.md) | 영문 문서를 다시 늘릴 때의 **단계별 범위**. 조건은 없습니다 |
| [reports/2026-09-05_WIKI_TOC](reports/2026-09-05_WIKI_TOC.md) | Wiki Tutorial 상세 목차. **포인터 유지** (`#145`) |
| [reports/2026-09-05_ARCHITECTURE_REVIEW](reports/2026-09-05_ARCHITECTURE_REVIEW.md) | 아키텍트 검토. 구조는 유지, 문서를 한 그림으로 |
| [reports/2026-09-05_V030_TO_V100_REVIEW](reports/2026-09-05_V030_TO_V100_REVIEW.md) | v0.3.0→v1.0.0 전. SimpleKIS 예제 보류, P0–P2 |

## 그 밖에

| 문서 | 내용 |
|---|---|
| [NEWSLETTER_TEMPLATE](NEWSLETTER_TEMPLATE.md) | 뉴스레터 서식 (빈 양식) |
| [`diagrams/`](diagrams/) | PlantUML 원본과 렌더 결과 |

---

## 현재 값은 문서가 아니라 코드에서

문서와 코드가 어긋나면 **코드가 맞습니다.** 자주 묻는 값의 출처입니다.

| 알고 싶은 것 | 어디서 |
|---|---|
| 버전 | `git describe` / `vmkis.__version__` (git 태그가 유일한 출처) |
| 의존성 하한 | `pyproject.toml` 의 `[project] dependencies` |
| Rate Limit | `src/vmkis/__env__.py` |
| 공개 API 목록 | `vmkis.__all__` |
| 테스트·커버리지 | `uv run pytest -m 'not requires_api and not performance' --cov` |
