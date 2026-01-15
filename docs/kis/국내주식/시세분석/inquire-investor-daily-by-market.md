# 시장별 투자자매매동향(일별) [국내주식-075]

> [국내주식] 시세분석

시장별 투자자매매동향(일별) API입니다.
한국투자 HTS(eFriend Plus) > [0404] 시장별 일별동향 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `0cc848c0-4928-4b89-bca4-62df430e4a45` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHPTJ04040000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
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
| `tr_id` | 거래ID | String | 13 | Y | FHPTJ04040000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (업종 U) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 코스피, 코스닥 : 업종분류코드 (종목정보파일 - 업종코드 참조) |
| `FID_INPUT_DATE_1` | 입력 날짜1 | String | 10 | Y | ex. 20240517 |
| `FID_INPUT_ISCD_1` | 입력 종목코드 | String | 12 | Y | 코스피(KSP), 코스닥(KSQ) |
| `FID_INPUT_DATE_2` | 입력 날짜2 | String | 10 | Y | 입력 날짜1과 동일날짜 입력 |
| `FID_INPUT_ISCD_2` | 하위 분류코드 | String | 10 | Y | 코스피, 코스닥 : 업종분류코드 (종목정보파일 - 업종코드 참조) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:U
FID_INPUT_ISCD:0001
FID_INPUT_DATE_1:20240517
FID_INPUT_ISCD_1:KSP
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
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `bstp_nmix_oprc` | 업종 지수 시가2 | String | 112 | Y |  |
| `bstp_nmix_hgpr` | 업종 지수 최고가 | String | 112 | Y |  |
| `bstp_nmix_lwpr` | 업종 지수 최저가 | String | 112 | Y |  |
| `stck_prdy_clpr` | 주식 전일 종가 | String | 10 | Y |  |
| `frgn_ntby_qty` | 외국인 순매수 수량 | String | 12 | Y |  |
| `frgn_reg_ntby_qty` | 외국인 등록 순매수 수량 | String | 18 | Y |  |
| `frgn_nreg_ntby_qty` | 외국인 비등록 순매수 수량 | String | 18 | Y |  |
| `prsn_ntby_qty` | 개인 순매수 수량 | String | 12 | Y |  |
| `orgn_ntby_qty` | 기관계 순매수 수량 | String | 18 | Y |  |
| `scrt_ntby_qty` | 증권 순매수 수량 | String | 12 | Y |  |
| `ivtr_ntby_qty` | 투자신탁 순매수 수량 | String | 12 | Y |  |
| `pe_fund_ntby_vol` | 사모 펀드 순매수 거래량 | String | 18 | Y |  |
| `bank_ntby_qty` | 은행 순매수 수량 | String | 12 | Y |  |
| `insu_ntby_qty` | 보험 순매수 수량 | String | 12 | Y |  |
| `mrbn_ntby_qty` | 종금 순매수 수량 | String | 12 | Y |  |
| `fund_ntby_qty` | 기금 순매수 수량 | String | 12 | Y |  |
| `etc_ntby_qty` | 기타 순매수 수량 | String | 12 | Y |  |
| `etc_orgt_ntby_vol` | 기타 단체 순매수 거래량 | String | 18 | Y |  |
| `etc_corp_ntby_vol` | 기타 법인 순매수 거래량 | String | 18 | Y |  |
| `frgn_ntby_tr_pbmn` | 외국인 순매수 거래 대금 | String | 18 | Y |  |
| `frgn_reg_ntby_pbmn` | 외국인 등록 순매수 대금 | String | 18 | Y |  |
| `frgn_nreg_ntby_pbmn` | 외국인 비등록 순매수 대금 | String | 18 | Y |  |
| `prsn_ntby_tr_pbmn` | 개인 순매수 거래 대금 | String | 18 | Y |  |
| `orgn_ntby_tr_pbmn` | 기관계 순매수 거래 대금 | String | 18 | Y |  |
| `scrt_ntby_tr_pbmn` | 증권 순매수 거래 대금 | String | 18 | Y |  |
| `ivtr_ntby_tr_pbmn` | 투자신탁 순매수 거래 대금 | String | 18 | Y |  |
| `pe_fund_ntby_tr_pbmn` | 사모 펀드 순매수 거래 대금 | String | 18 | Y |  |
| `bank_ntby_tr_pbmn` | 은행 순매수 거래 대금 | String | 18 | Y |  |
| `insu_ntby_tr_pbmn` | 보험 순매수 거래 대금 | String | 18 | Y |  |
| `mrbn_ntby_tr_pbmn` | 종금 순매수 거래 대금 | String | 18 | Y |  |
| `fund_ntby_tr_pbmn` | 기금 순매수 거래 대금 | String | 18 | Y |  |
| `etc_ntby_tr_pbmn` | 기타 순매수 거래 대금 | String | 18 | Y |  |
| `etc_orgt_ntby_tr_pbmn` | 기타 단체 순매수 거래 대금 | String | 18 | Y |  |
| `etc_corp_ntby_tr_pbmn` | 기타 법인 순매수 거래 대금 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240517",
            "bstp_nmix_prpr": "2724.62",
            "bstp_nmix_prdy_vrss": "-28.38",
            "prdy_vrss_sign": "5",
            "bstp_nmix_prdy_ctrt": "-1.03",
            "bstp_nmix_oprc": "2751.47",
            "bstp_nmix_hgpr": "2752.17",
            "bstp_nmix_lwpr": "2724.62",
            "stck_prdy_clpr": "2753.00",
            "frgn_ntby_qty": "-18565",
            "frgn_reg_ntby_qty": "-18009",
            "frgn_nreg_ntby_qty": "-557",
            "prsn_ntby_qty": "22524",
            "orgn_ntby_qty": "-4738",
            "scrt_ntby_qty": "-1148",
            "ivtr_ntby_qty": "-609",
            "pe_fund_ntby_vol": "-431",
            "bank_ntby_qty": "103",
            "insu_ntby_qty": "-156",
            "mrbn_ntby_qty": "-175",
            "fund_ntby_qty": "-2322",
            "etc_ntby_qty": "779",
            "etc_orgt_ntby_vol": "0",
            "etc_corp_ntby_vol": "779",
            "frgn_ntby_tr_pbmn": "-597490",
            "frgn_reg_ntby_pbmn": "-597676",
            "frgn_nreg_ntby_pbmn": "186",
            "prsn_ntby_tr_pbmn": "720787",
            "orgn_ntby_tr_pbmn": "-150685",
            "scrt_ntby_tr_pbmn": "-18893",
            "ivtr_ntby_tr_pbmn": "-7246",
            "pe_fund_ntby_tr_pbmn": "-25668",
            "bank_ntby_tr_pbmn": "3326",
            "insu_ntby_tr_pbmn": "-13791",
            "mrbn_ntby_tr_pbmn": "-2742",
            "fund_ntby_tr_pbmn": "-85671",
            "etc_ntby_tr_pbmn": "27388",
            "etc_orgt_ntby_tr_pbmn": "0",
            "etc_corp_ntby_tr_pbmn": "27388"
        },
        {
            "stck_bsop_date": "20240516",
            "bstp_nmix_prpr": "2753.00",
            "bstp_nmix_prdy_vrss": "22.66",
            "prdy_vrss_sign": "2",
            "bstp_nmix_prdy_ctrt": "0.83",
            "bstp_nmix_oprc": "2770.27",
            "bstp_nmix_hgpr": "2773.46",
            "bstp_nmix_lwpr": "2748.22",
            "stck_prdy_clpr": "2730.34",
            "frgn_ntby_qty": "5326",
            "frgn_reg_ntby_qty": "5287",
            "frgn_nreg_ntby_qty": "38",
            "prsn_ntby_qty": "-14059",
            "orgn_ntby_qty": "8886",
            "scrt_ntby_qty": "11036",
            "ivtr_ntby_qty": "359",
            "pe_fund_ntby_vol": "850",
            "bank_ntby_qty": "41",
            "insu_ntby_qty": "-989",
            "mrbn_ntby_qty": "-341",
            "fund_ntby_qty": "-2070",
            "etc_ntby_qty": "-153",
            "etc_orgt_ntby_vol": "0",
            "etc_corp_ntby_vol": "-153",
            "frgn_ntby_tr_pbmn": "425869",
            "frgn_reg_ntby_pbmn": "425686",
            "frgn_nreg_ntby_pbmn": "183",
            "prsn_ntby_tr_pbmn": "-964779",
            "orgn_ntby_tr_pbmn": "593789",
            "scrt_ntby_tr_pbmn": "680881",
            "ivtr_ntby_tr_pbmn": "20139",
            "pe_fund_ntby_tr_pbmn": "11277",
            "bank_ntby_tr_pbmn": "-589",
            "insu_ntby_tr_pbmn": "-29395",
            "mrbn_ntby_tr_pbmn": "-19913",
            "fund_ntby_tr_pbmn": "-68611",
            "etc_ntby_tr_pbmn": "-54879",
            "etc_orgt_ntby_tr_pbmn": "0",
            "etc_corp_ntby_tr_pbmn": "-54879"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

