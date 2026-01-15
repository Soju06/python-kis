# 해외선물옵션 증거금상세 [해외선물-032]

> [해외선물옵션] 주문/계좌

해외선물옵션 증거금상세 API입니다.
한국투자 HTS(eFriend Force) > [0867] 해외선물옵션 증거금상세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

[증거금 상세설명]
- SPAN, EUREX 증거금
1. 가격변동증거금 : 보유하고 있는 미결제를 Product Class 별로 구간[SPAN-16구간, EUREX-29구간)손익 합계액 산출하며 최대손실구간의 금액을 해당 Class의 증거금으로 산정
2. 스프레드증거금 : 보유하고 있는 미결제를 Product Class 별로 스프레드 산정하며 스프레드 증거금 적용
** 스프레드 산정방법 : SPAN은 선물+옵션의 Delta Spread로 계산, EUREX는 선물의 Spread만 산정 보유중인 옵선가치를 평가하며 청산가치가 양수(고객미 수취할 금액이 있는 경우)에 해당하는 금액을 증거금에서 할인
3. 옵션가격증거금 : 보유중인 옵션가치를 평가하여 청산가치가 양수(고객이 수취할 금액이 있는 경우)에 해당하는 금액을 증거금에서 할인
**계산식 : MAXID, 온선평가대금 Class별 합계액) ** 산출된 값을 음수처리함 옵션 미결제약정에 대해 최소로 징구하는 증거금
4. 옵선최소증거금 증거금 : 옵션 미결제약정에 대해 최소로 징구하는 증거금
﻿** SPAN : 매도옵선회소증거금(행사가별로 상미)과 매수옵선최소증거금(계약당 1Tick에 해당하는 금액)
** EUREX : 매수옵선최소증거금(계약당 1Tick에 해당하는 금액)(EUREX는 매도옵션최소증거금이 가격변동증거금에 포함되어 있음)
5. 일방해소증거금 : (기본개념)보유중인 포트폴리오 중에서 머느 일방향을 전량 청산했을 경우 잔존하는 미결제 약정의 최대손실가능액을 사전에 징구함
가격상승포지션과 가격하락포지션에 대해 최불리증거금을 각각 산정하며 큰 금액을 증거금으로 장구
﻿* 가격장승포지션 : 선물매수포지션, 풋옵션매도포지션
﻿* 가격하락포지션 : 선물매도포지션, 콜옵션매도포지선

- 일반 증거금
1. 선물미결제증거금 : 선물미결제약정에 대해 계약당증거금율 적용
2. 매도옵션미결제증거금 : 매도옵션미결제약정에 대해 옵선계약당 증거금을 적용
** 옵션계약당증거금 : 각 종목별 최불리증거금액으로 해외 거래소에서 계산하며 제공되는 데이터임
3. 매수옵션미결제증거금 : 매수옵션최소증거금으로 1Tick에 해당하는 금액을 적용

- 주문 증거금
1. 선물 주문증거금 : 선물 미체결주문에 대해 계약당 증거금을 적용(신규주문에 한해 징수)
2. 매도옵션 주문증거금 : 옵션매도 미체결주문에 대해 계약당증거금을 적용(신규주문에 한해 징수)
3. 매수옵션 주문증거금 : 옵션매수 미체결주문에 대해 최소증거금(Tick Value와 10 중에서 큰 금액)과 만기행사예약한 미체결주문에 대한 행사예약증거금을 징수
4. 매수옵션 주문대금 : 옵션매수 미체결주문의 매수대금(주문가격을 기준으로 대금 산정, 시장가주문시 현재가 +50틱으로 매수대금 산정)
5. 매수옵선행사예약증거금 : 옵선매수 미결제약정 중에서 행사예약한 수량에 대해 기초자산선물의 계약당 증거금을 징수


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5ff633c1-c50d-4494-9456-0c558031c678` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/margin-detail` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `OTFM3115R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
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
| `tr_id` | 거래ID | String | 13 | Y | OTFM3115R |
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
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y |  |
| `CRCY_CD` | 통화코드 | String | 3 | Y | 'TKR(TOT_KRW), TUS(TOT_USD),  USD(미국달러), HKD(홍콩달러), CNY(중국위안화), JPY )일본엔화), VND(베트남동)' |
| `INQR_DT` | 조회일자 | String | 8 | Y |  |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:08
CRCY_CD:TKR
INQR_DT:20240522
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
| `output` | 응답상세 | String |   | Y |  |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `resp_dt` | 응답일자 | String | 8 | Y |  |
| `acnt_net_risk_mgna_aply_yn` | 계좌순위험증거금적용여부 | String | 1 | Y |  |
| `fm_ord_psbl_amt` | FM주문가능금액 | String | 20 | Y |  |
| `fm_add_mgn_amt` | FM추가증거금액 | String | 20 | Y |  |
| `fm_brkg_mgn_amt` | FM위탁증거금액 | String | 20 | Y |  |
| `fm_excc_brkg_mgn_amt` | FM정산위탁증거금액 | String | 20 | Y |  |
| `fm_ustl_mgn_amt` | FM미결제증거금액 | String | 20 | Y |  |
| `fm_mntn_mgn_amt` | FM유지증거금액 | String | 20 | Y |  |
| `fm_ord_mgn_amt` | FM주문증거금액 | String | 20 | Y |  |
| `fm_futr_ord_mgn_amt` | FM선물주문증거금액 | String | 20 | Y |  |
| `fm_opt_buy_ord_amt` | FM옵션매수주문금액 | String | 20 | Y |  |
| `fm_opt_sll_ord_mgn_amt` | FM옵션매도주문증거금액 | String | 20 | Y |  |
| `fm_opt_buy_ord_mgn_amt` | FM옵션매수주문증거금액 | String | 20 | Y |  |
| `fm_ecis_rsvn_mgn_amt` | FM행사예약증거금액 | String | 20 | Y |  |
| `fm_span_brkg_mgn_amt` | FMSPAN위탁증거금액 | String | 20 | Y |  |
| `fm_span_pric_altr_mgn_amt` | FMSPAN가격변동증거금액 | String | 20 | Y |  |
| `fm_span_term_sprd_mgn_amt` | FMSPAN기간스프레드증거금액 | String | 20 | Y |  |
| `fm_span_buy_opt_min_mgn_amt` | FMSPAN옵션가격증거금액 | String | 20 | Y |  |
| `fm_span_opt_min_mgn_amt` | FMSPAN옵션최소증거금액 | String | 20 | Y |  |
| `fm_span_tot_risk_mgn_amt` | FMSPAN총위험증거금액 | String | 20 | Y |  |
| `fm_span_mntn_mgn_amt` | FMSPAN유지증거금액 | String | 20 | Y |  |
| `fm_span_mntn_pric_altr_mgn_amt` | FMSPAN유지가격변동증거금액 | String | 20 | Y |  |
| `fm_span_mntn_term_sprd_mgn_amt` | FMSPAN유지기간스프레드증거금액 | String | 20 | Y |  |
| `fm_span_mntn_opt_pric_mgn_amt` | FMSPAN유지옵션가격증거금액 | String | 20 | Y |  |
| `fm_span_mntn_opt_min_mgn_amt` | FMSPAN유지옵션최소증거금액 | String | 20 | Y |  |
| `fm_span_mntn_tot_risk_mgn_amt` | FMSPAN유지총위험증거금액 | String | 20 | Y |  |
| `fm_eurx_brkg_mgn_amt` | FMEUREX위탁증거금액 | String | 20 | Y |  |
| `fm_eurx_pric_altr_mgn_amt` | FMEUREX가격변동증거금액 | String | 20 | Y |  |
| `fm_eurx_term_sprd_mgn_amt` | FMEUREX기간스프레드증거금액 | String | 20 | Y |  |
| `fm_eurx_opt_pric_mgn_amt` | FMEUREX옵션가격증거금액 | String | 20 | Y |  |
| `fm_eurx_buy_opt_min_mgn_amt` | FMEUREX매수옵션최소증거금액 | String | 20 | Y |  |
| `fm_eurx_tot_risk_mgn_amt` | FMEUREX총위험증거금액 | String | 20 | Y |  |
| `fm_eurx_mntn_mgn_amt` | FMEUREX유지증거금액 | String | 20 | Y |  |
| `fm_eurx_mntn_pric_altr_mgn_amt` | FMEUREX유지가격변동증거금액 | String | 20 | Y |  |
| `fm_eurx_mntn_term_sprd_mgn_amt` | FMEUREX기간스프레드증거금액 | String | 20 | Y |  |
| `fm_eurx_mntn_opt_pric_mgn_amt` | FMEUREX유지옵션가격증거금액 | String | 20 | Y |  |
| `fm_eurx_mntn_tot_risk_mgn_amt` | FMEUREX유지총위험증거금액 | String | 20 | Y |  |
| `fm_gnrl_brkg_mgn_amt` | FM일반위탁증거금액 | String | 20 | Y |  |
| `fm_futr_ustl_mgn_amt` | FM선물미결제증거금액 | String | 20 | Y |  |
| `fm_sll_opt_ustl_mgn_amt` | FM매도옵션미결제증거금액 | String | 20 | Y |  |
| `fm_buy_opt_ustl_mgn_amt` | FM매수옵션미결제증거금액 | String | 20 | Y |  |
| `fm_sprd_ustl_mgn_amt` | FM스프레드미결제증거금액 | String | 20 | Y |  |
| `fm_avg_dsct_mgn_amt` | FMAVG할인증거금액 | String | 20 | Y |  |
| `fm_gnrl_mntn_mgn_amt` | FM일반유지증거금액 | String | 20 | Y |  |
| `fm_futr_mntn_mgn_amt` | FM선물유지증거금액 | String | 20 | Y |  |
| `fm_opt_mntn_mgn_amt` | FM옵션유지증거금액 | String | 20 | Y |  |

### 응답 예시

```json
{
  "output": {
    "cano": "12345678",
    "acnt_prdt_cd": "08",
    "crcy_cd": "TKR",
    "resp_dt": "20240522",
    "acnt_net_risk_mgna_aply_yn": "Y",
    "fm_ord_psbl_amt": "86128052",
    "fm_add_mgn_amt": "0",
    "fm_brkg_mgn_amt": "49082990",
    "fm_excc_brkg_mgn_amt": "49082990",
    "fm_ustl_mgn_amt": "49082990",
    "fm_mntn_mgn_amt": "44620900",
    "fm_ord_mgn_amt": "0",
    "fm_futr_ord_mgn_amt": "0",
    "fm_opt_buy_ord_amt": "0",
    "fm_opt_sll_ord_mgn_amt": "0",
    "fm_opt_buy_ord_mgn_amt": "0",
    "fm_ecis_rsvn_mgn_amt": "0",
    "fm_span_brkg_mgn_amt": "49082990",
    "fm_span_pric_altr_mgn_amt": "49082990",
    "fm_span_term_sprd_mgn_amt": "0",
    "fm_span_buy_opt_min_mgn_amt": "0",
    "fm_span_opt_min_mgn_amt": "0",
    "fm_span_tot_risk_mgn_amt": "49082990",
    "fm_span_mntn_mgn_amt": "44620900",
    "fm_span_mntn_pric_altr_mgn_amt": "44620900",
    "fm_span_mntn_term_sprd_mgn_amt": "0",
    "fm_span_mntn_opt_pric_mgn_amt": "0",
    "fm_span_mntn_opt_min_mgn_amt": "0",
    "fm_span_mntn_tot_risk_mgn_amt": "44620900",
    "fm_eurx_brkg_mgn_amt": "0",
    "fm_eurx_pric_altr_mgn_amt": "0",
    "fm_eurx_term_sprd_mgn_amt": "0",
    "fm_eurx_opt_pric_mgn_amt": "0",
    "fm_eurx_buy_opt_min_mgn_amt": "0",
    "fm_eurx_tot_risk_mgn_amt": "0",
    "fm_eurx_mntn_mgn_amt": "0",
    "fm_eurx_mntn_pric_altr_mgn_amt": "0",
    "fm_eurx_mntn_term_sprd_mgn_amt": "0",
    "fm_eurx_mntn_opt_pric_mgn_amt": "0",
    "fm_eurx_mntn_tot_risk_mgn_amt": "0",
    "fm_gnrl_brkg_mgn_amt": "0",
    "fm_futr_ustl_mgn_amt": "0",
    "fm_sll_opt_ustl_mgn_amt": "0",
    "fm_buy_opt_ustl_mgn_amt": "0",
    "fm_sprd_ustl_mgn_amt": "0",
    "fm_avg_dsct_mgn_amt": "0",
    "fm_gnrl_mntn_mgn_amt": "0",
    "fm_futr_mntn_mgn_amt": "0",
    "fm_opt_mntn_mgn_amt": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

