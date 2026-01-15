# 장내채권현재가(호가) [국내주식-132]

> [장내채권] 기본시세

장내채권현재가(호가) API입니다. 
한국투자 HTS(eFriend Plus) > [0978] 장내채권주문 "우측 호가창" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `0a5782f0-0c05-4feb-90f4-b86f09b45327` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/quotations/inquire-asking-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHKBJ773401C0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
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
| `tr_id` | 거래ID | String | 13 | Y | FHKBJ773401C0 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | B: 장내 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 채권종목코드 ex. KR2088012A16 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:B
FID_INPUT_ISCD:KR2088012A16
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
| `output` | 응답상세 | String |   | Y |  |
| `aspr_acpt_hour` | 호가 접수 시간 | String | 6 | Y |  |
| `bond_askp1` | 채권 매도호가1 | String | 112 | Y |  |
| `bond_askp2` | 채권 매도호가2 | String | 112 | Y |  |
| `bond_askp3` | 채권 매도호가3 | String | 112 | Y |  |
| `bond_askp4` | 채권 매도호가4 | String | 112 | Y |  |
| `bond_askp5` | 채권 매도호가5 | String | 112 | Y |  |
| `bond_bidp1` | 채권 매수호가1 | String | 112 | Y |  |
| `bond_bidp2` | 채권 매수호가2 | String | 112 | Y |  |
| `bond_bidp3` | 채권 매수호가3 | String | 112 | Y |  |
| `bond_bidp4` | 채권 매수호가4 | String | 112 | Y |  |
| `bond_bidp5` | 채권 매수호가5 | String | 112 | Y |  |
| `askp_rsqn1` | 매도호가 잔량1 | String | 12 | Y |  |
| `askp_rsqn2` | 매도호가 잔량2 | String | 12 | Y |  |
| `askp_rsqn3` | 매도호가 잔량3 | String | 12 | Y |  |
| `askp_rsqn4` | 매도호가 잔량4 | String | 12 | Y |  |
| `askp_rsqn5` | 매도호가 잔량5 | String | 12 | Y |  |
| `bidp_rsqn1` | 매수호가 잔량1 | String | 12 | Y |  |
| `bidp_rsqn2` | 매수호가 잔량2 | String | 12 | Y |  |
| `bidp_rsqn3` | 매수호가 잔량3 | String | 12 | Y |  |
| `bidp_rsqn4` | 매수호가 잔량4 | String | 12 | Y |  |
| `bidp_rsqn5` | 매수호가 잔량5 | String | 12 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `ntby_aspr_rsqn` | 순매수 호가 잔량 | String | 12 | Y |  |
| `seln_ernn_rate1` | 매도 수익 비율1 | String | 84 | Y |  |
| `seln_ernn_rate2` | 매도 수익 비율2 | String | 84 | Y |  |
| `seln_ernn_rate3` | 매도 수익 비율3 | String | 84 | Y |  |
| `seln_ernn_rate4` | 매도 수익 비율4 | String | 84 | Y |  |
| `seln_ernn_rate5` | 매도 수익 비율5 | String | 84 | Y |  |
| `shnu_ernn_rate1` | 매수2 수익 비율1 | String | 84 | Y |  |
| `shnu_ernn_rate2` | 매수2 수익 비율2 | String | 84 | Y |  |
| `shnu_ernn_rate3` | 매수2 수익 비율3 | String | 84 | Y |  |
| `shnu_ernn_rate4` | 매수2 수익 비율4 | String | 84 | Y |  |
| `shnu_ernn_rate5` | 매수2 수익 비율5 | String | 84 | Y |  |

### 응답 예시

```json
{
  "output": {
    "aspr_acpt_hour": "094618",
    "bond_askp1": "0.00",
    "bond_askp2": "0.00",
    "bond_askp3": "0.00",
    "bond_askp4": "0.00",
    "bond_askp5": "0.00",
    "bond_bidp1": "10190.20",
    "bond_bidp2": "10189.70",
    "bond_bidp3": "10189.40",
    "bond_bidp4": "10188.90",
    "bond_bidp5": "10188.60",
    "askp_rsqn1": "0",
    "askp_rsqn2": "0",
    "askp_rsqn3": "0",
    "askp_rsqn4": "0",
    "askp_rsqn5": "0",
    "bidp_rsqn1": "320138",
    "bidp_rsqn2": "53685",
    "bidp_rsqn3": "9081",
    "bidp_rsqn4": "8232",
    "bidp_rsqn5": "4020",
    "total_askp_rsqn": "0",
    "total_bidp_rsqn": "425156",
    "ntby_aspr_rsqn": "425156",
    "seln_ernn_rate1": "0.000",
    "seln_ernn_rate2": "0.000",
    "seln_ernn_rate3": "0.000",
    "seln_ernn_rate4": "0.000",
    "seln_ernn_rate5": "0.000",
    "shnu_ernn_rate1": "4.549",
    "shnu_ernn_rate2": "4.556",
    "shnu_ernn_rate3": "4.560",
    "shnu_ernn_rate4": "4.567",
    "shnu_ernn_rate5": "4.571"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
