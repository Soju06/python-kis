> **동결 — 2025-12-20 시점의 계획 문서입니다.** 원래 자리는
> `docs/guidelines/GITHUB_DISCUSSIONS_SETUP.md` 였습니다.
>
> **Discussions 는 2026-08-28 에 비활성화했습니다.** 이 문서가 지시한 7단계는
> 실행된 적이 없습니다 — 커스텀 카테고리 0개, 핀 Discussion 0개, README 링크
> 0곳. 8개월간 게시물은 GitHub 자동 생성 환영글 1건뿐이었고 댓글은 0이었습니다.
>
> 이 문서의 전제가 지금 저장소와 맞지 않습니다. 대상 버전이 `v2.2.0`/`v2.3.0`
> (현재 `0.0.1`)이고, "1개월 후 토론 20건 · 활성 참여자 10명 · 커뮤니티 리더
> 3~5명 선정"과 "긴급 24시간 내 응답"을 성과 지표로 잡고 있습니다. **1인
> 프로젝트가 지킬 수 없는 약속입니다.**
>
> 지금 무엇을 볼 것인가 — 창구는 GitHub Issues 하나입니다.
> `CONTRIBUTING.md` 와 `.github/ISSUE_TEMPLATE/` 를 보세요.

---

# GitHub Discussions 설정 가이드

**작성일**: 2025-12-20
**상태**: 설정 지침 문서
**목표**: VM-Stock-KIS 커뮤니티 허브 구축

---

## 개요

GitHub Discussions는 VM-Stock-KIS 사용자들이 질문하고, 아이디어를 공유하고, 공지를 받을 수 있는 중앙 커뮤니티 플랫폼입니다.

**장점**:

- ✅ GitHub 계정으로 쉽게 접근
- ✅ 검색 가능한 아카이브
- ✅ 개발자와 사용자 직접 소통
- ✅ 피드백 수집
- ✅ 커뮤니티 리더 선정 가능

---

## 1단계: GitHub Discussions 활성화

### 1.1 저장소 설정

```text
GitHub 저장소 → Settings → General
```

**절차**:

1. 저장소 메인 페이지 → **Settings** 탭 클릭
2. 좌측 메뉴 → **Discussions** 섹션 찾기
3. "Discussions 활성화" 체크박스 선택
4. **Save changes** 클릭

**결과**: 저장소에 Discussions 탭이 나타남 ✅

### 1.2 권한 설정

```text
Settings → Discussions → Permissions
```

**설정**:

```yaml
누가 토론을 시작할 수 있는가:
  - 저장소 권한자 ✅
  - 저장소 트리거 ✅
  - 모든 게스트 ✅

누가 댓글을 달 수 있는가:
  - 저장소 권한자 ✅
  - 저장소 트리거 ✅
  - 모든 게스트 ✅
```

---

## 2단계: Discussion 카테고리 생성

### 2.1 기본 카테고리 (4개)

#### 1️⃣ Announcements (공지사항)

```yaml
이름: Announcements
설명: "새로운 버전 출시, 유지보수 일정, 중요 공지"
이모지: 📢
권한: 저장소 권한자만 게시 가능
범주: Product Announcements
```

**사용 예시**:

- "v2.3.0 출시: 새로운 기능 5개 추가"
- "예정된 유지보수: 12월 25일 18:00~22:00"
- "API 변경 공지: quote() 메서드 개선"

#### 2️⃣ General (일반)

```yaml
이름: General
설명: "일반적인 질문, 토론, 아이디어 공유"
이모지: 💬
권한: 모든 사람이 게시 가능
범주: General
```

**사용 예시**:

- "VM-Stock-KIS를 사용해본 경험 공유합니다"
- "다른 사람들은 이 기능을 어떻게 사용하고 있나요?"
- "거래 알고리즘 구축 팁 공유"

#### 3️⃣ Q&A (질문 & 답변)

```yaml
이름: Q&A
설명: "기술 질문, 버그 리포팅, 문제 해결"
이모지: ❓
권한: 모든 사람이 게시 가능
범주: Help
```

**사용 예시**:

- "quote() 메서드가 None을 반환합니다"
- "초기화할 때 ConnectionError가 발생합니다"
- "환경변수 설정 방법을 모르겠습니다"

#### 4️⃣ Ideas (기능 제안)

```yaml
이름: Ideas
설명: "새로운 기능 제안, 개선 아이디어"
이모지: 💡
권한: 모든 사람이 게시 가능
범주: Feature Request
```

**사용 예시**:

- "실시간 데이터 구독 기능이 필요합니다"
- "CSV 내보내기 기능 추가를 제안합니다"
- "간단한 백테스팅 도구를 추가하면 어떨까요?"

---

## 3단계: Discussion 템플릿 생성

### 3.1 템플릿 파일 생성

경로: `.github/DISCUSSION_TEMPLATE/`

#### Q&A 템플릿: `.github/DISCUSSION_TEMPLATE/question.yml`

```yaml
body:
  - type: markdown
    attributes:
      value: |
        감사합니다! VM-Stock-KIS 커뮤니티에 질문을 제출해주셨습니다.
        다른 사용자들을 도와드릴 수 있도록 최대한 자세하게 설명해주세요.

  - type: textarea
    id: description
    attributes:
      label: "질문 내용"
      description: "어떤 문제가 있나요? 최대한 자세하게 설명해주세요."
      placeholder: |
        예: "quote() 메서드를 호출했을 때 None이 반환됩니다.
        다음과 같이 코드를 작성했습니다..."
      required: true

  - type: textarea
    id: code
    attributes:
      label: "재현 코드"
      description: "문제를 재현할 수 있는 최소한의 코드를 제공해주세요."
      language: python
      placeholder: |
        from vmkis import VmKis
        kis = VmKis()
        quote = kis.stock("005930").quote()
        print(quote)
      required: false

  - type: dropdown
    id: environment
    attributes:
      label: "환경"
      options:
        - "Windows"
        - "macOS"
        - "Linux"
        - "기타"
      required: true

  - type: textarea
    id: context
    attributes:
      label: "추가 정보"
      description: |
        - Python 버전: (예: 3.9)
        - vmkis 버전: (예: 2.2.0)
        - 에러 메시지:
      placeholder: |
        Python 3.11
        vmkis 2.2.0

        에러:
        ...
      required: false

  - type: checkboxes
    id: checklist
    attributes:
      label: "확인 사항"
      options:
        - label: "FAQ를 읽었습니다"
          required: false
        - label: "같은 질문이 없는지 확인했습니다"
          required: false
        - label: "최소한의 재현 코드를 제공했습니다"
          required: false
```

#### Idea 템플릿: `.github/DISCUSSION_TEMPLATE/feature-request.yml`

```yaml
body:
  - type: markdown
    attributes:
      value: |
        VM-Stock-KIS를 더 좋게 만드는 데 도움을 주셔서 감사합니다! 🎉
        새로운 기능 제안을 자세히 설명해주세요.

  - type: textarea
    id: summary
    attributes:
      label: "기능 요약"
      description: "어떤 기능을 추가하고 싶나요?"
      placeholder: "예: 실시간 데이터 구독 기능"
      required: true

  - type: textarea
    id: problem
    attributes:
      label: "현재의 문제점"
      description: "이 기능이 해결할 문제를 설명해주세요."
      placeholder: |
        현재 quote() 메서드는 일회성 호출만 가능합니다.
        실시간 가격 변동을 모니터링할 수 없습니다.
      required: true

  - type: textarea
    id: solution
    attributes:
      label: "제안하는 솔루션"
      description: "이 기능이 어떻게 작동했으면 좋겠나요?"
      placeholder: |
        예를 들어:
        ```python
        listener = kis.stock("005930").subscribe_quote(on_price_change)
        ```
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: "대안"
      description: "다른 방법으로 이 문제를 해결할 수 있나요?"
      required: false

  - type: checkboxes
    id: checklist
    attributes:
      label: "확인 사항"
      options:
        - label: "이 기능이 VM-Stock-KIS의 범위에 맞다고 생각합니다"
          required: false
        - label: "유사한 기능 요청이 없는지 확인했습니다"
          required: false
```text

#### General 템플릿: `.github/DISCUSSION_TEMPLATE/general.yml`

```yaml
body:
  - type: markdown
    attributes:
      value: |
        VM-Stock-KIS 커뮤니티에 오신 것을 환영합니다! 💙
        아이디어, 경험, 질문을 자유롭게 공유해주세요.

  - type: textarea
    id: message
    attributes:
      label: "내용"
      description: "무엇이 궁금한가요?"
      required: true

  - type: textarea
    id: context
    attributes:
      label: "추가 정보"
      description: "더 많은 맥락을 제공해주세요."
      required: false
```

### 3.2 파일 목록

```text
.github/DISCUSSION_TEMPLATE/
├── question.yml              # Q&A 템플릿
├── feature-request.yml       # 기능 제안 템플릿
├── general.yml               # 일반 토론 템플릿
└── config.json               # (선택사항) 추가 설정
```

### 3.3 Git에 커밋

```bash
git add .github/DISCUSSION_TEMPLATE/
git commit -m "chore: GitHub Discussions 템플릿 추가"
git push origin main
```

---

## 4단계: 모더레이션 가이드

### 4.1 모더레이션 정책

**목표**:

- 존중하고 긍정적인 커뮤니티 유지
- 중복된 질문 방지
- 빠른 응답 시간

**역할**:

- **관리자** (유지보수자): Discussions 관리, 스팸 제거
- **커뮤니티 리더** (경험 많은 사용자): 질문 답변 지원
- **사용자**: 질문, 아이디어 제안

### 4.2 응답 시간

```text
우선순위:    응답 시간
🔴 긴급      24시간 내
🟡 높음       48시간 내
🟢 일반       1주 내
```

**긴급 (🔴)**:

- API 동작 불가 (버그)
- 보안 문제
- 심각한 오류

**높음 (🟡)**:

- 설치/설정 문제
- 주요 기능 문제

**일반 (🟢)**:

- 기능 제안
- 일반 질문
- 경험 공유

### 4.3 스팸 & 부적절한 콘텐츠

**금지 항목**:

- ❌ 광고, 마케팅 콘텐츠
- ❌ 욕설, 모욕적 언어
- ❌ 스팸 링크
- ❌ 중복된 질문 (기존 스레드로 리다이렉트)

**조치**:

1. 첫 위반: 경고 댓글 (삭제 후 설명)
2. 재위반: Discussion 잠금
3. 지속적 위반: 사용자 차단

### 4.4 레이블 (Labels)

```text
🏷️ Labels를 사용하여 Discussion을 분류합니다.

상태:
  - needs-reply    (답변 필요)
  - answered       (답변됨)
  - needs-triage   (검토 필요)

카테고리:
  - installation   (설치 문제)
  - authentication (인증 문제)
  - api-bug        (API 버그)
  - feature-idea   (기능 제안)
  - documentation  (문서 개선)

우선순위:
  - priority-high
  - priority-medium
  - priority-low
```

---

## 5단계: 초기 핀(Pin)된 Discussion

### 5.1 시작하기 Discussion

**제목**: "🎯 VM-Stock-KIS 시작하기"

**내용**:

```markdown
# VM-Stock-KIS에 오신 것을 환영합니다! 👋

VM-Stock-KIS는 한국투자증권 API를 Python으로 쉽게 사용할 수 있는 라이브러리입니다.

## 🚀 빠른 시작
- [5분 만에 시작하기](docs/user/en/QUICKSTART.md)
- [설치 가이드](docs/user/en/README.md)

## ❓ 자주 묻는 질문
- [FAQ](docs/FAQ.md)
- [문제 해결](docs/user/en/QUICKSTART.md#troubleshooting)

## 💬 커뮤니티
- 질문이 있으신가요? [Q&A](#) 카테고리에서 질문해주세요.
- 기능 제안이 있으신가요? [Ideas](#) 카테고리에서 제안해주세요.
- 경험을 공유하고 싶으신가요? [General](#) 카테고리를 방문해주세요.

## 📚 문서
- [공식 문서](https://github.com/...)
- [예제 코드](examples/)
- [API 레퍼런스](docs/)
- [기여 가이드](CONTRIBUTING.md)

## 🎓 튜토리얼
- [YouTube 튜토리얼: 5분 안에 시작하기](#) (곧 공개)
- [예제 Jupyter Notebook](examples/tutorial_basic.ipynb)

행운을 빕니다! 🎉
```

### 5.2 커뮤니티 가이드 Discussion

**제목**: "📋 커뮤니티 행동 강령"

**내용**:

```markdown
# 커뮤니티 행동 강령

VM-Stock-KIS 커뮤니티는 모든 참여자를 존중하고 포용하는 환경을 추구합니다.

## 우리의 약속
- 존경과 존중
- 포용성
- 투명성
- 책임

## 행동 지침
- ✅ 다른 사람을 존중해주세요
- ✅ 건설적인 비판을 제공해주세요
- ✅ 질문에 성실하게 답변해주세요
- ✅ 커뮤니티의 성장을 도와주세요

## 금지 행위
- ❌ 욕설, 모욕적 언어
- ❌ 차별 발언
- ❌ 개인 공격
- ❌ 스팸, 광고

## 보고 방법
부적절한 행동을 발견하면:
1. 댓글로 지적해주세요.
2. 또는 이메일로 보고해주세요: maintainers@...

감사합니다! 🙏
```

---

## 6단계: 자동화 (GitHub Actions)

### 6.1 자동 응답 봇 (선택사항)

**파일**: `.github/workflows/auto-responder.yml`

```yaml
name: Auto-responder
on:
  discussions:
    types: [created, transferred]

jobs:
  welcome:
    runs-on: ubuntu-latest
    if: github.event.action == 'created'
    steps:
      - name: Add welcome comment
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.discussions.createComment({
              repository_id: context.repo.repo_id,
              discussion_number: context.payload.discussion.number,
              body: '감사합니다! 🙏\n\n빠른 답변을 위해:\n1. FAQ를 먼저 확인해주세요.\n2. 재현 코드를 제공해주세요.\n3. 환경 정보를 기재해주세요.'
            })
```

### 6.2 유휴 Discussion 알림 (선택사항)

```yaml
# 14일 이상 답변 없는 Q&A에 자동 알림
name: Idle questions reminder
on:
  schedule:
    - cron: '0 9 * * 1'  # 매주 월요일 오전 9시

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Check idle discussions
        # 구현: 14일 이상 미답변 토론 조회
```

---

## 7단계: 런칭 체크리스트

### 설정 확인

- [ ] Discussions 활성화됨
- [ ] 4개 카테고리 생성됨
- [ ] 3개 템플릿 파일 추가됨
- [ ] 2개 핀 Discussion 생성됨
- [ ] 모더레이션 가이드 준비됨
- [ ] 레이블 설정 완료됨

### 문서화

- [ ] README.md에 Discussions 링크 추가
- [ ] CONTRIBUTING.md에 커뮤니티 정보 추가
- [ ] GitHub에 커뮤니티 탭 설정 (커뮤니티 가이드)

### 홍보

- [ ] 첫 공지사항 게시 (v2.2.0 출시 소식)
- [ ] YouTube 영상에서 언급
- [ ] 소셜 미디어에 공유
- [ ] 예제에서 Discussions 링크 추가

---

## 8단계: 초기 활성화

### Week 1 활동 계획

```text
일정             활동
======================================
Day 1            Discussions 활성화
Day 2-3          체크리스트 완료
Day 4-7          초기 핀 Discussion 5-7개 생성
Week 2           커뮤니티 리더 선정
Week 3           첫 GitHub Discussions 라이브
```

### 첫 공지사항

```markdown
제목: "VM-Stock-KIS GitHub Discussions 오픈! 🎉"

안녕하세요!

오늘부터 VM-Stock-KIS GitHub Discussions가 오픈됩니다! 🎊

이제 다음을 통해 커뮤니티와 소통할 수 있습니다:
- ❓ Q&A: 기술 질문 및 문제 해결
- 💡 Ideas: 새로운 기능 제안
- 💬 General: 경험 공유 및 자유로운 토론
- 📢 Announcements: 새로운 버전 및 중요 공지

우리는 존경과 포용의 커뮤니티를 만들고 싶습니다.
여러분의 참여와 의견을 기다리고 있습니다! 🙏

👉 시작하기: [GitHub Discussions](#)
📚 문서: [공식 가이드](#)

감사합니다! 🙏
```

---

## 성과 지표 (1개월 후)

```text
지표                     목표
====================================
토론 개수                 20+
답변율                    90%
평균 응답 시간            48시간 이내
활성 참여자               10+
커뮤니티 리더 선정        3-5명
```

---

## 참고 자료

- [GitHub Discussions 공식 문서](https://docs.github.com/en/discussions)
- [Discussion 템플릿](https://docs.github.com/en/discussions/managing-discussions-for-your-community/about-discussions)
- [커뮤니티 모더레이션](https://docs.github.com/en/communities/moderating-comments-and-conversations)
- [VM-Stock-KIS CONTRIBUTING.md](../../CONTRIBUTING.md)

---

**작성일**: 2025-12-20
**상태**: ✅ 설정 가이드 완성 (구현 준비)
**다음**: GitHub에서 직접 설정 실행 및 초기화
