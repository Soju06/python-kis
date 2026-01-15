# 해외선물옵션 장운영시간 [해외선물-030]

> [해외선물옵션] 기본시세

해외선물 장운영시간 API입니다.
한국투자 HTS(eFriend Force) > [6773] 해외선물 장운영시간 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3acd4025-6e95-46dc-a90d-b38215912d11` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/market-time` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `OTFM2229R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
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
| `tr_id` | 거래ID | String | 13 | Y | OTFM2229R |
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
| `FM_PDGR_CD` | FM상품군코드 | String | 10 | Y | 공백 |
| `FM_CLAS_CD` | FM클래스코드 | String | 3 | Y | '공백(전체), 001(통화), 002(금리), 003(지수), 004(농산물),005(축산물),006(금속),007(에너지)' |
| `FM_EXCG_CD` | FM거래소코드 | String | 10 | Y | 'CME(CME), EUREX(EUREX), HKEx(HKEx), ICE(ICE), SGX(SGX), OSE(OSE), ASX(ASX), CBOE(CBOE), MDEX(MDE... |
| `OPT_YN` | 옵션여부 | String | 1 | Y | %(전체), N(선물), Y(옵션) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |

### 요청 예시

```json
FM_PDGR_CD:
FM_CLAS_CD:
FM_EXCG_CD:CME
OPT_YN:%
CTX_AREA_NK200:
CTX_AREA_FK200:
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
| `output` | 응답상세 | Object |   | Y |  |
| `fm_pdgr_cd` | FM상품군코드 | String | 10 | Y |  |
| `fm_pdgr_name` | FM상품군명 | String | 60 | Y |  |
| `fm_excg_cd` | FM거래소코드 | String | 10 | Y |  |
| `fm_excg_name` | FM거래소명 | String | 60 | Y |  |
| `fuop_dvsn_name` | 선물옵션구분명 | String | 60 | Y |  |
| `fm_clas_cd` | FM클래스코드 | String | 3 | Y |  |
| `fm_clas_name` | FM클래스명 | String | 30 | Y |  |
| `am_mkmn_strt_tmd` | 오전장운영시작시각 | String | 6 | Y |  |
| `am_mkmn_end_tmd` | 오전장운영종료시각 | String | 6 | Y |  |
| `pm_mkmn_strt_tmd` | 오후장운영시작시각 | String | 6 | Y |  |
| `pm_mkmn_end_tmd` | 오후장운영종료시각 | String | 6 | Y |  |
| `mkmn_nxdy_strt_tmd` | 장운영익일시작시각 | String | 6 | Y |  |
| `mkmn_nxdy_end_tmd` | 장운영익일종료시각 | String | 6 | Y |  |
| `base_mket_strt_tmd` | 기본시장시작시각 | String | 6 | Y |  |
| `base_mket_end_tmd` | 기본시장종료시각 | String | 6 | Y |  |

### 응답 예시

```json
{
    "ctx_area_nk200": "CME^003^2ES^                                                                                                                                                                                            ",
    "ctx_area_fk200": "^CME^%^                                                                                                                                                                                                 ",
    "output": [
        {
            "fm_pdgr_cd": "6A",
            "fm_pdgr_name": "Australian Dollar",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6B",
            "fm_pdgr_name": "British pounds",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6C",
            "fm_pdgr_name": "Canadian Dollar",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6E",
            "fm_pdgr_name": "Euro FX",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6J",
            "fm_pdgr_name": "Japanese Yen",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6L",
            "fm_pdgr_name": "Brazilian Real",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6M",
            "fm_pdgr_name": "Mexican PESO",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6N",
            "fm_pdgr_name": "NewZealand Dollars",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6S",
            "fm_pdgr_name": "Swiss Franc",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "6Z",
            "fm_pdgr_name": "South African Rand",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "E7",
            "fm_pdgr_name": "E-mini Euro FX",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "J7",
            "fm_pdgr_name": "E-Mini YEN",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "M6A",
            "fm_pdgr_name": "E-micro AUD",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "M6B",
            "fm_pdgr_name": "E-micro GBP",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "M6E",
            "fm_pdgr_name": "E-micro EUR",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "MCD",
            "fm_pdgr_name": "E-micro CAD",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },
        {
            "fm_pdgr_cd": "MJY",
            "fm_pdgr_name": "E-micro JPY",
            "fm_excg_cd": "CME",
            "fm_excg_name": "Chicago Mercantile Exchange",
            "fuop_dvsn_name": "선물",
            "fm_clas_cd": "001",
            "fm_clas_name": "통화",
            "am_mkmn_strt_tmd": "070000",
            "am_mkmn_end_tmd": "060000",
            "pm_mkmn_strt_tmd": "",
            "pm_mkmn_end_tmd": "",
            "mkmn_nxdy_strt_tmd": "",
            "mkmn_nxdy_end_tmd": "",
            "base_mket_strt_tmd": "070000",
            "base_mket_end_tmd": "060000"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "KIOK0500",
    "msg1": "조회가 계속됩니다..다음버튼을 Click 하십시오.                                   "
}
```

