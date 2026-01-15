# 매도가능수량조회 [국내주식-165]

> [국내주식] 주문/계좌

매도가능수량조회 API입니다. 
한국투자 HTS(eFriend Plus) > [0971] 주식 매도 화면에서 종목코드 입력 후 "가능" 클릭 시 매도가능수량이 확인되는 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

특정종목 매도가능수량 확인 시, 매도주문 내시려는 주문종목(PDNO)으로 API 호출 후 
output > ord_psbl_qty(주문가능수량) 확인하실 수 있습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `b71fba6a-5759-4efa-a7e0-5e93e7e0e02d` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/inquire-psbl-sell` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `TTTC8408R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19
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
| `tr_id` | 거래ID | String | 13 | Y | TTTC8408R |
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
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌상품코드 |
| `PDNO` | 종목번호 | String | 12 | Y | 보유종목 코드 ex)000660 |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
PDNO:005930
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
| `output1` | 응답상세 | String |   | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `buy_qty` | 매수수량 | String | 10 | Y |  |
| `sll_qty` | 매도수량 | String | 10 | Y |  |
| `cblc_qty` | 잔고수량 | String | 19 | Y |  |
| `nsvg_qty` | 비저축수량 | String | 19 | Y |  |
| `ord_psbl_qty` | 주문가능수량 | String | 10 | Y |  |
| `pchs_avg_pric` | 매입평균가격 | String | 184 | Y |  |
| `pchs_amt` | 매입금액 | String | 19 | Y |  |
| `now_pric` | 현재가 | String | 8 | Y |  |
| `evlu_amt` | 평가금액 | String | 19 | Y |  |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y |  |
| `evlu_pfls_rt` | 평가손익율 | String | 72 | Y |  |

### 응답 예시

```json
{
  "output": {
    "pdno": "005930",
    "prdt_name": "삼성전자",
    "buy_qty": "1746",
    "sll_qty": "2",
    "cblc_qty": "1744",
    "nsvg_qty": "0",
    "ord_psbl_qty": "1744",
    "pchs_avg_pric": "54388.4874",
    "pchs_amt": "0",
    "now_pric": "75800",
    "evlu_amt": "132195200",
    "evlu_pfls_amt": "37341678",
    "evlu_pfls_rt": "39.36"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0420",
  "msg1": "정상적으로 조회되었습니다                                                       "
}
```
