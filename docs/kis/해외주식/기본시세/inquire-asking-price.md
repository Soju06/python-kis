# 해외주식 현재가 호가 [해외주식-033]

> [해외주식] 기본시세

해외주식 현재가 호가 API입니다.
미국 거래소는 10호가, 그 외 국가 거래소는 1호가만 제공됩니다.  
한국투자 HTS(eFriend Plus) > [7620] 해외주식 현재가 화면에서 "왼쪽 호가 창" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 지연시세 지연시간 : 미국 - 실시간무료(0분 지연, 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보)
                                홍콩, 베트남, 중국, 일본 - 15분지연
   미국의 경우 0분 지연 시세로 제공되나, 장중 당일 시가는 상이할 수 있으며, 익일 정정 표시됩니다.

※ 2024년 12월 13일(금) 오후 5시부터 HTS(efriend Plus) [7781] 시세신청(실시간) 화면에서 유료 서비스 신청 후 접근토큰 발급하면 최대 2시간 이후 실시간 유료 시세 수신 가능

※ 미국주식 시세의 경우 주간거래시간을 제외한 정규장, 애프터마켓, 프리마켓 시간대에 동일한 API(TR)로 시세 조회가 되는 점 유의 부탁드립니다.

[미국주식시세 이용시 유의사항]
■ 무료 실시간 시세(나스닥 토탈뷰)를 별도 신청없이 제공하고 있으며, 유료 시세 서비스를 신청하시더라도 OpenAPI의 경우 무료 시세로만 제공하고있습니다.
※ 무료(매수/매도 각 10호가) : 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보
※ 유료(매수/매도 각 1호가) : OpenAPI 서비스 미제공
■ 무료 실시간 시세 서비스는 유료 실시간 시세 서비스 대비 평균 50% 수준에 해당하는 정보이므로 현재가/호가/순간체결량/차트 등에서 일시적·부분적 차이가 있을 수 있습니다. 
■ 무료 실시간 시세 서비스의 시가, 저가, 고가, 종가는 타 매체의 유료 실시간 시세 서비스와 다를 수 있으며, 이로 인해 발생하는 손실에 대해서 당사가 책임지지 않습니다.
    이용에 유의 부탁드립니다.

(출처: 한국투자증권 외화증권 거래설명서 - https://www.truefriend.com/main/customer/guide/Guide.jsp?&cmd=TF04ag010002¤tPage=1&num=64)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ed60877a-6183-433a-9a8c-ef56ed9bc679` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/inquire-asking-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `HHDFS76200100` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19
- **최종 수정일**: 2025-12-05

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFS76200100 |
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
| `AUTH` | 사용자권한정보 | String | 32 | Y | 공백 |
| `EXCD` | 거래소코드 | String | 4 | Y | NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스  HKS : 홍콩 SHS : 상해  SZS : 심천 HSX : 호치민 HNX : 하노이 TSE : 도쿄  BAY : 뉴욕(... |
| `SYMB` | 종목코드 | String | 16 | Y | 종목코드 예)TSLA |

### 요청 예시

```json
AUTH:
EXCD:NAS
SYMB:TSLA
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
| `output1` | 응답상세 | String | 100 | Y |  |
| `rsym` | 실시간조회종목코드 | String | 16 | Y |  |
| `zdiv` | 소수점자리수 | String | 1 | Y |  |
| `curr` | 통화 | String | 4 | Y |  |
| `base` | 전일종가 | String | 12 | Y |  |
| `open` | 시가 | String | 12 | Y |  |
| `high` | 고가 | String | 12 | Y |  |
| `low` | 저가 | String | 12 | Y |  |
| `last` | 현재가 | String | 12 | Y |  |
| `dymd` | 호가일자 | String | 8 | Y |  |
| `dhms` | 호가시간 | String | 6 | Y |  |
| `bvol` | 매수호가총잔량 | String | 10 | Y |  |
| `avol` | 매도호가총잔량 | String | 10 | Y |  |
| `bdvl` | 매수호가총잔량대비 | String | 10 | Y |  |
| `advl` | 매도호가총잔량대비 | String | 10 | Y |  |
| `code` | 종목코드 | String | 16 | Y |  |
| `ropen` | 시가율 | String | 12 | Y |  |
| `rhigh` | 고가율 | String | 12 | Y |  |
| `rlow` | 저가율 | String | 12 | Y |  |
| `rclose` | 현재가율 | String | 12 | Y |  |
| `output2` | 응답상세 | String | 100 | Y |  |
| `pbid1` | 매수호가가격1 | String | 12 | Y |  |
| `pask1` | 매도호가가격1 | String | 12 | Y |  |
| `vbid1` | 매수호가잔량1 | String | 10 | Y |  |
| `vask1` | 매도호가잔량1 | String | 10 | Y |  |
| `dbid1` | 매수호가대비1 | String | 10 | Y |  |
| `dask1` | 매도호가대비1 | String | 10 | Y |  |
| `pbid2` | 매수호가가격2 | String | 12 | Y | 미국 거래소만 수신 |
| `pask2` | 매도호가가격2 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid2` | 매수호가잔량2 | String | 10 | Y | 미국 거래소만 수신 |
| `vask2` | 매도호가잔량2 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid2` | 매수호가대비2 | String | 10 | Y | 미국 거래소만 수신 |
| `dask2` | 매도호가대비2 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid3` | 매수호가가격3 | String | 12 | Y | 미국 거래소만 수신 |
| `pask3` | 매도호가가격3 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid3` | 매수호가잔량3 | String | 10 | Y | 미국 거래소만 수신 |
| `vask3` | 매도호가잔량3 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid3` | 매수호가대비3 | String | 10 | Y | 미국 거래소만 수신 |
| `dask3` | 매도호가대비3 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid4` | 매수호가가격4 | String | 12 | Y | 미국 거래소만 수신 |
| `pask4` | 매도호가가격4 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid4` | 매수호가잔량4 | String | 10 | Y | 미국 거래소만 수신 |
| `vask4` | 매도호가잔량4 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid4` | 매수호가대비4 | String | 10 | Y | 미국 거래소만 수신 |
| `dask4` | 매도호가대비4 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid5` | 매수호가가격5 | String | 12 | Y | 미국 거래소만 수신 |
| `pask5` | 매도호가가격5 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid5` | 매수호가잔량5 | String | 10 | Y | 미국 거래소만 수신 |
| `vask5` | 매도호가잔량5 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid5` | 매수호가대비5 | String | 10 | Y | 미국 거래소만 수신 |
| `dask5` | 매도호가대비5 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid6` | 매수호가가격6 | String | 12 | Y | 미국 거래소만 수신 |
| `pask6` | 매도호가가격6 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid6` | 매수호가잔량6 | String | 10 | Y | 미국 거래소만 수신 |
| `vask6` | 매도호가잔량6 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid6` | 매수호가대비6 | String | 10 | Y | 미국 거래소만 수신 |
| `dask6` | 매도호가대비6 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid7` | 매수호가가격7 | String | 12 | Y | 미국 거래소만 수신 |
| `pask7` | 매도호가가격7 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid7` | 매수호가잔량7 | String | 10 | Y | 미국 거래소만 수신 |
| `vask7` | 매도호가잔량7 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid7` | 매수호가대비7 | String | 10 | Y | 미국 거래소만 수신 |
| `dask7` | 매도호가대비7 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid8` | 매수호가가격8 | String | 12 | Y | 미국 거래소만 수신 |
| `pask8` | 매도호가가격8 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid8` | 매수호가잔량8 | String | 10 | Y | 미국 거래소만 수신 |
| `vask8` | 매도호가잔량8 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid8` | 매수호가대비8 | String | 10 | Y | 미국 거래소만 수신 |
| `dask8` | 매도호가대비8 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid9` | 매수호가가격9 | String | 12 | Y | 미국 거래소만 수신 |
| `pask9` | 매도호가가격9 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid9` | 매수호가잔량9 | String | 10 | Y | 미국 거래소만 수신 |
| `vask9` | 매도호가잔량9 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid9` | 매수호가대비9 | String | 10 | Y | 미국 거래소만 수신 |
| `dask9` | 매도호가대비9 | String | 10 | Y | 미국 거래소만 수신 |
| `pbid10` | 매수호가가격10 | String | 12 | Y | 미국 거래소만 수신 |
| `pask10` | 매도호가가격10 | String | 12 | Y | 미국 거래소만 수신 |
| `vbid10` | 매수호가잔량10 | String | 10 | Y | 미국 거래소만 수신 |
| `vask10` | 매도호가잔량10 | String | 10 | Y | 미국 거래소만 수신 |
| `dbid10` | 매수호가대비10 | String | 10 | Y | 미국 거래소만 수신 |
| `dask10` | 매도호가대비10 | String | 10 | Y | 미국 거래소만 수신 |
| `output3` | 응답상세 | Object | 100 | Y |  |
| `vstm` | VCMStart시간 | String | 6 | Y | 데이터 없음 |
| `vetm` | VCMEnd시간 | String | 6 | Y | 데이터 없음 |
| `csbp` | CAS/VCM기준가 | String | 12 | Y | 데이터 없음 |
| `cshi` | CAS/VCMHighprice | String | 12 | Y | 데이터 없음 |
| `cslo` | CAS/VCMLowprice | String | 12 | Y | 데이터 없음 |
| `iep` | IEP | String | 12 | Y | 데이터 없음 |
| `iev` | IEV | String | 12 | Y | 데이터 없음 |

### 응답 예시

```json
{
  "output1": {
    "rsym": "DNASTSLA",
    "zdiv": "4",
    "curr": "USD",
    "base": "149.9300",
    "open": "148.9700",
    "high": "150.9400",
    "low": "146.2200",
    "last": "147.0500",
    "dymd": "20240420",
    "dhms": "090000",
    "bvol": "0",
    "avol": "10759",
    "bdvl": "-1053",
    "advl": "-985",
    "code": "TSLA",
    "ropen": "-0.64",
    "rhigh": "+0.67",
    "rlow": "-2.47",
    "rclose": "-1.92"
  },
  "output2": {
    "pbid1": "0.0000",
    "pask1": "147.0000",
    "vbid1": "0",
    "vask1": "9730",
    "dbid1": "-275",
    "dask1": "9720",
    "pbid2": "0.0000",
    "pask2": "147.0000",
    "vbid2": "0",
    "vask2": "11",
    "dbid2": "-300",
    "dask2": "-216",
    "pbid3": "0.0000",
    "pask3": "147.0000",
    "vbid3": "0",
    "vask3": "643",
    "dbid3": "-5",
    "dask3": "-28",
    "pbid4": "0.0000",
    "pask4": "147.0000",
    "vbid4": "0",
    "vask4": "299",
    "dbid4": "-135",
    "dask4": "289",
    "pbid5": "0.0000",
    "pask5": "147.0000",
    "vbid5": "0",
    "vask5": "43",
    "dbid5": "-300",
    "dask5": "-57",
    "pbid6": "0.0000",
    "pask6": "147.0000",
    "vbid6": "0",
    "vask6": "15",
    "dbid6": "-30",
    "dask6": "-9715",
    "pbid7": "0.0000",
    "pask7": "147.0000",
    "vbid7": "0",
    "vask7": "18",
    "dbid7": "-2",
    "dask7": "7",
    "pbid8": "0.0000",
    "pask8": "0.0000",
    "vbid8": "0",
    "vask8": "0",
    "dbid8": "-3",
    "dask8": "-643",
    "pbid9": "0.0000",
    "pask9": "0.0000",
    "vbid9": "0",
    "vask9": "0",
    "dbid9": "-1",
    "dask9": "-299",
    "pbid10": "0.0000",
    "pask10": "0.0000",
    "vbid10": "0",
    "vask10": "0",
    "dbid10": "-2",
    "dask10": "-43"
  },
  "output3": {
    "vstm": "",
    "vetm": "",
    "csbp": "",
    "cshi": "",
    "cslo": "",
    "iep": "",
    "iev": ""
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
