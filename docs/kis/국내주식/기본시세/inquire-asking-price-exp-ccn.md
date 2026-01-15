# 주식현재가 호가/예상체결[v1_국내주식-011]

> [국내주식] 기본시세

주식현재가 호가 예상체결 API입니다. 매수 매도 호가를 확인하실 수 있습니다. 실시간 데이터를 원하신다면 웹소켓 API를 활용하세요.

[국내주식-011 v1] 주식현재가 호가 예상체결

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `af3d3794-92c0-4f3b-8041-4ca4ddcda5de` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `FHKST01010200` |
| **TR ID (모의)** | `FHKST01010200` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST01010200 |
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

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "000660"
}
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
| `aspr_acpt_hour` | 호가 접수 시간 | String | 6 | Y |  |
| `askp1` | 매도호가1 | String | 10 | Y |  |
| `askp2` | 매도호가2 | String | 10 | Y |  |
| `askp3` | 매도호가3 | String | 10 | Y |  |
| `askp4` | 매도호가4 | String | 10 | Y |  |
| `askp5` | 매도호가5 | String | 10 | Y |  |
| `askp6` | 매도호가6 | String | 10 | Y |  |
| `askp7` | 매도호가7 | String | 10 | Y |  |
| `askp8` | 매도호가8 | String | 10 | Y |  |
| `askp9` | 매도호가9 | String | 10 | Y |  |
| `askp10` | 매도호가10 | String | 10 | Y |  |
| `bidp1` | 매수호가1 | String | 10 | Y |  |
| `bidp2` | 매수호가2 | String | 10 | Y |  |
| `bidp3` | 매수호가3 | String | 10 | Y |  |
| `bidp4` | 매수호가4 | String | 10 | Y |  |
| `bidp5` | 매수호가5 | String | 10 | Y |  |
| `bidp6` | 매수호가6 | String | 10 | Y |  |
| `bidp7` | 매수호가7 | String | 10 | Y |  |
| `bidp8` | 매수호가8 | String | 10 | Y |  |
| `bidp9` | 매수호가9 | String | 10 | Y |  |
| `bidp10` | 매수호가10 | String | 10 | Y |  |
| `askp_rsqn1` | 매도호가 잔량1 | String | 12 | Y |  |
| `askp_rsqn2` | 매도호가 잔량2 | String | 12 | Y |  |
| `askp_rsqn3` | 매도호가 잔량3 | String | 12 | Y |  |
| `askp_rsqn4` | 매도호가 잔량4 | String | 12 | Y |  |
| `askp_rsqn5` | 매도호가 잔량5 | String | 12 | Y |  |
| `askp_rsqn6` | 매도호가 잔량6 | String | 12 | Y |  |
| `askp_rsqn7` | 매도호가 잔량7 | String | 12 | Y |  |
| `askp_rsqn8` | 매도호가 잔량8 | String | 12 | Y |  |
| `askp_rsqn9` | 매도호가 잔량9 | String | 12 | Y |  |
| `askp_rsqn10` | 매도호가 잔량10 | String | 12 | Y |  |
| `bidp_rsqn1` | 매수호가 잔량1 | String | 12 | Y |  |
| `bidp_rsqn2` | 매수호가 잔량2 | String | 12 | Y |  |
| `bidp_rsqn3` | 매수호가 잔량3 | String | 12 | Y |  |
| `bidp_rsqn4` | 매수호가 잔량4 | String | 12 | Y |  |
| `bidp_rsqn5` | 매수호가 잔량5 | String | 12 | Y |  |
| `bidp_rsqn6` | 매수호가 잔량6 | String | 12 | Y |  |
| `bidp_rsqn7` | 매수호가 잔량7 | String | 12 | Y |  |
| `bidp_rsqn8` | 매수호가 잔량8 | String | 12 | Y |  |
| `bidp_rsqn9` | 매수호가 잔량9 | String | 12 | Y |  |
| `bidp_rsqn10` | 매수호가 잔량10 | String | 12 | Y |  |
| `askp_rsqn_icdc1` | 매도호가 잔량 증감1 | String | 10 | Y |  |
| `askp_rsqn_icdc2` | 매도호가 잔량 증감2 | String | 10 | Y |  |
| `askp_rsqn_icdc3` | 매도호가 잔량 증감3 | String | 10 | Y |  |
| `askp_rsqn_icdc4` | 매도호가 잔량 증감4 | String | 10 | Y |  |
| `askp_rsqn_icdc5` | 매도호가 잔량 증감5 | String | 10 | Y |  |
| `askp_rsqn_icdc6` | 매도호가 잔량 증감6 | String | 10 | Y |  |
| `askp_rsqn_icdc7` | 매도호가 잔량 증감7 | String | 10 | Y |  |
| `askp_rsqn_icdc8` | 매도호가 잔량 증감8 | String | 10 | Y |  |
| `askp_rsqn_icdc9` | 매도호가 잔량 증감9 | String | 10 | Y |  |
| `askp_rsqn_icdc10` | 매도호가 잔량 증감10 | String | 10 | Y |  |
| `bidp_rsqn_icdc1` | 매수호가 잔량 증감1 | String | 10 | Y |  |
| `bidp_rsqn_icdc2` | 매수호가 잔량 증감2 | String | 10 | Y |  |
| `bidp_rsqn_icdc3` | 매수호가 잔량 증감3 | String | 10 | Y |  |
| `bidp_rsqn_icdc4` | 매수호가 잔량 증감4 | String | 10 | Y |  |
| `bidp_rsqn_icdc5` | 매수호가 잔량 증감5 | String | 10 | Y |  |
| `bidp_rsqn_icdc6` | 매수호가 잔량 증감6 | String | 10 | Y |  |
| `bidp_rsqn_icdc7` | 매수호가 잔량 증감7 | String | 10 | Y |  |
| `bidp_rsqn_icdc8` | 매수호가 잔량 증감8 | String | 10 | Y |  |
| `bidp_rsqn_icdc9` | 매수호가 잔량 증감9 | String | 10 | Y |  |
| `bidp_rsqn_icdc10` | 매수호가 잔량 증감10 | String | 10 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `total_askp_rsqn_icdc` | 총 매도호가 잔량 증감 | String | 10 | Y |  |
| `total_bidp_rsqn_icdc` | 총 매수호가 잔량 증감 | String | 10 | Y |  |
| `ovtm_total_askp_icdc` | 시간외 총 매도호가 증감 | String | 10 | Y |  |
| `ovtm_total_bidp_icdc` | 시간외 총 매수호가 증감 | String | 10 | Y |  |
| `ovtm_total_askp_rsqn` | 시간외 총 매도호가 잔량 | String | 12 | Y |  |
| `ovtm_total_bidp_rsqn` | 시간외 총 매수호가 잔량 | String | 12 | Y |  |
| `ntby_aspr_rsqn` | 순매수 호가 잔량 | String | 12 | Y |  |
| `new_mkop_cls_code` | 신 장운영 구분 코드 | String | 2 | Y | ' '00' : 장전 예상체결가와 장마감 동시호가 '49' : 장후 예상체결가  (1) 첫 번째 비트 1 : 장개시전 2 : 장중 3 : 장종료후 4 : 시간외단일가 7 : ... |
| `output2` | 응답상세 | String |   | Y |  |
| `antc_mkop_cls_code` | 예상 장운영 구분 코드 | String | 3 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `stck_sdpr` | 주식 기준가 | String | 10 | Y |  |
| `antc_cnpr` | 예상 체결가 | String | 10 | Y |  |
| `antc_cntg_vrss_sign` | 예상 체결 대비 부호 | String | 1 | Y |  |
| `antc_cntg_vrss` | 예상 체결 대비 | String | 10 | Y |  |
| `antc_cntg_prdy_ctrt` | 예상 체결 전일 대비율 | String | 11 | Y |  |
| `antc_vol` | 예상 거래량 | String | 18 | Y |  |
| `stck_shrn_iscd` | 주식 단축 종목코드 | String | 9 | Y |  |
| `vi_cls_code` | VI적용구분코드 | String | 1 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "aspr_acpt_hour": "160000",
    "askp1": "128000",
    "askp2": "128500",
    "askp3": "129000",
    "askp4": "129500",
    "askp5": "130000",
    "askp6": "130500",
    "askp7": "131000",
    "askp8": "131500",
    "askp9": "132000",
    "askp10": "132500",
    "bidp1": "127500",
    "bidp2": "127000",
    "bidp3": "126500",
    "bidp4": "126000",
    "bidp5": "125500",
    "bidp6": "125000",
    "bidp7": "124500",
    "bidp8": "124000",
    "bidp9": "123500",
    "bidp10": "123000",
    "askp_rsqn1": "69454",
    "askp_rsqn2": "189698",
    "askp_rsqn3": "154732",
    "askp_rsqn4": "85703",
    "askp_rsqn5": "158696",
    "askp_rsqn6": "31395",
    "askp_rsqn7": "50738",
    "askp_rsqn8": "21039",
    "askp_rsqn9": "39424",
    "askp_rsqn10": "29126",
    "bidp_rsqn1": "83147",
    "bidp_rsqn2": "27469",
    "bidp_rsqn3": "25200",
    "bidp_rsqn4": "18544",
    "bidp_rsqn5": "13251",
    "bidp_rsqn6": "15742",
    "bidp_rsqn7": "15070",
    "bidp_rsqn8": "24995",
    "bidp_rsqn9": "11658",
    "bidp_rsqn10": "15773",
    "askp_rsqn_icdc1": "0",
    "askp_rsqn_icdc2": "0",
    "askp_rsqn_icdc3": "0",
    "askp_rsqn_icdc4": "0",
    "askp_rsqn_icdc5": "0",
    "askp_rsqn_icdc6": "0",
    "askp_rsqn_icdc7": "0",
    "askp_rsqn_icdc8": "0",
    "askp_rsqn_icdc9": "0",
    "askp_rsqn_icdc10": "0",
    "bidp_rsqn_icdc1": "0",
    "bidp_rsqn_icdc2": "0",
    "bidp_rsqn_icdc3": "0",
    "bidp_rsqn_icdc4": "0",
    "bidp_rsqn_icdc5": "0",
    "bidp_rsqn_icdc6": "0",
    "bidp_rsqn_icdc7": "0",
    "bidp_rsqn_icdc8": "0",
    "bidp_rsqn_icdc9": "0",
    "bidp_rsqn_icdc10": "0",
    "total_askp_rsqn": "830005",
    "total_bidp_rsqn": "250849",
    "total_askp_rsqn_icdc": "0",
    "total_bidp_rsqn_icdc": "0",
    "ovtm_total_askp_icdc": "0",
    "ovtm_total_bidp_icdc": "0",
    "ovtm_total_askp_rsqn": "2943",
    "ovtm_total_bidp_rsqn": "0",
    "ntby_aspr_rsqn": "-579156",
    "new_mkop_cls_code": "31"
  },
  "output2": {
    "antc_mkop_cls_code": "112",
    "stck_prpr": "128000",
    "stck_oprc": "125500",
    "stck_hgpr": "128500",
    "stck_lwpr": "124500",
    "stck_sdpr": "124500",
    "antc_cnpr": "128000",
    "antc_cntg_vrss_sign": "2",
    "antc_cntg_vrss": "3500",
    "antc_cntg_prdy_ctrt": "2.81",
    "antc_vol": "220006",
    "stck_shrn_iscd": "000660",
    "vi_cls_code": "N"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다!"
}
```

