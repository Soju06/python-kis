# 장내채권 주문체결내역 [국내주식-127]

> [장내채권] 주문/계좌

장내채권 주문체결내역 API입니다. 
한국투자 HTS(eFriend Plus) > [0978] 장내채권주문 '채권주문체결' 탭의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4803d486-0b85-4d6f-9bc1-164fef860905` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/trading/inquire-daily-ccld` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTSC8013R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
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
| `tr_id` | 거래ID | String | 13 | Y | CTSC8013R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y | 종합계좌번호 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌상품코드 |
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y | 일자 ~ (1주일 이내) |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y | ~ 일자 (조회 당일) |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | %(전체), 01(매도), 02(매수) |
| `SORT_SQN_DVSN` | 정렬순서구분 | String | 2 | Y | 01(주문순서), 02(주문역순) |
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `NCCS_YN` | 미체결여부 | String | 1 | Y | N(전체), C(체결), Y(미체결) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
INQR_STRT_DT:20240401
INQR_END_DT:20240425
SLL_BUY_DVSN_CD:%
SORT_SQN_DVSN:01
PDNO:
NCCS_YN:N
CTX_AREA_FK200:
CTX_AREA_NK200:
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
| `output1` | 응답상세 | Object |  | Y |  |
| `tot_ord_qty` | 총주문수량 | String | 10 | Y |  |
| `tot_ccld_qty_smtl` | 총체결수량합계 | String | 19 | Y |  |
| `tot_bond_ccld_avg_unpr` | 총채권체결평균단가 | String | 182 | Y |  |
| `tot_ccld_amt_smtl` | 총체결금액합계 | String | 19 | Y |  |
| `output2` | 응답상세 | String |   | Y | array |
| `ord_dt` | 주문일자 | String | 8 | Y |  |
| `odno` | 주문번호 | String | 10 | Y |  |
| `orgn_odno` | 원주문번호 | String | 10 | Y |  |
| `ord_dvsn_name` | 주문구분명 | String | 60 | Y |  |
| `sll_buy_dvsn_cd_name` | 매도매수구분코드명 | String | 60 | Y |  |
| `shtn_pdno` | 단축상품번호 | String | 12 | Y |  |
| `prdt_abrv_name` | 상품약어명 | String | 60 | Y |  |
| `ord_qty` | 주문수량 | String | 10 | Y |  |
| `bond_ord_unpr` | 채권주문단가 | String | 182 | Y |  |
| `ord_tmd` | 주문시각 | String | 6 | Y |  |
| `tot_ccld_qty` | 총체결수량 | String | 10 | Y |  |
| `bond_avg_unpr` | 채권평균단가 | String | 182 | Y |  |
| `tot_ccld_amt` | 총체결금액 | String | 19 | Y |  |
| `loan_dt` | 대출일자 | String | 8 | Y |  |
| `buy_dt` | 매수일자 | String | 8 | Y |  |
| `samt_mket_ptci_yn_name` | 소액시장참여여부명 | String | 10 | Y |  |
| `sprx_psbl_yn_ifom` | 분리과세가능여부알림 | String | 60 | Y |  |
| `ord_mdia_dvsn_name` | 주문매체구분명 | String | 60 | Y |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | Y |  |
| `nccs_qty` | 미체결수량 | String | 10 | Y |  |
| `ord_gno_brno` | 주문채번지점번호 | String | 5 | Y |  |

### 응답 예시

```json
{
  "ctx_area_nk200": " !^                                                                                                                                                                                                     ",
  "ctx_area_fk200": "null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^null!^%!^null                                                                                     ",
  "output1": [
    {
      "ord_dt": "20240425",
      "odno": "0000015201",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수",
      "shtn_pdno": "KR6095572D81",
      "prdt_abrv_name": "AJ네트웍스63-2",
      "ord_qty": "1",
      "bond_ord_unpr": "10450.00",
      "ord_tmd": "102033",
      "tot_ccld_qty": "1",
      "bond_avg_unpr": "10250.00",
      "tot_ccld_amt": "1025",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "0",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015202",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수",
      "shtn_pdno": "KR6095572D81",
      "prdt_abrv_name": "AJ네트웍스63-2",
      "ord_qty": "1",
      "bond_ord_unpr": "10450.00",
      "ord_tmd": "135029",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "0",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015203",
      "orgn_odno": "0000015202",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "매수취소*",
      "shtn_pdno": "KR6095572D81",
      "prdt_abrv_name": "AJ네트웍스63-2",
      "ord_qty": "1",
      "bond_ord_unpr": "0.00",
      "ord_tmd": "135108",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "0",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015204",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수",
      "shtn_pdno": "KR101501D942",
      "prdt_abrv_name": "국민주택1종19-04",
      "ord_qty": "1",
      "bond_ord_unpr": "10929.90",
      "ord_tmd": "163441",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "1",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015205",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수",
      "shtn_pdno": "KR103502G990",
      "prdt_abrv_name": "국고01125-3909(19-6)",
      "ord_qty": "1",
      "bond_ord_unpr": "7299.00",
      "ord_tmd": "163612",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "1",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015206",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수",
      "shtn_pdno": "KR103502G990",
      "prdt_abrv_name": "국고01125-3909(19-6)",
      "ord_qty": "1",
      "bond_ord_unpr": "7299.00",
      "ord_tmd": "163618",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "1",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015207",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수",
      "shtn_pdno": "KR2088012A16",
      "prdt_abrv_name": "경남지역개발20-01",
      "ord_qty": "1",
      "bond_ord_unpr": "10206.60",
      "ord_tmd": "163922",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "1",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015208",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수",
      "shtn_pdno": "KR2088012A16",
      "prdt_abrv_name": "경남지역개발20-01",
      "ord_qty": "1",
      "bond_ord_unpr": "10206.60",
      "ord_tmd": "164006",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "1",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015209",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수거부",
      "shtn_pdno": "KR6095572D81",
      "prdt_abrv_name": "AJ네트웍스63-2",
      "ord_qty": "2",
      "bond_ord_unpr": "10450.00",
      "ord_tmd": "170002",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "0",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015210",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수거부",
      "shtn_pdno": "KR6095572D81",
      "prdt_abrv_name": "AJ네트웍스63-2",
      "ord_qty": "1",
      "bond_ord_unpr": "10400.00",
      "ord_tmd": "170010",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "0",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015211",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수거부",
      "shtn_pdno": "KR6095572D81",
      "prdt_abrv_name": "AJ네트웍스63-2",
      "ord_qty": "5",
      "bond_ord_unpr": "10400.00",
      "ord_tmd": "170015",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "0",
      "ord_gno_brno": "01790"
    },
    {
      "ord_dt": "20240425",
      "odno": "0000015212",
      "orgn_odno": "",
      "ord_dvsn_name": "보통",
      "sll_buy_dvsn_cd_name": "현금매수거부",
      "shtn_pdno": "KR6095572D81",
      "prdt_abrv_name": "AJ네트웍스63-2",
      "ord_qty": "5",
      "bond_ord_unpr": "10200.00",
      "ord_tmd": "170019",
      "tot_ccld_qty": "0",
      "bond_avg_unpr": "0.00",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "buy_dt": "",
      "samt_mket_ptci_yn_name": "일반시장",
      "sprx_psbl_yn_ifom": "종합과세",
      "ord_mdia_dvsn_name": "33",
      "sll_buy_dvsn_cd": "02",
      "nccs_qty": "0",
      "ord_gno_brno": "01790"
    }
  ],
  "output2": {
    "tot_ord_qty": "6",
    "tot_ccld_qty_smtl": "1",
    "tot_bond_ccld_avg_unpr": "10250.00",
    "tot_ccld_amt_smtl": "1025"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```

