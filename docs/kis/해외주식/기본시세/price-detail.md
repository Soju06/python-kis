# 해외주식 현재가상세[v1_해외주식-029]

> [해외주식] 기본시세

해외주식 현재가상세 API입니다.

해당 API를 활용하여 해외주식 종목의 매매단위(vnit), 호가단위(e_hogau), PER, PBR, EPS, BPS 등의 데이터를 확인하실 수 있습니다.

해외주식 시세는 무료시세(지연시세)만이 제공되며, API로는 유료시세(실시간시세)를 받아보실 수 없습니다.

※ 지연시세 지연시간 : 미국 - 실시간무료(0분지연) / 홍콩, 베트남, 중국, 일본 - 15분지연
   미국의 경우 0분지연시세로 제공되나, 장중 당일 시가는 상이할 수 있으며, 익일 정정 표시됩니다.

※ 2024년 12월 13일(금) 오후 5시부터 HTS(efriend Plus) [7781] 시세신청(실시간) 화면에서 유료 서비스 신청 후 접근토큰 발급하면 최대 2시간 이후 실시간 유료 시세 수신 가능

※ 미국주식 시세의 경우 주간거래시간을 제외한 정규장, 애프터마켓, 프리마켓 시간대에 동일한 API(TR)로 시세 조회가 되는 점 유의 부탁드립니다.

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


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `abc66a03-8103-4f6d-8ba8-450c2b935e14` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/price-detail` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDFS76200200` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-04-14
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
| `tr_id` | 거래ID | String | 13 | Y | HHDFS76200200 |
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
| `AUTH` | 사용자권한정보 | String | 32 | Y |  |
| `EXCD` | 거래소명 | String | 4 | Y | HKS : 홍콩 NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 TSE : 도쿄 SHS : 상해 SZS : 심천 SHI : 상해지수 SZI : 심천지수 HSX : 호치민 ... |
| `SYMB` | 종목코드 | String | 16 | Y |  |

### 요청 예시

```json
{
  "AUTH": "",
  "EXCD": "NAS",
  "SYMB": "TSLA"
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
| `output` | 응답상세 | String |   | Y |  |
| `rsym` | 실시간조회종목코드 | String | 16 | Y |  |
| `pvol` | 전일거래량 | String | 14 | Y |  |
| `open` | 시가 | String | 12 | Y |  |
| `high` | 고가 | String | 12 | Y |  |
| `low` | 저가 | String | 12 | Y |  |
| `last` | 현재가 | String | 12 | Y |  |
| `base` | 전일종가 | String | 12 | Y |  |
| `tomv` | 시가총액 | String | 16 | Y |  |
| `pamt` | 전일거래대금 | String | 14 | Y |  |
| `uplp` | 상한가 | String | 12 | Y |  |
| `dnlp` | 하한가 | String | 12 | Y |  |
| `h52p` | 52주최고가 | String | 12 | Y |  |
| `h52d` | 52주최고일자 | String | 8 | Y |  |
| `l52p` | 52주최저가 | String | 12 | Y |  |
| `l52d` | 52주최저일자 | String | 8 | Y |  |
| `perx` | PER | String | 10 | Y |  |
| `pbrx` | PBR | String | 10 | Y |  |
| `epsx` | EPS | String | 10 | Y |  |
| `bpsx` | BPS | String | 10 | Y |  |
| `shar` | 상장주수 | String | 16 | Y |  |
| `mcap` | 자본금 | String | 16 | Y |  |
| `curr` | 통화 | String | 4 | Y |  |
| `zdiv` | 소수점자리수 | String | 1 | Y |  |
| `vnit` | 매매단위 | String | 6 | Y |  |
| `t_xprc` | 원환산당일가격 | String | 12 | Y |  |
| `t_xdif` | 원환산당일대비 | String | 12 | Y |  |
| `t_xrat` | 원환산당일등락 | String | 12 | Y |  |
| `p_xprc` | 원환산전일가격 | String | 12 | Y |  |
| `p_xdif` | 원환산전일대비 | String | 12 | Y |  |
| `p_xrat` | 원환산전일등락 | String | 12 | Y |  |
| `t_rate` | 당일환율 | String | 12 | Y |  |
| `p_rate` | 전일환율 | String | 12 | Y |  |
| `t_xsgn` | 원환산당일기호 | String | 1 | Y | HTS 색상표시용 |
| `p_xsng` | 원환산전일기호 | String | 1 | Y | HTS 색상표시용 |
| `e_ordyn` | 거래가능여부 | String | 20 | Y |  |
| `e_hogau` | 호가단위 | String | 8 | Y |  |
| `e_icod` | 업종(섹터) | String | 40 | Y |  |
| `e_parp` | 액면가 | String | 12 | Y |  |
| `tvol` | 거래량 | String | 14 | Y |  |
| `tamt` | 거래대금 | String | 14 | Y |  |
| `etyp_nm` | ETP 분류명 | String | 20 | Y |  |

### 응답 예시

```json
{
  "output": {
    "rsym": "DNASTSLA",
    "zdiv": "4",
    "curr": "USD",
    "vnit": "1",
    "open": "257.2600",
    "high": "259.0794",
    "low": "242.0100",
    "last": "245.0100",
    "base": "258.0800",
    "pvol": "108861698",
    "pamt": "28090405673",
    "uplp": "0.0000",
    "dnlp": "0.0000",
    "h52p": "313.8000",
    "h52d": "20220921",
    "l52p": "101.8100",
    "l52d": "20230106",
    "perx": "69.51",
    "pbrx": "15.21",
    "epsx": "3.52",
    "bpsx": "16.11",
    "shar": "3173990000",
    "mcap": "3000000",
    "tomv": "777659289900",
    "t_xprc": "323658",
    "t_xdif": "17265",
    "t_xrat": "-5.06",
    "p_xprc": "0",
    "p_xdif": "0",
    "p_xrat": " 0.00",
    "t_rate": "1321.00",
    "p_rate": "",
    "t_xsgn": "5",
    "p_xsng": "3",
    "e_ordyn": "매매 가능",
    "e_hogau": "0.0100",
    "e_icod": "자동차",
    "e_parp": "0.0000",
    "tvol": "132541640",
    "tamt": "32907071789",
    "etyp_nm": ""
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

