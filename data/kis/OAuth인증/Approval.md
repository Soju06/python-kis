# 실시간 (웹소켓) 접속키 발급[실시간-000]

> OAuth인증

실시간 (웹소켓) 접속키 발급받으실 수 있는 API 입니다.
웹소켓 이용 시 해당 키를 appkey와 appsecret 대신 헤더에 넣어 API를 호출합니다.

접속키의 유효기간은 24시간이지만, 접속키는 세션 연결 시 초기 1회만 사용하기 때문에 접속키 인증 후에는 세션종료되지 않는 이상 접속키 신규 발급받지 않으셔도 365일 내내 웹소켓 데이터 수신하실 수 있습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5c87ba63-740a-4166-93ac-803510bb9c02` |
| **HTTP Method** | `POST` |
| **URL** | `/oauth2/Approval` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | 미지원 |
| **TR ID (모의)** | 미지원 |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-14T18:27:14+09:00
- **최종 수정일**: 2023-06-27T13:53:49+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 20 | N | application/json; utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `grant_type` | 권한부여타입 | String | 18 | Y | "client_credentials" |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `secretkey` | 시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) * 주의 : appsecret와 secretkey는 동일하오니 착오없으시기 바랍니다. (용어가 다른점 양해 부탁드립니다.) |

### 요청 예시

```json
{
  "grant_type": "client_credentials",
  "appkey": "PSg5dctL9dKPo727J13Ur405OSXXXXXXXXXX",
  "secretkey": "yo2t8zS68zpdjGuWvFyM9VikjXE0i0CbgPEamnqPA00G0bIfrdfQb2RUD1xP7SqatQXr1cD1fGUNsb78MMXoq6o4lAYt9YTtHAjbMoFy+c72kbq5owQY1Pvp39/x6ejpJlXCj7gE3yVOB/h25Hvl+URmYeBTfrQeOqIAOYc/OIXXXXXXXXXX"
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | Y | 웹소켓 이용 시 발급받은 웹소켓 접속키를 appkey와 appsecret 대신 헤더에 넣어 API 호출합니다. |

### 응답 예시

```json
{
  "approval_key": "a2585daf-8c09-4587-9fce-8ab893XXXXX"
}
```

