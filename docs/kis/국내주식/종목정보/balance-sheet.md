# 국내주식 대차대조표[v1_국내주식-078]

> [국내주식] 종목정보

국내주식 대차대조표 API입니다.
한국투자 HTS(eFriend Plus) > [0635] 재무분석종합 화면의 하단 '1. 대차대조표' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f77aedcb-b46f-4aa0-b062-f03b9a444405` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/finance/balance-sheet` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHKST66430100`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-29
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST66430100 |
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
| `FID_DIV_CLS_CODE` | 분류 구분 코드 | String | 2 | Y | 0: 년, 1: 분기 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | J |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 000660 : 종목코드 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_div_cls_code": "1"
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
| `output` | 응답상세 | Object |   | Y | array |
| `stac_yymm` | 결산 년월 | String | 6 | Y |  |
| `cras` | 유동자산 | String | 112 | Y |  |
| `fxas` | 고정자산 | String | 112 | Y |  |
| `total_aset` | 자산총계 | String | 102 | Y |  |
| `flow_lblt` | 유동부채 | String | 112 | Y |  |
| `fix_lblt` | 고정부채 | String | 112 | Y |  |
| `total_lblt` | 부채총계 | String | 102 | Y |  |
| `cpfn` | 자본금 | String | 22 | Y |  |
| `cfp_surp` | 자본 잉여금 | String | 182 | Y | 출력되지 않는 데이터(99.99 로 표시) |
| `prfi_surp` | 이익 잉여금 | String | 182 | Y | 출력되지 않는 데이터(99.99 로 표시) |
| `total_cptl` | 자본총계 | String | 102 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stac_yymm": "202312",
      "cras": "1959366.00",
      "fxas": "2599694.00",
      "total_aset": "4559060.00",
      "flow_lblt": "757195.00",
      "fix_lblt": "165087.00",
      "total_lblt": "922281.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3636779.00"
    },
    {
      "stac_yymm": "202309",
      "cras": "2064386.00",
      "fxas": "2480278.00",
      "total_aset": "4544664.00",
      "flow_lblt": "736252.00",
      "fix_lblt": "169486.00",
      "total_lblt": "905738.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3638926.00"
    },
    {
      "stac_yymm": "202306",
      "cras": "2039754.00",
      "fxas": "2440252.00",
      "total_aset": "4480006.00",
      "flow_lblt": "707806.00",
      "fix_lblt": "182443.00",
      "total_lblt": "890249.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3589756.00"
    },
    {
      "stac_yymm": "202303",
      "cras": "2144421.00",
      "fxas": "2396496.00",
      "total_aset": "4540918.00",
      "flow_lblt": "760574.00",
      "fix_lblt": "182349.00",
      "total_lblt": "942924.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3597994.00"
    },
    {
      "stac_yymm": "202212",
      "cras": "2184706.00",
      "fxas": "2299539.00",
      "total_aset": "4484245.00",
      "flow_lblt": "783449.00",
      "fix_lblt": "153301.00",
      "total_lblt": "936749.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3547496.00"
    },
    {
      "stac_yymm": "202209",
      "cras": "2508806.00",
      "fxas": "2193978.00",
      "total_aset": "4702784.00",
      "flow_lblt": "852857.00",
      "fix_lblt": "400859.00",
      "total_lblt": "1253715.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3449069.00"
    },
    {
      "stac_yymm": "202206",
      "cras": "2362875.00",
      "fxas": "2117532.00",
      "total_aset": "4480407.00",
      "flow_lblt": "833623.00",
      "fix_lblt": "367717.00",
      "total_lblt": "1201340.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3279067.00"
    },
    {
      "stac_yymm": "202203",
      "cras": "2323691.00",
      "fxas": "2069579.00",
      "total_aset": "4393270.00",
      "flow_lblt": "904637.00",
      "fix_lblt": "335723.00",
      "total_lblt": "1240360.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3152909.00"
    },
    {
      "stac_yymm": "202112",
      "cras": "2181632.00",
      "fxas": "2084580.00",
      "total_aset": "4266212.00",
      "flow_lblt": "881171.00",
      "fix_lblt": "336041.00",
      "total_lblt": "1217212.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "3048999.00"
    },
    {
      "stac_yymm": "202109",
      "cras": "2127930.00",
      "fxas": "1976277.00",
      "total_aset": "4104207.00",
      "flow_lblt": "818720.00",
      "fix_lblt": "317826.00",
      "total_lblt": "1136546.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2967661.00"
    },
    {
      "stac_yymm": "202106",
      "cras": "1911185.00",
      "fxas": "1936591.00",
      "total_aset": "3847777.00",
      "flow_lblt": "724615.00",
      "fix_lblt": "299920.00",
      "total_lblt": "1024534.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2823243.00"
    },
    {
      "stac_yymm": "202103",
      "cras": "2091554.00",
      "fxas": "1836709.00",
      "total_aset": "3928263.00",
      "flow_lblt": "901095.00",
      "fix_lblt": "284482.00",
      "total_lblt": "1185577.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2742686.00"
    },
    {
      "stac_yymm": "202012",
      "cras": "1982156.00",
      "fxas": "1800201.00",
      "total_aset": "3782357.00",
      "flow_lblt": "756044.00",
      "fix_lblt": "266834.00",
      "total_lblt": "1022877.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2759480.00"
    },
    {
      "stac_yymm": "202009",
      "cras": "2036349.00",
      "fxas": "1721538.00",
      "total_aset": "3757887.00",
      "flow_lblt": "730464.00",
      "fix_lblt": "266061.00",
      "total_lblt": "996526.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2761362.00"
    },
    {
      "stac_yymm": "202006",
      "cras": "1861368.00",
      "fxas": "1718227.00",
      "total_aset": "3579595.00",
      "flow_lblt": "618637.00",
      "fix_lblt": "262880.00",
      "total_lblt": "881517.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2698078.00"
    },
    {
      "stac_yymm": "202003",
      "cras": "1867397.00",
      "fxas": "1707178.00",
      "total_aset": "3574575.00",
      "flow_lblt": "647633.00",
      "fix_lblt": "263065.00",
      "total_lblt": "910698.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2663877.00"
    },
    {
      "stac_yymm": "201912",
      "cras": "1813853.00",
      "fxas": "1711792.00",
      "total_aset": "3525645.00",
      "flow_lblt": "637828.00",
      "fix_lblt": "259013.00",
      "total_lblt": "896841.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2628804.00"
    },
    {
      "stac_yymm": "201909",
      "cras": "1860421.00",
      "fxas": "1673439.00",
      "total_aset": "3533860.00",
      "flow_lblt": "633032.00",
      "fix_lblt": "266405.00",
      "total_lblt": "899437.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2634422.00"
    },
    {
      "stac_yymm": "201906",
      "cras": "1734335.00",
      "fxas": "1695067.00",
      "total_aset": "3429401.00",
      "flow_lblt": "593093.00",
      "fix_lblt": "258838.00",
      "total_lblt": "851931.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2577470.00"
    },
    {
      "stac_yymm": "201903",
      "cras": "1773885.00",
      "fxas": "1676794.00",
      "total_aset": "3450679.00",
      "flow_lblt": "673541.00",
      "fix_lblt": "244986.00",
      "total_lblt": "918527.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2532152.00"
    },
    {
      "stac_yymm": "201812",
      "cras": "1746974.00",
      "fxas": "1646598.00",
      "total_aset": "3393572.00",
      "flow_lblt": "690815.00",
      "fix_lblt": "225226.00",
      "total_lblt": "916041.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2477532.00"
    },
    {
      "stac_yymm": "201809",
      "cras": "1762820.00",
      "fxas": "1609137.00",
      "total_aset": "3371958.00",
      "flow_lblt": "747059.00",
      "fix_lblt": "203868.00",
      "total_lblt": "950926.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2421032.00"
    },
    {
      "stac_yymm": "201806",
      "cras": "1569768.00",
      "fxas": "1617115.00",
      "total_aset": "3186884.00",
      "flow_lblt": "656023.00",
      "fix_lblt": "199612.00",
      "total_lblt": "855635.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2331248.00"
    },
    {
      "stac_yymm": "201803",
      "cras": "1549420.00",
      "fxas": "1575312.00",
      "total_aset": "3124731.00",
      "flow_lblt": "682986.00",
      "fix_lblt": "209146.00",
      "total_lblt": "892132.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2232599.00"
    },
    {
      "stac_yymm": "201712",
      "cras": "1469825.00",
      "fxas": "1547696.00",
      "total_aset": "3017521.00",
      "flow_lblt": "671751.00",
      "fix_lblt": "200855.00",
      "total_lblt": "872607.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2144914.00"
    },
    {
      "stac_yymm": "201709",
      "cras": "1453223.00",
      "fxas": "1512562.00",
      "total_aset": "2965786.00",
      "flow_lblt": "661726.00",
      "fix_lblt": "197147.00",
      "total_lblt": "858873.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2106913.00"
    },
    {
      "stac_yymm": "201706",
      "cras": "1321727.00",
      "fxas": "1454168.00",
      "total_aset": "2775894.00",
      "flow_lblt": "584684.00",
      "fix_lblt": "184153.00",
      "total_lblt": "768837.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "2007057.00"
    },
    {
      "stac_yymm": "201703",
      "cras": "1292842.00",
      "fxas": "1349332.00",
      "total_aset": "2642174.00",
      "flow_lblt": "568431.00",
      "fix_lblt": "175563.00",
      "total_lblt": "743994.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "1898180.00"
    },
    {
      "stac_yymm": "201612",
      "cras": "1414297.00",
      "fxas": "1207446.00",
      "total_aset": "2621743.00",
      "flow_lblt": "547041.00",
      "fix_lblt": "145072.00",
      "total_lblt": "692113.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "1929630.00"
    },
    {
      "stac_yymm": "201609",
      "cras": "1321668.00",
      "fxas": "1123047.00",
      "total_aset": "2444715.00",
      "flow_lblt": "504595.00",
      "fix_lblt": "144756.00",
      "total_lblt": "649351.00",
      "cpfn": "8975",
      "cfp_surp": "99.99",
      "prfi_surp": "99.99",
      "total_cptl": "1795364.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
