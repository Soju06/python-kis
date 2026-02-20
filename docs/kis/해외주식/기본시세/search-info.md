# 해외주식 상품기본정보[v1_해외주식-034]

> [해외주식] 기본시세

해외주식 상품기본정보 API입니다.
시세제공기관(연합)에서 제공하는 해외주식 상품기본정보 데이터를 확인하실 수 있습니다.

※ 해당자료는 시세제공기관(연합)의 자료를 제공하고 있으며, 오류와 지연이 발생할 수 있습니다.
※ 위 정보에 의한 투자판단의 최종책임은 정보이용자에게 있으며, 당사와 시세제공기관(연합)는 어떠한 법적인 책임도 지지 않사오니 투자에 참고로만 이용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `7f77a12b-b23c-4605-93ea-4e1b3c0356fb` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/search-info` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTPF1702R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-16T16:45:15+09:00
- **최종 수정일**: 2025-04-30T12:14:29+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTPF1702R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | 512  미국 나스닥 / 513  미국 뉴욕 / 529  미국 아멕스  515  일본 501  홍콩 / 543  홍콩CNY / 558  홍콩USD 507  베트남 하노이 / 508  베트남 호치민 551  중국 상해A / 552  중국 심천A |
| `PDNO` | 상품번호 | String | 12 | Y | 예) AAPL (애플) |

### 요청 예시

```json
{
  "PDNO": "AAPL",
  "PRDT_TYPE_CD": "512"
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세1 | String |   | Y |  |
| `std_pdno` | 표준상품번호 | String | 12 | Y |  |
| `prdt_eng_name` | 상품영문명 | String | 60 | Y |  |
| `natn_cd` | 국가코드 | String | 3 | Y |  |
| `natn_name` | 국가명 | String | 60 | Y |  |
| `tr_mket_cd` | 거래시장코드 | String | 2 | Y |  |
| `tr_mket_name` | 거래시장명 | String | 60 | Y |  |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | Y |  |
| `ovrs_excg_name` | 해외거래소명 | String | 60 | Y |  |
| `tr_crcy_cd` | 거래통화코드 | String | 3 | Y |  |
| `ovrs_papr` | 해외액면가 | String | 195 | Y |  |
| `crcy_name` | 통화명 | String | 60 | Y |  |
| `ovrs_stck_dvsn_cd` | 해외주식구분코드 | String | 2 | Y | 01.주식 02.WARRANT 03.ETF 04.우선주 |
| `prdt_clsf_cd` | 상품분류코드 | String | 6 | Y |  |
| `prdt_clsf_name` | 상품분류명 | String | 60 | Y |  |
| `sll_unit_qty` | 매도단위수량 | String | 10 | Y |  |
| `buy_unit_qty` | 매수단위수량 | String | 10 | Y |  |
| `tr_unit_amt` | 거래단위금액 | String | 238 | Y |  |
| `lstg_stck_num` | 상장주식수 | String | 19 | Y |  |
| `lstg_dt` | 상장일자 | String | 8 | Y |  |
| `ovrs_stck_tr_stop_dvsn_cd` | 해외주식거래정지구분코드 | String | 2 | Y | ※ 해당 값 지연 반영될 수 있는 점 유의 부탁드립니다.  01.정상 02.거래정지(ALL) 03.거래중단 04.매도정지 05.거래정지(위탁) 06.매수정지 |
| `lstg_abol_item_yn` | 상장폐지종목여부 | String | 1 | Y |  |
| `ovrs_stck_prdt_grp_no` | 해외주식상품그룹번호 | String | 20 | Y |  |
| `lstg_yn` | 상장여부 | String | 1 | Y |  |
| `tax_levy_yn` | 세금징수여부 | String | 1 | Y |  |
| `ovrs_stck_erlm_rosn_cd` | 해외주식등록사유코드 | String | 2 | Y |  |
| `ovrs_stck_hist_rght_dvsn_cd` | 해외주식이력권리구분코드 | String | 2 | Y |  |
| `chng_bf_pdno` | 변경전상품번호 | String | 12 | Y |  |
| `prdt_type_cd_2` | 상품유형코드2 | String | 3 | Y |  |
| `ovrs_item_name` | 해외종목명 | String | 60 | Y |  |
| `sedol_no` | SEDOL번호 | String | 15 | Y |  |
| `blbg_tckr_text` | 블름버그티커내용 | String | 100 | Y |  |
| `ovrs_stck_etf_risk_drtp_cd` | 해외주식ETF위험지표코드 | String | 3 | Y | 001.ETF 002.ETN 003.ETC(Exchage Traded Commodity) 004.Others(REIT's, Mutual Fund) 005.VIX Underlying ETF 006.VIX Underlying ETN |
| `etp_chas_erng_rt_dbnb` | ETP추적수익율배수 | String | 236 | Y |  |
| `istt_usge_isin_cd` | 기관용도ISIN코드 | String | 12 | Y |  |
| `mint_svc_yn` | MINT서비스여부 | String | 1 | Y |  |
| `mint_svc_yn_chng_dt` | MINT서비스여부변경일자 | String | 8 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `lei_cd` | LEI코드 | String | 20 | Y |  |
| `ovrs_stck_stop_rson_cd` | 해외주식정지사유코드 | String | 2 | Y | 01.권리발생 02.ISIN상이 03.기타 04.급등락종목 05.상장폐지(예정) 06.종목코드,거래소변경 07.PTP종목 |
| `lstg_abol_dt` | 상장폐지일자 | String | 8 | Y |  |
| `mini_stk_tr_stat_dvsn_cd` | 미니스탁거래상태구분코드 | String | 2 | Y | 01.정상 02.매매 불가 03.매수 불가 04.매도 불가 |
| `mint_frst_svc_erlm_dt` | MINT최초서비스등록일자 | String | 8 | Y |  |
| `mint_dcpt_trad_psbl_yn` | MINT소수점매매가능여부 | String | 1 | Y |  |
| `mint_fnum_trad_psbl_yn` | MINT정수매매가능여부 | String | 1 | Y |  |
| `mint_cblc_cvsn_ipsb_yn` | MINT잔고전환불가여부 | String | 1 | Y |  |
| `ptp_item_yn` | PTP종목여부 | String | 1 | Y |  |
| `ptp_item_trfx_exmt_yn` | PTP종목양도세면제여부 | String | 1 | Y |  |
| `ptp_item_trfx_exmt_strt_dt` | PTP종목양도세면제시작일자 | String | 8 | Y |  |
| `ptp_item_trfx_exmt_end_dt` | PTP종목양도세면제종료일자 | String | 8 | Y |  |
| `dtm_tr_psbl_yn` | 주간거래가능여부 | String | 1 | Y |  |
| `sdrf_stop_ecls_yn` | 급등락정지제외여부 | String | 1 | Y |  |
| `sdrf_stop_ecls_erlm_dt` | 급등락정지제외등록일자 | String | 8 | Y |  |
| `memo_text1` | 메모내용1 | String | 500 | Y |  |
| `ovrs_now_pric1` | 해외현재가격1 | String | 23 | Y | 23.5 |
| `last_rcvg_dtime` | 최종수신일시 | String | 14 | Y |  |

### 응답 예시

```json
{
  "output": {
    "std_pdno": "US0378331005",
    "prdt_eng_name": "APPLE INC",
    "natn_cd": "840",
    "natn_name": "미국",
    "tr_mket_cd": "01",
    "tr_mket_name": "나스닥",
    "ovrs_excg_cd": "NASD",
    "ovrs_excg_name": "나스닥",
    "tr_crcy_cd": "USD",
    "ovrs_papr": "0.00000",
    "crcy_name": "미국달러",
    "ovrs_stck_dvsn_cd": "01",
    "prdt_clsf_cd": "101210",
    "prdt_clsf_name": "해외주식",
    "sll_unit_qty": "1",
    "buy_unit_qty": "1",
    "tr_unit_amt": "0",
    "lstg_stck_num": "15441900000",
    "lstg_dt": "",
    "ovrs_stck_tr_stop_dvsn_cd": "01",
    "lstg_abol_item_yn": "N",
    "ovrs_stck_prdt_grp_no": "4621",
    "lstg_yn": "Y",
    "tax_levy_yn": "N",
    "ovrs_stck_erlm_rosn_cd": "00",
    "ovrs_stck_hist_rght_dvsn_cd": "00",
    "chng_bf_pdno": "",
    "prdt_type_cd_2": "",
    "ovrs_item_name": "",
    "sedol_no": "2046251",
    "blbg_tckr_text": "AAPL US",
    "ovrs_stck_etf_risk_drtp_cd": "",
    "etp_chas_erng_rt_dbnb": "0.000000",
    "istt_usge_isin_cd": "US0378331005",
    "mint_svc_yn": "Y",
    "mint_svc_yn_chng_dt": "20220711",
    "prdt_name": "애플",
    "lei_cd": "HWUPKR0MPOU8FGXBT394",
    "ovrs_stck_stop_rson_cd": "",
    "lstg_abol_dt": "",
    "mini_stk_tr_stat_dvsn_cd": "01",
    "mint_frst_svc_erlm_dt": "20220711",
    "mint_dcpt_trad_psbl_yn": "Y",
    "mint_fnum_trad_psbl_yn": "Y",
    "mint_cblc_cvsn_ipsb_yn": "N",
    "ptp_item_yn": "N",
    "ptp_item_trfx_exmt_yn": "N",
    "ptp_item_trfx_exmt_strt_dt": "",
    "ptp_item_trfx_exmt_end_dt": "",
    "dtm_tr_psbl_yn": "Y",
    "sdrf_stop_ecls_yn": "N",
    "sdrf_stop_ecls_erlm_dt": "00000000"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0530",
  "msg1": "조회되었습니다                                                                  "
}
```

