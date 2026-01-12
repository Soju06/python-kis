# 종목조건검색 목록조회[국내주식-038]

> [국내주식] 시세분석

HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API입니다.
종목조건검색 목록조회 API(/uapi/domestic-stock/v1/quotations/psearch-title)의 output인 'seq'을 종목조건검색조회 API(/uapi/domestic-stock/v1/quotations/psearch-result)의 input으로 사용하시면 됩니다.

※ 시스템 안정성을 위해 API로 제공되는 조건검색 결과의 경우 조건당 100건으로 제한을 둔 점 양해 부탁드립니다.

※ [0110] 화면의 '대상변경' 설정사항은 HTS [0110] 사용자 조건검색 화면에만 적용됨에 유의 부탁드립니다.

※ '조회가 계속 됩니다. (다음을 누르십시오.)' 오류 발생 시 해결방법
→ HTS(efriend Plus) [0110] 조건검색 화면에서 조건을 등록하신 후, 왼쪽 하단의 "사용자조건 서버저장" 클릭하셔서 등록한 조건들을 서버로 보낸 후 다시 API 호출 시도 부탁드립니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `24413e7f-cca6-4ab4-8598-b9d4e2d4305d` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/psearch-title` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `HHKST03900300` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-03-31
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
| `tr_id` | 거래ID | String | 13 | Y | HHKST03900300 |
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
| `user_id` | 사용자 HTS ID | String | 40 | Y |  |

### 요청 예시

```json
{
  "user_id": "abcd9876"
}
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
| `output2` | 응답상세 | Object |   | Y | Array |
| `user_id` | HTS ID | String | 40 | Y |  |
| `seq` | 조건키값 | String | 10 | Y | 해당 값을 종목조건검색조회 API의 input으로 사용 (0번부터 시작) |
| `grp_nm` | 그룹명 | String | 40 | Y | HTS(eFriend Plus) [0110] "사용자조건검색"화면을 통해 등록한 사용자조건 그룹 |
| `condition_nm` | 조건명 | String | 40 | Y | 등록한 사용자 조건명 |

### 응답 예시

```json
{
  "output2": [
    {
      "user_id": "abcd9876",
      "seq": "0",
      "grp_nm": "임시그룹",
      "condition_nm": "RSI전략1_14_9_PER_부채비율"
    },
    {
      "user_id": "abcd9876",
      "seq": "1",
      "grp_nm": "임시그룹",
      "condition_nm": "모멘텀전략1_5_3_PER_부채비율"
    },
    {
      "user_id": "abcd9876",
      "seq": "2",
      "grp_nm": "임시그룹",
      "condition_nm": "외국계거래량_10000이상_PER_부채비율"
    },
    {
      "user_id": "abcd9876",
      "seq": "3",
      "grp_nm": "임시그룹",
      "condition_nm": "이평전략1_5_20_PER_부채비율"
    },
    {
      "user_id": "abcd9876",
      "seq": "4",
      "grp_nm": "임시그룹",
      "condition_nm": "이평전략2_5_20_PER_부채비율"
    },
    {
      "user_id": "abcd9876",
      "seq": "5",
      "grp_nm": "임시그룹",
      "condition_nm": "테스트3"
    },
    {
      "user_id": "abcd9876",
      "seq": "6",
      "grp_nm": "임시그룹",
      "condition_nm": "테트스"
    },
    {
      "user_id": "abcd9876",
      "seq": "7",
      "grp_nm": "임시그룹",
      "condition_nm": "테트스2"
    },
    {
      "user_id": "abcd9876",
      "seq": "8",
      "grp_nm": "임시그룹",
      "condition_nm": "투자경고제외"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
