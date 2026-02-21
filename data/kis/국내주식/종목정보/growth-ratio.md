# 국내주식 성장성비율[v1_국내주식-085]

> [국내주식] 종목정보

국내주식 성장성비율 API입니다.
한국투자 HTS(eFriend Plus) > [0635] 재무분석종합 화면의 하단 '7.성장성비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `e7a0d02d-2aec-4358-8738-65c7c6da3b1b` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/finance/growth-ratio` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKST66430800` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15T09:15:48+09:00
- **최종 수정일**: 2025-05-14T13:19:55+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST66430800 |
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
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | ex : 000660 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0: 년, 1: 분기 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_div_cls_code": "1"
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
| `output` | 응답상세 | Object |   | Y | array |
| `stac_yymm` | 결산 년월 | String | 6 | Y |  |
| `grs` | 매출액 증가율 | String | 124 | Y |  |
| `bsop_prfi_inrt` | 영업 이익 증가율 | String | 124 | Y |  |
| `equt_inrt` | 자기자본 증가율 | String | 92 | Y |  |
| `totl_aset_inrt` | 총자산 증가율 | String | 92 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stac_yymm": "202312",
      "grs": "-14.33",
      "bsop_prfi_inrt": "-84.86",
      "equt_inrt": "2.52",
      "totl_aset_inrt": "1.67"
    },
    {
      "stac_yymm": "202309",
      "grs": "-17.52",
      "bsop_prfi_inrt": "-90.42",
      "equt_inrt": "5.50",
      "totl_aset_inrt": "-3.36"
    },
    {
      "stac_yymm": "202306",
      "grs": "-20.15",
      "bsop_prfi_inrt": "-95.36",
      "equt_inrt": "9.47",
      "totl_aset_inrt": "-0.01"
    },
    {
      "stac_yymm": "202303",
      "grs": "-18.05",
      "bsop_prfi_inrt": "-95.47",
      "equt_inrt": "14.12",
      "totl_aset_inrt": "3.36"
    },
    {
      "stac_yymm": "202212",
      "grs": "8.09",
      "bsop_prfi_inrt": "-15.99",
      "equt_inrt": "16.35",
      "totl_aset_inrt": "5.11"
    },
    {
      "stac_yymm": "202209",
      "grs": "14.15",
      "bsop_prfi_inrt": "3.45",
      "equt_inrt": "16.22",
      "totl_aset_inrt": "14.58"
    },
    {
      "stac_yymm": "202206",
      "grs": "20.09",
      "bsop_prfi_inrt": "28.56",
      "equt_inrt": "16.15",
      "totl_aset_inrt": "16.44"
    },
    {
      "stac_yymm": "202203",
      "grs": "18.95",
      "bsop_prfi_inrt": "50.50",
      "equt_inrt": "14.96",
      "totl_aset_inrt": "11.84"
    },
    {
      "stac_yymm": "202112",
      "grs": "18.07",
      "bsop_prfi_inrt": "43.45",
      "equt_inrt": "10.49",
      "totl_aset_inrt": "12.79"
    },
    {
      "stac_yymm": "202109",
      "grs": "15.85",
      "bsop_prfi_inrt": "40.15",
      "equt_inrt": "7.47",
      "totl_aset_inrt": "9.22"
    },
    {
      "stac_yymm": "202106",
      "grs": "19.18",
      "bsop_prfi_inrt": "50.41",
      "equt_inrt": "4.64",
      "totl_aset_inrt": "7.49"
    },
    {
      "stac_yymm": "202103",
      "grs": "18.19",
      "bsop_prfi_inrt": "45.53",
      "equt_inrt": "2.96",
      "totl_aset_inrt": "9.89"
    },
    {
      "stac_yymm": "202012",
      "grs": "2.78",
      "bsop_prfi_inrt": "29.62",
      "equt_inrt": "4.97",
      "totl_aset_inrt": "7.28"
    },
    {
      "stac_yymm": "202009",
      "grs": "2.78",
      "bsop_prfi_inrt": "30.76",
      "equt_inrt": "4.82",
      "totl_aset_inrt": "6.34"
    },
    {
      "stac_yymm": "202006",
      "grs": "-0.20",
      "bsop_prfi_inrt": "13.74",
      "equt_inrt": "4.68",
      "totl_aset_inrt": "4.38"
    },
    {
      "stac_yymm": "202003",
      "grs": "5.61",
      "bsop_prfi_inrt": "3.43",
      "equt_inrt": "5.20",
      "totl_aset_inrt": "3.59"
    },
    {
      "stac_yymm": "201912",
      "grs": "-5.48",
      "bsop_prfi_inrt": "-52.84",
      "equt_inrt": "6.11",
      "totl_aset_inrt": "3.89"
    },
    {
      "stac_yymm": "201909",
      "grs": "-7.58",
      "bsop_prfi_inrt": "-57.14",
      "equt_inrt": "8.81",
      "totl_aset_inrt": "4.80"
    },
    {
      "stac_yymm": "201906",
      "grs": "-8.85",
      "bsop_prfi_inrt": "-57.95",
      "equt_inrt": "10.56",
      "totl_aset_inrt": "7.61"
    },
    {
      "stac_yymm": "201903",
      "grs": "-13.50",
      "bsop_prfi_inrt": "-60.15",
      "equt_inrt": "13.42",
      "totl_aset_inrt": "10.43"
    },
    {
      "stac_yymm": "201812",
      "grs": "1.75",
      "bsop_prfi_inrt": "9.77",
      "equt_inrt": "15.51",
      "totl_aset_inrt": "12.46"
    },
    {
      "stac_yymm": "201809",
      "grs": "6.28",
      "bsop_prfi_inrt": "24.91",
      "equt_inrt": "14.91",
      "totl_aset_inrt": "13.70"
    },
    {
      "stac_yymm": "201806",
      "grs": "6.72",
      "bsop_prfi_inrt": "27.32",
      "equt_inrt": "16.15",
      "totl_aset_inrt": "14.81"
    },
    {
      "stac_yymm": "201803",
      "grs": "19.82",
      "bsop_prfi_inrt": "58.03",
      "equt_inrt": "17.62",
      "totl_aset_inrt": "18.26"
    },
    {
      "stac_yymm": "201712",
      "grs": "18.68",
      "bsop_prfi_inrt": "83.46",
      "equt_inrt": "11.16",
      "totl_aset_inrt": "15.10"
    },
    {
      "stac_yymm": "201709",
      "grs": "16.87",
      "bsop_prfi_inrt": "92.30",
      "equt_inrt": "17.35",
      "totl_aset_inrt": "21.31"
    },
    {
      "stac_yymm": "201706",
      "grs": "10.75",
      "bsop_prfi_inrt": "61.71",
      "equt_inrt": "10.37",
      "totl_aset_inrt": "13.78"
    },
    {
      "stac_yymm": "201703",
      "grs": "1.54",
      "bsop_prfi_inrt": "48.27",
      "equt_inrt": "6.44",
      "totl_aset_inrt": "9.52"
    },
    {
      "stac_yymm": "201612",
      "grs": "0.60",
      "bsop_prfi_inrt": "10.70",
      "equt_inrt": "7.76",
      "totl_aset_inrt": "8.26"
    },
    {
      "stac_yymm": "201609",
      "grs": "0.81",
      "bsop_prfi_inrt": "-1.24",
      "equt_inrt": "-0.66",
      "totl_aset_inrt": "-0.85"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

