# 국내옵션전광판_콜풋[국내선물-022]

> [국내선물옵션] 기본시세

국내옵션전광판_콜풋 API입니다.
한국투자 HTS(eFriend Plus) > [0503] 선물옵션 종합시세(Ⅰ) 화면의 "중앙" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ output1, output2 각각 100건까지만 확인이 가능합니다. (FY25년도 서비스 개선 예정)
※ 조회시간이 긴 API인 점 참고 부탁드리며, 잦은 호출을 삼가해주시기 바랍니다. (1초당 최대 1건 권장)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `d9b0e346-a67d-43c6-938a-508e2d8507c6` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/display-board-callput` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPIF05030100` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
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
| `tr_id` | 거래ID | String | 13 | Y | FHPIF05030100 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (O: 옵션) |
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20503) |
| `FID_MRKT_CLS_CODE` | 시장 구분 코드 | String | 2 | Y | 시장구분코드 (CO: 콜옵션) |
| `FID_MTRT_CNT` | 만기 수 | String | 11 | Y | - FID_COND_MRKT_CLS_CODE : 공백(KOSPI200), MKI(미니KOSPI200), KQI(KOSDAQ150) 인 경우 : 만기년월(YYYYMM) 입력 (... |
| `FID_COND_MRKT_CLS_CODE` | 조건 시장 구분 코드 | String | 6 | Y | 공백: KOSPI200 MKI: 미니KOSPI200 WKM: KOSPI200위클리(월) WKI: KOSPI200위클리(목) KQI: KOSDAQ150 |
| `FID_MRKT_CLS_CODE1` | 시장 구분 코드 | String | 2 | Y | 시장구분코드 (PO: 풋옵션) |

### 요청 예시

```json
fid_cond_mrkt_div_code:O
fid_cond_scr_div_code:20503
fid_mrkt_cls_code:CO
fid_mtrt_cnt:202405
fid_cond_mrkt_cls_code:
fid_mrkt_cls_code1:PO
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
| `acpr` | 행사가 | String | 112 | Y |  |
| `unch_prpr` | 환산 현재가 | String | 112 | Y |  |
| `optn_shrn_iscd` | 옵션 단축 종목코드 | String | 9 | Y |  |
| `optn_prpr` | 옵션 현재가 | String | 112 | Y |  |
| `optn_prdy_vrss` | 옵션 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `optn_prdy_ctrt` | 옵션 전일 대비율 | String | 82 | Y |  |
| `optn_bidp` | 옵션 매수호가 | String | 112 | Y |  |
| `optn_askp` | 옵션 매도호가 | String | 112 | Y |  |
| `tmvl_val` | 시간가치 값 | String | 132 | Y |  |
| `nmix_sdpr` | 지수 기준가 | String | 112 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `seln_rsqn` | 매도 잔량 | String | 12 | Y |  |
| `shnu_rsqn` | 매수2 잔량 | String | 12 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `hts_otst_stpl_qty` | HTS 미결제 약정 수량 | String | 18 | Y |  |
| `otst_stpl_qty_icdc` | 미결제 약정 수량 증감 | String | 10 | Y |  |
| `delta_val` | 델타 값 | String | 114 | Y |  |
| `gama` | 감마 | String | 84 | Y |  |
| `vega` | 베가 | String | 84 | Y |  |
| `theta` | 세타 | String | 84 | Y |  |
| `rho` | 로우 | String | 84 | Y |  |
| `hts_ints_vltl` | HTS 내재 변동성 | String | 114 | Y |  |
| `invl_val` | 내재가치 값 | String | 132 | Y |  |
| `esdg` | 괴리도 | String | 114 | Y |  |
| `dprt` | 괴리율 | String | 82 | Y |  |
| `hist_vltl` | 역사적 변동성 | String | 114 | Y |  |
| `hts_thpr` | HTS 이론가 | String | 112 | Y |  |
| `optn_oprc` | 옵션 시가2 | String | 112 | Y |  |
| `optn_hgpr` | 옵션 최고가 | String | 112 | Y |  |
| `optn_lwpr` | 옵션 최저가 | String | 112 | Y |  |
| `optn_mxpr` | 옵션 상한가 | String | 112 | Y |  |
| `optn_llam` | 옵션 하한가 | String | 112 | Y |  |
| `atm_cls_name` | ATM 구분 명 | String | 10 | Y |  |
| `rgbf_vrss_icdc` | 직전 대비 증감 | String | 10 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `futs_antc_cnpr` | 선물예상체결가 | String | 112 | Y |  |
| `futs_antc_cntg_vrss` | 선물예상체결대비 | String | 112 | Y |  |
| `antc_cntg_vrss_sign` | 예상 체결 대비 부호 | String | 1 | Y |  |
| `antc_cntg_prdy_ctrt` | 예상 체결 전일 대비율 | String | 82 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `acpr` | 행사가 | String | 112 | Y |  |
| `unch_prpr` | 환산 현재가 | String | 112 | Y |  |
| `optn_shrn_iscd` | 옵션 단축 종목코드 | String | 9 | Y |  |
| `optn_prpr` | 옵션 현재가 | String | 112 | Y |  |
| `optn_prdy_vrss` | 옵션 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `optn_prdy_ctrt` | 옵션 전일 대비율 | String | 82 | Y |  |
| `optn_bidp` | 옵션 매수호가 | String | 112 | Y |  |
| `optn_askp` | 옵션 매도호가 | String | 112 | Y |  |
| `tmvl_val` | 시간가치 값 | String | 132 | Y |  |
| `nmix_sdpr` | 지수 기준가 | String | 112 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `seln_rsqn` | 매도 잔량 | String | 12 | Y |  |
| `shnu_rsqn` | 매수2 잔량 | String | 12 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `hts_otst_stpl_qty` | HTS 미결제 약정 수량 | String | 18 | Y |  |
| `otst_stpl_qty_icdc` | 미결제 약정 수량 증감 | String | 10 | Y |  |
| `delta_val` | 델타 값 | String | 114 | Y |  |
| `gama` | 감마 | String | 84 | Y |  |
| `vega` | 베가 | String | 84 | Y |  |
| `theta` | 세타 | String | 84 | Y |  |
| `rho` | 로우 | String | 84 | Y |  |
| `hts_ints_vltl` | HTS 내재 변동성 | String | 114 | Y |  |
| `invl_val` | 내재가치 값 | String | 132 | Y |  |
| `esdg` | 괴리도 | String | 114 | Y |  |
| `dprt` | 괴리율 | String | 82 | Y |  |
| `hist_vltl` | 역사적 변동성 | String | 114 | Y |  |
| `hts_thpr` | HTS 이론가 | String | 112 | Y |  |
| `optn_oprc` | 옵션 시가2 | String | 112 | Y |  |
| `optn_hgpr` | 옵션 최고가 | String | 112 | Y |  |
| `optn_lwpr` | 옵션 최저가 | String | 112 | Y |  |
| `optn_mxpr` | 옵션 상한가 | String | 112 | Y |  |
| `optn_llam` | 옵션 하한가 | String | 112 | Y |  |
| `atm_cls_name` | ATM 구분 명 | String | 10 | Y |  |
| `rgbf_vrss_icdc` | 직전 대비 증감 | String | 10 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `futs_antc_cnpr` | 선물예상체결가 | String | 112 | Y |  |
| `futs_antc_cntg_vrss` | 선물예상체결대비 | String | 112 | Y |  |
| `antc_cntg_vrss_sign` | 예상 체결 대비 부호 | String | 1 | Y |  |
| `antc_cntg_prdy_ctrt` | 예상 체결 전일 대비율 | String | 82 | Y |  |

### 응답 예시

```json
{
    "output1": [
        {
            "acpr": "480.00",
            "unch_prpr": "3505.17",
            "optn_shrn_iscd": "201V05480",
            "optn_prpr": "0.01",
            "optn_prdy_vrss": "0.00",
            "prdy_vrss_sign": "3",
            "optn_prdy_ctrt": "0.00",
            "optn_bidp": "0.00",
            "optn_askp": "0.01",
            "tmvl_val": "0.01",
            "nmix_sdpr": "0.01",
            "acml_vol": "34",
            "seln_rsqn": "1710",
            "shnu_rsqn": "0",
            "acml_tr_pbmn": "85",
            "hts_otst_stpl_qty": "642",
            "otst_stpl_qty_icdc": "39",
            "delta_val": "0.0000",
            "gama": "0.0000",
            "vega": "0.0000",
            "theta": "-0.0000",
            "rho": "0.0000",
            "hts_ints_vltl": "31.5614",
            "invl_val": "0.00",
            "esdg": "0.01",
            "dprt": "9999.99",
            "hist_vltl": "16.9285",
            "hts_thpr": "0.00",
            "optn_oprc": "0.01",
            "optn_hgpr": "0.01",
            "optn_lwpr": "0.01",
            "optn_mxpr": "5.20",
            "optn_llam": "0.01",
            "atm_cls_name": "OTM",
            "rgbf_vrss_icdc": "1",
            "total_askp_rsqn": "1710",
            "total_bidp_rsqn": "0",
            "futs_antc_cnpr": "0.00",
            "futs_antc_cntg_vrss": "0.00",
            "antc_cntg_vrss_sign": "0",
            "antc_cntg_prdy_ctrt": "0.00"
        },
		...
    ],
    "output2": [
        {
            "acpr": "480.00",
            "unch_prpr": "3505.17",
            "optn_shrn_iscd": "301V05480",
            "optn_prpr": "108.45",
            "optn_prdy_vrss": "0.00",
            "prdy_vrss_sign": "3",
            "optn_prdy_ctrt": "0.00",
            "optn_bidp": "78.35",
            "optn_askp": "142.60",
            "tmvl_val": "-4.30",
            "nmix_sdpr": "108.45",
            "acml_vol": "0",
            "seln_rsqn": "10",
            "shnu_rsqn": "10",
            "acml_tr_pbmn": "0",
            "hts_otst_stpl_qty": "48",
            "otst_stpl_qty_icdc": "0",
            "delta_val": "-1.0000",
            "gama": "0.0000",
            "vega": "0.0000",
            "theta": "0.0460",
            "rho": "-0.3541",
            "hts_ints_vltl": "0.0000",
            "invl_val": "112.75",
            "esdg": "-3.06",
            "dprt": "-2.74",
            "hist_vltl": "16.9285",
            "hts_thpr": "111.51",
            "optn_oprc": "0.00",
            "optn_hgpr": "0.00",
            "optn_lwpr": "0.00",
            "optn_mxpr": "142.60",
            "optn_llam": "78.35",
            "atm_cls_name": "ITM",
            "rgbf_vrss_icdc": "0",
            "total_askp_rsqn": "10",
            "total_bidp_rsqn": "10",
            "futs_antc_cnpr": "0.00",
            "futs_antc_cntg_vrss": "0.00",
            "antc_cntg_vrss_sign": "0",
            "antc_cntg_prdy_ctrt": "0.00"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

