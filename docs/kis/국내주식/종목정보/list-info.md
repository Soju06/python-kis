# 예탁원정보(상장정보일정)[국내주식-150]

> [국내주식] 종목정보

예탁원정보(상장정보일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0666] 상장정보 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `01fd59f1-e7f6-4192-8b02-d52e5dd7c8f3` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/list-info` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `HHKDB669107C0` |
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
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669107C0 |
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
| `T_DT` | 조회일자To | String | 8 | Y | ~ 일자 |
| `F_DT` | 조회일자From | String | 8 | Y | 일자 ~ |
| `CTS` | CTS | String | 17 | Y | 공백 |

### 요청 예시

```json
cts:
f_dt:20230301
t_dt:20240326
sht_cd:
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
| `list_dt` | 상장/등록일 | String | 10 | Y |  |
| `sht_cd` | 종목코드 | String | 9 | Y |  |
| `isin_name` | 종목명 | String | 40 | Y |  |
| `stk_kind` | 주식종류 | String | 10 | Y |  |
| `issue_type` | 사유 | String | 21 | Y |  |
| `issue_stk_qty` | 상장주식수 | String | 12 | Y |  |
| `tot_issue_stk_qty` | 총발행주식수 | String | 12 | Y |  |
| `issue_price` | 발행가 | String | 9 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "list_dt": "20240326",
      "sht_cd": "034220",
      "isin_name": "LG디스플레이",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "   142184300",
      "tot_issue_stk_qty": "   500000000",
      "issue_price": "     9090"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "047560",
      "isin_name": "이스트소프트",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       13000",
      "tot_issue_stk_qty": "    11488232",
      "issue_price": "    15000"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "054180",
      "isin_name": "메디콕스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     2348484",
      "tot_issue_stk_qty": "    57151168",
      "issue_price": "      792"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "067310",
      "isin_name": "하나마이크론",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "        5500",
      "tot_issue_stk_qty": "    52136475",
      "issue_price": "     9275"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "146060",
      "isin_name": "율촌",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     2391679",
      "tot_issue_stk_qty": "    24015595",
      "issue_price": "     1154"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "403490",
      "isin_name": "우듬지팜",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "      288000",
      "tot_issue_stk_qty": "    45212464",
      "issue_price": "     1000"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "455900",
      "isin_name": "엔젤로보틱스",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "     1648000",
      "tot_issue_stk_qty": "    14322012",
      "issue_price": "    20000"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "455900",
      "isin_name": "엔젤로보틱스",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "      692224",
      "tot_issue_stk_qty": "    14322012",
      "issue_price": "     2891"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "455900",
      "isin_name": "엔젤로보틱스",
      "stk_kind": "보통",
      "issue_type": "통일교체",
      "issue_stk_qty": "     8850720",
      "tot_issue_stk_qty": "    14322012",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240326",
      "sht_cd": "455900",
      "isin_name": "엔젤로보틱스",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "      161120",
      "tot_issue_stk_qty": "    14322012",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "007980",
      "isin_name": "태평양물산",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      162337",
      "tot_issue_stk_qty": "    51175130",
      "issue_price": "     1848"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "119650",
      "isin_name": "케이씨코트렐",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "    12733857",
      "tot_issue_stk_qty": "    63669287",
      "issue_price": "     1380"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "123840",
      "isin_name": "뉴온",
      "stk_kind": "보통",
      "issue_type": "합병",
      "issue_stk_qty": "   175537376",
      "tot_issue_stk_qty": "   277394122",
      "issue_price": "      100"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "151910",
      "isin_name": "에스비더블유생명과학",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     1700680",
      "tot_issue_stk_qty": "   190071722",
      "issue_price": "      294"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "192230",
      "isin_name": "아리바이오",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       16500",
      "tot_issue_stk_qty": "    23632031",
      "issue_price": "     7500"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "192650",
      "isin_name": "드림텍",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       45000",
      "tot_issue_stk_qty": "    68852050",
      "issue_price": "     4518"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "222080",
      "isin_name": "씨아이에스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      350261",
      "tot_issue_stk_qty": "    71440876",
      "issue_price": "     9707"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "373200",
      "isin_name": "하인크코리아",
      "stk_kind": "보통",
      "issue_type": "무상증자",
      "issue_stk_qty": "    56778657",
      "tot_issue_stk_qty": "    75705657",
      "issue_price": "      100"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "420570",
      "isin_name": "제이투케이바이오",
      "stk_kind": "보통",
      "issue_type": "통일교체",
      "issue_stk_qty": "     5059840",
      "tot_issue_stk_qty": "     5574115",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240325",
      "sht_cd": "420570",
      "isin_name": "제이투케이바이오",
      "stk_kind": "보통",
      "issue_type": "합병",
      "issue_stk_qty": "      514275",
      "tot_issue_stk_qty": "     5574115",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "005320",
      "isin_name": "국동",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      144300",
      "tot_issue_stk_qty": "    66750697",
      "issue_price": "      693"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "005810",
      "isin_name": "풍산홀딩스",
      "stk_kind": "보통",
      "issue_type": "무상증자",
      "issue_stk_qty": "     4668764",
      "tot_issue_stk_qty": "    14417292",
      "issue_price": "     5000"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "012510",
      "isin_name": "더존비즈온",
      "stk_kind": "보통",
      "issue_type": "합병",
      "issue_stk_qty": "     9423939",
      "tot_issue_stk_qty": "    30382784",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "024850",
      "isin_name": "에이치엘비이노베이션",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     2681010",
      "tot_issue_stk_qty": "    72378055",
      "issue_price": "     1022"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "036180",
      "isin_name": "지더블유바이텍",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "    28911564",
      "tot_issue_stk_qty": "    91464525",
      "issue_price": "      588"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "038460",
      "isin_name": "바이오스마트",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      140230",
      "tot_issue_stk_qty": "    21437123",
      "issue_price": "     3209"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "060280",
      "isin_name": "큐렉소",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "        5000",
      "tot_issue_stk_qty": "    41084990",
      "issue_price": "     9510"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "066970",
      "isin_name": "엘앤에프",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "         168",
      "tot_issue_stk_qty": "    36255993",
      "issue_price": "    71430"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "115450",
      "isin_name": "에이치엘비테라퓨틱스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       15351",
      "tot_issue_stk_qty": "    77948338",
      "issue_price": "     3619"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "197140",
      "isin_name": "디지캡",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       16000",
      "tot_issue_stk_qty": "     9596854",
      "issue_price": "     4098"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "199730",
      "isin_name": "바이오인프라",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       37500",
      "tot_issue_stk_qty": "     4834367",
      "issue_price": "     6667"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "314930",
      "isin_name": "바이오다인",
      "stk_kind": "보통",
      "issue_type": "무상증자",
      "issue_stk_qty": "    23581408",
      "tot_issue_stk_qty": "    29764103",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "403550",
      "isin_name": "쏘카",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "        3125",
      "tot_issue_stk_qty": "    32791402",
      "issue_price": "    16000"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "440110",
      "isin_name": "파두",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       34520",
      "tot_issue_stk_qty": "    49072322",
      "issue_price": "     7107"
    },
    {
      "list_dt": "20240322",
      "sht_cd": "441270",
      "isin_name": "파인엠텍",
      "stk_kind": "보통",
      "issue_type": "국내BW행사",
      "issue_stk_qty": "       42313",
      "tot_issue_stk_qty": "    36928663",
      "issue_price": "     7090"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "023960",
      "isin_name": "에쓰씨엔지니어링",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       23132",
      "tot_issue_stk_qty": "    32861366",
      "issue_price": "     1513"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "064520",
      "isin_name": "테크엘",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       50124",
      "tot_issue_stk_qty": "    22005961",
      "issue_price": "     3990"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "065650",
      "isin_name": "메디프론디비티",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "     3814835",
      "tot_issue_stk_qty": "    63153285",
      "issue_price": "      983"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "114840",
      "isin_name": "아이패밀리에스씨",
      "stk_kind": "보통",
      "issue_type": "무상증자",
      "issue_stk_qty": "     8600972",
      "tot_issue_stk_qty": "    17201944",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "199800",
      "isin_name": "툴젠",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "        2000",
      "tot_issue_stk_qty": "     7930258",
      "issue_price": "    32850"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "222080",
      "isin_name": "씨아이에스",
      "stk_kind": "보통",
      "issue_type": "합병",
      "issue_stk_qty": "      544552",
      "tot_issue_stk_qty": "    71440876",
      "issue_price": "    11116"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "245620",
      "isin_name": "이원다이애그노믹스",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "    17633408",
      "tot_issue_stk_qty": "   138493951",
      "issue_price": "      431"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "323410",
      "isin_name": "카카오뱅크",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "        5000",
      "tot_issue_stk_qty": "   476921137",
      "issue_price": "     5000"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "417010",
      "isin_name": "나노팀",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "      228000",
      "tot_issue_stk_qty": "    19724328",
      "issue_price": "     2631"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "437730",
      "isin_name": "삼현",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "     2033333",
      "tot_issue_stk_qty": "    10569189",
      "issue_price": "    30000"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "437730",
      "isin_name": "삼현",
      "stk_kind": "보통",
      "issue_type": "통일교체",
      "issue_stk_qty": "     8535856",
      "tot_issue_stk_qty": "    10569189",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240321",
      "sht_cd": "452300",
      "isin_name": "캡스톤파트너스",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       66250",
      "tot_issue_stk_qty": "    14060755",
      "issue_price": "      560"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "001210",
      "isin_name": "금호전기",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      260416",
      "tot_issue_stk_qty": "    38069709",
      "issue_price": "      768"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "011300",
      "isin_name": "성안",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     1828152",
      "tot_issue_stk_qty": "    70551785",
      "issue_price": "     1094"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "031310",
      "isin_name": "아이즈비전",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       61859",
      "tot_issue_stk_qty": "    22843356",
      "issue_price": "     2829"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "067630",
      "isin_name": "에이치엘비생명과학",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       20990",
      "tot_issue_stk_qty": "   107122760",
      "issue_price": "    11434"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "170900",
      "isin_name": "동아에스티",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "          56",
      "tot_issue_stk_qty": "     8834970",
      "issue_price": "    72359"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "255220",
      "isin_name": "에스지이",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     1692045",
      "tot_issue_stk_qty": "    61173984",
      "issue_price": "     1182"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "255220",
      "isin_name": "에스지이",
      "stk_kind": "보통",
      "issue_type": "국내BW행사",
      "issue_stk_qty": "       87918",
      "tot_issue_stk_qty": "    61173984",
      "issue_price": "     1125"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "321550",
      "isin_name": "티움바이오",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "      220001",
      "tot_issue_stk_qty": "    25662498",
      "issue_price": "     7500"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "355150",
      "isin_name": "코스텍시스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      186000",
      "tot_issue_stk_qty": "     7706770",
      "issue_price": "     5000"
    },
    {
      "list_dt": "20240320",
      "sht_cd": "457190",
      "isin_name": "이수스페셜티케미컬",
      "stk_kind": "보통",
      "issue_type": "국내BW행사",
      "issue_stk_qty": "        1059",
      "tot_issue_stk_qty": "     5599832",
      "issue_price": "    18602"
    },
    {
      "list_dt": "20240319",
      "sht_cd": "007280",
      "isin_name": "한국특강",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      223713",
      "tot_issue_stk_qty": "    60813311",
      "issue_price": "     1788"
    },
    {
      "list_dt": "20240319",
      "sht_cd": "032980",
      "isin_name": "바이온",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      220264",
      "tot_issue_stk_qty": "    40517904",
      "issue_price": "      908"
    },
    {
      "list_dt": "20240319",
      "sht_cd": "064800",
      "isin_name": "젬백스링크",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       71123",
      "tot_issue_stk_qty": "   107875617",
      "issue_price": "     1406"
    },
    {
      "list_dt": "20240319",
      "sht_cd": "073570",
      "isin_name": "리튬포어스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      218575",
      "tot_issue_stk_qty": "    35970918",
      "issue_price": "     4575"
    },
    {
      "list_dt": "20240319",
      "sht_cd": "082740",
      "isin_name": "한화엔진 주식회사",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "    11903148",
      "tot_issue_stk_qty": "    83447142",
      "issue_price": "     7520"
    },
    {
      "list_dt": "20240319",
      "sht_cd": "174900",
      "isin_name": "앱클론",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "      130707",
      "tot_issue_stk_qty": "    16423321",
      "issue_price": "    10079"
    },
    {
      "list_dt": "20240319",
      "sht_cd": "367000",
      "isin_name": "플래티어",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       21000",
      "tot_issue_stk_qty": "     8388207",
      "issue_price": "     4930"
    },
    {
      "list_dt": "20240318",
      "sht_cd": "000040",
      "isin_name": "케이알모터스",
      "stk_kind": "보통",
      "issue_type": "자본감소",
      "issue_stk_qty": "    29132868",
      "tot_issue_stk_qty": "    29132868",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240318",
      "sht_cd": "001720",
      "isin_name": "신영증권",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "        4950",
      "tot_issue_stk_qty": "     9434532",
      "issue_price": "    16233"
    },
    {
      "list_dt": "20240318",
      "sht_cd": "114630",
      "isin_name": "폴라리스우노",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      506512",
      "tot_issue_stk_qty": "    77757548",
      "issue_price": "      691"
    },
    {
      "list_dt": "20240318",
      "sht_cd": "123840",
      "isin_name": "뉴온",
      "stk_kind": "보통",
      "issue_type": "상호변경",
      "issue_stk_qty": "   277394122",
      "tot_issue_stk_qty": "   277394122",
      "issue_price": "      100"
    },
    {
      "list_dt": "20240318",
      "sht_cd": "214870",
      "isin_name": "뉴지랩파마",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "    13670000",
      "tot_issue_stk_qty": "    46796106",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240318",
      "sht_cd": "217330",
      "isin_name": "싸이토젠",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "        3286",
      "tot_issue_stk_qty": "    22423102",
      "issue_price": "    15290"
    },
    {
      "list_dt": "20240318",
      "sht_cd": "311390",
      "isin_name": "네오크레마",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "     2922552",
      "tot_issue_stk_qty": "    10979147",
      "issue_price": "     6159"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "035720",
      "isin_name": "카카오",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "      154263",
      "tot_issue_stk_qty": "   445243887",
      "issue_price": "    28199"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "047920",
      "isin_name": "에이치엘비제약",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       15000",
      "tot_issue_stk_qty": "    31746701",
      "issue_price": "     5608"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "059270",
      "isin_name": "해성티피씨",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       33000",
      "tot_issue_stk_qty": "    10797992",
      "issue_price": "     3000"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "067630",
      "isin_name": "에이치엘비생명과학",
      "stk_kind": "보통",
      "issue_type": "국내BW행사",
      "issue_stk_qty": "      738038",
      "tot_issue_stk_qty": "   107122760",
      "issue_price": "     8889"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "079160",
      "isin_name": "씨제이씨지브이",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "          50",
      "tot_issue_stk_qty": "   122432139",
      "issue_price": "    17745"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "082740",
      "isin_name": "한화엔진 주식회사",
      "stk_kind": "보통",
      "issue_type": "상호변경",
      "issue_stk_qty": "    71543994",
      "tot_issue_stk_qty": "    83447142",
      "issue_price": "     1000"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "117670",
      "isin_name": "알파홀딩스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     1645434",
      "tot_issue_stk_qty": "    39641629",
      "issue_price": "      942"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "139670",
      "isin_name": "키네마스터",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "       22899",
      "tot_issue_stk_qty": "    14118810",
      "issue_price": "    13100"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "140860",
      "isin_name": "파크시스템스",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "        2000",
      "tot_issue_stk_qty": "     6970859",
      "issue_price": "    25940"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "214330",
      "isin_name": "금호에이치티",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "     2384614",
      "tot_issue_stk_qty": "   213914131",
      "issue_price": "      650"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "261200",
      "isin_name": "덴티스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       55358",
      "tot_issue_stk_qty": "    15809700",
      "issue_price": "     9032"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "272110",
      "isin_name": "케이엔제이보통주",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       15000",
      "tot_issue_stk_qty": "     7975395",
      "issue_price": "     3000"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "282880",
      "isin_name": "코윈테크",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      160365",
      "tot_issue_stk_qty": "    10825983",
      "issue_price": "    24943"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "288330",
      "isin_name": "브릿지바이오테라퓨틱스",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "      279328",
      "tot_issue_stk_qty": "    24119154",
      "issue_price": "     7160"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "348370",
      "isin_name": "엔켐",
      "stk_kind": "보통",
      "issue_type": "국내BW행사",
      "issue_stk_qty": "        2859",
      "tot_issue_stk_qty": "    18694319",
      "issue_price": "    78677"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "348370",
      "isin_name": "엔켐",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "      301947",
      "tot_issue_stk_qty": "    18694319",
      "issue_price": "    55648"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "384470",
      "isin_name": "코어라인소프트",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      272453",
      "tot_issue_stk_qty": "    12793664",
      "issue_price": "     5322"
    },
    {
      "list_dt": "20240315",
      "sht_cd": "418620",
      "isin_name": "이에이트",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       52000",
      "tot_issue_stk_qty": "     9647677",
      "issue_price": "     9761"
    },
    {
      "list_dt": "20240314",
      "sht_cd": "052770",
      "isin_name": "아이톡시",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "      646825",
      "tot_issue_stk_qty": "    43550918",
      "issue_price": "     1260"
    },
    {
      "list_dt": "20240314",
      "sht_cd": "084180",
      "isin_name": "수성웹툰",
      "stk_kind": "보통",
      "issue_type": "상호변경",
      "issue_stk_qty": "   115499325",
      "tot_issue_stk_qty": "   115499325",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240314",
      "sht_cd": "091810",
      "isin_name": "티웨이항공",
      "stk_kind": "보통",
      "issue_type": "주식전환",
      "issue_stk_qty": "    14607425",
      "tot_issue_stk_qty": "   215378976",
      "issue_price": "     1643"
    },
    {
      "list_dt": "20240314",
      "sht_cd": "139050",
      "isin_name": "비에프랩스",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       19724",
      "tot_issue_stk_qty": "     8644551",
      "issue_price": "    10545"
    },
    {
      "list_dt": "20240314",
      "sht_cd": "276240",
      "isin_name": "엘리비젼",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "     2360000",
      "tot_issue_stk_qty": "    10413138",
      "issue_price": "      500"
    },
    {
      "list_dt": "20240314",
      "sht_cd": "311060",
      "isin_name": "엘에이티",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "       26000",
      "tot_issue_stk_qty": "     7074134",
      "issue_price": "     2063"
    },
    {
      "list_dt": "20240314",
      "sht_cd": "377300",
      "isin_name": "카카오페이",
      "stk_kind": "보통",
      "issue_type": "STOCKOPTION행사",
      "issue_stk_qty": "        2700",
      "tot_issue_stk_qty": "   134470018",
      "issue_price": "    34101"
    },
    {
      "list_dt": "20240313",
      "sht_cd": "000520",
      "isin_name": "삼일제약",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "       46474",
      "tot_issue_stk_qty": "    19806074",
      "issue_price": "     7531"
    },
    {
      "list_dt": "20240313",
      "sht_cd": "000520",
      "isin_name": "삼일제약",
      "stk_kind": "보통",
      "issue_type": "국내BW행사",
      "issue_stk_qty": "     1131380",
      "tot_issue_stk_qty": "    19806074",
      "issue_price": "     7071"
    },
    {
      "list_dt": "20240313",
      "sht_cd": "032350",
      "isin_name": "롯데관광개발",
      "stk_kind": "보통",
      "issue_type": "국내CB행사",
      "issue_stk_qty": "      396432",
      "tot_issue_stk_qty": "    76185869",
      "issue_price": "    10090"
    },
    {
      "list_dt": "20240313",
      "sht_cd": "036220",
      "isin_name": "오상헬스케어",
      "stk_kind": "보통",
      "issue_type": "유상증자",
      "issue_stk_qty": "     1019700",
      "tot_issue_stk_qty": "    14104416",
      "issue_price": "    20000"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

