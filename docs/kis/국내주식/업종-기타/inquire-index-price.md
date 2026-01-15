# 국내업종 현재지수[v1_국내주식-063]

> [국내주식] 업종/기타

국내업종 현재지수 API입니다.
한국투자 HTS(eFriend Plus) > [0210] 업종 현재지수 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `868b0fe2-fdb5-4a32-bdb2-00db12269230` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-index-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHPUP02100000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-16
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPUP02100000 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | 업종(U) |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조) |

### 요청 예시

```json
{
"fid_cond_mrkt_div_code":"U"
"fid_input_iscd":"1001"
}
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
| `output` | 응답상세1 | String |   | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `prdy_tr_pbmn` | 전일 거래 대금 | String | 18 | Y |  |
| `bstp_nmix_oprc` | 업종 지수 시가2 | String | 112 | Y |  |
| `prdy_nmix_vrss_nmix_oprc` | 전일 지수 대비 지수 시가2 | String | 112 | Y |  |
| `oprc_vrss_prpr_sign` | 시가2 대비 현재가 부호 | String | 1 | Y |  |
| `bstp_nmix_oprc_prdy_ctrt` | 업종 지수 시가2 전일 대비율 | String | 82 | Y |  |
| `bstp_nmix_hgpr` | 업종 지수 최고가 | String | 112 | Y |  |
| `prdy_nmix_vrss_nmix_hgpr` | 전일 지수 대비 지수 최고가 | String | 112 | Y |  |
| `hgpr_vrss_prpr_sign` | 최고가 대비 현재가 부호 | String | 1 | Y |  |
| `bstp_nmix_hgpr_prdy_ctrt` | 업종 지수 최고가 전일 대비율 | String | 82 | Y |  |
| `bstp_nmix_lwpr` | 업종 지수 최저가 | String | 112 | Y |  |
| `prdy_clpr_vrss_lwpr` | 전일 종가 대비 최저가 | String | 10 | Y |  |
| `lwpr_vrss_prpr_sign` | 최저가 대비 현재가 부호 | String | 1 | Y |  |
| `prdy_clpr_vrss_lwpr_rate` | 전일 종가 대비 최저가 비율 | String | 84 | Y |  |
| `ascn_issu_cnt` | 상승 종목 수 | String | 7 | Y |  |
| `uplm_issu_cnt` | 상한 종목 수 | String | 7 | Y |  |
| `stnr_issu_cnt` | 보합 종목 수 | String | 7 | Y |  |
| `down_issu_cnt` | 하락 종목 수 | String | 7 | Y |  |
| `lslm_issu_cnt` | 하한 종목 수 | String | 7 | Y |  |
| `dryy_bstp_nmix_hgpr` | 연중업종지수최고가 | String | 112 | Y |  |
| `dryy_hgpr_vrss_prpr_rate` | 연중 최고가 대비 현재가 비율 | String | 84 | Y |  |
| `dryy_bstp_nmix_hgpr_date` | 연중업종지수최고가일자 | String | 8 | Y |  |
| `dryy_bstp_nmix_lwpr` | 연중업종지수최저가 | String | 112 | Y |  |
| `dryy_lwpr_vrss_prpr_rate` | 연중 최저가 대비 현재가 비율 | String | 84 | Y |  |
| `dryy_bstp_nmix_lwpr_date` | 연중업종지수최저가일자 | String | 8 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `seln_rsqn_rate` | 매도 잔량 비율 | String | 84 | Y |  |
| `shnu_rsqn_rate` | 매수2 잔량 비율 | String | 84 | Y |  |
| `ntby_rsqn` | 순매수 잔량 | String | 12 | Y |  |

### 응답 예시

```json
{
  "output": {
    "bstp_nmix_prpr": "857.60",
    "bstp_nmix_prdy_vrss": "-1.61",
    "prdy_vrss_sign": "5",
    "bstp_nmix_prdy_ctrt": "-0.19",
    "acml_vol": "1312496",
    "prdy_vol": "1222188",
    "acml_tr_pbmn": "11507962",
    "prdy_tr_pbmn": "11203385",
    "bstp_nmix_oprc": "863.69",
    "prdy_nmix_vrss_nmix_oprc": "4.48",
    "oprc_vrss_prpr_sign": "2",
    "bstp_nmix_oprc_prdy_ctrt": "0.52",
    "bstp_nmix_hgpr": "864.24",
    "prdy_nmix_vrss_nmix_hgpr": "5.03",
    "hgpr_vrss_prpr_sign": "2",
    "bstp_nmix_hgpr_prdy_ctrt": "0.59",
    "bstp_nmix_lwpr": "854.72",
    "prdy_clpr_vrss_lwpr": "-4.49",
    "lwpr_vrss_prpr_sign": "5",
    "prdy_clpr_vrss_lwpr_rate": "-0.52",
    "ascn_issu_cnt": "828",
    "uplm_issu_cnt": "5",
    "stnr_issu_cnt": "94",
    "down_issu_cnt": "716",
    "lslm_issu_cnt": "1",
    "dryy_bstp_nmix_hgpr": "890.06",
    "dryy_hgpr_vrss_prpr_rate": "3.65",
    "dryy_bstp_nmix_hgpr_date": "20240109",
    "dryy_bstp_nmix_lwpr": "786.28",
    "dryy_lwpr_vrss_prpr_rate": "-9.07",
    "dryy_bstp_nmix_lwpr_date": "20240201",
    "total_askp_rsqn": "24146999",
    "total_bidp_rsqn": "40450437",
    "seln_rsqn_rate": "37.38",
    "shnu_rsqn_rate": "62.62",
    "ntby_rsqn": "16303438"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
