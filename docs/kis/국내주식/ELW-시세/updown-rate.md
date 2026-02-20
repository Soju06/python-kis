# ELW 상승률순위[국내주식-167]

> [국내주식] ELW 시세

ELW 상승률순위 API입니다. 
한국투자 HTS(eFriend Plus) > [0277] ELW 상승률순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `9f6b3c41-d44a-4ae1-8324-aa222d19c6bf` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/ranking/updown-rate` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPEW02770000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05T13:37:31+09:00
- **최종 수정일**: 2025-05-07T09:29:44+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02770000 |
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
| `FID_COND_MRKT_DIV_CODE` | 사용자권한정보 | String | 2 | Y | 시장구분코드 (W) |
| `FID_COND_SCR_DIV_CODE` | 거래소코드 | String | 5 | Y | Unique key(20277) |
| `FID_UNAS_INPUT_ISCD` | 상승율/하락율 구분 | String | 12 | Y | '000000(전체), 2001(코스피200) , 3003(코스닥150), 005930(삼성전자) ' |
| `FID_INPUT_ISCD` | N일자값 | String | 12 | Y | '00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)' |
| `FID_INPUT_RMNN_DYNU_1` | 거래량조건 | String | 5 | Y | '0(전체), 1(1개월이하), 2(1개월~2개월),  3(2개월~3개월), 4(3개월~6개월), 5(6개월~9개월),6(9개월~12개월), 7(12개월이상)' |
| `FID_DIV_CLS_CODE` | NEXT KEY BUFF | String | 2 | Y | 0(전체), 1(콜), 2(풋) |
| `FID_INPUT_PRICE_1` | 사용자권한정보 | String | 12 | Y |  |
| `FID_INPUT_PRICE_2` | 거래소코드 | String | 12 | Y |  |
| `FID_INPUT_VOL_1` | 상승율/하락율 구분 | String | 18 | Y |  |
| `FID_INPUT_VOL_2` | N일자값 | String | 18 | Y |  |
| `FID_INPUT_DATE_1` | 거래량조건 | String | 10 | Y |  |
| `FID_RANK_SORT_CLS_CODE` | NEXT KEY BUFF | String | 2 | Y | '0(상승율), 1(하락율), 2(시가대비상승율) , 3(시가대비하락율), 4(변동율)' |
| `FID_BLNG_CLS_CODE` | 사용자권한정보 | String | 2 | Y | 0(전체) |
| `FID_INPUT_DATE_2` | 거래소코드 | String | 10 | Y |  |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_COND_SCR_DIV_CODE:20277
FID_UNAS_INPUT_ISCD:000000
FID_INPUT_ISCD:00000
FID_INPUT_RMNN_DYNU_1:0
FID_DIV_CLS_CODE:0
FID_INPUT_PRICE_1:
FID_INPUT_PRICE_2:
FID_INPUT_VOL_1:
FID_INPUT_VOL_2:
FID_INPUT_DATE_1:1
FID_RANK_SORT_CLS_CODE:0
FID_BLNG_CLS_CODE:0
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
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `elw_shrn_iscd` | ELW단축종목코드 | String | 9 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `stck_sdpr` | 주식기준가 | String | 10 | Y |  |
| `sdpr_vrss_prpr_sign` | 기준가대비현재가부호 | String | 1 | Y |  |
| `sdpr_vrss_prpr` | 기준가대비현재가 | String | 10 | Y |  |
| `sdpr_vrss_prpr_rate` | 기준가대비현재가비율 | String | 84 | Y |  |
| `stck_oprc` | 주식시가2 | String | 10 | Y |  |
| `oprc_vrss_prpr_sign` | 시가2대비현재가부호 | String | 1 | Y |  |
| `oprc_vrss_prpr` | 시가2대비현재가 | String | 10 | Y |  |
| `oprc_vrss_prpr_rate` | 시가2대비현재가비율 | String | 84 | Y |  |
| `stck_hgpr` | 주식최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식최저가 | String | 10 | Y |  |
| `prd_rsfl_sign` | 기간등락부호 | String | 1 | Y |  |
| `prd_rsfl` | 기간등락 | String | 10 | Y |  |
| `prd_rsfl_rate` | 기간등락비율 | String | 84 | Y |  |
| `stck_cnvr_rate` | 주식전환비율 | String | 136 | Y |  |
| `hts_rmnn_dynu` | HTS잔존일수 | String | 5 | Y |  |
| `acpr` | 행사가 | String | 112 | Y |  |
| `unas_isnm` | 기초자산명 | String | 40 | Y |  |
| `unas_shrn_iscd` | 기초자산코드 | String | 12 | Y |  |
| `lp_hldn_rate` | LP보유비율 | String | 84 | Y |  |
| `prit` | 패리티 | String | 112 | Y |  |
| `prls_qryr_stpr_prc` | 손익분기주가가격 | String | 112 | Y |  |
| `delta_val` | 델타값 | String | 114 | Y |  |
| `theta` | 세타 | String | 84 | Y |  |
| `prls_qryr_rate` | 손익분기비율 | String | 84 | Y |  |
| `stck_lstn_date` | 주식상장일자 | String | 8 | Y |  |
| `stck_last_tr_date` | 주식최종거래일자 | String | 8 | Y |  |
| `hts_ints_vltl` | HTS내재변동성 | String | 114 | Y |  |
| `lvrg_val` | 레버리지값 | String | 114 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "hts_kor_isnm": "한국JAKWLS일렉콜",
            "elw_shrn_iscd": "57JAKW",
            "elw_prpr": "460",
            "prdy_vrss": "350",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "318.18",
            "acml_vol": "3320",
            "stck_sdpr": "110",
            "sdpr_vrss_prpr_sign": "2",
            "sdpr_vrss_prpr": "460",
            "sdpr_vrss_prpr_rate": "0.00",
            "stck_oprc": "470",
            "oprc_vrss_prpr_sign": "5",
            "oprc_vrss_prpr": "-10",
            "oprc_vrss_prpr_rate": "-2.13",
            "stck_hgpr": "605",
            "stck_lwpr": "0",
            "prd_rsfl_sign": "2",
            "prd_rsfl": "0",
            "prd_rsfl_rate": "34.44",
            "stck_cnvr_rate": "0.010000",
            "hts_rmnn_dynu": "63",
            "acpr": "95600.00",
            "unas_isnm": "LS ELECTRIC",
            "unas_shrn_iscd": "010120",
            "lp_hldn_rate": "99.96",
            "prit": "146.12",
            "prls_qryr_stpr_prc": "141600.00",
            "delta_val": "0.930744",
            "theta": "0.7829",
            "prls_qryr_rate": "1.3600",
            "stck_lstn_date": "20231116",
            "stck_last_tr_date": "20240613",
            "hts_ints_vltl": "71.91",
            "lvrg_val": "2.820154"
        },
        {
            "hts_kor_isnm": "KBJF27KOSPI200콜",
            "elw_shrn_iscd": "58JF27",
            "elw_prpr": "2395",
            "prdy_vrss": "1745",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "268.46",
            "acml_vol": "100",
            "stck_sdpr": "650",
            "sdpr_vrss_prpr_sign": "2",
            "sdpr_vrss_prpr": "2395",
            "sdpr_vrss_prpr_rate": "0.00",
            "stck_oprc": "2395",
            "oprc_vrss_prpr_sign": "3",
            "oprc_vrss_prpr": "0",
            "oprc_vrss_prpr_rate": "0.00",
            "stck_hgpr": "2395",
            "stck_lwpr": "0",
            "prd_rsfl_sign": "3",
            "prd_rsfl": "0",
            "prd_rsfl_rate": "0.00",
            "stck_cnvr_rate": "100.000000",
            "hts_rmnn_dynu": "28",
            "acpr": "345.00",
            "unas_isnm": "KOSPI200",
            "unas_shrn_iscd": "2001",
            "lp_hldn_rate": "99.99",
            "prit": "106.44",
            "prls_qryr_stpr_prc": "368.95",
            "delta_val": "0.900891",
            "theta": "13.8535",
            "prls_qryr_rate": "0.4600",
            "stck_lstn_date": "20231228",
            "stck_last_tr_date": "20240509",
            "hts_ints_vltl": "19.71",
            "lvrg_val": "13.810659"
        },
		...
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

