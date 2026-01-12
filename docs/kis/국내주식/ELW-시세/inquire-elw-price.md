# ELW 현재가 시세[v1_국내주식-014]

> [국내주식] ELW 시세

ELW 현재가 시세 API입니다. ELW 관련 정보를 얻을 수 있습니다.

ELW 현재가 시세

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `07313e08-45f2-4423-abb2-2a49752910ae` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-elw-price` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHKEW15010000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19
- **최종 수정일**: 2025-06-19

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 40 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKEW15010000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | W |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목번호 (6자리) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "000660"
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
| `output1` | 응답상세 | Object |   | Y | array |
| `elw_shrn_iscd` | ELW 단축 종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `elw_prpr` | ELW 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 11 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vrss_vol_rate` | 전일 대비 거래량 비율 | String | 13 | Y |  |
| `unas_shrn_iscd` | 기초자산 단축 종목코드 | String | 9 | Y |  |
| `unas_isnm` | 기초자산 종목명 | String | 40 | Y |  |
| `unas_prpr` | 기초자산 현재가 | String | 14 | Y |  |
| `unas_prdy_vrss` | 기초자산 전일 대비 | String | 14 | Y |  |
| `unas_prdy_vrss_sign` | 기초자산 전일 대비 부호 | String | 1 | Y |  |
| `unas_prdy_ctrt` | 기초자산 전일 대비율 | String | 11 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `vol_tnrt` | 거래량 회전율 | String | 11 | Y |  |
| `elw_oprc` | ELW 시가2 | String | 10 | Y |  |
| `elw_hgpr` | ELW 최고가 | String | 10 | Y |  |
| `elw_lwpr` | ELW 최저가 | String | 10 | Y |  |
| `stck_prdy_clpr` | 주식 전일 종가 | String | 10 | Y |  |
| `hts_thpr` | HTS 이론가 | String | 14 | Y |  |
| `dprt` | 괴리율 | String | 11 | Y |  |
| `atm_cls_name` | ATM 구분 명 | String | 10 | Y |  |
| `hts_ints_vltl` | HTS 내재 변동성 | String | 16 | Y |  |
| `acpr` | 행사가 | String | 14 | Y |  |
| `pvt_scnd_dmrs_prc` | 피벗 2차 디저항 가격 | String | 10 | Y |  |
| `pvt_frst_dmrs_prc` | 피벗 1차 디저항 가격 | String | 10 | Y |  |
| `pvt_pont_val` | 피벗 포인트 값 | String | 10 | Y |  |
| `pvt_frst_dmsp_prc` | 피벗 1차 디지지 가격 | String | 10 | Y |  |
| `pvt_scnd_dmsp_prc` | 피벗 2차 디지지 가격 | String | 10 | Y |  |
| `dmsp_val` | 디지지 값 | String | 10 | Y |  |
| `dmrs_val` | 디저항 값 | String | 10 | Y |  |
| `elw_sdpr` | ELW 기준가 | String | 10 | Y |  |
| `apprch_rate` | 접근도 | String | 14 | Y |  |
| `tick_conv_prc` | 틱환산가 | String | 11 | Y |  |
| `invt_epmd_cntt` | 투자 유의 내용 | String | 200 | Y |  |

### 응답 예시

```json
{
  "output": {
    "elw_prpr": "0",
    "prdy_vrss": "0",
    "prdy_ctrt": "0.00",
    "acml_vol": "0",
    "prdy_vrss_vol_rate": "0.00",
    "unas_isnm": "BASKET",
    "unas_prpr": "0.00",
    "unas_prdy_vrss": "0.00",
    "unas_prdy_vrss_sign": "3",
    "unas_prdy_ctrt": "0.00",
    "bidp": "0",
    "askp": "0",
    "acml_tr_pbmn": "0",
    "vol_tnrt": "0.00",
    "elw_oprc": "0",
    "elw_hgpr": "0",
    "elw_lwpr": "0",
    "stck_prdy_clpr": "0",
    "hts_thpr": "0.00",
    "dprt": "0.00",
    "atm_cls_name": "ATM",
    "hts_ints_vltl": "0.00",
    "acpr": "0.00",
    "pvt_scnd_dmrs_prc": "0",
    "pvt_frst_dmrs_prc": "0",
    "pvt_pont_val": "0",
    "pvt_frst_dmsp_prc": "0",
    "pvt_scnd_dmsp_prc": "0",
    "dmsp_val": "0",
    "dmrs_val": "0",
    "elw_sdpr": "0",
    "apprch_rate": "0.00",
    "tick_conv_prc": "0.00"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다!"
}
```
