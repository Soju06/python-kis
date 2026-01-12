# 주식현재가 회원사[v1_국내주식-013]

> [국내주식] 기본시세

주식 현재가 회원사 API입니다. 회원사의 투자 정보를 확인할 수 있습니다.

[국내주식-013 v1] 주식현재가 회원사

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `cf3b44a4-1864-4cc3-8650-ba4e2dbcbf06` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-member` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHKST01010600` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자/모의투자] FHKST01010600 : 주식현재가 회원사 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인 P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호 ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "000660"
}
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | Y | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 성공 실패 여부  성공 : 0   실패 : 0외 값 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output` | 응답상세 | String | null | Y |  |
| `seln_mbcr_no1` | 매도 회원사 번호1 | String | 5 | Y |  |
| `seln_mbcr_no2` | 매도 회원사 번호2 | String | 5 | Y |  |
| `seln_mbcr_no3` | 매도 회원사 번호3 | String | 5 | Y |  |
| `seln_mbcr_no4` | 매도 회원사 번호4 | String | 5 | Y |  |
| `seln_mbcr_no5` | 매도 회원사 번호5 | String | 5 | Y |  |
| `seln_mbcr_name1` | 매도 회원사 명1 | String | 40 | Y |  |
| `seln_mbcr_name2` | 매도 회원사 명2 | String | 40 | Y |  |
| `seln_mbcr_name3` | 매도 회원사 명3 | String | 40 | Y |  |
| `seln_mbcr_name4` | 매도 회원사 명4 | String | 40 | Y |  |
| `seln_mbcr_name5` | 매도 회원사 명5 | String | 40 | Y |  |
| `total_seln_qty1` | 총 매도 수량1 | String | 18 | Y |  |
| `total_seln_qty2` | 총 매도 수량2 | String | 18 | Y |  |
| `total_seln_qty3` | 총 매도 수량3 | String | 18 | Y |  |
| `total_seln_qty4` | 총 매도 수량4 | String | 18 | Y |  |
| `total_seln_qty5` | 총 매도 수량5 | String | 18 | Y |  |
| `seln_mbcr_rlim1` | 매도 회원사 비중1 | String | 9 | Y |  |
| `seln_mbcr_rlim2` | 매도 회원사 비중2 | String | 9 | Y |  |
| `seln_mbcr_rlim3` | 매도 회원사 비중3 | String | 9 | Y |  |
| `seln_mbcr_rlim4` | 매도 회원사 비중4 | String | 9 | Y |  |
| `seln_mbcr_rlim5` | 매도 회원사 비중5 | String | 9 | Y |  |
| `seln_qty_icdc1` | 매도 수량 증감1 | String | 10 | Y |  |
| `seln_qty_icdc2` | 매도 수량 증감2 | String | 10 | Y |  |
| `seln_qty_icdc3` | 매도 수량 증감3 | String | 10 | Y |  |
| `seln_qty_icdc4` | 매도 수량 증감4 | String | 10 | Y |  |
| `seln_qty_icdc5` | 매도 수량 증감5 | String | 10 | Y |  |
| `shnu_mbcr_no1` | 매수2 회원사 번호1 | String | 5 | Y |  |
| `shnu_mbcr_no2` | 매수2 회원사 번호2 | String | 5 | Y |  |
| `shnu_mbcr_no3` | 매수2 회원사 번호3 | String | 5 | Y |  |
| `shnu_mbcr_no4` | 매수2 회원사 번호4 | String | 5 | Y |  |
| `shnu_mbcr_no5` | 매수2 회원사 번호5 | String | 5 | Y |  |
| `shnu_mbcr_name1` | 매수2 회원사 명1 | String | 40 | Y |  |
| `shnu_mbcr_name2` | 매수2 회원사 명2 | String | 40 | Y |  |
| `shnu_mbcr_name3` | 매수2 회원사 명3 | String | 40 | Y |  |
| `shnu_mbcr_name4` | 매수2 회원사 명4 | String | 40 | Y |  |
| `shnu_mbcr_name5` | 매수2 회원사 명5 | String | 40 | Y |  |
| `total_shnu_qty1` | 총 매수2 수량1 | String | 18 | Y |  |
| `total_shnu_qty2` | 총 매수2 수량2 | String | 18 | Y |  |
| `total_shnu_qty3` | 총 매수2 수량3 | String | 18 | Y |  |
| `total_shnu_qty4` | 총 매수2 수량4 | String | 18 | Y |  |
| `total_shnu_qty5` | 총 매수2 수량5 | String | 18 | Y |  |
| `shnu_mbcr_rlim1` | 매수2 회원사 비중1 | String | 9 | Y |  |
| `shnu_mbcr_rlim2` | 매수2 회원사 비중2 | String | 9 | Y |  |
| `shnu_mbcr_rlim3` | 매수2 회원사 비중3 | String | 9 | Y |  |
| `shnu_mbcr_rlim4` | 매수2 회원사 비중4 | String | 9 | Y |  |
| `shnu_mbcr_rlim5` | 매수2 회원사 비중5 | String | 9 | Y |  |
| `shnu_qty_icdc1` | 매수2 수량 증감1 | String | 10 | Y |  |
| `shnu_qty_icdc2` | 매수2 수량 증감2 | String | 10 | Y |  |
| `shnu_qty_icdc3` | 매수2 수량 증감3 | String | 10 | Y |  |
| `shnu_qty_icdc4` | 매수2 수량 증감4 | String | 10 | Y |  |
| `shnu_qty_icdc5` | 매수2 수량 증감5 | String | 10 | Y |  |
| `glob_total_seln_qty` | 외국계 총 매도 수량 | String | 18 | Y |  |
| `glob_seln_rlim` | 외국계 매도 비중 | String | 9 | Y |  |
| `glob_ntby_qty` | 외국계 순매수 수량 | String | 12 | Y |  |
| `glob_total_shnu_qty` | 외국계 총 매수2 수량 | String | 18 | Y |  |
| `glob_shnu_rlim` | 외국계 매수2 비중 | String | 9 | Y |  |
| `seln_mbcr_glob_yn_1` | 매도 회원사 외국계 여부1 | String | 1 | Y |  |
| `seln_mbcr_glob_yn_2` | 매도 회원사 외국계 여부2 | String | 1 | Y |  |
| `seln_mbcr_glob_yn_3` | 매도 회원사 외국계 여부3 | String | 1 | Y |  |
| `seln_mbcr_glob_yn_4` | 매도 회원사 외국계 여부4 | String | 1 | Y |  |
| `seln_mbcr_glob_yn_5` | 매도 회원사 외국계 여부5 | String | 1 | Y |  |
| `shnu_mbcr_glob_yn_1` | 매수2 회원사 외국계 여부1 | String | 1 | Y |  |
| `shnu_mbcr_glob_yn_2` | 매수2 회원사 외국계 여부2 | String | 1 | Y |  |
| `shnu_mbcr_glob_yn_3` | 매수2 회원사 외국계 여부3 | String | 1 | Y |  |
| `shnu_mbcr_glob_yn_4` | 매수2 회원사 외국계 여부4 | String | 1 | Y |  |
| `shnu_mbcr_glob_yn_5` | 매수2 회원사 외국계 여부5 | String | 1 | Y |  |
| `glob_total_seln_qty_icdc` | 외국계 총 매도 수량 증감 | String | 10 | Y |  |
| `glob_total_shnu_qty_icdc` | 외국계 총 매수2 수량 증감 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": {
    "seln_mbcr_no1": "00086",
    "seln_mbcr_no2": "00005",
    "seln_mbcr_no3": "00050",
    "seln_mbcr_no4": "00030",
    "seln_mbcr_no5": "00002",
    "seln_mbcr_name1": "BNK증권",
    "seln_mbcr_name2": "미래에셋증권",
    "seln_mbcr_name3": "키움증권",
    "seln_mbcr_name4": "삼성증권",
    "seln_mbcr_name5": "신한투자",
    "total_seln_qty1": "801848",
    "total_seln_qty2": "684589",
    "total_seln_qty3": "310639",
    "total_seln_qty4": "275035",
    "total_seln_qty5": "235001",
    "seln_mbcr_rlim1": "20.52",
    "seln_mbcr_rlim2": "17.52",
    "seln_mbcr_rlim3": "7.95",
    "seln_mbcr_rlim4": "7.04",
    "seln_mbcr_rlim5": "6.01",
    "seln_qty_icdc1": "8000",
    "seln_qty_icdc2": "39472",
    "seln_qty_icdc3": "27755",
    "seln_qty_icdc4": "13612",
    "seln_qty_icdc5": "4047",
    "shnu_mbcr_no1": "00086",
    "shnu_mbcr_no2": "00005",
    "shnu_mbcr_no3": "00033",
    "shnu_mbcr_no4": "00045",
    "shnu_mbcr_no5": "00036",
    "shnu_mbcr_name1": "BNK증권",
    "shnu_mbcr_name2": "미래에셋증권",
    "shnu_mbcr_name3": "JP모간",
    "shnu_mbcr_name4": "골드만",
    "shnu_mbcr_name5": "모간서울",
    "total_shnu_qty1": "822175",
    "total_shnu_qty2": "598966",
    "total_shnu_qty3": "378758",
    "total_shnu_qty4": "354965",
    "total_shnu_qty5": "261357",
    "shnu_mbcr_rlim1": "21.04",
    "shnu_mbcr_rlim2": "15.33",
    "shnu_mbcr_rlim3": "9.69",
    "shnu_mbcr_rlim4": "9.08",
    "shnu_mbcr_rlim5": "6.69",
    "shnu_qty_icdc1": "0",
    "shnu_qty_icdc2": "2397",
    "shnu_qty_icdc3": "20698",
    "shnu_qty_icdc4": "17168",
    "shnu_qty_icdc5": "11893",
    "glob_total_seln_qty": "38125",
    "glob_seln_rlim": "0.98",
    "glob_ntby_qty": "1142513",
    "glob_total_shnu_qty": "1180638",
    "glob_shnu_rlim": "30.21",
    "seln_mbcr_glob_yn_1": "N",
    "seln_mbcr_glob_yn_2": "N",
    "seln_mbcr_glob_yn_3": "N",
    "seln_mbcr_glob_yn_4": "N",
    "seln_mbcr_glob_yn_5": "N",
    "shnu_mbcr_glob_yn_1": "N",
    "shnu_mbcr_glob_yn_2": "N",
    "shnu_mbcr_glob_yn_3": "Y",
    "shnu_mbcr_glob_yn_4": "Y",
    "shnu_mbcr_glob_yn_5": "Y",
    "glob_total_seln_qty_icdc": "0",
    "glob_total_shnu_qty_icdc": "49759"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다!"
}
```
