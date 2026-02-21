# 주식정정취소가능주문조회[v1_국내주식-004]

> [국내주식] 주문/계좌

주식정정취소가능주문조회 API입니다. 한 번의 호출에 최대 50건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

※ 주식주문(정정취소) 호출 전에 반드시 주식정정취소가능주문조회 호출을 통해 정정취소가능수량(output > psbl_qty)을 확인하신 후 정정취소주문 내시기 바랍니다.

[국내주식-004 v1] 주식정정취소가능주문조회

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `d4537e9c-73f7-414c-9fb0-4eae3bc397d0` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC0084R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15T12:57:48+09:00
- **최종 수정일**: 2025-04-30T09:58:38+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | ※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] (구)TTTC8036R → (신)TTTC0084R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y | '공란 : 최초 조회시는  이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)' |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y | '공란 : 최초 조회시  이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)' |
| `INQR_DVSN_1` | 조회구분1 | String | 1 | Y | '0 주문 1 종목' |
| `INQR_DVSN_2` | 조회구분2 | String | 1 | Y | '0 전체 1 매도 2 매수' |

### 요청 예시

```json
{
  "ACNT_PRDT_CD": "01",
  "CANO": "810XXXXX",
  "CTX_AREA_FK100": "",
  "CTX_AREA_NK100": "",
  "INQR_DVSN_1": "0",
  "INQR_DVSN_2": "0"
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | Object |   | Y | array |
| `ord_gno_brno` | 주문채번지점번호 | String | 5 | Y | 주문시 한국투자증권 시스템에서 지정된 영업점코드 |
| `odno` | 주문번호 | String | 10 | Y | 주문시 한국투자증권 시스템에서 채번된 주문번호 |
| `orgn_odno` | 원주문번호 | String | 6 | Y | 정정/취소주문 인경우 원주문번호 |
| `ord_dvsn_name` | 주문구분명 | String | 5 | Y |  |
| `pdno` | 상품번호 | String | 10 | Y | 종목번호(뒤 6자리만 해당) |
| `prdt_name` | 상품명 | String | 6 | Y | 종목명 |
| `rvse_cncl_dvsn_name` | 정정취소구분명 | String | 5 | Y | 정정 또는 취소 여부 표시 |
| `ord_qty` | 주문수량 | String | 10 | Y |  |
| `ord_unpr` | 주문단가 | String | 6 | Y | 1주당 주문가격 |
| `ord_tmd` | 주문시각 | String | 5 | Y | 주문시각(시분초HHMMSS) |
| `tot_ccld_qty` | 총체결수량 | String | 10 | Y | 주문 수량 중 체결된 수량 |
| `tot_ccld_amt` | 총체결금액 | String | 6 | Y | 주문금액 중 체결금액 |
| `psbl_qty` | 가능수량 | String | 5 | Y | 정정/취소 주문 가능 수량 |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 10 | Y | 01 : 매도 / 02 : 매수 |
| `ord_dvsn_cd` | 주문구분코드 | String | 6 | Y | [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) 21 : 중간가 22 : 스톱지정가 23 : 중간가IOC 24 : 중간가FOK  [NXT] 00 : 지정가 03 : 최유리지정가 04 : 최우선지정가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) 21 : 중간가 22 : 스톱지정가 23 : 중간가IOC 24 : 중간가FOK  [SOR] 00 : 지정가 01 : 시장가 03 : 최유리지정가 04 : 최우선지정가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) |
| `mgco_aptm_odno` | 운용사지정주문번호 | String | 5 | Y |  |
| `excg_dvsn_cd` | 거래소구분코드 | String | 2 | Y |  |
| `excg_id_dvsn_cd` | 거래소ID구분코드 | String | 3 | Y |  |
| `excg_id_dvsn_name` | 거래소ID구분명 | String | 100 | Y |  |
| `stpm_cndt_pric` | 스톱지정가조건가격 | String | 9 | Y |  |
| `stpm_efct_occr_yn` | 스톱지정가효력발생여부 | String | 1 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "81055689^01^                                                                                        ",
  "ctx_area_nk100": "                                                                                                    ",
  "output": [
    {
      "ord_gno_brno": "06010",
      "odno": "0001569139",
      "orgn_odno": "0001569136",
      "ord_dvsn_name": "지정가",
      "pdno": "009150",
      "prdt_name": "SamsungElecMech",
      "rvse_cncl_dvsn_name": "BUY AMEND*",
      "ord_qty": "1",
      "ord_unpr": "140000",
      "ord_tmd": "131438",
      "tot_ccld_qty": "0",
      "tot_ccld_amt": "0",
      "psbl_qty": "1",
      "sll_buy_dvsn_cd": "02",
      "ord_dvsn_cd": "00",
      "mgco_aptm_odno": ""
    },
    {
      "ord_gno_brno": "06010",
      "odno": "0001569138",
      "orgn_odno": "",
      "ord_dvsn_name": "지정가",
      "pdno": "009150",
      "prdt_name": "SamsungElecMech",
      "rvse_cncl_dvsn_name": "",
      "ord_qty": "1",
      "ord_unpr": "200000",
      "ord_tmd": "131421",
      "tot_ccld_qty": "0",
      "tot_ccld_amt": "0",
      "psbl_qty": "1",
      "sll_buy_dvsn_cd": "02",
      "ord_dvsn_cd": "00",
      "mgco_aptm_odno": ""
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

