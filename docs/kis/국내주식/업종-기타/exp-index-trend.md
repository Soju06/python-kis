# 국내주식 예상체결지수 추이[국내주식-121]

> [국내주식] 업종/기타

국내주식 예상체결지수 추이 API입니다. 
한국투자 HTS(eFriend Plus) > [0184] 예상체결지수 추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `020c2367-4e2c-4e9a-85b4-c5daaa73f600` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/exp-index-trend` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `FHPST01840000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01840000 |
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
| `FID_MKOP_CLS_CODE` | 장운영 구분 코드 | String | 2 | Y | 1: 장시작전, 2: 장마감 |
| `FID_INPUT_HOUR_1` | 입력 시간1 | String | 10 | Y | 10(10초), 30(30초), 60(1분), 600(10분) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001: KRX100 |
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 U) |

### 요청 예시

```json
fid_cond_mrkt_div_code:U
fid_input_iscd:0001
fid_input_hour_1:
fid_mkop_cls_code:1
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
| `output` | 응답상세 | Object |   | Y | array |
| `stck_cntg_hour` | 주식 단축 종목코드 | String | 6 | Y |  |
| `bstp_nmix_prpr` | HTS 한글 종목명 | String | 112 | Y |  |
| `prdy_vrss_sign` | 주식 현재가 | String | 1 | Y |  |
| `bstp_nmix_prdy_vrss` | 전일 대비 | String | 112 | Y |  |
| `prdy_ctrt` | 전일 대비 부호 | String | 82 | Y |  |
| `acml_vol` | 전일 대비율 | String | 18 | Y |  |
| `acml_tr_pbmn` | 기준가 대비 현재가 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_cntg_hour": "666666",
      "bstp_nmix_prpr": "2765.30",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "18.67",
      "prdy_ctrt": "0.68",
      "acml_vol": "5951",
      "acml_tr_pbmn": "130953"
    },
    {
      "stck_cntg_hour": "085950",
      "bstp_nmix_prpr": "2766.50",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "19.87",
      "prdy_ctrt": "0.72",
      "acml_vol": "5641",
      "acml_tr_pbmn": "122873"
    },
    {
      "stck_cntg_hour": "085940",
      "bstp_nmix_prpr": "2768.19",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "21.56",
      "prdy_ctrt": "0.78",
      "acml_vol": "5369",
      "acml_tr_pbmn": "115013"
    },
    {
      "stck_cntg_hour": "085930",
      "bstp_nmix_prpr": "2766.70",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.07",
      "prdy_ctrt": "0.73",
      "acml_vol": "5168",
      "acml_tr_pbmn": "107488"
    },
    {
      "stck_cntg_hour": "085920",
      "bstp_nmix_prpr": "2767.01",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.38",
      "prdy_ctrt": "0.74",
      "acml_vol": "5052",
      "acml_tr_pbmn": "103832"
    },
    {
      "stck_cntg_hour": "085910",
      "bstp_nmix_prpr": "2767.09",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.46",
      "prdy_ctrt": "0.74",
      "acml_vol": "4919",
      "acml_tr_pbmn": "101950"
    },
    {
      "stck_cntg_hour": "085900",
      "bstp_nmix_prpr": "2766.91",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.28",
      "prdy_ctrt": "0.74",
      "acml_vol": "4840",
      "acml_tr_pbmn": "99526"
    },
    {
      "stck_cntg_hour": "085850",
      "bstp_nmix_prpr": "2767.06",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.43",
      "prdy_ctrt": "0.74",
      "acml_vol": "4740",
      "acml_tr_pbmn": "93391"
    },
    {
      "stck_cntg_hour": "085840",
      "bstp_nmix_prpr": "2767.12",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.49",
      "prdy_ctrt": "0.75",
      "acml_vol": "4655",
      "acml_tr_pbmn": "92533"
    },
    {
      "stck_cntg_hour": "085830",
      "bstp_nmix_prpr": "2767.27",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.64",
      "prdy_ctrt": "0.75",
      "acml_vol": "4639",
      "acml_tr_pbmn": "91639"
    },
    {
      "stck_cntg_hour": "085820",
      "bstp_nmix_prpr": "2767.35",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.72",
      "prdy_ctrt": "0.75",
      "acml_vol": "4560",
      "acml_tr_pbmn": "90798"
    },
    {
      "stck_cntg_hour": "085810",
      "bstp_nmix_prpr": "2767.22",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.59",
      "prdy_ctrt": "0.75",
      "acml_vol": "4541",
      "acml_tr_pbmn": "93370"
    },
    {
      "stck_cntg_hour": "085800",
      "bstp_nmix_prpr": "2767.08",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.45",
      "prdy_ctrt": "0.74",
      "acml_vol": "4487",
      "acml_tr_pbmn": "91617"
    },
    {
      "stck_cntg_hour": "085750",
      "bstp_nmix_prpr": "2766.75",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.12",
      "prdy_ctrt": "0.73",
      "acml_vol": "4440",
      "acml_tr_pbmn": "90268"
    },
    {
      "stck_cntg_hour": "085740",
      "bstp_nmix_prpr": "2766.96",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.33",
      "prdy_ctrt": "0.74",
      "acml_vol": "4483",
      "acml_tr_pbmn": "90078"
    },
    {
      "stck_cntg_hour": "085730",
      "bstp_nmix_prpr": "2766.93",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.30",
      "prdy_ctrt": "0.74",
      "acml_vol": "4427",
      "acml_tr_pbmn": "89631"
    },
    {
      "stck_cntg_hour": "085720",
      "bstp_nmix_prpr": "2766.96",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.33",
      "prdy_ctrt": "0.74",
      "acml_vol": "4402",
      "acml_tr_pbmn": "89052"
    },
    {
      "stck_cntg_hour": "085710",
      "bstp_nmix_prpr": "2767.00",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.37",
      "prdy_ctrt": "0.74",
      "acml_vol": "4525",
      "acml_tr_pbmn": "87706"
    },
    {
      "stck_cntg_hour": "085700",
      "bstp_nmix_prpr": "2767.08",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.45",
      "prdy_ctrt": "0.74",
      "acml_vol": "4660",
      "acml_tr_pbmn": "84754"
    },
    {
      "stck_cntg_hour": "085650",
      "bstp_nmix_prpr": "2767.40",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.77",
      "prdy_ctrt": "0.76",
      "acml_vol": "4636",
      "acml_tr_pbmn": "84339"
    },
    {
      "stck_cntg_hour": "085640",
      "bstp_nmix_prpr": "2767.30",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.67",
      "prdy_ctrt": "0.75",
      "acml_vol": "4569",
      "acml_tr_pbmn": "84041"
    },
    {
      "stck_cntg_hour": "085630",
      "bstp_nmix_prpr": "2767.37",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.74",
      "prdy_ctrt": "0.76",
      "acml_vol": "4559",
      "acml_tr_pbmn": "83314"
    },
    {
      "stck_cntg_hour": "085620",
      "bstp_nmix_prpr": "2767.43",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.80",
      "prdy_ctrt": "0.76",
      "acml_vol": "4490",
      "acml_tr_pbmn": "83074"
    },
    {
      "stck_cntg_hour": "085610",
      "bstp_nmix_prpr": "2767.74",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "21.11",
      "prdy_ctrt": "0.77",
      "acml_vol": "4436",
      "acml_tr_pbmn": "80274"
    },
    {
      "stck_cntg_hour": "085600",
      "bstp_nmix_prpr": "2766.95",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.32",
      "prdy_ctrt": "0.74",
      "acml_vol": "4032",
      "acml_tr_pbmn": "78386"
    },
    {
      "stck_cntg_hour": "085550",
      "bstp_nmix_prpr": "2766.86",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.23",
      "prdy_ctrt": "0.74",
      "acml_vol": "4026",
      "acml_tr_pbmn": "77796"
    },
    {
      "stck_cntg_hour": "085540",
      "bstp_nmix_prpr": "2766.90",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.27",
      "prdy_ctrt": "0.74",
      "acml_vol": "3946",
      "acml_tr_pbmn": "76794"
    },
    {
      "stck_cntg_hour": "085530",
      "bstp_nmix_prpr": "2767.15",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.52",
      "prdy_ctrt": "0.75",
      "acml_vol": "3932",
      "acml_tr_pbmn": "76859"
    },
    {
      "stck_cntg_hour": "085520",
      "bstp_nmix_prpr": "2766.95",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "20.32",
      "prdy_ctrt": "0.74",
      "acml_vol": "3922",
      "acml_tr_pbmn": "75766"
    },
    {
      "stck_cntg_hour": "085510",
      "bstp_nmix_prpr": "2766.37",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_vrss": "19.74",
      "prdy_ctrt": "0.72",
      "acml_vol": "4008",
      "acml_tr_pbmn": "75458"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
