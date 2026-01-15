# 투자계좌자산현황조회[v1_국내주식-048]

> [국내주식] 주문/계좌

투자계좌자산현황조회 API입니다.

output1은 한국투자 HTS(eFriend Plus) > [0891] 계좌 자산비중(결제기준) 화면 아래 테이블의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `052c663e-73db-43ee-b1a0-702a14de31fc` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/inquire-account-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `CTRP6548R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-04-21
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
| `tr_id` | 거래ID | String | 13 | Y | CTRP6548R |
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
| `INQR_DVSN_1` | 조회구분1 | String | 1 | Y | 공백입력 |
| `BSPR_BF_DT_APLY_YN` | 기준가이전일자적용여부 | String | 1 | Y | 공백입력 |

### 요청 예시

```json
{
	"CANO":"12345678",
	"ACNT_PRDT_CD":"01",
	"INQR_DVSN_1":"",
	"BSPR_BF_DT_APLY_YN":"",
}
```

## 응답 (Response)

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
| `Output1` | 응답상세 | Object |   | Y | Array [아래 순서대로 출력 : 20항목] 1: 주식 2: 펀드/MMW 3: IMA 4: 채권 5: ELS/DLS 6: WRAP 7: 신탁 8: RP/발행어음 9: 해외주... |
| `pchs_amt` | 매입금액 | String | 19 | Y |  |
| `evlu_amt` | 평가금액 | String | 19 | Y |  |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y |  |
| `crdt_lnd_amt` | 신용대출금액 | String | 19 | Y |  |
| `real_nass_amt` | 실제순자산금액 | String | 19 | Y |  |
| `whol_weit_rt` | 전체비중율 | String | 228 | Y |  |
| `Output2` | 응답상세2 | String |   | Y |  |
| `pchs_amt_smtl` | 매입금액합계 | String | 19 | Y | 유가매입금액 |
| `nass_tot_amt` | 순자산총금액 | String | 19 | Y |  |
| `loan_amt_smtl` | 대출금액합계 | String | 19 | Y |  |
| `evlu_pfls_amt_smtl` | 평가손익금액합계 | String | 19 | Y | 평가손익금액 |
| `evlu_amt_smtl` | 평가금액합계 | String | 19 | Y | 유가평가금액 |
| `tot_asst_amt` | 총자산금액 | String | 19 | Y | 총 자산금액 |
| `tot_lnda_tot_ulst_lnda` | 총대출금액총융자대출금액 | String | 19 | Y |  |
| `cma_auto_loan_amt` | CMA자동대출금액 | String | 19 | Y |  |
| `tot_mgln_amt` | 총담보대출금액 | String | 19 | Y |  |
| `stln_evlu_amt` | 대주평가금액 | String | 19 | Y |  |
| `crdt_fncg_amt` | 신용융자금액 | String | 19 | Y |  |
| `ocl_apl_loan_amt` | OCL_APL대출금액 | String | 19 | Y |  |
| `pldg_stup_amt` | 질권설정금액 | String | 19 | Y |  |
| `frcr_evlu_tota` | 외화평가총액 | String | 19 | Y |  |
| `tot_dncl_amt` | 총예수금액 | String | 19 | Y |  |
| `cma_evlu_amt` | CMA평가금액 | String | 19 | Y |  |
| `dncl_amt` | 예수금액 | String | 19 | Y |  |
| `tot_sbst_amt` | 총대용금액 | String | 19 | Y |  |
| `thdt_rcvb_amt` | 당일미수금액 | String | 20 | Y |  |
| `ovrs_stck_evlu_amt1` | 해외주식평가금액1 | String | 236 | Y |  |
| `ovrs_bond_evlu_amt` | 해외채권평가금액 | String | 236 | Y |  |
| `mmf_cma_mgge_loan_amt` | MMFCMA담보대출금액 | String | 19 | Y |  |
| `sbsc_dncl_amt` | 청약예수금액 | String | 19 | Y |  |
| `pbst_sbsc_fnds_loan_use_amt` | 공모주청약자금대출사용금액 | String | 20 | Y |  |
| `etpr_crdt_grnt_loan_amt` | 기업신용공여대출금액 | String | 19 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "pchs_amt": "129105",
      "evlu_amt": "406000",
      "evlu_pfls_amt": "276895",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "406000",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "161026228",
      "evlu_amt": "185144504",
      "evlu_pfls_amt": "24118276",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "185144504",
      "whol_weit_rt": "0.01000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "1651434483743",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "1651434483743",
      "whol_weit_rt": "99.97000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "249855300",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "249855300",
      "whol_weit_rt": "0.01000000"
    },
    {
      "pchs_amt": "0",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "0",
      "whol_weit_rt": "0.00000000"
    },
    {
      "pchs_amt": "161155333",
      "evlu_amt": "1651869889547",
      "evlu_pfls_amt": "24395171",
      "crdt_lnd_amt": "0",
      "real_nass_amt": "1651869889547",
      "whol_weit_rt": "100.00000000"
    }
  ],
  "output2": {
    "pchs_amt_smtl": "161155333",
    "nass_tot_amt": "185550504",
    "loan_amt_smtl": "0",
    "evlu_pfls_amt_smtl": "24395171",
    "evlu_amt_smtl": "185550504",
    "tot_asst_amt": "1651869889547",
    "tot_lnda_tot_ulst_lnda": "0",
    "cma_auto_loan_amt": "0",
    "tot_mgln_amt": "0",
    "stln_evlu_amt": "0",
    "crdt_fncg_amt": "0",
    "ocl_apl_loan_amt": "0",
    "pldg_stup_amt": "0",
    "frcr_evlu_tota": "1651434483743",
    "tot_dncl_amt": "249855300",
    "cma_evlu_amt": "0",
    "dncl_amt": "249855300",
    "tot_sbst_amt": "0",
    "thdt_rcvb_amt": "0",
    "ovrs_stck_evlu_amt1": "185144504.000000",
    "ovrs_bond_evlu_amt": "0.000000",
    "mmf_cma_mgge_loan_amt": "0",
    "sbsc_dncl_amt": "0",
    "pbst_sbsc_fnds_loan_use_amt": "0",
    "etpr_crdt_grnt_loan_amt": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0530",
  "msg1": "조회되었습니다                                                                  "
}
```
