# 해외선물옵션 당일주문내역조회 [v1_해외선물-004]

> [해외선물옵션] 주문/계좌

해외선물옵션 당일주문내역조회 API입니다.

해외선물옵션 당일주문내역조회 [v1_해외선물-004]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `d1d7b8f1-6dc8-4439-a27f-5aa2c73b12f3` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/inquire-ccld` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `OTFM3116R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-08-05
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
| `tr_id` | 거래ID | String | 13 | Y | OTFM3116R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | 법인 : "001" / default   개인: "" |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `CCLD_NCCS_DVSN` | 체결미체결구분 | String | 2 | Y | 01:전체 / 02:체결 / 03:미체결 |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | %%:전체 / 01:매도 / 02:매수 |
| `FUOP_DVSN` | 선물옵션구분 | String | 2 | Y | 00:전체 / 01:선물 / 02:옵션 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |

### 요청 예시

```json
{
	"CANO":"80012345",
	"ACNT_PRDT_CD":"08",
	"CCLD_NCCS_DVSN":"01",
	"SLL_BUY_DVSN_CD":"01",
	"FUOP_DVSN":"00",
	"CTX_AREA_FK100":"",
	"CTX_AREA_NK100":"",
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
| `output` | 응답상세1 | Object |  | N | Array |
| `cano` | 종합계좌번호 | String | 8 | N |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | N |  |
| `ord_dt` | 주문일자 | String | 8 | N |  |
| `odno` | 주문번호 | String | 8 | N | 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송    (ex. ORGN_ODNO : 00360686) |
| `orgn_ord_dt` | 원주문일자 | String | 8 | N |  |
| `orgn_odno` | 원주문번호 | String | 8 | N | 원주문번호(ex. 00360685) |
| `ovrs_futr_fx_pdno` | 해외선물FX상품번호 | String | 32 | N |  |
| `rcit_dvsn_cd` | 접수구분코드 | String | 2 | N | 05	온라인 |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | N | 01:매도, 02:매수 |
| `trad_stgy_dvsn_cd` | 매매전략구분코드 | String | 2 | N |  |
| `bass_pric_type_cd` | 기준가격유형코드 | String | 2 | N | 01	시가평가 02	액면가 03	기준가격 04	대용가 |
| `ord_stat_cd` | 주문상태코드 | String | 2 | N |  |
| `fm_ord_qty` | FM주문수량 | String | 10 | N |  |
| `fm_ord_pric` | FM주문가격 | String | 20 | N |  |
| `fm_stop_ord_pric` | FMSTOP주문가격 | String | 20 | N |  |
| `rsvn_dvsn` | 예약구분 | String | 2 | N |  |
| `fm_ccld_qty` | FM체결수량 | String | 10 | N |  |
| `fm_ccld_pric` | FM체결가격 | String | 20 | N |  |
| `fm_ord_rmn_qty` | FM주문잔여수량 | String | 10 | N |  |
| `ord_grp_name` | 주문그룹명 | String | 60 | N |  |
| `erlm_dtl_dtime` | 등록상세일시 | String | 17 | N |  |
| `ccld_dtl_dtime` | 체결상세일시 | String | 17 | N |  |
| `ord_stfno` | 주문직원번호 | String | 6 | N |  |
| `rmks1` | 비고1 | String | 100 | N |  |
| `new_lqd_dvsn_cd` | 신규청산구분코드 | String | 2 | N | 01	신규 02	청산 |
| `fm_lqd_lmt_ord_pric` | FM청산LIMIT주문가격 | String | 20 | N |  |
| `fm_lqd_stop_pric` | FM청산STOP가격 | String | 20 | N |  |
| `ccld_cndt_cd` | 체결조건코드 | String | 1 | N |  |
| `noti_vald_dt` | 게시유효일자 | String | 8 | N |  |
| `acnt_type_cd` | 계좌유형코드 | String | 2 | N |  |
| `fuop_dvsn` | 선물옵션구분 | String | 2 | N | 01:선물, 02: 옵션 |

### 응답 예시

```json
{
  "ctx_area_fk200": "81012345^08^01^02^00^                                                                                                                                                                                   ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output": [
    {
      "cano": "81012345",
      "acnt_prdt_cd": "08",
      "ord_dt": "20221214",
      "odno": "00298048",
      "orgn_ord_dt": "",
      "orgn_odno": "",
      "ovrs_futr_fx_pdno": "6BZ22",
      "rcit_dvsn_cd": "00",
      "sll_buy_dvsn_cd": "02",
      "trad_stgy_dvsn_cd": "00",
      "bass_pric_type_cd": "1",
      "ord_stat_cd": "02",
      "fm_ord_qty": "1",
      "fm_ord_pric": "1.1700",
      "fm_stop_ord_pric": "0.0000",
      "rsvn_dvsn": "N",
      "fm_ccld_qty": "0",
      "fm_ccld_pric": "0.0000",
      "fm_ord_rmn_qty": "1",
      "ord_grp_name": "",
      "erlm_dtl_dtime": "20221214134455791",
      "ccld_dtl_dtime": "",
      "ord_stfno": "invent",
      "rmks1": "",
      "new_lqd_dvsn_cd": "1",
      "fm_lqd_lmt_ord_pric": "0.0000",
      "fm_lqd_stop_pric": "0.0000",
      "ccld_cndt_cd": "6",
      "noti_vald_dt": "",
      "acnt_type_cd": "1",
      "fuop_dvsn": "01"
    },
    {
      "cano": "81012345",
      "acnt_prdt_cd": "08",
      "ord_dt": "20221214",
      "odno": "00298045",
      "orgn_ord_dt": "20221214",
      "orgn_odno": "00298044",
      "ovrs_futr_fx_pdno": "6BZ22",
      "rcit_dvsn_cd": "02",
      "sll_buy_dvsn_cd": "02",
      "trad_stgy_dvsn_cd": "00",
      "bass_pric_type_cd": "1",
      "ord_stat_cd": "02",
      "fm_ord_qty": "1",
      "fm_ord_pric": "0.0000",
      "fm_stop_ord_pric": "0.0000",
      "rsvn_dvsn": "N",
      "fm_ccld_qty": "0",
      "fm_ccld_pric": "0.0000",
      "fm_ord_rmn_qty": "0",
      "ord_grp_name": "",
      "erlm_dtl_dtime": "20221214134356649",
      "ccld_dtl_dtime": "",
      "ord_stfno": "invent",
      "rmks1": "",
      "new_lqd_dvsn_cd": "1",
      "fm_lqd_lmt_ord_pric": "0.0000",
      "fm_lqd_stop_pric": "0.0000",
      "ccld_cndt_cd": "6",
      "noti_vald_dt": "",
      "acnt_type_cd": "1",
      "fuop_dvsn": "01"
    },
    {
      "cano": "81012345",
      "acnt_prdt_cd": "08",
      "ord_dt": "20221214",
      "odno": "00298044",
      "orgn_ord_dt": "",
      "orgn_odno": "",
      "ovrs_futr_fx_pdno": "6BZ22",
      "rcit_dvsn_cd": "00",
      "sll_buy_dvsn_cd": "02",
      "trad_stgy_dvsn_cd": "00",
      "bass_pric_type_cd": "1",
      "ord_stat_cd": "02",
      "fm_ord_qty": "1",
      "fm_ord_pric": "1.1700",
      "fm_stop_ord_pric": "0.0000",
      "rsvn_dvsn": "N",
      "fm_ccld_qty": "0",
      "fm_ccld_pric": "0.0000",
      "fm_ord_rmn_qty": "0",
      "ord_grp_name": "",
      "erlm_dtl_dtime": "20221214134351411",
      "ccld_dtl_dtime": "",
      "ord_stfno": "invent",
      "rmks1": "",
      "new_lqd_dvsn_cd": "1",
      "fm_lqd_lmt_ord_pric": "0.0000",
      "fm_lqd_stop_pric": "0.0000",
      "ccld_cndt_cd": "6",
      "noti_vald_dt": "",
      "acnt_type_cd": "1",
      "fuop_dvsn": "01"
    },
    {
      "cano": "81012345",
      "acnt_prdt_cd": "08",
      "ord_dt": "20221214",
      "odno": "00298040",
      "orgn_ord_dt": "",
      "orgn_odno": "",
      "ovrs_futr_fx_pdno": "6BZ22",
      "rcit_dvsn_cd": "00",
      "sll_buy_dvsn_cd": "02",
      "trad_stgy_dvsn_cd": "00",
      "bass_pric_type_cd": "1",
      "ord_stat_cd": "02",
      "fm_ord_qty": "1",
      "fm_ord_pric": "1.1700",
      "fm_stop_ord_pric": "0.0000",
      "rsvn_dvsn": "N",
      "fm_ccld_qty": "0",
      "fm_ccld_pric": "0.0000",
      "fm_ord_rmn_qty": "1",
      "ord_grp_name": "",
      "erlm_dtl_dtime": "20221214134100992",
      "ccld_dtl_dtime": "",
      "ord_stfno": "invent",
      "rmks1": "",
      "new_lqd_dvsn_cd": "1",
      "fm_lqd_lmt_ord_pric": "0.0000",
      "fm_lqd_stop_pric": "0.0000",
      "ccld_cndt_cd": "6",
      "noti_vald_dt": "",
      "acnt_type_cd": "1",
      "fuop_dvsn": "01"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```
