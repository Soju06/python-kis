# 국내주식 매물대/거래비중 [국내주식-196]

> [국내주식] 시세분석

국내주식 매물대/거래비중 API입니다.
한국투자 HTS(eFriend Plus) > [0113] 당일가격대별 매물대 화면의 데이터 중 일부를 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `49cc5311-ae48-44e5-bc5c-7618f1ee61cd` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/pbar-tratio` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHPST01130000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24T10:14:14+09:00
- **최종 수정일**: 2025-05-14T14:39:17+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST01130000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 주식단축종목코드 |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | Uniquekey(20113) |
| `FID_INPUT_HOUR_1` | 입력시간1 | String | 10 | Y | 공백 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_INPUT_ISCD:136480
FID_COND_SCR_DIV_CODE:20113
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
| `output1` | 응답상세 | String |   | Y |  |
| `rprs_mrkt_kor_name` | 대표시장한글명 | String | 40 | Y |  |
| `stck_shrn_iscd` | 주식단축종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `prdy_vol` | 전일거래량 | String | 18 | Y |  |
| `wghn_avrg_stck_prc` | 가중평균주식가격 | String | 192 | Y |  |
| `lstn_stcn` | 상장주수 | String | 18 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `data_rank` | 데이터순위 | String | 10 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `cntg_vol` | 체결거래량 | String | 18 | Y |  |
| `acml_vol_rlim` | 누적거래량비중 | String | 72 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "rprs_mrkt_kor_name": "KOSDAQ",
    "stck_shrn_iscd": "136480",
    "hts_kor_isnm": "하림",
    "stck_prpr": "3240",
    "prdy_vrss_sign": "5",
    "prdy_vrss": "-65",
    "prdy_ctrt": "-1.97",
    "acml_vol": "847563",
    "prdy_vol": "974060",
    "wghn_avrg_stck_prc": "3256.34",
    "lstn_stcn": "106209702"
  },
  "output2": [
    {
      "data_rank": "1",
      "stck_prpr": "3255",
      "cntg_vol": "124515",
      "acml_vol_rlim": "14.69"
    },
    {
      "data_rank": "2",
      "stck_prpr": "3260",
      "cntg_vol": "123909",
      "acml_vol_rlim": "14.62"
    },
    {
      "data_rank": "3",
      "stck_prpr": "3250",
      "cntg_vol": "87983",
      "acml_vol_rlim": "10.38"
    },
    {
      "data_rank": "4",
      "stck_prpr": "3245",
      "cntg_vol": "83496",
      "acml_vol_rlim": "9.85"
    },
    {
      "data_rank": "5",
      "stck_prpr": "3235",
      "cntg_vol": "72101",
      "acml_vol_rlim": "8.51"
    },
    {
      "data_rank": "6",
      "stck_prpr": "3240",
      "cntg_vol": "70712",
      "acml_vol_rlim": "8.34"
    },
    {
      "data_rank": "7",
      "stck_prpr": "3265",
      "cntg_vol": "65838",
      "acml_vol_rlim": "7.77"
    },
    {
      "data_rank": "8",
      "stck_prpr": "3275",
      "cntg_vol": "57283",
      "acml_vol_rlim": "6.76"
    },
    {
      "data_rank": "9",
      "stck_prpr": "3270",
      "cntg_vol": "56295",
      "acml_vol_rlim": "6.64"
    },
    {
      "data_rank": "10",
      "stck_prpr": "3230",
      "cntg_vol": "30998",
      "acml_vol_rlim": "3.66"
    },
    {
      "data_rank": "11",
      "stck_prpr": "3290",
      "cntg_vol": "27419",
      "acml_vol_rlim": "3.24"
    },
    {
      "data_rank": "12",
      "stck_prpr": "3280",
      "cntg_vol": "15080",
      "acml_vol_rlim": "1.78"
    },
    {
      "data_rank": "13",
      "stck_prpr": "3295",
      "cntg_vol": "13623",
      "acml_vol_rlim": "1.61"
    },
    {
      "data_rank": "14",
      "stck_prpr": "3285",
      "cntg_vol": "9580",
      "acml_vol_rlim": "1.13"
    },
    {
      "data_rank": "15",
      "stck_prpr": "3310",
      "cntg_vol": "3646",
      "acml_vol_rlim": "0.43"
    },
    {
      "data_rank": "16",
      "stck_prpr": "3225",
      "cntg_vol": "2199",
      "acml_vol_rlim": "0.26"
    },
    {
      "data_rank": "17",
      "stck_prpr": "3300",
      "cntg_vol": "1898",
      "acml_vol_rlim": "0.22"
    },
    {
      "data_rank": "18",
      "stck_prpr": "3305",
      "cntg_vol": "988",
      "acml_vol_rlim": "0.12"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

