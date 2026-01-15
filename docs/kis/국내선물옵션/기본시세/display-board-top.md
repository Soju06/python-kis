# 국내선물 기초자산 시세[국내선물-021]

> [국내선물옵션] 기본시세

국내선물 기초자산 시세 API입니다. 
한국투자 HTS(eFriend Plus) > [0503] 선물옵션 종합시세(Ⅰ) 화면의 "상단 바" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4112fd5d-43b7-4dc4-bf44-33df58981847` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/display-board-top` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHPIF05030000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPIF05030000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (F: 선물) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 선물최근월물 ex)(101V06) |
| `FID_COND_MRKT_DIV_CODE1` | 조건 시장 분류 코드 | String | 2 | Y | 공백 |
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | 공백 |
| `FID_MTRT_CNT` | 만기 수 | String | 11 | Y | 공백 |
| `FID_COND_MRKT_CLS_CODE` | 조건 시장 구분 코드 | String | 6 | Y | 공백 |

### 요청 예시

```json
fid_cond_mrkt_div_code:F
fid_input_iscd:101V06
fid_cond_mrkt_div_code1:
fid_cond_scr_div_code:
fid_mtrt_cnt:
fid_cond_mrkt_cls_code:
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
| `output1` | 응답상세 | String |   | Y |  |
| `unas_prpr` | 기초자산 현재가 | String | 112 | Y |  |
| `unas_prdy_vrss` | 기초자산 전일 대비 | String | 112 | Y |  |
| `unas_prdy_vrss_sign` | 기초자산 전일 대비 부호 | String | 1 | Y |  |
| `unas_prdy_ctrt` | 기초자산 전일 대비율 | String | 82 | Y |  |
| `unas_acml_vol` | 기초자산 누적 거래량 | String | 18 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `futs_prpr` | 선물 현재가 | String | 112 | Y |  |
| `futs_prdy_vrss` | 선물 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `futs_prdy_ctrt` | 선물 전일 대비율 | String | 82 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `hts_rmnn_dynu` | HTS 잔존 일수 | String | 5 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "unas_prpr": "367.25",
    "unas_prdy_vrss": "-3.47",
    "unas_prdy_vrss_sign": "5",
    "unas_prdy_ctrt": "-0.94",
    "unas_acml_vol": "161725000",
    "hts_kor_isnm": "F 202406",
    "futs_prpr": "369.35",
    "futs_prdy_vrss": "-3.45",
    "prdy_vrss_sign": "5",
    "futs_prdy_ctrt": "-0.93"
  },
  "output2": [],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
