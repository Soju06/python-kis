# 해외주식 매수가능금액조회[v1_해외주식-014]

> [해외주식] 주문/계좌

해외주식 매수가능금액조회 API입니다.

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

[v1_해외주식-014]해외주식 매수가능금액조회

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `2a155fee-882f-4d80-8183-559f2f6983e9` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-psamount` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `TTTS3007R` |
| **TR ID (모의)** | `VTTS3007R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-07-15T15:54:15+09:00
- **최종 수정일**: 2025-04-30T10:50:55+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTS3007R  [모의투자] VTTS3007R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | N | B : 법인 / P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | 법인 : "001" / 개인: ""(Default) |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥 / NYSE : 뉴욕 / AMEX : 아멕스 SEHK : 홍콩 / SHAA : 중국상해 / SZAA : 중국심천 TKSE : 일본 / HASE : 하노이거래소 / VNSE : 호치민거래소 |
| `OVRS_ORD_UNPR` | 해외주문단가 | String | 27 | Y | 해외주문단가 (23.8) 정수부분 23자리, 소수부분 8자리 |
| `ITEM_CD` | 종목코드 | String | 12 | Y | 종목코드 |

### 요청 예시

```json
"input": {
            "ACNT_PRDT_CD": "01",
            "CANO": "81019777",
            "ITEM_CD": "00011",
            "OVRS_EXCG_CD": "SEHK",
            "OVRS_ORD_UNPR": "133.200"
        }
```

## 응답

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
| `output` | 응답상세1 | String |  | N |  |
| `tr_crcy_cd` | 거래통화코드 | String | 3 | N | 18.2 |
| `ord_psbl_frcr_amt` | 주문가능외화금액 | String | 21 | N | 18.2 |
| `sll_ruse_psbl_amt` | 매도재사용가능금액 | String | 21 | N | 가능금액 산정 시 사용 |
| `ovrs_ord_psbl_amt` | 해외주문가능금액 | String | 21 | N | - 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능금액 |
| `max_ord_psbl_qty` | 최대주문가능수량 | String | 19 | N | - 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능수량 - 매수 시 수량단위 절사해서 사용     예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주 |
| `echm_af_ord_psbl_amt` | 환전이후주문가능금액 | String | 21 | N | 사용되지 않는 사항(0으로 출력) |
| `echm_af_ord_psbl_qty` | 환전이후주문가능수량 | String | 19 | N | 사용되지 않는 사항(0으로 출력) |
| `ord_psbl_qty` | 주문가능수량 | String | 10 | N | 22(20.1) |
| `exrt` | 환율 | String | 22 | N | 25(18.6) |
| `frcr_ord_psbl_amt1` | 외화주문가능금액1 | String | 25 | N | - 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능금액 |
| `ovrs_max_ord_psbl_qty` | 해외최대주문가능수량 | String | 19 | N | - 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능수량 - 매수 시 수량단위 절사해서 사용     예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주 |

### 응답 예시

```json
"output": {
            "echm_af_ord_psbl_amt": "0.00",
            "echm_af_ord_psbl_qty": "0",
            "exrt": "165.5400000000",
            "frcr_ord_psbl_amt1": "955**.12",
            "max_ord_psbl_qty": "744**",
            "ord_psbl_frcr_amt": "999**.52",
            "ord_psbl_qty": "744**",
            "ovrs_max_ord_psbl_qty": "717**",
            "ovrs_ord_psbl_amt": "992**.35",
            "sll_ruse_psbl_amt": "0.00",
            "tr_crcy_cd": "HKD"
        }
```

