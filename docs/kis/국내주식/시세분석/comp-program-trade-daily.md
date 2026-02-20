# 프로그램매매 종합현황(일별)[국내주식-115]

> [국내주식] 시세분석

프로그램매매 종합현황(일별) API입니다. 
한국투자 HTS(eFriend Plus) > [0460] 프로그램매매 종합현황 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

* 8개월 이상 과거 조회는 불가하며 에러메시지가 발생합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3b0af8ef-13b4-4514-a07a-1bc718d07005` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/comp-program-trade-daily` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPPG04600001` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05T13:25:19+09:00
- **최종 수정일**: 2025-06-17T13:48:14+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | '※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] (구)FHPPG04600000 → (신)FHPPG04600001' |
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
| `FID_COND_MRKT_DIV_CODE` | 시장 분류 코드 | String | 2 | Y | J : KRX, NX : NXT, UN : 통합 |
| `FID_MRKT_CLS_CODE` | 시장 구분 코드 | String | 2 | Y | K:코스피, Q:코스닥 |
| `FID_INPUT_DATE_1` | 검색시작일 | String | 10 | Y | 공백 입력, 입력 시 ~ 입력일자까지 조회됨 * 8개월 이상 과거 조회 불가 |
| `FID_INPUT_DATE_2` | 검색종료일 | String | 10 | Y | 공백 입력 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:UN
FID_MRKT_CLS_CODE:K
FID_INPUT_DATE_1:
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
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `nabt_entm_seln_tr_pbmn` | 비차익 위탁 매도 거래 대금 | String | 18 | Y |  |
| `nabt_onsl_seln_vol` | 비차익 자기 매도 거래량 | String | 18 | Y |  |
| `whol_onsl_seln_tr_pbmn` | 전체 자기 매도 거래 대금 | String | 18 | Y |  |
| `arbt_smtn_shnu_vol` | 차익 합계 매수2 거래량 | String | 18 | Y |  |
| `nabt_smtn_shnu_tr_pbmn` | 비차익 합계 매수2 거래 대금 | String | 18 | Y |  |
| `arbt_entm_ntby_qty` | 차익 위탁 순매수 수량 | String | 18 | Y |  |
| `nabt_entm_ntby_tr_pbmn` | 비차익 위탁 순매수 거래 대금 | String | 18 | Y |  |
| `arbt_entm_seln_vol` | 차익 위탁 매도 거래량 | String | 18 | Y |  |
| `nabt_entm_seln_vol_rate` | 비차익 위탁 매도 거래량 비율 | String | 82 | Y |  |
| `nabt_onsl_seln_vol_rate` | 비차익 자기 매도 거래량 비율 | String | 82 | Y |  |
| `whol_onsl_seln_tr_pbmn_rate` | 전체 자기 매도 거래 대금 비율 | String | 82 | Y |  |
| `arbt_smtm_shun_vol_rate` | 차익 합계 매수 거래량 비율 | String | 72 | Y |  |
| `nabt_smtm_shun_tr_pbmn_rate` | 비차익 합계 매수 거래대금 비율 | String | 72 | Y |  |
| `arbt_entm_ntby_qty_rate` | 차익 위탁 순매수 수량 비율 | String | 82 | Y |  |
| `nabt_entm_ntby_tr_pbmn_rate` | 비차익 위탁 순매수 거래 대금 | String | 82 | Y |  |
| `arbt_entm_seln_vol_rate` | 차익 위탁 매도 거래량 비율 | String | 82 | Y |  |
| `nabt_entm_seln_tr_pbmn_rate` | 비차익 위탁 매도 거래 대금 비 | String | 82 | Y |  |
| `nabt_onsl_seln_tr_pbmn` | 비차익 자기 매도 거래 대금 | String | 18 | Y |  |
| `whol_smtn_seln_vol` | 전체 합계 매도 거래량 | String | 18 | Y |  |
| `arbt_smtn_shnu_tr_pbmn` | 차익 합계 매수2 거래 대금 | String | 18 | Y |  |
| `whol_entm_shnu_vol` | 전체 위탁 매수2 거래량 | String | 18 | Y |  |
| `arbt_entm_ntby_tr_pbmn` | 차익 위탁 순매수 거래 대금 | String | 18 | Y |  |
| `nabt_onsl_ntby_qty` | 비차익 자기 순매수 수량 | String | 18 | Y |  |
| `arbt_entm_seln_tr_pbmn` | 차익 위탁 매도 거래 대금 | String | 18 | Y |  |
| `nabt_onsl_seln_tr_pbmn_rate` | 비차익 자기 매도 거래 대금 비 | String | 82 | Y |  |
| `whol_seln_vol_rate` | 전체 매도 거래량 비율 | String | 72 | Y |  |
| `arbt_smtm_shun_tr_pbmn_rate` | 차익 합계 매수 거래대금 비율 | String | 72 | Y |  |
| `whol_entm_shnu_vol_rate` | 전체 위탁 매수 거래량 비율 | String | 82 | Y |  |
| `arbt_entm_ntby_tr_pbmn_rate` | 차익 위탁 순매수 거래 대금 비 | String | 82 | Y |  |
| `nabt_onsl_ntby_qty_rate` | 비차익 자기 순매수 수량 비율 | String | 82 | Y |  |
| `arbt_entm_seln_tr_pbmn_rate` | 차익 위탁 매도 거래 대금 비율 | String | 82 | Y |  |
| `nabt_smtn_seln_vol` | 비차익 합계 매도 거래량 | String | 18 | Y |  |
| `whol_smtn_seln_tr_pbmn` | 전체 합계 매도 거래 대금 | String | 18 | Y |  |
| `nabt_entm_shnu_vol` | 비차익 위탁 매수2 거래량 | String | 18 | Y |  |
| `whol_entm_shnu_tr_pbmn` | 전체 위탁 매수2 거래 대금 | String | 18 | Y |  |
| `arbt_onsl_ntby_qty` | 차익 자기 순매수 수량 | String | 18 | Y |  |
| `nabt_onsl_ntby_tr_pbmn` | 비차익 자기 순매수 거래 대금 | String | 18 | Y |  |
| `arbt_onsl_seln_tr_pbmn` | 차익 자기 매도 거래 대금 | String | 18 | Y |  |
| `nabt_smtm_seln_vol_rate` | 비차익 합계 매도 거래량 비율 | String | 72 | Y |  |
| `whol_seln_tr_pbmn_rate` | 전체 매도 거래대금 비율 | String | 72 | Y |  |
| `nabt_entm_shnu_vol_rate` | 비차익 위탁 매수 거래량 비율 | String | 82 | Y |  |
| `whol_entm_shnu_tr_pbmn_rate` | 전체 위탁 매수 거래 대금 비율 | String | 82 | Y |  |
| `arbt_onsl_ntby_qty_rate` | 차익 자기 순매수 수량 비율 | String | 82 | Y |  |
| `nabt_onsl_ntby_tr_pbmn_rate` | 비차익 자기 순매수 거래 대금 | String | 82 | Y |  |
| `arbt_onsl_seln_tr_pbmn_rate` | 차익 자기 매도 거래 대금 비율 | String | 82 | Y |  |
| `nabt_smtn_seln_tr_pbmn` | 비차익 합계 매도 거래 대금 | String | 18 | Y |  |
| `arbt_entm_shnu_vol` | 차익 위탁 매수2 거래량 | String | 18 | Y |  |
| `nabt_entm_shnu_tr_pbmn` | 비차익 위탁 매수2 거래 대금 | String | 18 | Y |  |
| `whol_onsl_shnu_vol` | 전체 자기 매수2 거래량 | String | 18 | Y |  |
| `arbt_onsl_ntby_tr_pbmn` | 차익 자기 순매수 거래 대금 | String | 18 | Y |  |
| `nabt_smtn_ntby_qty` | 비차익 합계 순매수 수량 | String | 18 | Y |  |
| `arbt_onsl_seln_vol` | 차익 자기 매도 거래량 | String | 18 | Y |  |
| `nabt_smtm_seln_tr_pbmn_rate` | 비차익 합계 매도 거래대금 비율 | String | 72 | Y |  |
| `arbt_entm_shnu_vol_rate` | 차익 위탁 매수 거래량 비율 | String | 82 | Y |  |
| `nabt_entm_shnu_tr_pbmn_rate` | 비차익 위탁 매수 거래 대금 비 | String | 82 | Y |  |
| `whol_onsl_shnu_tr_pbmn` | 전체 자기 매수2 거래 대금 | String | 18 | Y |  |
| `arbt_onsl_ntby_tr_pbmn_rate` | 차익 자기 순매수 거래 대금 비 | String | 82 | Y |  |
| `nabt_smtm_ntby_qty_rate` | 비차익 합계 순매수 수량 비율 | String | 72 | Y |  |
| `arbt_onsl_seln_vol_rate` | 차익 자기 매도 거래량 비율 | String | 82 | Y |  |
| `whol_entm_seln_vol` | 전체 위탁 매도 거래량 | String | 18 | Y |  |
| `arbt_entm_shnu_tr_pbmn` | 차익 위탁 매수2 거래 대금 | String | 18 | Y |  |
| `nabt_onsl_shnu_vol` | 비차익 자기 매수2 거래량 | String | 18 | Y |  |
| `whol_onsl_shnu_tr_pbmn_rate` | 전체 자기 매수 거래 대금 비율 | String | 82 | Y |  |
| `arbt_smtn_ntby_qty` | 차익 합계 순매수 수량 | String | 18 | Y |  |
| `nabt_smtn_ntby_tr_pbmn` | 비차익 합계 순매수 거래 대금 | String | 18 | Y |  |
| `arbt_smtn_seln_vol` | 차익 합계 매도 거래량 | String | 18 | Y |  |
| `whol_entm_seln_tr_pbmn` | 전체 위탁 매도 거래 대금 | String | 18 | Y |  |
| `arbt_entm_shnu_tr_pbmn_rate` | 차익 위탁 매수 거래 대금 비율 | String | 82 | Y |  |
| `nabt_onsl_shnu_vol_rate` | 비차익 자기 매수 거래량 비율 | String | 82 | Y |  |
| `whol_onsl_shnu_vol_rate` | 전체 자기 매수 거래량 비율 | String | 82 | Y |  |
| `arbt_smtm_ntby_qty_rate` | 차익 합계 순매수 수량 비율 | String | 72 | Y |  |
| `nabt_smtm_ntby_tr_pbmn_rate` | 비차익 합계 순매수 거래대금 비 | String | 72 | Y |  |
| `arbt_smtm_seln_vol_rate` | 차익 합계 매도 거래량 비율 | String | 72 | Y |  |
| `whol_entm_seln_vol_rate` | 전체 위탁 매도 거래량 비율 | String | 82 | Y |  |
| `arbt_onsl_shnu_vol` | 차익 자기 매수2 거래량 | String | 18 | Y |  |
| `nabt_onsl_shnu_tr_pbmn` | 비차익 자기 매수2 거래 대금 | String | 18 | Y |  |
| `whol_smtn_shnu_vol` | 전체 합계 매수2 거래량 | String | 18 | Y |  |
| `arbt_smtn_ntby_tr_pbmn` | 차익 합계 순매수 거래 대금 | String | 18 | Y |  |
| `whol_entm_ntby_qty` | 전체 위탁 순매수 수량 | String | 18 | Y |  |
| `arbt_smtn_seln_tr_pbmn` | 차익 합계 매도 거래 대금 | String | 18 | Y |  |
| `whol_entm_seln_tr_pbmn_rate` | 전체 위탁 매도 거래 대금 비율 | String | 82 | Y |  |
| `arbt_onsl_shnu_vol_rate` | 차익 자기 매수 거래량 비율 | String | 82 | Y |  |
| `nabt_onsl_shnu_tr_pbmn_rate` | 비차익 자기 매수 거래 대금 비 | String | 82 | Y |  |
| `whol_shun_vol_rate` | 전체 매수 거래량 비율 | String | 72 | Y |  |
| `arbt_smtm_ntby_tr_pbmn_rate` | 차익 합계 순매수 거래대금 비율 | String | 72 | Y |  |
| `whol_entm_ntby_qty_rate` | 전체 위탁 순매수 수량 비율 | String | 82 | Y |  |
| `arbt_smtm_seln_tr_pbmn_rate` | 차익 합계 매도 거래대금 비율 | String | 72 | Y |  |
| `whol_onsl_seln_vol` | 전체 자기 매도 거래량 | String | 18 | Y |  |
| `arbt_onsl_shnu_tr_pbmn` | 차익 자기 매수2 거래 대금 | String | 18 | Y |  |
| `nabt_smtn_shnu_vol` | 비차익 합계 매수2 거래량 | String | 18 | Y |  |
| `whol_smtn_shnu_tr_pbmn` | 전체 합계 매수2 거래 대금 | String | 18 | Y |  |
| `nabt_entm_ntby_qty` | 비차익 위탁 순매수 수량 | String | 18 | Y |  |
| `whol_entm_ntby_tr_pbmn` | 전체 위탁 순매수 거래 대금 | String | 18 | Y |  |
| `nabt_entm_seln_vol` | 비차익 위탁 매도 거래량 | String | 18 | Y |  |
| `whol_onsl_seln_vol_rate` | 전체 자기 매도 거래량 비율 | String | 82 | Y |  |
| `arbt_onsl_shnu_tr_pbmn_rate` | 차익 자기 매수 거래 대금 비율 | String | 82 | Y |  |
| `nabt_smtm_shun_vol_rate` | 비차익 합계 매수 거래량 비율 | String | 72 | Y |  |
| `whol_shun_tr_pbmn_rate` | 전체 매수 거래대금 비율 | String | 72 | Y |  |
| `nabt_entm_ntby_qty_rate` | 비차익 위탁 순매수 수량 비율 | String | 82 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240404",
            "arbt_entm_seln_vol": "945",
            "arbt_entm_seln_vol_rate": "0.20",
            "arbt_entm_seln_tr_pbmn": "60184",
            "arbt_entm_seln_tr_pbmn_rate": "0.50",
            "arbt_onsl_seln_tr_pbmn": "116742",
            "arbt_onsl_seln_tr_pbmn_rate": "0.97",
            "arbt_onsl_seln_vol": "1893",
            "arbt_onsl_seln_vol_rate": "0.40",
            "arbt_smtn_seln_vol": "2839",
            "arbt_smtm_seln_vol_rate": "0.59",
            "arbt_smtn_seln_tr_pbmn": "176926",
            "arbt_smtm_seln_tr_pbmn_rate": "1.48",
            "nabt_entm_seln_vol": "72995",
            "nabt_entm_seln_tr_pbmn": "2335987",
            "nabt_entm_seln_vol_rate": "15.27",
            "nabt_entm_seln_tr_pbmn_rate": "19.50",
            "nabt_onsl_seln_vol": "335",
            "nabt_onsl_seln_vol_rate": "0.07",
            "nabt_onsl_seln_tr_pbmn": "18428",
            "nabt_onsl_seln_tr_pbmn_rate": "0.15",
            "nabt_smtn_seln_vol": "73331",
            "nabt_smtm_seln_vol_rate": "15.34",
            "nabt_smtn_seln_tr_pbmn": "2354415",
            "nabt_smtm_seln_tr_pbmn_rate": "19.66",
            "whol_entm_seln_vol": "73940",
            "whol_entm_seln_tr_pbmn": "2396171",
            "whol_entm_seln_vol_rate": "15.47",
            "whol_entm_seln_tr_pbmn_rate": "20.00",
            "whol_onsl_seln_vol": "2229",
            "whol_onsl_seln_vol_rate": "0.47",
            "whol_onsl_seln_tr_pbmn": "135170",
            "whol_onsl_seln_tr_pbmn_rate": "1.13",
            "whol_smtn_seln_vol": "76169",
            "whol_seln_vol_rate": "15.94",
            "whol_smtn_seln_tr_pbmn": "2531340",
            "whol_seln_tr_pbmn_rate": "21.13",
            "arbt_entm_shnu_vol": "798",
            "arbt_entm_shnu_vol_rate": "0.17",
            "arbt_entm_shnu_tr_pbmn": "50818",
            "arbt_entm_shnu_tr_pbmn_rate": "0.42",
            "arbt_onsl_shnu_vol": "247",
            "arbt_onsl_shnu_vol_rate": "0.05",
            "arbt_onsl_shnu_tr_pbmn": "15309",
            "arbt_onsl_shnu_tr_pbmn_rate": "0.13",
            "arbt_smtn_shnu_vol": "1045",
            "arbt_smtm_shun_vol_rate": "0.22",
            "arbt_smtn_shnu_tr_pbmn": "66127",
            "arbt_smtm_shun_tr_pbmn_rate": "0.55",
            "nabt_entm_shnu_vol": "73441",
            "nabt_entm_shnu_vol_rate": "15.37",
            "nabt_entm_shnu_tr_pbmn": "2581806",
            "nabt_entm_shnu_tr_pbmn_rate": "21.55",
            "nabt_onsl_shnu_vol": "250",
            "nabt_onsl_shnu_vol_rate": "0.05",
            "nabt_onsl_shnu_tr_pbmn": "11652",
            "nabt_onsl_shnu_tr_pbmn_rate": "0.10",
            "nabt_smtn_shnu_vol": "73691",
            "nabt_smtm_shun_vol_rate": "15.42",
            "nabt_smtn_shnu_tr_pbmn": "2593458",
            "nabt_smtm_shun_tr_pbmn_rate": "21.65",
            "whol_entm_shnu_vol": "74239",
            "whol_entm_shnu_vol_rate": "15.53",
            "whol_entm_shnu_tr_pbmn": "2632624",
            "whol_entm_shnu_tr_pbmn_rate": "21.98",
            "whol_onsl_shnu_vol": "497",
            "whol_onsl_shnu_tr_pbmn": "26961",
            "whol_onsl_shnu_tr_pbmn_rate": "0.23",
            "whol_onsl_shnu_vol_rate": "0.10",
            "whol_smtn_shnu_vol": "74736",
            "whol_shun_vol_rate": "15.64",
            "whol_smtn_shnu_tr_pbmn": "2659585",
            "whol_shun_tr_pbmn_rate": "22.20",
            "arbt_entm_ntby_qty": "-147",
            "arbt_entm_ntby_qty_rate": "-0.03",
            "arbt_entm_ntby_tr_pbmn": "-9366",
            "arbt_entm_ntby_tr_pbmn_rate": "-0.08",
            "arbt_onsl_ntby_qty": "-1646",
            "arbt_onsl_ntby_qty_rate": "-0.34",
            "arbt_onsl_ntby_tr_pbmn": "-101433",
            "arbt_onsl_ntby_tr_pbmn_rate": "-0.85",
            "arbt_smtn_ntby_qty": "-1793",
            "arbt_smtm_ntby_qty_rate": "-0.38",
            "arbt_smtn_ntby_tr_pbmn": "-110799",
            "arbt_smtm_ntby_tr_pbmn_rate": "-0.93",
            "nabt_entm_ntby_qty": "446",
            "nabt_entm_ntby_qty_rate": "0.09",
            "nabt_entm_ntby_tr_pbmn": "245819",
            "nabt_entm_ntby_tr_pbmn_rate": "2.05",
            "nabt_onsl_ntby_qty": "-85",
            "nabt_onsl_ntby_qty_rate": "-0.02",
            "nabt_onsl_ntby_tr_pbmn": "-6776",
            "nabt_onsl_ntby_tr_pbmn_rate": "-0.06",
            "nabt_smtn_ntby_qty": "361",
            "nabt_smtm_ntby_qty_rate": "0.08",
            "nabt_smtn_ntby_tr_pbmn": "239043",
            "nabt_smtm_ntby_tr_pbmn_rate": "2.00",
            "whol_entm_ntby_qty": "299",
            "whol_entm_ntby_qty_rate": "0.06",
            "whol_entm_ntby_tr_pbmn": "236453",
            "whol_entm_ntby_tr_pbmn_rate": "1.97",
            "whol_onsl_ntby_qty": "-1732",
            "whol_onsl_ntby_qty_rate": "-0.36",
            "whol_onsl_ntby_tr_pbmn": "-108209",
            "whol_onsl_ntby_tr_pbmn_rate": "-0.90",
            "whol_smtn_ntby_qty": "-1433",
            "whol_ntby_qty_rate": "-0.30",
            "whol_smtn_ntby_tr_pbmn": "128245",
            "whol_ntby_tr_pbmn_rate": "1.07",
            "bstp_nmix_prpr": "",
            "bstp_nmix_prdy_vrss": "",
            "prdy_vrss_sign": ""
        },
        {
            "stck_bsop_date": "20240403",
            "arbt_entm_seln_vol": "769",
            "arbt_entm_seln_vol_rate": "0.12",
            "arbt_entm_seln_tr_pbmn": "48480",
            "arbt_entm_seln_tr_pbmn_rate": "0.37",
            "arbt_onsl_seln_tr_pbmn": "192333",
            "arbt_onsl_seln_tr_pbmn_rate": "1.45",
            "arbt_onsl_seln_vol": "3118",
            "arbt_onsl_seln_vol_rate": "0.49",
            "arbt_smtn_seln_vol": "3887",
            "arbt_smtm_seln_vol_rate": "0.61",
            "arbt_smtn_seln_tr_pbmn": "240813",
            "arbt_smtm_seln_tr_pbmn_rate": "1.82",
            "nabt_entm_seln_vol": "94356",
            "nabt_entm_seln_tr_pbmn": "3076931",
            "nabt_entm_seln_vol_rate": "14.72",
            "nabt_entm_seln_tr_pbmn_rate": "23.21",
            "nabt_onsl_seln_vol": "3323",
            "nabt_onsl_seln_vol_rate": "0.52",
            "nabt_onsl_seln_tr_pbmn": "207163",
            "nabt_onsl_seln_tr_pbmn_rate": "1.56",
            "nabt_smtn_seln_vol": "97679",
            "nabt_smtm_seln_vol_rate": "15.24",
            "nabt_smtn_seln_tr_pbmn": "3284094",
            "nabt_smtm_seln_tr_pbmn_rate": "24.77",
            "whol_entm_seln_vol": "95125",
            "whol_entm_seln_tr_pbmn": "3125411",
            "whol_entm_seln_vol_rate": "14.84",
            "whol_entm_seln_tr_pbmn_rate": "23.58",
            "whol_onsl_seln_vol": "6440",
            "whol_onsl_seln_vol_rate": "1.01",
            "whol_onsl_seln_tr_pbmn": "399496",
            "whol_onsl_seln_tr_pbmn_rate": "3.01",
            "whol_smtn_seln_vol": "101566",
            "whol_seln_vol_rate": "15.85",
            "whol_smtn_seln_tr_pbmn": "3524908",
            "whol_seln_tr_pbmn_rate": "26.59",
            "arbt_entm_shnu_vol": "916",
            "arbt_entm_shnu_vol_rate": "0.14",
            "arbt_entm_shnu_tr_pbmn": "57765",
            "arbt_entm_shnu_tr_pbmn_rate": "0.44",
            "arbt_onsl_shnu_vol": "151",
            "arbt_onsl_shnu_vol_rate": "0.02",
            "arbt_onsl_shnu_tr_pbmn": "9682",
            "arbt_onsl_shnu_tr_pbmn_rate": "0.07",
            "arbt_smtn_shnu_vol": "1067",
            "arbt_smtm_shun_vol_rate": "0.17",
            "arbt_smtn_shnu_tr_pbmn": "67446",
            "arbt_smtm_shun_tr_pbmn_rate": "0.51",
            "nabt_entm_shnu_vol": "88098",
            "nabt_entm_shnu_vol_rate": "13.75",
            "nabt_entm_shnu_tr_pbmn": "2576437",
            "nabt_entm_shnu_tr_pbmn_rate": "19.43",
            "nabt_onsl_shnu_vol": "206",
            "nabt_onsl_shnu_vol_rate": "0.03",
            "nabt_onsl_shnu_tr_pbmn": "8168",
            "nabt_onsl_shnu_tr_pbmn_rate": "0.06",
            "nabt_smtn_shnu_vol": "88304",
            "nabt_smtm_shun_vol_rate": "13.78",
            "nabt_smtn_shnu_tr_pbmn": "2584605",
            "nabt_smtm_shun_tr_pbmn_rate": "19.50",
            "whol_entm_shnu_vol": "89014",
            "whol_entm_shnu_vol_rate": "13.89",
            "whol_entm_shnu_tr_pbmn": "2634202",
            "whol_entm_shnu_tr_pbmn_rate": "19.87",
            "whol_onsl_shnu_vol": "357",
            "whol_onsl_shnu_tr_pbmn": "17849",
            "whol_onsl_shnu_tr_pbmn_rate": "0.13",
            "whol_onsl_shnu_vol_rate": "0.06",
            "whol_smtn_shnu_vol": "89371",
            "whol_shun_vol_rate": "13.95",
            "whol_smtn_shnu_tr_pbmn": "2652051",
            "whol_shun_tr_pbmn_rate": "20.00",
            "arbt_entm_ntby_qty": "147",
            "arbt_entm_ntby_qty_rate": "0.02",
            "arbt_entm_ntby_tr_pbmn": "9284",
            "arbt_entm_ntby_tr_pbmn_rate": "0.07",
            "arbt_onsl_ntby_qty": "-2967",
            "arbt_onsl_ntby_qty_rate": "-0.46",
            "arbt_onsl_ntby_tr_pbmn": "-182651",
            "arbt_onsl_ntby_tr_pbmn_rate": "-1.38",
            "arbt_smtn_ntby_qty": "-2819",
            "arbt_smtm_ntby_qty_rate": "-0.44",
            "arbt_smtn_ntby_tr_pbmn": "-173367",
            "arbt_smtm_ntby_tr_pbmn_rate": "-1.31",
            "nabt_entm_ntby_qty": "-6259",
            "nabt_entm_ntby_qty_rate": "-0.98",
            "nabt_entm_ntby_tr_pbmn": "-500494",
            "nabt_entm_ntby_tr_pbmn_rate": "-3.78",
            "nabt_onsl_ntby_qty": "-3116",
            "nabt_onsl_ntby_qty_rate": "-0.49",
            "nabt_onsl_ntby_tr_pbmn": "-198996",
            "nabt_onsl_ntby_tr_pbmn_rate": "-1.50",
            "nabt_smtn_ntby_qty": "-9375",
            "nabt_smtm_ntby_qty_rate": "-1.46",
            "nabt_smtn_ntby_tr_pbmn": "-699489",
            "nabt_smtm_ntby_tr_pbmn_rate": "-5.28",
            "whol_entm_ntby_qty": "-6112",
            "whol_entm_ntby_qty_rate": "-0.95",
            "whol_entm_ntby_tr_pbmn": "-491210",
            "whol_entm_ntby_tr_pbmn_rate": "-3.71",
            "whol_onsl_ntby_qty": "-6083",
            "whol_onsl_ntby_qty_rate": "-0.95",
            "whol_onsl_ntby_tr_pbmn": "-381647",
            "whol_onsl_ntby_tr_pbmn_rate": "-2.88",
            "whol_smtn_ntby_qty": "-12195",
            "whol_ntby_qty_rate": "-1.90",
            "whol_smtn_ntby_tr_pbmn": "-872856",
            "whol_ntby_tr_pbmn_rate": "-6.58",
            "bstp_nmix_prpr": "",
            "bstp_nmix_prdy_vrss": "",
            "prdy_vrss_sign": ""
        },
        {
            "stck_bsop_date": "20240402",
            "arbt_entm_seln_vol": "857",
            "arbt_entm_seln_vol_rate": "0.14",
            "arbt_entm_seln_tr_pbmn": "54673",
            "arbt_entm_seln_tr_pbmn_rate": "0.42",
            "arbt_onsl_seln_tr_pbmn": "78907",
            "arbt_onsl_seln_tr_pbmn_rate": "0.60",
            "arbt_onsl_seln_vol": "1282",
            "arbt_onsl_seln_vol_rate": "0.20",
            "arbt_smtn_seln_vol": "2138",
            "arbt_smtm_seln_vol_rate": "0.34",
            "arbt_smtn_seln_tr_pbmn": "133579",
            "arbt_smtm_seln_tr_pbmn_rate": "1.02",
            "nabt_entm_seln_vol": "78391",
            "nabt_entm_seln_tr_pbmn": "2385531",
            "nabt_entm_seln_vol_rate": "12.44",
            "nabt_entm_seln_tr_pbmn_rate": "18.19",
            "nabt_onsl_seln_vol": "893",
            "nabt_onsl_seln_vol_rate": "0.14",
            "nabt_onsl_seln_tr_pbmn": "54722",
            "nabt_onsl_seln_tr_pbmn_rate": "0.42",
            "nabt_smtn_seln_vol": "79284",
            "nabt_smtm_seln_vol_rate": "12.58",
            "nabt_smtn_seln_tr_pbmn": "2440253",
            "nabt_smtm_seln_tr_pbmn_rate": "18.60",
            "whol_entm_seln_vol": "79247",
            "whol_entm_seln_tr_pbmn": "2440203",
            "whol_entm_seln_vol_rate": "12.57",
            "whol_entm_seln_tr_pbmn_rate": "18.60",
            "whol_onsl_seln_vol": "2175",
            "whol_onsl_seln_vol_rate": "0.35",
            "whol_onsl_seln_tr_pbmn": "133628",
            "whol_onsl_seln_tr_pbmn_rate": "1.02",
            "whol_smtn_seln_vol": "81422",
            "whol_seln_vol_rate": "12.92",
            "whol_smtn_seln_tr_pbmn": "2573832",
            "whol_seln_tr_pbmn_rate": "19.62",
            "arbt_entm_shnu_vol": "760",
            "arbt_entm_shnu_vol_rate": "0.12",
            "arbt_entm_shnu_tr_pbmn": "48775",
            "arbt_entm_shnu_tr_pbmn_rate": "0.37",
            "arbt_onsl_shnu_vol": "3",
            "arbt_onsl_shnu_vol_rate": "0.00",
            "arbt_onsl_shnu_tr_pbmn": "657",
            "arbt_onsl_shnu_tr_pbmn_rate": "0.01",
            "arbt_smtn_shnu_vol": "762",
            "arbt_smtm_shun_vol_rate": "0.12",
            "arbt_smtn_shnu_tr_pbmn": "49432",
            "arbt_smtm_shun_tr_pbmn_rate": "0.38",
            "nabt_entm_shnu_vol": "74157",
            "nabt_entm_shnu_vol_rate": "11.76",
            "nabt_entm_shnu_tr_pbmn": "3086213",
            "nabt_entm_shnu_tr_pbmn_rate": "23.53",
            "nabt_onsl_shnu_vol": "187",
            "nabt_onsl_shnu_vol_rate": "0.03",
            "nabt_onsl_shnu_tr_pbmn": "8119",
            "nabt_onsl_shnu_tr_pbmn_rate": "0.06",
            "nabt_smtn_shnu_vol": "74344",
            "nabt_smtm_shun_vol_rate": "11.79",
            "nabt_smtn_shnu_tr_pbmn": "3094332",
            "nabt_smtm_shun_tr_pbmn_rate": "23.59",
            "whol_entm_shnu_vol": "74916",
            "whol_entm_shnu_vol_rate": "11.88",
            "whol_entm_shnu_tr_pbmn": "3134988",
            "whol_entm_shnu_tr_pbmn_rate": "23.90",
            "whol_onsl_shnu_vol": "190",
            "whol_onsl_shnu_tr_pbmn": "8775",
            "whol_onsl_shnu_tr_pbmn_rate": "0.07",
            "whol_onsl_shnu_vol_rate": "0.03",
            "whol_smtn_shnu_vol": "75107",
            "whol_shun_vol_rate": "11.91",
            "whol_smtn_shnu_tr_pbmn": "3143764",
            "whol_shun_tr_pbmn_rate": "23.97",
            "arbt_entm_ntby_qty": "-97",
            "arbt_entm_ntby_qty_rate": "-0.02",
            "arbt_entm_ntby_tr_pbmn": "-5897",
            "arbt_entm_ntby_tr_pbmn_rate": "-0.04",
            "arbt_onsl_ntby_qty": "-1279",
            "arbt_onsl_ntby_qty_rate": "-0.20",
            "arbt_onsl_ntby_tr_pbmn": "-78250",
            "arbt_onsl_ntby_tr_pbmn_rate": "-0.60",
            "arbt_smtn_ntby_qty": "-1376",
            "arbt_smtm_ntby_qty_rate": "-0.22",
            "arbt_smtn_ntby_tr_pbmn": "-84147",
            "arbt_smtm_ntby_tr_pbmn_rate": "-0.64",
            "nabt_entm_ntby_qty": "-4234",
            "nabt_entm_ntby_qty_rate": "-0.67",
            "nabt_entm_ntby_tr_pbmn": "700682",
            "nabt_entm_ntby_tr_pbmn_rate": "5.34",
            "nabt_onsl_ntby_qty": "-706",
            "nabt_onsl_ntby_qty_rate": "-0.11",
            "nabt_onsl_ntby_tr_pbmn": "-46603",
            "nabt_onsl_ntby_tr_pbmn_rate": "-0.36",
            "nabt_smtn_ntby_qty": "-4940",
            "nabt_smtm_ntby_qty_rate": "-0.78",
            "nabt_smtn_ntby_tr_pbmn": "654079",
            "nabt_smtm_ntby_tr_pbmn_rate": "4.99",
            "whol_entm_ntby_qty": "-4331",
            "whol_entm_ntby_qty_rate": "-0.69",
            "whol_entm_ntby_tr_pbmn": "694785",
            "whol_entm_ntby_tr_pbmn_rate": "5.30",
            "whol_onsl_ntby_qty": "-1985",
            "whol_onsl_ntby_qty_rate": "-0.31",
            "whol_onsl_ntby_tr_pbmn": "-124853",
            "whol_onsl_ntby_tr_pbmn_rate": "-0.95",
            "whol_smtn_ntby_qty": "-6316",
            "whol_ntby_qty_rate": "-1.00",
            "whol_smtn_ntby_tr_pbmn": "569932",
            "whol_ntby_tr_pbmn_rate": "4.35",
            "bstp_nmix_prpr": "",
            "bstp_nmix_prdy_vrss": "",
            "prdy_vrss_sign": ""
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

