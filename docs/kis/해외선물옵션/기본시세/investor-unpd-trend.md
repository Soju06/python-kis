# 해외선물 미결제추이 [해외선물-029]

> [해외선물옵션] 기본시세

해외선물 미결제추이 API입니다.
한국투자 HTS(eFriend Force) > [5503] 해외선물 미결제약정추이 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 해외선물 투자자별 미결제약정 추이 자료설명
1. 해외선물 투자자별 미결제약정 자료는 미국상품선물위원회(CFTC)에서 매주 1회 발표하고 있습니다.
2. 기준일은 매주 화요일이며, 발표는 매주 금요일 15:30 (미국동부표준시)에 하며, 당사는 매주 토요일 아침에 자료를 업데이트하고 있습니다.
3. 활용방법 : CFTC에서 발표하는 미결제약점 동향자료는 각 선물시장의 투기자금 동향을 파약하는데 용이하며, 특히, 상품시장에서 유용하게 활용할 수 있습니다.
4. 주요항목 설명
. 투기거래자 : 실물보유 또는 보유중인 실물에 대한 헤지목적이 아닌 가격변동에 따른 이익을 목적으로 거래하는 고객으로 주로 투자은행, 자산운용사, 헤지펀드, 개인투자자등임
﻿﻿. 헤지거래자 : 실물보유 또는 보유중인 실물에 대한 헤지목적으로 거래하는 고객으로 주로 일반기업, 생산업체, 원자재공급업체등임.
﻿﻿. 보고누락분 : 시장전체 미결제약정과 투기거래자와 헤지거래자 보고분 합계와의 차이로 투자주제가 확인안된 거래임.
. 투자자 : 최종거래고객 기준이 아닌 거래소 회원 단위 기준임.
5. CFTC 홈페이지: http://www.cftc.gov/index.htm


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `d5dc7247-6f82-4cd7-8133-afabd8f003f7` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/investor-unpd-trend` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDDB95030000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17
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
| `tr_id` | 거래ID | String | 13 | Y | HHDDB95030000 |
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
| `PROD_ISCD` | 상품 | String | 5 | Y | 금리 (GE, ZB, ZF,ZN,ZT), 금속(GC, PA, PL,SI, HG), 농산물(CC, CT,KC, OJ, SB, ZC,ZL, ZM, ZO, ZR, ZS, ZW), ... |
| `BSOP_DATE` | 일자 | String | 8 | Y | 기준일(ex)20240513) |
| `UPMU_GUBUN` | 구분 | String | 1 | Y | 0(수량), 1(증감) |
| `CTS_KEY` | CTS_KEY | String | 16 | Y | 공백 |

### 요청 예시

```json
PROD_ISCD:ES
BSOP_DATE:20240624
UPMU_GUBUN:0
CTS_KEY:
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
| `output1` | 응답상세 | String |   | Y |  |
| `row_cnt` | 응답레코드카운트 | String | 4 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `prod_iscd` | 상품 | String | 5 | Y |  |
| `cftc_iscd` | CFTC코드 | String | 10 | Y |  |
| `bsop_date` | 일자 | String | 8 | Y |  |
| `bidp_spec` | 매수투기 | String | 10 | Y |  |
| `askp_spec` | 매도투기 | String | 10 | Y |  |
| `spread_spec` | 스프레드투기 | String | 10 | Y |  |
| `bidp_hedge` | 매수헤지 | String | 10 | Y |  |
| `askp_hedge` | 매도헤지 | String | 10 | Y |  |
| `hts_otst_smtn` | 미결제합계 | String | 10 | Y |  |
| `bidp_missing` | 매수누락 | String | 10 | Y |  |
| `askp_missing` | 매도누락 | String | 10 | Y |  |
| `bidp_spec_cust` | 매수투기고객 | String | 10 | Y |  |
| `askp_spec_cust` | 매도투기고객 | String | 10 | Y |  |
| `spread_spec_cust` | 스프레드투기고객 | String | 10 | Y |  |
| `bidp_hedge_cust` | 매수헤지고객 | String | 10 | Y |  |
| `askp_hedge_cust` | 매도헤지고객 | String | 10 | Y |  |
| `cust_smtn` | 고객합계 | String | 10 | Y |  |

### 응답 예시

```json
{
    "output1": {
        "row_cnt": "0100"
    },
    "output2": [
        {
            "prod_iscd": "ES",
            "cftc_iscd": "13874A",
            "bsop_date": "20240611",
            "bidp_spec": "270380",
            "askp_spec": "381794",
            "spread_spec": "0",
            "bidp_hedge": "1606798",
            "askp_hedge": "1617849",
            "hts_otst_smtn": "2266096",
            "bidp_missing": "297310",
            "askp_missing": "174845",
            "bidp_spec_cust": "80",
            "askp_spec_cust": "68",
            "spread_spec_cust": "55",
            "bidp_hedge_cust": "253",
            "askp_hedge_cust": "205",
            "cust_smtn": "472"
        },
        {
            "prod_iscd": "ES",
            "cftc_iscd": "13874A",
            "bsop_date": "20240604",
            "bidp_spec": "265433",
            "askp_spec": "330433",
            "spread_spec": "0",
            "bidp_hedge": "1534557",
            "askp_hedge": "1581649",
            "hts_otst_smtn": "2160026",
            "bidp_missing": "287673",
            "askp_missing": "175581",
            "bidp_spec_cust": "76",
            "askp_spec_cust": "68",
            "spread_spec_cust": "45",
            "bidp_hedge_cust": "262",
            "askp_hedge_cust": "207",
            "cust_smtn": "474"
        },
        {
            "prod_iscd": "ES",
            "cftc_iscd": "13874A",
            "bsop_date": "20240528",
            "bidp_spec": "330937",
            "askp_spec": "333145",
            "spread_spec": "0",
            "bidp_hedge": "1503708",
            "askp_hedge": "1609652",
            "hts_otst_smtn": "2179731",
            "bidp_missing": "289071",
            "askp_missing": "180919",
            "bidp_spec_cust": "80",
            "askp_spec_cust": "63",
            "spread_spec_cust": "39",
            "bidp_hedge_cust": "251",
            "askp_hedge_cust": "203",
            "cust_smtn": "469"
        },
        {
            "prod_iscd": "ES",
            "cftc_iscd": "13874A",
            "bsop_date": "20240521",
            "bidp_spec": "304226",
            "askp_spec": "327000",
            "spread_spec": "0",
            "bidp_hedge": "1501724",
            "askp_hedge": "1593706",
            "hts_otst_smtn": "2148201",
            "bidp_missing": "288496",
            "askp_missing": "173740",
            "bidp_spec_cust": "78",
            "askp_spec_cust": "66",
            "spread_spec_cust": "42",
            "bidp_hedge_cust": "249",
            "askp_hedge_cust": "205",
            "cust_smtn": "470"
        },
        {
            "prod_iscd": "ES",
            "cftc_iscd": "13874A",
            "bsop_date": "20240514",
            "bidp_spec": "273398",
            "askp_spec": "298682",
            "spread_spec": "0",
            "bidp_hedge": "1477881",
            "askp_hedge": "1550928",
            "hts_otst_smtn": "2081097",
            "bidp_missing": "278004",
            "askp_missing": "179673",
            "bidp_spec_cust": "83",
            "askp_spec_cust": "67",
            "spread_spec_cust": "45",
            "bidp_hedge_cust": "248",
            "askp_hedge_cust": "201",
            "cust_smtn": "470"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "",
    "msg1": "정상 조회되었습니다."
}
```

