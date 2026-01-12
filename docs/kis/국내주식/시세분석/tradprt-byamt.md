# 국내주식 체결금액별 매매비중 [국내주식-192]

> [국내주식] 시세분석

국내주식 체결금액별 매매비중 API입니다.
한국투자 HTS(eFriend Plus) > [0135] 체결금액별 매매비중 화면의 "상단 표" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `b290d16e-aa18-4e41-9c08-f4d941efe9a1` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/tradprt-byamt` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHKST111900C0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST111900C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | J: KRX, NX: NXT, UN: 통합 |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | Uniquekey(11119) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 종목코드(ex)(005930 (삼성전자)) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_COND_SCR_DIV_CODE:11119
FID_INPUT_ISCD:005930
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
| `output` | 응답상세 | Object |   | Y | array |
| `prpr_name` | 가격명 | String | 40 | Y |  |
| `smtn_avrg_prpr` | 합계 평균가격 | String | 10 | Y |  |
| `acml_vol` | 합계 거래량 | String | 18 | Y |  |
| `whol_ntby_qty_rate` | 합계 순매수비율 | String | 72 | Y |  |
| `ntby_cntg_csnu` | 합계 순매수건수 | String | 10 | Y |  |
| `seln_cnqn_smtn` | 매도 거래량 | String | 18 | Y |  |
| `whol_seln_vol_rate` | 매도 거래량비율 | String | 72 | Y |  |
| `seln_cntg_csnu` | 매도 건수 | String | 10 | Y |  |
| `shnu_cnqn_smtn` | 매수 거래량 | String | 18 | Y |  |
| `whol_shun_vol_rate` | 매수 거래량비율 | String | 72 | Y |  |
| `shnu_cntg_csnu` | 매수 건수 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "prpr_name": "3백 이하",
      "smtn_avrg_prpr": "78315",
      "acml_vol": "291426",
      "whol_ntby_qty_rate": "0.37",
      "ntby_cntg_csnu": "13297",
      "seln_cnqn_smtn": "126451",
      "whol_seln_vol_rate": "1.21",
      "seln_cntg_csnu": "16084",
      "shnu_cnqn_smtn": "164975",
      "whol_shun_vol_rate": "1.58",
      "shnu_cntg_csnu": "29381"
    },
    {
      "prpr_name": "5백 이하",
      "smtn_avrg_prpr": "78317",
      "acml_vol": "138138",
      "whol_ntby_qty_rate": "-0.13",
      "ntby_cntg_csnu": "-278",
      "seln_cnqn_smtn": "75634",
      "whol_seln_vol_rate": "0.73",
      "seln_cntg_csnu": "1525",
      "shnu_cnqn_smtn": "62504",
      "whol_shun_vol_rate": "0.60",
      "shnu_cntg_csnu": "1247"
    },
    {
      "prpr_name": "1천 이하",
      "smtn_avrg_prpr": "78304",
      "acml_vol": "378958",
      "whol_ntby_qty_rate": "0.10",
      "ntby_cntg_csnu": "110",
      "seln_cnqn_smtn": "184499",
      "whol_seln_vol_rate": "1.77",
      "seln_cntg_csnu": "2000",
      "shnu_cnqn_smtn": "194459",
      "whol_shun_vol_rate": "1.87",
      "shnu_cntg_csnu": "2110"
    },
    {
      "prpr_name": "3천 이하",
      "smtn_avrg_prpr": "78328",
      "acml_vol": "720672",
      "whol_ntby_qty_rate": "-0.51",
      "ntby_cntg_csnu": "-330",
      "seln_cnqn_smtn": "387086",
      "whol_seln_vol_rate": "3.72",
      "seln_cntg_csnu": "1993",
      "shnu_cnqn_smtn": "333586",
      "whol_shun_vol_rate": "3.20",
      "shnu_cntg_csnu": "1663"
    },
    {
      "prpr_name": "5천 이하",
      "smtn_avrg_prpr": "78349",
      "acml_vol": "429911",
      "whol_ntby_qty_rate": "0.16",
      "ntby_cntg_csnu": "63",
      "seln_cnqn_smtn": "206855",
      "whol_seln_vol_rate": "1.99",
      "seln_cntg_csnu": "426",
      "shnu_cnqn_smtn": "223056",
      "whol_shun_vol_rate": "2.14",
      "shnu_cntg_csnu": "489"
    },
    {
      "prpr_name": "1억 이하",
      "smtn_avrg_prpr": "78336",
      "acml_vol": "580130",
      "whol_ntby_qty_rate": "-1.24",
      "ntby_cntg_csnu": "-153",
      "seln_cnqn_smtn": "354585",
      "whol_seln_vol_rate": "3.40",
      "seln_cntg_csnu": "402",
      "shnu_cnqn_smtn": "225545",
      "whol_shun_vol_rate": "2.17",
      "shnu_cntg_csnu": "249"
    },
    {
      "prpr_name": "5억 이하",
      "smtn_avrg_prpr": "78326",
      "acml_vol": "1664623",
      "whol_ntby_qty_rate": "-1.57",
      "ntby_cntg_csnu": "-61",
      "seln_cnqn_smtn": "914220",
      "whol_seln_vol_rate": "8.78",
      "seln_cntg_csnu": "306",
      "shnu_cnqn_smtn": "750403",
      "whol_shun_vol_rate": "7.21",
      "shnu_cntg_csnu": "245"
    },
    {
      "prpr_name": "5억 초과",
      "smtn_avrg_prpr": "78316",
      "acml_vol": "6210233",
      "whol_ntby_qty_rate": "-18.01",
      "ntby_cntg_csnu": "-55",
      "seln_cnqn_smtn": "4042917",
      "whol_seln_vol_rate": "38.82",
      "seln_cntg_csnu": "173",
      "shnu_cnqn_smtn": "2167316",
      "whol_shun_vol_rate": "20.81",
      "shnu_cntg_csnu": "118"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
