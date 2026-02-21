# 퇴직연금 체결기준잔고[v1_국내주식-032]

> [국내주식] 주문/계좌

​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다.
KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.

퇴직연금 체결기준잔고[v1_국내주식-032]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `6e8dc8ed-f026-497c-a40c-098448a94241` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/pension/inquire-present-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC2202R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-28T15:10:26+09:00
- **최종 수정일**: 2025-04-30T10:07:41+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | TTTC2202R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 29 |
| `USER_DVSN_CD` | 사용자구분코드 | String | 2 | Y | 00 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y |  |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y |  |

### 요청 예시

```json
{
  "CANO": "63512345",
  "ACNT_PRDT_CD": "29",
  "USER_DVSN_CD": "00",
  "CTX_AREA_FK100": "",
  "CTX_AREA_NK100": ""
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
| `output1` | 응답상세1 | Object |   | Y | Array |
| `cblc_dvsn` | 잔고구분 | String | 2 | Y |  |
| `cblc_dvsn_name` | 잔고구분명 | String | 60 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `hldg_qty` | 보유수량 | String | 19 | Y |  |
| `slpsb_qty` | 매도가능수량 | String | 10 | Y |  |
| `pchs_avg_pric` | 매입평균가격 | String | 184 | Y |  |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y |  |
| `evlu_pfls_rt` | 평가손익율 | String | 72 | Y |  |
| `prpr` | 현재가 | String | 19 | Y |  |
| `evlu_amt` | 평가금액 | String | 19 | Y |  |
| `pchs_amt` | 매입금액 | String | 19 | Y |  |
| `cblc_weit` | 잔고비중 | String | 238 | Y |  |
| `output2` | 응답상세2 | Object |   | Y | Array |
| `pchs_amt_smtl_amt` | 매입금액합계금액 | String | 19 | Y |  |
| `evlu_amt_smtl_amt` | 평가금액합계금액 | String | 19 | Y |  |
| `evlu_pfls_smtl_amt` | 평가손익합계금액 | String | 19 | Y |  |
| `trad_pfls_smtl` | 매매손익합계 | String | 19 | Y |  |
| `thdt_tot_pfls_amt` | 당일총손익금액 | String | 19 | Y |  |
| `pftrt` | 수익률 | String | 238 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "63512345^29^00^                                                                                     ",
  "ctx_area_nk100": "                                                                                                    ",
  "output1": [
    {
      "cblc_dvsn": "01",
      "cblc_dvsn_name": "사용자",
      "pdno": "069500",
      "prdt_name": "KODEX 200",
      "hldg_qty": "6",
      "slpsb_qty": "6",
      "pchs_avg_pric": "35670.0000",
      "evlu_pfls_amt": "-3330",
      "evlu_pfls_rt": "-1.56",
      "prpr": "35115",
      "evlu_amt": "210690",
      "pchs_amt": "214020",
      "cblc_weit": "53.06651890"
    },
    {
      "cblc_dvsn": "01",
      "cblc_dvsn_name": "사용자",
      "pdno": "091160",
      "prdt_name": "KODEX 반도체",
      "hldg_qty": "7",
      "slpsb_qty": "7",
      "pchs_avg_pric": "35820.0000",
      "evlu_pfls_amt": "-64400",
      "evlu_pfls_rt": "-25.68",
      "prpr": "26620",
      "evlu_amt": "186340",
      "pchs_amt": "250740",
      "cblc_weit": "46.93348110"
    }
  ],
  "output2": [
    {
      "pchs_amt_smtl_amt": "464760",
      "evlu_amt_smtl_amt": "397030",
      "evlu_pfls_smtl_amt": "-67730",
      "trad_pfls_smtl": "0",
      "thdt_tot_pfls_amt": "-67730",
      "pftrt": "-14.57311300"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

