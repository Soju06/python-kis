# 장내채권 발행정보[국내주식-156]

> [장내채권] 기본시세

장내채권 발행정보 API입니다.
한국투자 HTS(eFriend Plus) > [7216] 채권 발행정보 화면의 상단 채권정보 데이터를 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `cf45db98-43d0-476a-8774-d9690365300a` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/quotations/issue-info` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `CTPF1101R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
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
| `tr_id` | 거래ID | String | 13 | Y | CTPF1101R |
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
| `PDNO` | 사용자권한정보 | String | 12 | Y | 채권 종목번호(ex. KR6449111CB8) |
| `PRDT_TYPE_CD` | 거래소코드 | String | 3 | Y | Unique key(302) |

### 요청 예시

```json
PDNO:KR6449111CB8
PRDT_TYPE_CD:302
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
| `output` | 응답상세 | String |   | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `prdt_eng_name` | 상품영문명 | String | 60 | Y |  |
| `ivst_heed_prdt_yn` | 투자유의상품여부 | String | 1 | Y |  |
| `exts_yn` | 연장여부 | String | 1 | Y |  |
| `bond_clsf_cd` | 채권분류코드 | String | 6 | Y |  |
| `bond_clsf_kor_name` | 채권분류한글명 | String | 60 | Y |  |
| `papr` | 액면가 | String | 19 | Y |  |
| `int_mned_dvsn_cd` | 이자월말구분코드 | String | 1 | Y |  |
| `rvnu_shap_cd` | 매출형태코드 | String | 1 | Y |  |
| `issu_amt` | 발행금액 | String | 19 | Y |  |
| `lstg_rmnd` | 상장잔액 | String | 19 | Y |  |
| `int_dfrm_mcnt` | 이자지급개월수 | String | 6 | Y |  |
| `bond_int_dfrm_mthd_cd` | 채권이자지급방법코드 | String | 2 | Y |  |
| `splt_rdpt_rcnt` | 분할상환횟수 | String | 6 | Y |  |
| `prca_dfmt_term_mcnt` | 원금거치기간개월수 | String | 6 | Y |  |
| `int_anap_dvsn_cd` | 이자선후급구분코드 | String | 1 | Y |  |
| `bond_rght_dvsn_cd` | 채권권리구분코드 | String | 2 | Y |  |
| `prdt_pclc_text` | 상품특성내용 | String | 500 | Y |  |
| `prdt_abrv_name` | 상품약어명 | String | 60 | Y |  |
| `prdt_eng_abrv_name` | 상품영문약어명 | String | 60 | Y |  |
| `sprx_psbl_yn` | 분리과세가능여부 | String | 1 | Y |  |
| `pbff_pplc_ofrg_mthd_cd` | 공모사모모집방법코드 | String | 2 | Y |  |
| `cmco_cd` | 주간사코드 | String | 4 | Y |  |
| `issu_istt_cd` | 발행기관코드 | String | 5 | Y |  |
| `issu_istt_name` | 발행기관명 | String | 60 | Y |  |
| `pnia_dfrm_agcy_istt_cd` | 원리금지급대행기관코드 | String | 4 | Y |  |
| `dsct_ec_rt` | 할인할증율 | String | 238 | Y |  |
| `srfc_inrt` | 표면이율 | String | 238 | Y |  |
| `expd_rdpt_rt` | 만기상환율 | String | 238 | Y |  |
| `expd_asrc_erng_rt` | 만기보장수익율 | String | 238 | Y |  |
| `bond_grte_istt_name` | 채권보증기관명 | String | 60 | Y |  |
| `int_dfrm_day_type_cd` | 이자지급일유형코드 | String | 2 | Y |  |
| `ksd_int_calc_unit_cd` | 증권예탁결제원이자계산단위코드 | String | 1 | Y |  |
| `int_wunt_uder_prcs_dvsn_cd` | 이자원화단위미만처리구분코드 | String | 1 | Y |  |
| `rvnu_dt` | 매출일자 | String | 8 | Y |  |
| `issu_dt` | 발행일자 | String | 8 | Y |  |
| `lstg_dt` | 상장일자 | String | 8 | Y |  |
| `expd_dt` | 만기일자 | String | 8 | Y |  |
| `rdpt_dt` | 상환일자 | String | 8 | Y |  |
| `sbst_pric` | 대용가격 | String | 19 | Y |  |
| `rgbf_int_dfrm_dt` | 직전이자지급일자 | String | 8 | Y |  |
| `nxtm_int_dfrm_dt` | 차기이자지급일자 | String | 8 | Y |  |
| `frst_int_dfrm_dt` | 최초이자지급일자 | String | 8 | Y |  |
| `ecis_pric` | 행사가격 | String | 19 | Y |  |
| `rght_stck_std_pdno` | 권리주식표준상품번호 | String | 12 | Y |  |
| `ecis_opng_dt` | 행사개시일자 | String | 8 | Y |  |
| `ecis_end_dt` | 행사종료일자 | String | 8 | Y |  |
| `bond_rvnu_mthd_cd` | 채권매출방법코드 | String | 2 | Y |  |
| `oprt_stfno` | 조작직원번호 | String | 6 | Y |  |
| `oprt_stff_name` | 조작직원명 | String | 60 | Y |  |
| `rgbf_int_dfrm_wday` | 직전이자지급요일 | String | 2 | Y |  |
| `nxtm_int_dfrm_wday` | 차기이자지급요일 | String | 2 | Y |  |
| `kis_crdt_grad_text` | 한국신용평가신용등급내용 | String | 500 | Y |  |
| `kbp_crdt_grad_text` | 한국채권평가신용등급내용 | String | 500 | Y |  |
| `nice_crdt_grad_text` | 한국신용정보신용등급내용 | String | 500 | Y |  |
| `fnp_crdt_grad_text` | 에프앤자산평가신용등급내용 | String | 500 | Y |  |
| `dpsi_psbl_yn` | 예탁가능여부 | String | 1 | Y |  |
| `pnia_int_calc_unpr` | 원리금이자계산단가 | String | 234 | Y |  |
| `prcm_idx_bond_yn` | 물가지수채권여부 | String | 1 | Y |  |
| `expd_exts_srdp_rcnt` | 만기연장분할상환횟수 | String | 10 | Y |  |
| `expd_exts_srdp_rt` | 만기연장분할상환율 | String | 2212 | Y |  |
| `loan_psbl_yn` | 대출가능여부 | String | 1 | Y |  |
| `grte_dvsn_cd` | 보증구분코드 | String | 1 | Y |  |
| `fnrr_rank_dvsn_cd` | 선후순위구분코드 | String | 1 | Y |  |
| `krx_lstg_abol_dvsn_cd` | 한국거래소상장폐지구분코드 | String | 1 | Y |  |
| `asst_rqdi_dvsn_cd` | 자산유동화구분코드 | String | 2 | Y |  |
| `opcb_dvsn_cd` | 옵션부사채구분코드 | String | 1 | Y |  |
| `crfd_item_yn` | 크라우드펀딩종목여부 | String | 1 | Y |  |
| `crfd_item_rstc_cclc_dt` | 크라우드펀딩종목제한해지일자 | String | 8 | Y |  |
| `bond_nmpr_unit_pric` | 채권호가단위가격 | String | 202 | Y |  |
| `ivst_heed_bond_dvsn_name` | 투자유의채권구분명 | String | 60 | Y |  |
| `add_erng_rt` | 추가수익율 | String | 238 | Y |  |
| `add_erng_rt_aply_dt` | 추가수익율적용일자 | String | 8 | Y |  |
| `bond_tr_stop_dvsn_cd` | 채권거래정지구분코드 | String | 1 | Y |  |
| `ivst_heed_bond_dvsn_cd` | 투자유의채권구분코드 | String | 1 | Y |  |
| `pclr_cndt_text` | 특이조건내용 | String | 500 | Y |  |
| `hbbd_yn` | 하이브리드채권여부 | String | 1 | Y |  |
| `cdtl_cptl_scty_type_cd` | 조건부자본증권유형코드 | String | 1 | Y |  |
| `elec_scty_yn` | 전자증권여부 | String | 1 | Y |  |
| `sq1_clop_ecis_opng_dt` | 1차콜옵션행사개시일자 | String | 8 | Y |  |
| `frst_erlm_stfno` | 최초등록직원번호 | String | 6 | Y |  |
| `frst_erlm_dt` | 최초등록일자 | String | 8 | Y |  |
| `frst_erlm_tmd` | 최초등록시각 | String | 6 | Y |  |
| `tlg_rcvg_dtl_dtime` | 전문수신상세일시 | String | 17 | Y |  |

### 응답 예시

```json
{
  "output": {
    "pdno": "KR6449111CB8",
    "prdt_type_cd": "302",
    "prdt_name": "2022기보제일차유동화전문1-1(사)",
    "prdt_eng_name": "2022 KIBO 1st Securitization Specialty1-1(S)",
    "ivst_heed_prdt_yn": "N",
    "exts_yn": "N",
    "bond_clsf_cd": "116100",
    "bond_clsf_kor_name": "일반사채",
    "papr": "10000",
    "int_mned_dvsn_cd": "1",
    "rvnu_shap_cd": "2",
    "issu_amt": "77839700000",
    "lstg_rmnd": "77839700000",
    "int_dfrm_mcnt": "3",
    "bond_int_dfrm_mthd_cd": "03",
    "splt_rdpt_rcnt": "0",
    "prca_dfmt_term_mcnt": "0",
    "int_anap_dvsn_cd": "2",
    "bond_rght_dvsn_cd": "",
    "prdt_pclc_text": "",
    "prdt_abrv_name": "2022기보제일차유1-1(사)",
    "prdt_eng_abrv_name": "2022 KIBO 1st SEC1-1(S)",
    "sprx_psbl_yn": "N",
    "pbff_pplc_ofrg_mthd_cd": "01",
    "cmco_cd": "2117",
    "issu_istt_cd": "44911",
    "issu_istt_name": "2022기보제일차유동화전문 유한회사",
    "pnia_dfrm_agcy_istt_cd": "1105",
    "dsct_ec_rt": "0.000000",
    "srfc_inrt": "5.931000",
    "expd_rdpt_rt": "0.000000",
    "expd_asrc_erng_rt": "0.000000",
    "bond_grte_istt_name": "2022기보제일차유동화전문 유한회사",
    "int_dfrm_day_type_cd": "01",
    "ksd_int_calc_unit_cd": "1",
    "int_wunt_uder_prcs_dvsn_cd": "1",
    "rvnu_dt": "",
    "issu_dt": "20221116",
    "lstg_dt": "20221116",
    "expd_dt": "20241116",
    "rdpt_dt": "20241116",
    "sbst_pric": "8900",
    "rgbf_int_dfrm_dt": "20240516",
    "nxtm_int_dfrm_dt": "20240816",
    "frst_int_dfrm_dt": "",
    "ecis_pric": "0",
    "rght_stck_std_pdno": "",
    "ecis_opng_dt": "",
    "ecis_end_dt": "",
    "bond_rvnu_mthd_cd": "",
    "oprt_stfno": "BATCH",
    "oprt_stff_name": "",
    "rgbf_int_dfrm_wday": "05",
    "nxtm_int_dfrm_wday": "06",
    "kis_crdt_grad_text": "AAA",
    "kbp_crdt_grad_text": "AAA",
    "nice_crdt_grad_text": "AAA",
    "fnp_crdt_grad_text": "AAA",
    "dpsi_psbl_yn": "Y",
    "pnia_int_calc_unpr": "0",
    "prcm_idx_bond_yn": "N",
    "expd_exts_srdp_rcnt": "0",
    "expd_exts_srdp_rt": "0",
    "loan_psbl_yn": "N",
    "grte_dvsn_cd": "4",
    "fnrr_rank_dvsn_cd": "1",
    "krx_lstg_abol_dvsn_cd": "Y",
    "asst_rqdi_dvsn_cd": "11",
    "opcb_dvsn_cd": "",
    "crfd_item_yn": "N",
    "crfd_item_rstc_cclc_dt": "",
    "bond_nmpr_unit_pric": "0.100000",
    "ivst_heed_bond_dvsn_name": "",
    "add_erng_rt": "0.000000",
    "add_erng_rt_aply_dt": "",
    "bond_tr_stop_dvsn_cd": "N",
    "ivst_heed_bond_dvsn_cd": "0",
    "pclr_cndt_text": "",
    "hbbd_yn": "N",
    "cdtl_cptl_scty_type_cd": "",
    "elec_scty_yn": "Y",
    "sq1_clop_ecis_opng_dt": "",
    "frst_erlm_stfno": "",
    "frst_erlm_dt": "",
    "frst_erlm_tmd": ""
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0530",
  "msg1": "조회되었습니다                                                                  "
}
```
