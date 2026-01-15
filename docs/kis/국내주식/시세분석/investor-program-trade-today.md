# 프로그램매매 투자자매매동향(당일) [국내주식-116]

> [국내주식] 시세분석

프로그램매매 투자자매매동향(당일) API입니다.
한국투자 HTS(eFriend Plus) > [0466] 프로그램매매 투자자별 동향 화면 의 "당일동향" 표의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `b664e9df-7ab6-4b89-89a0-5537ae380caf` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/investor-program-trade-today` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `HHPPG046600C1` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
- **최종 수정일**: 2025-06-09

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | '※ 구TR은 사전고지 없이 막힐 수 있으므로 반드시 신TR로 변경이용 부탁드립니다. [실전투자] (구)HHPPG046600C0 → (신)HHPPG046600C1' |
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
| `EXCH_DIV_CLS_CODE` | 거래소 구분 코드 | String | 2 | Y | J : KRX, NX : NXT, UN : 통합 |
| `MRKT_DIV_CLS_CODE` | 시장 구분 코드 | String | 1 | Y | 1:코스피, 4:코스닥 |

### 요청 예시

```json
MRKT_DIV_CLS_CODE:1
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
| `invr_cls_code` | 투자자코드 | String | 4 | Y |  |
| `all_seln_qty` | 전체매도수량 | String | 18 | Y |  |
| `all_seln_amt` | 전체매도대금 | String | 18 | Y |  |
| `invr_cls_name` | 투자자 구분 명 | String | 20 | Y |  |
| `all_shnu_qty` | 전체매수수량 | String | 18 | Y |  |
| `all_shnu_amt` | 전체매수대금 | String | 18 | Y |  |
| `all_ntby_amt` | 전체순매수대금 | String | 12 | Y |  |
| `arbt_seln_qty` | 차익매도수량 | String | 18 | Y |  |
| `all_ntby_qty` | 전체순매수수량 | String | 12 | Y |  |
| `arbt_shnu_qty` | 차익매수수량 | String | 18 | Y |  |
| `arbt_ntby_qty` | 차익순매수수량 | String | 12 | Y |  |
| `arbt_seln_amt` | 차익매도대금 | String | 18 | Y |  |
| `arbt_shnu_amt` | 차익매수대금 | String | 18 | Y |  |
| `arbt_ntby_amt` | 차익순매수대금 | String | 12 | Y |  |
| `nabt_seln_qty` | 비차익매도수량 | String | 18 | Y |  |
| `nabt_shnu_qty` | 비차익매수수량 | String | 18 | Y |  |
| `nabt_ntby_qty` | 비차익순매수수량 | String | 12 | Y |  |
| `nabt_seln_amt` | 비차익매도대금 | String | 18 | Y |  |
| `nabt_shnu_amt` | 비차익매수대금 | String | 18 | Y |  |
| `nabt_ntby_amt` | 비차익순매수대금 | String | 12 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "invr_cls_code": "7100",
      "invr_cls_name": "기 타",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "0",
      "arbt_ntby_qty": "0",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "0",
      "arbt_ntby_amt": "0",
      "nabt_seln_qty": "289",
      "nabt_shnu_qty": "242",
      "nabt_ntby_qty": "-47",
      "nabt_seln_amt": "7151",
      "nabt_shnu_amt": "4006",
      "nabt_ntby_amt": "-3145",
      "all_seln_qty": "289",
      "all_shnu_qty": "242",
      "all_ntby_qty": "-47",
      "all_seln_amt": "7151",
      "all_shnu_amt": "4006",
      "all_ntby_amt": "-3145"
    },
    {
      "invr_cls_code": "6000",
      "invr_cls_name": "연기금등",
      "arbt_seln_qty": "440",
      "arbt_shnu_qty": "410",
      "arbt_ntby_qty": "-29",
      "arbt_seln_amt": "27863",
      "arbt_shnu_amt": "25971",
      "arbt_ntby_amt": "-1891",
      "nabt_seln_qty": "608",
      "nabt_shnu_qty": "474",
      "nabt_ntby_qty": "-134",
      "nabt_seln_amt": "16795",
      "nabt_shnu_amt": "23282",
      "nabt_ntby_amt": "6486",
      "all_seln_qty": "1049",
      "all_shnu_qty": "885",
      "all_ntby_qty": "-164",
      "all_seln_amt": "44658",
      "all_shnu_amt": "49253",
      "all_ntby_amt": "4595"
    },
    {
      "invr_cls_code": "5000",
      "invr_cls_name": "기타금융",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "0",
      "arbt_ntby_qty": "0",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "0",
      "arbt_ntby_amt": "0",
      "nabt_seln_qty": "0",
      "nabt_shnu_qty": "0",
      "nabt_ntby_qty": "0",
      "nabt_seln_amt": "0",
      "nabt_shnu_amt": "20",
      "nabt_ntby_amt": "20",
      "all_seln_qty": "0",
      "all_shnu_qty": "0",
      "all_ntby_qty": "0",
      "all_seln_amt": "0",
      "all_shnu_amt": "20",
      "all_ntby_amt": "20"
    },
    {
      "invr_cls_code": "2000",
      "invr_cls_name": "보 험",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "0",
      "arbt_ntby_qty": "0",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "0",
      "arbt_ntby_amt": "0",
      "nabt_seln_qty": "211",
      "nabt_shnu_qty": "110",
      "nabt_ntby_qty": "-101",
      "nabt_seln_amt": "12580",
      "nabt_shnu_amt": "6296",
      "nabt_ntby_amt": "-6283",
      "all_seln_qty": "211",
      "all_shnu_qty": "110",
      "all_ntby_qty": "-101",
      "all_seln_amt": "12580",
      "all_shnu_amt": "6296",
      "all_ntby_amt": "-6283"
    },
    {
      "invr_cls_code": "4000",
      "invr_cls_name": "은 행",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "0",
      "arbt_ntby_qty": "0",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "0",
      "arbt_ntby_amt": "0",
      "nabt_seln_qty": "28",
      "nabt_shnu_qty": "65",
      "nabt_ntby_qty": "36",
      "nabt_seln_amt": "563",
      "nabt_shnu_amt": "851",
      "nabt_ntby_amt": "288",
      "all_seln_qty": "28",
      "all_shnu_qty": "65",
      "all_ntby_qty": "36",
      "all_seln_amt": "563",
      "all_shnu_amt": "851",
      "all_ntby_amt": "288"
    },
    {
      "invr_cls_code": "3100",
      "invr_cls_name": "사 모",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "0",
      "arbt_ntby_qty": "0",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "0",
      "arbt_ntby_amt": "0",
      "nabt_seln_qty": "303",
      "nabt_shnu_qty": "181",
      "nabt_ntby_qty": "-121",
      "nabt_seln_amt": "12440",
      "nabt_shnu_amt": "8092",
      "nabt_ntby_amt": "-4348",
      "all_seln_qty": "303",
      "all_shnu_qty": "181",
      "all_ntby_qty": "-121",
      "all_seln_amt": "12440",
      "all_shnu_amt": "8092",
      "all_ntby_amt": "-4348"
    },
    {
      "invr_cls_code": "3000",
      "invr_cls_name": "투 신",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "0",
      "arbt_ntby_qty": "0",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "0",
      "arbt_ntby_amt": "0",
      "nabt_seln_qty": "764",
      "nabt_shnu_qty": "806",
      "nabt_ntby_qty": "41",
      "nabt_seln_amt": "41009",
      "nabt_shnu_amt": "38826",
      "nabt_ntby_amt": "-2183",
      "all_seln_qty": "764",
      "all_shnu_qty": "806",
      "all_ntby_qty": "41",
      "all_seln_amt": "41009",
      "all_shnu_amt": "38826",
      "all_ntby_amt": "-2183"
    },
    {
      "invr_cls_code": "1000",
      "invr_cls_name": "금융투자",
      "arbt_seln_qty": "445",
      "arbt_shnu_qty": "2",
      "arbt_ntby_qty": "-443",
      "arbt_seln_amt": "28429",
      "arbt_shnu_amt": "143",
      "arbt_ntby_amt": "-28285",
      "nabt_seln_qty": "98",
      "nabt_shnu_qty": "70",
      "nabt_ntby_qty": "-27",
      "nabt_seln_amt": "5176",
      "nabt_shnu_amt": "6003",
      "nabt_ntby_amt": "826",
      "all_seln_qty": "543",
      "all_shnu_qty": "72",
      "all_ntby_qty": "-470",
      "all_seln_amt": "33605",
      "all_shnu_amt": "6146",
      "all_ntby_amt": "-27459"
    },
    {
      "invr_cls_code": "8888",
      "invr_cls_name": "기 관",
      "arbt_seln_qty": "885",
      "arbt_shnu_qty": "413",
      "arbt_ntby_qty": "-472",
      "arbt_seln_amt": "56292",
      "arbt_shnu_amt": "26114",
      "arbt_ntby_amt": "-30177",
      "nabt_seln_qty": "2014",
      "nabt_shnu_qty": "1709",
      "nabt_ntby_qty": "-305",
      "nabt_seln_amt": "88565",
      "nabt_shnu_amt": "83373",
      "nabt_ntby_amt": "-5192",
      "all_seln_qty": "2900",
      "all_shnu_qty": "2122",
      "all_ntby_qty": "-778",
      "all_seln_amt": "144858",
      "all_shnu_amt": "109487",
      "all_ntby_amt": "-35370"
    },
    {
      "invr_cls_code": "8000",
      "invr_cls_name": "개 인",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "0",
      "arbt_ntby_qty": "0",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "0",
      "arbt_ntby_amt": "0",
      "nabt_seln_qty": "683",
      "nabt_shnu_qty": "528",
      "nabt_ntby_qty": "-154",
      "nabt_seln_amt": "16867",
      "nabt_shnu_amt": "9496",
      "nabt_ntby_amt": "-7371",
      "all_seln_qty": "683",
      "all_shnu_qty": "528",
      "all_ntby_qty": "-154",
      "all_seln_amt": "16867",
      "all_shnu_amt": "9496",
      "all_ntby_amt": "-7371"
    },
    {
      "invr_cls_code": "9100",
      "invr_cls_name": "외국인",
      "arbt_seln_qty": "0",
      "arbt_shnu_qty": "57",
      "arbt_ntby_qty": "57",
      "arbt_seln_amt": "0",
      "arbt_shnu_amt": "4321",
      "arbt_ntby_amt": "4321",
      "nabt_seln_qty": "88573",
      "nabt_shnu_qty": "73539",
      "nabt_ntby_qty": "-15034",
      "nabt_seln_amt": "2640145",
      "nabt_shnu_amt": "1983063",
      "nabt_ntby_amt": "-657082",
      "all_seln_qty": "88573",
      "all_shnu_qty": "73596",
      "all_ntby_qty": "-14976",
      "all_seln_amt": "2640145",
      "all_shnu_amt": "1987384",
      "all_ntby_amt": "-652761"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

