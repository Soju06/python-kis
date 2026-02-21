# ELW 신규상장종목 [국내주식-181]

> [국내주식] ELW 시세

ELW 신규상장종목 API입니다. 
한국투자 HTS(eFriend Plus) > [0297] ELW 신규상장종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `147e81db-e0d2-40cd-95f5-d8da90c2d998` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/newly-listed` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKEW154800C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12T12:36:57+09:00
- **최종 수정일**: 2025-05-07T09:31:20+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKEW154800C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | 시장구분코드 (W) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | Unique key(11548) |
| `FID_DIV_CLS_CODE` | 분류구분코드 | String | 2 | Y | 전체(02), 콜(00), 풋(01) |
| `FID_UNAS_INPUT_ISCD` | 기초자산입력종목코드 | String | 12 | Y | 'ex) 000000(전체), 2001(코스피200) , 3003(코스닥150), 005930(삼성전자) ' |
| `FID_INPUT_ISCD_2` | 입력종목코드2 | String | 8 | Y | '00003(한국투자증권), 00017(KB증권),  00005(미래에셋증권)' |
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y | 날짜 (ex) 20240402) |
| `FID_BLNC_CLS_CODE` | 결재방법 | String | 2 | Y | 0(전체), 1(일반), 2(조기종료) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_COND_SCR_DIV_CODE:11548
FID_DIV_CLS_CODE:02
FID_UNAS_INPUT_ISCD:000000
FID_INPUT_ISCD_2:00003
FID_INPUT_DATE_1:20240410
FID_BLNG_CLS_CODE:0
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
| `output` | 응답상세 | Object |   | Y | array |
| `stck_lstn_date` | 주식상장일자 | String | 8 | Y |  |
| `elw_kor_isnm` | ELW한글종목명 | String | 40 | Y |  |
| `elw_shrn_iscd` | ELW단축종목코드 | String | 9 | Y |  |
| `unas_isnm` | 기초자산종목명 | String | 40 | Y |  |
| `pblc_co_name` | 발행회사명 | String | 40 | Y |  |
| `lstn_stcn` | 상장주수 | String | 18 | Y |  |
| `acpr` | 행사가 | String | 112 | Y |  |
| `stck_last_tr_date` | 주식최종거래일자 | String | 8 | Y |  |
| `elw_ko_barrier` | 조기종료발생기준가격 | String | 112 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K924HLB콜",
            "elw_shrn_iscd": "57K924",
            "unas_isnm": "HLB",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "7100000",
            "acpr": "78000.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K925HMM콜",
            "elw_shrn_iscd": "57K925",
            "unas_isnm": "HMM",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "6700000",
            "acpr": "20000.00",
            "stck_last_tr_date": "20240912",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K926HMM콜",
            "elw_shrn_iscd": "57K926",
            "unas_isnm": "HMM",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "5600000",
            "acpr": "20000.00",
            "stck_last_tr_date": "20241212",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KB45HMM풋",
            "elw_shrn_iscd": "57KB45",
            "unas_isnm": "HMM",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "6900000",
            "acpr": "17700.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K927KB금융콜",
            "elw_shrn_iscd": "57K927",
            "unas_isnm": "KB금융",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "24400000",
            "acpr": "73600.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K928KB금융콜",
            "elw_shrn_iscd": "57K928",
            "unas_isnm": "KB금융",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "22300000",
            "acpr": "73600.00",
            "stck_last_tr_date": "20240912",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K929KB금융콜",
            "elw_shrn_iscd": "57K929",
            "unas_isnm": "KB금융",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "18200000",
            "acpr": "72000.00",
            "stck_last_tr_date": "20240711",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K930KB금융콜",
            "elw_shrn_iscd": "57K930",
            "unas_isnm": "KB금융",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "20000000",
            "acpr": "70500.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국K931KB금융콜",
            "elw_shrn_iscd": "57K931",
            "unas_isnm": "KB금융",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "15700000",
            "acpr": "69000.00",
            "stck_last_tr_date": "20240711",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KB46KB금융풋",
            "elw_shrn_iscd": "57KB46",
            "unas_isnm": "KB금융",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "11200000",
            "acpr": "65000.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KB47KB금융풋",
            "elw_shrn_iscd": "57KB47",
            "unas_isnm": "KB금융",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "12000000",
            "acpr": "63700.00",
            "stck_last_tr_date": "20240711",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KB98KOSPI200풋",
            "elw_shrn_iscd": "57KB98",
            "unas_isnm": "KOSPI200",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "7000000",
            "acpr": "400.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KB99KOSPI200풋",
            "elw_shrn_iscd": "57KB99",
            "unas_isnm": "KOSPI200",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "7000000",
            "acpr": "395.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KC00KOSPI200풋",
            "elw_shrn_iscd": "57KC00",
            "unas_isnm": "KOSPI200",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "7000000",
            "acpr": "390.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KC01KOSPI200풋",
            "elw_shrn_iscd": "57KC01",
            "unas_isnm": "KOSPI200",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "9000000",
            "acpr": "387.50",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KC02KOSPI200풋",
            "elw_shrn_iscd": "57KC02",
            "unas_isnm": "KOSPI200",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "10000000",
            "acpr": "385.00",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },
        {
            "stck_lstn_date": "20240320",
            "elw_kor_isnm": "한국KC03KOSPI200풋",
            "elw_shrn_iscd": "57KC03",
            "unas_isnm": "KOSPI200",
            "pblc_co_name": "한국투자증권(주)",
            "lstn_stcn": "9000000",
            "acpr": "382.50",
            "stck_last_tr_date": "20240613",
            "elw_ko_barrier": "0.00"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

