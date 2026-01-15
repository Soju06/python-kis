# 국내주식업종기간별시세(일/주/월/년)[v1_국내주식-021]

> [국내주식] 업종/기타

국내주식 업종기간별시세(일/주/월/년) API입니다.
실전계좌/모의계좌의 경우, 한 번의 호출에 최대 50건까지 확인 가능합니다.

[국내주식-021 v1] 업종기간별시세(일/주/월/년)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `184519fc-37b5-4687-bebf-d3ddf5659729` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHKUP03500100` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-05-25
- **최종 수정일**: 2025-05-07

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 40 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | '[실전투자/모의투자] FHKUP03500100' |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 필수] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 업종 : U |
| `FID_INPUT_ISCD` | 업종 상세코드 | String | 2 | Y | '0001 : 종합 0002 : 대형주 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)' |
| `FID_INPUT_DATE_1` | 조회 시작일자 | String | 10 | Y | 조회 시작일자 (ex. 20220501) |
| `FID_INPUT_DATE_2` | 조회 종료일자 | String | 10 | Y | 조회 종료일자 (ex. 20220530) |
| `FID_PERIOD_DIV_CODE` | '	기간분류코드' | String | 32 | Y | '	D:일봉 W:주봉, M:월봉, Y:년봉' |

### 요청 예시

```json
"input": {
            "fid_cond_mrkt_div_code": "U",
            "fid_input_date_1": "20220411",
            "fid_input_date_2": "20220509",
            "fid_input_iscd": "0001",
            "fid_period_div_code": "D"
        }
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | N | [법인 필수] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output1` | 응답상세 | String |   | Y | Single |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `prdy_nmix` | 전일 지수 | String | 112 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `bstp_nmix_oprc` | 업종 지수 시가2 | String | 112 | Y |  |
| `bstp_nmix_hgpr` | 업종 지수 최고가 | String | 112 | Y |  |
| `bstp_nmix_lwpr` | 업종 지수 최저가 | String | 112 | Y |  |
| `futs_prdy_oprc` | 선물 전일 시가 | String | 112 | Y |  |
| `futs_prdy_hgpr` | 선물 전일 최고가 | String | 112 | Y |  |
| `futs_prdy_lwpr` | 선물 전일 최저가 | String | 112 | Y |  |
| `output2` | 응답상세 | Object |   | Y | Array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_oprc` | 업종 지수 시가2 | String | 112 | Y |  |
| `bstp_nmix_hgpr` | 업종 지수 최고가 | String | 112 | Y |  |
| `bstp_nmix_lwpr` | 업종 지수 최저가 | String | 112 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `mod_yn` | 변경 여부 | String | 1 | Y |  |

### 응답 예시

```json
"output1": {
            "acml_tr_pbmn": "4736153",
            "acml_vol": "305715",
            "bstp_cls_code": "0001",
            "bstp_nmix_hgpr": "2653.87",
            "bstp_nmix_lwpr": "2634.29",
            "bstp_nmix_oprc": "2651.63",
            "bstp_nmix_prdy_ctrt": "0.11",
            "bstp_nmix_prdy_vrss": "2.78",
            "bstp_nmix_prpr": "2642.07",
            "futs_prdy_hgpr": "2641.68",
            "futs_prdy_lwpr": "2605.38",
            "futs_prdy_oprc": "2605.78",
            "hts_kor_isnm": "\uc885\ud569",
            "prdy_nmix": "2639.29",
            "prdy_vol": "755653",
            "prdy_vrss_sign": "2"
        },
        "output2": [
            {
                "acml_tr_pbmn": "9289660",
                "acml_vol": "892653",
                "bstp_nmix_hgpr": "2642.75",
                "bstp_nmix_lwpr": "2606.08",
                "bstp_nmix_oprc": "2634.32",
                "bstp_nmix_prpr": "2610.81",
                "mod_yn": "N",
                "stck_bsop_date": "20220509"
            },
            {
                "acml_tr_pbmn": "10595418",
                "acml_vol": "1333936",
.....
```
