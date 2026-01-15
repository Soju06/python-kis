# 관심종목 그룹별 종목조회 [국내주식-203]

> [국내주식] 시세분석

관심종목 그룹별 종목조회 API입니다.
① 관심종목 그룹조회 → ② 관심종목 그룹별 종목조회 → ③ 관심종목(멀티종목) 시세조회 순서대로 호출하셔서 관심종목 시세 조회 가능합니다.

※ 한 번의 호출에 최대 30종목의 시세 확인 가능합니다.

한국투자증권 Github 에서 관심종목 복수시세조회 파이썬 샘플코드를 참고하실 수 있습니다.
https://github.com/koreainvestment/open-trading-api/blob/main/rest/get_interest_stocks_price.py


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4d8c6e7a-a026-4f8d-8c64-9e7ecbc3d97e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `HHKCM113004C6` |
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
| `tr_id` | 거래ID | String | 13 | Y | HHKCM113004C6 |
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
| `TYPE` | 관심종목구분코드                 | String | 1 | Y | Unique key(1) |
| `USER_ID` | 사용자 ID                 | String | 16 | Y | HTS_ID 입력 |
| `DATA_RANK` | 데이터 순위            | String | 10 | Y | 공백 |
| `INTER_GRP_CODE` | 관심 그룹 코드        | String | 3 | Y | 관심그룹 조회 결과의 그룹 값 입력 |
| `INTER_GRP_NAME` | 관심 그룹 명       | String | 40 | Y | 공백 |
| `HTS_KOR_ISNM` | HTS 한글 종목명      | String | 40 | Y | 공백 |
| `CNTG_CLS_CODE` | 체결 구분 코드          | String | 1 | Y | 공백 |
| `FID_ETC_CLS_CODE` | 기타 구분 코드  | String | 2 | Y | Unique key(4) |

### 요청 예시

```json
TYPE:1
USER_ID:{{HTS_ID}}
DATA_RANK:
INTER_GRP_CODE:002
INTER_GRP_NAME:
HTS_KOR_ISNM:
CNTG_CLS_CODE:
FID_ETC_CLS_CODE:4
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
| `output1` | 응답상세 | String |   | Y |  |
| `data_rank` | 데이터 순위      | String | 10 | Y |  |
| `inter_grp_name` | 관심 그룹 명 | String | 40 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `fid_mrkt_cls_code` | FID 시장 구분 코드 | String | 2 | Y |  |
| `data_rank` | 데이터 순위           | String | 10 | Y |  |
| `exch_code` | 거래소코드                | String | 4 | Y |  |
| `jong_code` | 종목코드                | String | 16 | Y |  |
| `color_code` | 생상 코드               | String | 8 | Y |  |
| `memo` | 메모                      | String | 128 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명     | String | 40 | Y |  |
| `fxdt_ntby_qty` | 기준일 순매수 수량  | String | 12 | Y |  |
| `cntg_unpr` | 체결단가              | String | 11 | Y |  |
| `cntg_cls_code` | 체결 구분 코드         | String | 1 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "data_rank": "0000000002",
    "inter_grp_name": "관심종목02"
  },
  "output2": [
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000001",
      "exch_code": "KRX",
      "jong_code": "006840",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "AK홀딩스",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000002",
      "exch_code": "KRX",
      "jong_code": "054620",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "APS홀딩스",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000003",
      "exch_code": "KRX",
      "jong_code": "265520",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "AP시스템",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000004",
      "exch_code": "KRX",
      "jong_code": "211270",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "AP위성",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000005",
      "exch_code": "KRX",
      "jong_code": "138930",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "BNK금융지주",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000006",
      "exch_code": "KRX",
      "jong_code": "001460",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "BYC",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000007",
      "exch_code": "KRX",
      "jong_code": "001465",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "BYC우",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000008",
      "exch_code": "KRX",
      "jong_code": "013720",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CBI",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000009",
      "exch_code": "KRX",
      "jong_code": "001040",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000010",
      "exch_code": "KRX",
      "jong_code": "079160",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ CGV",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000011",
      "exch_code": "KRX",
      "jong_code": "035760",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ ENM",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000012",
      "exch_code": "KRX",
      "jong_code": "311690",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ 바이오사이언스",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000013",
      "exch_code": "KRX",
      "jong_code": "00104K",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ4우(전환)",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000014",
      "exch_code": "KRX",
      "jong_code": "000120",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ대한통운",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000015",
      "exch_code": "KRX",
      "jong_code": "011150",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ씨푸드",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000016",
      "exch_code": "KRX",
      "jong_code": "011155",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "CJ씨푸드1우",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000017",
      "exch_code": "KRX",
      "jong_code": "060310",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "3S",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000018",
      "exch_code": "KRX",
      "jong_code": "095570",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "AJ네트웍스",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000019",
      "exch_code": "KRX",
      "jong_code": "006840",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "AK홀딩스",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000020",
      "exch_code": "KRX",
      "jong_code": "054620",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "APS",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000021",
      "exch_code": "KRX",
      "jong_code": "265520",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "AP시스템",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    },
    {
      "fid_mrkt_cls_code": "J",
      "data_rank": "0000000022",
      "exch_code": "KRX",
      "jong_code": "211270",
      "color_code": "-1",
      "memo": "",
      "hts_kor_isnm": "AP위성",
      "fxdt_ntby_qty": "0",
      "cntg_unpr": "0.000000",
      "cntg_cls_code": "0"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

