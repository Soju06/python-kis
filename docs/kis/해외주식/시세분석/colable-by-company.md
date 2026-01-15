# 당사 해외주식담보대출 가능 종목 [해외주식-051]

> [해외주식] 시세분석

당사 해외주식담보대출 가능 종목 API입니다.
한국투자 HTS(eFriend Plus) > [0497] 당사 해외주식담보대출 가능 종목 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

한 번의 호출에 20건까지 조회가 가능하며 다음조회가 불가하기에, PDNO에 데이터 확인하고자 하는 종목코드를 입력하여 단건조회용으로 사용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `967e60c7-f1eb-4f23-b893-71747556ad49` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/colable-by-company` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `CTLN4050R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17
- **최종 수정일**: 2025-05-15

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTLN4050R |
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
| `PDNO` | 상품번호 | String | 12 | Y | ex)AMD |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | 공백 |
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y | 공백 |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y | 공백 |
| `INQR_DVSN` | 조회구분 | String | 2 | Y | 공백 |
| `NATN_CD` | 국가코드 | String | 3 | Y | 840(미국), 344(홍콩), 156(중국) |
| `INQR_SQN_DVSN` | 조회순서구분 | String | 2 | Y | 01(이름순), 02(코드순) |
| `RT_DVSN_CD` | 비율구분코드 | String | 2 | Y | 공백 |
| `RT` | 비율 | String | 238 | Y | 공백 |
| `LOAN_PSBL_YN` | 대출가능여부 | String | 1 | Y | 공백 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y | 공백 |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y | 공백 |

### 요청 예시

```json
PDNO:AMD
PRDT_TYPE_CD:
INQR_STRT_DT:
INQR_END_DT:
INQR_DVSN:
NATN_CD:840
INQR_SQN_DVSN:02
RT_DVSN_CD:
RT:
LOAN_PSBL_YN:
CTX_AREA_FK100:
CTX_AREA_NK100:
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
| `pdno` | 상품번호 | String | 12 | Y |  |
| `ovrs_item_name` | 해외종목명 | String | 60 | Y |  |
| `loan_rt` | 대출비율 | String | 238 | Y |  |
| `mgge_mntn_rt` | 담보유지비율 | String | 238 | Y |  |
| `mgge_ensu_rt` | 담보확보비율 | String | 238 | Y |  |
| `loan_exec_psbl_yn` | 대출실행가능여부 | String | 1 | Y |  |
| `stff_name` | 직원명 | String | 60 | Y |  |
| `erlm_dt` | 등록일자 | String | 8 | Y |  |
| `tr_mket_name` | 거래시장명 | String | 60 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `natn_kor_name` | 국가한글명 | String | 60 | Y |  |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | Y |  |
| `output2` | 응답상세 | String |   | Y | array |
| `loan_psbl_item_num` | 대출가능종목수 | String | 20 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "AMD!^!^!^!^!^840!^02                                                                                ",
  "ctx_area_nk100": "                                                                                                    ",
  "output1": [
    {
      "pdno": "AMD",
      "ovrs_item_name": "AMD",
      "loan_rt": "50.00000000",
      "mgge_mntn_rt": "170.00000000",
      "mgge_ensu_rt": "170.00000000",
      "loan_exec_psbl_yn": "Y",
      "stff_name": "109477.석재민",
      "erlm_dt": "20221230",
      "tr_mket_name": "나스닥",
      "crcy_cd": "USD",
      "natn_kor_name": "미국",
      "ovrs_excg_cd": "NASD"
    }
  ],
  "output2": {
    "loan_psbl_item_num": "403"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```

