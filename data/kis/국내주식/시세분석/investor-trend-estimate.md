# 종목별 외인기관 추정가집계[v1_국내주식-046]

> [국내주식] 시세분석

국내주식 종목별 외국인, 기관 추정가집계 API입니다.

한국투자 MTS > 국내 현재가 > 투자자 > 투자자동향 탭 > 왼쪽구분을 '추정(주)'로 선택 시 확인 가능한 데이터를 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

증권사 직원이 장중에 집계/입력한 자료를 단순 누계한 수치로서,
입력시간은 외국인 09:30, 11:20, 13:20, 14:30 / 기관종합 10:00, 11:20, 13:20, 14:30 이며, 사정에 따라 변동될 수 있습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `7fcf90d5-5e84-484a-8000-9121fb0a81d7` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/investor-trend-estimate` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHPTJ04160200` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-04-14T07:28:15+09:00
- **최종 수정일**: 2025-05-14T14:29:37+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHPTJ04160200 |
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
| `MKSC_SHRN_ISCD` | 종목코드 | String | 12 | Y | 종목코드 |

### 요청 예시

```json
{
  "MKSC_SHRN_ISCD": "000660"
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
| `output2` | 응답상세 | Object |   | Y | Array |
| `bsop_hour_gb` | 입력구분 | String | 1 | Y | 1: 09시 30분 입력 2: 10시 00분 입력  3: 11시 20분 입력  4: 13시 20분 입력  5: 14시 30분 입력 |
| `frgn_fake_ntby_qty` | 외국인수량(가집계) | String | 18 | Y |  |
| `orgn_fake_ntby_qty` | 기관수량(가집계) | String | 18 | Y |  |
| `sum_fake_ntby_qty` | 합산수량(가집계) | String | 18 | Y |  |

### 응답 예시

```json
{
  "output2": [
    {
      "bsop_hour_gb": "5",
      "frgn_fake_ntby_qty": "-00000000000030000",
      "orgn_fake_ntby_qty": "000000000000121000",
      "sum_fake_ntby_qty": "000000000000091000"
    },
    {
      "bsop_hour_gb": "4",
      "frgn_fake_ntby_qty": "-00000000000093000",
      "orgn_fake_ntby_qty": "000000000000130000",
      "sum_fake_ntby_qty": "000000000000037000"
    },
    {
      "bsop_hour_gb": "3",
      "frgn_fake_ntby_qty": "-00000000000026000",
      "orgn_fake_ntby_qty": "000000000000037000",
      "sum_fake_ntby_qty": "000000000000011000"
    },
    {
      "bsop_hour_gb": "2",
      "frgn_fake_ntby_qty": "-00000000000038000",
      "orgn_fake_ntby_qty": "000000000000022000",
      "sum_fake_ntby_qty": "-00000000000016000"
    },
    {
      "bsop_hour_gb": "1",
      "frgn_fake_ntby_qty": "-00000000000023000",
      "orgn_fake_ntby_qty": "000000000000000000",
      "sum_fake_ntby_qty": "-00000000000023000"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

