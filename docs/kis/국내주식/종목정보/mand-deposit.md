# 예탁원정보(의무예치일정)[국내주식-153]

> [국내주식] 종목정보

예탁원정보(의무예치일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0758] 의무예치 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `b742d5ef-6d97-4e75-ae25-52daf2f08021` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/mand-deposit` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `HHKDB669110C0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669110C0 |
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
| `T_DT` | 조회일자To | String | 8 | Y | ~ 일자 |
| `SHT_CD` | 종목코드 | String | 9 | Y | 공백: 전체,  특정종목 조회시 : 종목코드 |
| `F_DT` | 조회일자From | String | 8 | Y | 일자 ~ |
| `CTS` | CTS | String | 17 | Y | 공백 |

### 요청 예시

```json
cts:
f_dt:20230301
t_dt:20240326
sht_cd:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `sht_cd` | 종목코드 | String | 9 | Y |  |
| `isin_name` | 종목명 | String | 40 | Y |  |
| `stk_qty` | 주식수 | String | 12 | Y |  |
| `depo_date` | 예치일 | String | 23 | Y |  |
| `depo_reason` | 사유 | String | 10 | Y |  |
| `tot_issue_qty_per_rate` | 총발행주식수대비비율(%) | String | 52 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "sht_cd": "27322R",
      "isin_name": "뷰텔7우",
      "stk_qty": "       68966",
      "depo_date": "2024/03/26 ~ 2025/03/26",
      "depo_reason": "모집매출",
      "tot_issue_qty_per_rate": "10000"
    },
    {
      "sht_cd": "455900",
      "isin_name": "엔젤로보틱스",
      "stk_qty": "       48000",
      "depo_date": "2024/03/26 ~ 2024/06/26",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": "33.51"
    },
    {
      "sht_cd": "455900",
      "isin_name": "엔젤로보틱스",
      "stk_qty": "     4224840",
      "depo_date": "2024/03/26 ~ 2027/03/26",
      "depo_reason": "최대주주",
      "tot_issue_qty_per_rate": "3014."
    },
    {
      "sht_cd": "455900",
      "isin_name": "엔젤로보틱스",
      "stk_qty": "      307036",
      "depo_date": "2024/03/26 ~ 2024/04/26",
      "depo_reason": "최대주주",
      "tot_issue_qty_per_rate": "214.3"
    },
    {
      "sht_cd": "45590S",
      "isin_name": "엔젤로보틱스 8우",
      "stk_qty": "       65128",
      "depo_date": "2024/03/26 ~ 2024/04/26",
      "depo_reason": "벤처금융",
      "tot_issue_qty_per_rate": "700.0"
    },
    {
      "sht_cd": "45590S",
      "isin_name": "엔젤로보틱스 8우",
      "stk_qty": "      865277",
      "depo_date": "2024/03/26 ~ 2024/04/26",
      "depo_reason": "최대주주",
      "tot_issue_qty_per_rate": "9300."
    },
    {
      "sht_cd": "119650",
      "isin_name": "케이씨코트렐",
      "stk_qty": "    12733857",
      "depo_date": "2024/03/25 ~ 2025/03/25",
      "depo_reason": "모집매출",
      "tot_issue_qty_per_rate": "2000."
    },
    {
      "sht_cd": "123840",
      "isin_name": "뉴온",
      "stk_qty": "    62516803",
      "depo_date": "2024/03/25 ~ 2024/09/25",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": "2253."
    },
    {
      "sht_cd": "420570",
      "isin_name": "제이투케이바이오",
      "stk_qty": "         951",
      "depo_date": "2024/03/25 ~ 2024/09/25",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": " 1.71"
    },
    {
      "sht_cd": "019570",
      "isin_name": "리더스기술투자",
      "stk_qty": "     8905532",
      "depo_date": "2024/03/22 ~ 2025/03/22",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": "1697."
    },
    {
      "sht_cd": "036180",
      "isin_name": "지더블유바이텍",
      "stk_qty": "    28911564",
      "depo_date": "2024/03/22 ~ 2025/03/22",
      "depo_reason": "모집매출",
      "tot_issue_qty_per_rate": "3160."
    },
    {
      "sht_cd": "069110",
      "isin_name": "코스온",
      "stk_qty": "     4000000",
      "depo_date": "2024/03/22 ~ 2025/03/22",
      "depo_reason": "모집매출",
      "tot_issue_qty_per_rate": "1107."
    },
    {
      "sht_cd": "440110",
      "isin_name": "파두",
      "stk_qty": "      270200",
      "depo_date": "2024/03/22 ~ 2024/08/07",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": "55.06"
    },
    {
      "sht_cd": "222080",
      "isin_name": "씨아이에스",
      "stk_qty": "       42636",
      "depo_date": "2024/03/21 ~ 2024/09/21",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": " 5.97"
    },
    {
      "sht_cd": "245620",
      "isin_name": "이원다이애그노믹스",
      "stk_qty": "    17633408",
      "depo_date": "2024/03/21 ~ 2025/03/21",
      "depo_reason": "모집매출",
      "tot_issue_qty_per_rate": "1273."
    },
    {
      "sht_cd": "437730",
      "isin_name": "삼현",
      "stk_qty": "       33333",
      "depo_date": "2024/03/21 ~ 2024/06/21",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": "31.54"
    },
    {
      "sht_cd": "437730",
      "isin_name": "삼현",
      "stk_qty": "      390320",
      "depo_date": "2024/03/21 ~ 2024/04/21",
      "depo_reason": "벤처금융",
      "tot_issue_qty_per_rate": "369.3"
    },
    {
      "sht_cd": "476180",
      "isin_name": "마이공사",
      "stk_qty": "      100000",
      "depo_date": "2024/03/20 ~ 2024/09/20",
      "depo_reason": "-",
      "tot_issue_qty_per_rate": "2000."
    },
    {
      "sht_cd": "082740",
      "isin_name": "한화엔진 주식회사",
      "stk_qty": "    11903148",
      "depo_date": "2024/03/19 ~ 2025/03/19",
      "depo_reason": "모집매출",
      "tot_issue_qty_per_rate": "1426."
    },
    {
      "sht_cd": "214870",
      "isin_name": "뉴지랩파마",
      "stk_qty": "    13670000",
      "depo_date": "2024/03/18 ~ 2025/03/18",
      "depo_reason": "모집매출",
      "tot_issue_qty_per_rate": "2921."
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
