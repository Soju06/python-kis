# 외국계 매매종목 가집계 [국내주식-161]

> [국내주식] 시세분석

외국계 매매종목 가집계 API입니다.
한국투자 HTS(eFriend Plus) > [0430] 외국계 매매종목 가집계 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f13f5e30-1065-451b-bcd3-06543b840a2e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/frgnmem-trade-estimate` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHKST644100C0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST644100C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | 시장구분코드 (J) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | Uniquekey (16441) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 0000(전체), 1001(코스피), 2001(코스닥) |
| `FID_RANK_SORT_CLS_CODE` | 순위정렬구분코드 | String | 2 | Y | 0(금액순), 1(수량순) |
| `FID_RANK_SORT_CLS_CODE_2` | 순위정렬구분코드2 | String | 2 | Y | 0(매수순), 1(매도순) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_COND_SCR_DIV_CODE:16441
FID_INPUT_ISCD:0000
FID_RANK_SORT_CLS_CODE:0
FID_RANK_SORT_CLS_CODE_2:0
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
| `stck_shrn_iscd` | 주식단축종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `glob_ntsl_qty` | 외국계순매도수량 | String | 12 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `glob_total_seln_qty` | 외국계총매도수량 | String | 18 | Y |  |
| `glob_total_shnu_qty` | 외국계총매수2수량 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_shrn_iscd": "005930",
            "hts_kor_isnm": "삼성전자",
            "glob_ntsl_qty": "3870530",
            "stck_prpr": "81300",
            "prdy_vrss": "3700",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.77",
            "acml_vol": "24892595",
            "glob_total_seln_qty": "547879",
            "glob_total_shnu_qty": "4418409"
        },
        {
            "stck_shrn_iscd": "000660",
            "hts_kor_isnm": "SK하이닉스",
            "glob_ntsl_qty": "964256",
            "stck_prpr": "179600",
            "prdy_vrss": "6400",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.70",
            "acml_vol": "4333233",
            "glob_total_seln_qty": "680043",
            "glob_total_shnu_qty": "1644299"
        },
        {
            "stck_shrn_iscd": "267260",
            "hts_kor_isnm": "HD현대일렉트릭",
            "glob_ntsl_qty": "329507",
            "stck_prpr": "252000",
            "prdy_vrss": "22000",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "9.57",
            "acml_vol": "955597",
            "glob_total_seln_qty": "87986",
            "glob_total_shnu_qty": "417493"
        },
        {
            "stck_shrn_iscd": "005935",
            "hts_kor_isnm": "삼성전자우",
            "glob_ntsl_qty": "455400",
            "stck_prpr": "66900",
            "prdy_vrss": "2300",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.56",
            "acml_vol": "1554888",
            "glob_total_seln_qty": "211634",
            "glob_total_shnu_qty": "667034"
        },
        {
            "stck_shrn_iscd": "011070",
            "hts_kor_isnm": "LG이노텍",
            "glob_ntsl_qty": "79842",
            "stck_prpr": "239500",
            "prdy_vrss": "5000",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "2.13",
            "acml_vol": "283787",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "79842"
        },
        {
            "stck_shrn_iscd": "012450",
            "hts_kor_isnm": "한화에어로스페이스",
            "glob_ntsl_qty": "56853",
            "stck_prpr": "218500",
            "prdy_vrss": "3000",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "1.39",
            "acml_vol": "334636",
            "glob_total_seln_qty": "15218",
            "glob_total_shnu_qty": "72071"
        },
        {
            "stck_shrn_iscd": "010140",
            "hts_kor_isnm": "삼성중공업",
            "glob_ntsl_qty": "1230023",
            "stck_prpr": "9600",
            "prdy_vrss": "210",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "2.24",
            "acml_vol": "7158181",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "1230023"
        },
        {
            "stck_shrn_iscd": "009150",
            "hts_kor_isnm": "삼성전기",
            "glob_ntsl_qty": "73431",
            "stck_prpr": "158000",
            "prdy_vrss": "6900",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.57",
            "acml_vol": "551401",
            "glob_total_seln_qty": "3452",
            "glob_total_shnu_qty": "76883"
        },
        {
            "stck_shrn_iscd": "316140",
            "hts_kor_isnm": "우리금융지주",
            "glob_ntsl_qty": "605764",
            "stck_prpr": "14190",
            "prdy_vrss": "60",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.42",
            "acml_vol": "2313443",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "605764"
        },
        {
            "stck_shrn_iscd": "010120",
            "hts_kor_isnm": "LS ELECTRIC",
            "glob_ntsl_qty": "47936",
            "stck_prpr": "164800",
            "prdy_vrss": "5000",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.13",
            "acml_vol": "787906",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "47936"
        },
        {
            "stck_shrn_iscd": "035420",
            "hts_kor_isnm": "NAVER",
            "glob_ntsl_qty": "35414",
            "stck_prpr": "194800",
            "prdy_vrss": "200",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.10",
            "acml_vol": "1270446",
            "glob_total_seln_qty": "3814",
            "glob_total_shnu_qty": "39228"
        },
        {
            "stck_shrn_iscd": "034020",
            "hts_kor_isnm": "두산에너빌리티",
            "glob_ntsl_qty": "407917",
            "stck_prpr": "17080",
            "prdy_vrss": "530",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.20",
            "acml_vol": "4896880",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "407917"
        },
        {
            "stck_shrn_iscd": "032830",
            "hts_kor_isnm": "삼성생명",
            "glob_ntsl_qty": "71420",
            "stck_prpr": "88300",
            "prdy_vrss": "4500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "5.37",
            "acml_vol": "428755",
            "glob_total_seln_qty": "106254",
            "glob_total_shnu_qty": "177674"
        },
        {
            "stck_shrn_iscd": "196170",
            "hts_kor_isnm": "알테오젠",
            "glob_ntsl_qty": "29877",
            "stck_prpr": "177300",
            "prdy_vrss": "100",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.06",
            "acml_vol": "848702",
            "glob_total_seln_qty": "902",
            "glob_total_shnu_qty": "30779"
        },
        {
            "stck_shrn_iscd": "031980",
            "hts_kor_isnm": "피에스케이홀딩스",
            "glob_ntsl_qty": "107530",
            "stck_prpr": "50500",
            "prdy_vrss": "3900",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "8.37",
            "acml_vol": "625360",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "107530"
        },
        {
            "stck_shrn_iscd": "036930",
            "hts_kor_isnm": "주성엔지니어링",
            "glob_ntsl_qty": "139898",
            "stck_prpr": "34950",
            "prdy_vrss": "600",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "1.75",
            "acml_vol": "782431",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "139898"
        },
        {
            "stck_shrn_iscd": "259960",
            "hts_kor_isnm": "크래프톤",
            "glob_ntsl_qty": "18822",
            "stck_prpr": "257500",
            "prdy_vrss": "6500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "2.59",
            "acml_vol": "192541",
            "glob_total_seln_qty": "20936",
            "glob_total_shnu_qty": "39758"
        },
        {
            "stck_shrn_iscd": "024110",
            "hts_kor_isnm": "기업은행",
            "glob_ntsl_qty": "296747",
            "stck_prpr": "13760",
            "prdy_vrss": "100",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.73",
            "acml_vol": "1259841",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "296747"
        },
        {
            "stck_shrn_iscd": "047810",
            "hts_kor_isnm": "한국항공우주",
            "glob_ntsl_qty": "75000",
            "stck_prpr": "53200",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "499071",
            "glob_total_seln_qty": "0",
            "glob_total_shnu_qty": "75000"
        },
        {
            "stck_shrn_iscd": "298040",
            "hts_kor_isnm": "효성중공업",
            "glob_ntsl_qty": "13317",
            "stck_prpr": "298000",
            "prdy_vrss": "9500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.29",
            "acml_vol": "127846",
            "glob_total_seln_qty": "435",
            "glob_total_shnu_qty": "13752"
        },
        {
            "stck_shrn_iscd": "000720",
            "hts_kor_isnm": "현대건설",
            "glob_ntsl_qty": "105515",
            "stck_prpr": "35600",
            "prdy_vrss": "350",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.99",
            "acml_vol": "383978",
            "glob_total_seln_qty": "9872",
            "glob_total_shnu_qty": "115387"
        },
        {
            "stck_shrn_iscd": "084370",
            "hts_kor_isnm": "유진테크",
            "glob_ntsl_qty": "60338",
            "stck_prpr": "57600",
            "prdy_vrss": "2200",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.97",
            "acml_vol": "242728",
            "glob_total_seln_qty": "18396",
            "glob_total_shnu_qty": "78734"
        },
        {
            "stck_shrn_iscd": "064350",
            "hts_kor_isnm": "현대로템",
            "glob_ntsl_qty": "91584",
            "stck_prpr": "38100",
            "prdy_vrss": "150",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.40",
            "acml_vol": "1032621",
            "glob_total_seln_qty": "2256",
            "glob_total_shnu_qty": "93840"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
