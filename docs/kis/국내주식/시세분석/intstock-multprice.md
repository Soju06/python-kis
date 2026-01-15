# 관심종목(멀티종목) 시세조회 [국내주식-205]

> [국내주식] 시세분석

관심종목(멀티종목) 시세조회 API입니다.
① 관심종목 그룹조회 → ② 관심종목 그룹별 종목조회 → ③ 관심종목(멀티종목) 시세조회 순서대로 호출하셔서 관심종목 시세 조회 가능합니다.

※ 한 번의 호출에 최대 30종목의 시세 확인 가능합니다.
그룹별종목조회 결과를 아래와 같이 입력하셔서 총 30종목까지 복수종목 조회 가능합니다.(아래 Example 참고)
. fid_mrkt_cls_code(시장구분) → FID_COND_MRKT_DIV_CODE_1
. jong_code(종목코드) 1 → FID_INPUT_ISCD_1
...

한국투자증권 Github 에서 관심종목 복수시세조회 파이썬 샘플코드를 참고하실 수 있습니다.
https://github.com/koreainvestment/open-trading-api/blob/main/rest/get_interest_stocks_price.py


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fee465d1-7fd5-4c66-b4a4-731b813d569d` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/intstock-multprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHKST11300006` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST11300006 |
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
| `FID_COND_MRKT_DIV_CODE_1` | 조건 시장 분류 코드1 | String | 2 | Y | 그룹별종목조회 결과 fid_mrkt_cls_code(시장구분) 1 입력 J: KRX, NX: NXT, UN: 통합 ex) J |
| `FID_INPUT_ISCD_1` | 입력 종목코드1 | String | 16 | Y | 그룹별종목조회 결과 jong_code(종목코드) 1 입력 ex) 005930 |
| `FID_COND_MRKT_DIV_CODE_2` | 조건 시장 분류 코드2 | String | 2 | Y |  |
| `FID_INPUT_ISCD_2` | 입력 종목코드2 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_3` | 조건 시장 분류 코드3 | String | 2 | Y |  |
| `FID_INPUT_ISCD_3` | 입력 종목코드3 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_4` | 조건 시장 분류 코드4 | String | 2 | Y |  |
| `FID_INPUT_ISCD_4` | 입력 종목코드4 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_5` | 조건 시장 분류 코드5 | String | 2 | Y |  |
| `FID_INPUT_ISCD_5` | 입력 종목코드5 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_6` | 조건 시장 분류 코드6 | String | 2 | Y |  |
| `FID_INPUT_ISCD_6` | 입력 종목코드6 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_7` | 조건 시장 분류 코드7 | String | 2 | Y |  |
| `FID_INPUT_ISCD_7` | 입력 종목코드7 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_8` | 조건 시장 분류 코드8 | String | 2 | Y |  |
| `FID_INPUT_ISCD_8` | 입력 종목코드8 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_9` | 조건 시장 분류 코드9 | String | 2 | Y |  |
| `FID_INPUT_ISCD_9` | 입력 종목코드9 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_10` | 조건 시장 분류 코드10 | String | 12 | Y |  |
| `FID_INPUT_ISCD_10` | 입력 종목코드10 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_11` | 조건 시장 분류 코드11 | String | 2 | Y |  |
| `FID_INPUT_ISCD_11` | 입력 종목코드11 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_12` | 조건 시장 분류 코드12 | String | 2 | Y |  |
| `FID_INPUT_ISCD_12` | 입력 종목코드12 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_13` | 조건 시장 분류 코드13 | String | 2 | Y |  |
| `FID_INPUT_ISCD_13` | 입력 종목코드13 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_14` | 조건 시장 분류 코드14 | String | 2 | Y |  |
| `FID_INPUT_ISCD_14` | 입력 종목코드14 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_15` | 조건 시장 분류 코드15 | String | 2 | Y |  |
| `FID_INPUT_ISCD_15` | 입력 종목코드15 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_16` | 조건 시장 분류 코드16 | String | 2 | Y |  |
| `FID_INPUT_ISCD_16` | 입력 종목코드16 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_17` | 조건 시장 분류 코드17 | String | 2 | Y |  |
| `FID_INPUT_ISCD_17` | 입력 종목코드17 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_18` | 조건 시장 분류 코드18 | String | 2 | Y |  |
| `FID_INPUT_ISCD_18` |  입력 종목코드18 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_19` | 조건 시장 분류 코드19 | String | 2 | Y |  |
| `FID_INPUT_ISCD_19` | 입력 종목코드19 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_20` | 조건 시장 분류 코드20 | String | 2 | Y |  |
| `FID_INPUT_ISCD_20` | 입력 종목코드20 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_21` | 조건 시장 분류 코드21 | String | 2 | Y |  |
| `FID_INPUT_ISCD_21` | 입력 종목코드21 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_22` | 조건 시장 분류 코드22 | String | 2 | Y |  |
| `FID_INPUT_ISCD_22` | 입력 종목코드22 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_23` | 조건 시장 분류 코드23 | String | 2 | Y |  |
| `FID_INPUT_ISCD_23` | 입력 종목코드23 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_24` | 조건 시장 분류 코드24 | String | 2 | Y |  |
| `FID_INPUT_ISCD_24` | 입력 종목코드24 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_25` | 조건 시장 분류 코드25 | String | 2 | Y |  |
| `FID_INPUT_ISCD_25` | 입력 종목코드25 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_26` | 조건 시장 분류 코드26 | String | 16 | Y |  |
| `FID_INPUT_ISCD_26` | 입력 종목코드26 | String | 2 | Y |  |
| `FID_COND_MRKT_DIV_CODE_27` | 조건 시장 분류 코드27 | String | 2 | Y |  |
| `FID_INPUT_ISCD_27` | 입력 종목코드27 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_28` | 조건 시장 분류 코드28 | String | 2 | Y |  |
| `FID_INPUT_ISCD_28` | 입력 종목코드28 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_29` | 조건 시장 분류 코드29 | String | 2 | Y |  |
| `FID_INPUT_ISCD_29` | 입력 종목코드29 | String | 16 | Y |  |
| `FID_COND_MRKT_DIV_CODE_30` | 조건 시장 분류 코드30 | String | 2 | Y |  |
| `FID_INPUT_ISCD_30` | 입력 종목코드30 | String | 16 | Y |  |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE_1:J
FID_INPUT_ISCD_1:005930
FID_COND_MRKT_DIV_CODE_2:J
FID_INPUT_ISCD_2:000660
FID_COND_MRKT_DIV_CODE_3:U
FID_INPUT_ISCD_3:0001
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
| `kospi_kosdaq_cls_name` | 코스피 코스닥 구분 명 | String | 10 | Y |  |
| `mrkt_trtm_cls_name` | 시장 조치 구분 명 | String | 10 | Y |  |
| `hour_cls_code` | 시간 구분 코드 | String | 1 | Y |  |
| `inter_shrn_iscd` | 관심 단축 종목코드 | String | 16 | Y |  |
| `inter_kor_isnm` | 관심 한글 종목명 | String | 40 | Y |  |
| `inter2_prpr` | 관심2 현재가 | String | 11 | Y |  |
| `inter2_prdy_vrss` | 관심2 전일 대비 | String | 11 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `inter2_oprc` | 관심2 시가 | String | 11 | Y |  |
| `inter2_hgpr` | 관심2 고가 | String | 11 | Y |  |
| `inter2_lwpr` | 관심2 저가 | String | 11 | Y |  |
| `inter2_llam` | 관심2 하한가 | String | 11 | Y |  |
| `inter2_mxpr` | 관심2 상한가 | String | 11 | Y |  |
| `inter2_askp` | 관심2 매도호가 | String | 11 | Y |  |
| `inter2_bidp` | 관심2 매수호가 | String | 11 | Y |  |
| `seln_rsqn` | 매도 잔량 | String | 12 | Y |  |
| `shnu_rsqn` | 매수2 잔량 | String | 12 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `inter2_prdy_clpr` | 관심2 전일 종가 | String | 11 | Y |  |
| `oprc_vrss_hgpr_rate` | 시가 대비 최고가 비율 | String | 84 | Y |  |
| `intr_antc_cntg_vrss` | 관심 예상 체결 대비 | String | 11 | Y |  |
| `intr_antc_cntg_vrss_sign` | 관심 예상 체결 대비 부호 | String | 1 | Y |  |
| `intr_antc_cntg_prdy_ctrt` | 관심 예상 체결 전일 대비율 | String | 72 | Y |  |
| `intr_antc_vol` | 관심 예상 거래량 | String | 18 | Y |  |
| `inter2_sdpr` | 관심2 기준가 | String | 11 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "kospi_kosdaq_cls_name": "거래소",
      "mrkt_trtm_cls_name": "거래소",
      "hour_cls_code": "0",
      "inter_shrn_iscd": "005930",
      "inter_kor_isnm": "삼성전자",
      "inter2_prpr": "77400",
      "inter2_prdy_vrss": "-800",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.02",
      "acml_vol": "15713440",
      "inter2_oprc": "78600",
      "inter2_hgpr": "78800",
      "inter2_lwpr": "77200",
      "inter2_llam": "54800",
      "inter2_mxpr": "101600",
      "inter2_askp": "77400",
      "inter2_bidp": "77300",
      "seln_rsqn": "10248",
      "shnu_rsqn": "269626",
      "total_askp_rsqn": "1404667",
      "total_bidp_rsqn": "2150657",
      "acml_tr_pbmn": "1221686345500",
      "inter2_prdy_clpr": "78200",
      "oprc_vrss_hgpr_rate": "0.25",
      "intr_antc_cntg_vrss": "0",
      "intr_antc_cntg_vrss_sign": "3",
      "intr_antc_cntg_prdy_ctrt": "0.00",
      "intr_antc_vol": "0",
      "inter2_sdpr": "78200"
    },
    {
      "kospi_kosdaq_cls_name": "거래소",
      "mrkt_trtm_cls_name": "거래소",
      "hour_cls_code": "0",
      "inter_shrn_iscd": "000660",
      "inter_kor_isnm": "SK하이닉스",
      "inter2_prpr": "189900",
      "inter2_prdy_vrss": "-3100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.61",
      "acml_vol": "2758944",
      "inter2_oprc": "192000",
      "inter2_hgpr": "193500",
      "inter2_lwpr": "189900",
      "inter2_llam": "135100",
      "inter2_mxpr": "250500",
      "inter2_askp": "190000",
      "inter2_bidp": "189900",
      "seln_rsqn": "5625",
      "shnu_rsqn": "4782",
      "total_askp_rsqn": "27318",
      "total_bidp_rsqn": "33313",
      "acml_tr_pbmn": "528227479600",
      "inter2_prdy_clpr": "193000",
      "oprc_vrss_hgpr_rate": "0.78",
      "intr_antc_cntg_vrss": "0",
      "intr_antc_cntg_vrss_sign": "3",
      "intr_antc_cntg_prdy_ctrt": "0.00",
      "intr_antc_vol": "0",
      "inter2_sdpr": "193000"
    },
    {
      "kospi_kosdaq_cls_name": "업종",
      "mrkt_trtm_cls_name": "",
      "hour_cls_code": "2",
      "inter_shrn_iscd": "0001",
      "inter_kor_isnm": "종합",
      "inter2_prpr": "2724.62",
      "inter2_prdy_vrss": "-28.38",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.03",
      "acml_vol": "561107",
      "inter2_oprc": "2751.47",
      "inter2_hgpr": "2752.17",
      "inter2_lwpr": "2724.62",
      "inter2_llam": "",
      "inter2_mxpr": "",
      "inter2_askp": "",
      "inter2_bidp": "",
      "seln_rsqn": "",
      "shnu_rsqn": "",
      "total_askp_rsqn": "19237981",
      "total_bidp_rsqn": "49315150",
      "acml_tr_pbmn": "10288958",
      "inter2_prdy_clpr": "2753.00",
      "oprc_vrss_hgpr_rate": "",
      "intr_antc_cntg_vrss": "-28.18",
      "intr_antc_cntg_vrss_sign": "5",
      "intr_antc_cntg_prdy_ctrt": "-1.02",
      "intr_antc_vol": "560841",
      "inter2_sdpr": "2753.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

