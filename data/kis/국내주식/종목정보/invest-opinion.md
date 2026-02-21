# 국내주식 종목투자의견 [국내주식-188]

> [국내주식] 종목정보

국내주식 종목투자의견 API입니다.
한국투자 HTS(eFriend Plus) > [0605] 종목투자의견 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

한 번의 호출에 100건까지 조회가 가능하기에, 일자 파라미터(FID_INPUT_DATE_1, FID_INPUT_DATE_2)를 조절하여 다음 데이터 조회하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `9de56f62-938c-40df-970e-8fd13a59b445` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/invest-opinion` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHKST663300C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17T10:25:28+09:00
- **최종 수정일**: 2025-05-14T13:22:57+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST663300C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | J(시장 구분 코드) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 16633(Primary key) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 종목코드(ex) 005930(삼성전자)) |
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y | 이후 ~(ex) 0020231113) |
| `FID_INPUT_DATE_2` | 입력날짜2 | String | 10 | Y | ~ 이전(ex) 0020240513) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_COND_SCR_DIV_CODE:16633
FID_INPUT_ISCD:005930
FID_INPUT_DATE_1:20240101
FID_INPUT_DATE_2:20240528
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
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `invt_opnn` | 투자의견 | String | 40 | Y |  |
| `invt_opnn_cls_code` | 투자의견구분코드 | String | 2 | Y |  |
| `rgbf_invt_opnn` | 직전투자의견 | String | 40 | Y |  |
| `rgbf_invt_opnn_cls_code` | 직전투자의견구분코드 | String | 2 | Y |  |
| `mbcr_name` | 회원사명 | String | 50 | Y |  |
| `hts_goal_prc` | HTS목표가격 | String | 10 | Y |  |
| `stck_prdy_clpr` | 주식전일종가 | String | 10 | Y |  |
| `stck_nday_esdg` | 주식N일괴리도 | String | 10 | Y |  |
| `nday_dprt` | N일괴리율 | String | 82 | Y |  |
| `stft_esdg` | 주식선물괴리도 | String | 10 | Y |  |
| `dprt` | 괴리율 | String | 82 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240527",
            "invt_opnn": "매수",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "매수",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "SK",
            "hts_goal_prc": "105000",
            "stck_prdy_clpr": "75900",
            "stck_nday_esdg": "-29100",
            "nday_dprt": "-27.71",
            "stft_esdg": "-27400",
            "dprt": "-26.10"
        },
        {
            "stck_bsop_date": "20240520",
            "invt_opnn": "BUY",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "BUY",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "하이투자",
            "hts_goal_prc": "91000",
            "stck_prdy_clpr": "77400",
            "stck_nday_esdg": "-13600",
            "nday_dprt": "-14.95",
            "stft_esdg": "-13400",
            "dprt": "-14.73"
        },
        {
            "stck_bsop_date": "20240516",
            "invt_opnn": "매수",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "매수",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "미래에셋",
            "hts_goal_prc": "110000",
            "stck_prdy_clpr": "78300",
            "stck_nday_esdg": "-31700",
            "nday_dprt": "-28.82",
            "stft_esdg": "-32400",
            "dprt": "-29.45"
        },
        {
            "stck_bsop_date": "20240502",
            "invt_opnn": "BUY",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "BUY",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "다올투자",
            "hts_goal_prc": "105000",
            "stck_prdy_clpr": "77500",
            "stck_nday_esdg": "-27500",
            "nday_dprt": "-26.19",
            "stft_esdg": "-27400",
            "dprt": "-26.10"
        },
        {
            "stck_bsop_date": "20240502",
            "invt_opnn": "BUY",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "BUY",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "하이투자",
            "hts_goal_prc": "95000",
            "stck_prdy_clpr": "77500",
            "stck_nday_esdg": "-17500",
            "nday_dprt": "-18.42",
            "stft_esdg": "-17400",
            "dprt": "-18.32"
        },
        {
            "stck_bsop_date": "20240502",
            "invt_opnn": "BUY",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "BUY",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "KB",
            "hts_goal_prc": "120000",
            "stck_prdy_clpr": "77500",
            "stck_nday_esdg": "-42500",
            "nday_dprt": "-35.42",
            "stft_esdg": "-42400",
            "dprt": "-35.33"
        },
        {
            "stck_bsop_date": "20240502",
            "invt_opnn": "매수",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "매수",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "신한투자증권",
            "hts_goal_prc": "110000",
            "stck_prdy_clpr": "77500",
            "stck_nday_esdg": "-32500",
            "nday_dprt": "-29.55",
            "stft_esdg": "-32400",
            "dprt": "-29.45"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

