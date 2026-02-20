# 프로그램매매 종합현황(시간) [국내주식-114]

> [국내주식] 시세분석

프로그램매매 종합현황(시간) API입니다. 
한국투자 HTS(eFriend Plus) > [0460] 프로그램매매 종합현황 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 장시간(09:00~15:30) 동안의 최근 30분간의 데이터 확인이 가능하며, 다음조회가 불가합니다.
※ 장시간(09:00~15:30) 이후에는 bsop_hour 에 153000 ~ 170000 까지의 시간데이터가 출력되지만 데이터는 모두 동일한 장마감 데이터인 점 유의 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `0843477a-156b-4ac5-bf65-199b124b072f` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/comp-program-trade-today` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHPPG04600101` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03T12:40:22+09:00
- **최종 수정일**: 2025-06-13T10:44:48+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | '※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] (구)FHPPG04600100 → (신)FHPPG04600101' |
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
| `FID_COND_MRKT_DIV_CODE` | 시장 분류 코드 | String | 2 | Y | KRX : J , NXT : NX, 통합 : UN |
| `FID_MRKT_CLS_CODE` | 시장 구분 코드 | String | 2 | Y | K:코스피, Q:코스닥 |
| `FID_SCTN_CLS_CODE` | 구간 구분 코드 | String | 2 | Y | 공백 입력 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 공백 입력 |
| `FID_COND_MRKT_DIV_CODE1` | 시장 분류코드1 | String | 2 | Y | 공백 입력 |
| `FID_INPUT_HOUR_1` | 입력 시간1 | String | 10 | Y | 공백 입력 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_MRKT_CLS_CODE:Q
FID_SCTN_CLS_CODE:1
FID_INPUT_ISCD:
FID_COND_MRKT_DIV_CODE1:
FID_INPUT_HOUR_1:
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
| `bsop_hour` | 영업 시간 | String | 6 | Y |  |
| `arbt_smtn_seln_tr_pbmn` | 차익 합계 매도 거래 대금 | String | 18 | Y |  |
| `arbt_smtm_seln_tr_pbmn_rate` | 차익 합계 매도 거래대금 비율 | String | 72 | Y |  |
| `arbt_smtn_shnu_tr_pbmn` | 차익 합계 매수2 거래 대금 | String | 18 | Y |  |
| `arbt_smtm_shun_tr_pbmn_rate` | 차익합계매수거래대금비율 | String | 72 | Y |  |
| `nabt_smtn_seln_tr_pbmn` | 비차익 합계 매도 거래 대금 | String | 18 | Y |  |
| `nabt_smtm_seln_tr_pbmn_rate` | 비차익 합계 매도 거래대금 비율 | String | 72 | Y |  |
| `nabt_smtn_shnu_tr_pbmn` | 비차익 합계 매수2 거래 대금 | String | 18 | Y |  |
| `nabt_smtm_shun_tr_pbmn_rate` | 비차익합계매수거래대금비율 | String | 72 | Y |  |
| `arbt_smtn_ntby_tr_pbmn` | 차익 합계 순매수 거래 대금 | String | 18 | Y |  |
| `arbt_smtm_ntby_tr_pbmn_rate` | 차익 합계 순매수 거래대금 비율 | String | 72 | Y |  |
| `nabt_smtn_ntby_tr_pbmn` | 비차익 합계 순매수 거래 대금 | String | 18 | Y |  |
| `nabt_smtm_ntby_tr_pbmn_rate` | 비차익 합계 순매수 거래대금 비 | String | 72 | Y |  |
| `whol_smtn_ntby_tr_pbmn` | 전체 합계 순매수 거래 대금 | String | 18 | Y |  |
| `whol_ntby_tr_pbmn_rate` | 전체 순매수 거래대금 비율 | String | 72 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "bsop_hour": "170000",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981823",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859384",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136289",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165900",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165800",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165700",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165600",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165500",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165400",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165300",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165200",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165100",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "165000",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981818",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859379",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136284",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164900",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164800",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164700",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164600",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164500",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164400",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164300",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164200",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164100",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "164000",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122439",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981808",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859370",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136274",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163900",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163800",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163700",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163600",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163500",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163400",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163300",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163200",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    },
    {
      "bsop_hour": "163100",
      "arbt_smtn_seln_tr_pbmn": "63370",
      "arbt_smtm_seln_tr_pbmn_rate": "0.58",
      "arbt_smtn_shnu_tr_pbmn": "340275",
      "arbt_smtm_shun_tr_pbmn_rate": "3.11",
      "nabt_smtn_seln_tr_pbmn": "2122437",
      "nabt_smtm_seln_tr_pbmn_rate": "19.40",
      "nabt_smtn_shnu_tr_pbmn": "2981781",
      "nabt_smtm_shun_tr_pbmn_rate": "27.25",
      "arbt_smtn_ntby_tr_pbmn": "276905",
      "arbt_smtm_ntby_tr_pbmn_rate": "2.53",
      "nabt_smtn_ntby_tr_pbmn": "859343",
      "nabt_smtm_ntby_tr_pbmn_rate": "7.85",
      "whol_smtn_ntby_tr_pbmn": "1136248",
      "whol_ntby_tr_pbmn_rate": "10.39"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

