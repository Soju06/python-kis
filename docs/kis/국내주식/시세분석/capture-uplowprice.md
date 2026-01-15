# 국내주식 상하한가 포착 [국내주식-190]

> [국내주식] 시세분석

국내주식 상하한가 포착 API입니다.
한국투자 HTS(eFriend Plus) > [0917] 실시간 상하한가 포착 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `30654e7a-8eda-42ac-8b54-9f0287bde15d` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/capture-uplowprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHKST130000C0` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST130000C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | 시장구분(J) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | 11300(Unique key) |
| `FID_PRC_CLS_CODE` | 상하한가 구분코드 | String | 2 | Y | 0(상한가),1(하한가) |
| `FID_DIV_CLS_CODE` | 분류구분코드 | String | 2 | Y | '0(상하한가종목),6(8%상하한가 근접), 5(10%상하한가 근접), 1(15%상하한가 근접),2(20%상하한가 근접), 3(25%상하한가 근접)' |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 전체(0000), 코스피(0001),코스닥(1001) |
| `FID_TRGT_CLS_CODE` | 대상구분코드 | String | 32 | Y | 공백 입력 |
| `FID_TRGT_EXLS_CLS_CODE` | 대상제외구분코드 | String | 32 | Y | 공백 입력 |
| `FID_INPUT_PRICE_1` | 입력가격1 | String | 12 | Y | 공백 입력 |
| `FID_INPUT_PRICE_2` | 입력가격2 | String | 12 | Y | 공백 입력 |
| `FID_VOL_CNT` | 거래량수 | String | 12 | Y | 공백 입력 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_COND_SCR_DIV_CODE:11300
FID_PRC_CLS_CODE:0
FID_DIV_CLS_CODE:0
FID_INPUT_ISCD:0000
FID_TRGT_CLS_CODE:
FID_TRGT_EXLS_CLS_CODE:
FID_INPUT_PRICE_1:
FID_INPUT_PRICE_2:
FID_VOL_CNT:
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
| `mksc_shrn_iscd` | 유가증권단축종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `total_askp_rsqn` | 총매도호가잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총매수호가잔량 | String | 12 | Y |  |
| `askp_rsqn1` | 매도호가잔량1 | String | 12 | Y |  |
| `bidp_rsqn1` | 매수호가잔량1 | String | 12 | Y |  |
| `prdy_vol` | 전일거래량 | String | 18 | Y |  |
| `seln_cnqn` | 매도체결량 | String | 18 | Y |  |
| `shnu_cnqn` | 매수2체결량 | String | 18 | Y |  |
| `stck_llam` | 주식하한가 | String | 10 | Y |  |
| `stck_mxpr` | 주식상한가 | String | 10 | Y |  |
| `prdy_vrss_vol_rate` | 전일대비거래량비율 | String | 84 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mksc_shrn_iscd": "012800",
      "hts_kor_isnm": "대창",
      "stck_prpr": "2080",
      "prdy_vrss_sign": "1",
      "prdy_vrss": "478",
      "prdy_ctrt": "29.84",
      "acml_vol": "39937550",
      "total_askp_rsqn": "0",
      "total_bidp_rsqn": "2648946",
      "askp_rsqn1": "0",
      "bidp_rsqn1": "2299811",
      "prdy_vol": "4003121",
      "seln_cnqn": "2",
      "shnu_cnqn": "0",
      "stck_llam": "1122",
      "stck_mxpr": "2080",
      "prdy_vrss_vol_rate": "997.66"
    },
    {
      "mksc_shrn_iscd": "215100",
      "hts_kor_isnm": "로보로보",
      "stck_prpr": "5680",
      "prdy_vrss_sign": "1",
      "prdy_vrss": "1310",
      "prdy_ctrt": "29.98",
      "acml_vol": "10240653",
      "total_askp_rsqn": "0",
      "total_bidp_rsqn": "622698",
      "askp_rsqn1": "0",
      "bidp_rsqn1": "553376",
      "prdy_vol": "34944",
      "seln_cnqn": "40",
      "shnu_cnqn": "0",
      "stck_llam": "3060",
      "stck_mxpr": "5680",
      "prdy_vrss_vol_rate": "29305.90"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

