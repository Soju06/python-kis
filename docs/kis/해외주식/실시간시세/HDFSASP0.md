# 해외주식 실시간호가[실시간-021]

> [해외주식] 실시간시세

해외주식 실시간호가 API를 이용하여 미국 실시간 10호가(매수/매도) 시세가 무료로 제공됩니다. (미국은 유료시세 제공 X)

아시아 국가의 경우, HTS(efriend Plus) [7781] 시세신청(실시간) 화면에서 유료 서비스 신청 시, 
"해외주식 실시간호가 HDFSASP0" 을 이용하여 아시아국가 유료시세(실시간호가)를 받아보실 수 있습니다. (24.11.29 반영)
(아시아 국가 무료시세는 "해외주식 지연호가(아시아) HDFSASP1" 를 이용하시기 바랍니다.)

※ 미국 : 실시간 무료, 매수/매도 각 10호가 (0분지연, 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보)
※ 아시아(홍콩, 베트남, 중국, 일본) : 실시간 유료 (단, 중국은 HTS[7781]에서 실시간시세 무료로 신청 후 이용 가능)

해당 API로 미국주간거래(10:00~16:00) 시세 조회도 가능합니다.
※ 미국주간거래 실시간 조회 시, 맨 앞자리(R), tr_key 중 시장구분 값을 다음과 같이 입력 → 나스닥: BAQ, 뉴욕: BAY, 아멕스: BAA

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

​[미국주식시세 이용시 유의사항]

■ 무료 실시간 시세(나스닥 토탈뷰)를 별도 신청없이 제공하고 있으며, 유료 시세 서비스를 신청하시더라도 OpenAPI의 경우 무료 시세로만 제공하고있습니다. 
 
※ 무료(매수/매도 각 10호가) : 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보
※ 유료(매수/매도 각 1호가) : OpenAPI 서비스 미제공

■ 무료 실시간 시세 서비스는 유료 실시간 시세 서비스 대비 평균 50% 수준에 해당하는 정보이므로 현재가/호가/순간체결량/차트 등에서 일시적·부분적 차이가 
있을 수 있으며 이로 인해 발생하는 손실에 대해서 당사가 책임지지 않습니다.

■ 무료 실시간 시세 서비스의 시가, 저가, 고가, 종가는 유료 실시간 시세 서비스와 다를 수 있으며, 
종목별 과거 데이터(거래량, 시가, 종가, 고가, 차트 데이터 등)는 장 종료 후(오후 12시경) 유료 실시간 시세 서비스 데이터와 동일하게 업데이트됩니다.
(출처: 한국투자증권 외화증권 거래설명서 - https://securities.koreainvestment.com/main/customer/guide/Guide.jsp?&cmd=TF04ag010002¤tPage=1&num=64)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `19f840e8-d6be-4b68-94f5-9448a0c4f10b` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/HDFSASP0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HDFSASP0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-01-31
- **최종 수정일**: 2025-12-05

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | HDFSASP0 |
| `tr_key` | R거래소명종목코드 | String | 6 | Y | D+시장구분(3자리)+종목코드 예) DNASAAPL : D+NAS(나스닥)+AAPL(애플) [시장구분] NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스   R+시장구분... |

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
      "tr_id": "HDFSASP0",
      "tr_key": "RBAQAAPL"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `RSYM` | 실시간종목코드 | String | 16 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `SYMB` | 종목코드 | String | 16 | Y |  |
| `ZDIV` | 소숫점자리수 | String | 1 | Y |  |
| `XYMD` | 현지일자 | String | 8 | Y |  |
| `XHMS` | 현지시간 | String | 6 | Y |  |
| `KYMD` | 한국일자 | String | 8 | Y |  |
| `KHMS` | 한국시간 | String | 6 | Y |  |
| `BVOL` | 매수총잔량 | String | 10 | Y |  |
| `AVOL` | 매도총잔량 | String | 10 | Y |  |
| `BDVL` | 매수총잔량대비 | String | 10 | Y |  |
| `ADVL` | 매도총잔량대비 | String | 10 | Y |  |
| `PBID1` | 매수호가1 | String | 12 | Y |  |
| `PASK1` | 매도호가1 | String | 12 | Y |  |
| `VBID1` | 매수잔량1 | String | 10 | Y |  |
| `VASK1` | 매도잔량1 | String | 10 | Y |  |
| `DBID1` | 매수잔량대비1 | String | 10 | Y |  |
| `DASK1` | 매도잔량대비1 | String | 10 | Y |  |
| `PBID2` | 매수호가2 | String | 12 | Y |  |
| `PASK2` | 매도호가2 | String | 12 | Y |  |
| `VBID2` | 매수잔량2 | String | 10 | Y |  |
| `VASK2` | 매도잔량2 | String | 10 | Y |  |
| `DBID2` | 매수잔량대비2 | String | 10 | Y |  |
| `DASK2` | 매도잔량대비2 | String | 10 | Y |  |
| `PBID3` | 매수호가3 | String | 12 | Y |  |
| `PASK3` | 매도호가3 | String | 12 | Y |  |
| `VBID3` | 매수잔량3 | String | 10 | Y |  |
| `VASK3` | 매도잔량3 | String | 10 | Y |  |
| `DBID3` | 매수잔량대비3 | String | 10 | Y |  |
| `DASK3` | 매도잔량대비3 | String | 10 | Y |  |
| `PBID3` | 매수호가3 | String | 12 | Y |  |
| `PASK3` | 매도호가3 | String | 12 | Y |  |
| `VBID3` | 매수잔량3 | String | 10 | Y |  |
| `VASK3` | 매도잔량3 | String | 10 | Y |  |
| `DBID3` | 매수잔량대비3 | String | 10 | Y |  |
| `DASK3` | 매도잔량대비3 | String | 10 | Y |  |
| `PBID4` | 매수호가4 | String | 12 | Y |  |
| `PASK4` | 매도호가4 | String | 12 | Y |  |
| `VBID4` | 매수잔량4 | String | 10 | Y |  |
| `VASK4` | 매도잔량4 | String | 10 | Y |  |
| `DBID4` | 매수잔량대비4 | String | 10 | Y |  |
| `DASK4` | 매도잔량대비4 | String | 10 | Y |  |
| `PBID5` | 매수호가5 | String | 12 | Y |  |
| `PASK5` | 매도호가5 | String | 12 | Y |  |
| `VBID5` | 매수잔량5 | String | 10 | Y |  |
| `VASK5` | 매도잔량5 | String | 10 | Y |  |
| `DBID5` | 매수잔량대비5 | String | 10 | Y |  |
| `DASK5` | 매도잔량대비5 | String | 10 | Y |  |
| `PBID6` | 매수호가6 | String | 12 | Y |  |
| `PASK6` | 매도호가6 | String | 12 | Y |  |
| `VBID6` | 매수잔량6 | String | 10 | Y |  |
| `VASK6` | 매도잔량6 | String | 10 | Y |  |
| `DBID6` | 매수잔량대비6 | String | 10 | Y |  |
| `DASK6` | 매도잔량대비6 | String | 10 | Y |  |
| `PBID7` | 매수호가7 | String | 12 | Y |  |
| `PASK7` | 매도호가7 | String | 12 | Y |  |
| `VBID7` | 매수잔량7 | String | 10 | Y |  |
| `VASK7` | 매도잔량7 | String | 10 | Y |  |
| `DBID7` | 매수잔량대비7 | String | 10 | Y |  |
| `DASK7` | 매도잔량대비7 | String | 10 | Y |  |
| `PBID8` | 매수호가8 | String | 12 | Y |  |
| `PASK8` | 매도호가8 | String | 12 | Y |  |
| `VBID8` | 매수잔량8 | String | 10 | Y |  |
| `VASK8` | 매도잔량8 | String | 10 | Y |  |
| `DBID8` | 매수잔량대비8 | String | 10 | Y |  |
| `DASK8` | 매도잔량대비8 | String | 10 | Y |  |
| `PBID9` | 매수호가9 | String | 12 | Y |  |
| `PASK9` | 매도호가9 | String | 12 | Y |  |
| `VBID9` | 매수잔량9 | String | 10 | Y |  |
| `VASK9` | 매도잔량9 | String | 10 | Y |  |
| `DBID9` | 매수잔량대비9 | String | 10 | Y |  |
| `DASK9` | 매도잔량대비9 | String | 10 | Y |  |
| `PBID10` | 매수호가10 | String | 12 | Y |  |
| `PASK10` | 매도호가10 | String | 12 | Y |  |
| `VBID10` | 매수잔량10 | String | 10 | Y |  |
| `VASK10` | 매도잔량10 | String | 10 | Y |  |
| `DBID10` | 매수잔량대비10 | String | 10 | Y |  |
| `DASK10` | 매도잔량대비10 | String | 10 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "HDFSASP0", 
        "tr_key": "RBAQAAPL", 
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
0|HDFSASP0|001|RBAQAAPL^AAPL^4^20240506^202223^20240507^092223^1482^381^0^-10^182.8500^182.8700^350^57^0^-10^182.8400^182.9000^1^10^0^0^182.8300^182.9100^6^54^0^0^182.7900^182.9500^54^5^0^0^182.7500^182.9600^309^3^0^0^182.7300^182.9700^20^81^0^0^182.7000^182.9800^124^3^0^0^182.6600^182.9900^397^1^0^0^182.6500^183.0000^20^69^0^0^182.6300^183.0100^201^98^0^0
```

