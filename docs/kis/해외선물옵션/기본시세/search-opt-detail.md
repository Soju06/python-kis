# 해외옵션 상품기본정보 [해외선물-041]

> [해외선물옵션] 기본시세

해외옵션 상품기본정보 API입니다.

(중요) 해외옵션시세 출력값을 해석하실 때 focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다.

- focode.mst(해외지수옵션 종목마스터파일), (해외주식옵션 종목마스터파일) 다운로드 방법
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
| **API ID** | `42e2e7bd-c2ad-469b-91b2-3962c9931b79` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/search-opt-detail` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `HHDFO55200000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-08-23
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
| `tr_id` | 거래ID | String | 13 | Y | HHDFO55200000 |
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
| `QRY_CNT` | 요청개수 | String | 32 | Y | 입력한 코드 개수 |
| `SRS_CD_01` | 종목코드1 | String | 32 | Y | SRS_CD_01부터 차례로 입력(ex ) OESU24 C5500 최대 30개 까지 가능 |
| `SRS_CD_02...` | 종목코드2 | String | 32 | Y |  |
| `SRS_CD_30` | 종목코드30 | String | 32 | Y |  |

### 요청 예시

```json
QRY_CNT:3
SRS_CD_01:OESU24 C5600
SRS_CD_02:OESU24 C5590
SRS_CD_03:OESU24 C5580
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
| `output2` | 응답상세 | Object |   | Y | array |
| `exch_cd` | 거래소코드 | String | 10 | Y |  |
| `clas_cd` | 품목종류 | String | 1 | Y |  |
| `crc_cd` | 거래통화 | String | 10 | Y |  |
| `sttl_price` | 정산가 | String | 15 | Y | 정산가 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션 |
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
  "output2": [
    {
      "exch_cd": "CME",
      "clas_cd": "4",
      "crc_cd": "USD",
      "sttl_price": "          11000",
      "sttl_date": "20240826",
      "trst_mgn": "               7788",
      "disp_digit": "        10",
      "tick_sz": "                  0",
      "tick_val": "                2.5",
      "mrkt_open_date": "20240826",
      "mrkt_open_time": "000700",
      "mrkt_close_date": "20240827",
      "mrkt_close_time": "000600",
      "trd_fr_date": "20240610",
      "expr_date": "20240920",
      "trd_to_date": "20240920",
      "remn_cnt": "0026",
      "stat_tp": "",
      "ctrt_size": "                 50",
      "stl_tp": "현금결제",
      "frst_noti_date": ""
    },
    {
      "exch_cd": "CME",
      "clas_cd": "4",
      "crc_cd": "USD",
      "sttl_price": "          11675",
      "sttl_date": "20240826",
      "trst_mgn": "               7788",
      "disp_digit": "        10",
      "tick_sz": "                  0",
      "tick_val": "                2.5",
      "mrkt_open_date": "20240826",
      "mrkt_open_time": "000700",
      "mrkt_close_date": "20240827",
      "mrkt_close_time": "000600",
      "trd_fr_date": "20240610",
      "expr_date": "20240920",
      "trd_to_date": "20240920",
      "remn_cnt": "0026",
      "stat_tp": "",
      "ctrt_size": "                 50",
      "stl_tp": "현금결제",
      "frst_noti_date": ""
    },
    {
      "exch_cd": "CME",
      "clas_cd": "4",
      "crc_cd": "USD",
      "sttl_price": "          12400",
      "sttl_date": "20240826",
      "trst_mgn": "               7788",
      "disp_digit": "        10",
      "tick_sz": "                  0",
      "tick_val": "                2.5",
      "mrkt_open_date": "20240826",
      "mrkt_open_time": "000700",
      "mrkt_close_date": "20240827",
      "mrkt_close_time": "000600",
      "trd_fr_date": "20240718",
      "expr_date": "20240920",
      "trd_to_date": "20240920",
      "remn_cnt": "0026",
      "stat_tp": "",
      "ctrt_size": "                 50",
      "stl_tp": "현금결제",
      "frst_noti_date": ""
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
