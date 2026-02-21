# 국내주식 시간외호가[국내주식-077]

> [국내주식] 기본시세

국내주식 시간외호가 API입니다. 
한국투자 HTS(eFriend Plus) > [0230] 시간외 현재가 화면의 '호가' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `6b0b388e-f815-4009-b46d-e08e47575ca7` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST02300400` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05T10:47:10+09:00
- **최종 수정일**: 2025-04-30T10:16:59+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST02300400 |
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
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 |
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |

### 요청 예시

```json
fid_cond_mrkt_div_code:J
fid_input_iscd:005930
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
| `ovtm_untp_last_hour` | 시간외 단일가 최종 시간 | String | 6 | Y |  |
| `ovtm_untp_askp1` | 시간외 단일가 매도호가1 | String | 10 | Y |  |
| `ovtm_untp_askp2` | 시간외 단일가 매도호가2 | String | 10 | Y |  |
| `ovtm_untp_askp3` | 시간외 단일가 매도호가3 | String | 10 | Y |  |
| `ovtm_untp_askp4` | 시간외 단일가 매도호가4 | String | 10 | Y |  |
| `ovtm_untp_askp5` | 시간외 단일가 매도호가5 | String | 10 | Y |  |
| `ovtm_untp_askp6` | 시간외 단일가 매도호가6 | String | 10 | Y |  |
| `ovtm_untp_askp7` | 시간외 단일가 매도호가7 | String | 10 | Y |  |
| `ovtm_untp_askp8` | 시간외 단일가 매도호가8 | String | 10 | Y |  |
| `ovtm_untp_askp9` | 시간외 단일가 매도호가9 | String | 10 | Y |  |
| `ovtm_untp_askp10` | 시간외 단일가 매도호가10 | String | 10 | Y |  |
| `ovtm_untp_bidp1` | 시간외 단일가 매수호가1 | String | 10 | Y |  |
| `ovtm_untp_bidp2` | 시간외 단일가 매수호가2 | String | 10 | Y |  |
| `ovtm_untp_bidp3` | 시간외 단일가 매수호가3 | String | 10 | Y |  |
| `ovtm_untp_bidp4` | 시간외 단일가 매수호가4 | String | 10 | Y |  |
| `ovtm_untp_bidp5` | 시간외 단일가 매수호가5 | String | 10 | Y |  |
| `ovtm_untp_bidp6` | 시간외 단일가 매수호가6 | String | 10 | Y |  |
| `ovtm_untp_bidp7` | 시간외 단일가 매수호가7 | String | 10 | Y |  |
| `ovtm_untp_bidp8` | 시간외 단일가 매수호가8 | String | 10 | Y |  |
| `ovtm_untp_bidp9` | 시간외 단일가 매수호가9 | String | 10 | Y |  |
| `ovtm_untp_bidp10` | 시간외 단일가 매수호가10 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc1` | 시간외 단일가 매도호가 증감1 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc2` | 시간외 단일가 매도호가 증감2 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc3` | 시간외 단일가 매도호가 증감3 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc4` | 시간외 단일가 매도호가 증감4 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc5` | 시간외 단일가 매도호가 증감5 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc6` | 시간외 단일가 매도호가 증감6 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc7` | 시간외 단일가 매도호가 증감7 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc8` | 시간외 단일가 매도호가 증감8 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc9` | 시간외 단일가 매도호가 증감9 | String | 10 | Y |  |
| `ovtm_untp_askp_icdc10` | 시간외 단일가 매도호가 증감10 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc1` | 시간외 단일가 매수호가 증감1 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc2` | 시간외 단일가 매수호가 증감2 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc3` | 시간외 단일가 매수호가 증감3 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc4` | 시간외 단일가 매수호가 증감4 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc5` | 시간외 단일가 매수호가 증감5 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc6` | 시간외 단일가 매수호가 증감6 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc7` | 시간외 단일가 매수호가 증감7 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc8` | 시간외 단일가 매수호가 증감8 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc9` | 시간외 단일가 매수호가 증감9 | String | 10 | Y |  |
| `ovtm_untp_bidp_icdc10` | 시간외 단일가 매수호가 증감10 | String | 10 | Y |  |
| `ovtm_untp_askp_rsqn1` | 시간외 단일가 매도호가 잔량1 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn2` | 시간외 단일가 매도호가 잔량2 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn3` | 시간외 단일가 매도호가 잔량3 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn4` | 시간외 단일가 매도호가 잔량4 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn5` | 시간외 단일가 매도호가 잔량5 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn6` | 시간외 단일가 매도호가 잔량6 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn7` | 시간외 단일가 매도호가 잔량7 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn8` | 시간외 단일가 매도호가 잔량8 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn9` | 시간외 단일가 매도호가 잔량9 | String | 12 | Y |  |
| `ovtm_untp_askp_rsqn10` | 시간외 단일가 매도호가 잔량10 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn1` | 시간외 단일가 매수호가 잔량1 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn2` | 시간외 단일가 매수호가 잔량2 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn3` | 시간외 단일가 매수호가 잔량3 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn4` | 시간외 단일가 매수호가 잔량4 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn5` | 시간외 단일가 매수호가 잔량5 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn6` | 시간외 단일가 매수호가 잔량6 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn7` | 시간외 단일가 매수호가 잔량7 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn8` | 시간외 단일가 매수호가 잔량8 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn9` | 시간외 단일가 매수호가 잔량9 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn10` | 시간외 단일가 매수호가 잔량10 | String | 12 | Y |  |
| `ovtm_untp_total_askp_rsqn` | 시간외 단일가 총 매도호가 잔량 | String | 12 | Y |  |
| `ovtm_untp_total_bidp_rsqn` | 시간외 단일가 총 매수호가 잔량 | String | 12 | Y |  |
| `ovtm_untp_total_askp_rsqn_icdc` | 시간외 단일가 총 매도호가 잔량 | String | 10 | Y |  |
| `ovtm_untp_total_bidp_rsqn_icdc` | 시간외 단일가 총 매수호가 잔량 | String | 10 | Y |  |
| `ovtm_untp_ntby_bidp_rsqn` | 시간외 단일가 순매수 호가 잔량 | String | 12 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `total_askp_rsqn_icdc` | 총 매도호가 잔량 증감 | String | 10 | Y |  |
| `total_bidp_rsqn_icdc` | 총 매수호가 잔량 증감 | String | 10 | Y |  |
| `ovtm_total_askp_rsqn` | 시간외 총 매도호가 잔량 | String | 12 | Y |  |
| `ovtm_total_bidp_rsqn` | 시간외 총 매수호가 잔량 | String | 12 | Y |  |
| `ovtm_total_askp_icdc` | 시간외 총 매도호가 증감 | String | 10 | Y |  |
| `ovtm_total_bidp_icdc` | 시간외 총 매수호가 증감 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": {
    "ovtm_untp_last_hour": "161847",
    "ovtm_untp_askp1": "83600",
    "ovtm_untp_askp2": "83700",
    "ovtm_untp_askp3": "83800",
    "ovtm_untp_askp4": "0",
    "ovtm_untp_askp5": "0",
    "ovtm_untp_askp6": "0",
    "ovtm_untp_askp7": "0",
    "ovtm_untp_askp8": "0",
    "ovtm_untp_askp9": "0",
    "ovtm_untp_askp10": "0",
    "ovtm_untp_bidp1": "83500",
    "ovtm_untp_bidp2": "83400",
    "ovtm_untp_bidp3": "83300",
    "ovtm_untp_bidp4": "0",
    "ovtm_untp_bidp5": "0",
    "ovtm_untp_bidp6": "0",
    "ovtm_untp_bidp7": "0",
    "ovtm_untp_bidp8": "0",
    "ovtm_untp_bidp9": "0",
    "ovtm_untp_bidp10": "0",
    "ovtm_untp_askp_icdc1": "0",
    "ovtm_untp_askp_icdc2": "0",
    "ovtm_untp_askp_icdc3": "0",
    "ovtm_untp_bidp_icdc1": "1",
    "ovtm_untp_bidp_icdc2": "0",
    "ovtm_untp_bidp_icdc3": "0",
    "ovtm_untp_askp_rsqn1": "4498",
    "ovtm_untp_askp_rsqn2": "11671",
    "ovtm_untp_askp_rsqn3": "9625",
    "ovtm_untp_askp_rsqn4": "0",
    "ovtm_untp_askp_rsqn5": "0",
    "ovtm_untp_askp_rsqn6": "0",
    "ovtm_untp_askp_rsqn7": "0",
    "ovtm_untp_askp_rsqn8": "0",
    "ovtm_untp_askp_rsqn9": "0",
    "ovtm_untp_askp_rsqn10": "0",
    "ovtm_untp_bidp_rsqn1": "1219",
    "ovtm_untp_bidp_rsqn2": "2242",
    "ovtm_untp_bidp_rsqn3": "5603",
    "ovtm_untp_bidp_rsqn4": "0",
    "ovtm_untp_bidp_rsqn5": "0",
    "ovtm_untp_bidp_rsqn6": "0",
    "ovtm_untp_bidp_rsqn7": "0",
    "ovtm_untp_bidp_rsqn8": "0",
    "ovtm_untp_bidp_rsqn9": "0",
    "ovtm_untp_bidp_rsqn10": "0",
    "ovtm_untp_total_askp_rsqn": "25794",
    "ovtm_untp_total_bidp_rsqn": "9064",
    "ovtm_untp_total_askp_rsqn_icdc": "0",
    "ovtm_untp_total_bidp_rsqn_icdc": "1",
    "ovtm_untp_ntby_bidp_rsqn": "-16730",
    "total_askp_rsqn": "923970",
    "total_bidp_rsqn": "756893",
    "total_askp_rsqn_icdc": "0",
    "total_bidp_rsqn_icdc": "0",
    "ovtm_total_askp_rsqn": "36230",
    "ovtm_total_bidp_rsqn": "0",
    "ovtm_total_askp_icdc": "0",
    "ovtm_total_bidp_icdc": "0"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

