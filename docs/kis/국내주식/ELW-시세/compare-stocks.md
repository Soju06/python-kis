# ELW 비교대상종목조회 [국내주식-183]

> [국내주식] ELW 시세

ELW 비교대상종목조회 API입니다.
기초자산 종목코드를 입력하셔서 해당 종목을 기초자산으로 하는 ELW 목록을 조회하실 수 있습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ca2e71e1-5ef4-4489-b4c4-118e10588690` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/compare-stocks` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHKEW151701C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
- **최종 수정일**: 2025-05-07

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKEW151701C0 |
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
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 11517(Primary key) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 종목코드(ex)005930(삼성전자)) |

### 요청 예시

```json
FID_COND_SCR_DIV_CODE:11517
FID_INPUT_ISCD:005930
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
| `output` | 응답상세 | String |   | Y |  |
| `elw_shrn_iscd` | ELW단축종목코드 | String | 9 | Y |  |
| `elw_kor_isnm` | ELW한글종목명 | String | 40 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "elw_shrn_iscd": "58J782",
            "elw_kor_isnm": "KBJ782삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58J993",
            "elw_kor_isnm": "KBJ993삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58JC71",
            "elw_kor_isnm": "KBJC71삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58JC72",
            "elw_kor_isnm": "KBJC72삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58JC73",
            "elw_kor_isnm": "KBJC73삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58JC74",
            "elw_kor_isnm": "KBJC74삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58JC75",
            "elw_kor_isnm": "KBJC75삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58JC76",
            "elw_kor_isnm": "KBJC76삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58JE26",
            "elw_kor_isnm": "KBJE26삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58JE27",
            "elw_kor_isnm": "KBJE27삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58JE28",
            "elw_kor_isnm": "KBJE28삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58JE30",
            "elw_kor_isnm": "KBJE30삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K001",
            "elw_kor_isnm": "KBK001삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K002",
            "elw_kor_isnm": "KBK002삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K003",
            "elw_kor_isnm": "KBK003삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K004",
            "elw_kor_isnm": "KBK004삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K005",
            "elw_kor_isnm": "KBK005삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K006",
            "elw_kor_isnm": "KBK006삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K167",
            "elw_kor_isnm": "KBK167삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K168",
            "elw_kor_isnm": "KBK168삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K169",
            "elw_kor_isnm": "KBK169삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K314",
            "elw_kor_isnm": "KBK314삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K416",
            "elw_kor_isnm": "KBK416삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K417",
            "elw_kor_isnm": "KBK417삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K418",
            "elw_kor_isnm": "KBK418삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K419",
            "elw_kor_isnm": "KBK419삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K420",
            "elw_kor_isnm": "KBK420삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K421",
            "elw_kor_isnm": "KBK421삼성전자풋"
        },
        {
            "elw_shrn_iscd": "58K579",
            "elw_kor_isnm": "KBK579삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K580",
            "elw_kor_isnm": "KBK580삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K581",
            "elw_kor_isnm": "KBK581삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K582",
            "elw_kor_isnm": "KBK582삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K583",
            "elw_kor_isnm": "KBK583삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K584",
            "elw_kor_isnm": "KBK584삼성전자콜"
        },
        {
            "elw_shrn_iscd": "58K585",
            "elw_kor_isnm": "KBK585삼성전자풋"
        },
        ...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

