# 국내옵션전광판_옵션월물리스트[국내선물-020]

> [국내선물옵션] 기본시세

국내업종 국내옵션전광판_옵션월물리스트 API입니다. 
한국투자 HTS(eFriend Plus) > [0503] 선물옵션 종합시세(Ⅰ) 화면의 "월물리스트 목록 확인" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `89e1ffde-0cda-4426-8277-72710c193cf2` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/display-board-option-list` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPIO056104C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27T10:22:41+09:00
- **최종 수정일**: 2025-04-30T12:35:06+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPIO056104C0 |
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
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(509) |
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 공백 |
| `FID_COND_MRKT_CLS_CODE` | 조건 시장 구분 코드 | String | 6 | Y | 공백 |

### 요청 예시

```json
fid_cond_scr_div_code:509
fid_cond_mrkt_div_code:
fid_cond_mrkt_cls_code:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `mtrt_yymm_code` | 만기 년월 코드 | String | 6 | Y |  |
| `mtrt_yymm` | 만기 년월 | String | 6 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mtrt_yymm_code": "0V05",
      "mtrt_yymm": "202405"
    },
    {
      "mtrt_yymm_code": "0V06",
      "mtrt_yymm": "202406"
    },
    {
      "mtrt_yymm_code": "0V07",
      "mtrt_yymm": "202407"
    },
    {
      "mtrt_yymm_code": "0V08",
      "mtrt_yymm": "202408"
    },
    {
      "mtrt_yymm_code": "0V09",
      "mtrt_yymm": "202409"
    },
    {
      "mtrt_yymm_code": "0V10",
      "mtrt_yymm": "202410"
    },
    {
      "mtrt_yymm_code": "0V12",
      "mtrt_yymm": "202412"
    },
    {
      "mtrt_yymm_code": "0W03",
      "mtrt_yymm": "202503"
    },
    {
      "mtrt_yymm_code": "0W06",
      "mtrt_yymm": "202506"
    },
    {
      "mtrt_yymm_code": "0W12",
      "mtrt_yymm": "202512"
    },
    {
      "mtrt_yymm_code": "0612",
      "mtrt_yymm": "202612"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

