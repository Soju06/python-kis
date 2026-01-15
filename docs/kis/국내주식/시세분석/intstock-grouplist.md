# 관심종목 그룹조회 [국내주식-204]

> [국내주식] 시세분석

관심종목 그룹조회 API입니다.
① 관심종목 그룹조회 → ② 관심종목 그룹별 종목조회 → ③ 관심종목(멀티종목) 시세조회 순서대로 호출하셔서 관심종목 시세 조회 가능합니다.

※ 한 번의 호출에 최대 30종목의 시세 확인 가능합니다.

한국투자증권 Github 에서 관심종목 복수시세조회 파이썬 샘플코드를 참고하실 수 있습니다.
https://github.com/koreainvestment/open-trading-api/blob/main/rest/get_interest_stocks_price.py

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `6723d437-b275-4c10-b7fb-9ba788cad75e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/intstock-grouplist` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `HHKCM113004C7` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
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
| `tr_id` | 거래ID | String | 13 | Y | HHKCM113004C7 |
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
| `TYPE` | 관심종목구분코드                 | String | 1 | Y | Unique key(1) |
| `FID_ETC_CLS_CODE` | FID 기타 구분 코드  | String | 2 | Y | Unique key(00) |
| `USER_ID` | 사용자 ID                 | String | 16 | Y | HTS_ID 입력 |

### 요청 예시

```json
TYPE:1
FID_ETC_CLS_CODE:00
USER_ID:{{HTS_ID}}
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
| `output2` | 응답상세 | String |  | Y |  |
| `date` | 일자 | String | 8 | Y |  |
| `trnm_hour` | 전송 시간 | String | 6 | Y |  |
| `data_rank` | 데이터 순위      | String | 10 | Y |  |
| `inter_grp_code` | 관심 그룹 코드 | String | 3 | Y |  |
| `inter_grp_name` | 관심 그룹 명 | String | 40 | Y |  |
| `ask_cnt` | 요청 개수 | String | 4 | Y |  |

### 응답 예시

```json
{
  "output2": [
    {
      "date": "20230517",
      "trnm_hour": "171648",
      "data_rank": "0000000000",
      "inter_grp_code": "001",
      "inter_grp_name": "조건검색결과",
      "ask_cnt": "100"
    },
    {
      "date": "20240318",
      "trnm_hour": "133351",
      "data_rank": "0000000001",
      "inter_grp_code": "000",
      "inter_grp_name": "기본그룹1",
      "ask_cnt": "011"
    },
    {
      "date": "20240529",
      "trnm_hour": "090525",
      "data_rank": "0000000002",
      "inter_grp_code": "002",
      "inter_grp_name": "관심종목02",
      "ask_cnt": "022"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
