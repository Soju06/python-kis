# 해외주식 주문[v1_해외주식-001]

> [해외주식] 주문/계좌

해외주식 주문 API입니다.

* 모의투자의 경우, 모든 해외 종목 매매가 지원되지 않습니다. 일부 종목만 매매 가능한 점 유의 부탁드립니다.

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

* 해외 거래소 운영시간 외 API 호출 시 에러가 발생하오니 운영시간을 확인해주세요. (미국주식 주간주문은 "해외주식 미국주간주문"을 이용)
* 해외 거래소 운영시간(한국시간 기준)
1) 미국 : 23:30 ~ 06:00 (썸머타임 적용 시 22:30 ~ 05:00) 
   * 프리마켓(18:00 ~ 23:30, Summer Time : 17:00 ~ 22:30), 애프터마켓(06:00 ~ 07:00, Summer Time : 05:00 ~ 07:00) 시간대에도 주문 가능
2) 일본 : (오전) 09:00 ~ 11:30, (오후) 12:30 ~ 15:00
3) 상해 : 10:30 ~ 16:00
4) 홍콩 : (오전) 10:30 ~ 13:00, (오후) 14:00 ~ 17:00

* 기존에는 내부통제 요건에 따라 상장주식수의 1%를 초과하는 주문은 접수할 수 없었으나, 2025.08.14 시행 이후부터는 접수가 가능합니다. 단, 타 매체(HTS 등)는 안내 팝업 확인 후 주문이 가능하지만, Open API는 별도의 안내 화면 없이 주문이 바로 접수되므로 유의하시기 바랍니다.


※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

[해외주식-001 v1] 해외주식 주문

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `e4a7e5fd-eed5-4a85-93f0-f46b804dae5f` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/overseas-stock/v1/trading/order` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `(미국매수) TTTT1002U  (미국매도) TTTT1006U (아시아 국가 하단 규격서 참고)` |
| **TR ID (모의)** | `(미국매수) VTTT1002U  (미국매도) VTTT1001U  (아시아 국가 하단 규격서 참고)` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-08-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTT1002U : 미국 매수 주문 TTTT1006U : 미국 매도 주문 TTTS0308U : 일본 매수 주문 TTTS0307U : 일본 매도 주문  TTTS0... |
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
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE :... |
| `PDNO` | 상품번호 | String | 12 | Y | 종목코드 |
| `ORD_QTY` | 주문수량 | String | 10 | Y | 주문수량 (해외거래소 별 최소 주문수량 및 주문단위 확인 필요) |
| `OVRS_ORD_UNPR` | 해외주문단가 | String | 31 | Y | 1주당 가격 * 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 |
| `CTAC_TLNO` | 연락전화번호 | String | 20 | N |  |
| `MGCO_APTM_ODNO` | 운용사지정주문번호 | String | 12 | N |  |
| `SLL_TYPE` | 판매유형 | String | 2 | N | 제거 : 매수 00 : 매도 |
| `ORD_SVR_DVSN_CD` | 주문서버구분코드 | String | 1 | Y | "0"(Default) |
| `ORD_DVSN` | 주문구분 | String | 2 | Y | [Header tr_id TTTT1002U(미국 매수 주문)] 00 : 지정가 32 : LOO(장개시지정가) 34 : LOC(장마감지정가) 35 : TWAP (시간가중평균) ... |
| `START_TIME` | 시작시간 | String | 6 | N | ※ TWAP, VWAP 주문유형이고 알고리즘주문시간구분코드가 00일때 사용 ※ YYMMDD 형태로 입력 ※ 시간 입력 시 정규장 종료 5분전까지 입력 가능 |
| `END_TIME` | 종료시간 | String | 6 | N | ※ TWAP, VWAP 주문유형이고 알고리즘주문시간구분코드가 00일때 사용 ※ YYMMDD 형태로 입력 ※ 시간 입력 시 정규장 종료 5분전까지 입력 가능 |
| `ALGO_ORD_TMD_DVSN_CD` | 알고리즘주문시간구분코드 | String | 2 | N | 00 : 분할주문 시간 직접입력 , 02 : 정규장 종료시까지 |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "OVRS_EXCG_CD": "NASD",
  "PDNO": "AAPL",
  "ORD_QTY": "1",
  "OVRS_ORD_UNPR": "145.00",
  "CTAC_TLNO": "",
  "MGCO_APTM_ODNO": "",
  "ORD_SVR_DVSN_CD": "0",
  "ORD_DVSN": "00"
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
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output` | 응답상세 | String |  | Y |  |
| `KRX_FWDG_ORD_ORGNO` | 한국거래소전송주문조직번호 | String | 5 | Y | 주문시 한국투자증권 시스템에서 지정된 영업점코드 |
| `ODNO` | 주문번호 | String | 10 | Y | 주문시 한국투자증권 시스템에서 채번된 주문번호 |
| `ORD_TMD` | 주문시각 | String | 6 | Y | 주문시각(시분초HHMMSS) |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "KRX_FWDG_ORD_ORGNO": "01790",
    "ODNO": "0000004336",
    "ORD_TMD": "160524"
  }
}
```

