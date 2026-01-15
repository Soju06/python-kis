# 주식주문(현금)[v1_국내주식-001]

> [국내주식] 주문/계좌

국내주식주문(현금) API 입니다. 

※ TTC0802U(현금매수) 사용하셔서 미수매수 가능합니다. 단, 거래하시는 계좌가 증거금40%계좌로 신청이 되어있어야 가능합니다. 
※ 신용매수는 별도의 API가 준비되어 있습니다.

※ ORD_QTY(주문수량), ORD_UNPR(주문단가) 등을 String으로 전달해야 함에 유의 부탁드립니다.

※ ORD_UNPR(주문단가)가 없는 주문은 상한가로 주문금액을 선정하고 이후 체결이되면 체결금액로 정산됩니다.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

[국내주식-001 v1] 주식주문(현금)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `aade4c72-5fb7-418a-9ff2-254b4d5f0ceb` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/domestic-stock/v1/trading/order-cash` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `(매도) TTTC0011U (매수) TTTC0012U` |
| **TR ID (모의)** | `(매도) VTTC0011U (매수) VTTC0012U` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
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
| `tr_id` | 거래ID | String | 13 | Y | '※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] 국내주식주문 매도 : (구)TTTC0801U → (신)TTTC0011U 국내... |
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
| `CANO` | 종합계좌번호 | String | 8 | Y | 종합계좌번호 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 상품유형코드 |
| `PDNO` | 상품번호 | String | 12 | Y | 종목코드(6자리) , ETN의 경우 7자리 입력 |
| `SLL_TYPE` | 매도유형 (매도주문 시) | String | 2 | N | 01@일반매도 02@임의매매 05@대차매도 → 미입력시 01 일반매도로 진행 |
| `ORD_DVSN` | 주문구분 | String | 2 | Y | [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 ... |
| `ORD_QTY` | 주문수량 | String | 10 | Y | 주문수량 |
| `ORD_UNPR` | 주문단가 | String | 19 | Y | 주문단가 시장가 등 주문시, "0"으로 입력 |
| `CNDT_PRIC` | 조건가격 | String | 19 | N | 스탑지정가호가 주문 (ORD_DVSN이 22) 사용 시에만 필수 |
| `EXCG_ID_DVSN_CD` | 거래소ID구분코드 | String | 3 | N | 한국거래소 : KRX 대체거래소 (넥스트레이드) : NXT SOR (Smart Order Routing) : SOR → 미입력시 KRX로 진행되며, 모의투자는 KRX만 가능 |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "PDNO": "009150",
  "ORD_DVSN": "00",
  "ORD_QTY": "3",
  "ORD_UNPR": "150000"
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | Object |   | Y | single |
| `KRX_FWDG_ORD_ORGNO` | 거래소코드 | String | 5 | Y |  |
| `ODNO` | 주문번호 | String | 10 | Y |  |
| `ORD_TMD` | 주문시간 | String | 6 | Y |  |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "KRX_FWDG_ORD_ORGNO": "06010",
    "ODNO": "0001569157",
    "ORD_TMD": "155211"
  }
}
```

