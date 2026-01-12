# 해외선물 상품기본정보 [해외선물-023]

> [해외선물옵션] 기본시세

해외선물옵션 상품기본정보 API입니다.
QRY_CNT에 SRS_CD 요청 개수 입력, SRS_CD_01 ~SRS_CD_32 까지 최대 32건의 상품코드 추가 입력하여 해외선물옵션 상품기본정보 확인이 가능합니다. (아래 Example 참고)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `48c30d93-ffc0-47c7-a6ba-da728b0b3d5d` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/search-contract-detail` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `HHDFC55200000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
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
| `tr_id` | 거래ID | String | 13 | Y | HHDFC55200000 |
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
| `QRY_CNT` | 요청개수 | String | 4 | Y | 입력한 코드 개수 |
| `SRS_CD_01` | 품목종류 | String | 32 | Y | 최대 32개 까지 가능 |
| `SRS_CD_02…` | 품목종류… | String | 32 | Y |  |
| `SRS_CD_32` | 품목종류 | String | 32 | Y |  |

### 요청 예시

```json
QRY_CNT:2
SRS_CD_01:6AM24
SRS_CD_02:10YK24
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
| `clas_cd` | 품목종류 | String | 3 | Y |  |
| `crc_cd` | 거래통화 | String | 10 | Y |  |
| `sttl_price` | 정산가 | String | 15 | Y |  |
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
| `sub_exch_nm` | 서브거래소코드 | String | 32 | Y |  |

### 응답 예시

```json
{
  "output2": [
    {
      "exch_cd": "CME",
      "clas_cd": "001",
      "crc_cd": "USD",
      "sttl_price": "         6684.5",
      "sttl_date": "20240516",
      "trst_mgn": "               1595",
      "disp_digit": "        10",
      "tick_sz": "            0.00005",
      "tick_val": "                  5",
      "mrkt_open_date": "20240517",
      "mrkt_open_time": "070000",
      "mrkt_close_date": "20240518",
      "mrkt_close_time": "060000",
      "trd_fr_date": "20190604",
      "expr_date": "20240617",
      "trd_to_date": "20240617",
      "remn_cnt": "  29",
      "stat_tp": "1",
      "ctrt_size": "             100000",
      "stl_tp": "실물인수도",
      "frst_noti_date": "20240617",
      "sub_exch_nm": "CME"
    },
    {
      "exch_cd": "CME",
      "clas_cd": "002",
      "crc_cd": "USD",
      "sttl_price": "           4375",
      "sttl_date": "20240516",
      "trst_mgn": "                352",
      "disp_digit": "        10",
      "tick_sz": "              0.001",
      "tick_val": "                  1",
      "mrkt_open_date": "20240517",
      "mrkt_open_time": "070000",
      "mrkt_close_date": "20240518",
      "mrkt_close_time": "060000",
      "trd_fr_date": "20240315",
      "expr_date": "20240531",
      "trd_to_date": "20240531",
      "remn_cnt": "  15",
      "stat_tp": "1",
      "ctrt_size": "               1000",
      "stl_tp": "현금결제",
      "frst_noti_date": "20240531",
      "sub_exch_nm": "CBOT"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
