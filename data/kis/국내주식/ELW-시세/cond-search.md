# ELW 종목검색 [국내주식-166]

> [국내주식] ELW 시세

ELW 종목검색 API입니다.
한국투자 HTS(eFriend Plus) > [0291] ELW 종목검색 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
한 번의 호출에 최대 100건까지 확인 가능합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `264533d3-00eb-4794-984a-fecb84350f39` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/cond-search` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKEW15100000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17T10:22:52+09:00
- **최종 수정일**: 2025-05-07T09:38:23+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKEW15100000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | ELW(W) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 화면번호(11510) |
| `FID_RANK_SORT_CLS_CODE` | 순위정렬구분코드 | String | 2 | Y | '정렬1정렬안함(0)종목코드(1)현재가(2)대비율(3)거래량(4)행사가격(5) 전환비율(6)상장일(7)만기일(8)잔존일수(9)레버리지(10)' |
| `FID_INPUT_CNT_1` | 입력수1 | String | 12 | Y | 정렬1기준 - 상위(1)하위(2) |
| `FID_RANK_SORT_CLS_CODE_2` | 순위정렬구분코드2 | String | 2 | Y | 정렬2 |
| `FID_INPUT_CNT_2` | 입력수2 | String | 12 | Y | 정렬2기준 - 상위(1)하위(2) |
| `FID_RANK_SORT_CLS_CODE_3` | 순위정렬구분코드3 | String | 2 | Y | 정렬3 |
| `FID_INPUT_CNT_3` | 입력수3 | String | 12 | Y | 정렬3기준 - 상위(1)하위(2) |
| `FID_TRGT_CLS_CODE` | 대상구분코드 | String | 32 | Y | 0:발행회사종목코드,1:기초자산종목코드,2:FID시장구분코드,3:FID입력날짜1(상장일), 4:FID입력날짜2(만기일),5:LP회원사종목코드,6:행사가기초자산비교>=(1) <=(2),  7:잔존일 이상 이하, 8:현재가, 9:전일대비율, 10:거래량, 11:최종거래일, 12:레버리지 |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 발행사종목코드전체(00000) |
| `FID_UNAS_INPUT_ISCD` | 기초자산입력종목코드 | String | 12 | Y |  |
| `FID_MRKT_CLS_CODE` | 시장구분코드 | String | 2 | Y | 권리유형전체(A)콜(CO)풋(PO) |
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y | 상장일전체(0)금일(1)7일이하(2)8~30일(3)31~90일(4) |
| `FID_INPUT_DATE_2` | 입력날짜2 | String | 10 | Y | 만기일전체(0)1개월(1)1~2(2)2~3(3)3~6(4)6~9(5)9~12(6)12이상(7) |
| `FID_INPUT_ISCD_2` | 입력종목코드2 | String | 8 | Y |  |
| `FID_ETC_CLS_CODE` | 기타구분코드 | String | 2 | Y | 행사가전체(0)>=(1) |
| `FID_INPUT_RMNN_DYNU_1` | 입력잔존일수1 | String | 5 | Y | 잔존일이상 |
| `FID_INPUT_RMNN_DYNU_2` | 입력잔존일수2 | String | 5 | Y | 잔존일이하 |
| `FID_PRPR_CNT1` | 현재가수1 | String | 11 | Y | 현재가이상 |
| `FID_PRPR_CNT2` | 현재가수2 | String | 11 | Y | 현재가이하 |
| `FID_RSFL_RATE1` | 등락비율1 | String | 132 | Y | 전일대비율이상 |
| `FID_RSFL_RATE2` | 등락비율2 | String | 132 | Y | 전일대비율이하 |
| `FID_VOL1` | 거래량1 | String | 18 | Y | 거래량이상 |
| `FID_VOL2` | 거래량2 | String | 18 | Y | 거래량이하 |
| `FID_APLY_RANG_PRC_1` | 적용범위가격1 | String | 18 | Y | 최종거래일from |
| `FID_APLY_RANG_PRC_2` | 적용범위가격2 | String | 18 | Y | 최종거래일to |
| `FID_LVRG_VAL1` | 레버리지값1 | String | 114 | Y |  |
| `FID_LVRG_VAL2` | 레버리지값2 | String | 114 | Y |  |
| `FID_VOL3` | 거래량3 | String | 18 | Y | LP종료일from |
| `FID_VOL4` | 거래량4 | String | 18 | Y | LP종료일to |
| `FID_INTS_VLTL1` | 내재변동성1 | String | 114 | Y | 내재변동성이상 |
| `FID_INTS_VLTL2` | 내재변동성2 | String | 114 | Y | 내재변동성이하 |
| `FID_PRMM_VAL1` | 프리미엄값1 | String | 132 | Y | 프리미엄이상 |
| `FID_PRMM_VAL2` | 프리미엄값2 | String | 132 | Y | 프리미엄이하 |
| `FID_GEAR1` | 기어링1 | String | 84 | Y | 기어링이상 |
| `FID_GEAR2` | 기어링2 | String | 84 | Y | 기어링이하 |
| `FID_PRLS_QRYR_RATE1` | 손익분기비율1 | String | 132 | Y | 손익분기이상 |
| `FID_PRLS_QRYR_RATE2` | 손익분기비율2 | String | 132 | Y | 손익분기이하 |
| `FID_DELTA1` | 델타1 | String | 84 | Y | 델타이상 |
| `FID_DELTA2` | 델타2 | String | 84 | Y | 델타이하 |
| `FID_ACPR1` | 행사가1 | String | 133 | Y |  |
| `FID_ACPR2` | 행사가2 | String | 133 | Y |  |
| `FID_STCK_CNVR_RATE1` | 주식전환비율1 | String | 94 | Y | 전환비율이상 |
| `FID_STCK_CNVR_RATE2` | 주식전환비율2 | String | 94 | Y | 전환비율이하 |
| `FID_DIV_CLS_CODE` | 분류구분코드 | String | 2 | Y | 0:전체,1:일반,2:조기종료 |
| `FID_PRIT1` | 패리티1 | String | 112 | Y | 패리티이상 |
| `FID_PRIT2` | 패리티2 | String | 112 | Y | 패리티이하 |
| `FID_CFP1` | 자본지지점1 | String | 112 | Y | 배리어이상 |
| `FID_CFP2` | 자본지지점2 | String | 112 | Y | 배리어이하 |
| `FID_INPUT_NMIX_PRICE_1` | 지수가격1 | String | 112 | Y | LP보유비율이상 |
| `FID_INPUT_NMIX_PRICE_2` | 지수가격2 | String | 112 | Y | LP보유비율이하 |
| `FID_EGEA_VAL1` | E기어링값1 | String | 132 | Y | 접근도이상 |
| `FID_EGEA_VAL2` | E기어링값2 | String | 132 | Y | 접근도이하 |
| `FID_INPUT_DVDN_ERT` | 배당수익율 | String | 112 | Y | 손익분기점이상 |
| `FID_INPUT_HIST_VLTL` | 역사적변동성 | String | 112 | Y | 손익분기점이하 |
| `FID_THETA1` | 세타1 | String | 84 | Y | MONEYNESS이상 |
| `FID_THETA2` | 세타2 | String | 84 | Y | MONEYNESS이하 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_COND_SCR_DIV_CODE:11510
FID_RANK_SORT_CLS_CODE:0
FID_INPUT_CNT_1:1
FID_RANK_SORT_CLS_CODE_2:
FID_INPUT_CNT_2:
FID_RANK_SORT_CLS_CODE_3:
FID_INPUT_CNT_3:
FID_TRGT_CLS_CODE:
FID_INPUT_ISCD:
FID_UNAS_INPUT_ISCD:
FID_MRKT_CLS_CODE:
FID_INPUT_DATE_1:
FID_INPUT_DATE_2:
FID_INPUT_ISCD_2:
FID_ETC_CLS_CODE:
FID_INPUT_RMNN_DYNU_1:
FID_INPUT_RMNN_DYNU_2:
FID_PRPR_CNT1:
FID_PRPR_CNT2:
FID_RSFL_RATE1:
FID_RSFL_RATE2:
FID_VOL1:
FID_VOL2:
FID_APLY_RANG_PRC_1:
FID_APLY_RANG_PRC_2:
FID_LVRG_VAL1:
FID_LVRG_VAL2:
FID_VOL3:
FID_VOL4:
FID_INTS_VLTL1:
FID_INTS_VLTL2:
FID_PRMM_VAL1:
FID_PRMM_VAL2:
FID_GEAR1:
FID_GEAR2:
FID_PRLS_QRYR_RATE1:
FID_PRLS_QRYR_RATE2:
FID_DELTA1:
FID_DELTA2:
FID_ACPR1:
FID_ACPR2:
FID_STCK_CNVR_RATE1:
FID_STCK_CNVR_RATE2:
FID_DIV_CLS_CODE:
FID_PRIT1:
FID_PRIT2:
FID_CFP1:
FID_CFP2:
FID_INPUT_NMIX_PRICE_1:
FID_INPUT_NMIX_PRICE_2:
FID_EGEA_VAL1:
FID_EGEA_VAL2:
FID_INPUT_DVDN_ERT:
FID_INPUT_HIST_VLTL:
FID_THETA1:
FID_THETA2:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `bond_shrn_iscd` | 채권단축종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `rght_type_name` | 권리유형명 | String | 40 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `acpr` | 행사가 | String | 112 | Y |  |
| `stck_cnvr_rate` | 주식전환비율 | String | 136 | Y |  |
| `stck_lstn_date` | 주식상장일자 | String | 8 | Y |  |
| `stck_last_tr_date` | 주식최종거래일자 | String | 8 | Y |  |
| `hts_rmnn_dynu` | HTS잔존일수 | String | 5 | Y |  |
| `unas_isnm` | 기초자산종목명 | String | 40 | Y |  |
| `unas_prpr` | 기초자산현재가 | String | 112 | Y |  |
| `unas_prdy_vrss` | 기초자산전일대비 | String | 112 | Y |  |
| `unas_prdy_vrss_sign` | 기초자산전일대비부호 | String | 1 | Y |  |
| `unas_prdy_ctrt` | 기초자산전일대비율 | String | 82 | Y |  |
| `unas_acml_vol` | 기초자산누적거래량 | String | 18 | Y |  |
| `moneyness` | MONEYNESS | String | 132 | Y |  |
| `atm_cls_name` | ATM구분명 | String | 10 | Y |  |
| `prit` | 패리티 | String | 112 | Y |  |
| `delta_val` | 델타값 | String | 114 | Y |  |
| `hts_ints_vltl` | HTS내재변동성 | String | 114 | Y |  |
| `tmvl_val` | 시간가치값 | String | 132 | Y |  |
| `gear` | 기어링 | String | 84 | Y |  |
| `lvrg_val` | 레버리지값 | String | 114 | Y |  |
| `prls_qryr_rate` | 손익분기비율 | String | 84 | Y |  |
| `cfp` | 자본지지점 | String | 112 | Y |  |
| `lstn_stcn` | 상장주수 | String | 18 | Y |  |
| `pblc_co_name` | 발행회사명 | String | 40 | Y |  |
| `lp_mbcr_name` | LP회원사명 | String | 50 | Y |  |
| `lp_hldn_rate` | LP보유비율 | String | 84 | Y |  |
| `elw_rght_form` | ELW권리형태 | String | 20 | Y |  |
| `elw_ko_barrier` | 조기종료발생기준가격 | String | 112 | Y |  |
| `apprch_rate` | 접근도 | String | 112 | Y |  |
| `unas_shrn_iscd` | 기초자산단축종목코드 | String | 9 | Y |  |
| `mtrt_date` | 만기일자 | String | 8 | Y |  |
| `prmm_val` | 프리미엄값 | String | 114 | Y |  |
| `stck_lp_fin_date` | 주식LP종료일자 | String | 8 | Y |  |
| `tick_conv_prc` | 틱환산가 | String | 11 | Y |  |
| `prls_qryr_stpr_prc` | 손익분기주가가격 | String | 112 | Y |  |
| `lp_hvol` | LP보유량 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "bond_shrn_iscd": "57JAES",
            "hts_kor_isnm": "한국JAESKOSPI200콜",
            "rght_type_name": "CALL",
            "elw_prpr": "1560",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "325.00",
            "stck_cnvr_rate": "100.000000",
            "stck_lstn_date": "20231018",
            "stck_last_tr_date": "20240613",
            "hts_rmnn_dynu": "1",
            "unas_isnm": "KOSPI200",
            "unas_prpr": "377.90",
            "unas_prdy_vrss": "6.78",
            "unas_prdy_vrss_sign": "2",
            "unas_prdy_ctrt": "1.83",
            "unas_acml_vol": "80478000",
            "moneyness": "16.277",
            "atm_cls_name": "ITM",
            "prit": "116.27",
            "delta_val": "1.000000",
            "hts_ints_vltl": "0.00",
            "tmvl_val": "-3751.00",
            "gear": "24.2200",
            "lvrg_val": "24.219999",
            "prls_qryr_rate": "-9.8600",
            "cfp": "-10.2900",
            "lstn_stcn": "10000000",
            "pblc_co_name": "한국투자증권(주)",
            "lp_mbcr_name": "한국증권",
            "lp_hldn_rate": "100.00",
            "elw_rght_form": "표준형",
            "elw_ko_barrier": "0.00",
            "apprch_rate": "0.00",
            "unas_shrn_iscd": "2001",
            "mtrt_date": "20240617",
            "prmm_val": "4.13",
            "stck_lp_fin_date": "20240613",
            "tick_conv_prc": "5.00",
            "prls_qryr_stpr_prc": "340.60",
            "lp_hvol": "9999800"
        },
        {
            "bond_shrn_iscd": "57JAET",
            "hts_kor_isnm": "한국JAETKOSPI200콜",
            "rght_type_name": "CALL",
            "elw_prpr": "4090",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "322.50",
            "stck_cnvr_rate": "100.000000",
            "stck_lstn_date": "20231018",
            "stck_last_tr_date": "20240613",
            "hts_rmnn_dynu": "1",
            "unas_isnm": "KOSPI200",
            "unas_prpr": "377.90",
            "unas_prdy_vrss": "6.78",
            "unas_prdy_vrss_sign": "2",
            "unas_prdy_ctrt": "1.83",
            "unas_acml_vol": "80478000",
            "moneyness": "17.178",
            "atm_cls_name": "ITM",
            "prit": "117.17",
            "delta_val": "1.000000",
            "hts_ints_vltl": "0.00",
            "tmvl_val": "-1471.00",
            "gear": "9.2300",
            "lvrg_val": "9.230000",
            "prls_qryr_rate": "-3.8300",
            "cfp": "-4.2900",
            "lstn_stcn": "9000000",
            "pblc_co_name": "한국투자증권(주)",
            "lp_mbcr_name": "한국증권",
            "lp_hldn_rate": "99.99",
            "elw_rght_form": "표준형",
            "elw_ko_barrier": "0.00",
            "apprch_rate": "0.00",
            "unas_shrn_iscd": "2001",
            "mtrt_date": "20240617",
            "prmm_val": "10.82",
            "stck_lp_fin_date": "20240613",
            "tick_conv_prc": "5.00",
            "prls_qryr_stpr_prc": "363.40",
            "lp_hvol": "8999270"
        },
        {
            "bond_shrn_iscd": "57JAEV",
            "hts_kor_isnm": "한국JAEVKOSPI200콜",
            "rght_type_name": "CALL",
            "elw_prpr": "4510",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "320.00",
            "stck_cnvr_rate": "100.000000",
            "stck_lstn_date": "20231018",
            "stck_last_tr_date": "20240613",
            "hts_rmnn_dynu": "1",
            "unas_isnm": "KOSPI200",
            "unas_prpr": "377.90",
            "unas_prdy_vrss": "6.78",
            "unas_prdy_vrss_sign": "2",
            "unas_prdy_ctrt": "1.83",
            "unas_acml_vol": "80478000",
            "moneyness": "18.094",
            "atm_cls_name": "ITM",
            "prit": "118.09",
            "delta_val": "0.963518",
            "hts_ints_vltl": "177.59",
            "tmvl_val": "-1301.00",
            "gear": "8.3700",
            "lvrg_val": "8.064646",
            "prls_qryr_rate": "-3.3800",
            "cfp": "-3.8400",
            "lstn_stcn": "11000000",
            "pblc_co_name": "한국투자증권(주)",
            "lp_mbcr_name": "한국증권",
            "lp_hldn_rate": "99.99",
            "elw_rght_form": "표준형",
            "elw_ko_barrier": "0.00",
            "apprch_rate": "0.00",
            "unas_shrn_iscd": "2001",
            "mtrt_date": "20240617",
            "prmm_val": "11.93",
            "stck_lp_fin_date": "20240613",
            "tick_conv_prc": "4.82",
            "prls_qryr_stpr_prc": "365.10",
            "lp_hvol": "10999000"
        },
        {
            "bond_shrn_iscd": "57JAEW",
            "hts_kor_isnm": "한국JAEWKOSPI200콜",
            "rght_type_name": "CALL",
            "elw_prpr": "2555",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "317.50",
            "stck_cnvr_rate": "100.000000",
            "stck_lstn_date": "20231018",
            "stck_last_tr_date": "20240613",
            "hts_rmnn_dynu": "1",
            "unas_isnm": "KOSPI200",
            "unas_prpr": "377.90",
            "unas_prdy_vrss": "6.78",
            "unas_prdy_vrss_sign": "2",
            "unas_prdy_ctrt": "1.83",
            "unas_acml_vol": "80478000",
            "moneyness": "19.024",
            "atm_cls_name": "ITM",
            "prit": "119.02",
            "delta_val": "0.959424",
            "hts_ints_vltl": "191.44",
            "tmvl_val": "-3506.00",
            "gear": "14.7900",
            "lvrg_val": "14.189881",
            "prls_qryr_rate": "-9.2100",
            "cfp": "-9.8800",
            "lstn_stcn": "9000000",
            "pblc_co_name": "한국투자증권(주)",
            "lp_mbcr_name": "한국증권",
            "lp_hldn_rate": "99.99",
            "elw_rght_form": "표준형",
            "elw_ko_barrier": "0.00",
            "apprch_rate": "0.00",
            "unas_shrn_iscd": "2001",
            "mtrt_date": "20240617",
            "prmm_val": "6.76",
            "stck_lp_fin_date": "20240613",
            "tick_conv_prc": "4.80",
            "prls_qryr_stpr_prc": "343.05",
            "lp_hvol": "8998900"
        },
        {
            "bond_shrn_iscd": "57JAEX",
            "hts_kor_isnm": "한국JAEXKOSPI200콜",
            "rght_type_name": "CALL",
            "elw_prpr": "4850",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "315.00",
            "stck_cnvr_rate": "100.000000",
            "stck_lstn_date": "20231018",
            "stck_last_tr_date": "20240613",
            "hts_rmnn_dynu": "1",
            "unas_isnm": "KOSPI200",
            "unas_prpr": "377.90",
            "unas_prdy_vrss": "6.78",
            "unas_prdy_vrss_sign": "2",
            "unas_prdy_ctrt": "1.83",
            "unas_acml_vol": "80478000",
            "moneyness": "19.968",
            "atm_cls_name": "ITM",
            "prit": "119.96",
            "delta_val": "0.959709",
            "hts_ints_vltl": "200.01",
            "tmvl_val": "-1461.00",
            "gear": "7.7900",
            "lvrg_val": "7.476133",
            "prls_qryr_rate": "-3.8000",
            "cfp": "-4.3600",
            "lstn_stcn": "10000000",
            "pblc_co_name": "한국투자증권(주)",
            "lp_mbcr_name": "한국증권",
            "lp_hldn_rate": "99.99",
            "elw_rght_form": "표준형",
            "elw_ko_barrier": "0.00",
            "apprch_rate": "0.00",
            "unas_shrn_iscd": "2001",
            "mtrt_date": "20240617",
            "prmm_val": "12.83",
            "stck_lp_fin_date": "20240613",
            "tick_conv_prc": "4.80",
            "prls_qryr_stpr_prc": "363.50",
            "lp_hvol": "9999400"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

