# 기간별계좌권리현황조회 [국내주식-211]

> [국내주식] 주문/계좌

기간별계좌권리현황조회 API입니다.
한국투자 HTS(eFriend Plus) > [7344] 권리유형별 현황조회 화면을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `04275bfe-007a-45f6-8d4d-0682320a0741` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/period-rights` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTRGA011R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-06-14
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
| `tr_id` | 거래ID | String | 13 | Y | CTRGA011R |
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
| `INQR_DVSN` | 조회구분 | String | 2 | Y | 03 입력 |
| `CUST_RNCNO25` | 고객실명확인번호25 | String | 25 | Y | 공란 |
| `HMID` | 홈넷ID | String | 8 | Y | 공란 |
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 8자리 입력 (ex.12345678) |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 상품계좌번호 2자리 입력(ex. 01 or 22) |
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y | 조회시작일자(YYYYMMDD) |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y | 조회종료일자(YYYYMMDD) |
| `RGHT_TYPE_CD` | 권리유형코드 | String | 2 | Y | 공란 |
| `PDNO` | 상품번호 | String | 12 | Y | 공란 |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | 공란 |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y | 다음조회시 입력 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y | 다음조회시 입력 |

### 요청 예시

```json
INQR_DVSN:03
CUST_RNCNO25:
HMID:
CANO:12345678
ACNT_PRDT_CD:01
INQR_STRT_DT:20240508
INQR_END_DT:20241106
RGHT_TYPE_CD:
PDNO:
PRDT_TYPE_CD:
CTX_AREA_NK100:
CTX_AREA_FK100:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `acno10` | 계좌번호10 | String | 10 | Y |  |
| `rght_type_cd` | 권리유형코드 | String | 2 | Y | 1	유상 2	무상 3	배당 4	매수청구 5	공개매수 6	주주총회 7	신주인수권증서 8	반대의사 9	신주인수권증권 11	합병 12	회사분할 13	주식교환 14	액면분할 15	액... |
| `bass_dt` | 기준일자 | String | 8 | Y |  |
| `rght_cblc_type_cd` | 권리잔고유형코드 | String | 2 | Y | 1	입고 2	출고 3	출고입고 4	출고입금 5	출고출금 10	현금입금 11	단수주대금입금 12	교부금입금 13	유상감자대금입금 14	지연이자입금 15	이자지급 16	대주권리금... |
| `rptt_pdno` | 대표상품번호 | String | 12 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `shtn_pdno` | 단축상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `cblc_qty` | 잔고수량 | String | 19 | Y |  |
| `last_alct_qty` | 최종배정수량 | String | 19 | Y |  |
| `excs_alct_qty` | 초과배정수량 | String | 19 | Y |  |
| `tot_alct_qty` | 총배정수량 | String | 19 | Y |  |
| `last_ftsk_qty` | 최종단수주수량 | String | 191 | Y |  |
| `last_alct_amt` | 최종배정금액 | String | 19 | Y |  |
| `last_ftsk_chgs` | 최종단수주대금 | String | 19 | Y |  |
| `rdpt_prca` | 상환원금 | String | 19 | Y |  |
| `dlay_int_amt` | 지연이자금액 | String | 19 | Y |  |
| `lstg_dt` | 상장일자 | String | 8 | Y |  |
| `sbsc_end_dt` | 청약종료일자 | String | 8 | Y |  |
| `cash_dfrm_dt` | 현금지급일자 | String | 8 | Y |  |
| `rqst_qty` | 신청수량 | String | 19 | Y |  |
| `rqst_amt` | 신청금액 | String | 19 | Y |  |
| `rqst_dt` | 신청일자 | String | 8 | Y |  |
| `rfnd_dt` | 환불일자 | String | 8 | Y |  |
| `rfnd_amt` | 환불금액 | String | 19 | Y |  |
| `lstg_stqt` | 상장주수 | String | 19 | Y |  |
| `tax_amt` | 세금금액 | String | 19 | Y |  |
| `sbsc_unpr` | 청약단가 | String | 224 | Y |  |

### 응답 예시

```json
{
  "ctx_area_nk100": "                                                                                                    ",
  "ctx_area_fk100": "03!^!^!^12345678!^01!^20240508!^20241106!^!^!^                                                      ",
  "output": [
    {
      "acno10": "1234567801",
      "rght_type_cd": "01",
      "bass_dt": "20240919",
      "rght_cblc_type_cd": "01",
      "rptt_pdno": "00000A357880",
      "pdno": "00000A357880",
      "prdt_type_cd": "300",
      "shtn_pdno": "357880",
      "prdt_name": "비트나인",
      "cblc_qty": "1000",
      "last_alct_qty": "1050",
      "excs_alct_qty": "0",
      "tot_alct_qty": "1050",
      "last_ftsk_qty": "0.0000000000",
      "last_alct_amt": "0",
      "last_ftsk_chgs": "0",
      "rdpt_prca": "0",
      "dlay_int_amt": "0",
      "lstg_dt": "",
      "sbsc_end_dt": "20241011",
      "cash_dfrm_dt": "",
      "rqst_qty": "1000",
      "rqst_amt": "1865000",
      "rqst_dt": "20241011",
      "rfnd_dt": "",
      "rfnd_amt": "0",
      "lstg_stqt": "0",
      "tax_amt": "0",
      "sbsc_unpr": "1865.0000"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```

