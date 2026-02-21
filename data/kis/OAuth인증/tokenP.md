# 접근토큰발급(P)[인증-001]

> OAuth인증

본인 계좌에 필요한 인증 절차로, 인증을 통해 접근 토큰을 부여받아 오픈API 활용이 가능합니다.

1. 접근토큰(access_token)의 유효기간은 24시간 이며(1일 1회발급 원칙) 
   갱신발급주기는 6시간 입니다.(6시간 이내는 기존 발급키로 응답)

2. 접근토큰발급(/oauth2/tokenP) 시 접근토큰값(access_token)과 함께 수신되는 
   접근토큰 유효기간(acess_token_token_expired)을 이용해 접근토큰을 관리하실 수 있습니다.


[참고]

'23.4.28 이후 지나치게 잦은 토큰 발급 요청건을 제어 하기 위해 신규 접근토큰발급 이후 일정시간 이내에 재호출 시에는 직전 토큰값을 리턴하게 되었습니다. 일정시간 이후 접근토큰발급 API 호출 시에는 신규 토큰값을 리턴합니다. 
접근토큰발급 API 호출 및 코드 작성하실 때 해당 사항을 참고하시길 바랍니다.

※ 참고 : 포럼 > 공지사항 >  [수정] [중요] 접근 토큰 발급 변경 안내


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fa778c98-f68d-451e-8fff-b1c6bfe5cd30` |
| **HTTP Method** | `POST` |
| **URL** | `/oauth2/tokenP` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | 미지원 |
| **TR ID (모의)** | 미지원 |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-04-24T09:54:42+09:00
- **최종 수정일**: 2025-04-28T09:34:57+09:00

## 요청

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `grant_type` | 권한부여 Type | String | 18 | Y | client_credentials |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |

### 요청 예시

```json
{
  "grant_type": "client_credentials",
  "appkey": "PSg5dctL9dKPo727J13Ur405OSXXXXXXXXXX",
  "appsecret": "yo2t8zS68zpdjGuWvFyM9VikjXE0i0CbgPEamnqPA00G0bIfrdfQb2RUD1xP7SqatQXr1cD1fGUNsb78MMXoq6o4lAYt9YTtHAjbMoFy+c72kbq5owQY1Pvp39/x6ejpJlXCj7gE3yVOB/h25Hvl+URmYeBTfrQeOqIAOYc/OIXXXXXXXXXX"
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `access_token` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token ex) "eyJ0eXUxMiJ9.eyJz…..................................."   - 일반개인고객/일반법인고객   . Access token 유효기간 1일   .. 일정시간(6시간) 이내에 재호출 시에는 직전 토큰값을 리턴   . OAuth 2.0의 Client Credentials Grant 절차를 준용   - 제휴법인   . Access token 유효기간 3개월   . Refresh token 유효기간 1년   . OAuth 2.0의 Authorization Code Grant 절차를 준용 |
| `token_type` | 접근토큰유형 | String | 20 | Y | 접근토큰유형 : "Bearer" ※ API 호출 시, 접근토큰유형 "Bearer" 입력. ex) "Bearer eyJ...." |
| `expires_in` | 접근토큰 유효기간 | Number | 10 | Y | 유효기간(초) ex) 7776000 |
| `access_token_token_expired` | 접근토큰 유효기간(일시표시) | String | 50 | Y | 유효기간(년:월:일 시:분:초) ex) "2022-08-30 08:10:10" |

### 응답 예시

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImMwNzM1NTYzLTA1MjctNDNhZS05ODRiLTJiNWI1ZWZmOWYyMyIsImlzcyI6InVub2d3IiwiZXhwIjoxNjQ5NzUxMTAwLCJpYXQiOjE2NDE5NzUxMDAsImp0aSI6IkJTZlM0QUtSSnpRVGpmdHRtdXZlenVQUTlKajc3cHZGdjBZVyJ9.Oyt_C639yUjWmRhymlszgt6jDo8fvIKkkxH1mMngunV1T15SCC4I3Xe6MXxcY23DXunzBfR1uI0KXXXXXXXXXX",
  "access_token_token_expired": "2023-12-22 08:16:59",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

