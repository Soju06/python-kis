# 주식예약주문정정취소[v1_국내주식-018,019]

> [국내주식] 주문/계좌

국내주식 예약주문 정정/취소 API 입니다.
*  정정주문은 취소주문에 비해 필수 입력값이 추가 됩니다. 
   하단의 입력값을 참조하시기 바랍니다.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

[국내주식-018,019 v1] 주식예약주문정정취소

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `09cd3a87-6b6a-4741-bc7d-f6565c93d6d8` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/domestic-stock/v1/trading/order-resv-rvsecncl` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `(예약취소) CTSC0009U (예약정정) CTSC0013U` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-05-04T12:54:34+09:00
- **최종 수정일**: 2025-04-30T10:06:54+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] CTSC0009U : 국내주식예약취소주문 CTSC0013U : 국내주식예약정정주문 * 모의투자 사용 불가 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | [정정/취소] 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | [정정/취소] 계좌번호 체계(8-2)의 뒤 2자리 |
| `PDNO` | 종목코드(6자리) | String | 12 | Y | [정정] |
| `ORD_QTY` | 주문수량 | String | 10 | Y | [정정] 주문주식수 |
| `ORD_UNPR` | 주문단가 | String | 19 | Y | [정정] 1주당 가격  * 장전 시간외, 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 권고 |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | [정정] 01 : 매도 02 : 매수 |
| `ORD_DVSN_CD` | 주문구분코드 | String | 2 | Y | [정정] 00 : 지정가 01 : 시장가 02 : 조건부지정가 05 : 장전 시간외 |
| `ORD_OBJT_CBLC_DVSN_CD` | 주문대상잔고구분코드 | String | 2 | Y | [정정] 10 : 현금 12 : 주식담보대출 14 : 대여상환 21 : 자기융자신규 22 : 유통대주신규 23 : 유통융자신규 24 : 자기대주신규 25 : 자기융자상환 26 : 유통대주상환 27 : 유통융자상환 28 : 자기대주상환 |
| `LOAN_DT` | 대출일자 | String | 8 | N | [정정] |
| `RSVN_ORD_END_DT` | 예약주문종료일자 | String | 8 | N | [정정] |
| `CTAL_TLNO` | 연락전화번호 | String | 20 | N | [정정] |
| `RSVN_ORD_SEQ` | 예약주문순번 | String | 10 | Y | [정정/취소] |
| `RSVN_ORD_ORGNO` | 예약주문조직번호 | String | 5 | N | [정정/취소] |
| `RSVN_ORD_ORD_DT` | 예약주문주문일자 | String | 8 | N | [정정/취소] |

### 요청 예시

```json
{ 
	"_comment": "주식예약주문취소", 
	"CANO": "810XXXXX", 
	"ACNT_PRDT_CD": "01", 
	"RSVN_ORD_ORD_DT": "20220427", 
	"RSVN_ORD_SEQ": "39447", 
	"RSVN_ORD_ORGNO": "00" 
} 

{ 
	"_comment": "주식예약주문정정", 
	"CANO": "810XXXXX", 
	"ACNT_PRDT_CD": "01", 
	"PDNO": "009150", 
	"ORD_QTY": "10", 
	"ORD_UNPR": "140000", 
	"SLL_BUY_DVSN_CD":"01", 
	"ORD_DVSN_CD":"00", 
	"ORD_OBJT_CBLC_DVSN_CD":"10", 
	"LOAN_DT":"", 
	"RSVN_ORD_END_DT":"", 
	"CTAC_TLNO": "", 
	"RSVN_ORD_SEQ":"39453", 
	"RSVN_ORD_ORGNO":"", 
	"RSVN_ORD_ORD_DT":"20220427" 
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
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공  0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | String |  | Y |  |
| `nrml_prcs_yn` | 정상처리여부 | String | 1 | Y |  |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "KIOK0430",
  "msg1": "정상적으로 처리되었습니다",
  "output": {
    "NRML_PRCS_YN": "Y"
  }
}
```

