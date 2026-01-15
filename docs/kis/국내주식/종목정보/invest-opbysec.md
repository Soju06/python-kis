# 국내주식 증권사별 투자의견 [국내주식-189]

> [국내주식] 종목정보

국내주식 증권사별 투자의견 API입니다.
한국투자 HTS(eFriend Plus) > [0608] 증권사별 투자의견 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

한 번의 호출에 20건까지 조회가 가능하기에, 일자 파라미터(FID_INPUT_DATE_1, FID_INPUT_DATE_2)를 조절하여 다음 데이터 조회하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3a588de4-df48-49ac-88ca-9765998c00e1` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/invest-opbysec` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHKST663400C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17
- **최종 수정일**: 2025-05-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST663400C0 |
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
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 16634(Primary key) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) 참조) |
| `FID_DIV_CLS_CODE` | 분류구분코드 | String | 2 | Y | 전체(0) 매수(1) 중립(2) 매도(3) |
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y | 이후 ~ |
| `FID_INPUT_DATE_2` | 입력날짜2 | String | 10 | Y | ~ 이전 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_COND_SCR_DIV_CODE:16633
FID_INPUT_ISCD:999
FID_DIV_CLS_CODE:0
FID_INPUT_DATE_1:20240428
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
| `stck_shrn_iscd` | 주식단축종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `invt_opnn` | 투자의견 | String | 40 | Y |  |
| `invt_opnn_cls_code` | 투자의견구분코드 | String | 2 | Y |  |
| `rgbf_invt_opnn` | 직전투자의견 | String | 40 | Y |  |
| `rgbf_invt_opnn_cls_code` | 직전투자의견구분코드 | String | 2 | Y |  |
| `mbcr_name` | 회원사명 | String | 50 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `hts_goal_prc` | HTS목표가격 | String | 10 | Y |  |
| `stck_prdy_clpr` | 주식전일종가 | String | 10 | Y |  |
| `stft_esdg` | 주식선물괴리도 | String | 10 | Y |  |
| `dprt` | 괴리율 | String | 82 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240527",
            "stck_shrn_iscd": "454910",
            "hts_kor_isnm": "두산로보틱스",
            "invt_opnn": "NotRated",
            "invt_opnn_cls_code": "3",
            "rgbf_invt_opnn": "NotRated",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "상상인",
            "stck_prpr": "74300",
            "prdy_vrss": "500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.68",
            "hts_goal_prc": "0",
            "stck_prdy_clpr": "71600",
            "stft_esdg": "74300",
            "dprt": "0.00"
        },
        {
            "stck_bsop_date": "20240527",
            "stck_shrn_iscd": "389140",
            "hts_kor_isnm": "포바이포",
            "invt_opnn": "NotRated",
            "invt_opnn_cls_code": "3",
            "rgbf_invt_opnn": "NotRated",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "상상인",
            "stck_prpr": "10330",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "hts_goal_prc": "0",
            "stck_prdy_clpr": "10120",
            "stft_esdg": "10330",
            "dprt": "0.00"
        },
        {
            "stck_bsop_date": "20240527",
            "stck_shrn_iscd": "336260",
            "hts_kor_isnm": "두산퓨얼셀",
            "invt_opnn": "BUY",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "BUY",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "상상인",
            "stck_prpr": "26150",
            "prdy_vrss": "-50",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.19",
            "hts_goal_prc": "33000",
            "stck_prdy_clpr": "25000",
            "stft_esdg": "-6850",
            "dprt": "-20.76"
        },
        {
            "stck_bsop_date": "20240527",
            "stck_shrn_iscd": "298380",
            "hts_kor_isnm": "에이비엘바이오",
            "invt_opnn": "NotRated",
            "invt_opnn_cls_code": "3",
            "rgbf_invt_opnn": "NotRated",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "상상인",
            "stck_prpr": "23300",
            "prdy_vrss": "-100",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.43",
            "hts_goal_prc": "0",
            "stck_prdy_clpr": "24300",
            "stft_esdg": "23300",
            "dprt": "0.00"
        },
        {
            "stck_bsop_date": "20240527",
            "stck_shrn_iscd": "377740",
            "hts_kor_isnm": "바이오노트",
            "invt_opnn": "BUY",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "BUY",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "다올투자",
            "stck_prpr": "4135",
            "prdy_vrss": "-10",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.24",
            "hts_goal_prc": "5700",
            "stck_prdy_clpr": "4175",
            "stft_esdg": "-1565",
            "dprt": "-27.46"
        },
        {
            "stck_bsop_date": "20240527",
            "stck_shrn_iscd": "137310",
            "hts_kor_isnm": "에스디바이오센서",
            "invt_opnn": "HOLD",
            "invt_opnn_cls_code": "3",
            "rgbf_invt_opnn": "HOLD",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "다올투자",
            "stck_prpr": "10110",
            "prdy_vrss": "60",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.60",
            "hts_goal_prc": "11000",
            "stck_prdy_clpr": "10060",
            "stft_esdg": "-890",
            "dprt": "-8.09"
        },
        {
            "stck_bsop_date": "20240527",
            "stck_shrn_iscd": "298020",
            "hts_kor_isnm": "효성티앤씨",
            "invt_opnn": "매수",
            "invt_opnn_cls_code": "2",
            "rgbf_invt_opnn": "매수",
            "rgbf_invt_opnn_cls_code": "3",
            "mbcr_name": "IBK투자",
            "stck_prpr": "389000",
            "prdy_vrss": "-19000",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-4.66",
            "hts_goal_prc": "550000",
            "stck_prdy_clpr": "400500",
            "stft_esdg": "-161000",
            "dprt": "-29.27"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

