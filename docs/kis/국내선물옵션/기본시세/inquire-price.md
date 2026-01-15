# 선물옵션 시세[v1_국내선물-006]

> [국내선물옵션] 기본시세

선물옵션 시세 API입니다. 

※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

[국내선물-006 v1] 선물옵션 시세

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `0bb05819-d759-4789-8eda-27a0b88f02aa` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/inquire-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHMIF10000000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전/모의투자] FHMIF10000000 : 선물 옵션 시세 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인 P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션 CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 종목코드 (예: 101S03) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "F",
  "fid_input_iscd": "101S03"
}
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | Y | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공 0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output1` | 응답상세1 | String |  | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y | 종목명 |
| `futs_prpr` | 선물 현재가 | String | 14 | Y | 선물의 현재가격 |
| `futs_prdy_vrss` | 선물 전일 대비 | String | 14 | Y | 선물의 전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가) |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y | 1 : 상한  2 : 상승 3 : 보합 4 : 하한 5 : 하락 |
| `futs_prdy_clpr` | 선물 전일 종가 | String | 14 | Y | 해당 선물 종목의 전일 종가 |
| `futs_prdy_ctrt` | 선물 전일 대비율 | String | 11 | Y | 선물 전일 대비 / 당일 현재가 * 100 |
| `acml_vol` | 누적 거래량 | String | 18 | Y | 당일 조회시점까지 전체 거래량 |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y | 당일 조회시점까지 전체 거래금액 |
| `hts_otst_stpl_qty` | HTS 미결제 약정 수량 | String | 18 | Y | 현재까지 반대매매로 청산되지 않은 계약수 |
| `otst_stpl_qty_icdc` | 미결제 약정 수량 증감 | String | 10 | Y | 전일대비 미결제 약정 수량의 증감 |
| `futs_oprc` | 선물 시가2 | String | 14 | Y | 당일 최초 거래가격 |
| `futs_hgpr` | 선물 최고가 | String | 14 | Y | 당일 조회 시점까지 가장 높은 거래가격 |
| `futs_lwpr` | 선물 최저가 | String | 14 | Y | 당일 조회 시점까지 가장 낮은 거래가격 |
| `futs_mxpr` | 선물 상한가 | String | 14 | Y | 당일 거래 가능한 최고 가격 |
| `futs_llam` | 선물 하한가 | String | 14 | Y | 당일 거래 가능한 최저 가격 |
| `basis` | 베이시스 | String | 13 | Y | 이론베이시스 선물 이론가격과 현물가격과의 차이 |
| `futs_sdpr` | 선물 기준가 | String | 14 | Y |  |
| `hts_thpr` | HTS 이론가 | String | 14 | Y | 해당 월물의 이론적 가치를 계산한 것으로 주가지수 선물 이론가격은 (주가지수 선물 이론가격 = 주가지수 + 기간이자비용 - 기간배당수입) 로 계산 |
| `dprt` | 괴리율 | String | 11 | Y | 현재의 시장가가 이론가격으로부터 얼마나 벗어나 있는지에 대한 측정 자료 괴리도 = (현재가 - 이론가격) |
| `crbr_aply_mxpr` | 서킷브레이커 적용 상한가 | String | 14 | Y |  |
| `crbr_aply_llam` | 서킷브레이커 적용 하한가 | String | 14 | Y |  |
| `futs_last_tr_date` | 선물 최종 거래 일자 | String | 8 | Y | 해당 선물 종목의 마지막 거래일 |
| `hts_rmnn_dynu` | HTS 잔존 일수 | String | 5 | Y | 최종 거래일까지 남은 일수 |
| `futs_lstn_medm_hgpr` | 선물 상장 중 최고가 | String | 14 | Y | 해당 선물 종목의 상장일 이후 최고 거래가격 |
| `futs_lstn_medm_lwpr` | 선물 상장 중 최저가 | String | 14 | Y | 해당 선물 종목의 상장일 이후 최저 거래가격 |
| `delta_val` | 델타 값 | String | 16 | Y | 옵션 종목의 지표값 |
| `gama` | 감마 | String | 13 | Y | 옵션 종목의 지표값 |
| `theta` | 세타 | String | 13 | Y | 옵션 종목의 지표값 |
| `vega` | 베가 | String | 13 | Y | 옵션 종목의 지표값 |
| `rho` | 로우 | String | 13 | Y | 옵션 종목의 지표값 |
| `hist_vltl` | 역사적 변동성 | String | 16 | Y | 옵션 종목의 지표값 |
| `hts_ints_vltl` | HTS 내재 변동성 | String | 16 | Y | 옵션 종목의 지표값 |
| `mrkt_basis` | 시장 베이시스 | String | 13 | Y | 시장베이시스 현재 시장에서 형성된 선물가격과 현물가격과의 차이 |
| `acpr` | 행사가 | String | 14 | Y | 옵션의 행사가격 |
| `output2` | 응답상세2 | String |  | Y |  |
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y | 종목명 |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 14 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 14 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 11 | Y |  |
| `output3` | 응답상세3 | String |  | Y |  |
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 14 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 14 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 11 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "hts_kor_isnm": "F 202203",
    "futs_prpr": "395.00",
    "futs_prdy_vrss": "6.70",
    "prdy_vrss_sign": "2",
    "futs_prdy_clpr": "388.30",
    "futs_prdy_ctrt": "1.73",
    "acml_vol": "220924",
    "acml_tr_pbmn": "21741293338",
    "hts_otst_stpl_qty": "247121",
    "otst_stpl_qty_icdc": "-592",
    "futs_oprc": "391.05",
    "futs_hgpr": "395.15",
    "futs_lwpr": "391.00",
    "futs_mxpr": "419.35",
    "futs_llam": "357.25",
    "basis": "0.82",
    "futs_sdpr": "388.30",
    "hts_thpr": "395.48",
    "dprt": "-0.12",
    "crbr_aply_mxpr": "0.00",
    "crbr_aply_llam": "0.00",
    "futs_last_tr_date": "20220310",
    "hts_rmnn_dynu": "58",
    "futs_lstn_medm_hgpr": "434.00",
    "futs_lstn_medm_lwpr": "366.60",
    "delta_val": "1.0000",
    "gama": "0.0000",
    "theta": "0.0000",
    "vega": "0.0000",
    "rho": "0.0000",
    "mrkt_basis": "0.34"
  },
  "output2": {
    "bstp_cls_code": "0001",
    "hts_kor_isnm": "종합",
    "bstp_nmix_prpr": "2972.48",
    "prdy_vrss_sign": "2",
    "bstp_nmix_prdy_vrss": "45.10",
    "bstp_nmix_prdy_ctrt": "1.54"
  },
  "output3": {
    "bstp_cls_code": "2001",
    "hts_kor_isnm": "KOSPI200",
    "bstp_nmix_prpr": "394.66",
    "prdy_vrss_sign": "2",
    "bstp_nmix_prdy_vrss": "5.69",
    "bstp_nmix_prdy_ctrt": "1.46"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다!"
}
```
