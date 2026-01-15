# NAV 비교추이(종목)[v1_국내주식-069]

> [국내주식] 기본시세

NAV 비교추이(종목) API입니다.
한국투자 HTS(eFriend Plus) > [0244] ETF/ETN 비교추이(NAV/IIV) 좌측 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `46eea904-3984-4354-b4e9-8918f503fd79` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/etfetn/v1/quotations/nav-comparison-trend` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHPST02440000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-23
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST02440000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "069500"
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
| `output1` | 응답상세 | String |   | Y |  |
| `stck_prpr` | 주식 현재가 | String | 8 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 8 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 2 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 4 | Y |  |
| `acml_vol` | 누적 거래량 | String | 12 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 60 | Y |  |
| `stck_prdy_clpr` | 주식 전일 종가 | String | 10 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `stck_mxpr` | 주식 상한가 | String | 10 | Y |  |
| `stck_llam` | 주식 하한가 | String | 10 | Y |  |
| `output2` | 응답상세 | String |   | Y |  |
| `nav` | NAV | String | 11 | Y |  |
| `nav_prdy_vrss_sign` | NAV 전일 대비 부호 | String | 1 | Y |  |
| `nav_prdy_vrss` | NAV 전일 대비 | String | 11 | Y |  |
| `nav_prdy_ctrt` | NAV 전일 대비율 | String | 8 | Y |  |
| `prdy_clpr_nav` | NAV전일종가 | String | 11 | Y |  |
| `oprc_nav` | NAV시가 | String | 11 | Y |  |
| `hprc_nav` | NAV고가 | String | 11 | Y |  |
| `lprc_nav` | NAV저가 | String | 11 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "stck_prpr": "36090",
    "prdy_vrss": "110",
    "prdy_vrss_sign": "2",
    "prdy_ctrt": "0.31",
    "acml_vol": "3720111",
    "acml_tr_pbmn": "134826697200",
    "stck_prdy_clpr": "35980",
    "stck_oprc": "36300",
    "stck_hgpr": "36510",
    "stck_lwpr": "36040",
    "stck_mxpr": "46770",
    "stck_llam": "25190"
  },
  "output2": {
    "nav": "36127.30",
    "nav_prdy_vrss_sign": "2",
    "nav_prdy_vrss": "91.08",
    "nav_prdy_ctrt": "0.25",
    "prdy_clpr_nav": "36036.22",
    "oprc_nav": "36065.99",
    "hprc_nav": "36543.62",
    "lprc_nav": "36065.99"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
