# 해외선물옵션 예수금현황[해외선물-012]

> [해외선물옵션] 주문/계좌

해외선물옵션 예수금현황 API입니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `df4f0faf-db31-4650-b320-64a44ebdecf6` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/inquire-deposit` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `OTFM1411R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-07T12:55:16+09:00
- **최종 수정일**: 2025-04-30T12:55:13+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용)  ※ 토큰 지정시 토큰 타입("Bearer") 지정 필요. 즉, 발급받은 접근토큰 앞에 앞에 "Bearer" 붙여서 호출 EX) "Bearer eyJ..........8GA" |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | OTFM1411R |
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
| `CRCY_CD` | 통화코드 | String | 3 | Y | TUS: TOT_USD  / TKR: TOT_KRW KRW: 한국  / USD: 미국 EUR: EUR   / HKD: 홍콩 CNY: 중국  / JPY: 일본 VND: 베트남 |
| `INQR_DT` | 조회일자 | String | 8 | Y |  |

### 요청 예시

```json
{
	"CANO":"80012345",
	"ACNT_PRDT_CD":"08",
	"CRCY_CD":":"KRW",
	"INQR_DT":"20221214"
}
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
| `output` | 응답상세1 | String |   | Y |  |
| `fm_nxdy_dncl_amt` | FM익일예수금액 | String | 20 | Y |  |
| `fm_tot_asst_evlu_amt` | FM총자산평가금액 | String | 20 | Y |  |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `resp_dt` | 응답일자 | String | 8 | Y |  |
| `fm_dnca_rmnd` | FM예수금잔액 | String | 20 | Y |  |
| `fm_lqd_pfls_amt` | FM청산손익금액 | String | 20 | Y |  |
| `fm_fee` | FM수수료 | String | 20 | Y |  |
| `fm_fuop_evlu_pfls_amt` | FM선물옵션평가손익금액 | String | 20 | Y |  |
| `fm_rcvb_amt` | FM미수금액 | String | 20 | Y |  |
| `fm_brkg_mgn_amt` | FM위탁증거금액 | String | 20 | Y |  |
| `fm_mntn_mgn_amt` | FM유지증거금액 | String | 20 | Y |  |
| `fm_add_mgn_amt` | FM추가증거금액 | String | 20 | Y |  |
| `fm_risk_rt` | FM위험율 | String | 10 | Y |  |
| `fm_ord_psbl_amt` | FM주문가능금액 | String | 20 | Y |  |
| `fm_drwg_psbl_amt` | FM출금가능금액 | String | 20 | Y |  |
| `fm_echm_rqrm_amt` | FM환전요청금액 | String | 20 | Y |  |
| `fm_drwg_prar_amt` | FM출금예정금액 | String | 20 | Y |  |
| `fm_opt_tr_chgs` | FM옵션거래대금 | String | 20 | Y |  |
| `fm_opt_icld_asst_evlu_amt` | FM옵션포함자산평가금액 | String | 20 | Y |  |
| `fm_opt_evlu_amt` | FM옵션평가금액 | String | 20 | Y |  |
| `fm_crcy_sbst_amt` | FM통화대용금액 | String | 20 | Y |  |
| `fm_crcy_sbst_use_amt` | FM통화대용사용금액 | String | 20 | Y |  |
| `fm_crcy_sbst_stup_amt` | FM통화대용설정금액 | String | 20 | Y |  |

### 응답 예시

```json
{
  "output": {
    "cano": "81012345",
    "acnt_prdt_cd": "08",
    "crcy_cd": "KRW",
    "resp_dt": "20230104",
    "fm_dnca_rmnd": "9990000012",
    "fm_lqd_pfls_amt": "0",
    "fm_fee": "0",
    "fm_nxdy_dncl_amt": "9990000012",
    "fm_tot_asst_evlu_amt": "9990000012",
    "fm_fuop_evlu_pfls_amt": "0",
    "fm_rcvb_amt": "0",
    "fm_brkg_mgn_amt": "0",
    "fm_mntn_mgn_amt": "0",
    "fm_add_mgn_amt": "0",
    "fm_risk_rt": "0.00",
    "fm_ord_psbl_amt": "9718323936",
    "fm_drwg_psbl_amt": "9704739489",
    "fm_echm_rqrm_amt": "0",
    "fm_drwg_prar_amt": "0",
    "fm_opt_tr_chgs": "0",
    "fm_opt_icld_asst_evlu_amt": "9990000012",
    "fm_opt_evlu_amt": "0",
    "fm_crcy_sbst_amt": "0",
    "fm_crcy_sbst_use_amt": "0",
    "fm_crcy_sbst_stup_amt": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

