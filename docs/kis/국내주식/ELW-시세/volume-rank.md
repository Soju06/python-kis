# ELW 거래량순위[국내주식-168]

> [국내주식] ELW 시세

ELW 거래량순위 API입니다. 
한국투자 HTS(eFriend Plus) > [0278] ELW 거래량순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `6bd62480-d165-415e-9d82-bffe2f43aa7e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/ranking/volume-rank` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPEW02780000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
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
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02780000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | W |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 20278 |
| `FID_UNAS_INPUT_ISCD` | 기초자산입력종목코드 | String | 12 | Y | 000000 |
| `FID_INPUT_ISCD` | 발행사 | String | 12 | Y | 00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)' |
| `FID_INPUT_RMNN_DYNU_1` | 입력잔존일수 | String | 5 | Y |  |
| `FID_DIV_CLS_CODE` | 콜풋구분코드 | String | 2 | Y | 0(전체), 1(콜), 2(풋) |
| `FID_INPUT_PRICE_1` | 가격(이상) | String | 12 | Y | 거래가격1(이상) |
| `FID_INPUT_PRICE_2` | 가격(이하) | String | 12 | Y | 거래가격1(이하) |
| `FID_INPUT_VOL_1` | 거래량(이상) | String | 18 | Y | 거래량1(이상) |
| `FID_INPUT_VOL_2` | 거래량(이하) | String | 18 | Y | 거래량1(이하) |
| `FID_INPUT_DATE_1` | 조회기준일 | String | 10 | Y | 입력날짜(기준가 조회기준) |
| `FID_RANK_SORT_CLS_CODE` | 순위정렬구분코드 | String | 2 | Y | 0: 거래량순 1: 평균거래증가율 2: 평균거래회전율 3:거래금액순 4: 순매수잔량순 5: 순매도잔량순 |
| `FID_BLNG_CLS_CODE` | 소속구분코드 | String | 2 | Y | 0: 전체 |
| `FID_INPUT_ISCD_2` | LP발행사 | String | 8 | Y | 0000 |
| `FID_INPUT_DATE_2` | 만기일-최종거래일조회 | String | 10 | Y | 공백 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_COND_SCR_DIV_CODE:20278
FID_UNAS_INPUT_ISCD:000000
FID_INPUT_ISCD:00000
FID_INPUT_RMNN_DYNU_1:0
FID_DIV_CLS_CODE:0
FID_INPUT_PRICE_1:
FID_INPUT_PRICE_2:
FID_INPUT_VOL_1:
FID_INPUT_VOL_2:
FID_INPUT_DATE_1:
FID_RANK_SORT_CLS_CODE:0
FID_BLNG_CLS_CODE:0
FID_INPUT_ISCD_2:0000
FID_INPUT_DATE_2:
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
| `elw_kor_isnm` | ELW한글종목명 | String | 40 | Y |  |
| `elw_shrn_iscd` | ELW단축종목코드 | String | 9 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `lstn_stcn` | 상장주수 | String | 18 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `n_prdy_vol` | N전일거래량 | String | 18 | Y |  |
| `n_prdy_vol_vrss` | N전일거래량대비 | String | 18 | Y |  |
| `vol_inrt` | 거래량증가율 | String | 84 | Y |  |
| `vol_tnrt` | 거래량회전율 | String | 82 | Y |  |
| `nday_vol_tnrt` | N일거래량회전율 | String | 8 | Y |  |
| `acml_tr_pbmn` | 누적거래대금 | String | 18 | Y |  |
| `n_prdy_tr_pbmn` | N전일거래대금 | String | 18 | Y |  |
| `n_prdy_tr_pbmn_vrss` | N전일거래대금대비 | String | 18 | Y |  |
| `total_askp_rsqn` | 총매도호가잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총매수호가잔량 | String | 12 | Y |  |
| `ntsl_rsqn` | 순매도잔량 | String | 13 | Y |  |
| `ntby_rsqn` | 순매수잔량 | String | 12 | Y |  |
| `seln_rsqn_rate` | 매도잔량비율 | String | 84 | Y |  |
| `shnu_rsqn_rate` | 매수2잔량비율 | String | 84 | Y |  |
| `stck_cnvr_rate` | 주식전환비율 | String | 136 | Y |  |
| `hts_rmnn_dynu` | HTS잔존일수 | String | 5 | Y |  |
| `invl_val` | 내재가치값 | String | 132 | Y |  |
| `tmvl_val` | 시간가치값 | String | 132 | Y |  |
| `acpr` | 행사가 | String | 112 | Y |  |
| `lp_mbcr_name` | LP회원사명 | String | 50 | Y |  |
| `unas_isnm` | 기초자산명 | String | 40 | Y |  |
| `stck_last_tr_date` | 최종거래일 | String | 8 | Y |  |
| `unas_shrn_iscd` | 기초자산코드 | String | 12 | Y |  |
| `prdy_vol` | 전일거래량 | String | 18 | Y |  |
| `lp_hldn_rate` | LP보유비율 | String | 84 | Y |  |
| `prit` | 패리티 | String | 112 | Y |  |
| `prls_qryr_stpr_prc` | 손익분기주가가격 | String | 112 | Y |  |
| `delta_val` | 델타값 | String | 114 | Y |  |
| `theta` | 세타 | String | 84 | Y |  |
| `prls_qryr_rate` | 손익분기비율 | String | 84 | Y |  |
| `stck_lstn_date` | 주식상장일자 | String | 8 | Y |  |
| `hts_ints_vltl` | HTS내재변동성 | String | 114 | Y |  |
| `lvrg_val` | 레버리지값 | String | 114 | Y |  |
| `lp_ntby_qty` | LP순매도량 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "elw_kor_isnm": "한국JS54KOSPI200콜",
            "elw_shrn_iscd": "57JS54",
            "elw_prpr": "135",
            "prdy_vrss": "-100",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-42.55",
            "lstn_stcn": "10000000",
            "acml_vol": "44020240",
            "n_prdy_vol": "0",
            "n_prdy_vol_vrss": "44020240",
            "vol_inrt": "0.00",
            "vol_tnrt": "440.20",
            "nday_vol_tnrt": "440.20",
            "acml_tr_pbmn": "7881452400",
            "n_prdy_tr_pbmn": "7881452400",
            "n_prdy_tr_pbmn_vrss": "0",
            "total_askp_rsqn": "1512690",
            "total_bidp_rsqn": "337490",
            "ntsl_rsqn": "-1175200",
            "ntby_rsqn": "-1175200",
            "seln_rsqn_rate": "81.76",
            "shnu_rsqn_rate": "18.24",
            "stck_cnvr_rate": "100.000000",
            "hts_rmnn_dynu": "28",
            "invl_val": "0.00",
            "tmvl_val": "135.00",
            "acpr": "385.00",
            "lp_mbcr_name": "한국증권",
            "unas_isnm": "KOSPI200",
            "stck_last_tr_date": "20240509",
            "unas_shrn_iscd": "2001",
            "prdy_vol": "9013220",
            "lp_hldn_rate": "11.21",
            "prit": "95.38",
            "prls_qryr_stpr_prc": "386.35",
            "delta_val": "0.160726",
            "theta": "12.4577",
            "prls_qryr_rate": "5.2000",
            "stck_lstn_date": "20230817",
            "hts_ints_vltl": "16.98",
            "lvrg_val": "43.722294",
            "lp_ntby_qty": "5919560"
        },
        {
            "elw_kor_isnm": "한국JS57KOSPI200풋",
            "elw_shrn_iscd": "57JS57",
            "elw_prpr": "250",
            "prdy_vrss": "15",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "6.38",
            "lstn_stcn": "10000000",
            "acml_vol": "41360790",
            "n_prdy_vol": "0",
            "n_prdy_vol_vrss": "41360790",
            "vol_inrt": "0.00",
            "vol_tnrt": "413.61",
            "nday_vol_tnrt": "413.61",
            "acml_tr_pbmn": "9642006500",
            "n_prdy_tr_pbmn": "9642006500",
            "n_prdy_tr_pbmn_vrss": "0",
            "total_askp_rsqn": "591950",
            "total_bidp_rsqn": "320140",
            "ntsl_rsqn": "-271810",
            "ntby_rsqn": "-271810",
            "seln_rsqn_rate": "64.90",
            "shnu_rsqn_rate": "35.10",
            "stck_cnvr_rate": "100.000000",
            "hts_rmnn_dynu": "28",
            "invl_val": "0.00",
            "tmvl_val": "250.00",
            "acpr": "355.00",
            "lp_mbcr_name": "한국증권",
            "unas_isnm": "KOSPI200",
            "stck_last_tr_date": "20240509",
            "unas_shrn_iscd": "2001",
            "prdy_vol": "3829210",
            "lp_hldn_rate": "38.24",
            "prit": "96.66",
            "prls_qryr_stpr_prc": "352.50",
            "delta_val": "-0.227848",
            "theta": "15.2298",
            "prls_qryr_rate": "-4.0100",
            "stck_lstn_date": "20230817",
            "hts_ints_vltl": "19.27",
            "lvrg_val": "-33.470867",
            "lp_ntby_qty": "3929370"
        },
        {
            "elw_kor_isnm": "한국JS59KOSPI200풋",
            "elw_shrn_iscd": "57JS59",
            "elw_prpr": "165",
            "prdy_vrss": "5",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.12",
            "lstn_stcn": "11000000",
            "acml_vol": "34510630",
            "n_prdy_vol": "0",
            "n_prdy_vol_vrss": "34510630",
            "vol_inrt": "0.00",
            "vol_tnrt": "313.73",
            "nday_vol_tnrt": "313.73",
            "acml_tr_pbmn": "5293873100",
            "n_prdy_tr_pbmn": "5293873100",
            "n_prdy_tr_pbmn_vrss": "0",
            "total_askp_rsqn": "348740",
            "total_bidp_rsqn": "639850",
            "ntsl_rsqn": "291110",
            "ntby_rsqn": "291110",
            "seln_rsqn_rate": "35.28",
            "shnu_rsqn_rate": "64.72",
            "stck_cnvr_rate": "100.000000",
            "hts_rmnn_dynu": "28",
            "invl_val": "0.00",
            "tmvl_val": "165.00",
            "acpr": "350.00",
            "lp_mbcr_name": "한국증권",
            "unas_isnm": "KOSPI200",
            "stck_last_tr_date": "20240509",
            "unas_shrn_iscd": "2001",
            "prdy_vol": "7133790",
            "lp_hldn_rate": "37.29",
            "prit": "95.30",
            "prls_qryr_stpr_prc": "348.35",
            "delta_val": "-0.160062",
            "theta": "12.8688",
            "prls_qryr_rate": "-5.1400",
            "stck_lstn_date": "20230817",
            "hts_ints_vltl": "19.97",
            "lvrg_val": "-35.625000",
            "lp_ntby_qty": "3185360"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

