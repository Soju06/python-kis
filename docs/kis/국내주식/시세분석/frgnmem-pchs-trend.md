# 종목별 외국계 순매수추이 [국내주식-164]

> [국내주식] 시세분석

종목별 외국계 순매수추이 API입니다.
한국투자 HTS(eFriend Plus) > [0433] 종목별 외국계 순매수추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fdecab0c-4c48-499b-9436-4ac3d32dbd09` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/frgnmem-pchs-trend` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHKST644400C0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST644400C0 |
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
| `FID_INPUT_ISCD` | 조건시장분류코드 | String | 12 | Y | 종목코드(ex) 005930(삼성전자)) |
| `FID_INPUT_ISCD_2` | 조건화면분류코드 | String | 8 | Y | 외국계 전체(99999) |
| `FID_COND_MRKT_DIV_CODE` | 시장구분코드 | String | 10 | Y | J (KRX만 지원) |

### 요청 예시

```json
FID_INPUT_ISCD:005930
FID_INPUT_ISCD_2:99999
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
| `output` | 응답상세 | Object |   | Y | array |
| `bsop_hour` | 영업시간 | String | 6 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `frgn_seln_vol` | 외국인매도거래량 | String | 18 | Y |  |
| `frgn_shnu_vol` | 외국인매수2거래량 | String | 18 | Y |  |
| `glob_ntby_qty` | 외국계순매수수량 | String | 12 | Y |  |
| `frgn_ntby_qty_icdc` | 외국인순매수수량증감 | String | 10 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "bsop_hour": "153106",
            "stck_prpr": "81300",
            "prdy_vrss": "3700",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.77",
            "acml_vol": "24771461",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4418409",
            "glob_ntby_qty": "3870530",
            "frgn_ntby_qty_icdc": "194396"
        },
        {
            "bsop_hour": "151952",
            "stck_prpr": "81200",
            "prdy_vrss": "3600",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.64",
            "acml_vol": "23517309",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4224013",
            "glob_ntby_qty": "3676134",
            "frgn_ntby_qty_icdc": "3123"
        },
        {
            "bsop_hour": "151836",
            "stck_prpr": "81100",
            "prdy_vrss": "3500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.51",
            "acml_vol": "23404992",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4220890",
            "glob_ntby_qty": "3673011",
            "frgn_ntby_qty_icdc": "1700"
        },
        {
            "bsop_hour": "151724",
            "stck_prpr": "81100",
            "prdy_vrss": "3500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.51",
            "acml_vol": "23374199",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4219190",
            "glob_ntby_qty": "3671311",
            "frgn_ntby_qty_icdc": "1261"
        },
        {
            "bsop_hour": "151613",
            "stck_prpr": "81100",
            "prdy_vrss": "3500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.51",
            "acml_vol": "23327774",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4217929",
            "glob_ntby_qty": "3670050",
            "frgn_ntby_qty_icdc": "5152"
        },
        {
            "bsop_hour": "151503",
            "stck_prpr": "81100",
            "prdy_vrss": "3500",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.51",
            "acml_vol": "23255295",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4212777",
            "glob_ntby_qty": "3664898",
            "frgn_ntby_qty_icdc": "181"
        },
        {
            "bsop_hour": "151355",
            "stck_prpr": "81200",
            "prdy_vrss": "3600",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.64",
            "acml_vol": "23222914",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4212596",
            "glob_ntby_qty": "3664717",
            "frgn_ntby_qty_icdc": "87"
        },
        {
            "bsop_hour": "151245",
            "stck_prpr": "81200",
            "prdy_vrss": "3600",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.64",
            "acml_vol": "23207485",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4212509",
            "glob_ntby_qty": "3664630",
            "frgn_ntby_qty_icdc": "588"
        },
        {
            "bsop_hour": "151136",
            "stck_prpr": "81300",
            "prdy_vrss": "3700",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.77",
            "acml_vol": "23126698",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4211921",
            "glob_ntby_qty": "3664042",
            "frgn_ntby_qty_icdc": "4468"
        },
        {
            "bsop_hour": "151022",
            "stck_prpr": "81200",
            "prdy_vrss": "3600",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "4.64",
            "acml_vol": "23058530",
            "frgn_seln_vol": "547879",
            "frgn_shnu_vol": "4207453",
            "glob_ntby_qty": "3659574",
            "frgn_ntby_qty_icdc": "143"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
