# 해외주식 체결추이[해외주식-037]

> [해외주식] 기본시세

해외주식 체결추이 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `0a0f2b43-8a3f-44a4-80b7-f8cf4d6e2f37` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/inquire-ccnl` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `HHDFS76200300` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
- **최종 수정일**: 2025-06-20

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFS76200300 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `EXCD` | 거래소명 | String | 4 | Y | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 ' |
| `AUTH` | 사용자권한정보 | String | 32 | Y | 공백 |
| `KEYB` | NEXT KEY BUFF | String | 32 | Y | 공백 |
| `TDAY` | 당일전일구분 | String | 1 | Y | 0:전일, 1:당일 |
| `SYMB` | 종목코드 | String | 16 | Y | 해외종목코드 |

### 요청 예시

```json
AUTH:
EXCD:NAS
SYMB:AAPL
TDAY:0
KEYB:
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output1` | 응답상세 | Object |   | Y | array |
| `khms` | 한국기준시간 | String | 6 | Y |  |
| `last` | 체결가 | String | 12 | Y |  |
| `sign` | 기호 | String | 1 | Y |  |
| `diff` | 대비 | String | 12 | Y |  |
| `rate` | 등락율 | String | 12 | Y |  |
| `evol` | 체결량 | String | 10 | Y |  |
| `tvol` | 거래량 | String | 14 | Y |  |
| `mtyp` | 시장구분 | String | 1 | Y | 0: 장중 1:장전 2:장후 |
| `pbid` | 매수호가 | String | 12 | Y |  |
| `pask` | 매도호가 | String | 12 | Y |  |
| `vpow` | 체결강도 | String | 10 | Y |  |

### 응답 예시

```json
{
    "output1": [
        {
            "khms": "085957",
            "last": "195.2000",
            "sign": "5",
            "diff": "3.2200",
            "rate": "-1.62",
            "evol": "30",
            "tvol": "29159135",
            "mtyp": "",
            "pbid": "195.1500",
            "pask": "195.6000",
            "vpow": "71.66"
        },
        {
            "khms": "085957",
            "last": "195.2000",
            "sign": "5",
            "diff": "3.2200",
            "rate": "-1.62",
            "evol": "10",
            "tvol": "29159105",
            "mtyp": "",
            "pbid": "195.1500",
            "pask": "195.6000",
            "vpow": "71.66"
        },...
        {
            "khms": "085505",
            "last": "195.2700",
            "sign": "5",
            "diff": "3.1500",
            "rate": "-1.59",
            "evol": "50",
            "tvol": "29155328",
            "mtyp": "",
            "pbid": "195.2300",
            "pask": "195.3000",
            "vpow": "71.67"
        }
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
