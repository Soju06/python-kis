# 장내채권 기본조회 [국내주식-129]

> [장내채권] 기본시세

장내채권 기본조회 API입니다. 
장내채권의 상품정보를 확인 가능합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `56cf546c-a74f-467c-98b1-005967535e9e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/quotations/search-bond-info` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTPF1114R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
- **최종 수정일**: 2025-10-28

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTPF1114R |
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
| `PDNO` | 상품번호 | String | 12 | Y | 상품번호 |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | Unique key(302) |

### 요청 예시

```json
PDNO:KR2033022D33
PRDT_TYPE_CD:302
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
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `ksd_bond_item_name` | 증권예탁결제원채권종목명 | String | 100 | Y |  |
| `ksd_bond_item_eng_name` | 증권예탁결제원채권종목영문명 | String | 100 | Y |  |
| `ksd_bond_lstg_type_cd` | 증권예탁결제원채권상장유형코드 | String | 2 | Y |  |
| `ksd_ofrg_dvsn_cd` | 증권예탁결제원모집구분코드 | String | 2 | Y |  |
| `ksd_bond_int_dfrm_dvsn_cd` | 증권예탁결제원채권이자지급구분 | String | 1 | Y |  |
| `issu_dt` | 발행일자 | String | 8 | Y |  |
| `rdpt_dt` | 상환일자 | String | 8 | Y |  |
| `rvnu_dt` | 매출일자 | String | 8 | Y |  |
| `iso_crcy_cd` | 통화코드 | String | 3 | Y |  |
| `mdwy_rdpt_dt` | 중도상환일자 | String | 8 | Y |  |
| `ksd_rcvg_bond_dsct_rt` | 증권예탁결제원수신채권할인율 | String | 2212 | Y |  |
| `ksd_rcvg_bond_srfc_inrt` | 증권예탁결제원수신채권표면이율 | String | 2012 | Y |  |
| `bond_expd_rdpt_rt` | 채권만기상환율 | String | 2212 | Y |  |
| `ksd_prca_rdpt_mthd_cd` | 증권예탁결제원원금상환방법코드 | String | 2 | Y |  |
| `int_caltm_mcnt` | 이자계산기간개월수 | String | 10 | Y |  |
| `ksd_int_calc_unit_cd` | 증권예탁결제원이자계산단위코드 | String | 1 | Y | 1.발행금액 2.만원 3.십만원 4.백만원 |
| `uval_cut_dvsn_cd` | 절상절사구분코드 | String | 1 | Y |  |
| `uval_cut_dcpt_dgit` | 절상절사소수점자릿수 | String | 10 | Y |  |
| `ksd_dydv_caltm_aply_dvsn_cd` | 증권예탁결제원일할계산기간적용 | String | 1 | Y |  |
| `dydv_calc_dcnt` | 일할계산일수 | String | 5 | Y |  |
| `bond_expd_asrc_erng_rt` | 채권만기보장수익율 | String | 2212 | Y |  |
| `padf_plac_hdof_name` | 원리금지급장소본점명 | String | 60 | Y |  |
| `lstg_dt` | 상장일자 | String | 8 | Y |  |
| `lstg_abol_dt` | 상장폐지일자 | String | 8 | Y |  |
| `ksd_bond_issu_mthd_cd` | 증권예탁결제원채권발행방법코드 | String | 1 | Y |  |
| `laps_indf_yn` | 경과이자지급여부 | String | 1 | Y |  |
| `ksd_lhdy_pnia_dfrm_mthd_cd` | 증권예탁결제원공휴일원리금지급 | String | 1 | Y |  |
| `frst_int_dfrm_dt` | 최초이자지급일자 | String | 8 | Y |  |
| `ksd_prcm_lnkg_gvbd_yn` | 증권예탁결제원물가연동국고채여 | String | 1 | Y |  |
| `dpsi_end_dt` | 예탁종료일자 | String | 8 | Y |  |
| `dpsi_strt_dt` | 예탁시작일자 | String | 8 | Y |  |
| `dpsi_psbl_yn` | 예탁가능여부 | String | 1 | Y |  |
| `atyp_rdpt_bond_erlm_yn` | 비정형상환채권등록여부 | String | 1 | Y |  |
| `dshn_occr_yn` | 부도발생여부 | String | 1 | Y |  |
| `expd_exts_yn` | 만기연장여부 | String | 1 | Y |  |
| `pclr_ptcr_text` | 특이사항내용 | String | 500 | Y |  |
| `dpsi_psbl_excp_stat_cd` | 예탁가능예외상태코드 | String | 2 | Y |  |
| `expd_exts_srdp_rcnt` | 만기연장분할상환횟수 | String | 10 | Y |  |
| `expd_exts_srdp_rt` | 만기연장분할상환율 | String | 2212 | Y |  |
| `expd_rdpt_rt` | 만기상환율 | String | 238 | Y |  |
| `expd_asrc_erng_rt` | 만기보장수익율 | String | 238 | Y |  |
| `bond_int_dfrm_mthd_cd` | 채권이자지급방법코드 | String | 2 | Y | 01.할인채 02.복리채 03.이표채.확정금리 04.이표채.금리연동 05.이표채.변동금리 06.단리채 07.분할채 09.복5단2 19.기타.고정금리 29.기타.변동금리 |
| `int_dfrm_day_type_cd` | 이자지급일유형코드 | String | 2 | Y | 01.발행일 02.만기일 03.특정일 |
| `prca_dfmt_term_mcnt` | 원금거치기간개월수 | String | 6 | Y |  |
| `splt_rdpt_rcnt` | 분할상환횟수 | String | 6 | Y |  |
| `rgbf_int_dfrm_dt` | 직전이자지급일자 | String | 8 | Y |  |
| `nxtm_int_dfrm_dt` | 차기이자지급일자 | String | 8 | Y |  |
| `sprx_psbl_yn` | 분리과세가능여부 | String | 1 | Y |  |
| `ictx_rt_dvsn_cd` | 소득세율구분코드 | String | 2 | Y |  |
| `bond_clsf_cd` | 채권분류코드 | String | 6 | Y |  |
| `bond_clsf_kor_name` | 채권분류한글명 | String | 60 | Y |  |
| `int_mned_dvsn_cd` | 이자월말구분코드 | String | 1 | Y | 1.일자기준 2.말일기준 |
| `pnia_int_calc_unpr` | 원리금이자계산단가 | String | 234 | Y |  |
| `frn_intr` | FRN금리 | String | 1512 | Y |  |
| `aply_day_prcm_idx_lnkg_cefc` | 적용일물가지수연동계수 | String | 151 | Y |  |
| `ksd_expd_dydv_calc_bass_cd` | 증권예탁결제원만기일할계산기준 | String | 1 | Y |  |
| `expd_dydv_calc_dcnt` | 만기일할계산일수 | String | 7 | Y |  |
| `ksd_cbbw_dvsn_cd` | 증권예탁결제원신종사채구분코드 | String | 1 | Y |  |
| `crfd_item_yn` | 크라우드펀딩종목여부 | String | 1 | Y |  |
| `pnia_bank_ofdy_dfrm_mthd_cd` | 원리금은행휴무일지급방법코드 | String | 1 | Y |  |
| `qib_yn` | QIB여부 | String | 1 | Y |  |
| `qib_cclc_dt` | QIB해지일자 | String | 8 | Y |  |
| `csbd_yn` | 영구채여부 | String | 1 | Y |  |
| `csbd_cclc_dt` | 영구채해지일자 | String | 8 | Y |  |
| `ksd_opcb_yn` | 증권예탁결제원옵션부사채여부 | String | 1 | Y |  |
| `ksd_sodn_yn` | 증권예탁결제원후순위채권여부 | String | 1 | Y |  |
| `ksd_rqdi_scty_yn` | 증권예탁결제원유동화증권여부 | String | 1 | Y |  |
| `elec_scty_yn` | 전자증권여부 | String | 1 | Y |  |
| `rght_ecis_mbdy_dvsn_cd` | 권리행사주체구분코드 | String | 1 | Y |  |
| `int_rkng_mthd_dvsn_cd` | 이자산정방법구분코드 | String | 1 | Y |  |
| `ofrg_dvsn_cd` | 모집구분코드 | String | 2 | Y |  |
| `ksd_tot_issu_amt` | 증권예탁결제원총발행금액 | String | 202 | Y |  |
| `next_indf_chk_ecls_yn` | 다음이자지급체크제외여부 | String | 1 | Y |  |
| `ksd_bond_intr_dvsn_cd` | 증권예탁결제원채권금리구분코드 | String | 1 | Y |  |
| `ksd_inrt_aply_dvsn_cd` | 증권예탁결제원이율적용구분코드 | String | 1 | Y |  |
| `krx_issu_istt_cd` | KRX발행기관코드 | String | 5 | Y |  |
| `ksd_indf_frqc_uder_calc_cd` | 증권예탁결제원이자지급주기미만 | String | 1 | Y |  |
| `ksd_indf_frqc_uder_calc_dcnt` | 증권예탁결제원이자지급주기미만 | String | 4 | Y |  |
| `tlg_rcvg_dtl_dtime` | 전문수신상세일시 | String | 17 | Y |  |

### 응답 예시

```json
{
  "output": {
    "pdno": "KR2033022D33",
    "prdt_type_cd": "302",
    "ksd_bond_item_name": "충북지역개발채권 23-03",
    "ksd_bond_item_eng_name": "CHUNGBUK PROVINCIAL DEVELOPMENT 23-03",
    "ksd_bond_lstg_type_cd": "11",
    "ksd_ofrg_dvsn_cd": "11",
    "ksd_bond_int_dfrm_dvsn_cd": "3",
    "issu_dt": "20230331",
    "rdpt_dt": "20280331",
    "rvnu_dt": "20230302",
    "iso_crcy_cd": "KRW",
    "mdwy_rdpt_dt": "00000000",
    "ksd_rcvg_bond_dsct_rt": "0.000000000000",
    "ksd_rcvg_bond_srfc_inrt": "2.500000000000",
    "bond_expd_rdpt_rt": "100.000000000000",
    "ksd_prca_rdpt_mthd_cd": "11",
    "int_caltm_mcnt": "12",
    "ksd_int_calc_unit_cd": "1",
    "uval_cut_dvsn_cd": "2",
    "uval_cut_dcpt_dgit": "0",
    "ksd_dydv_caltm_aply_dvsn_cd": "1",
    "dydv_calc_dcnt": "0",
    "bond_expd_asrc_erng_rt": "0.000000000000",
    "padf_plac_hdof_name": "농협은행",
    "lstg_dt": "20230302",
    "lstg_abol_dt": "20280401",
    "ksd_bond_issu_mthd_cd": "2",
    "laps_indf_yn": "Y",
    "ksd_lhdy_pnia_dfrm_mthd_cd": "2",
    "frst_int_dfrm_dt": "00000000",
    "ksd_prcm_lnkg_gvbd_yn": "N",
    "dpsi_end_dt": "20280401",
    "dpsi_strt_dt": "20230302",
    "dpsi_psbl_yn": "Y",
    "atyp_rdpt_bond_erlm_yn": "N",
    "dshn_occr_yn": "N",
    "expd_exts_yn": "N",
    "pclr_ptcr_text": "",
    "dpsi_psbl_excp_stat_cd": "",
    "expd_exts_srdp_rcnt": "0",
    "expd_exts_srdp_rt": "0.000000000000",
    "expd_rdpt_rt": "0.00000000",
    "expd_asrc_erng_rt": "0.00000000",
    "bond_int_dfrm_mthd_cd": "02",
    "int_dfrm_day_type_cd": "02",
    "prca_dfmt_term_mcnt": "0",
    "splt_rdpt_rcnt": "0",
    "rgbf_int_dfrm_dt": "",
    "nxtm_int_dfrm_dt": "20280331",
    "sprx_psbl_yn": "N",
    "ictx_rt_dvsn_cd": "",
    "bond_clsf_cd": "112555",
    "bond_clsf_kor_name": "충북지역개발채권",
    "int_mned_dvsn_cd": "2",
    "pnia_int_calc_unpr": "0.0000",
    "frn_intr": "0.000000000000",
    "aply_day_prcm_idx_lnkg_cefc": "0.0000000000",
    "ksd_expd_dydv_calc_bass_cd": "",
    "expd_dydv_calc_dcnt": "0",
    "ksd_cbbw_dvsn_cd": "9",
    "crfd_item_yn": "N",
    "pnia_bank_ofdy_dfrm_mthd_cd": "1",
    "qib_yn": "N",
    "qib_cclc_dt": "00000000",
    "csbd_yn": "N",
    "csbd_cclc_dt": "00000000",
    "ksd_opcb_yn": "N",
    "ksd_sodn_yn": "N",
    "ksd_rqdi_scty_yn": "N",
    "elec_scty_yn": "Y",
    "rght_ecis_mbdy_dvsn_cd": "1",
    "int_rkng_mthd_dvsn_cd": "1",
    "ofrg_dvsn_cd": "",
    "ksd_tot_issu_amt": "17303560000.00",
    "next_indf_chk_ecls_yn": "N",
    "ksd_bond_intr_dvsn_cd": "1",
    "ksd_inrt_aply_dvsn_cd": "1",
    "krx_issu_istt_cd": "MB033",
    "ksd_indf_frqc_uder_calc_cd": "1",
    "ksd_indf_frqc_uder_calc_dcnt": "0",
    "tlg_rcvg_dtl_dtime": "20240625060514023"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0530",
  "msg1": "조회되었습니다                                                                  "
}
```

