# 해외결제일자조회[해외주식-017]

> [해외주식] 기본시세

해외결제일자조회 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1394ba1d-e17d-42c8-8e53-6bed5dce7588` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/quotations/countries-holiday` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `CTOS5011R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-12-23
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTOS5011R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | N | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `TRAD_DT` | 기준일자 | String | 8 | Y | 기준일자(YYYYMMDD) |
| `CTX_AREA_NK` | 연속조회키 | String | 20 | Y | 공백으로 입력 |
| `CTX_AREA_FK` | 연속조회검색조건 | String | 20 | Y | 공백으로 입력 |

### 요청 예시

```json
{
  "TRAD_DT": "20221227",
  "CTX_AREA_NK": "",
  "CTX_AREA_FK": ""
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
| `output` | 응답상세1 | String |   | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y | 512  미국 나스닥 / 513  미국 뉴욕거래소 / 529  미국 아멕스  515  일본 501  홍콩 / 543  홍콩CNY / 558  홍콩USD 507  베트남 하노이... |
| `tr_natn_cd` | 거래국가코드 | String | 3 | Y | 840 미국 / 392 일본 / 344 홍콩 704 베트남 / 156 중국 |
| `tr_natn_name` | 거래국가명 | String | 60 | Y |  |
| `natn_eng_abrv_cd` | 국가영문약어코드 | String | 2 | Y | US 미국 / JP 일본 / HK 홍콩 VN 베트남 / CN 중국 |
| `tr_mket_cd` | 거래시장코드 | String | 2 | Y |  |
| `tr_mket_name` | 거래시장명 | String | 60 | Y |  |
| `acpl_sttl_dt` | 현지결제일자 | String | 8 | Y | 현지결제일자(YYYYMMDD) |
| `dmst_sttl_dt` | 국내결제일자 | String | 8 | Y | 국내결제일자(YYYYMMDD) |

### 응답 예시

```json
{
  "ctx_area_fk": "20221227            ",
  "ctx_area_nk": "                    ",
  "output": [
    {
      "prdt_type_cd": "507",
      "tr_natn_cd": "704",
      "tr_natn_name": "베트남",
      "natn_eng_abrv_cd": "VN",
      "tr_mket_cd": "01",
      "tr_mket_name": "하노이거래소",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221229"
    },
    {
      "prdt_type_cd": "508",
      "tr_natn_cd": "704",
      "tr_natn_name": "베트남",
      "natn_eng_abrv_cd": "VN",
      "tr_mket_cd": "02",
      "tr_mket_name": "호치민거래소",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221229"
    },
    {
      "prdt_type_cd": "512",
      "tr_natn_cd": "840",
      "tr_natn_name": "미국",
      "natn_eng_abrv_cd": "US",
      "tr_mket_cd": "01",
      "tr_mket_name": "나스닥",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221230"
    },
    {
      "prdt_type_cd": "513",
      "tr_natn_cd": "840",
      "tr_natn_name": "미국",
      "natn_eng_abrv_cd": "US",
      "tr_mket_cd": "02",
      "tr_mket_name": "뉴욕거래소",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221230"
    },
    {
      "prdt_type_cd": "515",
      "tr_natn_cd": "392",
      "tr_natn_name": "일본",
      "natn_eng_abrv_cd": "JP",
      "tr_mket_cd": "01",
      "tr_mket_name": "일본",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221229"
    },
    {
      "prdt_type_cd": "527",
      "tr_natn_cd": "840",
      "tr_natn_name": "미국",
      "natn_eng_abrv_cd": "US",
      "tr_mket_cd": "03",
      "tr_mket_name": "미국",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221230"
    },
    {
      "prdt_type_cd": "528",
      "tr_natn_cd": "840",
      "tr_natn_name": "미국",
      "natn_eng_abrv_cd": "US",
      "tr_mket_cd": "04",
      "tr_mket_name": "미국",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221230"
    },
    {
      "prdt_type_cd": "529",
      "tr_natn_cd": "840",
      "tr_natn_name": "미국",
      "natn_eng_abrv_cd": "US",
      "tr_mket_cd": "05",
      "tr_mket_name": "아멕스",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221230"
    },
    {
      "prdt_type_cd": "556",
      "tr_natn_cd": "704",
      "tr_natn_name": "베트남",
      "natn_eng_abrv_cd": "VN",
      "tr_mket_cd": "03",
      "tr_mket_name": "업콤거래소",
      "acpl_sttl_dt": "20221229",
      "dmst_sttl_dt": "20221229"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
