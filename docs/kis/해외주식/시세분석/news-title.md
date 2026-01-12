# 해외뉴스종합(제목) [해외주식-053]

> [해외주식] 시세분석

해외뉴스종합(제목) API입니다.
한국투자 HTS(eFriend Plus) > [7702] 해외뉴스종합 화면의 "우측 상단 뉴스목록" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `9064a50c-0545-4b6c-8eb2-034f5214974b` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/news-title` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `HHPSTH60100C1` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
- **최종 수정일**: 2025-05-15

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHPSTH60100C1 |
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
| `INFO_GB` | 뉴스구분 | String | 1 | Y | 전체: 공백 |
| `CLASS_CD` | 중분류 | String | 2 | Y | 전체: 공백 |
| `NATION_CD` | 국가코드 | String | 2 | Y | 전체: 공백 CN(중국), HK(홍콩), US(미국) |
| `EXCHANGE_CD` | 거래소코드 | String | 3 | Y | 전체: 공백 |
| `SYMB` | 종목코드 | String | 20 | Y | 전체: 공백 |
| `DATA_DT` | 조회일자 | String | 8 | Y | 전체: 공백 특정일자(YYYYMMDD) ex. 20240502 |
| `DATA_TM` | 조회시간 | String | 6 | Y | 전체: 공백 전체: 공백 특정시간(HHMMSS) ex. 093500 |
| `CTS` | 다음키 | String | 35 | Y | 공백 입력 |

### 요청 예시

```json
INFO_GB:
CLASS_CD:
NATION_CD:
EXCHANGE_CD:
SYMB:
DATA_DT:
DATA_TM:
CTS:
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
| `outblock1` | 응답상세 | Object |   | Y | array |
| `info_gb` | 뉴스구분 | String | 1 | Y |  |
| `news_key` | 뉴스키 | String | 20 | Y |  |
| `data_dt` | 조회일자 | String | 8 | Y |  |
| `data_tm` | 조회시간 | String | 6 | Y |  |
| `class_cd` | 중분류 | String | 2 | Y |  |
| `class_name` | 중분류명 | String | 20 | Y |  |
| `source` | 자료원 | String | 20 | Y |  |
| `nation_cd` | 국가코드 | String | 2 | Y |  |
| `exchange_cd` | 거래소코드 | String | 3 | Y |  |
| `symb` | 종목코드 | String | 20 | Y |  |
| `symb_name` | 종목명 | String | 48 | Y |  |
| `title` | 제목 | String | 128 | Y |  |

### 응답 예시

```json
{
  "outblock1": [
    {
      "info_gb": "t",
      "news_key": "ICH709214",
      "data_dt": "20240503",
      "data_tm": "145447",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "",
      "symb": "",
      "symb_name": "",
      "title": "톰 리 “단기 내 금리인하 가능”"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709213",
      "data_dt": "20240503",
      "data_tm": "144451",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "",
      "symb": "",
      "symb_name": "",
      "title": "美 연준, 7월 금리인하 예상 GS 외"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709212",
      "data_dt": "20240503",
      "data_tm": "144313",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "NAS",
      "symb": "NFLX",
      "symb_name": "넷플릭스",
      "title": "넷플릭스, 광고 전망 낙관 제프리스"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709215",
      "data_dt": "20240503",
      "data_tm": "143706",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "",
      "symb": "",
      "symb_name": "",
      "title": "美 4월 비농업부문 고용자 수 +24.0만 명 추정 아데코"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709208",
      "data_dt": "20240503",
      "data_tm": "142518",
      "class_cd": "03",
      "class_name": "전략/산업",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "",
      "symb": "",
      "symb_name": "",
      "title": "美 모기지 금리, 5주 연속 상승"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709207",
      "data_dt": "20240503",
      "data_tm": "141851",
      "class_cd": "02",
      "class_name": "정책",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "",
      "symb": "",
      "symb_name": "",
      "title": "금리, 현재 정점에 있을 확률 높아 펀드스트랫"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709206",
      "data_dt": "20240503",
      "data_tm": "140506",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "NYS",
      "symb": "FSLY",
      "symb_name": "패스틀리",
      "title": "패스틀리, 단기 악재 직면 - BofA"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709205",
      "data_dt": "20240503",
      "data_tm": "135416",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "NYS",
      "symb": "TJX",
      "symb_name": "TJX",
      "title": "TJX, 기존 소매점 위협 중 - UBS"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709204",
      "data_dt": "20240503",
      "data_tm": "134647",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "NAS",
      "symb": "TTD",
      "symb_name": "트레이드 데스크",
      "title": "트레이드 데스크, 광고시장 현대화로 수혜 가능 - 제프리스"
    },
    {
      "info_gb": "t",
      "news_key": "ICH709203",
      "data_dt": "20240503",
      "data_tm": "133734",
      "class_cd": "05",
      "class_name": "종목리포트",
      "source": "연합미국",
      "nation_cd": "US",
      "exchange_cd": "NYS",
      "symb": "MGM",
      "symb_name": "MGM 리조츠 인터내셔널",
      "title": "MGM 리조트, 매출 증가세 가속 중 - 서스퀘하나"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
