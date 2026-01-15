# 종합 시황/공시(제목) [국내주식-141]

> [국내주식] 업종/기타

종합 시황/공시(제목) API입니다. 
한국투자 HTS(eFriend Plus) > [0601] 종합 시황/공시 화면의 "우측 상단 리스트" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fbfe7300-7096-4938-840b-9f7c328cc5fd` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/news-title` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKST01011800` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12
- **최종 수정일**: 2025-05-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST01011800 |
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
| `FID_NEWS_OFER_ENTP_CODE` | 뉴스 제공 업체 코드 | String | 40 | Y | 공백 필수 입력 |
| `FID_COND_MRKT_CLS_CODE` | 조건 시장 구분 코드  | String | 6 | Y | 공백 필수 입력 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 공백: 전체, 종목코드 : 해당코드가 등록된 뉴스 |
| `FID_TITL_CNTT` | 제목 내용 | String | 132 | Y | 공백 필수 입력 |
| `FID_INPUT_DATE_1` | 입력 날짜 | String | 10 | Y | 공백: 현재기준, 조회일자(ex 00YYYYMMDD) |
| `FID_INPUT_HOUR_1` | 입력 시간 | String | 10 | Y | 공백: 현재기준, 조회시간(ex 0000HHMMSS) |
| `FID_RANK_SORT_CLS_CODE` | 순위 정렬 구분 코드 | String | 2 | Y | 공백 필수 입력 |
| `FID_INPUT_SRNO` | 입력 일련번호 | String | 20 | Y | 공백 필수 입력 |

### 요청 예시

```json
FID_NEWS_OFER_ENTP_CODE:
FID_COND_MRKT_CLS_CODE:
FID_INPUT_ISCD:
FID_TITL_CNTT:
FID_INPUT_DATE_1:
FID_INPUT_HOUR_1:
FID_RANK_SORT_CLS_CODE:
FID_INPUT_SRNO:
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
| `output` | 응답상세 | String | 200 | Y |  |
| `cntt_usiq_srno` | 내용 조회용 일련번호 | String | 20 | Y |  |
| `news_ofer_entp_code` | 뉴스 제공 업체 코드 | String | 1 | Y | '2'  /* 한경  news  */ '3'  /* 사용안함 */ '4'  /* 이데일리    */ '5'  /* 머니투데이  */ '6'  /* 연합뉴스    */ '7' ... |
| `data_dt` | 작성일자 | String | 8 | Y |  |
| `data_tm` | 작성시간 | String | 6 | Y |  |
| `hts_pbnt_titl_cntt` | HTS 공시 제목 내용 | String | 400 | Y |  |
| `news_lrdv_code` | 뉴스 대구분 | String | 8 | Y | 1:0:종합 1:FGHIN:공시 2:F:거래소 3:01:수시공시 3:02:공정공시 3:03:시장조치 3:04:신고사항 3:05:정기공시  3:06:특수공시   3:07:발행공... |
| `dorg` | 자료원 | String | 20 | Y |  |
| `iscd1` | 종목 코드1 | String | 9 | Y |  |
| `iscd2` | 종목 코드2 | String | 9 | Y |  |
| `iscd3` | 종목 코드3 | String | 9 | Y |  |
| `iscd4` | 종목 코드4 | String | 9 | Y |  |
| `iscd5` | 종목 코드5 | String | 9 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "cntt_usiq_srno": "2024041217173779111",
            "news_ofer_entp_code": "9",
            "data_dt": "20240412",
            "data_tm": "171737",
            "hts_pbnt_titl_cntt": "금융투자협회, 인도 기프트 시티 규제당국 IFSCA와 라운드테이블",
            "news_lrdv_code": "10",
            "dorg": "뉴스핌",
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
            "cntt_usiq_srno": "2024041217173438610",
            "news_ofer_entp_code": "5",
            "data_dt": "20240412",
            "data_tm": "171734",
            "hts_pbnt_titl_cntt": "미국 매출 90% 껑충…BBQ, 지난해 4730억원 사상최대 매출",
            "news_lrdv_code": "B02",
            "dorg": "머니투데이",
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
            "cntt_usiq_srno": "2024041217172998812",
            "news_ofer_entp_code": "9",
            "data_dt": "20240412",
            "data_tm": "171729",
            "hts_pbnt_titl_cntt": "한미-한국여자의사회 제정 '젊은의학자학술상'에 정선재 부교수",
            "news_lrdv_code": "10",
            "dorg": "뉴스핌",
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
            "cntt_usiq_srno": "2024041217165428809",
            "news_ofer_entp_code": "6",
            "data_dt": "20240412",
            "data_tm": "171654",
            "hts_pbnt_titl_cntt": "[亞증시-종합] 강달러 속 혼조",
            "news_lrdv_code": "03",
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
            "cntt_usiq_srno": "2024041217161911807",
            "news_ofer_entp_code": "5",
            "data_dt": "20240412",
            "data_tm": "171619",
            "hts_pbnt_titl_cntt": "골드팡, 'Hello Spring' 진행..최대 61% 할인 이벤트",
            "news_lrdv_code": "B02",
            "dorg": "머니투데이",
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
            "cntt_usiq_srno": "2024041217161867008",
            "news_ofer_entp_code": "7",
            "data_dt": "20240412",
            "data_tm": "171618",
            "hts_pbnt_titl_cntt": "자람테크놀로지, 임원ㆍ주요주주 특정증권등 소유주식수 변동",
            "news_lrdv_code": "02",
            "dorg": "인포스탁",
            "iscd1": "389020",
            "iscd2": "",
            "iscd3": "",
            "iscd4": "",
            "iscd5": "",
            "iscd6": "",
            "iscd7": "",
            "iscd8": "",
            "iscd9": "",
            "iscd10": "",
            "kor_isnm1": "자람테크놀로지",
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

