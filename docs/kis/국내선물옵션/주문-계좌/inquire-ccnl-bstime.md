# 선물옵션 기준일체결내역[v1_국내선물-016]

> [국내선물옵션] 주문/계좌

선물옵션 기준일체결내역 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f64db1b8-012a-4e92-ab1c-e9b3b264b2b7` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-ccnl-bstime` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `CTFO5139R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-09-22
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
| `tr_id` | 거래ID | String | 13 | Y | CTFO5139R |
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
| `ORD_DT` | 주문일자 | String | 8 | Y | 주문일자(YYYYMMDD) |
| `FUOP_TR_STRT_TMD` | 선물옵션거래시작시각 | String | 6 | Y | 선물옵션거래시작시간(HHMMSS) |
| `FUOP_TR_END_TMD` | 선물옵션거래종료시각 | String | 6 | Y | 선물옵션거래종료시간(HHMMSS) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 연속조회검색조건200 |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 연속조회키200 |

### 요청 예시

```json
{
	"CANO":"12345678",
	"ACNT_PRDT_CD":"03",
	"ORD_DT":"20230920",
	"FUOP_TR_STRT_TMD":"000000",
	"FUOP_TR_END_TMD":"240000",
	"CTX_AREA_FK200":"",
	'CTX_AREA_NK200":""
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
| `output1` | 응답상세 | String |   | Y | array |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `odno` | 주문번호 | String | 10 | Y |  |
| `tr_type_name` | 거래유형명 | String | 60 | Y |  |
| `last_sttldt` | 최종결제일 | String | 8 | Y |  |
| `ccld_idx` | 체결지수 | String | 24 | Y |  |
| `ccld_qty` | 체결량 | String | 10 | Y |  |
| `trad_amt` | 매매금액 | String | 19 | Y |  |
| `fee` | 수수료 | String | 19 | Y |  |
| `ccld_btwn` | 체결시간 | String | 6 | Y |  |
| `output2` | 응답상세2 | String |   | Y |  |
| `tot_ccld_qty_smtl` | 총체결수량합계 | String | 19 | Y |  |
| `tot_ccld_amt_smtl` | 총체결금액합계 | String | 19 | Y |  |
| `fee_adjt` | 수수료조정 | String | 19 | Y |  |
| `fee_smtl` | 수수료합계 | String | 19 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "12345678!^03!^20230920!^000000!^240000                                                                                                                                                                  ",
  "ctx_area_nk200": " !^ !^ !^                                                                                                                                                                                               ",
  "output1": [
    {
      "pdno": "201T10340",
      "prdt_name": "코스피200 C 202310 340.0",
      "odno": "0000219602",
      "tr_type_name": "지수콜옵션매수",
      "last_sttldt": "20231012",
      "ccld_idx": "2.80000000",
      "ccld_qty": "1",
      "trad_amt": "700000",
      "fee": "2758",
      "ccld_btwn": "140144"
    },
    {
      "pdno": "101T12",
      "prdt_name": "코스피200 F 202312",
      "odno": "0000219606",
      "tr_type_name": "지수선물매수",
      "last_sttldt": "20231214",
      "ccld_idx": "335.50000000",
      "ccld_qty": "5",
      "trad_amt": "419375000",
      "fee": "41144",
      "ccld_btwn": "140121"
    }
  ],
  "output2": {
    "tot_ccld_qty_smtl": "6",
    "tot_ccld_amt_smtl": "420075000",
    "fee_adjt": "43902",
    "fee_smtl": "43890"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
