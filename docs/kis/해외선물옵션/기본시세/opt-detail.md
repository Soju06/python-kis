# 해외옵션종목상세 [해외선물-034]

> [해외선물옵션] 기본시세

해외옵션종목상세 API입니다.

(주의) sstl_price 자리에 정산가 X 전일종가 O 가 수신되는 점 유의 부탁드립니다.

(중요) 해외옵션시세 출력값을 해석하실 때 focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다.

- focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일) 다운로드 방법
  1) focode.mst(해외지수옵션 종목마스터파일)
     : 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션 클릭하여 다운로드 후
       Github의 헤더정보(https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/해외옵션정보.h)를 참고하여 해석
  2) fostkcode.mst(해외주식옵션 종목마스터파일)
     : 포럼 > FAQ > 종목정보 다운로드(해외) - 해외주식옵션 클릭하여 다운로드 후
       Github의 헤더정보(https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/해외주식옵션정보.h)를 참고하여 해석

- 소수점 계산 시, focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)의 sCalcDesz(계산 소수점) 값 참고
  EX) focode.mst 파일의 sCalcDesz(계산 소수점) 값
       품목코드 OES 계산소수점 -2 → 시세 7525 수신 시 75.25 로 해석
       품목코드 O6E 계산소수점 -4 → 시세 54.0 수신 시 0.0054 로 해석


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `89c2f9ea-62be-4c4a-bd07-66f3fe3234a6` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/opt-detail` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDFO55010100` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-08-23T12:22:02+09:00
- **최종 수정일**: 2025-04-30T12:59:29+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFO55010100 |
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
| `SRS_CD` | 종목명 | String | 32 | Y | ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고 |

### 요청 예시

```json
SRS_CD:OESU24 P5650
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
| `exch_cd` | 거래소코드 | String | 10 | Y |  |
| `clas_cd` | 품목종류 | String | 1 | Y |  |
| `crc_cd` | 거래통화 | String | 10 | Y |  |
| `sttl_price` | 전일종가 | String | 15 | Y | (★주의) 정산가 X 전일종가 O 가 수신됨  ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션 |
| `sttl_date` | 정산일 | String | 8 | Y |  |
| `trst_mgn` | 증거금 | String | 19 | Y |  |
| `disp_digit` | 가격표시진법 | String | 10 | Y |  |
| `tick_sz` | 틱사이즈 | String | 19 | Y |  |
| `tick_val` | 틱가치 | String | 19 | Y |  |
| `mrkt_open_date` | 장개시일자 | String | 8 | Y |  |
| `mrkt_open_time` | 장개시시각 | String | 6 | Y |  |
| `mrkt_close_date` | 장마감일자 | String | 8 | Y |  |
| `mrkt_close_time` | 장마감시각 | String | 6 | Y |  |
| `trd_fr_date` | 상장일 | String | 8 | Y |  |
| `expr_date` | 만기일 | String | 8 | Y |  |
| `trd_to_date` | 최종거래일 | String | 8 | Y |  |
| `remn_cnt` | 잔존일수 | String | 4 | Y |  |
| `stat_tp` | 매매여부 | String | 1 | Y |  |
| `ctrt_size` | 계약크기 | String | 19 | Y |  |
| `stl_tp` | 최종결제구분 | String | 20 | Y |  |
| `frst_noti_date` | 최초식별일 | String | 8 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "exch_cd": "CME",
    "clas_cd": "4",
    "crc_cd": "USD",
    "sttl_price": "           7525",
    "sttl_date": "20240826",
    "trst_mgn": "               7788",
    "disp_digit": "        10",
    "tick_sz": "                  0",
    "tick_val": "                2.5",
    "mrkt_open_date": "20240826",
    "mrkt_open_time": "070000",
    "mrkt_close_date": "20240827",
    "mrkt_close_time": "060000",
    "trd_fr_date": "20240610",
    "expr_date": "20240920",
    "trd_to_date": "20240920",
    "remn_cnt": "  26",
    "stat_tp": "1",
    "ctrt_size": "                 50",
    "stl_tp": "현금결제",
    "frst_noti_date": "20240920"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

