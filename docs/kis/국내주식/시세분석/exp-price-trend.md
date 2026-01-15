# 국내주식 예상체결가 추이[국내주식-118]

> [국내주식] 시세분석

국내주식 예상체결가 추이 API입니다.
한국투자 HTS(eFriend Plus) > [0184] 예상체결지수 추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `c4d31a39-d602-4848-9c00-1d9d3f494e63` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/exp-price-trend` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01810000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01810000 |
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
| `fid_mkop_cls_code` | 장운영 구분 코드 | String | 12 | Y | 0:전체, 4:체결량 0 제외 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |
| `fid_input_iscd` | 입력 종목코드 | String | 5 | Y | 종목코드(ex. 005930) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_mkop_cls_code": "0"
}
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
| `rprs_mrkt_kor_name` | 대표 시장 한글 명 | String | 40 | Y |  |
| `antc_cnpr` | 예상 체결가 | String | 10 | Y |  |
| `antc_cntg_vrss_sign` | 예상 체결 대비 부호 | String | 1 | Y |  |
| `antc_cntg_vrss` | 예상 체결 대비 | String | 10 | Y |  |
| `antc_cntg_prdy_ctrt` | 예상 체결 전일 대비율 | String | 82 | Y |  |
| `antc_vol` | 예상 거래량 | String | 18 | Y |  |
| `antc_tr_pbmn` | 예상 거래대금 | String | 19 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "rprs_mrkt_kor_name": "KOSPI200",
    "antc_cnpr": "72600",
    "antc_cntg_vrss_sign": "2",
    "antc_cntg_vrss": "300",
    "antc_cntg_prdy_ctrt": "0.41",
    "antc_vol": "420303",
    "antc_tr_pbmn": "30513997800"
  },
  "output2": [
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090023",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "420303"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090023",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "420196"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090023",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "420206"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090023",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "419330"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090022",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "419131"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090022",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418134"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090022",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418123"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090021",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418123"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090020",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418123"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090019",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418123"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090019",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418120"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090018",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418120"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090017",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418120"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090017",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418121"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090016",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418121"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090016",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "418003"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090016",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "417953"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090016",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "417729"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090016",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "417679"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090015",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "417679"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090015",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "417060"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090015",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "417050"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090015",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "416945"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090015",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "416921"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090015",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "416915"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090014",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "416915"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090014",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "416770"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090014",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "416759"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090014",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "415059"
    },
    {
      "stck_bsop_date": "20240318",
      "stck_cntg_hour": "090013",
      "stck_prpr": "72600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "300",
      "prdy_ctrt": "0.41",
      "acml_vol": "414942"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

