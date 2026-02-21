# 해외주식조건검색[v1_해외주식-015]

> [해외주식] 기본시세

해외주식 조건검색 API입니다.
한국투자 HTS(eFriend Plus) > [7641] 해외주식 조건검색 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
  
현재 조건검색 결과값은 최대 100개까지 조회 가능합니다. 다음 조회(100개 이후의 값) 기능에 대해서는 개선검토 중에 있습니다.

※ 지연시세 지연시간 : 미국 - 실시간무료(0분지연) / 홍콩, 베트남, 중국, 일본 - 15분지연 (중국은 실시간시세 신청 시 무료실시간시세 제공)
   미국의 경우 0분지연시세로 제공되나, 장중 당일 시가는 상이할 수 있으며, 익일 정정 표시됩니다.

※ 2024년 12월 13일(금) 오후 5시부터 HTS(efriend Plus) [7781] 시세신청(실시간) 화면에서 유료 서비스 신청 후 접근토큰 발급하면 최대 2시간 이후 실시간 유료 시세 수신 가능

※ 그날 거래량이나 시세 형성이 안된 종목은 해외주식 기간별시세(HHDFS76240000)에서는 조회되지만 
   해외주식 조건검색(HHDFS76410000)에서 조회되지 않습니다. (EX. NAS AATC)

[미국주식시세 이용시 유의사항]
■ 무료 실시간 시세 서비스가 기본 제공되며, 유료 실시간 시세 서비스는 HTS ‘[7781] 시세신청 (실시간)’과 MTS(모바일) ‘고객서비스 > 거래 서비스신청 > 해외주식 > 해외 실시간시세 신청’ 에서 신청 가능합니다.
※ 무료(매수/매도 각 1호가) : 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보
※ 유료(매수/매도 각 1호가) : 미국 전체 거래소들의 통합 주문체결 및 최우선 호가
■ 무료 실시간 시세 서비스는 유료 실시간 시세 서비스 대비 평균 50% 수준에 해당하는 정보이므로 
현재가/호가/순간체결량/차트 등에서 일시적·부분적 차이가 있을 수 있습니다. 
■ 무료∙유료 모두 미국에 상장된 종목(뉴욕, 나스닥, 아멕스 등)의 시세를 제공하며, 동일한 시스템을 사용하여 주문∙체결됩니다. 
단, 무료∙유료의 기반 데이터 차이로 호가 및 체결 데이터는 차이가 발생할 수 있고, 이로 인해 발생하는 손실에 대해서 당사가 책임지지 않습니다.
■ 무료 실시간 시세 서비스의 시가, 저가, 고가, 종가는 유료 실시간 시세 서비스와 다를 수 있으며, 
종목별 과거 데이터(거래량, 시가, 종가, 고가, 차트 데이터 등)는 장 종료 후(오후 12시경) 유료 실시간 시세 서비스 데이터와 동일하게 업데이트됩니다.
■ 유료 실시간 시세 서비스는 신청 시 1~12개월까지 기간 선택 후 해당 요금을 일괄 납부하며, 
해지 시 해지한 달의 말일까지 시세 제공 후 남은 기간 해당 금액이 환급되니 유의하시기 바랍니다.
(출처: 한국투자증권 외화증권 거래설명서 - https://www.truefriend.com/main/customer/guide/Guide.jsp?&cmd=TF04ag010002&currentPage=1&num=64)
■ output2에 조회되는 순위(rank)는 거래량을 기준으로 내림차순 정렬 시 나오는 순위인 점 참고 부탁드립니다.

해외주식조건검색[v1_해외주식-015]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `65db61e3-49a5-4a95-9cf3-61298c7b8461` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/inquire-search` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `HHDFS76410000` |
| **TR ID (모의)** | `HHDFS76410000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-08-19T15:58:11+09:00
- **최종 수정일**: 2025-04-30T12:13:17+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용)  ※ 토큰 지정시 토큰 타입("Bearer") 지정 필요. 즉, 발급받은 접근토큰 앞에 앞에 "Bearer" 붙여서 호출 EX) "Bearer eyJ..........8GA" |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFS76410000 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | N | B : 법인 / P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | 법인 : "001" / default   개인: "" |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `AUTH` | 사용자권한정보 | String | 32 | Y | "" (Null 값 설정) |
| `EXCD` | 거래소코드 | String | 4 | Y | NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 |
| `CO_YN_PRICECUR` | 현재가선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_PRICECUR` | 현재가시작범위가 | String | 12 | N | 단위: 각국통화(JPY, USD, HKD, CNY, VND) |
| `CO_EN_PRICECUR` | 현재가끝범위가 | String | 12 | N | 단위: 각국통화(JPY, USD, HKD, CNY, VND) |
| `CO_YN_RATE` | 등락율선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_RATE` | 등락율시작율 | String | 12 | N | % |
| `CO_EN_RATE` | 등락율끝율 | String | 12 | N | % |
| `CO_YN_VALX` | 시가총액선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_VALX` | 시가총액시작액 | String | 12 | N | 단위: 천 |
| `CO_EN_VALX` | 시가총액끝액 | String | 12 | N | 단위: 천 |
| `CO_YN_SHAR` | 발행주식수선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_SHAR` | 발행주식시작수 | String | 12 | N | 단위: 천 |
| `CO_EN_SHAR` | 발행주식끝수 | String | 112 | N | 단위: 천 |
| `CO_YN_VOLUME` | 거래량선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_VOLUME` | 거래량시작량 | String | 12 | N | 단위: 주 |
| `CO_EN_VOLUME` | 거래량끝량 | String | 12 | N | 단위: 주 |
| `CO_YN_AMT` | 거래대금선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_AMT` | 거래대금시작금 | String | 12 | N | 단위: 천 |
| `CO_EN_AMT` | 거래대금끝금 | String | 12 | N | 단위: 천 |
| `CO_YN_EPS` | EPS선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_EPS` | EPS시작 | String | 12 | N |  |
| `CO_EN_EPS` | EPS끝 | String | 12 | N |  |
| `CO_YN_PER` | PER선택조건 | String | 1 | N | 해당조건 사용시(1), 미사용시 필수항목아님 |
| `CO_ST_PER` | PER시작 | String | 12 | N |  |
| `CO_EN_PER` | PER끝 | String | 12 | N |  |
| `KEYB` | NEXT KEY BUFF | String | 8 | N | "" 공백 입력 |

### 요청 예시

```json
{
    "AUTH":"",
    "EXCD":"NAS",
    "CO_YN_PRICECUR":"1",
    "CO_ST_PRICECUR":"160",
    "CO_EN_PRICECUR":"161",
    "CO_YN_RATE":"",
    "CO_ST_RATE":"",
    "CO_EN_RATE":"",
    "CO_YN_VALX":"",
    "CO_ST_VALX":"",
    "CO_EN_VALX":"",
    "CO_YN_SHAR":"",
    "CO_ST_SHAR":"",
    "CO_EN_SHAR":"",
    "CO_YN_VOLUME":"",
    "CO_ST_VOLUME":"",
    "CO_EN_VOLUME":"",
    "CO_YN_AMT":"",
    "CO_ST_AMT":"",
    "CO_EN_AMT":"",
    CO_YN_EPS":"",
    CO_ST_EPS":"",
    CO_EN_EPS":"",
    CO_YN_PER":"",
    CO_ST_PER":"",
    CO_EN_PER":""
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
| `output1` | 응답상세1 | String |  | Y |  |
| `zdiv` | 소수점자리수 | String | 1 | Y | 소수점자리수 |
| `stat` | 거래상태정보 | String | 20 | Y | 거래상태정보 |
| `crec` | 현재조회종목수 | String | 6 | Y | 현재조회종목수 |
| `trec` | 전체조회종목수 | String | 6 | Y | 전체조회종목수 |
| `nrec` | Record Count | String | 4 | Y | Record Count |
| `output2` | 응답상세2 | Object |   | Y | 조회결과 상세 |
| `rsym` | 실시간조회심볼 | String | 32 | N | 실시간조회심볼  D+시장구분(3자리)+종목코드 예) DNASAAPL : D+NAS(나스닥)+AAPL(애플) [시장구분] NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 , TSE : 도쿄, HKS : 홍콩, SHS : 상해, SZS : 심천 HSX : 호치민, HNX : 하노이 |
| `excd` | 거래소코드 | String | 4 | N | 거래소코드 |
| `name` | 종목명 | String | 48 | N | 종목명 |
| `symb` | 종목코드 | String | 16 | N | 종목코드 |
| `last` | 현재가 | String | 12 | N | 현재가 |
| `shar` | 발행주식 | String | 14 | N | 발행주식수(단위: 천) |
| `valx` | 시가총액 | String | 14 | N | 시가총액(단위: 천) |
| `plow` | 저가 | String | 12 | N | 저가 |
| `phigh` | 고가 | String | 12 | N | 고가 |
| `popen` | 시가 | String | 12 | N | 시가 |
| `tvol` | 거래량 | String | 14 | N | 거래량(단위: 주) |
| `rate` | 등락율 | String | 12 | N | 등락율(%) |
| `diff` | 대비 | String | 12 | N | 대비 |
| `sign` | 기호 | String | 1 | N | 기호 |
| `avol` | 거래대금 | String | 14 | N | 거래대금(단위: 천) |
| `eps` | EPS | String | 14 | N | EPS |
| `per` | PER | String | 14 | N | PER |
| `rank` | 순위 | String | 6 | N | 순위 |
| `ename` | 영문종목명 | String | 48 | N | 영문종목명 |
| `e_ordyn` | 매매가능 | String | 2 | N | 가능 : O |

### 응답 예시

```json
{
  "output1": {
    "zdiv": "4",
    "stat": "무료실시간",
    "crec": "2",
    "trec": "2",
    "nrec": "2"
  },
  "output2": [
    {
      "rsym": "DNASTSLA",
      "excd": "NAS",
      "symb": "TSLA",
      "name": "테슬라",
      "last": "160.9500",
      "sign": "5",
      "diff": "6.8700",
      "rate": "-4.09",
      "tvol": "175862722",
      "popen": "174.8700",
      "phigh": "175.0500",
      "plow": "156.9100",
      "valx": "508239862",
      "shar": "3157750000",
      "avol": "28842552711",
      "eps": "3.24",
      "per": "49.73",
      "rank": "1",
      "ename": "TESLA INC",
      "e_ordyn": "○"
    },
    {
      "rsym": "DNASPANW",
      "excd": "NAS",
      "symb": "PANW",
      "name": "팔로 알토 네트웍스",
      "last": "160.7500",
      "sign": "5",
      "diff": "1.0300",
      "rate": "-0.64",
      "tvol": "3570070",
      "popen": "168.2200",
      "phigh": "168.9900",
      "plow": "159.7700",
      "valx": "48603888",
      "shar": "302357000",
      "avol": "580983313",
      "eps": "0.50",
      "per": "324.62",
      "rank": "2",
      "ename": "PALO ALTO NETWORKS INC",
      "e_ordyn": "○"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

