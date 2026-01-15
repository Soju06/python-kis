# 국내지수 실시간체결 [실시간-026]

> [국내주식] 실시간시세

[참고자료]
실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

[호출 데이터]
헤더와 바디 값을 합쳐 JSON 형태로 전송합니다.

[응답 데이터]
1. 정상 등록 여부 (JSON)
- JSON["body"]["msg1"] - 정상 응답 시, SUBSCRIBE SUCCESS
- JSON["body"]["output"]["iv"] - 실시간 결과 복호화에 필요한 AES256 IV (Initialize Vector)
- JSON["body"]["output"]["key"] - 실시간 결과 복호화에 필요한 AES256 Key

2. 실시간 결과 응답 ( | 로 구분되는 값)
ex) 0|H0STCNT0|004|005930^123929^73100^5^...
- 암호화 유무 : 0 암호화 되지 않은 데이터 / 1 암호화된 데이터
- TR_ID : 등록한 tr_id (ex. H0STCNT0)
- 데이터 건수 : (ex. 001 인 경우 데이터 건수 1건, 004인 경우 데이터 건수 4건)
- 응답 데이터 : 아래 response 데이터 참조 ( ^로 구분됨)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `914eb98d-8dd7-42a1-8f9d-da73f4a61ae7` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0UPCNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0UPCNT0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | H0UPCNT0 |
| `tr_key` | 종목코드 | String | 6 | Y | 업종구분코드 |

### 요청 예시

```json
{
  "header": {
    "approval_key": "35xxxxxa-bxxa-4xxb-87xxx-f56xxxxxxxxxx",
    "custtype": "P",
    "tr_type": "1",
    "content-type": "utf-8"
  },
  "body": {
    "input": {
      "tr_id": "H0UPCNT0",
      "tr_key": "0001"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `bsop_hour` | 영업 시간 | String | 6 | Y |  |
| `prpr_nmix` | 현재가 지수 | String | 1 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 1 | Y |  |
| `acml_vol` | 누적 거래량 | String | 1 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 1 | Y |  |
| `pcas_vol` | 건별 거래량 | String | 1 | Y |  |
| `pcas_tr_pbmn` | 건별 거래 대금 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 1 | Y |  |
| `oprc_nmix` | 시가 지수 | String | 1 | Y |  |
| `nmix_hgpr` | 지수 최고가 | String | 1 | Y |  |
| `nmix_lwpr` | 지수 최저가 | String | 1 | Y |  |
| `oprc_vrss_nmix_prpr` | 시가 대비 지수 현재가 | String | 1 | Y |  |
| `oprc_vrss_nmix_sign` | 시가 대비 지수 부호 | String | 1 | Y |  |
| `hgpr_vrss_nmix_prpr` | 최고가 대비 지수 현재가 | String | 1 | Y |  |
| `hgpr_vrss_nmix_sign` | 최고가 대비 지수 부호 | String | 1 | Y |  |
| `lwpr_vrss_nmix_prpr` | 최저가 대비 지수 현재가 | String | 1 | Y |  |
| `lwpr_vrss_nmix_sign` | 최저가 대비 지수 부호 | String | 1 | Y |  |
| `prdy_clpr_vrss_oprc_rate` | 전일 종가 대비 시가2 비율 | String | 1 | Y |  |
| `prdy_clpr_vrss_hgpr_rate` | 전일 종가 대비 최고가 비율 | String | 1 | Y |  |
| `prdy_clpr_vrss_lwpr_rate` | 전일 종가 대비 최저가 비율 | String | 1 | Y |  |
| `uplm_issu_cnt` | 상한 종목 수 | String | 1 | Y |  |
| `ascn_issu_cnt` | 상승 종목 수 | String | 1 | Y |  |
| `stnr_issu_cnt` |   보합 종목 수 | String | 1 | Y |  |
| `down_issu_cnt` | 하락 종목 수 | String | 1 | Y |  |
| `lslm_issu_cnt` |   하한 종목 수 | String | 1 | Y |  |
| `qtqt_ascn_issu_cnt` | 기세 상승 종목수 | String | 1 | Y |  |
| `qtqt_down_issu_cnt` | 기세 하락 종목수 | String | 1 | Y |  |
| `tick_vrss` | TICK대비 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0UPCNT0", 
        "tr_key": "0001", 
        "encrypt": "N"
        }, 
    "body": {
        "rt_cd": "0", 
        "msg_cd": "OPSP0000",
        "msg1": "SUBSCRIBE SUCCESS", 
        "output": {
            "iv": "0123456789abcdef", 
            "key": "abcdefghijklmnopabcdefghijklmnop"}
        }
}

# output
0|H0UPCNT0|001|0001^091240^2624.54^2^32.68^63952^1650684^439^10335^1.26^2615
.72^2624.82^2610.00^23.86^2^32.96^2^18.14^2^0.92^1.27^0.70^0^670^72^177^0^0^0^19
```

