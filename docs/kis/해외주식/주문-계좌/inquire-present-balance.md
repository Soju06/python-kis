# 해외주식 체결기준현재잔고[v1_해외주식-008]

> [해외주식] 주문/계좌

해외주식 잔고를 체결 기준으로 확인하는 API 입니다. 

HTS(eFriend Plus) [0839] 해외 체결기준잔고 화면을 API로 구현한 사항으로 화면을 함께 보시면 기능 이해가 쉽습니다.

(※모의계좌의 경우 output3(외화평가총액 등 확인 가능)만 정상 출력됩니다. 
잔고 확인을 원하실 경우에는 해외주식 잔고[v1_해외주식-006] API 사용을 부탁드립니다.)

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

해외주식 체결기준현재잔고 유의사항
1. 해외증권 체결기준 잔고현황을 조회하는 화면입니다.
2. 온라인국가는 수수료(국내/해외)가 반영된 최종 정산금액으로 잔고가 변동되며, 결제작업 지연등으로 인해 조회시간은 차이가 발생할 수 있습니다.
   - 아시아 온라인국가 : 매매일 익일    08:40 ~ 08:45분 경
   - 미국 온라인국가   : 당일 장 종료후 08:40 ~ 08:45분 경
  ※ 단, 애프터연장 참여 신청계좌는 10:30 ~ 10:35분 경(Summer Time : 09:30 ~ 09:35분 경)에 최종 정산금액으로 변동됩니다.
3. 미국 현재가 항목은 주간시세 및 애프터시세는 반영하지 않으며, 정규장 마감 후에는 종가로 조회됩니다.
4. 온라인국가를 제외한 국가의 현재가는 실시간 시세가 아니므로 주문화면의 잔고 평가금액 등과 차이가 발생할 수 있습니다.
5. 해외주식 담보대출 매도상환 체결내역은 해당 잔고화면에 반영되지 않습니다.
   결제가 완료된 이후 외화잔고에 포함되어 반영되오니 참고하여 주시기 바랍니다.
6. 외화평가금액은 당일 최초고시환율이 적용된 금액으로 실제 환전금액과는 차이가 있습니다. 
7. 미국은 메인 시스템이 아닌 별도 시스템을 통해 거래되므로, 18시 10~15분 이후 발생하는 미국 매매내역은 해당 화면에 실시간으로 반영되지 않으니 하단 내용을 참고하여 안내하여 주시기 바랍니다. 
   [외화잔고 및 해외 유가증권 현황 조회]
   - 일반/통합증거금 계좌 : 미국장 종료 + 30분 후 부터 조회 가능
                            단, 통합증거금 계좌에 한해 주문금액은 외화잔고 항목에 실시간 반영되며, 해외 유가증권 현황은 반영되지
                            않아 해외 유가증권 평가금액이 과다 또는 과소 평가될 수 있습니다. 
   - 애프터연장 신청계좌  : 실시간 반영 
                            단, 시스템정산작업시간(23:40~00:10) 및 거래량이 많은 경우 메인시스템에 반영되는 시간으로 인해 차이가 
                            발생할 수 있습니다.
   ※ 배치작업시간에 따라 시간은 변동될 수 있습니다.

[해외주식-008 v1] 해외주식 체결기준현재잔고

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `09baff2a-6e9d-4502-ba66-d7bb94094b67` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-present-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443    (output3만 이용 가능)` |
| **TR ID** | `CTRP6504R`, `VTRP6504R` |

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
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] CTRP6504R  [모의투자] VTRP6504R |
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
| `WCRC_FRCR_DVSN_CD` | 원화외화구분코드 | String | 2 | Y | 01 : 원화  02 : 외화 |
| `NATN_CD` | 국가코드 | String | 3 | Y | 000 전체 840 미국 344 홍콩 156 중국 392 일본 704 베트남 |
| `TR_MKET_CD` | 거래시장코드 | String | 2 | Y | [Request body NATN_CD 000 설정] 00 : 전체  [Request body NATN_CD 840 설정] 00 : 전체 01 : 나스닥(NASD) 02 : ... |
| `INQR_DVSN_CD` | 조회구분코드 | String | 2 | Y | 00 : 전체  01 : 일반해외주식  02 : 미니스탁 |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "01",
  "WCRC_FRCR_DVSN_CD": "01",
  "TR_MKET_CD": "00",
  "NATN_CD": "000",
  "INQR_DVSN_CD": "00"
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
| `output1` | 응답상세1 (체결기준 잔고) | String |  | Y | 체결기준현재잔고 없으면 빈값으로 출력 |
| `prdt_name` | 상품명 | String | 60 | Y | 종목명 |
| `cblc_qty13` | 잔고수량13 | String | 32 | Y | 결제보유수량 |
| `thdt_buy_ccld_qty1` | 당일매수체결수량1 | String | 32 | Y | 당일 매수 체결 완료 수량 |
| `thdt_sll_ccld_qty1` | 당일매도체결수량1 | String | 32 | Y | 당일 매도 체결 완료 수량 |
| `ccld_qty_smtl1` | 체결수량합계1 | String | 32 | Y | 체결기준 현재 보유수량 |
| `ord_psbl_qty1` | 주문가능수량1 | String | 32 | Y | 주문 가능한 주문 수량 |
| `frcr_pchs_amt` | 외화매입금액 | String | 29 | Y | 해당 종목의 외화 기준 매입금액 |
| `frcr_evlu_amt2` | 외화평가금액2 | String | 30 | Y | 해당 종목의 외화 기준 평가금액 |
| `evlu_pfls_amt2` | 평가손익금액2 | String | 31 | Y | 해당 종목의 매입금액과 평가금액의 외회기준 비교 손익 |
| `evlu_pfls_rt1` | 평가손익율1 | String | 32 | Y | 해당 종목의 평가손익을 기준으로 한 수익률 |
| `pdno` | 상품번호 | String | 12 | Y | 종목코드 |
| `bass_exrt` | 기준환율 | String | 31 | Y | 원화 평가 시 적용 환율 |
| `buy_crcy_cd` | 매수통화코드 | String | 3 | Y | USD : 미국달러 HKD : 홍콩달러 CNY : 중국위안화 JPY : 일본엔화 VND : 베트남동 |
| `ovrs_now_pric1` | 해외현재가격1 | String | 29 | Y | 해당 종목의 현재가 |
| `avg_unpr3` | 평균단가3 | String | 29 | Y | 해당 종목의 매수 평균 단가 |
| `tr_mket_name` | 거래시장명 | String | 60 | Y | 해당 종목의 거래시장명 |
| `natn_kor_name` | 국가한글명 | String | 60 | Y | 거래 국가명 |
| `pchs_rmnd_wcrc_amt` | 매입잔액원화금액 | String | 19 | Y |  |
| `thdt_buy_ccld_frcr_amt` | 당일매수체결외화금액 | String | 30 | Y | 당일 매수 외화금액 (Type: Object X String O) |
| `thdt_sll_ccld_frcr_amt` | 당일매도체결외화금액 | String | 30 | Y | 당일 매도 외화금액 |
| `unit_amt` | 단위금액 | String | 19 | Y |  |
| `std_pdno` | 표준상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `scts_dvsn_name` | 유가증권구분명 | String | 60 | Y |  |
| `loan_rmnd` | 대출잔액 | String | 19 | Y | 대출 미상환 금액 |
| `loan_dt` | 대출일자 | String | 8 | Y | 대출 실행일자 |
| `loan_expd_dt` | 대출만기일자 | String | 8 | Y | 대출 만기일자 |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 하노이거래소 VNSE : ... |
| `item_lnkg_excg_cd` | 종목연동거래소코드 | String | 4 | Y | prdt_dvsn(상품구분) : 직원용 데이터(Type: String, Length:2) |
| `output2` | 응답상세2 | String |  | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `crcy_cd_name` | 통화코드명 | String | 60 | Y |  |
| `frcr_buy_amt_smtl` | 외화매수금액합계 | String | 29 | Y | 해당 통화로 매수한 종목 전체의 매수금액 |
| `frcr_sll_amt_smtl` | 외화매도금액합계 | String | 29 | Y | 해당 통화로 매도한 종목 전체의 매수금액 |
| `frcr_dncl_amt_2` | 외화예수금액2 | String | 29 | Y | 외화로 표시된 외화사용가능금액 |
| `frst_bltn_exrt` | 최초고시환율 | String | 31 | Y |  |
| `frcr_buy_mgn_amt` | 외화매수증거금액 | String | 31 | Y | 매수증거금으로 사용된 외화금액 |
| `frcr_etc_mgna` | 외화기타증거금 | String | 31 | Y |  |
| `frcr_drwg_psbl_amt_1` | 외화출금가능금액1 | String | 29 | Y | 출금가능한 외화금액 |
| `frcr_evlu_amt2` | 출금가능원화금액 | String | 29 | Y | 출금가능한 원화금액 |
| `acpl_cstd_crcy_yn` | 현지보관통화여부 | String | 1 | Y |  |
| `nxdy_frcr_drwg_psbl_amt` | 익일외화출금가능금액 | String | 31 | Y |  |
| `output3` | 응답상세3 | String |  | Y |  |
| `pchs_amt_smtl` | 매입금액합계 | String | 19 | Y | 해외유가증권 매수금액의 원화 환산 금액 |
| `evlu_amt_smtl` | 평가금액합계 | String | 19 | Y | 해외유가증권 평가금액의 원화 환산 금액 |
| `evlu_pfls_amt_smtl` | 평가손익금액합계 | String | 19 | Y | 해외유가증권 평가손익의 원화 환산 금액 |
| `dncl_amt` | 예수금액 | String | 19 | Y |  |
| `cma_evlu_amt` | CMA평가금액 | String | 19 | Y |  |
| `tot_dncl_amt` | 총예수금액 | String | 19 | Y |  |
| `etc_mgna` | 기타증거금 | String | 19 | Y |  |
| `wdrw_psbl_tot_amt` | 인출가능총금액 | String | 19 | Y |  |
| `frcr_evlu_tota` | 외화평가총액 | String | 19 | Y |  |
| `evlu_erng_rt1` | 평가수익율1 | String | 31 | Y |  |
| `pchs_amt_smtl_amt` | 매입금액합계금액 | String | 19 | Y |  |
| `evlu_amt_smtl_amt` | 평가금액합계금액 | String | 19 | Y |  |
| `tot_evlu_pfls_amt` | 총평가손익금액 | String | 31 | Y |  |
| `tot_asst_amt` | 총자산금액 | String | 19 | Y |  |
| `buy_mgn_amt` | 매수증거금액 | String | 19 | Y |  |
| `mgna_tota` | 증거금총액 | String | 19 | Y |  |
| `frcr_use_psbl_amt` | 외화사용가능금액 | String | 20 | Y |  |
| `ustl_sll_amt_smtl` | 미결제매도금액합계 | String | 19 | Y |  |
| `ustl_buy_amt_smtl` | 미결제매수금액합계 | String | 19 | Y |  |
| `tot_frcr_cblc_smtl` | 총외화잔고합계 | String | 29 | Y |  |
| `tot_loan_amt` | 총대출금액 | String | 19 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "prdt_name": "애플",
      "cblc_qty13": "40.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "thdt_sll_ccld_qty1": "0.00000000",
      "ccld_qty_smtl1": "40.00000000",
      "ord_psbl_qty1": "40.00000000",
      "frcr_pchs_amt": "6411629.00000",
      "frcr_evlu_amt2": "8491110.000000",
      "evlu_pfls_amt2": "2079481.00000",
      "evlu_pfls_rt1": "32.43000000",
      "pdno": "AAPL",
      "bass_exrt": "1212.60000000",
      "buy_crcy_cd": "USD",
      "ovrs_now_pric1": "212277.75600",
      "avg_unpr3": "160290.7250",
      "tr_mket_name": "나스닥",
      "natn_kor_name": "미국",
      "pchs_rmnd_wcrc_amt": "5986768",
      "thdt_buy_ccld_frcr_amt": "0.000000",
      "thdt_sll_ccld_frcr_amt": "0.000000",
      "unit_amt": "1",
      "std_pdno": "US0378331005",
      "prdt_type_cd": "512",
      "scts_dvsn_name": "현금",
      "loan_rmnd": "0",
      "loan_dt": "",
      "loan_expd_dt": "",
      "ovrs_excg_cd": "NASD",
      "item_lnkg_excg_cd": "NAS"
    },
    {
      "prdt_name": "테슬라",
      "cblc_qty13": "5.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "thdt_sll_ccld_qty1": "0.00000000",
      "ccld_qty_smtl1": "5.00000000",
      "ord_psbl_qty1": "5.00000000",
      "frcr_pchs_amt": "4665399.00000",
      "frcr_evlu_amt2": "6616309.000000",
      "evlu_pfls_amt2": "1950910.00000",
      "evlu_pfls_rt1": "41.81000000",
      "pdno": "TSLA",
      "bass_exrt": "1212.60000000",
      "buy_crcy_cd": "USD",
      "ovrs_now_pric1": "1323261.87600",
      "avg_unpr3": "933079.8000",
      "tr_mket_name": "나스닥",
      "natn_kor_name": "미국",
      "pchs_rmnd_wcrc_amt": "4560861",
      "thdt_buy_ccld_frcr_amt": "0.000000",
      "thdt_sll_ccld_frcr_amt": "0.000000",
      "unit_amt": "1",
      "std_pdno": "US88160R1014",
      "prdt_type_cd": "512",
      "scts_dvsn_name": "현금",
      "loan_rmnd": "0",
      "loan_dt": "",
      "loan_expd_dt": "",
      "ovrs_excg_cd": "NASD",
      "item_lnkg_excg_cd": "NAS"
    },
    {
      "prdt_name": "월트디즈니",
      "cblc_qty13": "24.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "thdt_sll_ccld_qty1": "0.00000000",
      "ccld_qty_smtl1": "24.00000000",
      "ord_psbl_qty1": "24.00000000",
      "frcr_pchs_amt": "5039237.00000",
      "frcr_evlu_amt2": "3946867.000000",
      "evlu_pfls_amt2": "-1092370.00000",
      "evlu_pfls_rt1": "-21.67000000",
      "pdno": "DIS",
      "bass_exrt": "1212.60000000",
      "buy_crcy_cd": "USD",
      "ovrs_now_pric1": "164452.81200",
      "avg_unpr3": "209968.2080",
      "tr_mket_name": "뉴욕거래소",
      "natn_kor_name": "미국",
      "pchs_rmnd_wcrc_amt": "4766780",
      "thdt_buy_ccld_frcr_amt": "0.000000",
      "thdt_sll_ccld_frcr_amt": "0.000000",
      "unit_amt": "1",
      "std_pdno": "US2546871060",
      "prdt_type_cd": "513",
      "scts_dvsn_name": "현금",
      "loan_rmnd": "0",
      "loan_dt": "",
      "loan_expd_dt": "",
      "ovrs_excg_cd": "NYSE",
      "item_lnkg_excg_cd": "NYS"
    },
    {
      "prdt_name": "[4689]Z홀딩스",
      "cblc_qty13": "1300.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "thdt_sll_ccld_qty1": "0.00000000",
      "ccld_qty_smtl1": "1300.00000000",
      "ord_psbl_qty1": "1300.00000000",
      "frcr_pchs_amt": "8556162.00000",
      "frcr_evlu_amt2": "6618273.000000",
      "evlu_pfls_amt2": "-1937889.00000",
      "evlu_pfls_rt1": "-22.64000000",
      "pdno": "4689",
      "bass_exrt": "981.11000000",
      "buy_crcy_cd": "JPY",
      "ovrs_now_pric1": "5090.97900",
      "avg_unpr3": "6581.6630",
      "tr_mket_name": "일본",
      "natn_kor_name": "일본",
      "pchs_rmnd_wcrc_amt": "9196585",
      "thdt_buy_ccld_frcr_amt": "0.000000",
      "thdt_sll_ccld_frcr_amt": "0.000000",
      "unit_amt": "100",
      "std_pdno": "JP3933800009",
      "prdt_type_cd": "515",
      "scts_dvsn_name": "현금",
      "loan_rmnd": "0",
      "loan_dt": "",
      "loan_expd_dt": "",
      "ovrs_excg_cd": "TKSE",
      "item_lnkg_excg_cd": "TSE"
    },
    {
      "prdt_name": "ARK GENOMIC REVOLUTION ETF",
      "cblc_qty13": "36.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "thdt_sll_ccld_qty1": "0.00000000",
      "ccld_qty_smtl1": "36.00000000",
      "ord_psbl_qty1": "36.00000000",
      "frcr_pchs_amt": "3746679.00000",
      "frcr_evlu_amt2": "2022471.000000",
      "evlu_pfls_amt2": "-1724208.00000",
      "evlu_pfls_rt1": "-46.01000000",
      "pdno": "ARKG",
      "bass_exrt": "1212.60000000",
      "buy_crcy_cd": "USD",
      "ovrs_now_pric1": "56179.75800",
      "avg_unpr3": "104074.4160",
      "tr_mket_name": "아멕스",
      "natn_kor_name": "미국",
      "pchs_rmnd_wcrc_amt": "3533904",
      "thdt_buy_ccld_frcr_amt": "0.000000",
      "thdt_sll_ccld_frcr_amt": "0.000000",
      "unit_amt": "1",
      "std_pdno": "US00214Q3020",
      "prdt_type_cd": "529",
      "scts_dvsn_name": "현금",
      "loan_rmnd": "0",
      "loan_dt": "",
      "loan_expd_dt": "",
      "ovrs_excg_cd": "AMEX",
      "item_lnkg_excg_cd": "AMS"
    },
    {
      "prdt_name": "[002747]애사돈자동화",
      "cblc_qty13": "400.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "thdt_sll_ccld_qty1": "0.00000000",
      "ccld_qty_smtl1": "400.00000000",
      "ord_psbl_qty1": "400.00000000",
      "frcr_pchs_amt": "2327369.00000",
      "frcr_evlu_amt2": "1525444.000000",
      "evlu_pfls_amt2": "-801925.00000",
      "evlu_pfls_rt1": "-34.45000000",
      "pdno": "002747",
      "bass_exrt": "190.30000000",
      "buy_crcy_cd": "CNY",
      "ovrs_now_pric1": "3813.61200",
      "avg_unpr3": "5818.4220",
      "tr_mket_name": "심천A",
      "natn_kor_name": "중화인민공화국",
      "pchs_rmnd_wcrc_amt": "2121990",
      "thdt_buy_ccld_frcr_amt": "0.000000",
      "thdt_sll_ccld_frcr_amt": "0.000000",
      "unit_amt": "1",
      "std_pdno": "CNE100001X35",
      "prdt_type_cd": "552",
      "scts_dvsn_name": "현금",
      "loan_rmnd": "0",
      "loan_dt": "",
      "loan_expd_dt": "",
      "ovrs_excg_cd": "SZAA",
      "item_lnkg_excg_c
```
