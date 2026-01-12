# 주식주문(신용)[v1_국내주식-002]

> [국내주식] 주문/계좌

국내주식주문(신용) API입니다. 
※ 모의투자는 사용 불가합니다.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

[국내주식-002 v1] 주식주문(신용)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f5769e4a-24d5-44f9-a2d8-232d45abf988` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/domestic-stock/v1/trading/order-credit` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `(매도) TTTC0051U (매수) TTTC0052U` |

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
| `tr_id` | 거래ID | String | 13 | Y | '※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] 매도 : (구)TTTC0851U → (신)TTTC0051U 매수 : (구)T... |
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
| `PDNO` | 상품번호 | String | 5 | Y | 종목코드(6자리) |
| `SLL_TYPE` | 매도유형 | String | 10 | N | 공란 입력 |
| `CRDT_TYPE` | 신용유형 | String | 2 | Y | [매도] 22 : 유통대주신규, 24 : 자기대주신규, 25 : 자기융자상환, 27 : 유통융자상환 [매수] 21 : 자기융자신규, 23 : 유통융자신규 , 26 : 유통대주... |
| `LOAN_DT` | 대출일자 | String | 2 | Y | [신용매수]  신규 대출로, 오늘날짜(yyyyMMdd)) 입력   [신용매도]  매도할 종목의 대출일자(yyyyMMdd)) 입력 |
| `ORD_DVSN` | 주문구분 | String | 8 | Y | [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 ... |
| `ORD_QTY` | 주문수량 | String | 2 | Y |  |
| `ORD_UNPR` | 주문단가 | String | 5 | Y | 1주당 가격  * 장전 시간외, 장후 시간외, 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 권고 |
| `RSVN_ORD_YN` | 예약주문여부 | String | 2 | N | 정규 증권시장이 열리지 않는 시간 (15:10분 ~ 익일 7:30분) 에 주문을 미리 설정 하여 다음 영업일 또는 설정한 기간 동안 아침 동시 호가에 주문하는 것  Y : 예... |
| `EMGC_ORD_YN` | 비상주문여부 | String | 2 | N |  |
| `PGTR_DVSN` | 프로그램매매구분 | String | 10 | N |  |
| `MGCO_APTM_ODNO` | 운용사지정주문번호 | String | 19 | N |  |
| `LQTY_TR_NGTN_DTL_NO` | 대량거래협상상세번호 | String | 1 | N |  |
| `LQTY_TR_AGMT_NO` | 대량거래협정번호 | String | 20 | N |  |
| `LQTY_TR_NGTN_ID` | 대량거래협상자Id | String | 19 | N |  |
| `LP_ORD_YN` | LP주문여부 | String | 3 | N |  |
| `MDIA_ODNO` | 매체주문번호 | String | 10 | N |  |
| `ORD_SVR_DVSN_CD` | 주문서버구분코드 | String | 19 | N |  |
| `PGM_NMPR_STMT_DVSN_CD` | 프로그램호가신고구분코드 | String | 1 | N |  |
| `CVRG_SLCT_RSON_CD` | 반대매매선정사유코드 | String | 20 | N |  |
| `CVRG_SEQ` | 반대매매순번 | String | 19 | N |  |
| `EXCG_ID_DVSN_CD` | 거래소ID구분코드 | String | 3 | N | 한국거래소 : KRX 대체거래소 (넥스트레이드) : NXT SOR (Smart Order Routing) : SOR → 미입력시 KRX로 진행되며, 모의투자는 KRX만 가능 |
| `CNDT_PRIC` | 조건가격 | String | 19 | N | 스탑지정가호가에서 사용 |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "PDNO": "009150",
  "CRDT_TYPE": "21",
  "LOAN_DT": "20211103",
  "ORD_DVSN": "00",
  "ORD_QTY": "1",
  "ORD_UNPR": "130000",
  "RSVN_ORD_YN": "N"
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
| `output` | 응답상세 | String |   | Y | single |
| `krx_fwdg_ord_orgno` | 한국거래소전송주문조직번호 | String | 5 | Y |  |
| `odno` | 주문번호 | String | 10 | Y |  |
| `ord_tmd` | 주문시간 | String | 6 | Y |  |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "KRX_FWDG_ORD_ORGNO": "06010",
    "ODNO": "0001569138",
    "ORD_TMD": "131421"
  }
}
```
