# 해외주식 기간손익[v1_해외주식-032]

> [해외주식] 주문/계좌

해외주식 기간손익 API입니다.
한국투자 HTS(eFriend Plus) > [7717] 해외 기간손익 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

[해외 기간손익 유의 사항]
■ 단순 매체결내역을 기초로 만든 화면으로 매도체결시점의 체결기준 매입단가와 비교하여 손익이 계산됩니다.
  결제일의 환율과 금액을 기준으로 산출하는 해외주식 양도소득세 계산방식과는 상이하오니, 참고용으로만 활용하여 주시기 바랍니다.
■ 기간손익은 매매일 익일부터 조회가능합니다.
﻿﻿■ 매입금액/매도금액 원화 환산 시 매도일의 환율이 적용되어있습니다.
﻿﻿■ 손익금액의 비용은 "매도비용" 만 포함되어있습니다. 단, 동일 종목의 매수/매도가 동시에 있는 경우에는 해당일 발생한 매수비용도 함께 계산됩니다.
﻿﻿■ 담보상환내역은 기간손익화면에 표시되지 많으니 참고하여 주시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `147d1d34-3001-4958-b970-106935a19fe7` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-period-profit` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTS3039R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-06-02
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
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTS3039R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 2 | Y | 공란 : 전체,  NASD : 미국, SEHK : 홍콩, SHAA : 중국, TKSE : 일본, HASE : 베트남 |
| `NATN_CD` | 국가코드 | String | 2 | Y | 공란(Default) |
| `CRCY_CD` | 통화코드 | String | 2 | Y | 공란 : 전체 USD : 미국달러, HKD : 홍콩달러, CNY : 중국위안화,  JPY : 일본엔화, VND : 베트남동 |
| `PDNO` | 상품번호 | String | 2 | Y | 공란 : 전체 |
| `INQR_STRT_DT` | 조회시작일자 | String | 2 | Y | YYYYMMDD |
| `INQR_END_DT` | 조회종료일자 | String | 2 | Y | YYYYMMDD |
| `WCRC_FRCR_DVSN_CD` | 원화외화구분코드 | String | 2 | Y | 01 : 외화, 02 : 원화 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 2 | Y |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 2 | Y |  |

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
| `Output1` | 응답상세 | Object |   | Y | array |
| `trad_day` | 매매일 | String | 8 | Y |  |
| `ovrs_pdno` | 해외상품번호 | String | 12 | Y |  |
| `ovrs_item_name` | 해외종목명 | String | 60 | Y |  |
| `slcl_qty` | 매도청산수량 | String | 10 | Y |  |
| `pchs_avg_pric` | 매입평균가격 | String | 184 | Y |  |
| `frcr_pchs_amt1` | 외화매입금액1 | String | 185 | Y |  |
| `avg_sll_unpr` | 평균매도단가 | String | 238 | Y |  |
| `frcr_sll_amt_smtl1` | 외화매도금액합계1 | String | 186 | Y |  |
| `stck_sll_tlex` | 주식매도제비용 | String | 184 | Y |  |
| `ovrs_rlzt_pfls_amt` | 해외실현손익금액 | String | 145 | Y |  |
| `pftrt` | 수익률 | String | 238 | Y |  |
| `exrt` | 환율 | String | 201 | Y |  |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | Y |  |
| `frst_bltn_exrt` | 최초고시환율 | String | 238 | Y |  |
| `Output2` | 응답상세2 | String |   | Y |  |
| `stck_sll_amt_smtl` | 주식매도금액합계 | String | 184 | Y | WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시 |
| `stck_buy_amt_smtl` | 주식매수금액합계 | String | 184 | Y | WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시 |
| `smtl_fee1` | 합계수수료1 | String | 138 | Y | WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시 |
| `excc_dfrm_amt` | 정산지급금액 | String | 205 | Y | WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시 |
| `ovrs_rlzt_pfls_tot_amt` | 해외실현손익총금액 | String | 145 | Y | WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시 |
| `tot_pftrt` | 총수익률 | String | 238 | Y |  |
| `bass_dt` | 기준일자 | String | 8 | Y |  |
| `exrt` | 환율 | String | 201 | Y |  |

