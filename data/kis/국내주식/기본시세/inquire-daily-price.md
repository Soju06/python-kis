# 주식현재가 일자별[v1_국내주식-010]

> [국내주식] 기본시세

주식현재가 일자별 API입니다. 일/주/월별 주가를 확인할 수 있으며 최근 30일(주,별)로 제한되어 있습니다.

[국내주식-010 v1] 주식현재가 일자별

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `011d4de2-a4a0-47c0-aa47-20c65a26a763` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-daily-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `FHKST01010400` |
| **TR ID (모의)** | `FHKST01010400` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15T13:00:08+09:00
- **최종 수정일**: 2025-04-30T10:13:13+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST01010400 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |
| `FID_PERIOD_DIV_CODE` | 기간 분류 코드 | String | 32 | Y | 'D : (일)최근 30거래일  W : (주)최근 30주  M : (월)최근 30개월' |
| `FID_ORG_ADJ_PRC` | 수정주가 원주가 가격 | String | 10 | Y | '0 : 수정주가미반영 1 : 수정주가반영 * 수정주가는 액면분할/액면병합 등 권리 발생 시 과거 시세를 현재 주가에 맞게 보정한 가격' |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "000660",
  "fid_org_adj_prc": "0000000001",
  "fid_period_div_code": "D"
}
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
| `output` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `stck_clpr` | 주식 종가 | String | 10 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vrss_vol_rate` | 전일 대비 거래량 비율 | String | 84 | Y | 13(8.4) |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y | 11(8.2) |
| `hts_frgn_ehrt` | HTS 외국인 소진율 | String | 82 | Y | 11(8.2) |
| `frgn_ntby_qty` | 외국인 순매수 수량 | String | 12 | Y |  |
| `flng_cls_code` | 락 구분 코드 | String | 2 | Y | '01 : 권리락  02 : 배당락  03 : 분배락  04 : 권배락  05 : 중간(분기)배당락  06 : 권리중간배당락  07 : 권리분기배당락' |
| `acml_prtt_rate` | 누적 분할 비율 | String | 84 | Y | 13(8.4) |

### 응답 예시

```json
{
  "output": [
    {
      "stck_bsop_date": "20220111",
      "stck_oprc": "125500",
      "stck_hgpr": "128500",
      "stck_lwpr": "124500",
      "stck_clpr": "128000",
      "acml_vol": "3908418",
      "prdy_vrss_vol_rate": "13.31",
      "prdy_vrss": "3500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.81",
      "hts_frgn_ehrt": "49.39",
      "frgn_ntby_qty": "0",
      "flng_cls_code": "00",
      "acml_prtt_rate": "1.00"
    },
    {
      "stck_bsop_date": "20220110",
      "stck_oprc": "126500",
      "stck_hgpr": "127000",
      "stck_lwpr": "123000",
      "stck_clpr": "124500",
      "acml_vol": "3449197",
      "prdy_vrss_vol_rate": "5.48",
      "prdy_vrss": "-2500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.97",
      "hts_frgn_ehrt": "49.39",
      "frgn_ntby_qty": "293389",
      "flng_cls_code": "00",
      "acml_prtt_rate": "0.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다!"
}
```

