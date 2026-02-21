# 해외선물옵션 일별 주문내역[해외선물-013]

> [해외선물옵션] 주문/계좌

해외선물옵션 일별 주문내역 API입니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ca3e5ee4-a1f3-48a6-ab11-cd298ebef686` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/inquire-daily-order` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `OTFM3120R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-07T12:57:58+09:00
- **최종 수정일**: 2025-04-30T12:55:33+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용)  ※ 토큰 지정시 토큰 타입("Bearer") 지정 필요. 즉, 발급받은 접근토큰 앞에 앞에 "Bearer" 붙여서 호출 EX) "Bearer eyJ..........8GA" |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | OTFM3120R |
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
| `STRT_DT` | 시작일자 | String | 8 | Y |  |
| `END_DT` | 종료일자 | String | 8 | Y |  |
| `FM_PDGR_CD` | FM상품군코드 | String | 10 | Y |  |
| `CCLD_NCCS_DVSN` | 체결미체결구분 | String | 2 | Y | 01:전체 / 02:체결 / 03:미체결 |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | %%전체 / 01 : 매도 / 02 : 매수 |
| `FUOP_DVSN` | 선물옵션구분 | String | 2 | Y | 00:전체 / 01:선물 / 02:옵션 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |

### 요청 예시

```json
{
	"CANO":"12345678",
	"ACNT_PRDT_CD":"08",
	"STRT_DT":"20220101",
	"END_DT":"20221214",
	"FM_PDGR_CD":"",
	"CCLD_NCCS_DVSN":"01",
	"SLL_BUY_DVSN_CD":"%%",
	"FUOP_DVSN":"00",
	"CTX_AREA_FK200":"",
	"CTX_AREA_NK200":"",
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
| `output` | 응답상세1 | Object |   | Y | Array |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `dt` | 일자 | String | 8 | Y |  |
| `ord_dt` | 주문일자 | String | 8 | Y |  |
| `odno` | 주문번호 | String | 8 | Y | 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송    (ex. ORGN_ODNO : 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송    (ex. ORGN_ODNO : 00360686) |
| `orgn_ord_dt` | 원주문일자 | String | 8 | Y |  |
| `orgn_odno` | 원주문번호 | String | 8 | Y | 원주문번호(ex. 00360685) |
| `ovrs_futr_fx_pdno` | 해외선물FX상품번호 | String | 32 | Y |  |
| `rvse_cncl_dvsn_cd` | 정정취소구분코드 | String | 2 | Y | 청산체결이 없는 신규	00 청산체결이 없는 정정	01 청산체결이 없는 취소	02 청산체결이 있는 취소	02 청산체결이 있는 신규	03 청산체결이 있는 정정	04 행사	05 배정	06 소멸	07 만기	08 |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | Y |  |
| `cplx_ord_dvsn_cd` | 복합주문구분코드 | String | 1 | Y |  |
| `pric_dvsn_cd` | 가격구분코드 | String | 1 | Y |  |
| `rcit_dvsn_cd` | 접수구분코드 | String | 2 | Y |  |
| `fm_ord_qty` | FM주문수량 | String | 10 | Y |  |
| `fm_ord_pric` | FM주문가격 | String | 20 | Y |  |
| `fm_stop_ord_pric` | FMSTOP주문가격 | String | 20 | Y |  |
| `ecis_rsvn_ord_yn` | 행사예약주문여부 | String | 1 | Y |  |
| `fm_ccld_qty` | FM체결수량 | String | 10 | Y |  |
| `fm_ccld_pric` | FM체결가격 | String | 20 | Y |  |
| `fm_ord_rmn_qty` | FM주문잔여수량 | String | 10 | Y |  |
| `ord_grp_name` | 주문그룹명 | String | 60 | Y |  |
| `rcit_dtl_dtime` | 접수상세일시 | String | 17 | Y |  |
| `ccld_dtl_dtime` | 체결상세일시 | String | 17 | Y |  |
| `ordr_emp_no` | 주문자사원번호 | String | 6 | Y |  |
| `rjct_rson_name` | 거부사유명 | String | 60 | Y |  |
| `ccld_cndt_cd` | 체결조건코드 | String | 1 | Y |  |
| `trad_end_dt` | 매매종료일자 | String | 8 | Y |  |

### 응답 예시

```json
{
    "ctx_area_fk200": "12345678^08^20231206^20231206^^01^%%^00^                                                                                                                                                                ",
    "ctx_area_nk200": "                                                                                                                                                                                                        ",
    "output": [
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362398",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6CZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "2",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "3",
            "fm_ord_pric": "0.00000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "3",
            "fm_ccld_pric": "0.73935",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206092306005",
            "ccld_dtl_dtime": "20231206092306005",
            "ordr_emp_no": "109171",
            "rjct_rson_name": "",
            "ccld_cndt_cd": "2",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362397",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6CZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "2",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "1",
            "fm_ord_pric": "0.00000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "1",
            "fm_ccld_pric": "0.73925",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206092247252",
            "ccld_dtl_dtime": "20231206092247252",
            "ordr_emp_no": "109171",
            "rjct_rson_name": "",
            "ccld_cndt_cd": "2",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362396",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6CZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "2",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "1",
            "fm_ord_pric": "0.00000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "1",
            "fm_ccld_pric": "0.73920",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206092123893",
            "ccld_dtl_dtime": "20231206092123893",
            "ordr_emp_no": "109171",
            "rjct_rson_name": "",
            "ccld_cndt_cd": "2",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362395",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6CZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "2",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "1",
            "fm_ord_pric": "0.00000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "1",
            "fm_ccld_pric": "0.73915",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206092039261",
            "ccld_dtl_dtime": "20231206092039261",
            "ordr_emp_no": "109171",
            "rjct_rson_name": "",
            "ccld_cndt_cd": "2",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362394",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "10YZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "2",
            "rcit_dvsn_cd": "03",
            "fm_ord_qty": "1",
            "fm_ord_pric": "0.000",
            "fm_stop_ord_pric": "0.000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "0",
            "fm_ccld_pric": "0.000",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "",
            "ccld_dtl_dtime": "",
            "ordr_emp_no": "109171",
            "rjct_rson_name": "[정상적인거부]Text[Order price is outside bands 'Bid of 4269",
            "ccld_cndt_cd": "2",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362393",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6AZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "1",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "2",
            "fm_ord_pric": "0.65000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "0",
            "fm_ccld_pric": "0.00000",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206091838237",
            "ccld_dtl_dtime": "",
            "ordr_emp_no": "45TesT",
            "rjct_rson_name": "FCM 거부됨",
            "ccld_cndt_cd": "6",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362392",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6AZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "1",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "2",
            "fm_ord_pric": "0.65000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "0",
            "fm_ccld_pric": "0.00000",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206091835180",
            "ccld_dtl_dtime": "",
            "ordr_emp_no": "45TesT",
            "rjct_rson_name": "FCM 거부됨",
            "ccld_cndt_cd": "6",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362391",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6AZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "1",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "2",
            "fm_ord_pric": "0.65000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "0",
            "fm_ccld_pric": "0.00000",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206083023955",
            "ccld_dtl_dtime": "",
            "ordr_emp_no": "45TesT",
            "rjct_rson_name": "FCM 거부됨",
            "ccld_cndt_cd": "6",
            "trad_end_dt": ""
        },
        {
            "cano": "12345678",
            "acnt_prdt_cd": "08",
            "dt": "20231206",
            "ord_dt": "20231206",
            "odno": "00362390",
            "orgn_ord_dt": "",
            "orgn_odno": "",
            "ovrs_futr_fx_pdno": "6AZ23",
            "rvse_cncl_dvsn_cd": "00",
            "sll_buy_dvsn_cd": "02",
            "cplx_ord_dvsn_cd": "0",
            "pric_dvsn_cd": "1",
            "rcit_dvsn_cd": "02",
            "fm_ord_qty": "2",
            "fm_ord_pric": "0.65000",
            "fm_stop_ord_pric": "0.00000",
            "ecis_rsvn_ord_yn": "N",
            "fm_ccld_qty": "0",
            "fm_ccld_pric": "0.00000",
            "fm_ord_rmn_qty": "0",
            "ord_grp_name": "",
            "rcit_dtl_dtime": "20231206082401404",
            "ccld_dtl_dtime": "",
            "ordr_emp_no": "45TesT",
            "rjct_rson_name": "FCM 거부됨",
            "ccld_cndt_cd": "6",
            "trad_end_dt": ""
        }
    ],
    "rt_cd": "0",
    "msg_cd": "KIOK0510",
```

