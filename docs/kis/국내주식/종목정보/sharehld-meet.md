# 예탁원정보(주주총회일정) [국내주식-154]

> [국내주식] 종목정보

예탁원정보(주주총회일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0759] 주주총회 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `e2633b78-811f-40b8-a933-dcba64c3e0e8` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/sharehld-meet` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHKDB669111C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12T12:44:16+09:00
- **최종 수정일**: 2025-05-14T13:22:22+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669111C0 |
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
f_dt:20230101
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
| `gen_meet_dt` | 주총일자 | String | 10 | Y |  |
| `gen_meet_type` | 주총사유 | String | 8 | Y |  |
| `agenda` | 주총의안 | String | 71 | Y |  |
| `vote_tot_qty` | 의결권주식총수 | String | 12 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "record_date": "20240322",
      "sht_cd": "388370",
      "isin_name": "(주)우앤컴퍼니",
      "gen_meet_dt": "2024/04/18",
      "gen_meet_type": "임시총회",
      "agenda": "정관변경",
      "vote_tot_qty": "      959800"
    },
    {
      "record_date": "20240322",
      "sht_cd": "388370",
      "isin_name": "(주)우앤컴퍼니",
      "gen_meet_dt": "2024/04/18",
      "gen_meet_type": "임시총회",
      "agenda": "이사선임",
      "vote_tot_qty": "      959800"
    },
    {
      "record_date": "20240321",
      "sht_cd": "323530",
      "isin_name": "(주)아이월드제약",
      "gen_meet_dt": "2024/04/25",
      "gen_meet_type": "임시총회",
      "agenda": "사내이사 선임",
      "vote_tot_qty": "    25721999"
    },
    {
      "record_date": "20240321",
      "sht_cd": "323530",
      "isin_name": "(주)아이월드제약",
      "gen_meet_dt": "2024/04/25",
      "gen_meet_type": "임시총회",
      "agenda": "정관변경",
      "vote_tot_qty": "    25721999"
    },
    {
      "record_date": "20240321",
      "sht_cd": "323530",
      "isin_name": "(주)아이월드제약",
      "gen_meet_dt": "2024/04/25",
      "gen_meet_type": "임시총회",
      "agenda": "사외이사 선임",
      "vote_tot_qty": "    25721999"
    },
    {
      "record_date": "20240315",
      "sht_cd": "091090",
      "isin_name": "세원이앤씨(주)",
      "gen_meet_dt": "2024/04/12",
      "gen_meet_type": "임시총회",
      "agenda": "이사해임(주주제안)",
      "vote_tot_qty": "    52754723"
    },
    {
      "record_date": "20240315",
      "sht_cd": "091090",
      "isin_name": "세원이앤씨(주)",
      "gen_meet_dt": "2024/04/12",
      "gen_meet_type": "임시총회",
      "agenda": "정관변경(주주제안)",
      "vote_tot_qty": "    52754723"
    },
    {
      "record_date": "20240315",
      "sht_cd": "091090",
      "isin_name": "세원이앤씨(주)",
      "gen_meet_dt": "2024/04/12",
      "gen_meet_type": "임시총회",
      "agenda": "이사해임(주주제안)",
      "vote_tot_qty": "    52754723"
    },
    {
      "record_date": "20240315",
      "sht_cd": "091090",
      "isin_name": "세원이앤씨(주)",
      "gen_meet_dt": "2024/04/12",
      "gen_meet_type": "임시총회",
      "agenda": "사외이사 선임(주주제안)",
      "vote_tot_qty": "    52754723"
    },
    {
      "record_date": "20240315",
      "sht_cd": "091090",
      "isin_name": "세원이앤씨(주)",
      "gen_meet_dt": "2024/04/12",
      "gen_meet_type": "임시총회",
      "agenda": "사내이사 선임(주주제안)",
      "vote_tot_qty": "    52754723"
    },
    {
      "record_date": "20240312",
      "sht_cd": "380440",
      "isin_name": "엔에이치기업인수목적19호(주)",
      "gen_meet_dt": "2024/04/19",
      "gen_meet_type": "임시총회",
      "agenda": "청산결산보고서승인",
      "vote_tot_qty": "    10258000"
    },
    {
      "record_date": "20240308",
      "sht_cd": "263540",
      "isin_name": "(주)어스앤에어로스페이스",
      "gen_meet_dt": "2024/04/03",
      "gen_meet_type": "임시총회",
      "agenda": "사내이사 선임",
      "vote_tot_qty": "    14294091"
    },
    {
      "record_date": "20240308",
      "sht_cd": "263540",
      "isin_name": "(주)어스앤에어로스페이스",
      "gen_meet_dt": "2024/04/03",
      "gen_meet_type": "임시총회",
      "agenda": "사내이사 선임",
      "vote_tot_qty": "    14294091"
    },
    {
      "record_date": "20240308",
      "sht_cd": "263540",
      "isin_name": "(주)어스앤에어로스페이스",
      "gen_meet_dt": "2024/04/03",
      "gen_meet_type": "임시총회",
      "agenda": "정관변경",
      "vote_tot_qty": "    14294091"
    },
    {
      "record_date": "20240308",
      "sht_cd": "263540",
      "isin_name": "(주)어스앤에어로스페이스",
      "gen_meet_dt": "2024/04/03",
      "gen_meet_type": "임시총회",
      "agenda": "사내이사 선임",
      "vote_tot_qty": "    14294091"
    },
    {
      "record_date": "20240308",
      "sht_cd": "263540",
      "isin_name": "(주)어스앤에어로스페이스",
      "gen_meet_dt": "2024/04/03",
      "gen_meet_type": "임시총회",
      "agenda": "사외이사 선임",
      "vote_tot_qty": "    14294091"
    },
    {
      "record_date": "20240308",
      "sht_cd": "343990",
      "isin_name": "비즈플레이(주)",
      "gen_meet_dt": "2024/03/27",
      "gen_meet_type": "종류총회",
      "agenda": "정관변경",
      "vote_tot_qty": "    21751896"
    },
    {
      "record_date": "20240307",
      "sht_cd": "001140",
      "isin_name": "(주)국보",
      "gen_meet_dt": "2024/04/26",
      "gen_meet_type": "정기총회",
      "agenda": "사내이사 선임",
      "vote_tot_qty": "    13691728"
    },
    {
      "record_date": "20240307",
      "sht_cd": "001140",
      "isin_name": "(주)국보",
      "gen_meet_dt": "2024/04/26",
      "gen_meet_type": "정기총회",
      "agenda": "감사선임",
      "vote_tot_qty": "    13691728"
    },
    {
      "record_date": "20240307",
      "sht_cd": "001140",
      "isin_name": "(주)국보",
      "gen_meet_dt": "2024/04/26",
      "gen_meet_type": "정기총회",
      "agenda": "이사 보수한도액 승인",
      "vote_tot_qty": "    13691728"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

