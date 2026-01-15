# 해외주식 잔고[v1_해외주식-006]

> [해외주식] 주문/계좌

해외주식 잔고를 조회하는 API 입니다.
한국투자 HTS(eFriend Plus) > [7600] 해외주식 종합주문 화면의 좌측 하단 '실시간잔고' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 
다만 미국주간거래 가능종목에 대해서는 frcr_evlu_pfls_amt(외화평가손익금액), evlu_pfls_rt(평가손익율), ovrs_stck_evlu_amt(해외주식평가금액), now_pric2(현재가격2) 값이 HTS와는 상이하게 표출될 수 있습니다.
(주간시간 시간대에 HTS는 주간시세로 노출, API로는 야간시세로 노출)

실전계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. 

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

* 미니스탁 잔고는 해당 API로 확인이 불가합니다.

[해외주식-006 v1] 해외주식 잔고

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `0482dfb1-154c-476c-8a3b-6fc1da498dbf` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `TTTS3012R`, `VTTS3012R` |

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
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTS3012R  [모의투자] VTTS3012R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
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
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | [모의] NASD : 나스닥 NYSE : 뉴욕  AMEX : 아멕스  [실전] NASD : 미국전체 NAS : 나스닥 NYSE : 뉴욕  AMEX : 아멕스  [모의/실전 공... |
| `TR_CRCY_CD` | 거래통화코드 | String | 3 | Y | USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | N | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | N | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터) |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "OVRS_EXCG_CD": "NASD",
  "TR_CRCY_CD": "USD",
  "CTX_AREA_FK200": "",
  "CTX_AREA_NK200": ""
}
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | Y | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공  0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `ctx_area_fk200` | 연속조회검색조건200 | String | 200 | Y |  |
| `ctx_area_nk200` | 연속조회키200 | String | 200 | Y |  |
| `output1` | 응답상세1 | String |  | Y |  |
| `cano` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y | 계좌상품코드 |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `ovrs_pdno` | 해외상품번호 | String | 12 | Y |  |
| `ovrs_item_name` | 해외종목명 | String | 60 | Y |  |
| `frcr_evlu_pfls_amt` | 외화평가손익금액 | String | 30 | Y | 해당 종목의 매입금액과 평가금액의 외회기준 비교 손익 |
| `evlu_pfls_rt` | 평가손익율 | String | 10 | Y | 해당 종목의 평가손익을 기준으로 한 수익률 |
| `pchs_avg_pric` | 매입평균가격 | String | 23 | Y | 해당 종목의 매수 평균 단가 |
| `ovrs_cblc_qty` | 해외잔고수량 | String | 19 | Y |  |
| `ord_psbl_qty` | 주문가능수량 | String | 10 | Y | 매도 가능한 주문 수량 |
| `frcr_pchs_amt1` | 외화매입금액1 | String | 23 | Y | 해당 종목의 외화 기준 매입금액 |
| `ovrs_stck_evlu_amt` | 해외주식평가금액 | String | 32 | Y | 해당 종목의 외화 기준 평가금액 |
| `now_pric2` | 현재가격2 | String | 25 | Y | 해당 종목의 현재가 |
| `tr_crcy_cd` | 거래통화코드 | String | 3 | Y | USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동 |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 하노이거래소 VNSE : ... |
| `loan_type_cd` | 대출유형코드 | String | 2 | Y | 00 : 해당사항없음 01 : 자기융자일반형 03 : 자기융자투자형 05 : 유통융자일반형 06 : 유통융자투자형 07 : 자기대주 09 : 유통대주 10 : 현금 11 : ... |
| `loan_dt` | 대출일자 | String | 8 | Y | 대출 실행일자 |
| `expd_dt` | 만기일자 | String | 8 | Y | 대출 만기일자 |
| `output2` | 응답상세2 | String |  | Y |  |
| `frcr_pchs_amt1` | 외화매입금액1 | String | 24 | Y |  |
| `ovrs_rlzt_pfls_amt` | 해외실현손익금액 | String | 20 | Y |  |
| `ovrs_tot_pfls` | 해외총손익 | String | 24 | Y |  |
| `rlzt_erng_rt` | 실현수익율 | String | 32 | Y |  |
| `tot_evlu_pfls_amt` | 총평가손익금액 | String | 32 | Y |  |
| `tot_pftrt` | 총수익률 | String | 32 | Y |  |
| `frcr_buy_amt_smtl1` | 외화매수금액합계1 | String | 25 | Y |  |
| `ovrs_rlzt_pfls_amt2` | 해외실현손익금액2 | String | 24 | Y |  |
| `frcr_buy_amt_smtl2` | 외화매수금액합계2 | String | 25 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "                                                                                                                                                                                                        ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output1": [
    {
      "cano": "810XXXXX",
      "acnt_prdt_cd": "01",
      "prdt_type_cd": "512",
      "ovrs_pdno": "TSLA",
      "ovrs_item_name": "테슬라",
      "frcr_evlu_pfls_amt": "-3547254.185235",
      "evlu_pfls_rt": "-81.75",
      "pchs_avg_pric": "5832.2148",
      "ovrs_cblc_qty": "744",
      "ord_psbl_qty": "744",
      "frcr_pchs_amt1": "4339167.78523",
      "ovrs_stck_evlu_amt": "791913.60000000",
      "now_pric2": "1064.400000",
      "tr_crcy_cd": "USD",
      "ovrs_excg_cd": "NASD",
      "loan_type_cd": "10",
      "loan_dt": "",
      "expd_dt": ""
    },
    {
      "cano": "",
      "acnt_prdt_cd": "",
      "prdt_type_cd": "",
      "ovrs_pdno": "",
      "ovrs_item_name": "",
      "frcr_evlu_pfls_amt": "0.000000",
      "evlu_pfls_rt": "0.00",
      "pchs_avg_pric": "0.0000",
      "ovrs_cblc_qty": "0",
      "ord_psbl_qty": "0",
      "frcr_pchs_amt1": "0.00000",
      "ovrs_stck_evlu_amt": "0.00000000",
      "now_pric2": "0.000000",
      "tr_crcy_cd": "",
      "ovrs_excg_cd": "",
      "loan_type_cd": "",
      "loan_dt": "",
      "expd_dt": ""
    }
  ],
  "output2": {
    "frcr_pchs_amt1": "4339167.78523",
    "ovrs_rlzt_pfls_amt": "-4836.71476",
    "ovrs_tot_pfls": "-3547254.18524",
    "rlzt_erng_rt": "-82.93101266",
    "tot_evlu_pfls_amt": "791913.60000000",
    "tot_pftrt": "-81.74964327",
    "frcr_buy_amt_smtl1": "5832.214765",
    "ovrs_rlzt_pfls_amt2": "-5780841.48713",
    "frcr_buy_amt_smtl2": "6970663.087128"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```
