# 채권정정취소가능주문조회  [국내주식-126]

> [장내채권] 주문/계좌

채권정정취소가능주문조회 API입니다. 
정정취소가능한 채권주문 목록을 확인할 수 있습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `daf83679-be80-4ce8-9f1d-88e123a9ee0c` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/trading/inquire-psbl-rvsecncl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTSC8035R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26T09:21:45+09:00
- **최종 수정일**: 2025-04-30T13:06:26+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTSC8035R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y |  |
| `ORD_DT` | 주문일자 | String | 8 | Y |  |
| `ODNO` | 주문번호 | String | 10 | Y |  |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
ORD_DT:
ODNO:
CTX_AREA_FK200:
CTX_AREA_NK200:
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
| `odno` | 주문번호 | String | 10 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `rvse_cncl_dvsn_name` | 정정취소구분명 | String | 60 | Y |  |
| `ord_qty` | 주문수량 | String | 10 | Y |  |
| `bond_ord_unpr` | 채권주문단가 | String | 182 | Y |  |
| `ord_tmd` | 주문시각 | String | 6 | Y |  |
| `tot_ccld_qty` | 총체결수량 | String | 10 | Y |  |
| `tot_ccld_amt` | 총체결금액 | String | 19 | Y |  |
| `ord_psbl_qty` | 주문가능수량 | String | 10 | Y |  |
| `orgn_odno` | 원주문번호 | String | 10 | Y |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | Y |  |
| `ord_dvsn_cd` | 주문구분코드 | String | 2 | Y |  |
| `mgco_aptm_odno` | 운용사지정주문번호 | String | 12 | Y |  |
| `samt_mket_ptci_yn` | 소액시장참여여부 | String | 1 | Y |  |
| `prdt_abrv_name` | 상품약어명 | String | 60 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "0!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null                                                                                                                   ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output": [
    {
      "odno": "0000015401",
      "pdno": "KR6095572D81",
      "rvse_cncl_dvsn_name": "현금매수",
      "ord_qty": "1",
      "bond_ord_unpr": "10000.00",
      "ord_tmd": "104258",
      "tot_ccld_qty": "0",
      "tot_ccld_amt": "0",
      "ord_psbl_qty": "1",
      "orgn_odno": "",
      "sll_buy_dvsn_cd": "02",
      "ord_dvsn_cd": "01",
      "mgco_aptm_odno": "",
      "samt_mket_ptci_yn": "N",
      "prdt_abrv_name": "AJ네트웍스63-2"
    },
    {
      "odno": "0000015403",
      "pdno": "KR6095572D81",
      "rvse_cncl_dvsn_name": "현금매도",
      "ord_qty": "1",
      "bond_ord_unpr": "10460.00",
      "ord_tmd": "104448",
      "tot_ccld_qty": "0",
      "tot_ccld_amt": "0",
      "ord_psbl_qty": "1",
      "orgn_odno": "0000015402",
      "sll_buy_dvsn_cd": "01",
      "ord_dvsn_cd": "01",
      "mgco_aptm_odno": "",
      "samt_mket_ptci_yn": "N",
      "prdt_abrv_name": "AJ네트웍스63-2"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```

