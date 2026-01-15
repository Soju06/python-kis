# ETF/ETN 현재가[v1_국내주식-068]

> [국내주식] 기본시세

ETF/ETN 현재가 API입니다.
한국투자 HTS(eFriend Plus) > [0240] ETF/ETN 현재가 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `e53eb2e6-b292-4e2b-b150-22d92b401453` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/etfetn/v1/quotations/inquire-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHPST02400000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-23
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST02400000 |
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
| `fid_input_iscd` | FID 입력 종목코드 | String | 12 | Y | 종목코드 |
| `fid_cond_mrkt_div_code` | FID 조건 시장 분류 코드 | String | 2 | Y | J |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "069500"
}
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
| `output` | 응답상세 | String |   | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `stck_mxpr` | 주식 상한가 | String | 10 | Y |  |
| `stck_llam` | 주식 하한가 | String | 10 | Y |  |
| `stck_prdy_clpr` | 주식 전일 종가 | String | 10 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `prdy_clpr_vrss_oprc_rate` | 전일 종가 대비 시가2 비율 | String | 84 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `prdy_clpr_vrss_hgpr_rate` | 전일 종가 대비 최고가 비율 | String | 84 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `prdy_clpr_vrss_lwpr_rate` | 전일 종가 대비 최저가 비율 | String | 84 | Y |  |
| `prdy_last_nav` | 전일 최종 NAV | String | 112 | Y |  |
| `nav` | NAV | String | 112 | Y |  |
| `nav_prdy_vrss` | NAV 전일 대비 | String | 112 | Y |  |
| `nav_prdy_vrss_sign` | NAV 전일 대비 부호 | String | 1 | Y |  |
| `nav_prdy_ctrt` | NAV 전일 대비율 | String | 82 | Y |  |
| `trc_errt` | 추적 오차율 | String | 82 | Y |  |
| `stck_sdpr` | 주식 기준가 | String | 10 | Y |  |
| `stck_sspr` | 주식 대용가 | String | 10 | Y |  |
| `nmix_ctrt` | 지수 대비율 | String | 135 | Y |  |
| `etf_crcl_stcn` | ETF 유통 주수 | String | 18 | Y |  |
| `etf_ntas_ttam` | ETF 순자산 총액 | String | 22 | Y |  |
| `etf_frcr_ntas_ttam` | ETF 외화 순자산 총액 | String | 22 | Y |  |
| `frgn_limt_rate` | 외국인 한도 비율 | String | 84 | Y |  |
| `frgn_oder_able_qty` | 외국인 주문 가능 수량 | String | 18 | Y |  |
| `etf_cu_unit_scrt_cnt` | ETF CU 단위 증권 수 | String | 18 | Y |  |
| `etf_cnfg_issu_cnt` | ETF 구성 종목 수 | String | 18 | Y |  |
| `etf_dvdn_cycl` | ETF 배당 주기 | String | 2 | Y |  |
| `crcd` | 통화 코드 | String | 4 | Y |  |
| `etf_crcl_ntas_ttam` | ETF 유통 순자산 총액 | String | 22 | Y |  |
| `etf_frcr_crcl_ntas_ttam` | ETF 외화 유통 순자산 총액 | String | 22 | Y |  |
| `etf_frcr_last_ntas_wrth_val` | ETF 외화 최종 순자산 가치 값 | String | 13 | Y |  |
| `lp_oder_able_cls_code` | LP 주문 가능 구분 코드 | String | 2 | Y |  |
| `stck_dryy_hgpr` | 주식 연중 최고가 | String | 10 | Y |  |
| `dryy_hgpr_vrss_prpr_rate` | 연중 최고가 대비 현재가 비율 | String | 84 | Y |  |
| `dryy_hgpr_date` | 연중 최고가 일자 | String | 8 | Y |  |
| `stck_dryy_lwpr` | 주식 연중 최저가 | String | 10 | Y |  |
| `dryy_lwpr_vrss_prpr_rate` | 연중 최저가 대비 현재가 비율 | String | 84 | Y |  |
| `dryy_lwpr_date` | 연중 최저가 일자 | String | 8 | Y |  |
| `bstp_kor_isnm` | 업종 한글 종목명 | String | 40 | Y | ※ 거래소 정보로 특정 종목은 업종구분이 없어 데이터 미회신 |
| `vi_cls_code` | VI적용구분코드 | String | 1 | Y |  |
| `lstn_stcn` | 상장 주수 | String | 18 | Y |  |
| `frgn_hldn_qty` | 외국인 보유 수량 | String | 18 | Y |  |
| `frgn_hldn_qty_rate` | 외국인 보유 수량 비율 | String | 84 | Y |  |
| `etf_trc_ert_mltp` | ETF 추적 수익률 배수 | String | 126 | Y |  |
| `dprt` | 괴리율 | String | 82 | Y |  |
| `mbcr_name` | 회원사 명 | String | 50 | Y |  |
| `stck_lstn_date` | 주식 상장 일자 | String | 8 | Y |  |
| `mtrt_date` | 만기 일자 | String | 8 | Y |  |
| `shrg_type_code` | 분배금형태코드 | String | 2 | Y |  |
| `lp_hldn_rate` | LP 보유 비율 | String | 84 | Y |  |
| `etf_trgt_nmix_bstp_code` | ETF대상지수업종코드 | String | 4 | Y |  |
| `etf_div_name` | ETF 분류 명 | String | 40 | Y |  |
| `etf_rprs_bstp_kor_isnm` | ETF 대표 업종 한글 종목명 | String | 40 | Y |  |
| `lp_hldn_vol` | ETN LP 보유량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": {
    "stck_prpr": "36090",
    "prdy_vrss_sign": "2",
    "prdy_vrss": "110",
    "prdy_ctrt": "0.31",
    "acml_vol": "3719307",
    "prdy_vol": "6463600",
    "stck_mxpr": "46770",
    "stck_llam": "25190",
    "stck_prdy_clpr": "35980",
    "stck_oprc": "36300",
    "prdy_clpr_vrss_oprc_rate": "0.89",
    "stck_hgpr": "36510",
    "prdy_clpr_vrss_hgpr_rate": "1.47",
    "stck_lwpr": "36040",
    "prdy_clpr_vrss_lwpr_rate": "0.17",
    "prdy_last_nav": "36036.22",
    "nav": "36127.30",
    "nav_prdy_vrss": "91.08",
    "nav_prdy_vrss_sign": "2",
    "nav_prdy_ctrt": "0.25",
    "trc_errt": "0.53",
    "stck_sdpr": "35980",
    "stck_sspr": "28780",
    "etf_crcl_stcn": "191550000",
    "etf_ntas_ttam": "69027",
    "etf_frcr_ntas_ttam": "0",
    "frgn_limt_rate": "100.0000",
    "frgn_oder_able_qty": "150950685",
    "etf_cu_unit_scrt_cnt": "50000",
    "etf_cnfg_issu_cnt": "201",
    "etf_dvdn_cycl": "2",
    "crcd": "KRW",
    "etf_crcl_ntas_ttam": "0",
    "etf_frcr_crcl_ntas_ttam": "0",
    "etf_frcr_last_ntas_wrth_val": "0",
    "lp_oder_able_cls_code": "N",
    "stck_dryy_hgpr": "36510",
    "dryy_hgpr_vrss_prpr_rate": "-1.15",
    "dryy_hgpr_date": "20240223",
    "stck_dryy_lwpr": "32748",
    "dryy_lwpr_vrss_prpr_rate": "10.21",
    "dryy_lwpr_date": "20240118",
    "bstp_kor_isnm": "ETF(실물복제/수익증권)",
    "vi_cls_code": "N",
    "lstn_stcn": "191550000",
    "frgn_hldn_qty": "40599315",
    "frgn_hldn_qty_rate": "21.20",
    "etf_trc_ert_mltp": "1.00",
    "dprt": "-0.10",
    "mbcr_name": "삼성자산운용(ETF)",
    "stck_lstn_date": "20021014",
    "mtrt_date": "0",
    "shrg_type_code": "  ",
    "lp_hldn_rate": "0.00",
    "etf_trgt_nmix_bstp_code": "2001",
    "etf_div_name": "수익증권형",
    "etf_rprs_bstp_kor_isnm": "KOSPI200",
    "lp_hldn_vol": "0"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
