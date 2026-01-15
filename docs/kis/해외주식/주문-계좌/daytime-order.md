# 해외주식 미국주간주문[v1_해외주식-026]

> [해외주식] 주문/계좌

해외주식 미국주간주문 API입니다.

* 미국주식 주간거래 시 아래 참고 부탁드립니다.
. 포럼 > FAQ > 미국주식 주간거래 시 어떤 API를 사용해야 하나요?

* 미국주간거래의 경우, 모든 미국 종목 매매가 지원되지 않습니다. 일부 종목만 매매 가능한 점 유의 부탁드립니다.

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

* 미국주간거래시간 외 API 호출 시 에러가 발생하오니 운영시간을 확인해주세요.
. 주간거래(장전거래)(한국시간 기준) : 10:00 ~ 18:00 (Summer Time 동일)

* 한국투자증권 해외주식 시장별 매매안내(매매수수료, 거래시간 안내, 결제일 정보, 환전안내)
   https://securities.koreainvestment.com/main/bond/research/_static/TF03ca050000.jsp

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `9efc47d7-58ec-4f9e-8068-37795580fe67` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/overseas-stock/v1/trading/daytime-order` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `(주간매수) TTTS6036U (주간매도) TTTS6037U` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-03-17
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] 미국주간매수 : TTTS6036U 미국주간매도 : TTTS6037U |
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
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | NASD:나스닥 / NYSE:뉴욕 / AMEX:아멕스 |
| `PDNO` | 상품번호 | String | 12 | Y | 종목코드 |
| `ORD_QTY` | 주문수량 | String | 10 | Y | 해외거래소 별 최소 주문수량 및 주문단위 확인 필요 |
| `OVRS_ORD_UNPR` | 해외주문단가 | String | 32 | Y | 소수점 포함, 1주당 가격 * 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 |
| `CTAC_TLNO` | 연락전화번호 | String | 20 | N | " " |
| `MGCO_APTM_ODNO` | 운용사지정주문번호 | String | 12 | N | " " |
| `ORD_SVR_DVSN_CD` | 주문서버구분코드 | String | 1 | Y | "0" |
| `ORD_DVSN` | 주문구분 | String | 2 | Y | [미국 매수/매도 주문]  00 : 지정가  * 주간거래는 지정가만 가능 |

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | String |   | N |  |
| `KRX_FWDG_ORD_ORGNO` | 한국거래소전송주문조직번호 | String | 5 | Y | 주문시 한국투자증권 시스템에서 지정된 영업점코드 |
| `ODNO` | 주문번호 | String | 10 | Y | 주문시 한국투자증권 시스템에서 채번된 주문번호 |
| `ORD_TMD` | 주문시각 | String | 6 | Y | 주문시각(시분초HHMMSS) |

