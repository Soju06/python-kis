# 종목별 프로그램매매추이(일별) [국내주식-113]

> [국내주식] 시세분석

국내주식 종목별 프로그램매매추이(일별) API입니다.
한국투자 HTS(eFriend Plus) > [0465] 종목별 프로그램 매매추이 화면(혹은 한국투자 MTS > 국내 현재가 > 기타수급 > 프로그램) 의 "일자별" 클릭 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5ff6b5de-85e8-47e3-bb41-3e427c487bb3` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/program-trade-by-stock-daily` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHPPG04650201` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
- **최종 수정일**: 2025-06-09

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | '※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] (구)FHPPG04650200 → (신)FHPPG04650201' |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | KRX : J , NXT : NX, 통합 : UN |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 |
| `FID_INPUT_DATE_1` | 입력 날짜1 | String | 10 | Y | 기준일 (ex 0020240308), 미입력시 당일부터 조회 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_INPUT_ISCD:005930
FID_INPUT_DATE_1:20240517
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
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_clpr` | 주식 종가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `whol_smtn_seln_vol` | 전체 합계 매도 거래량 | String | 18 | Y |  |
| `whol_smtn_shnu_vol` | 전체 합계 매수2 거래량 | String | 18 | Y |  |
| `whol_smtn_ntby_qty` | 전체 합계 순매수 수량 | String | 18 | Y |  |
| `whol_smtn_seln_tr_pbmn` | 전체 합계 매도 거래 대금 | String | 18 | Y |  |
| `whol_smtn_shnu_tr_pbmn` | 전체 합계 매수2 거래 대금 | String | 18 | Y |  |
| `whol_smtn_ntby_tr_pbmn` | 전체 합계 순매수 거래 대금 | String | 18 | Y |  |
| `whol_ntby_vol_icdc` | 전체 순매수 거래량 증감 | String | 10 | Y |  |
| `whol_ntby_tr_pbmn_icdc2` | 전체 순매수 거래 대금 증감2 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240517",
            "stck_clpr": "77400",
            "prdy_vrss": "-800",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-1.02",
            "acml_vol": "15698949",
            "acml_tr_pbmn": "1220563293000",
            "whol_smtn_seln_vol": "6910299",
            "whol_smtn_shnu_vol": "3468820",
            "whol_smtn_ntby_qty": "-3441479",
            "whol_smtn_seln_tr_pbmn": "536935491000",
            "whol_smtn_shnu_tr_pbmn": "270120727200",
            "whol_smtn_ntby_tr_pbmn": "-266814763800",
            "whol_ntby_vol_icdc": "-3989127",
            "whol_ntby_tr_pbmn_icdc2": "-311124223700"
        },
        {
            "stck_bsop_date": "20240516",
            "stck_clpr": "78200",
            "prdy_vrss": "-100",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.13",
            "acml_vol": "20989778",
            "acml_tr_pbmn": "1656384883213",
            "whol_smtn_seln_vol": "4747160",
            "whol_smtn_shnu_vol": "5294808",
            "whol_smtn_ntby_qty": "547648",
            "whol_smtn_seln_tr_pbmn": "374517364400",
            "whol_smtn_shnu_tr_pbmn": "418826824300",
            "whol_smtn_ntby_tr_pbmn": "44309459900",
            "whol_ntby_vol_icdc": "631626",
            "whol_ntby_tr_pbmn_icdc2": "50772364600"
        },
        {
            "stck_bsop_date": "20240514",
            "stck_clpr": "78300",
            "prdy_vrss": "-100",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.13",
            "acml_vol": "11763992",
            "acml_tr_pbmn": "920737809850",
            "whol_smtn_seln_vol": "2056263",
            "whol_smtn_shnu_vol": "1972285",
            "whol_smtn_ntby_qty": "-83978",
            "whol_smtn_seln_tr_pbmn": "160973460500",
            "whol_smtn_shnu_tr_pbmn": "154510555800",
            "whol_smtn_ntby_tr_pbmn": "-6462904700",
            "whol_ntby_vol_icdc": "867690",
            "whol_ntby_tr_pbmn_icdc2": "67673387000"
        },
        {
            "stck_bsop_date": "20240513",
            "stck_clpr": "78400",
            "prdy_vrss": "-800",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-1.01",
            "acml_vol": "18652344",
            "acml_tr_pbmn": "1460962492700",
            "whol_smtn_seln_vol": "3971918",
            "whol_smtn_shnu_vol": "3020250",
            "whol_smtn_ntby_qty": "-951668",
            "whol_smtn_seln_tr_pbmn": "311400439700",
            "whol_smtn_shnu_tr_pbmn": "237264148000",
            "whol_smtn_ntby_tr_pbmn": "-74136291700",
            "whol_ntby_vol_icdc": "-1111550",
            "whol_ntby_tr_pbmn_icdc2": "-87529870000"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

