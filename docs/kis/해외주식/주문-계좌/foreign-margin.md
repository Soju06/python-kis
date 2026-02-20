# 해외증거금 통화별조회 [해외주식-035]

> [해외주식] 주문/계좌

해외증거금 통화별조회 API입니다.
한국투자 HTS(eFriend Plus) > [7718] 해외주식 증거금상세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f8d92c02-7537-4ae5-88ca-fe3d0a7155db` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/foreign-margin` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC2101R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10T10:11:22+09:00
- **최종 수정일**: 2025-04-30T10:52:20+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | TTTC2101R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `ACNT_PRDT_CD` | 계좌상품코드  | String | 2 | Y |  |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | Object |   | Y | array |
| `natn_name` | 국가명            | String | 60 | Y |  |
| `crcy_cd` | 통화코드           | String | 3 | Y |  |
| `frcr_dncl_amt1` | 외화예수금액        | String | 186 | Y |  |
| `ustl_buy_amt` | 미결제매수금액       | String | 182 | Y |  |
| `ustl_sll_amt` | 미결제매도금액       | String | 182 | Y |  |
| `frcr_rcvb_amt` | 외화미수금액        | String | 182 | Y |  |
| `frcr_mgn_amt` | 외화증거금액        | String | 186 | Y |  |
| `frcr_gnrl_ord_psbl_amt` | 외화일반주문가능금액   | String | 182 | Y |  |
| `frcr_ord_psbl_amt1` | 외화주문가능금액     | String | 186 | Y | 원화주문가능환산금액 |
| `itgr_ord_psbl_amt` | 통합주문가능금액     | String | 182 | Y |  |
| `bass_exrt` | 기준환율           | String | 238 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "natn_name": "미국",
      "crcy_cd": "USD",
      "frcr_dncl_amt1": "698.190000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "694.37",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "1094.52",
      "bass_exrt": "1349.40000000"
    },
    {
      "natn_name": "홍콩",
      "crcy_cd": "HKD",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "8247.35",
      "bass_exrt": "172.97000000"
    },
    {
      "natn_name": "홍콩",
      "crcy_cd": "CNY",
      "frcr_dncl_amt1": "1459.110000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "7705.45",
      "bass_exrt": "186.89000000"
    },
    {
      "natn_name": "중화인민공화국",
      "crcy_cd": "CNY",
      "frcr_dncl_amt1": "1459.110000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "1448.97",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "7713.10",
      "bass_exrt": "186.89000000"
    },
    {
      "natn_name": "일본",
      "crcy_cd": "JPY",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "164359.92",
      "bass_exrt": "8.68370000"
    },
    {
      "natn_name": "베트남",
      "crcy_cd": "VND",
      "frcr_dncl_amt1": "377568.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "네덜란드",
      "crcy_cd": "USD",
      "frcr_dncl_amt1": "698.190000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "1094.52",
      "bass_exrt": "1349.40000000"
    },
    {
      "natn_name": "프랑스",
      "crcy_cd": "USD",
      "frcr_dncl_amt1": "698.190000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "1094.52",
      "bass_exrt": "1349.40000000"
    },
    {
      "natn_name": "영국",
      "crcy_cd": "USD",
      "frcr_dncl_amt1": "698.190000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "1094.52",
      "bass_exrt": "1349.40000000"
    },
    {
      "natn_name": "스위스",
      "crcy_cd": "USD",
      "frcr_dncl_amt1": "698.190000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "1094.52",
      "bass_exrt": "1349.40000000"
    },
    {
      "natn_name": "싱가포르",
      "crcy_cd": "USD",
      "frcr_dncl_amt1": "698.190000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "1094.52",
      "bass_exrt": "1349.40000000"
    },
    {
      "natn_name": "독일",
      "crcy_cd": "USD",
      "frcr_dncl_amt1": "698.190000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "1094.52",
      "bass_exrt": "1349.40000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    },
    {
      "natn_name": "",
      "crcy_cd": "",
      "frcr_dncl_amt1": "0.000000",
      "ustl_buy_amt": "0.00",
      "ustl_sll_amt": "0.00",
      "frcr_rcvb_amt": "0.00",
      "frcr_mgn_amt": "0.000000",
      "frcr_gnrl_ord_psbl_amt": "0.00",
      "frcr_ord_psbl_amt1": "0.000000",
      "itgr_ord_psbl_amt": "0.00",
      "bass_exrt": "0.00000000"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

