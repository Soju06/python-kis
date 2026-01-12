# 국내옵션전광판_선물[국내선물-023]

> [국내선물옵션] 기본시세

국내옵션전광판_선물 API입니다. 
한국투자 HTS(eFriend Plus) > [0503] 선물옵션 종합시세(Ⅰ) 화면의 "하단" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `8362a35a-e7c2-4944-a4a2-5a716737388c` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/display-board-futures` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHPIF05030200`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPIF05030200 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (F: 선물) |
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20503) |
| `FID_COND_MRKT_CLS_CODE` | 조건 시장 구분 코드 | String | 6 | Y | 공백: KOSPI200 MKI: 미니KOSPI200 WKM: KOSPI200위클리(월) WKI: KOSPI200위클리(목) KQI: KOSDAQ150 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:F
FID_COND_SCR_DIV_CODE:20503
FID_COND_MRKT_CLS_CODE:MKI
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
| `output1` | 응답상세 | Object |   | Y | array |
| `futs_shrn_iscd` | 선물 단축 종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `futs_prpr` | 선물 현재가 | String | 112 | Y |  |
| `futs_prdy_vrss` | 선물 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `futs_prdy_ctrt` | 선물 전일 대비율 | String | 82 | Y |  |
| `hts_thpr` | HTS 이론가 | String | 112 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `futs_askp` | 선물 매도호가 | String | 112 | Y |  |
| `futs_bidp` | 선물 매수호가 | String | 112 | Y |  |
| `hts_otst_stpl_qty` | HTS 미결제 약정 수량 | String | 18 | Y |  |
| `futs_hgpr` | 선물 최고가 | String | 112 | Y |  |
| `futs_lwpr` | 선물 최저가 | String | 112 | Y |  |
| `hts_rmnn_dynu` | HTS 잔존 일수 | String | 5 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `futs_antc_cnpr` | 선물예상체결가 | String | 112 | Y |  |
| `futs_antc_cntg_vrss` | 선물예상체결대비 | String | 112 | Y |  |
| `antc_cntg_vrss_sign` | 예상 체결 대비 부호 | String | 1 | Y |  |
| `antc_cntg_prdy_ctrt` | 예상 체결 전일 대비율 | String | 82 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "futs_shrn_iscd": "105V05",
      "hts_kor_isnm": "미니F 202405",
      "futs_prpr": "368.28",
      "futs_prdy_vrss": "-3.32",
      "prdy_vrss_sign": "5",
      "futs_prdy_ctrt": "-0.89",
      "hts_thpr": "368.26",
      "acml_vol": "91624",
      "futs_askp": "368.28",
      "futs_bidp": "368.26",
      "hts_otst_stpl_qty": "38188",
      "futs_hgpr": "372.86",
      "futs_lwpr": "367.40",
      "hts_rmnn_dynu": "28",
      "total_askp_rsqn": "934",
      "total_bidp_rsqn": "282",
      "futs_antc_cnpr": "0.00",
      "futs_antc_cntg_vrss": "0.00",
      "antc_cntg_vrss_sign": "0",
      "antc_cntg_prdy_ctrt": "0.00"
    },
    {
      "futs_shrn_iscd": "105V06",
      "hts_kor_isnm": "미니F 202406",
      "futs_prpr": "369.48",
      "futs_prdy_vrss": "-3.32",
      "prdy_vrss_sign": "5",
      "futs_prdy_ctrt": "-0.89",
      "hts_thpr": "369.51",
      "acml_vol": "621",
      "futs_askp": "369.54",
      "futs_bidp": "369.48",
      "hts_otst_stpl_qty": "3433",
      "futs_hgpr": "374.16",
      "futs_lwpr": "368.64",
      "hts_rmnn_dynu": "63",
      "total_askp_rsqn": "68",
      "total_bidp_rsqn": "53",
      "futs_antc_cnpr": "0.00",
      "futs_antc_cntg_vrss": "0.00",
      "antc_cntg_vrss_sign": "0",
      "antc_cntg_prdy_ctrt": "0.00"
    },
    {
      "futs_shrn_iscd": "105V07",
      "hts_kor_isnm": "미니F 202407",
      "futs_prpr": "369.00",
      "futs_prdy_vrss": "-3.98",
      "prdy_vrss_sign": "5",
      "futs_prdy_ctrt": "-1.07",
      "hts_thpr": "369.43",
      "acml_vol": "19",
      "futs_askp": "370.24",
      "futs_bidp": "367.52",
      "hts_otst_stpl_qty": "31",
      "futs_hgpr": "372.00",
      "futs_lwpr": "369.00",
      "hts_rmnn_dynu": "91",
      "total_askp_rsqn": "257",
      "total_bidp_rsqn": "13",
      "futs_antc_cnpr": "0.00",
      "futs_antc_cntg_vrss": "0.00",
      "antc_cntg_vrss_sign": "0",
      "antc_cntg_prdy_ctrt": "0.00"
    },
    {
      "futs_shrn_iscd": "105V08",
      "hts_kor_isnm": "미니F 202408",
      "futs_prpr": "373.78",
      "futs_prdy_vrss": "0.00",
      "prdy_vrss_sign": "3",
      "futs_prdy_ctrt": "0.00",
      "hts_thpr": "370.41",
      "acml_vol": "0",
      "futs_askp": "403.58",
      "futs_bidp": "344.00",
      "hts_otst_stpl_qty": "1",
      "futs_hgpr": "0.00",
      "futs_lwpr": "0.00",
      "hts_rmnn_dynu": "119",
      "total_askp_rsqn": "4",
      "total_bidp_rsqn": "5",
      "futs_antc_cnpr": "0.00",
      "futs_antc_cntg_vrss": "0.00",
      "antc_cntg_vrss_sign": "0",
      "antc_cntg_prdy_ctrt": "0.00"
    },
    {
      "futs_shrn_iscd": "105V09",
      "hts_kor_isnm": "미니F 202409",
      "futs_prpr": "374.00",
      "futs_prdy_vrss": "-0.50",
      "prdy_vrss_sign": "5",
      "futs_prdy_ctrt": "-0.13",
      "hts_thpr": "371.67",
      "acml_vol": "3",
      "futs_askp": "404.36",
      "futs_bidp": "369.82",
      "hts_otst_stpl_qty": "10",
      "futs_hgpr": "374.00",
      "futs_lwpr": "371.00",
      "hts_rmnn_dynu": "154",
      "total_askp_rsqn": "4",
      "total_bidp_rsqn": "12",
      "futs_antc_cnpr": "0.00",
      "futs_antc_cntg_vrss": "0.00",
      "antc_cntg_vrss_sign": "0",
      "antc_cntg_prdy_ctrt": "0.00"
    },
    {
      "futs_shrn_iscd": "105V10",
      "hts_kor_isnm": "미니F 202410",
      "futs_prpr": "375.26",
      "futs_prdy_vrss": "0.00",
      "prdy_vrss_sign": "3",
      "futs_prdy_ctrt": "0.00",
      "hts_thpr": "371.72",
      "acml_vol": "0",
      "futs_askp": "405.18",
      "futs_bidp": "345.34",
      "hts_otst_stpl_qty": "0",
      "futs_hgpr": "0.00",
      "futs_lwpr": "0.00",
      "hts_rmnn_dynu": "182",
      "total_askp_rsqn": "4",
      "total_bidp_rsqn": "4",
      "futs_antc_cnpr": "0.00",
      "futs_antc_cntg_vrss": "0.00",
      "antc_cntg_vrss_sign": "0",
      "antc_cntg_prdy_ctrt": "0.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
