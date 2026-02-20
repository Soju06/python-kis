# 해외주식 미체결내역[v1_해외주식-005]

> [해외주식] 주문/계좌

접수된 해외주식 주문 중 체결되지 않은 미체결 내역을 조회하는 API입니다.
실전계좌의 경우, 한 번의 호출에 최대 40건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. 

※ 해외주식 미체결내역 API 모의투자에서는 사용이 불가합니다. 
   모의투자로 해외주식 미체결내역 확인시에는 해외주식 주문체결내역[v1_해외주식-007] API 조회하셔서 nccs_qty(미체결수량)으로 해외주식 미체결수량을 조회하실 수 있습니다.


* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

* 해외 거래소 운영시간(한국시간 기준)
1) 미국 : 23:30 ~ 06:00 (썸머타임 적용 시 22:30 ~ 05:00) 
   * 프리마켓(18:00 ~ 23:30, Summer Time : 17:00 ~ 22:30), 애프터마켓(06:00 ~ 07:00, Summer Time : 05:00 ~ 07:00)
2) 일본 : (오전) 09:00 ~ 11:30, (오후) 12:30 ~ 15:00
3) 상해 : 10:30 ~ 16:00
4) 홍콩 : (오전) 10:30 ~ 13:00, (오후) 14:00 ~ 17:00

[해외주식-005 v1] 해외주식 미체결내역

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `60cae69d-c121-4dd9-902c-1112567fd88e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-nccs` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `TTTS3018R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15T13:12:20+09:00
- **최종 수정일**: 2025-04-30T10:48:31+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용) 법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, Oauth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTS3018R |
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
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥 NYSE : 뉴욕  AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민  * NASD 인 경우만 미국전체로 조회되며 나머지 거래소 코드는 해당 거래소만 조회됨 * 공백 입력 시 다음조회가 불가능하므로, 반드시 거래소코드 입력해야 함 |
| `SORT_SQN` | 정렬순서 | String | 2 | Y | DS : 정순 그외 : 역순  [header tr_id: TTTS3018R] ""(공란) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터) |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "OVRS_EXCG_CD": "NYSE",
  "SORT_SQN": "DS",
  "CTX_AREA_FK200": "",
  "CTX_AREA_NK200": ""
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
| `ctx_area_fk200` | 연속조회검색조건200 | String | 200 | Y |  |
| `ctx_area_nk200` | 연속조회키200 | String | 200 | Y |  |
| `output` | 응답상세 | String |  | Y |  |
| `ord_dt` | 주문일자 | String | 8 | Y | 주문접수 일자 |
| `ord_gno_brno` | 주문채번지점번호 | String | 5 | Y | 계좌 개설 시 관리점으로 선택한 영업점의 고유번호 |
| `odno` | 주문번호 | String | 10 | Y | 접수한 주문의 일련번호 |
| `orgn_odno` | 원주문번호 | String | 10 | Y | 정정 또는 취소 대상 주문의 일련번호 |
| `pdno` | 상품번호 | String | 12 | Y | 종목코드 |
| `prdt_name` | 상품명 | String | 60 | Y | 종목명 |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | Y | 01 : 매도 02 : 매수 |
| `sll_buy_dvsn_cd_name` | 매도매수구분코드명 | String | 60 | Y | 매수매도구분명 |
| `rvse_cncl_dvsn_cd` | 정정취소구분코드 | String | 2 | Y | 01 : 정정 02 : 취소 |
| `rvse_cncl_dvsn_cd_name` | 정정취소구분코드명 | String | 60 | Y | 정정취소구분명 |
| `rjct_rson` | 거부사유 | String | 60 | Y | 정상 처리되지 못하고 거부된 주문의 사유 |
| `rjct_rson_name` | 거부사유명 | String | 60 | Y | 정상 처리되지 못하고 거부된 주문의 사유명 |
| `ord_tmd` | 주문시각 | String | 6 | Y | 주문 접수 시간 |
| `tr_mket_name` | 거래시장명 | String | 60 | Y |  |
| `tr_crcy_cd` | 거래통화코드 | String | 3 | Y | USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동 |
| `natn_cd` | 국가코드 | String | 3 | Y |  |
| `natn_kor_name` | 국가한글명 | String | 60 | Y |  |
| `ft_ord_qty` | FT주문수량 | String | 10 | Y | 주문수량 |
| `ft_ccld_qty` | FT체결수량 | String | 10 | Y | 체결된 수량 |
| `nccs_qty` | 미체결수량 | String | 10 | Y | 미체결수량 |
| `ft_ord_unpr3` | FT주문단가3 | String | 26 | Y | 주문가격 |
| `ft_ccld_unpr3` | FT체결단가3 | String | 26 | Y | 체결된 가격 |
| `ft_ccld_amt3` | FT체결금액3 | String | 23 | Y | 체결된 금액 |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민 |
| `prcs_stat_name` | 처리상태명 | String | 60 | Y | "" |
| `loan_type_cd` | 대출유형코드 | String | 2 | Y | 00 해당사항없음 01 자기융자일반형 03 자기융자투자형 05 유통융자일반형 06 유통융자투자형 07 자기대주 09 유통대주 10 현금 11 주식담보대출 12 수익증권담보대출 13 ELS담보대출 14 채권담보대출 15 해외주식담보대출 16 기업신용공여 31 소액자동담보대출 41 매도담보대출 42 환매자금대출 43 매입환매자금대출 44 대여매도담보대출 81 대차거래 82 법인CMA론 91 공모주청약자금대출 92 매입자금 93 미수론서비스 94 대여 |
| `loan_dt` | 대출일자 | String | 8 | Y | 대출 실행일자 |
| `usa_amk_exts_rqst_yn` | 미국애프터마켓연장신청여부 | String | 1 | Y | Y/N |
| `splt_buy_attr_name` | 분할매수속성명 | String | 60 | Y | 정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시됨 |

### 응답 예시

```json
{
  "ctx_area_fk200": "81055689^01^NYSE^DS^                                                                                                                                                                                    ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output": [
    {
      "ord_dt": "20220112",
      "ord_gno_brno": "01790",
      "odno": "0030138112",
      "orgn_odno": "",
      "pdno": "BA",
      "prdt_name": "보잉",
      "sll_buy_dvsn_cd": "02",
      "sll_buy_dvsn_cd_name": "매수",
      "rvse_cncl_dvsn_cd": "00",
      "rvse_cncl_dvsn_cd_name": "",
      "rjct_rson": "",
      "rjct_rson_name": "",
      "ord_tmd": "163209",
      "tr_mket_name": "뉴욕거래소",
      "tr_crcy_cd": "USD",
      "natn_cd": "840",
      "natn_kor_name": "미국",
      "ft_ord_qty": "1",
      "ft_ccld_qty": "0",
      "nccs_qty": "1",
      "ft_ord_unpr3": "200.00000000",
      "ft_ccld_unpr3": "0.00000000",
      "ft_ccld_amt3": "0.00000",
      "ovrs_excg_cd": "NYSE",
      "prcs_stat_name": "",
      "loan_type_cd": "10",
      "loan_dt": ""
    },
    {
      "ord_dt": "20220112",
      "ord_gno_brno": "01790",
      "odno": "0030138113",
      "orgn_odno": "",
      "pdno": "BA",
      "prdt_name": "보잉",
      "sll_buy_dvsn_cd": "02",
      "sll_buy_dvsn_cd_name": "매수",
      "rvse_cncl_dvsn_cd": "00",
      "rvse_cncl_dvsn_cd_name": "",
      "rjct_rson": "",
      "rjct_rson_name": "",
      "ord_tmd": "163211",
      "tr_mket_name": "뉴욕거래소",
      "tr_crcy_cd": "USD",
      "natn_cd": "840",
      "natn_kor_name": "미국",
      "ft_ord_qty": "1",
      "ft_ccld_qty": "0",
      "nccs_qty": "1",
      "ft_ord_unpr3": "200.00000000",
      "ft_ccld_unpr3": "0.00000000",
      "ft_ccld_amt3": "0.00000",
      "ovrs_excg_cd": "NYSE",
      "prcs_stat_name": "",
      "loan_type_cd": "10",
      "loan_dt": ""
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

