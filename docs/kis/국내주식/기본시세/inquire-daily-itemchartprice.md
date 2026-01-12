# 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]

> [국내주식] 기본시세

국내주식기간별시세(일/주/월/년) API입니다.
실전계좌/모의계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다.

[국내주식-016 v1] 국내주식기간별시세(일/주/월/년)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a08c3421-e50f-4f24-b1fe-64c12f723c77` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHKST03010100` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-05-25
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST03010100 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |
| `FID_INPUT_DATE_1` | 입력 날짜 1 | String | 10 | Y | 조회 시작일자 |
| `FID_INPUT_DATE_2` | 입력 날짜 2 | String | 10 | Y | 조회 종료일자 (최대 100개) |
| `FID_PERIOD_DIV_CODE` | 기간분류코드 | String | 32 | Y | D:일봉 W:주봉, M:월봉, Y:년봉 |
| `FID_ORG_ADJ_PRC` | 수정주가 원주가 가격 여부 | String | 10 | Y | 0:수정주가 1:원주가 |

### 요청 예시

```json
"input": {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_date_1": "20220411",
            "fid_input_date_2": "20220509",
            "fid_input_iscd": "000660",
            "fid_org_adj_prc": "0",
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
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output1` | 응답상세 | String |   | Y | single |
| `prdy_vrss` | 전일 대비  | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 11 | Y |  |
| `stck_prdy_clpr` | 주식 전일 종가 | String | 10 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `stck_shrn_iscd` | 주식 단축 종목코드 | String | 9 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `stck_mxpr` | 주식 상한가 | String | 10 | Y |  |
| `stck_llam` | 주식 하한가 | String | 10 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `stck_prdy_oprc` | 주식 전일 시가 | String | 10 | Y |  |
| `stck_prdy_hgpr` | 주식 전일 최고가 | String | 10 | Y |  |
| `stck_prdy_lwpr` | 주식 전일 최저가 | String | 10 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `prdy_vrss_vol` | 전일 대비 거래량 | String | 18 | Y |  |
| `vol_tnrt` | 거래량 회전율 | String | 11 | Y | 11(8.2) |
| `stck_fcam` | 주식 액면가 | String | 11 | Y |  |
| `lstn_stcn` | 상장 주수 | String | 18 | Y |  |
| `cpfn` | 자본금 | String | 22 | Y |  |
| `hts_avls` | HTS 시가총액 | String | 18 | Y |  |
| `per` | PER | String | 11 | Y | 11(8.2) |
| `eps` | EPS | String | 14 | Y | 14(11.2) |
| `pbr` | PBR | String | 11 | Y | 11(8.2) |
| `itewhol_loan_rmnd_ratem` | 전체 융자 잔고 비율 | String | 13 | Y | 13(8.4) |
| `output2` | 응답상세 | Object |   | Y | Array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_clpr` | 주식 종가 | String | 10 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `flng_cls_code` | 락 구분 코드 | String | 2 | Y | 01 : 권리락 02 : 배당락 03 : 분배락 04 : 권배락 05 : 중간(분기)배당락 06 : 권리중간배당락 07 : 권리분기배당락 |
| `prtt_rate` | 분할 비율 | String | 11 | Y | 기준가/전일 종가 |
| `mod_yn` | 변경 여부 | String | 1 | Y | 현재 영업일에 체결이 발생하지 않아 시가가 없을경우 Y 로 표시(차트에서 사용) |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `revl_issu_reas` | 재평가사유코드 | String | 2 | Y | 00:해당없음 01:회사분할 02:자본감소 03:장기간정지 04:초과분배 05:대규모배당 06:회사분할합병 07:ETN증권병합/분할 08:신종증권기세조정 99:기타 |

### 응답 예시

```json
"msg_cd": "MCA00000",
        "output1": {
            "acml_tr_pbmn": "236062833000",
            "acml_vol": "2106409",
            "askp": "112500",
            "bidp": "112000",
            "cpfn": "36577",
            "eps": "13190.00",
            "hts_avls": "815363",
            "hts_kor_isnm": "SK\ud558\uc774\ub2c9\uc2a4",
            "itewhol_loan_rmnd_ratem name": "0.32",
            "lstn_stcn": "728002365",
            "pbr": "1.26",
            "per": "8.49",
            "prdy_ctrt": "0.90",
            "prdy_vol": "3680049",
            "prdy_vrss": "1000",
            "prdy_vrss_sign": "2",
            "prdy_vrss_vol": "-1573640",
            "stck_fcam": "5000",
            "stck_hgpr": "113000",
            "stck_llam": "78000",
            "stck_lwpr": "111000",
            "stck_mxpr": "144000",
            "stck_oprc": "111500",
            "stck_prdy_clpr": "111000",
            "stck_prdy_hgpr": "112500",
            "stck_prdy_lwpr": "110000",
            "stck_prdy_oprc": "110500",
            "stck_prpr": "112000",
            "stck_shrn_iscd": "000660",
            "vol_tnrt": "0.29"
        },
        "output2": [
            {
                "acml_tr_pbmn": "237914727500",
                "acml_vol": "2203472",
                "flng_cls_code": "00",
                "mod_yn": "N",
                "prdy_vrss": "0",
                "prdy_vrss_sign": "3",
                "prtt_rate": "0.00",
                "revl_issu_reas": "",
                "stck_bsop_date": "20220509",
                "stck_clpr": "107500",
                "stck_hgpr": "109000",
                "stck_lwpr": "106500",
                "stck_oprc": "107000"
            },
....
```
