# (야간)선물옵션 증거금 상세 [국내선물-024]

> [국내선물옵션] 주문/계좌

(야간)선물옵션 증거금상세 API입니다.
한국투자 HTS(eFriend Force) > [2537] 야간선물옵션 증거금상세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `07126b90-256e-4b93-b0be-e1e59dfc89f0` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/ngt-margin-detail` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `(구) JTCE6003R (신) CTFN7107R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-06-06

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | (구) JTCE6003R (신) CTFN7107R |
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
| `MGNA_DVSN_CD` | 증거금 구분코드 | String | 2 | Y | 위탁(01), 유지(02) |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:03
MGNA_DVSN_CD:01
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
| `output1` | 응답상세 | Object |   | Y | array 아래 18가지 항목이 순서대로 출력됨 (1) A. 신규증거금 - 선물 - 1.개별종목 (2) A. 신규증거금 - 선물 - 2.스프레드 (3) A. 신규증거금 - 3... |
| `cash_amt` | 현금금액 | String | 19 | Y |  |
| `tot_amt` | 총금액 | String | 19 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array 아래 5가지 항목이 순서대로 출력됨 (1) 예수금 (2) 인출가능금액 (3) 주문가능금액 ﻿﻿(4) 위탁증거금액 ﻿﻿(5) 추가증거금액  ※ 인출가능금액은 정산 후... |
| `cash_amt` | 현금금액 | String | 19 | Y |  |
| `sbst_amt` | 대용금액 | String | 19 | Y |  |
| `tot_amt` | 총금액 | String | 19 | Y |  |
| `output3` | 응답상세 | String |   | Y |  |
| `base_dpsa_gdat_grad_cd` | 기본예탁금차등등급코드 | String | 2 | Y |  |
| `bfdy_sbst_sll_ccld_amt` | 전일대용매도체결금액 | String | 19 | Y |  |
| `bfdy_sbst_sll_sbst_amt` | 전일대용매도대용금액 | String | 19 | Y |  |
| `excc_dfpa` | 정산차금 | String | 19 | Y |  |
| `fee_amt` | 수수료금액 | String | 19 | Y |  |
| `nxdy_dncl_amt` | 익일예수금액 | String | 19 | Y |  |
| `opt_base_dpsa_gdat_grad_cd` | 옵션기본예탁금차등등급코드 | String | 2 | Y |  |
| `opt_buy_exus_acnt_yn` | 옵션매수전용계좌여부 | String | 1 | Y |  |
| `opt_dfpa` | 옵션차금 | String | 19 | Y |  |
| `prsm_dpast_amt` | 추정예탁자산금액 | String | 19 | Y |  |
| `thdt_sbst_sll_ccld_amt` | 당일대용매도체결금액 | String | 19 | Y |  |
| `thdt_sbst_sll_sbst_amt` | 당일대용매도대용금액 | String | 19 | Y |  |
| `output1` | 응답상세 | Object |   | Y | Array 신 TR 사용 필드 |
| `futr_new_mgn_amt` | 선물신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_sprd_ord_mgna` | 선물스프레드주문증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_sll_new_mgn_amt` | 옵션매도신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_buy_new_mgn_amt` | 옵션매수신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `new_mgn_amt` | 신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_pric_mgna` | 옵션가격증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `fuop_pric_altr_mgna` | 선물옵션가격변동증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_sprd_mgna` | 선물스프레드증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `uwdl_mgna` | 인수도증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `ctrt_per_min_mgna` | 계약당최소증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `tot_risk_mgna` | 총위험증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `netrisk_brkg_mgna` | 순위험위탁증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_sll_chgs` | 옵션매도대금 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_buy_chgs` | 옵션매수대금 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_loss_amt` | 선물손실금액 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_prft_amt` | 선물이익금액 | String | 19 | Y | 신 TR 사용 필드 |
| `thdt_ccld_net_loss_amt` | 당일체결순손실금액 | String | 19 | Y | 신 TR 사용 필드 |
| `brkg_mgna` | 위탁증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `output2` | 응답상세 | Object |   | Y | Array 신 TR 사용 필드 |
| `futr_new_mgn_amt` | 선물신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_sprd_ord_mgna` | 선물스프레드주문증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_sll_new_mgn_amt` | 옵션매도신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_buy_new_mgn_amt` | 옵션매수신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `new_mgn_amt` | 신규증거금액 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_pric_mgna` | 옵션가격증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `fuop_pric_altr_mgna` | 선물옵션가격변동증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_sprd_mgna` | 선물스프레드증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `uwdl_mgna` | 인수도증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `ctrt_per_min_mgna` | 계약당최소증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `tot_risk_mgna` | 총위험증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `netrisk_brkg_mgna` | 순위험위탁증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_sll_chgs` | 옵션매도대금 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_buy_chgs` | 옵션매수대금 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_loss_amt` | 선물손실금액 | String | 19 | Y | 신 TR 사용 필드 |
| `futr_prft_amt` | 선물이익금액 | String | 19 | Y | 신 TR 사용 필드 |
| `thdt_ccld_net_loss_amt` | 당일체결순손실금액 | String | 19 | Y | 신 TR 사용 필드 |
| `brkg_mgna` | 위탁증거금 | String | 19 | Y | 신 TR 사용 필드 |
| `output3` | 응답상세 | String |   | Y | Single 신 TR 사용 필드 |
| `dnca_cash` | 예수금현금 | String | 19 | Y | 신 TR 사용 필드 |
| `dnca_sbst` | 예수금대용 | String | 19 | Y | 신 TR 사용 필드 |
| `dnca_tota` | 예수금총액 | String | 19 | Y | 신 TR 사용 필드 |
| `wdrw_psbl_cash_amt` | 인출가능현금금액 | String | 19 | Y | 신 TR 사용 필드 |
| `wdrw_psbl_sbsa` | 인출가능대용금액 | String | 19 | Y | 신 TR 사용 필드 |
| `wdrw_psbl_tot_amt` | 인출가능총금액 | String | 19 | Y | 신 TR 사용 필드 |
| `ord_psbl_cash_amt` | 주문가능현금금액 | String | 19 | Y | 신 TR 사용 필드 |
| `ord_psbl_sbsa` | 주문가능대용금액 | String | 19 | Y | 신 TR 사용 필드 |
| `ord_psbl_tot_amt` | 주문가능총금액 | String | 19 | Y | 신 TR 사용 필드 |
| `brkg_mgna_cash_amt` | 위탁증거금현금금액 | String | 19 | Y | 신 TR 사용 필드 |
| `brkg_mgna_sbst` | 위탁증거금대용 | String | 19 | Y | 신 TR 사용 필드 |
| `brkg_mgna_tot_amt` | 위탁증거금총금액 | String | 19 | Y | 신 TR 사용 필드 |
| `add_mgna_cash_amt` | 추가증거금현금금액 | String | 19 | Y | 신 TR 사용 필드 |
| `add_mgna_sbsa` | 추가증거금대용금액 | String | 19 | Y | 신 TR 사용 필드 |
| `add_mgna_tot_amt` | 추가증거금총금액 | String | 19 | Y | 신 TR 사용 필드 |
| `bfdy_sbst_sll_sbst_amt` | 전일대용매도대용금액 | String | 19 | Y | 신 TR 사용 필드 |
| `thdt_sbst_sll_sbst_amt` | 당일대용매도대용금액 | String | 19 | Y | 신 TR 사용 필드 |
| `bfdy_sbst_sll_ccld_amt` | 전일대용매도체결금액 | String | 19 | Y | 신 TR 사용 필드 |
| `thdt_sbst_sll_ccld_amt` | 당일대용매도체결금액 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_dfpa` | 옵션차금 | String | 19 | Y | 신 TR 사용 필드 |
| `excc_dfpa` | 정산차금 | String | 19 | Y | 신 TR 사용 필드 |
| `fee_amt` | 수수료금액 | String | 19 | Y | 신 TR 사용 필드 |
| `nxdy_dncl_amt` | 익일예수금액 | String | 19 | Y | 신 TR 사용 필드 |
| `prsm_dpast_amt` | 추정예탁자산금액 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_buy_exus_acnt_yn` | 옵션매수전용계좌여부 | String | 19 | Y | 신 TR 사용 필드 |
| `base_dpsa_gdat_grad_cd` | 기본예탁금차등등급코드 | String | 19 | Y | 신 TR 사용 필드 |
| `opt_base_dpsa_gdat_grad_cd` | 옵션기본예탁금차등등급코드 | String | 19 | Y | 신 TR 사용 필드 |

### 응답 예시

```json
{
  "output1": [
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "tot_amt": "0"
    }
  ],
  "output2": [
    {
      "cash_amt": "100000000",
      "sbst_amt": "0",
      "tot_amt": "100000000"
    },
    {
      "cash_amt": "100000000",
      "sbst_amt": "0",
      "tot_amt": "100000000"
    },
    {
      "cash_amt": "100000000",
      "sbst_amt": "0",
      "tot_amt": "100000000"
    },
    {
      "cash_amt": "0",
      "sbst_amt": "0",
      "tot_amt": "0"
    },
    {
      "cash_amt": "0",
      "sbst_amt": "0",
      "tot_amt": "0"
    }
  ],
  "output3": {
    "bfdy_sbst_sll_sbst_amt": "0",
    "thdt_sbst_sll_sbst_amt": "0",
    "bfdy_sbst_sll_ccld_amt": "0",
    "thdt_sbst_sll_ccld_amt": "0",
    "opt_buy_exus_acnt_yn": "N",
    "base_dpsa_gdat_grad_cd": "03",
    "opt_dfpa": "0",
    "excc_dfpa": "0",
    "fee_amt": "0",
    "nxdy_dncl_amt": "100000000",
    "prsm_dpast_amt": "100000000",
    "opt_base_dpsa_gdat_grad_cd": "01"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

