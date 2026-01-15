# 해외선물옵션 주문 [v1_해외선물-001]

> [해외선물옵션] 주문/계좌

해외선물옵션 주문 API 입니다.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `749c8e3b-7e40-4f5b-82a3-11cad0a10e8d` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/order` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `OTFM3001U ` |

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
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] OTFM3001U : ASFM선물옵션주문신규 |
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
| `OVRS_FUTR_FX_PDNO` | 해외선물FX상품번호 | String | 32 | Y |  |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | 01 : 매도 02 : 매수 |
| `FM_LQD_USTL_CCLD_DT` | FM청산미결제체결일자 | String | 8 | N | 빈칸 (hedge청산만 이용) |
| `FM_LQD_USTL_CCNO` | FM청산미결제체결번호 | String | 10 | N | 빈칸 (hedge청산만 이용) |
| `PRIC_DVSN_CD` | 가격구분코드 | String | 1 | Y | 1.지정, 2. 시장, 3. STOP, 4 S/L |
| `FM_LIMIT_ORD_PRIC` | FMLIMIT주문가격 | String | 20 | Y | 지정가인 경우 가격 입력 * 시장가, STOP주문인 경우, 빈칸("") 입력 |
| `FM_STOP_ORD_PRIC` | FMSTOP주문가격 | String | 20 | Y | STOP 주문 가격 입력 * 시장가, 지정가인 경우, 빈칸("") 입력 |
| `FM_ORD_QTY` | FM주문수량 | String | 10 | Y |  |
| `FM_LQD_LMT_ORD_PRIC` | FM청산LIMIT주문가격 | String | 20 | N | 빈칸 (hedge청산만 이용) |
| `FM_LQD_STOP_ORD_PRIC` | FM청산STOP주문가격 | String | 20 | N | 빈칸 (hedge청산만 이용) |
| `CCLD_CNDT_CD` | 체결조건코드 | String | 1 | Y | 일반적으로 6 (EOD, 지정가)  GTD인 경우 5, 시장가인 경우만 2 |
| `CPLX_ORD_DVSN_CD` | 복합주문구분코드 | String | 1 | Y | 0 (hedge청산만 이용) |
| `ECIS_RSVN_ORD_YN` | 행사예약주문여부 | String | 1 | Y | N |
| `FM_HDGE_ORD_SCRN_YN` | FM_HEDGE주문화면여부 | String | 1 | Y | N |

### 요청 예시

```json
{
  "CANO": "81012345",
  "ACNT_PRDT_CD": "08",
  "OVRS_FUTR_FX_PDNO": "6BZ22",
  "SLL_BUY_DVSN_CD": "02",
  "FM_LQD_USTL_CCLD_DT": "",
  "FM_LQD_USTL_CCNO": "",
  "PRIC_DVSN_CD": "1",
  "FM_LIMIT_ORD_PRIC": "1.17",
  "FM_STOP_ORD_PRIC": "",
  "FM_ORD_QTY": "1",
  "FM_LQD_LMT_ORD_PRIC": "",
  "FM_LQD_STOP_ORD_PRIC": "",
  "CCLD_CNDT_CD": "6",
  "CPLX_ORD_DVSN_CD": "0",
  "ECIS_RSVN_ORD_YN": "N",
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
| `ORD_DT` | 주문일자 | String | 8 | N |  |
| `ODNO` | 주문번호 | String | 8 | N | 접수한 주문의 일련번호(ex. 00360686) * 정정/취소시 문자열처럼 "0"을 포함해서 전송    (ex. ORGN_ODNO : 00360686) |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "ORD_DT": "20221214",
    "ODNO": "00298040"
  }
}
```
