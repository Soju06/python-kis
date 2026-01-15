# 선물옵션 시세호가[v1_국내선물-007]

> [국내선물옵션] 기본시세

선물옵션 시세호가 API입니다.

[국내선물-007 v1] 선물옵션 시세호가

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `bec98736-8f5a-49a0-b325-5f6c40ff13b3` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/inquire-asking-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `FHMIF10010000` |
| **TR ID (모의)** | `FHMIF10010000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전/모의투자] FHMIF10010000 : 선물 옵션 시세 호가 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인 P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션 CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 종목코드 (예: 101S03) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "F",
  "fid_input_iscd": "101S06"
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | Y | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공 0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output1` | 응답상세1 | String |  | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y | 종목명 |
| `futs_prpr` | 선물 현재가 | String | 14 | Y | 선물의 현재가격 |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y | 1 : 상한  2 : 상승 3 : 보합 4 : 하한 5 : 하락 |
| `futs_prdy_vrss` | 선물 전일 대비 | String | 14 | Y | 선물의 전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가) |
| `futs_prdy_ctrt` | 선물 전일 대비율 | String | 11 | Y | 선물 전일 대비 / 당일 현재가 * 100 |
| `acml_vol` | 누적 거래량 | String | 18 | Y | 당일 조회시점까지 전체 거래량 |
| `futs_prdy_clpr` | 선물 전일 종가 | String | 14 | Y | 해당 선물 종목의 전일 종가 |
| `futs_shrn_iscd` | 선물 단축 종목코드 | String | 9 | Y |  |
| `output2` | 응답상세2 | Object |  | Y | Array |
| `futs_askp1` | 선물 매도호가1 | String | 14 | Y | 해당 종목의 매도호가 중 1번째 낮은 호가 |
| `futs_askp2` | 선물 매도호가2 | String | 14 | Y | 해당 종목의 매도호가 중 2번째 낮은 호가 |
| `futs_askp3` | 선물 매도호가3 | String | 14 | Y | 해당 종목의 매도호가 중 3번째 낮은 호가 |
| `futs_askp4` | 선물 매도호가4 | String | 14 | Y | 해당 종목의 매도호가 중 4번째 낮은 호가 |
| `futs_askp5` | 선물 매도호가5 | String | 14 | Y | 해당 종목의 매도호가 중 5번째 낮은 호가 |
| `futs_bidp1` | 선물 매수호가1 | String | 14 | Y | 해당 종목의 매수호가 중 가장 높은 호가 |
| `futs_bidp2` | 선물 매수호가1 | String | 14 | Y | 해당 종목의 매수호가 중 2번째 높은 호가 |
| `futs_bidp3` | 선물 매수호가3 | String | 14 | Y | 해당 종목의 매수호가 중 3번째 높은 호가 |
| `futs_bidp4` | 선물 매수호가4 | String | 14 | Y | 해당 종목의 매수호가 중 4번째 높은 호가 |
| `futs_bidp5` | 선물 매수호가5 | String | 14 | Y | 해당 종목의 매수호가 중 5번째 높은 호가 |
| `askp_rsqn1` | 매도호가 잔량1 | String | 12 | Y | 매도호가 1의 미체결수량 |
| `askp_rsqn2` | 매도호가 잔량2 | String | 12 | Y | 매도호가 2의 미체결수량 |
| `askp_rsqn3` | 매도호가 잔량3 | String | 12 | Y | 매도호가 3의 미체결수량 |
| `askp_rsqn4` | 매도호가 잔량4 | String | 12 | Y | 매도호가 4의 미체결수량 |
| `askp_rsqn5` | 매도호가 잔량5 | String | 12 | Y | 매도호가 5의 미체결수량 |
| `bidp_rsqn1` | 매수호가 잔량1 | String | 12 | Y | 매수호가 1의 미체결수량 |
| `bidp_rsqn2` | 매수호가 잔량2 | String | 12 | Y | 매수호가 2의 미체결수량 |
| `bidp_rsqn3` | 매수호가 잔량3 | String | 12 | Y | 매수호가 3의 미체결수량 |
| `bidp_rsqn4` | 매수호가 잔량4 | String | 12 | Y | 매수호가 4의 미체결수량 |
| `bidp_rsqn5` | 매수호가 잔량5 | String | 12 | Y | 매수호가 5의 미체결수량 |
| `askp_csnu1` | 매도호가 건수1 | String | 10 | Y | 매도호가 1의 미체결 주문 건수 |
| `askp_csnu2` | 매도호가 건수2 | String | 10 | Y | 매도호가 2의 미체결 주문 건수 |
| `askp_csnu3` | 매도호가 건수3 | String | 10 | Y | 매도호가 3의 미체결 주문 건수 |
| `askp_csnu4` | 매도호가 건수4 | String | 10 | Y | 매도호가 4의 미체결 주문 건수 |
| `askp_csnu5` | 매도호가 건수5 | String | 10 | Y | 매도호가 5의 미체결 주문 건수 |
| `bidp_csnu1` | 매수호가 건수1 | String | 10 | Y | 매수호가 1의 미체결 주문 건수 |
| `bidp_csnu2` | 매수호가 건수2 | String | 10 | Y | 매수호가 2의 미체결 주문 건수 |
| `bidp_csnu3` | 매수호가 건수3 | String | 10 | Y | 매수호가 3의 미체결 주문 건수 |
| `bidp_csnu4` | 매수호가 건수4 | String | 10 | Y | 매수호가 4의 미체결 주문 건수 |
| `bidp_csnu5` | 매수호가 건수5 | String | 10 | Y | 매수호가 5의 미체결 주문 건수 |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y | 매도호가 1~5의 잔량 합계 |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y | 매수호가 1~5의 잔량 합계 |
| `total_askp_csnu` | 총 매도호가 건수 | String | 10 | Y | 매도호가 1~5의 미체결 주문 건수 합계 |
| `total_bidp_csnu` | 총 매수호가 건수 | String | 10 | Y | 매수호가 1~5의 미체결 주문 건수 합계 |
| `aspr_acpt_hour` | 호가 접수 시간 | String | 6 | Y | 가장 최근 호가의 접수 시간 |

### 응답 예시

```json
{
  "output1": {
    "hts_kor_isnm": "F 202206",
    "futs_prpr": "364.40",
    "prdy_vrss_sign": "2",
    "futs_prdy_vrss": "3.00",
    "futs_prdy_ctrt": "0.83",
    "acml_vol": "193112",
    "futs_prdy_clpr": "361.40",
    "futs_shrn_iscd": "101S06"
  },
  "output2": {
    "futs_askp1": "364.40",
    "futs_askp2": "364.45",
    "futs_askp3": "364.50",
    "futs_askp4": "364.55",
    "futs_askp5": "364.60",
    "futs_bidp1": "364.35",
    "futs_bidp2": "364.30",
    "futs_bidp3": "364.25",
    "futs_bidp4": "364.20",
    "futs_bidp5": "364.15",
    "askp_rsqn1": "35",
    "askp_rsqn2": "47",
    "askp_rsqn3": "32",
    "askp_rsqn4": "56",
    "askp_rsqn5": "88",
    "bidp_rsqn1": "22",
    "bidp_rsqn2": "70",
    "bidp_rsqn3": "68",
    "bidp_rsqn4": "97",
    "bidp_rsqn5": "42",
    "askp_csnu1": "9",
    "askp_csnu2": "19",
    "askp_csnu3": "21",
    "askp_csnu4": "28",
    "askp_csnu5": "20",
    "bidp_csnu1": "9",
    "bidp_csnu2": "45",
    "bidp_csnu3": "26",
    "bidp_csnu4": "31",
    "bidp_csnu5": "22",
    "total_askp_rsqn": "7140",
    "total_bidp_rsqn": "9319",
    "total_askp_csnu": "1091",
    "total_bidp_csnu": "1115",
    "aspr_acpt_hour": "153744"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

