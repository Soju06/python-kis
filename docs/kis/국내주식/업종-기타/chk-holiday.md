# 국내휴장일조회[국내주식-040]

> [국내주식] 업종/기타

(★중요) 국내휴장일조회(TCA0903R) 서비스는 당사 원장서비스와 연관되어 있어 
단시간 내 다수 호출시 서비스에 영향을 줄 수 있어 가급적 1일 1회 호출 부탁드립니다.

국내휴장일조회 API입니다.
영업일, 거래일, 개장일, 결제일 여부를 조회할 수 있습니다.
주문을 넣을 수 있는지 확인하고자 하실 경우 개장일여부(opnd_yn)을 사용하시면 됩니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5c488ab2-59fd-486e-bf74-b68e813e35c0` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/chk-holiday` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `CTCA0903R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-12-23
- **최종 수정일**: 2025-05-07

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTCA0903R |
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
| `BASS_DT` | 기준일자 | String | 8 | Y | 기준일자(YYYYMMDD) |
| `CTX_AREA_NK` | 연속조회키 | String | 20 | Y | 공백으로 입력 |
| `CTX_AREA_FK` | 연속조회검색조건 | String | 20 | Y | 공백으로 입력 |

### 요청 예시

```json
{
  "BASS_DT": "20221227",
  "CTX_AREA_NK": "",
  "CTX_AREA_FK": ""
}
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
| `output` | 응답상세1 | String |   | Y |  |
| `bass_dt` | 기준일자 | String | 8 | Y | 기준일자(YYYYMMDD) |
| `wday_dvsn_cd` | 요일구분코드 | String | 2 | Y | 01:일요일, 02:월요일, 03:화요일, 04:수요일, 05:목요일, 06:금요일, 07:토요일 |
| `bzdy_yn` | 영업일여부 | String | 1 | Y | Y/N 금융기관이 업무를 하는 날 |
| `tr_day_yn` | 거래일여부 | String | 1 | Y | Y/N 증권 업무가 가능한 날(입출금, 이체 등의 업무 포함) |
| `opnd_yn` | 개장일여부 | String | 1 | Y | Y/N 주식시장이 개장되는 날 * 주문을 넣고자 할 경우 개장일여부(opnd_yn)를 사용 |
| `sttl_day_yn` | 결제일여부 | String | 1 | Y | Y/N 주식 거래에서 실제로 주식을 인수하고 돈을 지불하는 날 |

### 응답 예시

```json
{
  "ctx_area_nk": "20230119            ",
  "ctx_area_fk": "20221227            ",
  "output": [
    {
      "bass_dt": "20221227",
      "wday_dvsn_cd": "03",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20221228",
      "wday_dvsn_cd": "04",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20221229",
      "wday_dvsn_cd": "05",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20221230",
      "wday_dvsn_cd": "06",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "N",
      "sttl_day_yn": "N"
    },
    {
      "bass_dt": "20221231",
      "wday_dvsn_cd": "07",
      "bzdy_yn": "N",
      "tr_day_yn": "Y",
      "opnd_yn": "N",
      "sttl_day_yn": "N"
    },
    {
      "bass_dt": "20230101",
      "wday_dvsn_cd": "01",
      "bzdy_yn": "N",
      "tr_day_yn": "Y",
      "opnd_yn": "N",
      "sttl_day_yn": "N"
    },
    {
      "bass_dt": "20230102",
      "wday_dvsn_cd": "02",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230103",
      "wday_dvsn_cd": "03",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230104",
      "wday_dvsn_cd": "04",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230105",
      "wday_dvsn_cd": "05",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230106",
      "wday_dvsn_cd": "06",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230107",
      "wday_dvsn_cd": "07",
      "bzdy_yn": "N",
      "tr_day_yn": "Y",
      "opnd_yn": "N",
      "sttl_day_yn": "N"
    },
    {
      "bass_dt": "20230108",
      "wday_dvsn_cd": "01",
      "bzdy_yn": "N",
      "tr_day_yn": "Y",
      "opnd_yn": "N",
      "sttl_day_yn": "N"
    },
    {
      "bass_dt": "20230109",
      "wday_dvsn_cd": "02",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230110",
      "wday_dvsn_cd": "03",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230111",
      "wday_dvsn_cd": "04",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230112",
      "wday_dvsn_cd": "05",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230113",
      "wday_dvsn_cd": "06",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230114",
      "wday_dvsn_cd": "07",
      "bzdy_yn": "N",
      "tr_day_yn": "Y",
      "opnd_yn": "N",
      "sttl_day_yn": "N"
    },
    {
      "bass_dt": "20230115",
      "wday_dvsn_cd": "01",
      "bzdy_yn": "N",
      "tr_day_yn": "Y",
      "opnd_yn": "N",
      "sttl_day_yn": "N"
    },
    {
      "bass_dt": "20230116",
      "wday_dvsn_cd": "02",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230117",
      "wday_dvsn_cd": "03",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230118",
      "wday_dvsn_cd": "04",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    },
    {
      "bass_dt": "20230119",
      "wday_dvsn_cd": "05",
      "bzdy_yn": "Y",
      "tr_day_yn": "Y",
      "opnd_yn": "Y",
      "sttl_day_yn": "Y"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0500",
  "msg1": "조회가 계속됩니다..다음버튼을 Click 하십시오.                                   "
}
```
