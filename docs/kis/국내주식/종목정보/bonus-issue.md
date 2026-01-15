# 예탁원정보(무상증자일정) [국내주식-144]

> [국내주식] 종목정보

예탁원정보(무상증자일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0656] 무상증자 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `281cea6a-ae69-4837-99dd-e7e6ba1ff442` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/bonus-issue` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHKDB669101C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12
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
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669101C0 |
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
| `fix_rate` | 확정배정율 | String | 152 | Y |  |
| `odd_rec_price` | 단주기준가 | String | 9 | Y |  |
| `right_dt` | 권리락일 | String | 8 | Y |  |
| `odd_pay_dt` | 단주대금지급일 | String | 23 | Y |  |
| `list_date` | 상장/등록일 | String | 8 | Y |  |
| `tot_issue_stk_qty` | 발행주식 | String | 12 | Y |  |
| `issue_stk_qty` | 발행할주식 | String | 12 | Y |  |
| `stk_kind` | 주식종류 | String | 2 | Y |  |

### 응답 예시

```json
{
    "output1": [
        {
            "record_date": "20240326",
            "sht_cd": "466100",
            "isin_name": "클로봇",
            "fix_rate": "1000.0",
            "odd_rec_price": "000000000",
            "right_dt": "20240325",
            "odd_pay_dt": "",
            "list_date": "",
            "tot_issue_stk_qty": "     1885394",
            "issue_stk_qty": "    18853940",
            "stk_kind": "01"
        },
        {
            "record_date": "20240315",
            "sht_cd": "473980",
            "isin_name": "노머스",
            "fix_rate": "3900.0",
            "odd_rec_price": "000000000",
            "right_dt": "20240314",
            "odd_pay_dt": "",
            "list_date": "",
            "tot_issue_stk_qty": "      234220",
            "issue_stk_qty": "     9134580",
            "stk_kind": "01"
        },
        {
            "record_date": "20240314",
            "sht_cd": "377220",
            "isin_name": "프롬바이오",
            "fix_rate": "100.00",
            "odd_rec_price": "000000000",
            "right_dt": "20240313",
            "odd_pay_dt": "",
            "list_date": "20240405",
            "tot_issue_stk_qty": "    14155000",
            "issue_stk_qty": "    14155000",
            "stk_kind": "01"
        },
        {
            "record_date": "20240307",
            "sht_cd": "357230",
            "isin_name": "에이치피오",
            "fix_rate": "100.00",
            "odd_rec_price": "000000000",
            "right_dt": "20240306",
            "odd_pay_dt": "",
            "list_date": "20240329",
            "tot_issue_stk_qty": "    21149725",
            "issue_stk_qty": "    20337240",
            "stk_kind": "01"
        },
        {
            "record_date": "20240305",
            "sht_cd": "005810",
            "isin_name": "풍산홀딩스",
            "fix_rate": " 50.00",
            "odd_rec_price": "000029850",
            "right_dt": "20240304",
            "odd_pay_dt": "2024/03/29 ~ 2024/03/29",
            "list_date": "20240322",
            "tot_issue_stk_qty": "     9748528",
            "issue_stk_qty": "     4668764",
            "stk_kind": "01"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

