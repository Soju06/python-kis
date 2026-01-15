# KRX야간옵션 실시간체결가 [실시간-032]

> [국내선물옵션] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4d079440-555b-4773-a484-67bf170e9b27` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0EUCNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0EUCNT0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17
- **최종 수정일**: 2025-06-13

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | 1: 등록, 2:해제 |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 2 | Y | H0EUCNT0 |
| `tr_key` | 구분값 | String | 12 | Y | 야간옵션 종목코드 |

### 요청 예시

```json
{
  "header": {
    "approval_key": "35xxxxxa-bxxa-4xxb-87xxx-f56xxxxxxxxxx",
    "custtype": "P",
    "tr_type": "1",
    "content-type": "utf-8"
  },
  "body": {
    "input": {
      "tr_id": "H0EUCNT0",
      "tr_key": "301V06362"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `OPTN_SHRN_ISCD` | 옵션단축종목코드 | String | 9 | Y |  |
| `BSOP_HOUR` | 영업시간 | String | 6 | Y |  |
| `OPTN_PRPR` | 옵션현재가 | String | 1 | Y |  |
| `PRDY_VRSS_SIGN` | 전일대비부호 | String | 1 | Y |  |
| `OPTN_PRDY_VRSS` | 옵션전일대비 | String | 1 | Y |  |
| `PRDY_CTRT` | 전일대비율 | String | 1 | Y |  |
| `OPTN_OPRC` | 옵션시가2 | String | 1 | Y |  |
| `OPTN_HGPR` | 옵션최고가 | String | 1 | Y |  |
| `OPTN_LWPR` | 옵션최저가 | String | 1 | Y |  |
| `LAST_CNQN` | 최종거래량 | String | 1 | Y |  |
| `ACML_VOL` | 누적거래량 | String | 1 | Y |  |
| `ACML_TR_PBMN` | 누적거래대금 | String | 1 | Y |  |
| `HTS_THPR` | HTS이론가 | String | 1 | Y |  |
| `HTS_OTST_STPL_QTY` | HTS미결제약정수량 | String | 1 | Y |  |
| `OTST_STPL_QTY_ICDC` | 미결제약정수량증감 | String | 1 | Y |  |
| `OPRC_HOUR` | 시가시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가2대비현재가부호 | String | 1 | Y |  |
| `OPRC_VRSS_NMIX_PRPR` | 시가대비지수현재가 | String | 1 | Y |  |
| `HGPR_HOUR` | 최고가시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 최고가대비현재가부호 | String | 1 | Y |  |
| `HGPR_VRSS_NMIX_PRPR` | 최고가대비지수현재가 | String | 1 | Y |  |
| `LWPR_HOUR` | 최저가시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 최저가대비현재가부호 | String | 1 | Y |  |
| `LWPR_VRSS_NMIX_PRPR` | 최저가대비지수현재가 | String | 1 | Y |  |
| `SHNU_RATE` | 매수2비율 | String | 1 | Y |  |
| `PRMM_VAL` | 프리미엄값 | String | 1 | Y |  |
| `INVL_VAL` | 내재가치값 | String | 1 | Y |  |
| `TMVL_VAL` | 시간가치값 | String | 1 | Y |  |
| `DELTA` | 델타 | String | 1 | Y |  |
| `GAMA` | 감마 | String | 1 | Y |  |
| `VEGA` | 베가 | String | 1 | Y |  |
| `THETA` | 세타 | String | 1 | Y |  |
| `RHO` | 로우 | String | 1 | Y |  |
| `HTS_INTS_VLTL` | HTS내재변동성 | String | 1 | Y |  |
| `ESDG` | 괴리도 | String | 1 | Y |  |
| `OTST_STPL_RGBF_QTY_ICDC` | 미결제약정직전수량증감 | String | 1 | Y |  |
| `THPR_BASIS` | 이론베이시스 | String | 1 | Y |  |
| `UNAS_HIST_VLTL` | 역사적변동성 | String | 1 | Y |  |
| `CTTR` | 체결강도 | String | 1 | Y |  |
| `DPRT` | 괴리율 | String | 1 | Y |  |
| `MRKT_BASIS` | 시장베이시스 | String | 1 | Y |  |
| `OPTN_ASKP1` | 옵션매도호가1 | String | 1 | Y |  |
| `OPTN_BIDP1` | 옵션매수호가1 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 1 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 1 | Y |  |
| `SELN_CNTG_CSNU` | 매도체결건수 | String | 1 | Y |  |
| `SHNU_CNTG_CSNU` | 매수체결건수 | String | 1 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수체결건수 | String | 1 | Y |  |
| `SELN_CNTG_SMTN` | 총매도수량 | String | 1 | Y |  |
| `SHNU_CNTG_SMTN` | 총매수수량 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 1 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일거래량대비등락율 | String | 1 | Y |  |
| `DYNM_MXPR` | 실시간상한가 | String | 8 | Y |  |
| `DYNM_PRC_LIMT_YN` | 실시간가격제한구분 | String | 1 | Y |  |
| `DYNM_LLAM` | 실시간하한가 | String | 8 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0EUCNT0", 
        "tr_key": "301V06362", 
        "encrypt": "N"
        }, 
    "body": {
        "rt_cd": "0", 
        "msg_cd": "OPSP0000",
        "msg1": "SUBSCRIBE SUCCESS", 
        "output": {
            "iv": "0123456789abcdef", 
            "key": "abcdefghijklmnopabcdefghijklmnop"}
        }
}

# output
0|H0EUCNT0|001|301V06362^190612^2.98^5^-0.35^-10.51^3.06^3.09^2.98^1^106^0^-nan^0^0
^000000^5^-0.08^000000^5^-0.11^000000^3^0.00^0.25^0.00^0.00^2.98^-nan^-nan^-nan^nan^-nan^84.55^-nan^0
^-nan^nan^32.50^-nan^-363.10^3.00^2.98^15^1^33^18^-15^80^26^37^27^0.00

# output - 복호화 후
#### 야간옵션(EUREX) 체결 ####
============================================
### [1 / 1]
옵션단축종목코드     [301V06362]
영업시간         [190612]
옵션현재가        [2.98]
전일대비부호       [5]
옵션전일대비       [-0.35]
전일대비율        [-10.51]
옵션시가2        [3.06]
옵션최고가        [3.09]
옵션최저가        [2.98]
최종거래량        [1]
누적거래량        [106]
누적거래대금       [0]
HTS이론가       [-nan]
HTS미결제약정수량   [0]
미결제약정수량증감    [0]
시가시간         [000000]
시가2대비현재가부호   [5]
시가대비지수현재가    [-0.08]
최고가시간        [000000]
최고가대비현재가부호   [5]
최고가대비지수현재가   [-0.11]
최저가시간        [000000]
최저가대비현재가부호   [3]
최저가대비지수현재가   [0.00]
매수2비율        [0.25]
프리미엄값        [0.00]
내재가치값        [0.00]
시간가치값        [2.98]
델타           [-nan]
감마           [-nan]
베가           [-nan]
세타           [nan]
로우           [-nan]
HTS내재변동성     [84.55]
괴리도          [-nan]
미결제약정직전수량증감  [0]
이론베이시스       [-nan]
역사적변동성       [nan]
체결강도         [32.50]
괴리율          [-nan]
시장베이시스       [-363.10]
옵션매도호가1      [3.00]
옵션매수호가1      [2.98]
매도호가잔량1      [15]
매수호가잔량1      [1]
매도체결건수       [33]
매수체결건수       [18]
순매수체결건수      [-15]
총매도수량        [80]
총매수수량        [26]
총매도호가잔량      [37]
총매수호가잔량      [27]
전일거래량대비등락율   [0.00]
```

