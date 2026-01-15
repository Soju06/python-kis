# 장내채권 기간별시세(일) [국내주식-159]

> [장내채권] 기본시세

장내채권 기간별시세(일) API입니다. 
한국투자 HTS(eFriend Plus) > [0979] 장내채권종합주문 화면 가운데 "일별" 클릭 시 시세 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 

최근 30건까지 데이터 확인이 가능합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f5dcbbc3-bee6-4b83-a236-5f3a5bb59d72` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/quotations/inquire-daily-itemchartprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKBJ773701C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
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
| `tr_id` | 거래ID | String | 13 | Y | FHKBJ773701C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 구분 코드  | String | 6 | Y | Unique key(B) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:B
FID_INPUT_ISCD:KR101501D967
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
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `bond_oprc` | 채권시가2 | String | 112 | Y |  |
| `bond_hgpr` | 채권고가 | String | 112 | Y |  |
| `bond_lwpr` | 채권저가 | String | 112 | Y |  |
| `bond_prpr` | 채권현재가 | String | 112 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_bsop_date": "20240610",
      "bond_oprc": "0.00",
      "bond_hgpr": "0.00",
      "bond_lwpr": "0.00",
      "bond_prpr": "10997.10",
      "acml_vol": "0"
    },
    {
      "stck_bsop_date": "20240607",
      "bond_oprc": "10997.10",
      "bond_hgpr": "10997.10",
      "bond_lwpr": "10997.10",
      "bond_prpr": "10997.10",
      "acml_vol": "119"
    },
    {
      "stck_bsop_date": "20240605",
      "bond_oprc": "10997.50",
      "bond_hgpr": "10997.50",
      "bond_lwpr": "10997.50",
      "bond_prpr": "10997.50",
      "acml_vol": "97"
    },
    {
      "stck_bsop_date": "20240530",
      "bond_oprc": "10860.00",
      "bond_hgpr": "10860.00",
      "bond_lwpr": "10860.00",
      "bond_prpr": "10860.00",
      "acml_vol": "46"
    },
    {
      "stck_bsop_date": "20240529",
      "bond_oprc": "10873.00",
      "bond_hgpr": "10873.00",
      "bond_lwpr": "10873.00",
      "bond_prpr": "10873.00",
      "acml_vol": "3"
    },
    {
      "stck_bsop_date": "20240528",
      "bond_oprc": "8540.00",
      "bond_hgpr": "10700.00",
      "bond_lwpr": "8540.00",
      "bond_prpr": "10700.00",
      "acml_vol": "49"
    },
    {
      "stck_bsop_date": "20240520",
      "bond_oprc": "10867.70",
      "bond_hgpr": "10867.70",
      "bond_lwpr": "10867.70",
      "bond_prpr": "10867.70",
      "acml_vol": "14"
    },
    {
      "stck_bsop_date": "20240517",
      "bond_oprc": "10850.40",
      "bond_hgpr": "10850.40",
      "bond_lwpr": "10850.40",
      "bond_prpr": "10850.40",
      "acml_vol": "1015"
    },
    {
      "stck_bsop_date": "20240514",
      "bond_oprc": "10861.80",
      "bond_hgpr": "10863.50",
      "bond_lwpr": "10861.80",
      "bond_prpr": "10863.50",
      "acml_vol": "17549"
    },
    {
      "stck_bsop_date": "20240513",
      "bond_oprc": "10844.30",
      "bond_hgpr": "10861.10",
      "bond_lwpr": "10844.30",
      "bond_prpr": "10861.10",
      "acml_vol": "1963"
    },
    {
      "stck_bsop_date": "20240510",
      "bond_oprc": "10858.00",
      "bond_hgpr": "10858.00",
      "bond_lwpr": "10858.00",
      "bond_prpr": "10858.00",
      "acml_vol": "12"
    },
    {
      "stck_bsop_date": "20240509",
      "bond_oprc": "10857.00",
      "bond_hgpr": "10857.00",
      "bond_lwpr": "10857.00",
      "bond_prpr": "10857.00",
      "acml_vol": "2"
    },
    {
      "stck_bsop_date": "20240508",
      "bond_oprc": "10856.20",
      "bond_hgpr": "10856.20",
      "bond_lwpr": "10856.20",
      "bond_prpr": "10856.20",
      "acml_vol": "11"
    },
    {
      "stck_bsop_date": "20240424",
      "bond_oprc": "10820.70",
      "bond_hgpr": "10820.70",
      "bond_lwpr": "10820.70",
      "bond_prpr": "10820.70",
      "acml_vol": "931"
    },
    {
      "stck_bsop_date": "20240423",
      "bond_oprc": "10818.60",
      "bond_hgpr": "10819.00",
      "bond_lwpr": "10818.60",
      "bond_prpr": "10819.00",
      "acml_vol": "3708"
    },
    {
      "stck_bsop_date": "20240422",
      "bond_oprc": "10817.60",
      "bond_hgpr": "10823.00",
      "bond_lwpr": "10817.60",
      "bond_prpr": "10823.00",
      "acml_vol": "13959"
    },
    {
      "stck_bsop_date": "20240308",
      "bond_oprc": "10756.00",
      "bond_hgpr": "10788.00",
      "bond_lwpr": "10756.00",
      "bond_prpr": "10788.00",
      "acml_vol": "20"
    },
    {
      "stck_bsop_date": "20231108",
      "bond_oprc": "10600.00",
      "bond_hgpr": "10600.00",
      "bond_lwpr": "10600.00",
      "bond_prpr": "10600.00",
      "acml_vol": "949"
    },
    {
      "stck_bsop_date": "20231018",
      "bond_oprc": "10570.00",
      "bond_hgpr": "10620.00",
      "bond_lwpr": "10570.00",
      "bond_prpr": "10620.00",
      "acml_vol": "1890"
    },
    {
      "stck_bsop_date": "20231013",
      "bond_oprc": "10592.00",
      "bond_hgpr": "10630.00",
      "bond_lwpr": "10592.00",
      "bond_prpr": "10630.00",
      "acml_vol": "10714"
    },
    {
      "stck_bsop_date": "20231012",
      "bond_oprc": "10541.00",
      "bond_hgpr": "10592.00",
      "bond_lwpr": "10541.00",
      "bond_prpr": "10592.00",
      "acml_vol": "5691"
    },
    {
      "stck_bsop_date": "20230926",
      "bond_oprc": "10615.70",
      "bond_hgpr": "10615.70",
      "bond_lwpr": "10615.70",
      "bond_prpr": "10615.70",
      "acml_vol": "4731"
    },
    {
      "stck_bsop_date": "20230914",
      "bond_oprc": "10579.00",
      "bond_hgpr": "10579.00",
      "bond_lwpr": "10579.00",
      "bond_prpr": "10579.00",
      "acml_vol": "10"
    },
    {
      "stck_bsop_date": "20230913",
      "bond_oprc": "10501.00",
      "bond_hgpr": "10501.00",
      "bond_lwpr": "10501.00",
      "bond_prpr": "10501.00",
      "acml_vol": "9"
    },
    {
      "stck_bsop_date": "20230912",
      "bond_oprc": "10499.10",
      "bond_hgpr": "10540.00",
      "bond_lwpr": "10499.10",
      "bond_prpr": "10499.10",
      "acml_vol": "30"
    },
    {
      "stck_bsop_date": "20230829",
      "bond_oprc": "10389.00",
      "bond_hgpr": "10389.00",
      "bond_lwpr": "10389.00",
      "bond_prpr": "10389.00",
      "acml_vol": "4761"
    },
    {
      "stck_bsop_date": "20230825",
      "bond_oprc": "10550.00",
      "bond_hgpr": "10550.00",
      "bond_lwpr": "10550.00",
      "bond_prpr": "10550.00",
      "acml_vol": "12555"
    },
    {
      "stck_bsop_date": "20230818",
      "bond_oprc": "10299.20",
      "bond_hgpr": "10299.20",
      "bond_lwpr": "10299.20",
      "bond_prpr": "10299.20",
      "acml_vol": "2838"
    },
    {
      "stck_bsop_date": "20230814",
      "bond_oprc": "10350.00",
      "bond_hgpr": "10450.00",
      "bond_lwpr": "10350.00",
      "bond_prpr": "10450.00",
      "acml_vol": "2838"
    },
    {
      "stck_bsop_date": "20230720",
      "bond_oprc": "10527.00",
      "bond_hgpr": "10527.00",
      "bond_lwpr": "10527.00",
      "bond_prpr": "10527.00",
      "acml_vol": "18"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

