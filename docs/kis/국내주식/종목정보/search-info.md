# 상품기본조회[v1_국내주식-029]

> [국내주식] 종목정보



## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `00589d46-b8fe-4329-a20e-50dfe05f0d82` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/search-info` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTPF1604R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-28
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
| `tr_id` | 거래ID | String | 13 | Y | CTPF1604R |
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
| `PDNO` | 상품번호 | String | 12 | Y | '주식(하이닉스) :  000660 (코드 : 300) 선물(101S12) :  KR4101SC0009 (코드 : 301) 미국(AAPL) : AAPL (코드 : 512)' |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | '300 주식 301 선물옵션 302 채권 512  미국 나스닥 / 513  미국 뉴욕 / 529  미국 아멕스  515  일본 501  홍콩 / 543  홍콩CNY / 55... |

### 요청 예시

```json
{
  "PDNO": "AAPL",
  "PRDT_TYPE_CD": "512"
}
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
| `output` | 응답상세1 | String |   | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `prdt_name120` | 상품명120 | String | 120 | Y |  |
| `prdt_abrv_name` | 상품약어명 | String | 60 | Y |  |
| `prdt_eng_name` | 상품영문명 | String | 60 | Y |  |
| `prdt_eng_name120` | 상품영문명120 | String | 120 | Y |  |
| `prdt_eng_abrv_name` | 상품영문약어명 | String | 60 | Y |  |
| `std_pdno` | 표준상품번호 | String | 12 | Y |  |
| `shtn_pdno` | 단축상품번호 | String | 12 | Y |  |
| `prdt_sale_stat_cd` | 상품판매상태코드 | String | 2 | Y |  |
| `prdt_risk_grad_cd` | 상품위험등급코드 | String | 2 | Y |  |
| `prdt_clsf_cd` | 상품분류코드 | String | 6 | Y |  |
| `prdt_clsf_name` | 상품분류명 | String | 60 | Y |  |
| `sale_strt_dt` | 판매시작일자 | String | 8 | Y |  |
| `sale_end_dt` | 판매종료일자 | String | 8 | Y |  |
| `wrap_asst_type_cd` | 랩어카운트자산유형코드 | String | 2 | Y |  |
| `ivst_prdt_type_cd` | 투자상품유형코드 | String | 4 | Y |  |
| `ivst_prdt_type_cd_name` | 투자상품유형코드명 | String | 60 | Y |  |
| `frst_erlm_dt` | 최초등록일자 | String | 8 | Y |  |

### 응답 예시

```json
{
  "output": {
    "pdno": "AAPL",
    "prdt_type_cd": "512",
    "prdt_name": "애플",
    "prdt_name120": "애플",
    "prdt_abrv_name": "애플",
    "prdt_eng_name": "APPLE INC",
    "prdt_eng_name120": "APPLE INC",
    "prdt_eng_abrv_name": "APPLE INC",
    "std_pdno": "US0378331005",
    "shtn_pdno": "AAPL",
    "prdt_sale_stat_cd": "",
    "prdt_risk_grad_cd": "",
    "prdt_clsf_cd": "101210",
    "prdt_clsf_name": "해외주식",
    "sale_strt_dt": "",
    "sale_end_dt": "",
    "wrap_asst_type_cd": "06",
    "ivst_prdt_type_cd": "1012",
    "ivst_prdt_type_cd_name": "해외주식",
    "frst_erlm_dt": ""
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0530",
  "msg1": "조회되었습니다                                                                  "
}
```

