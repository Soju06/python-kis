# 해외속보(제목) [해외주식-055]

> [해외주식] 시세분석

해외속보(제목) API입니다.
한국투자 HTS(eFriend Plus) > [7704] 해외속보 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

최대 100건까지 조회 가능합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `b73a4cdf-402b-4e11-a161-609ea9451835` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/brknews-title` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHKST01011801` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17T10:28:33+09:00
- **최종 수정일**: 2025-05-15T10:33:21+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST01011801 |
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
| `FID_NEWS_OFER_ENTP_CODE` | 뉴스제공업체코드 | String | 40 | Y | 뉴스제공업체구분=>0:전체조회 |
| `FID_COND_MRKT_CLS_CODE` | 조건시장구분코드 | String | 6 | Y | 공백 |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 공백 |
| `FID_TITL_CNTT` | 제목내용 | String | 132 | Y | 공백 |
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y | 공백 |
| `FID_INPUT_HOUR_1` | 입력시간1 | String | 10 | Y | 공백 |
| `FID_RANK_SORT_CLS_CODE` | 순위정렬구분코드 | String | 2 | Y | 공백 |
| `FID_INPUT_SRNO` | 입력일련번호 | String | 20 | Y | 공백 |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 화면번호:11801 |

### 요청 예시

```json
FID_NEWS_OFER_ENTP_CODE:0
FID_COND_MRKT_CLS_CODE:00
FID_INPUT_ISCD:
FID_TITL_CNTT:
FID_INPUT_DATE_1:
FID_INPUT_HOUR_1:
FID_RANK_SORT_CLS_CODE:
FID_INPUT_SRNO:
FID_COND_SCR_DIV_CODE:11801
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
| `cntt_usiq_srno` | 내용조회용일련번호 | String | 20 | Y |  |
| `news_ofer_entp_code` | 뉴스제공업체코드 | String | 1 | Y |  |
| `data_dt` | 작성일자 | String | 8 | Y |  |
| `data_tm` | 작성시간 | String | 6 | Y |  |
| `hts_pbnt_titl_cntt` | HTS공시제목내용 | String | 400 | Y |  |
| `news_lrdv_code` | 뉴스대구분 | String | 8 | Y |  |
| `dorg` | 자료원 | String | 20 | Y |  |
| `iscd1` | 종목코드1 | String | 9 | Y |  |
| `iscd2` | 종목코드2 | String | 9 | Y |  |
| `iscd3` | 종목코드3 | String | 9 | Y |  |
| `iscd4` | 종목코드4 | String | 9 | Y |  |
| `iscd5` | 종목코드5 | String | 9 | Y |  |
| `iscd6` | 종목코드6 | String | 9 | Y |  |
| `iscd7` | 종목코드7 | String | 9 | Y |  |
| `iscd8` | 종목코드8 | String | 9 | Y |  |
| `iscd9` | 종목코드9 | String | 9 | Y |  |
| `iscd10` | 종목코드10 | String | 9 | Y |  |
| `kor_isnm1` | 한글종목명1 | String | 40 | Y |  |
| `kor_isnm2` | 한글종목명2 | String | 40 | Y |  |
| `kor_isnm3` | 한글종목명3 | String | 40 | Y |  |
| `kor_isnm4` | 한글종목명4 | String | 40 | Y |  |
| `kor_isnm5` | 한글종목명5 | String | 40 | Y |  |
| `kor_isnm6` | 한글종목명6 | String | 40 | Y |  |
| `kor_isnm7` | 한글종목명7 | String | 40 | Y |  |
| `kor_isnm8` | 한글종목명8 | String | 40 | Y |  |
| `kor_isnm9` | 한글종목명9 | String | 40 | Y |  |
| `kor_isnm10` | 한글종목명10 | String | 40 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "cntt_usiq_srno": "2024052817340622954",
            "news_ofer_entp_code": "U",
            "data_dt": "20240528",
            "data_tm": "173406",
            "hts_pbnt_titl_cntt": "“시진핑, 기업인들 만나 신에너지 분야 과잉투자 경고”",
            "news_lrdv_code": "38",
            "dorg": "서울경제",
            "iscd1": "",
            "iscd2": "",
            "iscd3": "",
            "iscd4": "",
            "iscd5": "",
            "iscd6": "",
            "iscd7": "",
            "iscd8": "",
            "iscd9": "",
            "iscd10": "",
            "kor_isnm1": " ",
            "kor_isnm2": "",
            "kor_isnm3": "",
            "kor_isnm4": "",
            "kor_isnm5": "",
            "kor_isnm6": "",
            "kor_isnm7": "",
            "kor_isnm8": "",
            "kor_isnm9": "",
            "kor_isnm10": ""
        },
        {
            "cntt_usiq_srno": "2024052817332725534",
            "news_ofer_entp_code": "6",
            "data_dt": "20240528",
            "data_tm": "173327",
            "hts_pbnt_titl_cntt": "군부대 찾은 라이칭더, 中포위훈련 언급하며 \"모두 잘 대응\"",
            "news_lrdv_code": "11",
            "dorg": "연합뉴스",
            "iscd1": "",
            "iscd2": "",
            "iscd3": "",
            "iscd4": "",
            "iscd5": "",
            "iscd6": "",
            "iscd7": "",
            "iscd8": "",
            "iscd9": "",
            "iscd10": "",
            "kor_isnm1": " ",
            "kor_isnm2": "",
            "kor_isnm3": "",
            "kor_isnm4": "",
            "kor_isnm5": "",
            "kor_isnm6": "",
            "kor_isnm7": "",
            "kor_isnm8": "",
            "kor_isnm9": "",
            "kor_isnm10": ""
        },
        {
            "cntt_usiq_srno": "2024052817332721133",
            "news_ofer_entp_code": "6",
            "data_dt": "20240528",
            "data_tm": "173327",
            "hts_pbnt_titl_cntt": "적십자 \"기후변화로 '극단적 더위' 일수 1년 새 26일 증가\"",
            "news_lrdv_code": "11",
            "dorg": "연합뉴스",
            "iscd1": "",
            "iscd2": "",
            "iscd3": "",
            "iscd4": "",
            "iscd5": "",
            "iscd6": "",
            "iscd7": "",
            "iscd8": "",
            "iscd9": "",
            "iscd10": "",
            "kor_isnm1": " ",
            "kor_isnm2": "",
            "kor_isnm3": "",
            "kor_isnm4": "",
            "kor_isnm5": "",
            "kor_isnm6": "",
            "kor_isnm7": "",
            "kor_isnm8": "",
            "kor_isnm9": "",
            "kor_isnm10": ""
        },
        {
            "cntt_usiq_srno": "2024052817312094823",
            "news_ofer_entp_code": "6",
            "data_dt": "20240528",
            "data_tm": "173120",
            "hts_pbnt_titl_cntt": "미국제재 우려했나…중국 하이크비전, 러시아 사업 중단설",
            "news_lrdv_code": "11",
            "dorg": "연합뉴스",
            "iscd1": "",
            "iscd2": "",
            "iscd3": "",
            "iscd4": "",
            "iscd5": "",
            "iscd6": "",
            "iscd7": "",
            "iscd8": "",
            "iscd9": "",
            "iscd10": "",
            "kor_isnm1": " ",
            "kor_isnm2": "",
            "kor_isnm3": "",
            "kor_isnm4": "",
            "kor_isnm5": "",
            "kor_isnm6": "",
            "kor_isnm7": "",
            "kor_isnm8": "",
            "kor_isnm9": "",
            "kor_isnm10": ""
        },
        {
            "cntt_usiq_srno": "2024052817304250020",
            "news_ofer_entp_code": "8",
            "data_dt": "20240528",
            "data_tm": "173042",
            "hts_pbnt_titl_cntt": "[유럽개장]장 초반 혼조세…獨 0.25%↑",
            "news_lrdv_code": "10",
            "dorg": "아시아 경제",
            "iscd1": "",
            "iscd2": "",
            "iscd3": "",
            "iscd4": "",
            "iscd5": "",
            "iscd6": "",
            "iscd7": "",
            "iscd8": "",
            "iscd9": "",
            "iscd10": "",
            "kor_isnm1": " ",
            "kor_isnm2": "",
            "kor_isnm3": "",
            "kor_isnm4": "",
            "kor_isnm5": "",
            "kor_isnm6": "",
            "kor_isnm7": "",
            "kor_isnm8": "",
            "kor_isnm9": "",
            "kor_isnm10": ""
        },
        {
            "cntt_usiq_srno": "2024052817264510344",
            "news_ofer_entp_code": "A",
            "data_dt": "20240528",
            "data_tm": "172645",
            "hts_pbnt_titl_cntt": "122m 협곡 아래로 떨어졌는데 멀쩡하디니…기적 일어난 美 10대",
            "news_lrdv_code": "10",
            "dorg": "매일경제",
            "iscd1": "",
            "iscd2": "",
            "iscd3": "",
            "iscd4": "",
            "iscd5": "",
            "iscd6": "",
            "iscd7": "",
            "iscd8": "",
            "iscd9": "",
            "iscd10": "",
            "kor_isnm1": " ",
            "kor_isnm2": "",
            "kor_isnm3": "",
            "kor_isnm4": "",
            "kor_isnm5": "",
            "kor_isnm6": "",
            "kor_isnm7": "",
            "kor_isnm8": "",
            "kor_isnm9": "",
            "kor_isnm10": ""
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

