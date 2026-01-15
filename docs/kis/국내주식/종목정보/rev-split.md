# 예탁원정보(액면교체일정)[국내주식-148]

> [국내주식] 종목정보

예탁원정보(액면교체일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0657] 액면교체 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `86565be8-1f1f-4387-9bae-5bae3031dba1` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/rev-split` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `HHKDB669105C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
- **최종 수정일**: 2025-05-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669105C0 |
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
| `SHT_CD` | 종목코드 | String | 9 | Y | 공백: 전체,  특정종목 조회시 : 종목코드 |
| `CTS` | CTS | String | 17 | Y | 공백 |
| `F_DT` | 조회일자From | String | 8 | Y | 일자 ~ |
| `T_DT` | 조회일자To | String | 8 | Y | ~ 일자 |
| `MARKET_GB` | 시장구분 | String | 1 | Y | 0:전체, 1:코스피, 2:코스닥 |

### 요청 예시

```json
cts:
f_dt:20230301
t_dt:20240326
sht_cd:
market_gb:1
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
| `output1` | 응답상세 | Object |   | Y | array |
| `record_date` | 기준일 | String | 8 | Y |  |
| `sht_cd` | 종목코드 | String | 9 | Y |  |
| `isin_name` | 종목명 | String | 40 | Y |  |
| `inter_bf_face_amt` | 변경전액면가 | String | 9 | Y |  |
| `inter_af_face_amt` | 변경후액면가 | String | 9 | Y |  |
| `td_stop_dt` | 매매거래정지기간 | String | 23 | Y |  |
| `list_dt` | 상장/등록일 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "record_date": "20230823",
      "sht_cd": "001390",
      "isin_name": "케이지케미칼",
      "inter_bf_face_amt": "000005000",
      "inter_af_face_amt": "000001000",
      "td_stop_dt": "2023/08/22 ~ 2023/08/27",
      "list_dt": "2023/08/28"
    },
    {
      "record_date": "20230823",
      "sht_cd": "011690",
      "isin_name": "와이투솔루션",
      "inter_bf_face_amt": "000000500",
      "inter_af_face_amt": "000002500",
      "td_stop_dt": "2023/08/22 ~ 2023/09/11",
      "list_dt": "2023/09/12"
    },
    {
      "record_date": "20230626",
      "sht_cd": "017860",
      "isin_name": "디에스단석",
      "inter_bf_face_amt": "000001000",
      "inter_af_face_amt": "000000500",
      "td_stop_dt": "2023/06/23 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230525",
      "sht_cd": "111380",
      "isin_name": "동인기연",
      "inter_bf_face_amt": "000010000",
      "inter_af_face_amt": "000000100",
      "td_stop_dt": "2023/05/24 ~",
      "list_dt": "2023/11/21"
    },
    {
      "record_date": "20230525",
      "sht_cd": "11138K",
      "isin_name": "동인기연1우",
      "inter_bf_face_amt": "000010000",
      "inter_af_face_amt": "000000100",
      "td_stop_dt": "2023/05/24 ~",
      "list_dt": "2023/11/21"
    },
    {
      "record_date": "20230509",
      "sht_cd": "002900",
      "isin_name": "티와이엠",
      "inter_bf_face_amt": "000000500",
      "inter_af_face_amt": "000002500",
      "td_stop_dt": "2023/05/08 ~ 2023/05/21",
      "list_dt": "2023/05/22"
    },
    {
      "record_date": "20230503",
      "sht_cd": "001140",
      "isin_name": "국보",
      "inter_bf_face_amt": "000000500",
      "inter_af_face_amt": "000005000",
      "td_stop_dt": "2023/05/02 ~ 2023/05/22",
      "list_dt": "2023/05/23"
    },
    {
      "record_date": "20230502",
      "sht_cd": "001440",
      "isin_name": "대한전선",
      "inter_bf_face_amt": "000000100",
      "inter_af_face_amt": "000001000",
      "td_stop_dt": "2023/04/28 ~ 2023/05/15",
      "list_dt": "2023/05/16"
    },
    {
      "record_date": "20230420",
      "sht_cd": "016590",
      "isin_name": "신대양제지",
      "inter_bf_face_amt": "000005000",
      "inter_af_face_amt": "000000500",
      "td_stop_dt": "2023/04/19 ~ 2023/04/23",
      "list_dt": "2023/04/24"
    },
    {
      "record_date": "20230414",
      "sht_cd": "049770",
      "isin_name": "동원에프앤비",
      "inter_bf_face_amt": "000005000",
      "inter_af_face_amt": "000001000",
      "td_stop_dt": "2023/04/13 ~ 2023/04/18",
      "list_dt": "2023/04/19"
    },
    {
      "record_date": "20230413",
      "sht_cd": "003120",
      "isin_name": "일성신약",
      "inter_bf_face_amt": "000005000",
      "inter_af_face_amt": "000001000",
      "td_stop_dt": "2023/04/12 ~ 2023/04/16",
      "list_dt": "2023/04/17"
    },
    {
      "record_date": "20230413",
      "sht_cd": "007120",
      "isin_name": "미래아이앤지",
      "inter_bf_face_amt": "000000100",
      "inter_af_face_amt": "000000500",
      "td_stop_dt": "2023/04/12 ~ 2023/05/03",
      "list_dt": "2023/05/04"
    },
    {
      "record_date": "20230411",
      "sht_cd": "002200",
      "isin_name": "한국수출포장공업",
      "inter_bf_face_amt": "000005000",
      "inter_af_face_amt": "000000500",
      "td_stop_dt": "2023/04/10 ~ 2023/04/16",
      "list_dt": "2023/04/17"
    },
    {
      "record_date": "20230410",
      "sht_cd": "380440",
      "isin_name": "엔에이치기업인수목적19호",
      "inter_bf_face_amt": "000000100",
      "inter_af_face_amt": "000000500",
      "td_stop_dt": "2023/04/07 ~ 2023/05/01",
      "list_dt": "2023/05/02"
    },
    {
      "record_date": "20230407",
      "sht_cd": "000480",
      "isin_name": "시알홀딩스",
      "inter_bf_face_amt": "000005000",
      "inter_af_face_amt": "000000500",
      "td_stop_dt": "2023/04/06 ~ 2023/04/12",
      "list_dt": "2023/04/13"
    },
    {
      "record_date": "20230407",
      "sht_cd": "003200",
      "isin_name": "일신방직",
      "inter_bf_face_amt": "000005000",
      "inter_af_face_amt": "000000500",
      "td_stop_dt": "2023/04/06 ~ 2023/04/13",
      "list_dt": "2023/04/14"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

