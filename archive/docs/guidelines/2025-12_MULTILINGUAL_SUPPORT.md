> **동결 — 2025-12 에 쓴 다국어 지원 정책입니다.** 원래 자리는
> `docs/guidelines/MULTILINGUAL_SUPPORT.md` 였습니다.
>
> **이 문서가 있는 동안 드리프트가 났습니다.** 356줄로 번역 유지 절차를 적어
> 두었지만 `#87` 은 영문에 들어가지 않았고, `#70` 의 개명도 영문 FAQ 에
> 오지 않았습니다. **정책 문서는 검사가 아닙니다.**
>
> `#104` 에서 영문을 `docs/user/en/README.md` 한 장으로 줄이기로 정했습니다.
> 유지 대상이 1개면 이 정책이 규율할 것이 없습니다. 영문을 다시 늘릴 때는
> 이 문서를 되살리지 말고 **그때의 단계에 맞는 규칙을 새로 정하세요.**
>
> 지금 무엇을 볼 것인가 —
> [`docs/user/en/README.md`](../../../docs/user/en/README.md) 와 `#104` 의 결정.
> 보관 기준은 [`archive/README.md`](../../README.md) 를 보세요.
> 근거: [`#104`](https://github.com/visualmoney/vm-stock-kis/issues/104)

# 다국어 지원 가이드라인 (MULTILINGUAL_SUPPORT.md)

**작성일**: 2025-12-20
**대상**: 개발자, 번역가, 커뮤니티 관리자
**버전**: v1.0

---

## 목표

VM-Stock-KIS 프로젝트를 **한국어**와 **영어**를 중심으로 다국어 지원하여, 글로벌 사용자가 쉽게 접근할 수 있도록 합니다.

---

## 1. 다국어 지원 정책

### 1.1 지원 언어 우선순위

| 언어 | 우선순위 | 지원 범위 | 관리자 |
|------|---------|---------|--------|
| **한국어 (Ko)** | 🔴 1순위 | 전체 문서, 실시간 지원 | 주 개발자 |
| **영어 (En)** | 🔴 1순위 | 주요 문서, 이슈/토론 | 번역가 |
| **중국어 (Zh)** | 🟡 2순위 | 문서 (선택), 이슈만 | 커뮤니티 |
| **일본어 (Ja)** | 🟡 2순위 | 문서 (선택), 이슈만 | 커뮤니티 |

### 1.2 문서 범주별 지원

| 문서 | 한국어 | 영어 | 기타 | 필수 여부 |
|------|-------|------|------|----------|
| **README** | ✅ | ✅ | ⚠️ | 필수 |
| **QUICKSTART** | ✅ | ✅ | ⚠️ | 필수 |
| **API Reference** | ✅ | ✅ | ❌ | 필수 |
| **FAQ** | ✅ | ✅ | ❌ | 필수 |
| **CONTRIBUTING** | ✅ | ✅ | ❌ | 필수 |
| **튜토리얼** | ✅ | ✅ | ❌ | 필수 |
| **블로그** | ✅ | ⚠️ | ❌ | 선택 |
| **비디오** | ✅ (자막) | ✅ (자막) | ❌ | 선택 |

---

## 2. 문서 구조

### 2.1 폴더 구조

```text
docs/
├── user/
│   ├── README.md                     # 한국어 목차 (링크 제공)
│   ├── ko/
│   │   ├── README.md                 # 한국어 소개
│   │   ├── QUICKSTART.md             # 빠른 시작
│   │   ├── INSTALLATION.md           # 설치 가이드
│   │   ├── CONFIGURATION.md          # 설정 방법
│   │   ├── TUTORIALS.md              # 튜토리얼 목차
│   │   ├── FAQ.md                    # 자주 묻는 질문
│   │   └── TROUBLESHOOTING.md        # 문제 해결
│   │
│   └── en/
│       ├── README.md                 # English introduction
│       ├── QUICKSTART.md             # Quick start guide
│       ├── INSTALLATION.md           # Installation guide
│       ├── CONFIGURATION.md          # Configuration guide
│       ├── TUTORIALS.md              # Tutorials index
│       ├── FAQ.md                    # Frequently asked questions
│       └── TROUBLESHOOTING.md        # Troubleshooting
│
├── guidelines/
│   ├── MULTILINGUAL_SUPPORT.md       # 이 문서
│   ├── REGIONAL_GUIDES.md            # 지역별 가이드
│   ├── TRANSLATION_RULES.md          # 번역 규칙
│   └── GLOSSARY_KO_EN.md             # 용어사전
```

### 2.2 루트 README 네비게이션

**`README.md` 상단에 언어 선택 추가**:

```markdown
# VM-Stock-KIS 한국투자증권 API 라이브러리

**언어 선택 / Language**:
- 🇰🇷 [한국어](./docs/user/ko/README.md)
- 🇬🇧 [English](./docs/user/en/README.md)

---

[기존 내용]
```

---

## 3. 번역 규칙

### 3.1 기본 원칙

| 원칙 | 설명 |
|------|------|
| **정확성** | 기술 용어 정확히 번역 (오역 방지) |
| **일관성** | 용어사전 준수 (같은 단어는 같게) |
| **가독성** | 자연스러운 문체 (기술 정확성 우선) |
| **최신성** | 원본 문서와 동기화 유지 |

### 3.2 번역 금지 항목

다음 항목은 **절대 번역하지 않음**:

```text
❌ 번역 금지:
- 함수명, 클래스명, 변수명
- 파일 경로 (Python import 포함)
- URL 링크
- 코드 예제의 주석 (영문 유지 가능)
- API 응답 JSON 키

✅ 번역 가능:
- 설명/설명 텍스트
- 주석의 설명 부분
- UI 텍스트 및 가이드
```

### 3.3 기술 용어 번역 (용어사전)

**다음 용어사전 준수**:

```text
# 용어사전 예시

Authentication → 인증 (❌ 보증, 증명)
Authorization → 인가 (❌ 승인)
Rate Limit → 요청 제한 (❌ 속도 제한)
Retry → 재시도 (❌ 재반복)
Timeout → 타임아웃 (❌ 시간 초과)
Subscription → 구독 (❌ 신청)
Quote → 시세 (❌ 견적, 인용)
Orderbook → 호가창 (❌ 주문 책)
Balance → 잔고 (❌ 잔액, 균형)
Position → 보유 (❌ 위치, 포지션)
Margin → 증거금 (❌ 여백, 마진)
Liquidation → 청산 (❌ 청소, 유동화)
Dividend → 배당금 (❌ 배당)
Split → 액면분할 (❌ 분할)
```

---

## 4. 번역 프로세스

### 4.1 번역 체크리스트

```text
[ ] 1. 최신 원본 문서 확인
[ ] 2. 용어사전 검토
[ ] 3. 초안 작성 (문단별)
[ ] 4. 자체 검토 (맞춤법, 기술 정확성)
[ ] 5. 동료 검토 요청 (GitHub PR)
[ ] 6. 최종 검증 (링크, 코드 예제)
[ ] 7. 병합 및 배포
```

### 4.2 번역 품질 기준

| 등급 | 기준 | 승인자 |
|------|------|--------|
| **A (우수)** | 0-2개 오타, 100% 이해도 | 1명 검토 가능 |
| **B (양호)** | 3-5개 오타, 95% 이해도 | 2명 검토 필요 |
| **C (수용)** | 6-10개 오타, 90% 이해도 | 재번역 권고 |
| **D (부적격)** | 10개+, 85% 미만 | 반려 및 재작성 |

### 4.3 번역 주기

| 문서 | 검토 주기 | 업데이트 주기 |
|------|---------|-------------|
| **필수 문서** | 2주 | 즉시 (원본 변경 시) |
| **튜토리얼** | 1개월 | 1개월 |
| **가이드** | 3개월 | 3개월 |
| **블로그** | 반기 | 반기 |

---

## 5. 자동 번역 CI/CD 설정 (선택사항)

### 5.1 번역 자동화 도구

```bash
# 옵션 1: GitHub Actions + Google Translate API
# 옵션 2: Crowdin (커뮤니티 번역 플랫폼)
# 옵션 3: Manual PR (추천: 품질 보증)
```

### 5.2 GitHub Actions 워크플로우 (향후)

```yaml
# .github/workflows/auto-translate.yml
name: Auto-translate on push

on:
  push:
    paths:
      - 'docs/user/ko/**'

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Translate KO → EN
        run: |
          # Google Translate API 호출
          # 자동 번역 생성
          # docs/user/en/ 업데이트
      - name: Create PR
        uses: peter-evans/create-pull-request@v4
```

---

## 6. 번역 검증 체크리스트

### 번역 문서 검증

```markdown
# 번역 검증 체크리스트 (PR 코멘트에 추가)

## 형식
- [ ] 마크다운 형식 올바름
- [ ] 코드 블록 포함 확인
- [ ] 링크 유효성 검사 (모든 상대 경로)
- [ ] 이미지 경로 정확함

## 언어
- [ ] 기술 용어 정확 (용어사전 준수)
- [ ] 맞춤법 검사 완료
- [ ] 문법 검사 완료
- [ ] 가독성 검증 (누군가에게 읽어주기)

## 내용
- [ ] 코드 예제 실행 가능 여부 확인
- [ ] 스크린샷/다이어그램 최신성
- [ ] 외부 링크 유효성 (문서 내)
- [ ] 버전 정보 일치

## 원본 동기화
- [ ] 원본 문서와 동일한 구조
- [ ] 원본과 같은 예제 포함
- [ ] 원본 최신 버전 반영
```

---

## 7. 커뮤니티 참여

### 7.1 번역 기여자 모집

```markdown
# 번역자 모집 (README 하단)

**번역 기여자 찾습니다!**

- 🇬🇧 English translations (진행 중)
- 🇨🇳 中文 (Chinese)
- 🇯🇵 日本語 (Japanese)

관심 있으신 분은 이슈를 열어주세요: [번역 기여 가이드](./CONTRIBUTING.md)
```

### 7.2 번역 보상 (선택사항)

```text
- 커뮤니티 인정 (CONTRIBUTORS.md 등재)
- 번역 완료 배지
- 월간 뉴스레터 기여 인정
```

---

## 8. 유지보수 전략

### 8.1 원본 변경 시 프로세스

```text
1. 한국어 문서 수정 (ko/)
2. 영어 문서 수정 (en/)
3. 버전 업데이트
4. CHANGELOG 기록
5. 번역자에게 알림 (향후 언어 추가 시)
```

### 8.2 번역 동기화 자동 알림

```bash
# 스크립트: scripts/check_translation_sync.py

import os

ko_files = set(os.listdir('docs/user/ko/'))
en_files = set(os.listdir('docs/user/en/'))

missing_en = ko_files - en_files
missing_ko = en_files - ko_files

if missing_en:
    print(f"⚠️ 영문 누락: {missing_en}")
if missing_ko:
    print(f"⚠️ 한글 누락: {missing_ko}")
```

---

## 9. 언어별 특수 사항

### 9.1 한국어 특수 사항

```markdown
# 주의사항
- 종성 처리 (을/를, 이/가 구분)
- 존댓말 사용 (사용자 친화적)
- 한자 금지 (순한글 권장)
- 시간 형식: HH:MM (24시간 형식)
```

### 9.2 영어 특수 사항

```markdown
# Guidelines
- American English 사용 (color vs colour)
- 첫 글자 대문자 (Title Case for headings)
- 단수/복수 구분 철저
- Time format: 12-hour or 24-hour (명시)
```

---

## 10. 성공 지표

| 지표 | 목표 | 검증 방법 |
|------|------|----------|
| **한국어 커버리지** | 100% | 필수 문서 완성도 |
| **영어 커버리지** | 100% | 필수 문서 완성도 |
| **번역 품질** | A등급 80%+ | 품질 검토 |
| **번역 동기화** | 100% | 자동 스크립트 |
| **커뮤니티 만족도** | 4.0/5.0+ | 설문조사 (분기별) |

---

## 참고 자료

- [CONTRIBUTING.md](../../CONTRIBUTING.md) - 기여 가이드
- [GLOSSARY_KO_EN.md](./GLOSSARY_KO_EN.md) - 용어사전
- [REGIONAL_GUIDES.md](./REGIONAL_GUIDES.md) - 지역별 가이드
- [Google Translate Style Guide](https://support.google.com/translate/)

---

**마지막 업데이트**: 2025-12-20
**검토 주기**: 분기별 (Q1, Q2, Q3, Q4)
**다음 검토**: Phase 4 Week 3
