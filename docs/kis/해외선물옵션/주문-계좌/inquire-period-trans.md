# 해외선물옵션 기간계좌거래내역[해외선물-014]

> [해외선물옵션] 주문/계좌

해외선물옵션 기간계좌거래내역 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `11cc8ad0-d3cc-4c55-8c2f-4923e8b87ee4` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/inquire-period-trans` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `OTFM3114R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-07
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
| `tr_id` | 거래ID | String | 13 | Y | OTFM3114R |
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
| `INQR_TERM_FROM_DT` | 조회기간FROM일자 | String | 8 | Y |  |
| `INQR_TERM_TO_DT` | 조회기간TO일자 | String | 8 | Y |  |
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `ACNT_TR_TYPE_CD` | 계좌거래유형코드 | String | 2 | Y | 1: 전체, 2:입출금 , 3: 결제 |
| `CRCY_CD` | 통화코드 | String | 3 | Y | '%%% : 전체 TUS: TOT_USD  / TKR: TOT_KRW KRW: 한국  / USD: 미국 EUR: EUR   / HKD: 홍콩 CNY: 중국  / JPY: 일본... |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK100값 : 다음페이지 조회시(2번째부터) |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100값 : 다음페이지 조회시(2번째부터) |
| `PWD_CHK_YN` | 비밀번호체크여부 | String | 1 | Y | 공란(Default) |

### 요청 예시

```json
{
  "INQR_TERM_FROM_DT": "20220101",
  "INQR_TERM_TO_DT": "20221214",
  "CANO": "80012345",
  "ACNT_PRDT_CD": "08",
  "ACNT_TR_TYPE_CD": "%%",
  "CRCY_CD": "%%%",
  "CTX_AREA_FK100": "",
  "CTX_AREA_NK100": "",
  "PWD_CHK_YN": ""
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
| `output` | 응답상세1 | Object |   | Y | Array |
| `bass_dt` | 기준일자 | String | 8 | Y |  |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `fm_ldgr_inog_seq` | FM원장출납순번 | String | 10 | Y |  |
| `acnt_tr_type_name` | 계좌거래유형명 | String | 60 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `tr_itm_name` | 거래항목명 | String | 60 | Y |  |
| `fm_iofw_amt` | FM입출금액 | String | 20 | Y |  |
| `fm_fee` | FM수수료 | String | 20 | Y |  |
| `fm_tax_amt` | FM세금금액 | String | 20 | Y |  |
| `fm_sttl_amt` | FM결제금액 | String | 20 | Y |  |
| `fm_bf_dncl_amt` | FM이전예수금액 | String | 20 | Y |  |
| `fm_dncl_amt` | FM예수금액 | String | 20 | Y |  |
| `fm_rcvb_occr_amt` | FM미수발생금액 | String | 20 | Y |  |
| `fm_rcvb_pybk_amt` | FM미수변제금액 | String | 20 | Y |  |
| `ovdu_int_pybk_amt` | 연체이자변제금액 | String | 20 | Y |  |
| `rmks_text` | 비고내용 | String | 500 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "20220101^20221214^81012345^08^%%^%%%^                                                               ",
  "ctx_area_nk100": "                                                                                                    ",
  "output": [],
  "rt_cd": "0",
  "msg_cd": "KIOK0560",
  "msg1": "조회할 내용이 없습니다                                                          "
}
```
