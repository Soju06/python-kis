# 해외주식 예약주문조회[v1_해외주식-013]

> [해외주식] 주문/계좌

해외주식 예약주문 조회 API입니다.
※ 모의투자는 사용 불가합니다.

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

[v1_해외주식-013]해외주식 예약주문조회

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `db7f9cb2-2ab8-43c6-a744-e996c309a801` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/order-resv-list` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `(미국) TTTT3039R (일본/중국/홍콩/베트남) TTTS3014R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-07-15
- **최종 수정일**: 2025-05-23

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] 미국 : TTTT3039R 일본, 중국, 홍콩, 베트남 : TTTS3014R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
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
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y | 조회시작일자(YYYYMMDD) |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y | 조회종료일자(YYYYMMDD) |
| `INQR_DVSN_CD` | 조회구분코드 | String | 2 | Y | 00 : 전체 01 : 일반해외주식  02 : 미니스탁 |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | [tr_id=TTTT3039R인 경우] 공백 입력 시 미국주식 전체조회 [tr_id=TTTS3014R인 경우] 공백 입력 시 아시아주식 전체조회  512 : 미국 나스닥 / ... |
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | [tr_id=TTTT3039R인 경우] 공백 입력 시 미국주식 전체조회 [tr_id=TTTS3014R인 경우] 공백 입력 시 아시아주식 전체조회  NASD : 나스닥 / NY... |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터) |

### 요청 예시

```json
"input": {
            "ACNT_PRDT_CD": "01",
            "CANO": "12345678",
            "CTX_AREA_FK200": "",
            "CTX_AREA_NK200": "",
            "INQR_DVSN_CD": "00",
            "INQR_END_DT": "20220709",
            "INQR_STRT_DT": "20220705",
            "OVRS_EXCG_CD": "SEHK",
            "PRDT_TYPE_CD": "501"
        }
```

## 응답 (Response)

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
| `ctx_area_fk200` | 연속조회검색조건200 | String | 200 | Y |  |
| `ctx_area_nk200` | 연속조회키200 | String | 200 | Y |  |
| `output` | 응답상세1 | String |  | N |  |
| `cncl_yn` | 취소여부 | String | 1 | N |  |
| `rsvn_ord_rcit_dt` | 예약주문접수일자 | String | 8 | N |  |
| `ovrs_rsvn_odno` | 해외예약주문번호 | String | 10 | N |  |
| `ord_dt` | 주문일자 | String | 8 | N |  |
| `ord_gno_brno` | 주문채번지점번호 | String | 5 | N |  |
| `odno` | 주문번호 | String | 10 | N |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | N |  |
| `sll_buy_dvsn_cd_name` | 매도매수구분명 | String | 60 | N |  |
| `ovrs_rsvn_ord_stat_cd` | 해외예약주문상태코드 | String | 2 | N |  |
| `ovrs_rsvn_ord_stat_cd_name` | 해외예약주문상태코드명 | String | 60 | N |  |
| `pdno` | 상품번호 | String | 12 | N |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | N |  |
| `prdt_name` | 상품명 | String | 60 | N |  |
| `ord_rcit_tmd` | 주문접수시각 | String | 6 | N |  |
| `ord_fwdg_tmd` | 주문전송시각 | String | 6 | N |  |
| `tr_dvsn_name` | 거래구분명 | String | 60 | N |  |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | N |  |
| `tr_mket_name` | 거래시장명 | String | 60 | N |  |
| `ord_stfno` | 주문직원번호 | String | 6 | N |  |
| `ft_ord_qty` | FT주문수량 | String | 10 | N |  |
| `ft_ord_unpr3` | FT주문단가3 | String | 27 | N |  |
| `ft_ccld_qty` | FT체결수량 | String | 10 | N |  |
| `nprc_rson_text` | 미처리사유내용 | String | 500 | N |  |
| `splt_buy_attr_name` | 분할매수속성명 | String | 60 | N | 정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시 |

### 응답 예시

```json
{
    "ctx_area_fk200": "12345678^01^20220809^20220830^00^                                                                                                                                                                       ",
    "ctx_area_nk200": "                                                                                                                                                                                                        ",
    "output": [
        {
            "cncl_yn": "N",
            "rsvn_ord_rcit_dt": "20250523",
            "ovrs_rsvn_odno": "0031111234",
            "ord_dt": "",
            "ord_gno_brno": "",
            "odno": "",
            "sll_buy_dvsn_cd": "02",
            "sll_buy_dvsn_cd_name": "TWAP지정가매수",
            "ovrs_rsvn_ord_stat_cd": "01",
            "ovrs_rsvn_ord_stat_cd_name": "접수",
            "pdno": "AAPL",
            "prdt_name": "애플",
            "ord_rcit_tmd": "161928",
            "ord_fwdg_tmd": "",
            "tr_dvsn_name": "접수",
            "ovrs_excg_cd": "NASD",
            "tr_mket_name": "NASDAQ",
            "ord_stfno": "999999",
            "ft_ord_qty": "100",
            "ft_ord_unpr3": "150.00000000",
            "ft_ccld_qty": "0",
            "ft_ccld_unpr3": "0.00000000",
            "nprc_rson_text": "",
            "splt_buy_attr_name": "00:00~04:00"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "KIOK0510",
    "msg1": "조회가 완료되었습니다                                                           "
}
```
