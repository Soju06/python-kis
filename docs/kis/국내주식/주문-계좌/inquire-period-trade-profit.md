# 기간별매매손익현황조회[v1_국내주식-060]

> [국내주식] 주문/계좌

기간별매매손익현황조회 API입니다.
한국투자 HTS(eFriend Plus) > [0856] 기간별 매매손익 화면 에서 "종목별" 클릭 시의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4755efc7-31c4-411c-af45-3e6948611f0a` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/inquire-period-trade-profit` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC8715R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-16
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | TTTC8715R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `SORT_DVSN` | 정렬구분 | String | 2 | Y | 00: 최근 순, 01: 과거 순, 02: 최근 순 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y |  |
| `PDNO` | 상품번호 | String | 12 | Y | ""공란입력 시, 전체 |
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y |  |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y |  |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y |  |
| `CBLC_DVSN` | 잔고구분 | String | 2 | Y | 00: 전체 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y |  |

### 요청 예시

```json
{
"CANO":"12345678",
"ACNT_PRDT_CD":"01",
"PDNO":"",
"INQR_STRT_DT":"20240216",
"INQR_END_DT":"20240216",
"SORT_DVSN":"02",
"CBLC_DVSN":"00",
"CTX_AREA_FK100":""
"CTX_AREA_FK100":""
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `ctx_area_nk100` | 연속조회키100 | String | 100 | Y |  |
| `ctx_area_fk100` | 연속조회검색조건100 | String | 100 | Y |  |
| `output1` | 응답상세 | Object |   | Y | array |
| `trad_dt` | 매매일자 | String | 8 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y | 종목번호(뒤 6자리만 해당) |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `trad_dvsn_name` | 매매구분명 | String | 60 | Y |  |
| `loan_dt` | 대출일자 | String | 8 | Y |  |
| `hldg_qty` | 보유수량 | String | 19 | Y |  |
| `pchs_unpr` | 매입단가 | String | 19 | Y |  |
| `buy_qty` | 매수수량 | String | 10 | Y |  |
| `buy_amt` | 매수금액 | String | 19 | Y |  |
| `sll_pric` | 매도가격 | String | 10 | Y |  |
| `sll_qty` | 매도수량 | String | 10 | Y |  |
| `sll_amt` | 매도금액 | String | 19 | Y |  |
| `rlzt_pfls` | 실현손익 | String | 19 | Y |  |
| `pfls_rt` | 손익률 | String | 238 | Y |  |
| `fee` | 수수료 | String | 19 | Y |  |
| `tl_tax` | 제세금 | String | 19 | Y |  |
| `loan_int` | 대출이자 | String | 19 | Y |  |
| `output2` | 응답상세2 | String |   | Y |  |
| `sll_qty_smtl` | 매도수량합계 | String | 19 | Y |  |
| `sll_tr_amt_smtl` | 매도거래금액합계 | String | 19 | Y |  |
| `sll_fee_smtl` | 매도수수료합계 | String | 19 | Y |  |
| `sll_tltx_smtl` | 매도제세금합계 | String | 19 | Y |  |
| `sll_excc_amt_smtl` | 매도정산금액합계 | String | 19 | Y |  |
| `buyqty_smtl` | 매수수량합계 | String | 8 | Y |  |
| `buy_tr_amt_smtl` | 매수거래금액합계 | String | 19 | Y |  |
| `buy_fee_smtl` | 매수수수료합계 | String | 19 | Y |  |
| `buy_tax_smtl` | 매수제세금합계 | String | 19 | Y |  |
| `buy_excc_amt_smtl` | 매수정산금액합계 | String | 19 | Y |  |
| `tot_qty` | 총수량 | String | 10 | Y |  |
| `tot_tr_amt` | 총거래금액 | String | 19 | Y |  |
| `tot_fee` | 총수수료 | String | 19 | Y |  |
| `tot_tltx` | 총제세금 | String | 19 | Y |  |
| `tot_excc_amt` | 총정산금액 | String | 19 | Y |  |
| `tot_rlzt_pfls` | 총실현손익 | String | 19 | Y |  |
| `loan_int` | 대출이자 | String | 19 | Y |  |
| `tot_pftrt` | 총수익률 | String | 238 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "                                                                                                    ",
  "ctx_area_nk100": "20240216^00000A000120^300^0^00000000^                                                               ",
  "output1": [
    {
      "trad_dt": "20240216",
      "pdno": "000J2552221D",
      "prdt_name": "SG 17WR",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "135",
      "buy_qty": "2",
      "buy_amt": "271",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "000J00532219",
      "prdt_name": "국동 9WR",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "130",
      "buy_qty": "10",
      "buy_amt": "1300",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000Q520057",
      "prdt_name": "미래에셋 인버스 2X 코스닥150 선물 ETN",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "1",
      "pchs_unpr": "9365",
      "buy_qty": "1",
      "buy_amt": "9365",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A900270",
      "prdt_name": "헝셩그룹",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "66",
      "pchs_unpr": "322",
      "buy_qty": "66",
      "buy_amt": "21252",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A402340",
      "prdt_name": "SK스퀘어",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "59000",
      "buy_qty": "10",
      "buy_amt": "590000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A373220",
      "prdt_name": "LG에너지솔루션",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "552000",
      "buy_qty": "10",
      "buy_amt": "5520000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A361610",
      "prdt_name": "SK아이이테크놀로지",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "110000",
      "buy_qty": "10",
      "buy_amt": "1100000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A352820",
      "prdt_name": "하이브",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "383000",
      "buy_qty": "2",
      "buy_amt": "766000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A302440",
      "prdt_name": "SK바이오사이언스",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "100000",
      "buy_qty": "10",
      "buy_amt": "1000000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A298050",
      "prdt_name": "효성첨단소재",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "480000",
      "buy_qty": "2",
      "buy_amt": "960000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A298020",
      "prdt_name": "효성티앤씨",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "365000",
      "buy_qty": "2",
      "buy_amt": "730000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A285130",
      "prdt_name": "SK케미칼",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "100000",
      "buy_qty": "10",
      "buy_amt": "1000000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A136480",
      "prdt_name": "하림",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "220",
      "pchs_unpr": "2893",
      "buy_qty": "226",
      "buy_amt": "526563",
      "sll_pric": "2936",
      "sll_qty": "7",
      "sll_amt": "20555",
      "rlzt_pfls": "304",
      "pfls_rt": "1.50116044",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A114090",
      "prdt_name": "GKL",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "1",
      "pchs_unpr": "15010",
      "buy_qty": "1",
      "buy_amt": "15010",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A097950",
      "prdt_name": "CJ제일제당",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "210500",
      "buy_qty": "10",
      "buy_amt": "2105000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A096770",
      "prdt_name": "SK이노베이션",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "228000",
      "buy_qty": "10",
      "buy_amt": "2280000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A093370",
      "prdt_name": "후성",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "15510",
      "buy_qty": "2",
      "buy_amt": "31020",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A057050",
      "prdt_name": "현대홈쇼핑",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "30100",
      "buy_qty": "2",
      "buy_amt": "60200",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A047050",
      "prdt_name": "포스코인터내셔널",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "74400",
      "buy_qty": "2",
      "buy_amt": "148800",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A036460",
      "prdt_name": "한국가스공사",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "27850",
      "buy_qty": "2",
      "buy_amt": "55700",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A035760",
      "prdt_name": "CJ ENM",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "11",
      "pchs_unpr": "58836",
      "buy_qty": "11",
      "buy_amt": "647200",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A035420",
      "prdt_name": "NAVER",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "356000",
      "buy_qty": "10",
      "buy_amt": "3560000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A035250",
      "prdt_name": "강원랜드",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "20950",
      "buy_qty": "10",
      "buy_amt": "209500",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A034730",
      "prdt_name": "SK",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "182700",
      "buy_qty": "10",
      "buy_amt": "1827000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A030200",
      "prdt_name": "KT",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "26050",
      "buy_qty": "10",
      "buy_amt": "260500",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A028670",
      "prdt_name": "팬오션",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "4865",
      "buy_qty": "2",
      "buy_amt": "9730",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A028260",
      "prdt_name": "삼성물산",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "5",
      "pchs_unpr": "156100",
      "buy_qty": "5",
      "buy_amt": "780500",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A018260",
      "prdt_name": "삼성에스디에스",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "250000",
      "buy_qty": "2",
      "buy_amt": "500000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A017670",
      "prdt_name": "SK텔레콤",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "50100",
      "buy_qty": "10",
      "buy_amt": "501000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A015760",
      "prdt_name": "한국전력",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "4",
      "pchs_unpr": "8030",
      "buy_qty": "4",
      "buy_amt": "32120",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A011790",
      "prdt_name": "SKC",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "49950",
      "buy_qty": "10",
      "buy_amt": "499500",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A011780",
      "prdt_name": "금호석유",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "200000",
      "buy_qty": "10",
      "buy_amt": "2000000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A009540",
      "prdt_name": "HD한국조선해양",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "170000",
      "buy_qty": "10",
      "buy_amt": "1700000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A008770",
      "prdt_name": "호텔신라",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "99850",
      "buy_qty": "2",
      "buy_amt": "199700",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A006260",
      "prdt_name": "LS",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "122000",
      "buy_qty": "10",
      "buy_amt": "1220000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A005940",
      "prdt_name": "NH투자증권",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "11710",
      "buy_qty": "10",
      "buy_amt": "117100",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A005930",
      "prdt_name": "삼성전자",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "1414",
      "pchs_unpr": "53213",
      "buy_qty": "1415",
      "buy_amt": "75510700",
      "sll_pric": "75900",
      "sll_qty": "1",
      "sll_amt": "75900",
      "rlzt_pfls": "22687",
      "pfls_rt": "42.63431868",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A005490",
      "prdt_name": "POSCO홀딩스",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "133500",
      "buy_qty": "10",
      "buy_amt": "1335000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A005380",
      "prdt_name": "현대차",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "240500",
      "buy_qty": "2",
      "buy_amt": "481000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A004800",
      "prdt_name": "효성",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "66400",
      "buy_qty": "2",
      "buy_amt": "132800",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A003670",
      "prdt_name": "포스코퓨처엠",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "531000",
      "buy_qty": "2",
      "buy_amt": "1062000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A003550",
      "prdt_name": "LG",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "105600",
      "buy_qty": "2",
      "buy_amt": "211200",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A002380",
      "prdt_name": "KCC",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "1",
      "pchs_unpr": "252000",
      "buy_qty": "1",
      "buy_amt": "252000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A001120",
      "prdt_name": "LX인터내셔널",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "1",
      "pchs_unpr": "34050",
      "buy_qty": "1",
      "buy_amt": "34050",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A000990",
      "prdt_name": "DB하이텍",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "23000",
      "buy_qty": "2",
      "buy_amt": "46000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A000670",
      "prdt_name": "영풍",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "4",
      "pchs_unpr": "640750",
      "buy_qty": "4",
      "buy_amt": "2563000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A000660",
      "prdt_name": "SK하이닉스",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "12",
      "pchs_unpr": "122583",
      "buy_qty": "10",
      "buy_amt": "1345000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A000270",
      "prdt_name": "기아",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "84500",
      "buy_qty": "10",
      "buy_amt": "845000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A000240",
      "prdt_name": "한국앤컴퍼니",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "2",
      "pchs_unpr": "23850",
      "buy_qty": "2",
      "buy_amt": "47700",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    },
    {
      "trad_dt": "20240216",
      "pdno": "00000A000210",
      "prdt_name": "DL",
      "trad_dvsn_name": "현금",
      "loan_dt": "",
      "hldg_qty": "10",
      "pchs_unpr": "50400",
      "buy_qty": "10",
      "buy_amt": "504000",
      "sll_pric": "0",
      "sll_qty": "0",
      "sll_amt": "0",
      "rlzt_pfls": "0",
      "pfls_rt": "0.00000000",
      "fee": "0",
      "tl_tax": "0",
      "loan_int": "0"
    }
  ],
  "output2": {
    "sll_qty_smtl": "8",
    "sll_tr_amt_smtl": "96455",
    "sll_fee_smtl": "0",
    "sll_tltx_smtl": "0",
    "sll_excc_amt_smtl": "96455",
    "buyqty_smtl": "2003",
    "buy_tr_amt_smtl": "116697331",
    "buy_fee_smtl": "0",
    "buy_tax_smtl": "0",
    "buy_excc_amt_smtl": "116697331",
    "tot_qty": "2011",
    "tot_tr_amt": "116793786",
    "tot_fee": "0",
    "tot_tltx": "0",
    "tot_excc_amt": "116793786",
    "tot_rlzt_pfls": "22991",
    "loan_int": "0",
    "tot_pftrt": "31.29560057"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0500",
  "msg1": "조회가 계속됩니다..다음버튼을 Click 하십시오.                                   "
}
```

