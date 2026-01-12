# ELW 만기예정/만기종목 [국내주식-184]

> [국내주식] ELW 시세

ELW 만기예정/만기종목 API입니다. 
한국투자 HTS(eFriend Plus) > [0290] ELW 만기예정/만기종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

최근 100건까지 데이터 조회 가능합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `d99d058d-4319-41ce-bce0-53c44a894ddb` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/expiration-stocks` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHKEW154700C0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-05-07

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKEW154700C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | W 입력 |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 11547 입력 |
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y | 입력날짜 ~ (ex) 20240402) |
| `FID_INPUT_DATE_2` | 입력날짜2 | String | 10 | Y | ~입력날짜 (ex) 20240408) |
| `FID_DIV_CLS_CODE` | 분류구분코드 | String | 2 | Y | 0(콜),1(풋),2(전체) |
| `FID_ETC_CLS_CODE` | 기타구분코드 | String | 2 | Y | 공백 입력 |
| `FID_UNAS_INPUT_ISCD` | 기초자산입력종목코드 | String | 12 | Y | 000000(전체), 2001(KOSPI 200), 기초자산코드(종목코드 ex. 삼성전자-005930) |
| `FID_INPUT_ISCD_2` | 발행회사코드 | String | 8 | Y | 00000(전체), 00003(한국투자증권), 00017(KB증권), 00005(미래에셋증권) |
| `FID_BLNG_CLS_CODE` | 결제방법 | String | 2 | Y | 0(전체),1(일반),2(조기종료) |
| `FID_INPUT_OPTION_1` | 입력옵션1 | String | 10 | Y | 공백 입력 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_COND_SCR_DIV_CODE:11547
FID_INPUT_DATE_1:20240611
FID_INPUT_DATE_2:20240618
FID_DIV_CLS_CODE:2
FID_ETC_CLS_CODE:
FID_UNAS_INPUT_ISCD:000000
FID_INPUT_ISCD_2:00000
FID_BLNG_CLS_CODE:0
FID_INPUT_OPTION_1:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `elw_shrn_iscd` | ELW단축종목코드 | String | 9 | Y |  |
| `elw_kor_isnm` | ELW한글종목명 | String | 40 | Y |  |
| `unas_isnm` | 기초자산종목명 | String | 40 | Y |  |
| `unas_prpr` | 기초자산현재가 | String | 112 | Y |  |
| `acpr` | 행사가 | String | 112 | Y |  |
| `stck_cnvr_rate` | 주식전환비율 | String | 136 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `stck_lstn_date` | 주식상장일자 | String | 8 | Y |  |
| `stck_last_tr_date` | 주식최종거래일자 | String | 8 | Y |  |
| `total_rdmp_amt` | 총상환금액 | String | 18 | Y |  |
| `rdmp_amt` | 상환금액 | String | 186 | Y |  |
| `lstn_stcn` | 상장주수 | String | 18 | Y |  |
| `lp_hvol` | LP보유량 | String | 18 | Y |  |
| `ccls_paym_prc` | 확정지급2가격 | String | 223 | Y |  |
| `mtrt_vltn_amt` | 만기평가금액 | String | 192 | Y |  |
| `evnt_prd_fin_date` | 행사2기간종료일자 | String | 8 | Y |  |
| `stlm_date` | 결제일자 | String | 8 | Y |  |
| `pblc_prc` | 발행가격 | String | 18 | Y |  |
| `unas_shrn_iscd` | 기초자산단축종목코드 | String | 9 | Y |  |
| `stnd_iscd` | 표준종목코드 | String | 12 | Y |  |
| `rdmp_ask_amt` | 상환청구금액 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "elw_shrn_iscd": "58K374",
            "elw_kor_isnm": "KBK374KOSPI200풋",
            "unas_isnm": "KOSPI200",
            "unas_prpr": "367.71",
            "acpr": "372.50",
            "stck_cnvr_rate": "100.000000",
            "elw_prpr": "515",
            "stck_lstn_date": "20240320",
            "stck_last_tr_date": "20240613",
            "total_rdmp_amt": "0",
            "rdmp_amt": "0.000000",
            "lstn_stcn": "5000000",
            "lp_hvol": "4982390",
            "ccls_paym_prc": "0.000",
            "mtrt_vltn_amt": "367.71",
            "evnt_prd_fin_date": "20240617",
            "stlm_date": "20240619",
            "pblc_prc": "1143",
            "unas_shrn_iscd": "2001",
            "stnd_iscd": "KRA583261E30",
            "rdmp_ask_amt": ""
        },
        {
            "elw_shrn_iscd": "58K373",
            "elw_kor_isnm": "KBK373KOSPI200풋",
            "unas_isnm": "KOSPI200",
            "unas_prpr": "367.71",
            "acpr": "370.00",
            "stck_cnvr_rate": "100.000000",
            "elw_prpr": "370",
            "stck_lstn_date": "20240320",
            "stck_last_tr_date": "20240613",
            "total_rdmp_amt": "0",
            "rdmp_amt": "0.000000",
            "lstn_stcn": "5000000",
            "lp_hvol": "4727930",
            "ccls_paym_prc": "0.000",
            "mtrt_vltn_amt": "367.71",
            "evnt_prd_fin_date": "20240617",
            "stlm_date": "20240619",
            "pblc_prc": "901",
            "unas_shrn_iscd": "2001",
            "stnd_iscd": "KRA583260E31",
            "rdmp_ask_amt": ""
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
