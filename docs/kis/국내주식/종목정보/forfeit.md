# 예탁원정보(실권주일정)[국내주식-152]

> [국내주식] 종목정보

예탁원정보(실권주일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0668] 실권주 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a4f2cae8-2180-428c-a456-6acf5cfbeafb` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/forfeit` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `HHKDB669109C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
- **최종 수정일**: 2025-05-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669109C0 |
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
| `SHT_CD` | 종목코드 | String | 9 | Y | 공백: 전체,  특정종목 조회시 : 종목코드 |
| `T_DT` | 조회일자To | String | 8 | Y | ~ 일자 |
| `F_DT` | 조회일자From | String | 8 | Y | 일자 ~ |
| `CTS` | CTS | String | 17 | Y | 공백 |

### 요청 예시

```json
cts:
f_dt:20230301
t_dt:20240326
sht_cd:
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
| `record_date` | 기준일 | String | 8 | Y |  |
| `sht_cd` | 종목코드 | String | 9 | Y |  |
| `isin_name` | 종목명 | String | 40 | Y |  |
| `subscr_dt` | 청약일 | String | 23 | Y |  |
| `subscr_price` | 공모가 | String | 9 | Y |  |
| `subscr_stk_qty` | 공모주식수 | String | 12 | Y |  |
| `refund_dt` | 환불일 | String | 10 | Y |  |
| `list_dt` | 상장/등록일 | String | 10 | Y |  |
| `lead_mgr` | 주간사 | String | 25 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "record_date": "20240131",
      "sht_cd": "001440",
      "isin_name": "대한전선",
      "subscr_dt": "2024/03/14 ~ 2024/03/15",
      "subscr_price": "000007460",
      "subscr_stk_qty": "    62000000",
      "refund_dt": "2024/03/19",
      "list_dt": "2024/04/02",
      "lead_mgr": "케이비증권,미래에셋증권,"
    },
    {
      "record_date": "20240131",
      "sht_cd": "001447",
      "isin_name": "대한전선2우",
      "subscr_dt": "2024/03/14 ~ 2024/03/15",
      "subscr_price": "000007460",
      "subscr_stk_qty": "    62000000",
      "refund_dt": "2024/03/19",
      "list_dt": "2024/04/02",
      "lead_mgr": "케이비증권,미래에셋증권,"
    },
    {
      "record_date": "20240131",
      "sht_cd": "001449",
      "isin_name": "대한전선3우",
      "subscr_dt": "2024/03/14 ~ 2024/03/15",
      "subscr_price": "000007460",
      "subscr_stk_qty": "    62000000",
      "refund_dt": "2024/03/19",
      "list_dt": "2024/04/02",
      "lead_mgr": "케이비증권,미래에셋증권,"
    },
    {
      "record_date": "20240131",
      "sht_cd": "00144A",
      "isin_name": "대한전선4우",
      "subscr_dt": "2024/03/14 ~ 2024/03/15",
      "subscr_price": "000007460",
      "subscr_stk_qty": "    62000000",
      "refund_dt": "2024/03/19",
      "list_dt": "2024/04/02",
      "lead_mgr": "케이비증권,미래에셋증권,"
    },
    {
      "record_date": "20240131",
      "sht_cd": "00144K",
      "isin_name": "대한전선5우",
      "subscr_dt": "2024/03/14 ~ 2024/03/15",
      "subscr_price": "000007460",
      "subscr_stk_qty": "    62000000",
      "refund_dt": "2024/03/19",
      "list_dt": "2024/04/02",
      "lead_mgr": "케이비증권,미래에셋증권,"
    },
    {
      "record_date": "20240126",
      "sht_cd": "034220",
      "isin_name": "LG디스플레이",
      "subscr_dt": "2024/03/11 ~ 2024/03/12",
      "subscr_price": "000009090",
      "subscr_stk_qty": "   142184300",
      "refund_dt": "2024/03/14",
      "list_dt": "2024/03/26",
      "lead_mgr": "한국투자증권,NH투자증권,"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

