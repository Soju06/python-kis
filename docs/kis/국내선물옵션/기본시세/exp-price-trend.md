# 선물옵션 일중예상체결추이[국내선물-018]

> [국내선물옵션] 기본시세

선물옵션 일중예상체결추이 API입니다. 
한국투자 HTS(eFriend Plus) > [0548] 선물옵션 예상체결추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `498e6384-f887-4fb2-9055-2cbc95790087` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/exp-price-trend` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHPIF05110100` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
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
| `tr_id` | 거래ID | String | 13 | Y | FHPIF05110100 |
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
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목번호 (지수선물:6자리, 지수옵션 9자리) |
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | F : 지수선물, O : 지수옵션 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:F
FID_INPUT_ISCD:101V06
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
| `output1` | 응답상세 | String |   | Y |  |
| `hts_kor_isnm` | 영업 시간 | String | 40 | Y |  |
| `futs_antc_cnpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `antc_cntg_vrss_sign` | 업종 지수 전일 대비 | String | 1 | Y |  |
| `futs_antc_cntg_vrss` | 전일 대비 부호 | String | 112 | Y |  |
| `antc_cntg_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `futs_sdpr` | 누적 거래 대금 | String | 112 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `stck_cntg_hour` | 주식체결시간 | String | 6 | Y |  |
| `futs_antc_cnpr` | 선물예상체결가 | String | 112 | Y |  |
| `antc_cntg_vrss_sign` | 예상체결대비부호 | String | 1 | Y |  |
| `futs_antc_cntg_vrss` | 선물예상체결대비 | String | 112 | Y |  |
| `antc_cntg_prdy_ctrt` | 예상체결전일대비율 | String | 82 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "hts_kor_isnm": "F 202406",
    "futs_antc_cnpr": "0.000",
    "antc_cntg_vrss_sign": "0",
    "futs_antc_cntg_vrss": "0.000",
    "antc_cntg_prdy_ctrt": "0.00",
    "futs_sdpr": "376.95"
  },
  "output2": [
    {
      "stck_cntg_hour": "084500",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "380.00",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.05",
      "antc_cntg_prdy_ctrt": "0.81"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "380.00",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.05",
      "antc_cntg_prdy_ctrt": "0.81"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "380.00",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.05",
      "antc_cntg_prdy_ctrt": "0.81"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "380.00",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.05",
      "antc_cntg_prdy_ctrt": "0.81"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.95",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "3.00",
      "antc_cntg_prdy_ctrt": "0.80"
    },
    {
      "stck_cntg_hour": "084459",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.90",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.95",
      "antc_cntg_prdy_ctrt": "0.78"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.80",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.85",
      "antc_cntg_prdy_ctrt": "0.76"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.80",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.85",
      "antc_cntg_prdy_ctrt": "0.76"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.75",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.80",
      "antc_cntg_prdy_ctrt": "0.74"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.75",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.80",
      "antc_cntg_prdy_ctrt": "0.74"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.75",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.80",
      "antc_cntg_prdy_ctrt": "0.74"
    },
    {
      "stck_cntg_hour": "084458",
      "futs_antc_cnpr": "379.75",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.80",
      "antc_cntg_prdy_ctrt": "0.74"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.75",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.80",
      "antc_cntg_prdy_ctrt": "0.74"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.75",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.80",
      "antc_cntg_prdy_ctrt": "0.74"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.75",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.80",
      "antc_cntg_prdy_ctrt": "0.74"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084457",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084456",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084455",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.70",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.75",
      "antc_cntg_prdy_ctrt": "0.73"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.60",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.65",
      "antc_cntg_prdy_ctrt": "0.70"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084454",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084453",
      "futs_antc_cnpr": "379.65",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.70",
      "antc_cntg_prdy_ctrt": "0.72"
    },
    {
      "stck_cntg_hour": "084453",
      "futs_antc_cnpr": "379.60",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.65",
      "antc_cntg_prdy_ctrt": "0.70"
    },
    {
      "stck_cntg_hour": "084453",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084453",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084453",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084453",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    },
    {
      "stck_cntg_hour": "084453",
      "futs_antc_cnpr": "379.55",
      "antc_cntg_vrss_sign": "2",
      "futs_antc_cntg_vrss": "2.60",
      "antc_cntg_prdy_ctrt": "0.69"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
