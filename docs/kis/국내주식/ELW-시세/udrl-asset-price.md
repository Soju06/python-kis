# ELW 기초자산별 종목시세 [국내주식-186]

> [국내주식] ELW 시세

ELW 기초자산별 종목시세  API입니다.
한국투자 HTS(eFriend Plus) > [0288] ELW 기초자산별 ELW 시세 화면의 "우측 기초자산별 종목 리스트" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `263ef907-db8c-4bf6-8da9-388c8fb4cf10` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/udrl-asset-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKEW154101C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
- **최종 수정일**: 2025-05-07

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKEW154101C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | 시장구분(W) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | Uniquekey(11541) |
| `FID_MRKT_CLS_CODE` | 시장구분코드 | String | 2 | Y | 전체(A),콜(C),풋(P) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | '00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)' |
| `FID_UNAS_INPUT_ISCD` | 기초자산입력종목코드 | String | 12 | Y |  |
| `FID_VOL_CNT` | 거래량수 | String | 12 | Y | 전일거래량(정수량미만) |
| `FID_TRGT_EXLS_CLS_CODE` | 대상제외구분코드 | String | 32 | Y | 거래불가종목제외(0:미체크,1:체크) |
| `FID_INPUT_PRICE_1` | 입력가격1 | String | 12 | Y | 가격~원이상 |
| `FID_INPUT_PRICE_2` | 입력가격2 | String | 12 | Y | 가격~월이하 |
| `FID_INPUT_VOL_1` | 입력거래량1 | String | 18 | Y | 거래량~계약이상 |
| `FID_INPUT_VOL_2` | 입력거래량2 | String | 18 | Y | 거래량~계약이하 |
| `FID_INPUT_RMNN_DYNU_1` | 입력잔존일수1 | String | 5 | Y | 잔존일(~일이상) |
| `FID_INPUT_RMNN_DYNU_2` | 입력잔존일수2 | String | 5 | Y | 잔존일(~일이하) |
| `FID_OPTION` | 옵션 | String | 5 | Y | 옵션상태(0:없음,1:ATM,2:ITM,3:OTM) |
| `FID_INPUT_OPTION_1` | 입력옵션1 | String | 10 | Y |  |
| `FID_INPUT_OPTION_2` | 입력옵션2 | String | 10 | Y |  |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_COND_SCR_DIV_CODE:11541
FID_MRKT_CLS_CODE:A
FID_INPUT_ISCD:00000
FID_UNAS_INPUT_ISCD:005930
FID_VOL_CNT:
FID_TRGT_EXLS_CLS_CODE:0
FID_INPUT_PRICE_1:
FID_INPUT_PRICE_2:
FID_INPUT_VOL_1:
FID_INPUT_VOL_2:
FID_INPUT_RMNN_DYNU_1:
FID_INPUT_RMNN_DYNU_2:
FID_OPTION:0
FID_INPUT_OPTION_1:
FID_INPUT_OPTION_2:
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
| `output` | 응답상세 | Object |   | Y | array |
| `elw_shrn_iscd` | ELW단축종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `acpr` | 행사가 | String | 112 | Y |  |
| `prls_qryr_stpr_prc` | 손익분기주가가격 | String | 112 | Y |  |
| `hts_rmnn_dynu` | HTS잔존일수 | String | 5 | Y |  |
| `hts_ints_vltl` | HTS내재변동성 | String | 114 | Y |  |
| `stck_cnvr_rate` | 주식전환비율 | String | 136 | Y |  |
| `lp_hvol` | LP보유량 | String | 18 | Y |  |
| `lp_rlim` | LP비중 | String | 52 | Y |  |
| `lvrg_val` | 레버리지값 | String | 114 | Y |  |
| `gear` | 기어링 | String | 84 | Y |  |
| `delta_val` | 델타값 | String | 114 | Y |  |
| `gama` | 감마 | String | 84 | Y |  |
| `vega` | 베가 | String | 84 | Y |  |
| `theta` | 세타 | String | 84 | Y |  |
| `prls_qryr_rate` | 손익분기비율 | String | 84 | Y |  |
| `cfp` | 자본지지점 | String | 112 | Y |  |
| `prit` | 패리티 | String | 112 | Y |  |
| `invl_val` | 내재가치값 | String | 132 | Y |  |
| `tmvl_val` | 시간가치값 | String | 132 | Y |  |
| `hts_thpr` | HTS이론가 | String | 112 | Y |  |
| `stck_lstn_date` | 주식상장일자 | String | 8 | Y |  |
| `stck_last_tr_date` | 주식최종거래일자 | String | 8 | Y |  |
| `lp_ntby_qty` | LP순매도량 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "elw_shrn_iscd": "57JAAQ",
            "hts_kor_isnm": "한국JAAQ삼성전자풋",
            "elw_prpr": "10",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "63300.00",
            "prls_qryr_stpr_prc": "62300.00",
            "hts_rmnn_dynu": "42",
            "hts_ints_vltl": "60.72",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "17298270",
            "lp_rlim": "99.99",
            "lvrg_val": "-9.448319",
            "gear": "77.7000",
            "delta_val": "-0.121600",
            "gama": "0.0000",
            "vega": "0.5078",
            "theta": "0.5759",
            "prls_qryr_rate": "-19.8100",
            "cfp": "-19.5600",
            "prit": "81.46",
            "invl_val": "0.00",
            "tmvl_val": "10.00",
            "hts_thpr": "0.18",
            "stck_lstn_date": "20231018",
            "stck_last_tr_date": "20240613",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAML",
            "hts_kor_isnm": "한국JAML삼성전자콜",
            "elw_prpr": "120",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "64700.00",
            "prls_qryr_stpr_prc": "76700.00",
            "hts_rmnn_dynu": "7",
            "hts_ints_vltl": "0.00",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "11995780",
            "lp_rlim": "99.96",
            "lvrg_val": "5.184000",
            "gear": "6.4800",
            "delta_val": "0.800000",
            "gama": "0.0000",
            "vega": "0.0000",
            "theta": "0.0669",
            "prls_qryr_rate": "-1.4100",
            "cfp": "-1.6700",
            "prit": "120.24",
            "invl_val": "132.00",
            "tmvl_val": "-12.00",
            "hts_thpr": "131.60",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240509",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAMM",
            "hts_kor_isnm": "한국JAMM삼성전자콜",
            "elw_prpr": "115",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "67300.00",
            "prls_qryr_stpr_prc": "78800.00",
            "hts_rmnn_dynu": "42",
            "hts_ints_vltl": "32.23",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "12499500",
            "lp_rlim": "100.00",
            "lvrg_val": "6.288443",
            "gear": "6.7600",
            "delta_val": "0.930243",
            "gama": "0.0000",
            "vega": "0.3368",
            "theta": "0.2915",
            "prls_qryr_rate": "1.2800",
            "cfp": "1.5000",
            "prit": "115.60",
            "invl_val": "105.00",
            "tmvl_val": "10.00",
            "hts_thpr": "108.09",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240613",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAMN",
            "hts_kor_isnm": "한국JAMN삼성전자콜",
            "elw_prpr": "120",
            "prdy_vrss": "5",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.35",
            "acml_vol": "10",
            "acpr": "68700.00",
            "prls_qryr_stpr_prc": "80700.00",
            "hts_rmnn_dynu": "161",
            "hts_ints_vltl": "27.90",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "8800820",
            "lp_rlim": "84.62",
            "lvrg_val": "5.212408",
            "gear": "6.4800",
            "delta_val": "0.804384",
            "gama": "0.0000",
            "vega": "1.3937",
            "theta": "0.2545",
            "prls_qryr_rate": "3.7200",
            "cfp": "4.4000",
            "prit": "113.24",
            "invl_val": "91.00",
            "tmvl_val": "29.00",
            "hts_thpr": "111.27",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20241010",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAMP",
            "hts_kor_isnm": "한국JAMP삼성전자콜",
            "elw_prpr": "90",
            "prdy_vrss": "-10",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-10.00",
            "acml_vol": "20",
            "acpr": "70200.00",
            "prls_qryr_stpr_prc": "79200.00",
            "hts_rmnn_dynu": "70",
            "hts_ints_vltl": "28.96",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "12997850",
            "lp_rlim": "99.98",
            "lvrg_val": "7.137444",
            "gear": "8.6400",
            "delta_val": "0.826093",
            "gama": "0.0000",
            "vega": "0.8580",
            "theta": "0.3448",
            "prls_qryr_rate": "1.7900",
            "cfp": "2.0300",
            "prit": "110.82",
            "invl_val": "76.00",
            "tmvl_val": "14.00",
            "hts_thpr": "86.23",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240711",
            "lp_ntby_qty": "-20"
        },
        {
            "elw_shrn_iscd": "57JAMR",
            "hts_kor_isnm": "한국JAMR삼성전자콜",
            "elw_prpr": "75",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "73300.00",
            "prls_qryr_stpr_prc": "80800.00",
            "hts_rmnn_dynu": "98",
            "hts_ints_vltl": "27.07",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "13926710",
            "lp_rlim": "98.77",
            "lvrg_val": "7.394173",
            "gear": "10.3700",
            "delta_val": "0.713035",
            "gama": "0.0000",
            "vega": "1.3629",
            "theta": "0.3448",
            "prls_qryr_rate": "3.8500",
            "cfp": "4.2600",
            "prit": "106.13",
            "invl_val": "45.00",
            "tmvl_val": "30.00",
            "hts_thpr": "68.15",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240808",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAMS",
            "hts_kor_isnm": "한국JAMS삼성전자콜",
            "elw_prpr": "120",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "73300.00",
            "prls_qryr_stpr_prc": "85300.00",
            "hts_rmnn_dynu": "133",
            "hts_ints_vltl": "26.88",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "13399930",
            "lp_rlim": "100.00",
            "lvrg_val": "4.540122",
            "gear": "6.4800",
            "delta_val": "0.700636",
            "gama": "0.0000",
            "vega": "1.6226",
            "theta": "0.3056",
            "prls_qryr_rate": "9.6400",
            "cfp": "11.3900",
            "prit": "106.13",
            "invl_val": "45.00",
            "tmvl_val": "75.00",
            "hts_thpr": "74.43",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240912",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAPS",
            "hts_kor_isnm": "한국JAPS삼성전자풋",
            "elw_prpr": "10",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "70000.00",
            "prls_qryr_stpr_prc": "69000.00",
            "hts_rmnn_dynu": "42",
            "hts_ints_vltl": "39.14",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "8789750",
            "lp_rlim": "99.88",
            "lvrg_val": "-13.763233",
            "gear": "77.7000",
            "delta_val": "-0.177133",
            "gama": "0.0000",
            "vega": "0.6533",
            "theta": "0.4692",
            "prls_qryr_rate": "-11.1900",
            "cfp": "-11.0500",
            "prit": "90.09",
            "invl_val": "0.00",
            "tmvl_val": "10.00",
            "hts_thpr": "3.39",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240613",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAPT",
            "hts_kor_isnm": "한국JAPT삼성전자풋",
            "elw_prpr": "20",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "0",
            "acpr": "70000.00",
            "prls_qryr_stpr_prc": "68000.00",
            "hts_rmnn_dynu": "133",
            "hts_ints_vltl": "31.53",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "7593700",
            "lp_rlim": "99.92",
            "lvrg_val": "-9.186005",
            "gear": "38.8500",
            "delta_val": "-0.236448",
            "gama": "0.0000",
            "vega": "1.4404",
            "theta": "0.2237",
            "prls_qryr_rate": "-12.4800",
            "cfp": "-12.1700",
            "prit": "90.09",
            "invl_val": "0.00",
            "tmvl_val": "20.00",
            "hts_thpr": "13.97",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240912",
            "lp_ntby_qty": "0"
        },
        {
            "elw_shrn_iscd": "57JAZR",
            "hts_kor_isnm": "한국JAZR삼성전자콜",
            "elw_prpr": "70",
            "prdy_vrss": "-10",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-12.50",
            "acml_vol": "5130",
            "acpr": "77300.00",
            "prls_qryr_stpr_prc": "84300.00",
            "hts_rmnn_dynu": "196",
            "hts_ints_vltl": "26.13",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "13970240",
            "lp_rlim": "97.69",
            "lvrg_val": "6.527688",
            "gear": "11.1000",
            "delta_val": "0.588080",
            "gama": "0.0000",
            "vega": "2.1844",
            "theta": "0.2725",
            "prls_qryr_rate": "8.4900",
            "cfp": "9.3300",
            "prit": "100.51",
            "invl_val": "6.00",
            "tmvl_val": "64.00",
            "hts_thpr": "60.18",
            "stck_lstn_date": "20231220",
            "stck_last_tr_date": "20241114",
            "lp_ntby_qty": "5020"
        },
        {
            "elw_shrn_iscd": "57JAZS",
            "hts_kor_isnm": "한국JAZS삼성전자콜",
            "elw_prpr": "55",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "504200",
            "acpr": "75600.00",
            "prls_qryr_stpr_prc": "81100.00",
            "hts_rmnn_dynu": "70",
            "hts_ints_vltl": "28.73",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "15421560",
            "lp_rlim": "98.23",
            "lvrg_val": "8.965918",
            "gear": "14.1200",
            "delta_val": "0.634980",
            "gama": "0.0000",
            "vega": "1.2562",
            "theta": "0.4515",
            "prls_qryr_rate": "4.3700",
            "cfp": "4.7000",
            "prit": "102.77",
            "invl_val": "23.00",
            "tmvl_val": "32.00",
            "hts_thpr": "46.86",
            "stck_lstn_date": "20231220",
            "stck_last_tr_date": "20240711",
            "lp_ntby_qty": "45700"
        },...
        {
            "elw_shrn_iscd": "57KA61",
            "hts_kor_isnm": "한국KA61삼성전자콜",
            "elw_prpr": "40",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "331400",
            "acpr": "78300.00",
            "prls_qryr_stpr_prc": "82300.00",
            "hts_rmnn_dynu": "70",
            "hts_ints_vltl": "28.17",
            "stck_cnvr_rate": "0.010000",
            "lp_hvol": "23296960",
            "lp_rlim": "99.99",
            "lvrg_val": "10.171226",
            "gear": "19.4200",
            "delta_val": "0.523750",
            "gama": "0.0000",
            "vega": "1.3308",
            "theta": "0.4570",
            "prls_qryr_rate": "5.9200",
            "cfp": "6.2400",
            "prit": "99.23",
            "invl_val": "0.00",
            "tmvl_val": "40.00",
            "hts_thpr": "32.21",
            "stck_lstn_date": "20240320",
            "stck_last_tr_date": "20240711",
            "lp_ntby_qty": "0"
        }
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

