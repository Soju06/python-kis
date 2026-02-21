# 장내채권현재가(일별) [국내주식-202]

> [장내채권] 기본시세

장내채권현재가(일별) API입니다. 
장내채권의 일별 시세데이터를 최근 100건까지 확인할 수 있습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/quotations/inquire-daily-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKBJ773404C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26T09:31:48+09:00
- **최종 수정일**: 2025-04-30T13:08:39+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKBJ773404C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | B (업종코드) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 채권종목코드(ex KR2033022D33) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:B
FID_INPUT_ISCD:KR6095572D81
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
| `output` | 응답상세 | String |   | Y |  |
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `bond_prpr` | 채권현재가 | String | 112 | Y |  |
| `bond_prdy_vrss` | 채권전일대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `bond_oprc` | 채권시가2 | String | 112 | Y |  |
| `bond_hgpr` | 채권고가 | String | 112 | Y |  |
| `bond_lwpr` | 채권저가 | String | 112 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240503",
            "bond_prpr": "10265.00",
            "bond_prdy_vrss": "-15.00",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.15",
            "acml_vol": "110000",
            "bond_oprc": "10265.00",
            "bond_hgpr": "10265.00",
            "bond_lwpr": "10265.00"
        },
        {
            "stck_bsop_date": "20240502",
            "bond_prpr": "10280.00",
            "bond_prdy_vrss": "-145.00",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-1.39",
            "acml_vol": "61278",
            "bond_oprc": "10280.00",
            "bond_hgpr": "10280.00",
            "bond_lwpr": "10280.00"
        },
        {
            "stck_bsop_date": "20240430",
            "bond_prpr": "10425.00",
            "bond_prdy_vrss": "5.00",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.05",
            "acml_vol": "5012",
            "bond_oprc": "10425.00",
            "bond_hgpr": "10425.00",
            "bond_lwpr": "10425.00"
        },
        {
            "stck_bsop_date": "20240429",
            "bond_prpr": "10420.00",
            "bond_prdy_vrss": "-30.00",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.29",
            "acml_vol": "9999",
            "bond_oprc": "10420.00",
            "bond_hgpr": "10420.00",
            "bond_lwpr": "10420.00"
        },
        {
            "stck_bsop_date": "20240426",
            "bond_prpr": "10450.00",
            "bond_prdy_vrss": "10.30",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.10",
            "acml_vol": "102001",
            "bond_oprc": "10430.00",
            "bond_hgpr": "10450.00",
            "bond_lwpr": "10430.00"
        },
        {
            "stck_bsop_date": "20240425",
            "bond_prpr": "10439.70",
            "bond_prdy_vrss": "39.70",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.38",
            "acml_vol": "5718",
            "bond_oprc": "10290.00",
            "bond_hgpr": "10439.70",
            "bond_lwpr": "10290.00"
        },
        {
            "stck_bsop_date": "20240424",
            "bond_prpr": "10400.00",
            "bond_prdy_vrss": "-100.00",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.95",
            "acml_vol": "3000",
            "bond_oprc": "10400.00",
            "bond_hgpr": "10400.00",
            "bond_lwpr": "10400.00"
        },
        {
            "stck_bsop_date": "20240423",
            "bond_prpr": "10500.00",
            "bond_prdy_vrss": "50.00",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.48",
            "acml_vol": "10023",
            "bond_oprc": "10400.00",
            "bond_hgpr": "10500.00",
            "bond_lwpr": "10400.00"
        },
        {
            "stck_bsop_date": "20240422",
            "bond_prpr": "10450.00",
            "bond_prdy_vrss": "50.00",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.48",
            "acml_vol": "185887",
            "bond_oprc": "10450.00",
            "bond_hgpr": "10500.00",
            "bond_lwpr": "10449.90"
        },
        {
            "stck_bsop_date": "20240416",
            "bond_prpr": "10400.00",
            "bond_prdy_vrss": "41.00",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.40",
            "acml_vol": "16204",
            "bond_oprc": "10270.10",
            "bond_hgpr": "10400.00",
            "bond_lwpr": "10270.10"
        },
        {
            "stck_bsop_date": "20240409",
            "bond_prpr": "10359.00",
            "bond_prdy_vrss": "0.00",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "25500",
            "bond_oprc": "10270.00",
            "bond_hgpr": "10359.00",
            "bond_lwpr": "10270.00"
        },
        {
            "stck_bsop_date": "20240408",
            "bond_prpr": "10359.00",
            "bond_prdy_vrss": "98.90",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.96",
            "acml_vol": "3908",
            "bond_oprc": "10270.00",
            "bond_hgpr": "10359.00",
            "bond_lwpr": "10201.40"
        },
        {
            "stck_bsop_date": "20240405",
            "bond_prpr": "10260.10",
            "bond_prdy_vrss": "10.10",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "0.10",
            "acml_vol": "86102",
            "bond_oprc": "10260.00",
            "bond_hgpr": "10369.70",
            "bond_lwpr": "10260.00"
        },
        {
            "stck_bsop_date": "20240404",
            "bond_prpr": "10250.00",
            "bond_prdy_vrss": "0.00",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "acml_vol": "160002",
            "bond_oprc": "10370.00",
            "bond_hgpr": "10370.00",
            "bond_lwpr": "10250.00"
        },
        {
            "stck_bsop_date": "20240403",
            "bond_prpr": "10250.00",
            "bond_prdy_vrss": "-10.00",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-0.10",
            "acml_vol": "15003",
            "bond_oprc": "10200.00",
            "bond_hgpr": "10250.00",
            "bond_lwpr": "10200.00"
        },
        {
            "stck_bsop_date": "20240402",
            "bond_prpr": "10260.00",
            "bond_prdy_vrss": "120.00",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "1.18",
            "acml_vol": "50000",
            "bond_oprc": "10260.00",
            "bond_hgpr": "10260.00",
            "bond_lwpr": "10260.00"
        },
		...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

