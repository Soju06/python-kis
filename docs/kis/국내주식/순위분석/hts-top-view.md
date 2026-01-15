# HTS조회상위20종목 [국내주식-214]

> [국내주식] 순위분석

HTS조회상위20종목 API입니다. 
한국투자 HTS(eFriend Plus) > [0158] 조회종목상위 화면의 "종목명", "종목코드" 표시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `636e216a-f3bb-4dc6-8bc3-e6d9babca5f1` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/hts-top-view` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `HHMCM000100C0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-11-08
- **최종 수정일**: 2025-06-24

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHMCM000100C0 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### 요청 예시

```json
없음
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
| `mrkt_div_cls_code` | 시장구분 | String | 9 | Y | J : 코스피, Q : 코스닥 |
| `mksc_shrn_iscd` | 종목코드 | String | 2 | Y | 종목코드 |

### 응답 예시

```json
{
  "output1": [
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "005930"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "233740"
    },
    {
      "mrkt_div_cls_code": "Q",
      "mksc_shrn_iscd": "458650"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "042660"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "251340"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "000660"
    },
    {
      "mrkt_div_cls_code": "Q",
      "mksc_shrn_iscd": "196170"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "475560"
    },
    {
      "mrkt_div_cls_code": "Q",
      "mksc_shrn_iscd": "163280"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "001470"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "272210"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "017860"
    },
    {
      "mrkt_div_cls_code": "Q",
      "mksc_shrn_iscd": "475960"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "000100"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "035420"
    },
    {
      "mrkt_div_cls_code": "Q",
      "mksc_shrn_iscd": "460930"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "066970"
    },
    {
      "mrkt_div_cls_code": "Q",
      "mksc_shrn_iscd": "378800"
    },
    {
      "mrkt_div_cls_code": "J",
      "mksc_shrn_iscd": "373220"
    },
    {
      "mrkt_div_cls_code": "Q",
      "mksc_shrn_iscd": "255220"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
