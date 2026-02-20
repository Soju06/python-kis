# 해외주식 정정취소주문[v1_해외주식-003]

> [해외주식] 주문/계좌

접수된 해외주식 주문을 정정하거나 취소하기 위한 API입니다.
(해외주식주문 시 Return 받은 ODNO를 참고하여 API를 호출하세요.)

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

* 해외 거래소 운영시간 외 API 호출 시 에러가 발생하오니 운영시간을 확인해주세요.
* 해외 거래소 운영시간(한국시간 기준)
1) 미국 : 23:30 ~ 06:00 (썸머타임 적용 시 22:30 ~ 05:00) 
   * 프리마켓(18:00 ~ 23:30, Summer Time : 17:00 ~ 22:30), 애프터마켓(06:00 ~ 07:00, Summer Time : 05:00 ~ 07:00) 시간대에도 주문 가능
2) 일본 : (오전) 09:00 ~ 11:30, (오후) 12:30 ~ 15:00
3) 상해 : 10:30 ~ 16:00
4) 홍콩 : (오전) 10:30 ~ 13:00, (오후) 14:00 ~ 17:00

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

[해외주식-003 v1] 해외주식 정정취소주문

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4812f155-bdb5-47ac-a35b-a70d3d8f14c9` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/overseas-stock/v1/trading/order-rvsecncl` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `(미국 정정·취소) TTTT1004U (아시아 국가 하단 규격서 참고)` |
| **TR ID (모의)** | `(미국 정정·취소) VTTT1004U (아시아 국가 하단 규격서 참고)` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15T13:08:14+09:00
- **최종 수정일**: 2025-04-30T10:46:53+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용) 법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용)  ※ 토큰 지정시 토큰 타입("Bearer") 지정 필요. 즉, 발급받은 접근토큰 앞에 앞에 "Bearer" 붙여서 호출 EX) "Bearer eyJ..........8GA" |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTT1004U : 미국 정정 취소 주문 TTTS1003U : 홍콩 정정 취소 주문 TTTS0309U : 일본 정정 취소 주문 TTTS0302U : 상해 취소 주문 TTTS0306U : 심천 취소 주문 TTTS0312U : 베트남 취소 주문   [모의투자] VTTT1004U : 미국 정정 취소 주문 VTTS1003U : 홍콩 정정 취소 주문 VTTS0309U : 일본 정정 취소 주문 VTTS0302U : 상해 취소 주문 VTTS0306U : 심천 취소 주문 VTTS0312U : 베트남 취소 주문 |
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
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥  NYSE : 뉴욕  AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민 |
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `ORGN_ODNO` | 원주문번호 | String | 10 | Y | 정정 또는 취소할 원주문번호 (해외주식_주문 API ouput ODNO  or 해외주식 미체결내역 API output ODNO 참고) |
| `RVSE_CNCL_DVSN_CD` | 정정취소구분코드 | String | 2 | Y | 01 : 정정  02 : 취소 |
| `ORD_QTY` | 주문수량 | String | 10 | Y |  |
| `OVRS_ORD_UNPR` | 해외주문단가 | String | 32 | Y | 취소주문 시, "0" 입력 |
| `MGCO_APTM_ODNO` | 운용사지정주문번호 | String | 12 | N |  |
| `ORD_SVR_DVSN_CD` | 주문서버구분코드 | String | 1 | N | "0"(Default) |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "OVRS_EXCG_CD": "NYSE",
  "PDNO": "BA",
  "ORGN_ODNO": "30135009",
  "RVSE_CNCL_DVSN_CD": "01",
  "ORD_QTY": "1",
  "OVRS_ORD_UNPR": "226.00",
  "CTAC_TLNO": "",
  "MGCO_APTM_ODNO": "",
  "ORD_SVR_DVSN_CD": "0"
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
    "ODNO": "0000004338",
    "ORD_TMD": "160710"
  }
}
```

