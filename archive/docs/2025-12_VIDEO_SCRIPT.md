> **동결 — 2025-12-20 에 쓴 튜토리얼 영상 대본입니다.** 원래 자리는
> `docs/guidelines/VIDEO_SCRIPT.md` 였습니다.
>
> **8개월간 제작되지 않았습니다.** 저장소 어디에도 영상 링크가 없고, 이 문서를
> 가리키던 것은 `docs/INDEX.md` 의 한 줄뿐이었습니다. "프로덕션 계획" 절이
> 있지만 실행된 흔적이 없습니다.
>
> 안의 서술도 그 시점에 묶여 있습니다 — 분량·해상도·자막 계획이 전부
> 2025-12 기준이고, 그 사이 배포명과 공개 API 가 바뀌었습니다.
>
> 다시 만들기로 하면 **여기서 옮겨 오지 말고 복사해서 제자리에 되살리세요**
> (`archive/README.md` 규칙 3). 그때는 대본을 현재 API 로 다시 맞춰야 합니다.
>
> 보관 기준은 [`archive/README.md`](../README.md) 를 보세요.
> 근거: [`#107`](https://github.com/visualmoney/vm-stock-kis/issues/107)

# 튜토리얼 영상 스크립트: "5분 안에 VM-Stock-KIS 시작하기"

**제작일**: 2025-12-20
**분량**: 약 5분 (300초)
**대상 관객**: Python 초보자, 트레이딩 관심자
**언어**: 한국어 (자막: 영어)
**해상도**: 1080p (1920x1080)
**프레임 레이트**: 30fps

---

## 프로덕션 계획

### 장비 요구사항

- 마이크 (또는 시스템 오디오)
- 화면 녹화 소프트웨어 (OBS, ScreenFlow, Camtasia)
- 편집 소프트웨어 (DaVinci Resolve, Adobe Premiere)
- 배경음악 (저작권 자유 음악)

### 시간대별 분량

```text
Scene 1 - 인트로:        30초  (0:00 ~ 0:30)
Scene 2 - 설치:         60초  (0:30 ~ 1:30)
Scene 3 - 설정:         60초  (1:30 ~ 2:30)
Scene 4 - 첫 호출:       80초  (2:30 ~ 3:50)
Scene 5 - 아웃트로:      50초  (3:50 ~ 4:40)
총:                    280초  (~4:40)
```

---

## Scene 1: 인트로 (0:00 ~ 0:30)

### 시각 요소

```text
┌─────────────────────────────────────────┐
│  [배경: 파란색 그래디언트]              │
│                                         │
│  VM-Stock-KIS 로고 [페이드인]             │
│                                         │
│  "5분 안에 시작하기"                    │
│  [텍스트 애니메이션]                    │
└─────────────────────────────────────────┘
```

### 스크립트 (자막 & 음성)

**한국어 음성** (30초):
> "안녕하세요! VM-Stock-KIS입니다.
> 한국투자증권 API를 Python으로 쉽게 사용할 수 있는 라이브러리입니다.
> 지금부터 5분 안에 첫 거래를 시작하는 방법을 보여드리겠습니다.
> 준비되셨나요? 시작합니다!"

**영어 자막**:
> "Hello! This is VM-Stock-KIS.
> A Python library for easy access to Korea Investment & Securities API.
> In the next 5 minutes, I'll show you how to make your first trade.
> Ready? Let's start!"

**배경음악**: Upbeat, Tech-focused (0:00 ~ 4:40 전체)

---

## Scene 2: 설치 (0:30 ~ 1:30)

### 시각 요소

```text
┌─────────────────────────────────────────────┐
│  [터미널 창 - 검은 배경]                    │
│                                             │
│  $ pip install vm-stock-kis                 │
│  Collecting vm-stock-kis...                 │
│  Successfully installed vm-stock-kis-0.0.1  │
│                                             │
│  [효과음: 설치 완료 신호음]                 │
└─────────────────────────────────────────────┘
```

### 스크립트 (60초)

**한국어 음성**:
> "먼저 설치부터 시작합니다.
> 터미널에서 `pip install vm-stock-kis`를 입력하기만 하면 됩니다.
> [일시정지 2초]
> 설치가 완료되었습니다!
> 정말 간단하죠?
> 이제 인증 정보를 준비할 차례입니다.
> 한국투자증권 홈페이지에서 App Key와 App Secret을 받으셔야 합니다.
> 개발자 포털에서 간단히 신청할 수 있습니다."

**영어 자막**:
> "First, let's install the library.
> Just type `pip install vm-stock-kis` in the terminal.
> Installation complete!
> Now we need authentication credentials.
> Get your App Key and Secret from the KIS Developer Portal.
> It only takes a few minutes to apply."

**화면 캡처**: pip install 실행 → 설치 완료

---

## Scene 3: 설정 (1:30 ~ 2:30)

### 시각 요소

```text
┌─────────────────────────────────────────┐
│  [코드 에디터 - VS Code]               │
│                                         │
│  config.yaml:                           │
│  kis:                                   │
│    app_key: "YOUR_APP_KEY"             │
│    app_secret: "YOUR_SECRET"           │
│    account_number: "00000000-01"       │
└─────────────────────────────────────────┘
```

### 스크립트 (60초)

**한국어 음성**:
> "이제 설정 파일을 만들겠습니다.
> config.yaml이라는 파일을 생성하고,
> [일시정지 1초]
> App Key와 Secret을 입력합니다.
> 계좌번호도 필요합니다.
> 편의상 환경변수로도 설정할 수 있습니다.
> 설정이 완료되면,
> 드디어 코드를 작성할 차례입니다!
> 정말 쉽습니다!"

**영어 자막**:
> "Create a config.yaml file.
> Enter your App Key, App Secret, and account number.
> Alternatively, use environment variables.
> Configuration is now complete!
> Time to write some code."

**화면 캡처**: VS Code에서 config.yaml 작성

---

## Scene 4: 첫 API 호출 (2:30 ~ 3:50)

### 시각 요소

```text
┌─────────────────────────────────────────┐
│  [코드 에디터 - Python 파일]           │
│                                         │
│  from vmkis import VmKis               │
│                                         │
│  kis = VmKis()                         │
│  quote = kis.stock("005930").quote()   │
│                                         │
│  print(f"삼성전자 가격: {quote.price}")  │
│                                         │
│  [실행]                                 │
│  > 삼성전자 가격: 60,000 KRW            │
└─────────────────────────────────────────┘
```

### 스크립트 (80초)

**한국어 음성**:
> "이제 Python 파일을 만들겠습니다.
> [일시정지 1초]
> 먼저 VmKis를 임포트합니다.
> 그 다음, VmKis 클라이언트를 초기화합니다.
> config.yaml에서 자동으로 설정을 읽습니다.
> [일시정지 2초]
> 이제 삼성전자 주가를 조회해봅시다.
> kis.stock('005930')은 삼성전자를 의미합니다.
> 그 다음 quote()를 호출하면 실시간 시세를 가져옵니다.
> [일시정지 1초]
> 보세요! 현재 가격이 출력되었습니다.
> 정말 간단하죠?
> [일시정지 1초]
> 이제 주문도 해볼 수 있습니다.
> kis.stock('005930').buy(quantity=10, price=60000)
> 이렇게 매수 주문을 할 수 있습니다.
> 물론 실제 계좌가 필요합니다!"

**영어 자막**:
> "Create a Python script.
> Import VmKis.
> Initialize the client.
> Query Samsung Electronics stock.
> kis.stock('005930').quote()
> Done! The current price is displayed.
> You can also place orders:
> kis.stock('005930').buy(quantity=10, price=60000)
> Simple as that!"

**화면 캡처**:

- Python 코드 작성 (라이브 입력)
- 코드 실행
- 출력 결과

---

## Scene 5: 아웃트로 (3:50 ~ 4:40)

### 시각 요소

```text
┌─────────────────────────────────────────┐
│  [마무리 슬라이드]                     │
│                                         │
│  다음 단계:                             │
│  1️⃣ FAQ 읽기                           │
│  2️⃣ 예제 코드 실습                     │
│  3️⃣ GitHub Issues 로 질문              │
│                                         │
│  문서: docs/user/en/                    │
│  GitHub: github.com/...                │
│                                         │
│  "더 많은 정보는 문서를 참고하세요!"    │
└─────────────────────────────────────────┘
```

### 스크립트 (50초)

**한국어 음성**:
> "축하합니다!
> 5분 만에 VM-Stock-KIS를 시작했습니다!
> [일시정지 1초]
> 이제 더 많은 것을 배울 준비가 되셨나요?
> [일시정지 1초]
> 다음 단계:
>
> 1. 공식 FAQ를 읽어보세요.
> 2. 예제 코드들을 실습해보세요.
> 3. GitHub Issues 로 질문하세요.
> [일시정지 1초]
> 모든 문서는 깃허브에서 찾을 수 있습니다.
> 감사합니다! 행운을 빕니다!"

**영어 자막**:
> "Congratulations!
> You've started VM-Stock-KIS in just 5 minutes!
> Next steps:
>
> 1. Read the FAQ
> 2. Try the example code
> 3. Ask on GitHub Issues
> Find all documentation on GitHub.
> Thank you! Happy trading!"

**배경음악**: 클라이맥스 → 페이드 아웃

---

## 편집 가이드

### 컬러 스킴

```text
주 색상:   파란색 (#007BFF)
강조색:    초록색 (#51CF66)
텍스트:   흰색 (#FFFFFF)
배경:     검은색 (#1A1A1A)
```

### 전환 효과

- Scene 간: 페이드 (0.5초)
- 텍스트 입장: 슬라이드 (0.3초)
- 코드 실행: 효과음 + 플래시

### 음성 설정

- **언어**: 한국어 (기본), 영어 (자막)
- **속도**: 일반 속도 (너무 빠르지 않게)
- **톤**: 친절하고 전문적
- **배경음악**: 낮은 볼륨 (음성을 방해하지 않을 수준)

### 자막 설정

- **폰트**: 명조체 (가독성 높음)
- **크기**: 해상도 1080p 기준 40pt
- **색상**: 하얀색 (검은색 테두리)
- **위치**: 하단 중앙
- **디스플레이**: 음성과 동기화

---

## 업로드 & 배포

### YouTube 준비

```yaml
제목: "VM-Stock-KIS: 5분 안에 거래 시작하기 | 한국투자증권 API"

설명:
"VM-Stock-KIS는 한국투자증권 API를 쉽게 사용할 수 있는 라이브러리입니다.
이 영상에서는 설치부터 첫 거래까지 5분만에 완성하는 방법을 보여드립니다.

⏱️ 시간대:
0:00 - 인트로
0:30 - 설치
1:30 - 설정
2:30 - 첫 API 호출
3:50 - 아웃트로

📚 문서:
- GitHub: https://github.com/...
- QUICKSTART: docs/user/en/QUICKSTART.md
- FAQ: docs/user/en/FAQ.md
- 예제: examples/

💬 커뮤니티:
- GitHub Issues: https://github.com/visualmoney/vm-stock-kis/issues
- 질문이 있으신가요? 이슈를 열어 주세요!

🔔 구독과 좋아요를 눌러주세요!

#VMStockKIS #거래 #API #한국투자증권"

태그:
python, trading, api, korea, kis, finance, tutorial, beginner

카테고리: 교육

언어: 한국어

자막: 영어 (자동 생성 또는 수동 추가)
```

### GitHub 저장소

```text
docs/
├── guidelines/
│   └── VIDEO_SCRIPT.md (이 파일)
└── user/
    ├── en/
    │   ├── README.md (영상 링크 포함)
    │   └── QUICKSTART.md
    └── ko/
        └── README.md (영상 링크 포함)
```

---

## 촬영 체크리스트

### 사전 준비

- [ ] 배경 정리 (책상, 모니터)
- [ ] 마이크 테스트
- [ ] 조명 확인 (충분한 밝기)
- [ ] 배경음악 준비
- [ ] 설치 완료된 시스템

### 촬영

- [ ] Scene 1 녹화 (인트로)
- [ ] Scene 2 녹화 (설치)
- [ ] Scene 3 녹화 (설정)
- [ ] Scene 4 녹화 (첫 호출)
- [ ] Scene 5 녹화 (아웃트로)

### 편집

- [ ] Scene 순서 정렬
- [ ] 음성 싱크 맞추기
- [ ] 자막 추가
- [ ] 배경음악 삽입
- [ ] 전환 효과 추가
- [ ] 색상 보정
- [ ] 최종 검토

### 배포

- [ ] YouTube 제목 & 설명 작성
- [ ] 자막 업로드 (SRT 파일)
- [ ] GitHub README에 링크 추가
- [ ] 언어별 버전 제작 (영어 자막 → 영어 더빙)

---

## 분석 & 피드백

### 성과 지표

```text
영상 업로드 2주 후:
- 조회수: 500+ (목표)
- 좋아요: 50+ (목표)
- 댓글: 20+ (피드백 수집)
- 구독자: +100 (목표)
```

### 개선 항목 (향후)

- [ ] 영어 더빙 버전
- [ ] 중국어 자막
- [ ] 일본어 자막
- [ ] 고급 튜토리얼 영상 (주문, 실시간 업데이트)
- [ ] 라이브 스트리밍 Q&A

---

## 참고 자료

- [QUICKSTART.md](../../QUICKSTART.md) - 빠른 시작 가이드
- [FAQ.md](../../docs/FAQ.md) - 자주 묻는 질문
- [examples/](../../examples/) - 예제 코드
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - 기여 가이드

---

**작성일**: 2025-12-20
**상태**: ✅ 스크립트 완성 (촬영 준비 완료)
**다음**: YouTube 영상 제작 (외부 제작사 의뢰 또는 자체 촬영)
