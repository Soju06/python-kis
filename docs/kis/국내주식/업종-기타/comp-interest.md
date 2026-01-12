# 금리 종합(국내채권/금리) [국내주식-155]

> [국내주식] 업종/기타

금리 종합(국내채권/금리) API입니다.
한국투자 HTS(eFriend Plus) > [0702] 금리 종합 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 11:30 이후에 신규데이터가 수신되는 점 참고하시기 바랍니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ecc36b93-6f99-4cd2-b16d-79b46734769a` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/comp-interest` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHPST07020000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST07020000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | Unique key(I) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | Unique key(20702) |
| `FID_DIV_CLS_CODE` | 분류구분코드 | String | 2 | Y | 1: 해외금리지표 |
| `FID_DIV_CLS_CODE1` | 분류구분코드 | String | 2 | Y | 공백 : 전체 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:I
FID_COND_SCR_DIV_CODE:20702
FID_DIV_CLS_CODE:1
FID_DIV_CLS_CODE1:
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
| `output1` | 응답상세 | String |   | Y | array |
| `bcdt_code` | 자료코드 | String | 5 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `bond_mnrt_prpr` | 채권금리현재가 | String | 114 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `bond_mnrt_prdy_vrss` | 채권금리전일대비 | String | 114 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `bcdt_code` | 자료코드 | String | 5 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `bond_mnrt_prpr` | 채권금리현재가 | String | 114 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `bond_mnrt_prdy_vrss` | 채권금리전일대비 | String | 114 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종지수전일대비율 | String | 82 | Y |  |
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "bcdt_code": "Y0201",
      "hts_kor_isnm": "미국 30년T-BOND",
      "bond_mnrt_prpr": "4.6500",
      "prdy_vrss_sign": "2",
      "bond_mnrt_prdy_vrss": "0.0100",
      "prdy_ctrt": "0.22",
      "stck_bsop_date": "20240411"
    },
    {
      "bcdt_code": "Y0202",
      "hts_kor_isnm": "미국 10년T-NOTE 수익률",
      "bond_mnrt_prpr": "4.5600",
      "prdy_vrss_sign": "2",
      "bond_mnrt_prdy_vrss": "0.0100",
      "prdy_ctrt": "0.22",
      "stck_bsop_date": "20240411"
    },
    {
      "bcdt_code": "Y0203",
      "hts_kor_isnm": "미국 1년T-BILL",
      "bond_mnrt_prpr": "5.1700",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0200",
      "prdy_ctrt": "-0.39",
      "stck_bsop_date": "20240411"
    },
    {
      "bcdt_code": "Y0204",
      "hts_kor_isnm": "미국 연방기금금리(콜)",
      "bond_mnrt_prpr": "5.3300",
      "prdy_vrss_sign": "3",
      "bond_mnrt_prdy_vrss": "0.0000",
      "prdy_ctrt": "0.00",
      "stck_bsop_date": "20240410"
    },
    {
      "bcdt_code": "Y0205",
      "hts_kor_isnm": "미국 재할인률",
      "bond_mnrt_prpr": "5.5000",
      "prdy_vrss_sign": "3",
      "bond_mnrt_prdy_vrss": "0.0000",
      "prdy_ctrt": "0.00",
      "stck_bsop_date": "20240410"
    },
    {
      "bcdt_code": "Y0206",
      "hts_kor_isnm": "미국 단기우대금리",
      "bond_mnrt_prpr": "8.5000",
      "prdy_vrss_sign": "3",
      "bond_mnrt_prdy_vrss": "0.0000",
      "prdy_ctrt": "0.00",
      "stck_bsop_date": "20240410"
    },
    {
      "bcdt_code": "Y0207",
      "hts_kor_isnm": "일본 10년 국채수익률",
      "bond_mnrt_prpr": "0.8540",
      "prdy_vrss_sign": "2",
      "bond_mnrt_prdy_vrss": "0.0530",
      "prdy_ctrt": "6.62",
      "stck_bsop_date": "20240411"
    }
  ],
  "output2": [
    {
      "bcdt_code": "Y0101",
      "hts_kor_isnm": "국고채 3년",
      "bond_mnrt_prpr": "3.4080",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0580",
      "bstp_nmix_prdy_ctrt": "-1.67",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0102",
      "hts_kor_isnm": "회사채 무보증 3년AA-",
      "bond_mnrt_prpr": "3.9630",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0530",
      "bstp_nmix_prdy_ctrt": "-1.32",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0103",
      "hts_kor_isnm": "회사채 3년 BBB-",
      "bond_mnrt_prpr": "10.1690",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0510",
      "bstp_nmix_prdy_ctrt": "-0.50",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0104",
      "hts_kor_isnm": "국고채 1년",
      "bond_mnrt_prpr": "3.4360",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0220",
      "bstp_nmix_prdy_ctrt": "-0.64",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0105",
      "hts_kor_isnm": "국고채 5년",
      "bond_mnrt_prpr": "3.4690",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0420",
      "bstp_nmix_prdy_ctrt": "-1.20",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0106",
      "hts_kor_isnm": "국고채 10년",
      "bond_mnrt_prpr": "3.5460",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0390",
      "bstp_nmix_prdy_ctrt": "-1.09",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0107",
      "hts_kor_isnm": "국민주택1종 (5년)",
      "bond_mnrt_prpr": "3.6010",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0390",
      "bstp_nmix_prdy_ctrt": "-1.07",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0108",
      "hts_kor_isnm": "한전채(3년)",
      "bond_mnrt_prpr": "3.7120",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0490",
      "bstp_nmix_prdy_ctrt": "-1.30",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0109",
      "hts_kor_isnm": "통안증권(364일)",
      "bond_mnrt_prpr": "3.3710",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0250",
      "bstp_nmix_prdy_ctrt": "-0.74",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0110",
      "hts_kor_isnm": "통안증권(2년)",
      "bond_mnrt_prpr": "3.4190",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0500",
      "bstp_nmix_prdy_ctrt": "-1.44",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0111",
      "hts_kor_isnm": "산금채(1년)",
      "bond_mnrt_prpr": "3.5560",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0280",
      "bstp_nmix_prdy_ctrt": "-0.78",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0112",
      "hts_kor_isnm": "C D (91일)",
      "bond_mnrt_prpr": "3.5600",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0100",
      "bstp_nmix_prdy_ctrt": "-0.28",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0113",
      "hts_kor_isnm": "C P (91일)",
      "bond_mnrt_prpr": "4.1800",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0100",
      "bstp_nmix_prdy_ctrt": "-0.24",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0114",
      "hts_kor_isnm": "콜 (1일)",
      "bond_mnrt_prpr": "3.5000",
      "prdy_vrss_sign": "2",
      "bond_mnrt_prdy_vrss": "0.0400",
      "bstp_nmix_prdy_ctrt": "1.16",
      "stck_bsop_date": "20240411"
    },
    {
      "bcdt_code": "Y0115",
      "hts_kor_isnm": "종합채권지수",
      "bond_mnrt_prpr": "102.8100",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.3400",
      "bstp_nmix_prdy_ctrt": "-0.33",
      "stck_bsop_date": "20240411"
    },
    {
      "bcdt_code": "Y0116",
      "hts_kor_isnm": "국고채 20년",
      "bond_mnrt_prpr": "3.4640",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0310",
      "bstp_nmix_prdy_ctrt": "-0.89",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0117",
      "hts_kor_isnm": "국고채 30년",
      "bond_mnrt_prpr": "3.3640",
      "prdy_vrss_sign": "5",
      "bond_mnrt_prdy_vrss": "-0.0240",
      "bstp_nmix_prdy_ctrt": "-0.71",
      "stck_bsop_date": "20240412"
    },
    {
      "bcdt_code": "Y0198",
      "hts_kor_isnm": "Call 지수",
      "bond_mnrt_prpr": "190.2051",
      "prdy_vrss_sign": "2",
      "bond_mnrt_prdy_vrss": "0.0185",
      "bstp_nmix_prdy_ctrt": "0.01",
      "stck_bsop_date": "20240411"
    },
    {
      "bcdt_code": "Y0199",
      "hts_kor_isnm": "CD AAA 3개월(13주)",
      "bond_mnrt_prpr": "203.2972",
      "prdy_vrss_sign": "2",
      "bond_mnrt_prdy_vrss": "0.0198",
      "bstp_nmix_prdy_ctrt": "0.01",
      "stck_bsop_date": "20240411"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
