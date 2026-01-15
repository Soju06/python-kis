# 해외주식 기간별권리조회 [해외주식-052]

> [해외주식] 시세분석

해외주식 기간별권리조회 API입니다.
한국투자 HTS(eFriend Plus) > [7520] 기간별해외증권권리조회 화면을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 확정여부가 '예정'으로 표시되는 경우는 권리정보가 변경될 수 있으니 참고자료로만 활용하시기 바랍니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `2151d14c-0fae-44a5-be38-c3f5ab8354bb` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/period-rights` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTRGT011R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19
- **최종 수정일**: 2025-05-15

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTRGT011R |
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
| `RGHT_TYPE_CD` | 권리유형코드 | String | 2 | Y | '%%(전체), 01(유상), 02(무상), 03(배당), 11(합병),  14(액면분할), 15(액면병합), 17(감자), 54(WR청구), 61(원리금상환), 71(WR소... |
| `INQR_DVSN_CD` | 조회구분코드 | String | 2 | Y | 02(현지기준일), 03(청약시작일), 04(청약종료일) |
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y | 일자 ~ |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y | ~ 일자 |
| `PDNO` | 상품번호 | String | 12 | Y | 공백 |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | 공백 |
| `CTX_AREA_NK50` | 연속조회키50 | String | 50 | Y | 공백 |
| `CTX_AREA_FK50` | 연속조회검색조건50 | String | 50 | Y | 공백 |

### 요청 예시

```json
RGHT_TYPE_CD:%%
INQR_DVSN_CD:02
INQR_STRT_DT:20240417
INQR_END_DT:20240417
PDNO:
PRDT_TYPE_CD:
CTX_AREA_NK50:
CTX_AREA_FK50:
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
| `bass_dt` | 기준일자 | String | 8 | Y |  |
| `rght_type_cd` | 권리유형코드 | String | 2 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `std_pdno` | 표준상품번호 | String | 12 | Y |  |
| `acpl_bass_dt` | 현지기준일자 | String | 8 | Y |  |
| `sbsc_strt_dt` | 청약시작일자 | String | 8 | Y |  |
| `sbsc_end_dt` | 청약종료일자 | String | 8 | Y |  |
| `cash_alct_rt` | 현금배정비율 | String | 191 | Y |  |
| `stck_alct_rt` | 주식배정비율 | String | 2012 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `crcy_cd2` | 통화코드2 | String | 3 | Y |  |
| `crcy_cd3` | 통화코드3 | String | 3 | Y |  |
| `crcy_cd4` | 통화코드4 | String | 3 | Y |  |
| `alct_frcr_unpr` | 배정외화단가 | String | 195 | Y |  |
| `stkp_dvdn_frcr_amt2` | 주당배당외화금액2 | String | 195 | Y |  |
| `stkp_dvdn_frcr_amt3` | 주당배당외화금액3 | String | 195 | Y |  |
| `stkp_dvdn_frcr_amt4` | 주당배당외화금액4 | String | 195 | Y |  |
| `dfnt_yn` | 확정여부 | String | 1 | Y |  |

### 응답 예시

```json
{
  "ctx_area_nk50": "                                                  ",
  "ctx_area_fk50": "%%!^02!^20240417!^20240417!^!^                    ",
  "output": [
    {
      "bass_dt": "20240418",
      "rght_type_cd": "03",
      "pdno": "000661",
      "prdt_name": "[000661]CHANGCHUN HIGH-TECH INDUSTRY (GROUP",
      "prdt_type_cd": "552",
      "std_pdno": "CNE0000007J8",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "",
      "sbsc_end_dt": "",
      "cash_alct_rt": "450.0000000000",
      "stck_alct_rt": "0.000000000000",
      "crcy_cd": "CNY",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "4.50000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240418",
      "rght_type_cd": "03",
      "pdno": "AIR",
      "prdt_name": "AIRBUS GROUP NV",
      "prdt_type_cd": "542",
      "std_pdno": "NL0000235190",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "",
      "sbsc_end_dt": "",
      "cash_alct_rt": "180.0000000000",
      "stck_alct_rt": "0.000000000000",
      "crcy_cd": "EUR",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "1.80000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240418",
      "rght_type_cd": "03",
      "pdno": "GYLD",
      "prdt_name": "ARROW ETF TR ARROW DOW JONES GLOBAL YIELD ETF",
      "prdt_type_cd": "513",
      "std_pdno": "US04273H1041",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "",
      "sbsc_end_dt": "",
      "cash_alct_rt": "12.6000000000",
      "stck_alct_rt": "0.000000000000",
      "crcy_cd": "USD",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "0.12600",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240418",
      "rght_type_cd": "03",
      "pdno": "NORAM",
      "prdt_name": "NORAM DRILLING",
      "prdt_type_cd": "525",
      "std_pdno": "NO0010360019",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "",
      "sbsc_end_dt": "",
      "cash_alct_rt": "43.8000000000",
      "stck_alct_rt": "0.000000000000",
      "crcy_cd": "NOK",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "0.43800",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240418",
      "rght_type_cd": "15",
      "pdno": "BENF",
      "prdt_name": "BENEFICIENT",
      "prdt_type_cd": "512",
      "std_pdno": "US08178Q3092",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "",
      "sbsc_end_dt": "",
      "cash_alct_rt": "0.0000000000",
      "stck_alct_rt": "1.250000000000",
      "crcy_cd": "USD",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "0.00000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240418",
      "rght_type_cd": "15",
      "pdno": "NCNA",
      "prdt_name": "NUCANA PLC SPON ADR EACH REP 25 ORD SHS(POST SPLIT)",
      "prdt_type_cd": "512",
      "std_pdno": "US67022C2052",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "",
      "sbsc_end_dt": "",
      "cash_alct_rt": "0.0000000000",
      "stck_alct_rt": "4.000000000000",
      "crcy_cd": "USD",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "0.00000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240415",
      "rght_type_cd": "54",
      "pdno": "WWRSF",
      "prdt_name": "RIVERNORTH CAPITAL AND INCM FD INC",
      "prdt_type_cd": "513",
      "std_pdno": "USX589013472",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "20240415",
      "sbsc_end_dt": "20240417",
      "cash_alct_rt": "0.0000000000",
      "stck_alct_rt": "33.333340000000",
      "crcy_cd": "USD",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "15.28000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240411",
      "rght_type_cd": "74",
      "pdno": "FTF",
      "prdt_name": "FRANKLIN LIMITED DURATION INCOME TR",
      "prdt_type_cd": "529",
      "std_pdno": "US35472T1016",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "20240411",
      "sbsc_end_dt": "20240416",
      "cash_alct_rt": "0.0000000000",
      "stck_alct_rt": "0.000000000000",
      "crcy_cd": "USD",
      "crcy_cd2": "USD",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "0.00000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240411",
      "rght_type_cd": "74",
      "pdno": "TEI",
      "prdt_name": "TEMPLETON EMERGING MARKETS INC FD",
      "prdt_type_cd": "513",
      "std_pdno": "US8801921094",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "20240411",
      "sbsc_end_dt": "20240416",
      "cash_alct_rt": "0.0000000000",
      "stck_alct_rt": "0.000000000000",
      "crcy_cd": "USD",
      "crcy_cd2": "USD",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "0.00000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    },
    {
      "bass_dt": "20240418",
      "rght_type_cd": "75",
      "pdno": "AIR",
      "prdt_name": "AIRBUS GROUP NV",
      "prdt_type_cd": "542",
      "std_pdno": "NL0000235190",
      "acpl_bass_dt": "20240417",
      "sbsc_strt_dt": "",
      "sbsc_end_dt": "",
      "cash_alct_rt": "100.0000000000",
      "stck_alct_rt": "0.000000000000",
      "crcy_cd": "EUR",
      "crcy_cd2": "",
      "crcy_cd3": "",
      "crcy_cd4": "",
      "alct_frcr_unpr": "1.00000",
      "stkp_dvdn_frcr_amt2": "0.00000",
      "stkp_dvdn_frcr_amt3": "0.00000",
      "stkp_dvdn_frcr_amt4": "0.00000",
      "dfnt_yn": "Y"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
