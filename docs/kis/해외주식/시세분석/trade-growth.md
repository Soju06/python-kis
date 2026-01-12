# 해외주식 거래증가율순위[해외주식-045]

> [해외주식] 시세분석

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `05980ed5-8ab1-471a-975c-3e129841cbb8` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/ranking/trade-growth` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `HHDFS76330000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
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
| `tr_id` | 거래ID | String | 13 | Y | HHDFS76330000 |
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
| `KEYB` | NEXT KEY BUFF | String | 8 | Y | 공백 |
| `AUTH` | 사용자권한정보 | String | 32 | Y | 공백 |
| `EXCD` | 거래소코드 | String | 4 | Y | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 ' |
| `NDAY` | N일자값 | String | 1 | Y | N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년) |
| `VOL_RANG` | 거래량조건 | String | 1 | Y | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상) |

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
| `msg1` | 응답메시지 | String | 80 | Y |  |
| `output1` | 응답상세 | String |  | Y |  |
| `zdiv` | 소수점자리수 | String | 1 | Y |  |
| `stat` | 거래상태정보 | String | 20 | Y |  |
| `crec` | 현재조회종목수 | String | 6 | Y |  |
| `trec` | 전체조회종목수 | String | 6 | Y |  |
| `nrec` | RecordCount | String | 4 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `rsym` | 실시간조회심볼 | String | 16 | Y |  |
| `excd` | 거래소코드 | String | 4 | Y |  |
| `symb` | 종목코드 | String | 1 | Y |  |
| `name` | 종목명 | String | 48 | Y |  |
| `last` | 현재가 | String | 16 | Y |  |
| `sign` | 기호 | String | 1 | Y |  |
| `diff` | 대비 | String | 12 | Y |  |
| `rate` | 등락율 | String | 12 | Y |  |
| `pask` | 매도호가 | String | 12 | Y |  |
| `pbid` | 매수호가 | String | 12 | Y |  |
| `tvol` | 거래량 | String | 14 | Y |  |
| `n_tvol` | 평균거래량 | String | 14 | Y |  |
| `n_rate` | 증가율 | String | 12 | Y |  |
| `rank` | 순위 | String | 6 | Y |  |
| `ename` | 영문종목명 | String | 48 | Y |  |
| `e_ordyn` | 매매가능 | String | 2 | Y |  |
