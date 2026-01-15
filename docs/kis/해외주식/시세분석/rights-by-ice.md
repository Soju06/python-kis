# 해외주식 권리종합 [해외주식-050]

> [해외주식] 시세분석

해외주식 권리종합 API입니다.
한국투자 HTS(eFriend Plus) > [7833] 해외주식 권리(ICE제공) 화면의 "전체" 탭 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 조회기간 기준일 입력시 참고 - 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일, 그 외: 발표일


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `cd4be4fc-4545-4147-ab9a-e5b0ccede0de` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/rights-by-ice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `HHDFS78330900` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
- **최종 수정일**: 2025-05-15

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFS78330900 |
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
| `NCOD` | 국가코드 | String | 2 | Y | CN:중국 HK:홍콩 US:미국 JP:일본 VN:베트남 |
| `SYMB` | 심볼 | String | 20 | Y | 종목코드 |
| `ST_YMD` | 일자 시작일 | String | 8 | Y | 미입력 시, 오늘-3개월 기간지정 시, 종료일 입력(ex. 20240514)  ※ 조회기간 기준일 입력시 참고 - 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일... |
| `ED_YMD` | 일자 종료일 | String | 8 | Y | 미입력 시, 오늘+3개월 기간지정 시, 종료일 입력(ex. 20240514)  ※ 조회기간 기준일 입력시 참고 - 상환: 상환일자, 조기상환: 조기상환일자, 티커변경: 적용일... |

### 요청 예시

```json
NCOD:US
SYMB:MAIN
ST_YMD:20240214
ED_YMD:20240514
```

## 응답

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
| `anno_dt` | ICE공시일 | String | 8 | Y |  |
| `ca_title` | 권리유형 | String | 12 | Y |  |
| `div_lock_dt` | 배당락일 | String | 8 | Y |  |
| `pay_dt` | 지급일 | String | 8 | Y |  |
| `record_dt` | 기준일 | String | 8 | Y |  |
| `validity_dt` | 효력일자 | String | 8 | Y |  |
| `local_end_dt` | 현지지시마감일 | String | 8 | Y |  |
| `lock_dt` | 권리락일 | String | 8 | Y |  |
| `delist_dt` | 상장폐지일 | String | 8 | Y |  |
| `redempt_dt` | 상환일자 | String | 8 | Y |  |
| `early_redempt_dt` | 조기상환일자 | String | 8 | Y |  |
| `effective_dt` | 적용일 | String | 8 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "anno_dt": "20240221",
      "ca_title": "현금배당",
      "div_lock_dt": "20240607",
      "pay_dt": "20240614",
      "record_dt": "20240607",
      "validity_dt": "",
      "local_end_dt": "",
      "lock_dt": "",
      "delist_dt": "",
      "redempt_dt": "",
      "early_redempt_dt": "",
      "effective_dt": ""
    },
    {
      "anno_dt": "20240221",
      "ca_title": "현금배당",
      "div_lock_dt": "20240405",
      "pay_dt": "20240415",
      "record_dt": "20240408",
      "validity_dt": "",
      "local_end_dt": "",
      "lock_dt": "",
      "delist_dt": "",
      "redempt_dt": "",
      "early_redempt_dt": "",
      "effective_dt": ""
    },
    {
      "anno_dt": "20240221",
      "ca_title": "현금배당",
      "div_lock_dt": "20240507",
      "pay_dt": "20240515",
      "record_dt": "20240508",
      "validity_dt": "",
      "local_end_dt": "",
      "lock_dt": "",
      "delist_dt": "",
      "redempt_dt": "",
      "early_redempt_dt": "",
      "effective_dt": ""
    },
    {
      "anno_dt": "20240507",
      "ca_title": "현금배당",
      "div_lock_dt": "20240808",
      "pay_dt": "20240815",
      "record_dt": "20240808",
      "validity_dt": "",
      "local_end_dt": "",
      "lock_dt": "",
      "delist_dt": "",
      "redempt_dt": "",
      "early_redempt_dt": "",
      "effective_dt": ""
    },
    {
      "anno_dt": "20240507",
      "ca_title": "현금배당",
      "div_lock_dt": "20240708",
      "pay_dt": "20240715",
      "record_dt": "20240708",
      "validity_dt": "",
      "local_end_dt": "",
      "lock_dt": "",
      "delist_dt": "",
      "redempt_dt": "",
      "early_redempt_dt": "",
      "effective_dt": ""
    },
    {
      "anno_dt": "20240507",
      "ca_title": "현금배당",
      "div_lock_dt": "20240906",
      "pay_dt": "20240913",
      "record_dt": "20240906",
      "validity_dt": "",
      "local_end_dt": "",
      "lock_dt": "",
      "delist_dt": "",
      "redempt_dt": "",
      "early_redempt_dt": "",
      "effective_dt": ""
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

