# 해외주식 예약주문접수취소[v1_해외주식-004]

> [해외주식] 주문/계좌

접수된 미국주식 예약주문을 취소하기 위한 API입니다.
(해외주식 예약주문접수 시 Return 받은 ODNO를 참고하여 API를 호출하세요.)

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

[해외주식-004 v1] 해외주식 예약주문접수취소

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ec92f2c8-c3bd-4f80-b1f3-ea0716577f02` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/overseas-stock/v1/trading/order-resv-ccnl` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `(미국 예약주문 취소접수) TTTT3017U (아시아국가 미제공)` |
| **TR ID (모의)** | `(미국 예약주문 취소접수) VTTT3017U (아시아국가 미제공)` |

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
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTT3017U : 미국예약주문접수 취소  [모의투자] VTTT3017U : 미국예약주문접수 취소 (일본, 홍콩 등 타국가 개발 진행 예정) |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인 P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호 ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `RSYN_ORD_RCIT_DT` | 해외주문접수일자 | String | 8 | Y |  |
| `OVRS_RSVN_ODNO` | 해외예약주문번호 | String | 10 | Y | 해외주식_예약주문접수 API Output ODNO(주문번호) 참고 |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "RSVN_ORD_RCIT_DT": "20211124",
  "OVRS_RSVN_ODNO": "30135682"
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | Y | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공  0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output` | 응답상세 | String |  | Y |  |
| `OVRS_RSVN_ODNO` | 해외예약주문번호 | String | 10 | Y |  |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK1711",
  "msg1": "취소주문이 접수되었습니다.",
  "output": {
    "OVRS_RSVN_ODNO": "0030138295"
  }
}
```

