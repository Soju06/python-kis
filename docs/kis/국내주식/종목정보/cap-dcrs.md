# 예탁원정보(자본감소일정)[국내주식-149]

> [국내주식] 종목정보

예탁원정보(자본감소일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0665] 자본감소 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `27e843a3-826a-4a92-95f1-12be4c111898` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/cap-dcrs` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `HHKDB669106C0`, `모의투자 미지원` |

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
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669106C0 |
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
| `CTS` | CTS | String | 17 | Y | 공백 |
| `F_DT` | 조회일자From | String | 8 | Y | 일자 ~ |
| `T_DT` | 조회일자To | String | 8 | Y | ~ 일자 |
| `SHT_CD` | 종목코드 | String | 9 | Y | 공백: 전체,  특정종목 조회시 : 종목코드 |

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
| `record_date` | 기준일 | String | 8 | Y |  |
| `sht_cd` | 종목코드 | String | 9 | Y |  |
| `isin_name` | 종목명 | String | 40 | Y |  |
| `stk_kind` | 주식종류 | String | 10 | Y |  |
| `reduce_cap_type` | 감자구분 | String | 9 | Y |  |
| `reduce_cap_rate` | 감자배정율 | String | 142 | Y |  |
| `comp_way` | 계산방법 | String | 6 | Y |  |
| `td_stop_dt` | 매매거래정지기간 | String | 23 | Y |  |
| `list_dt` | 상장/등록일 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "record_date": "20240315",
      "sht_cd": "067390",
      "isin_name": "아스트",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2024/03/14 ~ 2024/03/31",
      "list_dt": "2024/04/01"
    },
    {
      "record_date": "20240226",
      "sht_cd": "000040",
      "isin_name": "케이알모터스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.30",
      "comp_way": "곱하기",
      "td_stop_dt": "2024/02/23 ~ 2024/03/17",
      "list_dt": "2024/03/18"
    },
    {
      "record_date": "20240208",
      "sht_cd": "033180",
      "isin_name": "케이에이치필룩스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2024/02/07 ~ 2024/02/28",
      "list_dt": "2024/02/29"
    },
    {
      "record_date": "20240207",
      "sht_cd": "219750",
      "isin_name": "지티지웰니스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 4.00",
      "comp_way": "나누기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20240129",
      "sht_cd": "057880",
      "isin_name": "피에이치씨",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "2024/01/26 ~ 2024/02/20",
      "list_dt": "2024/02/21"
    },
    {
      "record_date": "20240115",
      "sht_cd": "001140",
      "isin_name": "국보",
      "stk_kind": "보통",
      "reduce_cap_type": "",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2024/01/12 ~ 2024/02/01",
      "list_dt": "2024/02/02"
    },
    {
      "record_date": "20240108",
      "sht_cd": "078130",
      "isin_name": "국일제지",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2024/01/05 ~ 2024/02/21",
      "list_dt": "2024/02/22"
    },
    {
      "record_date": "20240102",
      "sht_cd": "013090",
      "isin_name": "인켈",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.07",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20240102",
      "sht_cd": "013095",
      "isin_name": "인켈1우",
      "stk_kind": "우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.07",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20240102",
      "sht_cd": "013097",
      "isin_name": "인켈2우",
      "stk_kind": "2우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.07",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231227",
      "sht_cd": "078130",
      "isin_name": "국일제지",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/26 ~ 2024/02/20",
      "list_dt": "2024/02/21"
    },
    {
      "record_date": "20231227",
      "sht_cd": "088240",
      "isin_name": "대우조선해양건설",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.00",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231226",
      "sht_cd": "043590",
      "isin_name": "웰킵스하이텍",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.75",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/22 ~ 2024/01/18",
      "list_dt": "2024/01/19"
    },
    {
      "record_date": "20231222",
      "sht_cd": "227420",
      "isin_name": "도부마스크",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": "2024/01/19"
    },
    {
      "record_date": "20231218",
      "sht_cd": "076610",
      "isin_name": "해성옵틱스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/15 ~ 2024/01/07",
      "list_dt": "2024/01/08"
    },
    {
      "record_date": "20231218",
      "sht_cd": "217480",
      "isin_name": "에스디생명공학",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.70",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/15 ~ 2024/01/24",
      "list_dt": "2024/01/25"
    },
    {
      "record_date": "20231215",
      "sht_cd": "321080",
      "isin_name": "메타엠",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.43",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/14 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231214",
      "sht_cd": "299910",
      "isin_name": "베스파",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.10",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/13 ~ 2024/01/14",
      "list_dt": "2024/01/15"
    },
    {
      "record_date": "20231213",
      "sht_cd": "314170",
      "isin_name": "메디에이지",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/12 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231211",
      "sht_cd": "003560",
      "isin_name": "아이에이치큐",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.33",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/08 ~ 2024/01/03",
      "list_dt": "2024/01/04"
    },
    {
      "record_date": "20231211",
      "sht_cd": "078860",
      "isin_name": "아이오케이컴퍼니",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/08 ~ 2023/12/26",
      "list_dt": "2023/12/27"
    },
    {
      "record_date": "20231208",
      "sht_cd": "088240",
      "isin_name": "대우조선해양건설",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.00",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231208",
      "sht_cd": "08824K",
      "isin_name": "대우조선해양건설1우",
      "stk_kind": "우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.00",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231208",
      "sht_cd": "08824L",
      "isin_name": "대우조선해양건설2우",
      "stk_kind": "2우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.00",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231208",
      "sht_cd": "08824M",
      "isin_name": "대우조선해양건설3우",
      "stk_kind": "3우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.00",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231207",
      "sht_cd": "159910",
      "isin_name": "스킨앤스킨",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.10",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/06 ~ 2023/12/26",
      "list_dt": "2023/12/27"
    },
    {
      "record_date": "20231205",
      "sht_cd": "013090",
      "isin_name": "인켈",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.01",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/04 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231205",
      "sht_cd": "013095",
      "isin_name": "인켈1우",
      "stk_kind": "우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.01",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/04 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231205",
      "sht_cd": "013097",
      "isin_name": "인켈2우",
      "stk_kind": "2우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.01",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/04 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231204",
      "sht_cd": "002880",
      "isin_name": "대유에이텍",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 3.00",
      "comp_way": "나누기",
      "td_stop_dt": "2023/12/01 ~ 2023/12/19",
      "list_dt": "2023/12/20"
    },
    {
      "record_date": "20231204",
      "sht_cd": "174880",
      "isin_name": "장원테크",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/01 ~ 2023/12/20",
      "list_dt": "2023/12/21"
    },
    {
      "record_date": "20231204",
      "sht_cd": "406830",
      "isin_name": "여기어때컴퍼니",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.46",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/01 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231204",
      "sht_cd": "40683K",
      "isin_name": "여기어때컴퍼니1우",
      "stk_kind": "우선",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.46",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/12/01 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231129",
      "sht_cd": "299910",
      "isin_name": "베스파",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.33",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/28 ~ 2024/01/14",
      "list_dt": "2024/01/15"
    },
    {
      "record_date": "20231127",
      "sht_cd": "412790",
      "isin_name": "테람스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.10",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231123",
      "sht_cd": "181690",
      "isin_name": "디엔지비",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.25",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/22 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231117",
      "sht_cd": "058450",
      "isin_name": "엔터파트너즈",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/16 ~ 2023/12/11",
      "list_dt": "2023/12/12"
    },
    {
      "record_date": "20231117",
      "sht_cd": "155960",
      "isin_name": "지디",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.10",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/16 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231117",
      "sht_cd": "186630",
      "isin_name": "리치앤타임",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/16 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231113",
      "sht_cd": "144620",
      "isin_name": "코오롱머티리얼",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.75",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/10 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231107",
      "sht_cd": "181690",
      "isin_name": "디엔지비",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/06 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231106",
      "sht_cd": "148140",
      "isin_name": "비디아이",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.10",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/11/03 ~ 2023/12/11",
      "list_dt": "2023/12/12"
    },
    {
      "record_date": "20231101",
      "sht_cd": "155900",
      "isin_name": "바다로19호선박투자회사",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/10/31 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231030",
      "sht_cd": "197210",
      "isin_name": "리드",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.10",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/10/27 ~",
      "list_dt": ""
    },
    {
      "record_date": "20231030",
      "sht_cd": "238500",
      "isin_name": "로보쓰리에이아이앤로보틱스",
      "stk_kind": "보통",
      "reduce_cap_type": "",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/10/27 ~ 2023/11/16",
      "list_dt": "2023/11/17"
    },
    {
      "record_date": "20231020",
      "sht_cd": "148140",
      "isin_name": "비디아이",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.25",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/10/19 ~ 2023/12/11",
      "list_dt": "2023/12/12"
    },
    {
      "record_date": "20231018",
      "sht_cd": "115390",
      "isin_name": "락앤락",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.86",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/10/17 ~ 2023/11/05",
      "list_dt": "2023/11/06"
    },
    {
      "record_date": "20231012",
      "sht_cd": "326830",
      "isin_name": "모르페우스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20231010",
      "sht_cd": "005110",
      "isin_name": "한창",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/10/06 ~ 2023/10/26",
      "list_dt": "2023/10/27"
    },
    {
      "record_date": "20230926",
      "sht_cd": "065560",
      "isin_name": "녹원씨엔아이",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/25 ~ 2023/10/22",
      "list_dt": "2023/10/23"
    },
    {
      "record_date": "20230925",
      "sht_cd": "447800",
      "isin_name": "브릿지벤처스",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230922",
      "sht_cd": "101140",
      "isin_name": "인바이오젠",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/21 ~ 2023/10/22",
      "list_dt": "2023/10/23"
    },
    {
      "record_date": "20230922",
      "sht_cd": "101145",
      "isin_name": "인바이오젠1우",
      "stk_kind": "우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/21 ~ 2023/10/22",
      "list_dt": "2023/10/23"
    },
    {
      "record_date": "20230919",
      "sht_cd": "06911M",
      "isin_name": "코스온3우",
      "stk_kind": "3우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.17",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/18 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230914",
      "sht_cd": "234760",
      "isin_name": "고위드",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.72",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/13 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230912",
      "sht_cd": "069110",
      "isin_name": "코스온",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.17",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/11 ~ 2023/10/10",
      "list_dt": "2023/10/11"
    },
    {
      "record_date": "20230911",
      "sht_cd": "046640",
      "isin_name": "씨디데이타",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.40",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230907",
      "sht_cd": "058420",
      "isin_name": "제이웨이",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/06 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230907",
      "sht_cd": "05842L",
      "isin_name": "제이웨이2우",
      "stk_kind": "2우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/06 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230906",
      "sht_cd": "033180",
      "isin_name": "케이에이치필룩스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.33",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/09/05 ~ 2023/10/03",
      "list_dt": "2023/10/04"
    },
    {
      "record_date": "20230823",
      "sht_cd": "003560",
      "isin_name": "아이에이치큐",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.07",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/08/22 ~ 2023/09/13",
      "list_dt": "2023/09/14"
    },
    {
      "record_date": "20230822",
      "sht_cd": "036630",
      "isin_name": "세종텔레콤",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.81",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/08/21 ~ 2023/09/07",
      "list_dt": "2023/09/08"
    },
    {
      "record_date": "20230822",
      "sht_cd": "043420",
      "isin_name": "에코이에스",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.73",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230822",
      "sht_cd": "220630",
      "isin_name": "맘스터치앤컴퍼니",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.26",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/08/21 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230811",
      "sht_cd": "000360",
      "isin_name": "삼환기업",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/08/10 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230807",
      "sht_cd": "048180",
      "isin_name": "씨제이푸드빌",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.63",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230807",
      "sht_cd": "434840",
      "isin_name": "니즈게임즈",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.88",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/08/04 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230725",
      "sht_cd": "111870",
      "isin_name": "케이에이치전자",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.07",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/07/24 ~ 2023/08/16",
      "list_dt": "2023/08/17"
    },
    {
      "record_date": "20230720",
      "sht_cd": "091090",
      "isin_name": "세원이앤씨",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/07/19 ~ 2023/08/13",
      "list_dt": "2023/08/14"
    },
    {
      "record_date": "20230719",
      "sht_cd": "203810",
      "isin_name": "국제16호선박투자회사",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.16",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/07/18 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230710",
      "sht_cd": "087800",
      "isin_name": "KDB생명보험",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.25",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/07/07 ~ 2023/07/26",
      "list_dt": "2023/07/27"
    },
    {
      "record_date": "20230703",
      "sht_cd": "038530",
      "isin_name": "케이바이오컴퍼니",
      "stk_kind": "보통",
      "reduce_cap_type": "",
      "reduce_cap_rate": " 1.00",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/06/30 ~ 2023/07/20",
      "list_dt": "2023/07/21"
    },
    {
      "record_date": "20230612",
      "sht_cd": "197210",
      "isin_name": "리드",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.04",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/06/09 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230612",
      "sht_cd": "19721K",
      "isin_name": "리드1우",
      "stk_kind": "우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.04",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/06/09 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230608",
      "sht_cd": "139050",
      "isin_name": "시티랩스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.07",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/06/07 ~ 2023/06/27",
      "list_dt": "2023/06/28"
    },
    {
      "record_date": "20230515",
      "sht_cd": "373560",
      "isin_name": "페이투스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230509",
      "sht_cd": "351160",
      "isin_name": "케이온네트워크",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.58",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/05/08 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230508",
      "sht_cd": "138690",
      "isin_name": "엘아이에스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.04",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/05/04 ~ 2023/06/26",
      "list_dt": "2023/06/27"
    },
    {
      "record_date": "20230502",
      "sht_cd": "115580",
      "isin_name": "현대인프라코어",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/28 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230501",
      "sht_cd": "333830",
      "isin_name": "티비에스머티리얼",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.10",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230428",
      "sht_cd": "113300",
      "isin_name": "세명테크",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/27 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230424",
      "sht_cd": "112240",
      "isin_name": "에스에프씨",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/21 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230420",
      "sht_cd": "050320",
      "isin_name": "에스에이치엔엘",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230420",
      "sht_cd": "05032K",
      "isin_name": "에스에이치엔엘1우",
      "stk_kind": "우선",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230418",
      "sht_cd": "203810",
      "isin_name": "국제16호선박투자회사",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.91",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/17 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230418",
      "sht_cd": "391360",
      "isin_name": "버디버디(budybudy)",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/17 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230417",
      "sht_cd": "141020",
      "isin_name": "디에스앤엘",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.25",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/14 ~ 2023/05/08",
      "list_dt": "2023/05/09"
    },
    {
      "record_date": "20230417",
      "sht_cd": "219750",
      "isin_name": "지티지웰니스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/14 ~ 2023/05/07",
      "list_dt": "2023/05/08"
    },
    {
      "record_date": "20230417",
      "sht_cd": "329820",
      "isin_name": "정금에프앤씨",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.05",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230413",
      "sht_cd": "019570",
      "isin_name": "리더스기술투자",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.33",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/12 ~ 2023/05/02",
      "list_dt": "2023/05/03"
    },
    {
      "record_date": "20230411",
      "sht_cd": "050090",
      "isin_name": "비케이홀딩스",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.25",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/04/10 ~ 2023/05/07",
      "list_dt": "2023/05/08"
    },
    {
      "record_date": "20230403",
      "sht_cd": "362570",
      "isin_name": "아이프리원",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.50",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/03/31 ~",
      "list_dt": ""
    },
    {
      "record_date": "20230329",
      "sht_cd": "101000",
      "isin_name": "상상인인더스트리",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.25",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/03/28 ~ 2023/04/20",
      "list_dt": "2023/04/21"
    },
    {
      "record_date": "20230323",
      "sht_cd": "075120",
      "isin_name": "현대아산",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.33",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/03/22 ~ 2023/04/10",
      "list_dt": "2023/04/11"
    },
    {
      "record_date": "20230321",
      "sht_cd": "109960",
      "isin_name": "에이프로젠헬스케어앤게임즈",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.20",
      "comp_way": "곱하기",
      "td_stop_dt": "2023/03/20 ~ 2023/04/06",
      "list_dt": "2023/04/07"
    },
    {
      "record_date": "20230315",
      "sht_cd": "329820",
      "isin_name": "정금에프앤씨",
      "stk_kind": "보통",
      "reduce_cap_type": "무상감자",
      "reduce_cap_rate": " 0.25",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230309",
      "sht_cd": "037870",
      "isin_name": "유베이스",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.86",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    },
    {
      "record_date": "20230309",
      "sht_cd": "434200",
      "isin_name": "예스코서비스",
      "stk_kind": "보통",
      "reduce_cap_type": "유상감자",
      "reduce_cap_rate": " 0.08",
      "comp_way": "곱하기",
      "td_stop_dt": "",
      "list_dt": ""
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
