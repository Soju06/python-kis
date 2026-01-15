# 주식현재가 투자자[v1_국내주식-012]

> [국내주식] 기본시세

주식현재가 투자자 API입니다. 개인, 외국인, 기관 등 투자 정보를 확인할 수 있습니다.

[유의사항]
- 외국인은 외국인(외국인투자등록 고유번호가 있는 경우)+기타 외국인을 지칭합니다.
- 당일 데이터는 장 종료 후 제공됩니다.

[국내주식-012 v1] 주식현재가 투자자

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `e27baf2f-6ec0-4029-b4fd-4c873f340478` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-investor` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHKST01010900` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST01010900 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J : KRX, NX : NXT, UN : 통합 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "000660"
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
| `output` | 응답상세 | Object |   | Y | Array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_clpr` | 주식 종가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prsn_ntby_qty` | 개인 순매수 수량 | String | 12 | Y |  |
| `frgn_ntby_qty` | 외국인 순매수 수량 | String | 12 | Y |  |
| `orgn_ntby_qty` | 기관계 순매수 수량 | String | 18 | Y |  |
| `prsn_ntby_tr_pbmn` | 개인 순매수 거래 대금 | String | 18 | Y |  |
| `frgn_ntby_tr_pbmn` | 외국인 순매수 거래 대금 | String | 18 | Y |  |
| `orgn_ntby_tr_pbmn` | 기관계 순매수 거래 대금 | String | 18 | Y |  |
| `prsn_shnu_vol` | 개인 매수2 거래량 | String | 18 | Y |  |
| `frgn_shnu_vol` | 외국인 매수2 거래량 | String | 18 | Y |  |
| `orgn_shnu_vol` | 기관계 매수2 거래량 | String | 18 | Y |  |
| `prsn_shnu_tr_pbmn` | 개인 매수2 거래 대금 | String | 18 | Y |  |
| `frgn_shnu_tr_pbmn` | 외국인 매수2 거래 대금 | String | 18 | Y |  |
| `orgn_shnu_tr_pbmn` | 기관계 매수2 거래 대금 | String | 18 | Y |  |
| `prsn_seln_vol` | 개인 매도 거래량 | String | 18 | Y |  |
| `frgn_seln_vol` | 외국인 매도 거래량 | String | 18 | Y |  |
| `orgn_seln_vol` | 기관계 매도 거래량 | String | 18 | Y |  |
| `prsn_seln_tr_pbmn` | 개인 매도 거래 대금 | String | 18 | Y |  |
| `frgn_seln_tr_pbmn` | 외국인 매도 거래 대금 | String | 18 | Y |  |
| `orgn_seln_tr_pbmn` | 기관계 매도 거래 대금 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_bsop_date": "20220113",
      "stck_clpr": "129500",
      "prdy_vrss": "1000",
      "prdy_vrss_sign": "2",
      "prsn_ntby_qty": "-287624",
      "frgn_ntby_qty": "797458",
      "orgn_ntby_qty": "-503653",
      "prsn_ntby_tr_pbmn": "-37176",
      "frgn_ntby_tr_pbmn": "102959",
      "orgn_ntby_tr_pbmn": "-64984",
      "prsn_shnu_vol": "467525",
      "frgn_shnu_vol": "1442791",
      "orgn_shnu_vol": "2219433",
      "prsn_shnu_tr_pbmn": "60368",
      "frgn_shnu_tr_pbmn": "186166",
      "orgn_shnu_tr_pbmn": "286505",
      "prsn_seln_vol": "755149",
      "frgn_seln_vol": "645333",
      "orgn_seln_vol": "2723086",
      "prsn_seln_tr_pbmn": "97544",
      "frgn_seln_tr_pbmn": "83207",
      "orgn_seln_tr_pbmn": "351489"
    },
    {
      "stck_bsop_date": "20220112",
      "stck_clpr": "128500",
      "prdy_vrss": "500",
      "prdy_vrss_sign": "2",
      "prsn_ntby_qty": "-74249",
      "frgn_ntby_qty": "-134600",
      "orgn_ntby_qty": "206812",
      "prsn_ntby_tr_pbmn": "-9687",
      "frgn_ntby_tr_pbmn": "-17094",
      "orgn_ntby_tr_pbmn": "26530",
      "prsn_shnu_vol": "608748",
      "frgn_shnu_vol": "721756",
      "orgn_shnu_vol": "2201966",
      "prsn_shnu_tr_pbmn": "77943",
      "frgn_shnu_tr_pbmn": "92615",
      "orgn_shnu_tr_pbmn": "281965",
      "prsn_seln_vol": "682997",
      "frgn_seln_vol": "856356",
      "orgn_seln_vol": "1995154",
      "prsn_seln_tr_pbmn": "87630",
      "frgn_seln_tr_pbmn": "109708",
      "orgn_seln_tr_pbmn": "255435"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다!"
}
```
