# 선물옵션 총자산현황[v1_국내선물-014]

> [국내선물옵션] 주문/계좌

선물옵션 총자산현황 API 입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `24abcfa1-a95b-4344-bb7f-11f2523f8355` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-deposit` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `CTRP6550R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-09-08
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
| `tr_id` | 거래ID | String | 13 | Y | CTRP6550R |
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

### 요청 예시

```json
{
	"CANO":"12345678",
	"ACNT_PRDT_CD":"03",
}
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
| `dnca_tota` | 예수금총액 | String | 19 | Y |  |
| `bfdy_chck_amt` | 전일수표금액 | String | 19 | Y |  |
| `thdt_chck_amt` | 당일수표금액 | String | 19 | Y |  |
| `rlth_uwdl_dpos_amt` | 실물인수도예치금액 | String | 19 | Y |  |
| `brkg_mgna_cash` | 위탁증거금현금 | String | 19 | Y |  |
| `wdrw_psbl_tot_amt` | 인출가능총금액 | String | 19 | Y |  |
| `ord_psbl_cash` | 주문가능현금 | String | 19 | Y |  |
| `ord_psbl_tota` | 주문가능총액 | String | 19 | Y |  |
| `dnca_sbst` | 예수금대용 | String | 19 | Y |  |
| `scts_sbst_amt` | 유가증권대용금액 | String | 19 | Y |  |
| `frcr_evlu_amt` | 외화평가금액 | String | 19 | Y |  |
| `brkg_mgna_sbst` | 위탁증거금대용 | String | 19 | Y |  |
| `sbst_rlse_psbl_amt` | 대용해제가능금액 | String | 19 | Y |  |
| `mtnc_rt` | 유지비율 | String | 238 | Y |  |
| `add_mgna_tota` | 추가증거금총액 | String | 19 | Y |  |
| `add_mgna_cash` | 추가증거금현금 | String | 19 | Y |  |
| `rcva` | 미수금 | String | 19 | Y |  |
| `futr_trad_pfls` | 선물매매손익 | String | 19 | Y |  |
| `opt_trad_pfls_amt` | 옵션매매손익금액 | String | 19 | Y |  |
| `trad_pfls_smtl` | 매매손익합계 | String | 19 | Y |  |
| `futr_evlu_pfls_amt` | 선물평가손익금액 | String | 19 | Y |  |
| `opt_evlu_pfls_amt` | 옵션평가손익금액 | String | 19 | Y |  |
| `evlu_pfls_smtl` | 평가손익합계 | String | 19 | Y |  |
| `excc_dfpa` | 정산차금 | String | 19 | Y |  |
| `opt_dfpa` | 옵션차금 | String | 19 | Y |  |
| `brkg_fee` | 위탁수수료 | String | 19 | Y |  |
| `nxdy_dnca` | 익일예수금 | String | 19 | Y |  |
| `prsm_dpast_amt` | 추정예탁자산금액 | String | 19 | Y |  |
| `cash_mntn_amt` | 현금유지금액 | String | 19 | Y |  |
| `hack_acdt_acnt_move_amt` | 해킹사고계좌이전금액 | String | 19 | Y |  |

### 응답 예시

```json
{
  "output": {
    "dnca_tota": "100000000",
    "bfdy_chck_amt": "0",
    "thdt_chck_amt": "0",
    "rlth_uwdl_dpos_amt": "0",
    "brkg_mgna_cash": "17907612",
    "wdrw_psbl_tot_amt": "34046775",
    "ord_psbl_cash": "64184775",
    "ord_psbl_tota": "64184775",
    "dnca_sbst": "0",
    "scts_sbst_amt": "0",
    "frcr_evlu_amt": "0",
    "brkg_mgna_sbst": "17907613",
    "sbst_rlse_psbl_amt": "0",
    "mtnc_rt": "418.23000000",
    "add_mgna_tota": "0",
    "add_mgna_cash": "0",
    "rcva": "0",
    "futr_trad_pfls": "0",
    "opt_trad_pfls_amt": "0",
    "trad_pfls_smtl": "0",
    "futr_evlu_pfls_amt": "4187500",
    "opt_evlu_pfls_amt": "-697500",
    "evlu_pfls_smtl": "3490000",
    "excc_dfpa": "-30138000",
    "opt_dfpa": "0",
    "brkg_fee": "0",
    "nxdy_dnca": "69862000",
    "prsm_dpast_amt": "69864500",
    "cash_mntn_amt": "0",
    "hack_acdt_acnt_move_amt": "0"
  },
  "rt_cd": "0",
  "msg_cd": "APRP0126",
  "msg1": "조회이(가) 완료되었습니다.                                                      "
}
```
