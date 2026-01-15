# 주식통합증거금 현황 [국내주식-191]

> [국내주식] 주문/계좌

주식통합증거금 현황 API입니다.
한국투자 HTS(eFriend Plus) > [0867] 통합증거금조회 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 해당 화면은 일반계좌와 통합증거금 신청계좌에 대해서 국내 및 해외 주문가능금액을 간단하게 조회하는 화면입니다.
※ 해외 국가별 상세한 증거금현황을 원하시면 [해외주식] 주문/계좌 > 해외증거금 통화별조회 API를 이용하여 주시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `32b7ac44-2d64-466d-9343-7e9d4e7ab0e4` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/intgr-margin` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC0869R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | TTTC0869R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `CMA_EVLU_AMT_ICLD_YN` | CMA평가금액포함여부 | String | 1 | Y | N 입력 |
| `WCRC_FRCR_DVSN_CD` | 원화외화구분코드 | String | 2 | Y | 01(외화기준),02(원화기준) |
| `FWEX_CTRT_FRCR_DVSN_CD` | 선도환계약외화구분코드 | String | 2 | Y | 01(외화기준),02(원화기준) |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
CMA_EVLU_AMT_ICLD_YN:N
WCRC_FRCR_DVSN_CD:01
FWEX_CTRT_FRCR_DVSN_CD:01
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
| `output` | 응답상세 | String |   | Y |  |
| `acmga_rt` | 계좌증거금율 | String | 114 | Y |  |
| `acmga_pct100_aptm_rson` | 계좌증거금100퍼센트지정사유 | String | 100 | Y |  |
| `stck_cash_objt_amt` | 주식현금대상금액 | String | 184 | Y |  |
| `stck_sbst_objt_amt` | 주식대용대상금액 | String | 184 | Y |  |
| `stck_evlu_objt_amt` | 주식평가대상금액 | String | 184 | Y |  |
| `stck_ruse_psbl_objt_amt` | 주식재사용가능대상금액 | String | 184 | Y |  |
| `stck_fund_rpch_chgs_objt_amt` | 주식펀드환매대금대상금액 | String | 184 | Y |  |
| `stck_fncg_rdpt_objt_atm` | 주식융자상환금대상금액 | String | 184 | Y |  |
| `bond_ruse_psbl_objt_amt` | 채권재사용가능대상금액 | String | 184 | Y |  |
| `stck_cash_use_amt` | 주식현금사용금액 | String | 184 | Y |  |
| `stck_sbst_use_amt` | 주식대용사용금액 | String | 184 | Y |  |
| `stck_evlu_use_amt` | 주식평가사용금액 | String | 184 | Y |  |
| `stck_ruse_psbl_amt_use_amt` | 주식재사용가능금사용금액 | String | 184 | Y |  |
| `stck_fund_rpch_chgs_use_amt` | 주식펀드환매대금사용금액 | String | 184 | Y |  |
| `stck_fncg_rdpt_amt_use_amt` | 주식융자상환금사용금액 | String | 184 | Y |  |
| `bond_ruse_psbl_amt_use_amt` | 채권재사용가능금사용금액 | String | 184 | Y |  |
| `stck_cash_ord_psbl_amt` | 주식현금주문가능금액 | String | 184 | Y |  |
| `stck_sbst_ord_psbl_amt` | 주식대용주문가능금액 | String | 184 | Y |  |
| `stck_evlu_ord_psbl_amt` | 주식평가주문가능금액 | String | 184 | Y |  |
| `stck_ruse_psbl_ord_psbl_amt` | 주식재사용가능주문가능금액 | String | 184 | Y |  |
| `stck_fund_rpch_ord_psbl_amt` | 주식펀드환매주문가능금액 | String | 184 | Y |  |
| `bond_ruse_psbl_ord_psbl_amt` | 채권재사용가능주문가능금액 | String | 184 | Y |  |
| `rcvb_amt` | 미수금액 | String | 19 | Y |  |
| `stck_loan_grta_ruse_psbl_amt` | 주식대출보증금재사용가능금액 | String | 184 | Y |  |
| `stck_cash20_max_ord_psbl_amt` | 주식현금20최대주문가능금액 | String | 184 | Y |  |
| `stck_cash30_max_ord_psbl_amt` | 주식현금30최대주문가능금액 | String | 184 | Y |  |
| `stck_cash40_max_ord_psbl_amt` | 주식현금40최대주문가능금액 | String | 184 | Y |  |
| `stck_cash50_max_ord_psbl_amt` | 주식현금50최대주문가능금액 | String | 184 | Y |  |
| `stck_cash60_max_ord_psbl_amt` | 주식현금60최대주문가능금액 | String | 184 | Y |  |
| `stck_cash100_max_ord_psbl_amt` | 주식현금100최대주문가능금액 | String | 184 | Y |  |
| `stck_rsip100_max_ord_psbl_amt` | 주식재사용불가100최대주문가능 | String | 184 | Y |  |
| `bond_max_ord_psbl_amt` | 채권최대주문가능금액 | String | 184 | Y |  |
| `stck_fncg45_max_ord_psbl_amt` | 주식융자45최대주문가능금액 | String | 182 | Y |  |
| `stck_fncg50_max_ord_psbl_amt` | 주식융자50최대주문가능금액 | String | 184 | Y |  |
| `stck_fncg60_max_ord_psbl_amt` | 주식융자60최대주문가능금액 | String | 184 | Y |  |
| `stck_fncg70_max_ord_psbl_amt` | 주식융자70최대주문가능금액 | String | 182 | Y |  |
| `stck_stln_max_ord_psbl_amt` | 주식대주최대주문가능금액 | String | 184 | Y |  |
| `lmt_amt` | 한도금액 | String | 19 | Y |  |
| `ovrs_stck_itgr_mgna_dvsn_name` | 해외주식통합증거금구분명 | String | 40 | Y |  |
| `usd_objt_amt` | 미화대상금액 | String | 182 | Y |  |
| `usd_use_amt` | 미화사용금액 | String | 182 | Y |  |
| `usd_ord_psbl_amt` | 미화주문가능금액 | String | 182 | Y |  |
| `hkd_objt_amt` | 홍콩달러대상금액 | String | 182 | Y |  |
| `hkd_use_amt` | 홍콩달러사용금액 | String | 182 | Y |  |
| `hkd_ord_psbl_amt` | 홍콩달러주문가능금액 | String | 182 | Y |  |
| `jpy_objt_amt` | 엔화대상금액 | String | 182 | Y |  |
| `jpy_use_amt` | 엔화사용금액 | String | 182 | Y |  |
| `jpy_ord_psbl_amt` | 엔화주문가능금액 | String | 182 | Y |  |
| `cny_objt_amt` | 위안화대상금액 | String | 182 | Y |  |
| `cny_use_amt` | 위안화사용금액 | String | 182 | Y |  |
| `cny_ord_psbl_amt` | 위안화주문가능금액 | String | 182 | Y |  |
| `usd_ruse_objt_amt` | 미화재사용대상금액 | String | 182 | Y |  |
| `usd_ruse_amt` | 미화재사용금액 | String | 182 | Y |  |
| `usd_ruse_ord_psbl_amt` | 미화재사용주문가능금액 | String | 182 | Y |  |
| `hkd_ruse_objt_amt` | 홍콩달러재사용대상금액 | String | 182 | Y |  |
| `hkd_ruse_amt` | 홍콩달러재사용금액 | String | 182 | Y |  |
| `hkd_ruse_ord_psbl_amt` | 홍콩달러재사용주문가능금액 | String | 172 | Y |  |
| `jpy_ruse_objt_amt` | 엔화재사용대상금액 | String | 182 | Y |  |
| `jpy_ruse_amt` | 엔화재사용금액 | String | 182 | Y |  |
| `jpy_ruse_ord_psbl_amt` | 엔화재사용주문가능금액 | String | 182 | Y |  |
| `cny_ruse_objt_amt` | 위안화재사용대상금액 | String | 182 | Y |  |
| `cny_ruse_amt` | 위안화재사용금액 | String | 182 | Y |  |
| `cny_ruse_ord_psbl_amt` | 위안화재사용주문가능금액 | String | 182 | Y |  |
| `usd_gnrl_ord_psbl_amt` | 미화일반주문가능금액 | String | 182 | Y |  |
| `usd_itgr_ord_psbl_amt` | 미화통합주문가능금액 | String | 182 | Y |  |
| `hkd_gnrl_ord_psbl_amt` | 홍콩달러일반주문가능금액 | String | 182 | Y |  |
| `hkd_itgr_ord_psbl_amt` | 홍콩달러통합주문가능금액 | String | 182 | Y |  |
| `jpy_gnrl_ord_psbl_amt` | 엔화일반주문가능금액 | String | 182 | Y |  |
| `jpy_itgr_ord_psbl_amt` | 엔화통합주문가능금액 | String | 182 | Y |  |
| `cny_gnrl_ord_psbl_amt` | 위안화일반주문가능금액 | String | 182 | Y |  |
| `cny_itgr_ord_psbl_amt` | 위안화통합주문가능금액 | String | 182 | Y |  |
| `stck_itgr_cash20_ord_psbl_amt` | 주식통합현금20주문가능금액 | String | 182 | Y |  |
| `stck_itgr_cash30_ord_psbl_amt` | 주식통합현금30주문가능금액 | String | 182 | Y |  |
| `stck_itgr_cash40_ord_psbl_amt` | 주식통합현금40주문가능금액 | String | 182 | Y |  |
| `stck_itgr_cash50_ord_psbl_amt` | 주식통합현금50주문가능금액 | String | 182 | Y |  |
| `stck_itgr_cash60_ord_psbl_amt` | 주식통합현금60주문가능금액 | String | 182 | Y |  |
| `stck_itgr_cash100_ord_psbl_amt` | 주식통합현금100주문가능금액 | String | 182 | Y |  |
| `stck_itgr_100_ord_psbl_amt` | 주식통합100주문가능금액 | String | 182 | Y |  |
| `stck_itgr_fncg45_ord_psbl_amt` | 주식통합융자45주문가능금액 | String | 182 | Y |  |
| `stck_itgr_fncg50_ord_psbl_amt` | 주식통합융자50주문가능금액 | String | 182 | Y |  |
| `stck_itgr_fncg60_ord_psbl_amt` | 주식통합융자60주문가능금액 | String | 182 | Y |  |
| `stck_itgr_fncg70_ord_psbl_amt` | 주식통합융자70주문가능금액 | String | 182 | Y |  |
| `stck_itgr_stln_ord_psbl_amt` | 주식통합대주주문가능금액 | String | 182 | Y |  |
| `bond_itgr_ord_psbl_amt` | 채권통합주문가능금액 | String | 182 | Y |  |
| `stck_cash_ovrs_use_amt` | 주식현금해외사용금액 | String | 182 | Y |  |
| `stck_sbst_ovrs_use_amt` | 주식대용해외사용금액 | String | 182 | Y |  |
| `stck_evlu_ovrs_use_amt` | 주식평가해외사용금액 | String | 182 | Y |  |
| `stck_re_use_amt_ovrs_use_amt` | 주식재사용금액해외사용금액 | String | 182 | Y |  |
| `stck_fund_rpch_ovrs_use_amt` | 주식펀드환매해외사용금액 | String | 182 | Y |  |
| `stck_fncg_rdpt_ovrs_use_amt` | 주식융자상환해외사용금액 | String | 182 | Y |  |
| `bond_re_use_ovrs_use_amt` | 채권재사용해외사용금액 | String | 182 | Y |  |
| `usd_oth_mket_use_amt` | 미화타시장사용금액 | String | 182 | Y |  |
| `jpy_oth_mket_use_amt` | 엔화타시장사용금액 | String | 182 | Y |  |
| `cny_oth_mket_use_amt` | 위안화타시장사용금액 | String | 182 | Y |  |
| `hkd_oth_mket_use_amt` | 홍콩달러타시장사용금액 | String | 182 | Y |  |
| `usd_re_use_oth_mket_use_amt` | 미화재사용타시장사용금액 | String | 182 | Y |  |
| `jpy_re_use_oth_mket_use_amt` | 엔화재사용타시장사용금액 | String | 182 | Y |  |
| `cny_re_use_oth_mket_use_amt` | 위안화재사용타시장사용금액 | String | 182 | Y |  |
| `hkd_re_use_oth_mket_use_amt` | 홍콩달러재사용타시장사용금액 | String | 182 | Y |  |
| `hgkg_cny_re_use_amt` | 홍콩위안화재사용금액 | String | 182 | Y |  |
| `usd_frst_bltn_exrt` | 미국달러최초고시환율 | String | 23 | Y |  |
| `hkd_frst_bltn_exrt` | 홍콩달러최초고시환율 | String | 23 | Y |  |
| `jpy_frst_bltn_exrt` | 일본엔화최초고시환율 | String | 23 | Y |  |
| `cny_frst_bltn_exrt` | 중국위안화최초고시환율 | String | 23 | Y |  |

### 응답 예시

```json
{
    "output": {
        "acmga_rt": "100.0000",
        "acmga_pct100_aptm_rson": "고객100%신청",
        "stck_cash_objt_amt": "249855306.0000",
        "stck_sbst_objt_amt": "137816.0000",
        "stck_evlu_objt_amt": "176966.0000",
        "stck_ruse_psbl_objt_amt": "261213.0000",
        "stck_fund_rpch_chgs_objt_amt": "0.0000",
        "stck_fncg_rdpt_objt_atm": "0.0000",
        "bond_ruse_psbl_objt_amt": "1024.0000",
        "stck_cash_use_amt": "240482730.0000",
        "stck_sbst_use_amt": "20295.0000",
        "stck_evlu_use_amt": "20295.0000",
        "stck_ruse_psbl_amt_use_amt": "261213.0000",
        "stck_fund_rpch_chgs_use_amt": "0.0000",
        "stck_fncg_rdpt_amt_use_amt": "0.0000",
        "bond_ruse_psbl_amt_use_amt": "1024.0000",
        "stck_cash_ord_psbl_amt": "9372576.0000",
        "stck_sbst_ord_psbl_amt": "117521.0000",
        "stck_evlu_ord_psbl_amt": "156671.0000",
        "stck_ruse_psbl_ord_psbl_amt": "0.0000",
        "stck_fund_rpch_ord_psbl_amt": "0.0000",
        "bond_ruse_psbl_ord_psbl_amt": "0.0000",
        "rcvb_amt": "0",
        "stck_loan_grta_ruse_psbl_amt": "0.0000",
        "stck_cash20_max_ord_psbl_amt": "8128560.1990",
        "stck_cash30_max_ord_psbl_amt": "8128560.1990",
        "stck_cash40_max_ord_psbl_amt": "8128560.1990",
        "stck_cash50_max_ord_psbl_amt": "8128560.1990",
        "stck_cash60_max_ord_psbl_amt": "8128560.1990",
        "stck_cash100_max_ord_psbl_amt": "8128560.1990",
        "stck_rsip100_max_ord_psbl_amt": "8128560.1990",
        "bond_max_ord_psbl_amt": "9316675.9443",
        "stck_fncg45_max_ord_psbl_amt": "20942905.49",
        "stck_fncg50_max_ord_psbl_amt": "18869350.4950",
        "stck_fncg60_max_ord_psbl_amt": "15750449.5868",
        "stck_fncg70_max_ord_psbl_amt": "13516343.26",
        "stck_stln_max_ord_psbl_amt": "9307424.0318",
        "lmt_amt": "0",
        "ovrs_stck_itgr_mgna_dvsn_name": "",
        "usd_objt_amt": "0.00",
        "usd_use_amt": "0.00",
        "usd_ord_psbl_amt": "0.00",
        "hkd_objt_amt": "0.00",
        "hkd_use_amt": "0.00",
        "hkd_ord_psbl_amt": "0.00",
        "jpy_objt_amt": "0.00",
        "jpy_use_amt": "0.00",
        "jpy_ord_psbl_amt": "0.00",
        "cny_objt_amt": "0.00",
        "cny_use_amt": "0.00",
        "cny_ord_psbl_amt": "0.00",
        "usd_ruse_objt_amt": "0.00",
        "usd_ruse_amt": "0.00",
        "usd_ruse_ord_psbl_amt": "0.00",
        "hkd_ruse_objt_amt": "0.00",
        "hkd_ruse_amt": "0.00",
        "hkd_ruse_ord_psbl_amt": "0.00",
        "jpy_ruse_objt_amt": "0.00",
        "jpy_ruse_amt": "0.00",
        "jpy_ruse_ord_psbl_amt": "0.00",
        "cny_ruse_objt_amt": "0.00",
        "cny_ruse_amt": "0.00",
        "cny_ruse_ord_psbl_amt": "0.00",
        "usd_gnrl_ord_psbl_amt": "0.00",
        "usd_itgr_ord_psbl_amt": "0.00",
        "hkd_gnrl_ord_psbl_amt": "0.00",
        "hkd_itgr_ord_psbl_amt": "0.00",
        "jpy_gnrl_ord_psbl_amt": "0.00",
        "jpy_itgr_ord_psbl_amt": "0.00",
        "cny_gnrl_ord_psbl_amt": "0.00",
        "cny_itgr_ord_psbl_amt": "0.00",
        "stck_itgr_cash20_ord_psbl_amt": "0.00",
        "stck_itgr_cash30_ord_psbl_amt": "0.00",
        "stck_itgr_cash40_ord_psbl_amt": "0.00",
        "stck_itgr_cash50_ord_psbl_amt": "0.00",
        "stck_itgr_cash60_ord_psbl_amt": "0.00",
        "stck_itgr_cash100_ord_psbl_amt": "0.00",
        "stck_itgr_100_ord_psbl_amt": "0.00",
        "stck_itgr_fncg45_ord_psbl_amt": "0.00",
        "stck_itgr_fncg50_ord_psbl_amt": "0.00",
        "stck_itgr_fncg60_ord_psbl_amt": "0.00",
        "stck_itgr_fncg70_ord_psbl_amt": "0.00",
        "stck_itgr_stln_ord_psbl_amt": "0.00",
        "bond_itgr_ord_psbl_amt": "0.00",
        "stck_cash_ovrs_use_amt": "0.00",
        "stck_sbst_ovrs_use_amt": "0.00",
        "stck_evlu_ovrs_use_amt": "0.00",
        "stck_re_use_amt_ovrs_use_amt": "0.00",
        "stck_fund_rpch_ovrs_use_amt": "0.00",
        "stck_fncg_rdpt_ovrs_use_amt": "0.00",
        "bond_re_use_ovrs_use_amt": "0.00",
        "usd_oth_mket_use_amt": "0.00",
        "jpy_oth_mket_use_amt": "0.00",
        "cny_oth_mket_use_amt": "0.00",
        "hkd_oth_mket_use_amt": "0.00",
        "usd_re_use_oth_mket_use_amt": "0.00",
        "jpy_re_use_oth_mket_use_amt": "0.00",
        "cny_re_use_oth_mket_use_amt": "0.00",
        "hkd_re_use_oth_mket_use_amt": "0.00",
        "hgkg_cny_re_use_amt": "0.00",
        "hgkg_cny_re_use_objt_amt": "0.00",
        "hgkg_cny_re_use_ord_psbl_amt": "0.00",
        "hgkg_cny_re_use_oth_use_amt": "0.00"
        "hgkg_cny_re_use_oth_use_amt": "0.00",
        "usd_frst_bltn_exrt": "1467.00000000",
        "hkd_frst_bltn_exrt": "188.61000000",
        "jpy_frst_bltn_exrt": "10.06000000",
        "cny_frst_bltn_exrt": "200.70000000"
    },
    "rt_cd": "0",
    "msg_cd": "KIOK0510",
    "msg1": "조회가 완료되었습니다                                                           "
}
```

