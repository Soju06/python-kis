# /explore-kis-api

KIS API 레퍼런스 탐색 스킬.

## Description

KIS API 레퍼런스 문서(`data/kis/`)를 탐색하여 endpoint 정보, 요청/응답 구조, 파라미터를 조회합니다.

## Arguments

- `[keyword]` — 검색 키워드 (endpoint 이름, 경로, 기능 설명)
- `[category]` — 카테고리 (국내주식, 해외주식, 국내선물옵션, 해외선물옵션, 장내채권)

## Workflow

### Search

키워드 또는 카테고리로 문서 검색:

```
data/kis/
├── 국내주식/       — 국내 주식 시세, 주문, 계좌
├── 해외주식/       — 해외 주식 시세, 주문, 계좌
├── 국내선물옵션/   — 국내 선물/옵션
├── 해외선물옵션/   — 해외 선물/옵션
├── 장내채권/       — 장내 채권
├── OAuth인증/      — 인증/토큰
├── FAQ/            — 자주 묻는 질문
└── 종목정보파일/   — 마스터 데이터 파일 스펙
```

### Output

endpoint 정보 요약:
- Endpoint name
- UUID
- HTTP method + path
- TR ID (demo/real)
- Request parameters (type, required, description)
- Response fields (type, description)

## Usage Examples

- `/explore-kis-api 투자자` — 투자자 관련 endpoint 검색
- `/explore-kis-api 해외주식 시세` — 해외주식 시세 endpoint 검색
- `/explore-kis-api e27baf2f` — 특정 UUID로 endpoint 조회
