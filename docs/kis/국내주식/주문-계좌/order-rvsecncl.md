# 주식주문(정정취소)[v1_국내주식-003]

> [국내주식] 주문/계좌

주문 건에 대하여 정정 및 취소하는 API입니다. 단, 이미 체결된 건은 정정 및 취소가 불가합니다.

※ 정정은 원주문에 대한 주문단가 혹은 주문구분을 변경하는 사항으로, 정정이 가능한 수량은 원주문수량을 초과 할 수 없습니다.

※ 주식주문(정정취소) 호출 전에 반드시 주식정정취소가능주문조회 호출을 통해 정정취소가능수량(output > psbl_qty)을 확인하신 후 정정취소주문 내시기 바랍니다.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

[국내주식-003 v1] 주식주문(정정취소)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4bfdfb2b-34a7-43f6-935a-e637724f960a` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/domestic-stock/v1/trading/order-rvsecncl` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `VTTC0013U`, `TTTC0013U` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
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
| `tr_id` | 거래ID | String | 13 | Y | ※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] 정정/취소 (구)TTTC0803U → (신)TTTC0013U 정정/취소 (모의... |
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
| `KRX_FWDG_ORD_ORGNO` | 한국거래소전송주문조직번호 | String | 5 | Y |  |
| `ORGN_ODNO` | 원주문번호 | String | 10 | Y | 원주문번호 |
| `ORD_DVSN` | 주문구분 | String | 2 | Y | [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 ... |
| `RVSE_CNCL_DVSN_CD` | 정정취소구분코드 | String | 2 | Y | 01@정정 02@취소 |
| `ORD_QTY` | 주문수량 | String | 10 | Y | 주문수량 |
| `ORD_UNPR` | 주문단가 | String | 19 | Y | 주문단가 |
| `QTY_ALL_ORD_YN` | 잔량전부주문여부 | String | 1 | Y | 'Y@전량 N@일부' |
| `CNDT_PRIC` | 조건가격 | String | 19 | N | 스탑지정가호가에서 사용 |
| `EXCG_ID_DVSN_CD` | 거래소ID구분코드 | String | 3 | N | 한국거래소 : KRX 대체거래소 (넥스트레이드) : NXT SOR (Smart Order Routing) : SOR → 미입력시 KRX로 진행되며, 모의투자는 KRX만 가능 |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "KRX_FWDG_ORD_ORGNO": "",
  "ORGN_ODNO": "0001566017",
  "ORD_DVSN": "00",
  "RVSE_CNCL_DVSN_CD": "01",
  "ORD_QTY": "1",
  "ORD_UNPR": "180000",
  "QTY_ALL_ORD_YN": "N"
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
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | Object |   | Y | single |
| `krx_fwdg_ord_orgno` | 한국거래소전송주문조직번호 | String | 5 | Y |  |
| `odno` | 주문번호 | String | 10 | Y |  |
| `ord_tmd` | 주문시각 | String | 6 | Y |  |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "KRX_FWDG_ORD_ORGNO": "06010",
    "ODNO": "0001569139",
    "ORD_TMD": "131438"
  }
}
```
