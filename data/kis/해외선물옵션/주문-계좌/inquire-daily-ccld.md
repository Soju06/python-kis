# 해외선물옵션 일별 체결내역[해외선물-011]

> [해외선물옵션] 주문/계좌

해외선물옵션 일별 체결내역 API입니다.
거래소 체결 내역에 따라 , output1에 동일한 주문번호의 데이터들이 수신될 수 있습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `17cfbb44-0389-4b56-9d0c-7410930747d4` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/inquire-daily-ccld` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `OTFM3122R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-07T12:53:43+09:00
- **최종 수정일**: 2026-02-11T09:59:49+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용)  ※ 토큰 지정시 토큰 타입("Bearer") 지정 필요. 즉, 발급받은 접근토큰 앞에 앞에 "Bearer" 붙여서 호출 EX) "Bearer eyJ..........8GA" |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | OTFM3122R |
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
| `STRT_DT` | 시작일자 | String | 8 | Y | 시작일자(YYYYMMDD) |
| `END_DT` | 종료일자 | String | 8 | Y | 종료일자(YYYYMMDD) |
| `FUOP_DVSN_CD` | 선물옵션구분코드 | String | 2 | Y | 00:전체 / 01:선물 / 02:옵션 |
| `FM_PDGR_CD` | FM상품군코드 | String | 10 | Y | 공란(Default) |
| `CRCY_CD` | 통화코드 | String | 3 | Y | %%% : 전체 TUS: TOT_USD  / TKR: TOT_KRW KRW: 한국  / USD: 미국 EUR: EUR   / HKD: 홍콩 CNY: 중국  / JPY: 일본 VND: 베트남 |
| `FM_ITEM_FTNG_YN` | FM종목합산여부 | String | 1 | Y | "N"(Default) |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | %%: 전체 / 01 : 매도 / 02 : 매수 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |

### 요청 예시

```json
{
	"CANO":"80012345",
	"ACNT_PRDT_CD":"08",
	"STRT_DT":"20221010",
	"END_DT":"20221216",
	"FUOP_DVSN":"00",
	"FM_PDGR_CD":"",
	"CRCY_CD":"%%%",
	"FM_ITEM_FTNG_YN":"N",
	"SLL_BUY_DVSN_CD":"%%",
	"CTX_AREA_FK100":"",
	"CTX_AREA_NK100":"",
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
| `output2` | 응답상세2 | String |   | Y |  |
| `fm_tot_ccld_qty` | FM총체결수량 | String | 10 | Y |  |
| `fm_tot_futr_agrm_amt` | FM총선물약정금액 | String | 20 | Y |  |
| `fm_tot_opt_agrm_amt` | FM총옵션약정금액 | String | 20 | Y |  |
| `fm_fee_smtl` | FM수수료합계 | String | 20 | Y |  |
| `output1` | 응답상세1 | Object |   | Y | Array |
| `dt` | 일자 | String | 8 | Y |  |
| `ccno` | 체결번호 | String | 8 | Y |  |
| `ovrs_futr_fx_pdno` | 해외선물FX상품번호 | String | 32 | Y |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 3 | Y |  |
| `fm_ccld_qty` | FM체결수량 | String | 10 | Y |  |
| `fm_ccld_amt` | FM체결금액 | String | 20 | Y |  |
| `fm_futr_ccld_amt` | FM선물체결금액 | String | 20 | Y |  |
| `fm_opt_ccld_amt` | FM옵션체결금액 | String | 20 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `fm_fee` | FM수수료 | String | 20 | Y |  |
| `fm_futr_pure_agrm_amt` | FM선물순약정금액 | String | 20 | Y |  |
| `fm_opt_pure_agrm_amt` | FM옵션순약정금액 | String | 20 | Y |  |
| `ccld_dtl_dtime` | 체결상세일시 | String | 17 | Y |  |
| `ord_dt` | 주문일자 | String | 8 | Y |  |
| `odno` | 주문번호 | String | 8 | Y | 접수한 주문의 일련번호(ex. 00360686) |
| `ord_mdia_dvsn_name` | 주문매체구분명 | String | 60 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "80012345^08^20221010^20221216^00^^%%%^N^%%^                                                                                                                                                             ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output1": [
    {
      "dt": "20221020",
      "ccno": "00004090",
      "ovrs_futr_fx_pdno": "6AZ22",
      "sll_buy_dvsn_cd": "02",
      "fm_ccld_qty": "1",
      "fm_ccld_amt": ".62955",
      "fm_futr_ccld_amt": "62955",
      "fm_opt_ccld_amt": "0",
      "crcy_cd": "USD",
      "fm_fee": "12.5",
      "fm_futr_pure_agrm_amt": "62967.5",
      "fm_opt_pure_agrm_amt": "0",
      "ccld_dtl_dtime": "20221020132204282",
      "ord_dt": "20221020",
      "odno": "00284471",
      "ord_mdia_dvsn_name": "일반"
    },
    {
      "dt": "20221020",
      "ccno": "00004089",
      "ovrs_futr_fx_pdno": "6AZ22",
      "sll_buy_dvsn_cd": "02",
      "fm_ccld_qty": "1",
      "fm_ccld_amt": ".62945",
      "fm_futr_ccld_amt": "62945",
      "fm_opt_ccld_amt": "0",
      "crcy_cd": "USD",
      "fm_fee": "12.5",
      "fm_futr_pure_agrm_amt": "62957.5",
      "fm_opt_pure_agrm_amt": "0",
      "ccld_dtl_dtime": "20221020125948252",
      "ord_dt": "20221020",
      "odno": "00284466",
      "ord_mdia_dvsn_name": "일반"
    }
  ],
  "output2": {
    "fm_tot_ccld_qty": "2",
    "fm_tot_futr_agrm_amt": "125900",
    "fm_tot_opt_agrm_amt": "0",
    "fm_fee_smtl": "25"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

