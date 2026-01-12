# ELW LP매매추이 [국내주식-182]

> [국내주식] ELW 시세

ELW LP매매추이 API입니다.
한국투자 HTS(eFriend Plus) > [0376] ELW LP매매추이 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `e5f413ec-3e68-47d7-931f-d7eb263990d9` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/lp-trade-trend` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHPEW03760000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
- **최종 수정일**: 2025-05-15

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPEW03760000 |
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
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 입력종목코드(ex 52K577(미래 K577KOSDAQ150콜) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_INPUT_ISCD:57K281
```

## 응답 (Response)

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
| `output1` | 응답상세 | String |   | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `prdy_vol` | 전일거래량 | String | 18 | Y |  |
| `stck_cnvr_rate` | 주식전환비율 | String | 136 | Y |  |
| `prit` | 패리티 | String | 112 | Y |  |
| `lvrg_val` | 레버리지값 | String | 114 | Y |  |
| `gear` | 기어링 | String | 84 | Y |  |
| `prls_qryr_rate` | 손익분기비율 | String | 84 | Y |  |
| `cfp` | 자본지지점 | String | 112 | Y |  |
| `invl_val` | 내재가치값 | String | 132 | Y |  |
| `tmvl_val` | 시간가치값 | String | 132 | Y |  |
| `acpr` | 행사가 | String | 112 | Y |  |
| `elw_ko_barrier` | 조기종료발생기준가격 | String | 112 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `lp_seln_qty` | LP매도수량 | String | 19 | Y |  |
| `lp_seln_avrg_unpr` | LP매도평균단가 | String | 19 | Y |  |
| `lp_shnu_qty` | LP매수수량 | String | 19 | Y |  |
| `lp_shnu_avrg_unpr` | LP매수평균단가 | String | 19 | Y |  |
| `lp_hvol` | LP보유량 | String | 18 | Y |  |
| `lp_hldn_rate` | LP보유비율 | String | 84 | Y |  |
| `prsn_deal_qty` | 개인매매수량 | String | 19 | Y |  |
| `apprch_rate` | 접근도 | String | 112 | Y |  |

### 응답 예시

```json
{
    "output1": {
        "elw_prpr": "40",
        "prdy_vrss_sign": "2",
        "prdy_vrss": "5",
        "prdy_ctrt": "14.29",
        "acml_vol": "320750",
        "prdy_vol": "114850",
        "stck_cnvr_rate": "0.010000",
        "prit": "103.35",
        "lvrg_val": "-12.130651",
        "gear": "19.3500",
        "prls_qryr_rate": "-1.8000",
        "cfp": "-1.7100",
        "invl_val": "27.00",
        "tmvl_val": "13.00",
        "acpr": "80000.00",
        "elw_ko_barrier": "0.00"
    },
    "output2": [
        {
            "stck_bsop_date": "20240516",
            "elw_prpr": "35",
            "prdy_vrss_sign": "3",
            "prdy_vrss": "0",
            "prdy_ctrt": "0.00",
            "lp_seln_qty": "30030",
            "lp_seln_avrg_unpr": "30",
            "lp_shnu_qty": "84810",
            "lp_shnu_avrg_unpr": "34",
            "lp_hvol": "7999900",
            "lp_hldn_rate": "99.99",
            "prsn_deal_qty": "10",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240514",
            "elw_prpr": "35",
            "prdy_vrss_sign": "5",
            "prdy_vrss": "-5",
            "prdy_ctrt": "-12.50",
            "lp_seln_qty": "73510",
            "lp_seln_avrg_unpr": "35",
            "lp_shnu_qty": "74440",
            "lp_shnu_avrg_unpr": "35",
            "lp_hvol": "7945120",
            "lp_hldn_rate": "99.31",
            "prsn_deal_qty": "1260",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240513",
            "elw_prpr": "40",
            "prdy_vrss_sign": "2",
            "prdy_vrss": "10",
            "prdy_ctrt": "33.33",
            "lp_seln_qty": "282010",
            "lp_seln_avrg_unpr": "36",
            "lp_shnu_qty": "277980",
            "lp_shnu_avrg_unpr": "36",
            "lp_hvol": "7944190",
            "lp_hldn_rate": "99.30",
            "prsn_deal_qty": "11140",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240510",
            "elw_prpr": "30",
            "prdy_vrss_sign": "2",
            "prdy_vrss": "5",
            "prdy_ctrt": "20.00",
            "lp_seln_qty": "137480",
            "lp_seln_avrg_unpr": "27",
            "lp_shnu_qty": "209950",
            "lp_shnu_avrg_unpr": "25",
            "lp_hvol": "7948220",
            "lp_hldn_rate": "99.35",
            "prsn_deal_qty": "2040",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240509",
            "elw_prpr": "25",
            "prdy_vrss_sign": "3",
            "prdy_vrss": "0",
            "prdy_ctrt": "0.00",
            "lp_seln_qty": "280020",
            "lp_seln_avrg_unpr": "25",
            "lp_shnu_qty": "209910",
            "lp_shnu_avrg_unpr": "25",
            "lp_hvol": "7875750",
            "lp_hldn_rate": "98.44",
            "prsn_deal_qty": "120",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240508",
            "elw_prpr": "25",
            "prdy_vrss_sign": "3",
            "prdy_vrss": "0",
            "prdy_ctrt": "0.00",
            "lp_seln_qty": "630000",
            "lp_seln_avrg_unpr": "25",
            "lp_shnu_qty": "630000",
            "lp_shnu_avrg_unpr": "25",
            "lp_hvol": "7945860",
            "lp_hldn_rate": "99.32",
            "prsn_deal_qty": "10000",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240507",
            "elw_prpr": "25",
            "prdy_vrss_sign": "5",
            "prdy_vrss": "-20",
            "prdy_ctrt": "-44.44",
            "lp_seln_qty": "98550",
            "lp_seln_avrg_unpr": "27",
            "lp_shnu_qty": "160420",
            "lp_shnu_avrg_unpr": "28",
            "lp_hvol": "7945860",
            "lp_hldn_rate": "99.32",
            "prsn_deal_qty": "26200",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240503",
            "elw_prpr": "45",
            "prdy_vrss_sign": "3",
            "prdy_vrss": "0",
            "prdy_ctrt": "0.00",
            "lp_seln_qty": "501890",
            "lp_seln_avrg_unpr": "40",
            "lp_shnu_qty": "491690",
            "lp_shnu_avrg_unpr": "40",
            "lp_hvol": "7883990",
            "lp_hldn_rate": "98.55",
            "prsn_deal_qty": "8440",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240502",
            "elw_prpr": "45",
            "prdy_vrss_sign": "3",
            "prdy_vrss": "0",
            "prdy_ctrt": "0.00",
            "lp_seln_qty": "402940",
            "lp_seln_avrg_unpr": "40",
            "lp_shnu_qty": "332240",
            "lp_shnu_avrg_unpr": "40",
            "lp_hvol": "7894190",
            "lp_hldn_rate": "98.67",
            "prsn_deal_qty": "54100",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240430",
            "elw_prpr": "45",
            "prdy_vrss_sign": "5",
            "prdy_vrss": "-5",
            "prdy_ctrt": "-10.00",
            "lp_seln_qty": "27840",
            "lp_seln_avrg_unpr": "48",
            "lp_shnu_qty": "33540",
            "lp_shnu_avrg_unpr": "45",
            "lp_hvol": "7964890",
            "lp_hldn_rate": "99.56",
            "prsn_deal_qty": "710",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240429",
            "elw_prpr": "50",
            "prdy_vrss_sign": "3",
            "prdy_vrss": "0",
            "prdy_ctrt": "0.00",
            "lp_seln_qty": "211510",
            "lp_seln_avrg_unpr": "50",
            "lp_shnu_qty": "175810",
            "lp_shnu_avrg_unpr": "50",
            "lp_hvol": "7959190",
            "lp_hldn_rate": "99.49",
            "prsn_deal_qty": "15700",
            "apprch_rate": "0.00"
        },
        {
            "stck_bsop_date": "20240426",
            "elw_prpr": "50",
            "prdy_vrss_sign": "3",
            "prdy_vrss": "0",
            "prdy_ctrt": "0.00",
            "lp_seln_qty": "35700",
            "lp_seln_avrg_unpr": "50",
            "lp_shnu_qty": "91400",
            "lp_shnu_avrg_unpr": "48",
            "lp_hvol": "7994890",
            "lp_hldn_rate": "99.93",
            "prsn_deal_qty": "60",
            "apprch_rate": "0.00"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
