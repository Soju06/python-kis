# 해외선물옵션 정정취소주문 [v1_해외선물-002, 003]

> [해외선물옵션] 주문/계좌

해외선물옵션 정정취소주문 API 입니다.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a0822304-5dba-4912-b62d-d82bd88858fa` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/order-rvsecncl` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `(정정) OTFM3002U (취소) OTFM3003U`, `모의투자 미지원` |

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
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] OTFM3002U : 해외선물옵션주문정정 OTFM3003U : 해외선물옵션주문취소 |
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
| `ORGN_ORD_DT` | 원주문일자 | String | 8 | Y | 원 주문 시 출력되는 ORD_DT 값을 입력 (현지거래일) |
| `ORGN_ODNO` | 원주문번호 | String | 8 | Y | 정정/취소시 주문번호(ODNO) 8자리를 문자열처럼 "0"을 포함해서 전송 (원 주문 시 출력된 ODNO 값 활용) (ex. ORGN_ODNO : 00360686) |
| `FM_LIMIT_ORD_PRIC` | FMLIMIT주문가격 | String | 20 | N | OTFM3002U(해외선물옵션주문정정)만 사용 |
| `FM_STOP_ORD_PRIC` | FMSTOP주문가격 | String | 20 | N | OTFM3002U(해외선물옵션주문정정)만 사용 |
| `FM_LQD_LMT_ORD_PRIC` | FM청산LIMIT주문가격 | String | 20 | N | OTFM3002U(해외선물옵션주문정정)만 사용 |
| `FM_LQD_STOP_ORD_PRIC` | FM청산STOP주문가격 | String | 20 | N | OTFM3002U(해외선물옵션주문정정)만 사용 |
| `FM_HDGE_ORD_SCRN_YN` | FM_HEDGE주문화면여부 | String | 1 | Y | N |
| `FM_MKPR_CVSN_YN` | FM시장가전환여부 | String | 1 | N | OTFM3003U(해외선물옵션주문취소)만 사용  ※ FM_MKPR_CVSN_YN 항목에 'Y'로 설정하여 취소주문을 접수할 경우, 주문 취소확인이 들어오면 원장에서 시장가주문... |

### 요청 예시

```json
{
  "CANO": "81012345",
  "ACNT_PRDT_CD": "08",
  "ORGN_ORD_DT": "20221214",
  "ORGN_ODNO": "00298044",
  "FM_MKPR_CVSN_YN": "N",
  "FM_HDGE_ORD_SCRN_YN": "N"
}
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공 0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` |   | String |   | N |  |
| `ORD_DT` | 주문일자 | String | 8 | N | YYYYMMDD(ex. 20230811) |
| `ODNO` | 주문번호 | String | 8 | N | 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송    (ex. ORGN_ODNO : 00360686) |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "ORD_DT": "20221214",
    "ODNO": "00298045"
  }
}
```
