# 당사 대주가능 종목 [국내주식-195]

> [국내주식] 종목정보

당사 대주가능 종목 API입니다. 
한국투자 HTS(eFriend Plus) > [0490] 당사 대주가능 종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 본 API는 다음조회가 불가합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ca0f8e3e-9f99-4ebd-a81c-c5f8017c4d65` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/lendable-by-company` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `CTSC2702R` |

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
| `tr_id` | 거래ID | String | 13 | Y | CTSC2702R |
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
| `EXCG_DVSN_CD` | 거래소구분코드 | String | 2 | Y | 00(전체), 02(거래소), 03(코스닥) |
| `PDNO` | 상품번호 | String | 12 | Y | 공백 : 전체조회, 종목코드 입력 시 해당종목만 조회 |
| `THCO_STLN_PSBL_YN` | 당사대주가능여부 | String | 1 | Y | Y |
| `INQR_DVSN_1` | 조회구분1 | String | 1 | Y | 0 : 전체조회, 1: 종목코드순 정렬 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 미입력 (다음조회 불가) |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y | 미입력 (다음조회 불가) |

### 요청 예시

```json
EXCG_DVSN_CD:00
PDNO:
THCO_STLN_PSBL_YN:Y
INQR_DVSN_1:0
CTX_AREA_FK200:
CTX_AREA_NK100:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `papr` | 액면가 | String | 19 | Y |  |
| `bfdy_clpr` | 전일종가 | String | 19 | Y | 전일종가 |
| `sbst_prvs` | 대용가 | String | 19 | Y |  |
| `tr_stop_dvsn_name` | 거래정지구분명 | String | 60 | Y |  |
| `psbl_yn_name` | 가능여부명 | String | 60 | Y |  |
| `lmt_qty1` | 한도수량1 | String | 19 | Y |  |
| `use_qty1` | 사용수량1 | String | 19 | Y |  |
| `trad_psbl_qty2` | 매매가능수량2 | String | 19 | Y | 가능수량 |
| `rght_type_cd` | 권리유형코드 | String | 2 | Y |  |
| `bass_dt` | 기준일자 | String | 8 | Y |  |
| `psbl_yn` | 가능여부 | String | 1 | Y |  |
| `output2` | 응답상세 | String |   | Y |  |
| `tot_stup_lmt_qty` | 총설정한도수량 | String | 19 | Y |  |
| `brch_lmt_qty` | 지점한도수량 | String | 19 | Y |  |
| `rqst_psbl_qty` | 신청가능수량 | String | 19 | Y |  |

### 응답 예시

```json
{
    "ctx_area_fk200": "00!^!^Y!^0                                                                                                                                                                                              ",
    "ctx_area_nk100": "                                                                                                    ",
    "output1": [
        {
            "pdno": "130960",
            "prdt_name": "CJ E&M",
            "papr": "5000",
            "bfdy_clpr": "0",
            "sbst_prvs": "0",
            "tr_stop_dvsn_name": "거래정지",
            "psbl_yn_name": "가능",
            "lmt_qty1": "10520",
            "use_qty1": "0",
            "trad_psbl_qty2": "10520",
            "rght_type_cd": "11",
            "bass_dt": "20180629",
            "psbl_yn": "Y"
        },
        {
            "pdno": "110550",
            "prdt_name": "HIT 골드",
            "papr": "0",
            "bfdy_clpr": "0",
            "sbst_prvs": "0",
            "tr_stop_dvsn_name": "거래정지",
            "psbl_yn_name": "가능",
            "lmt_qty1": "0",
            "use_qty1": "0",
            "trad_psbl_qty2": "0",
            "rght_type_cd": "32",
            "bass_dt": "20111222",
            "psbl_yn": "Y"
        },
        {
            "pdno": "124090",
            "prdt_name": "HIT 보험",
            "papr": "0",
            "bfdy_clpr": "0",
            "sbst_prvs": "0",
            "tr_stop_dvsn_name": "거래정지",
            "psbl_yn_name": "가능",
            "lmt_qty1": "0",
            "use_qty1": "0",
            "trad_psbl_qty2": "0",
            "rght_type_cd": "32",
            "bass_dt": "20111219",
            "psbl_yn": "Y"
        },
        {
            "pdno": "002550",
            "prdt_name": "KB손해보험",
            "papr": "500",
            "bfdy_clpr": "0",
            "sbst_prvs": "0",
            "tr_stop_dvsn_name": "거래정지",
            "psbl_yn_name": "가능",
            "lmt_qty1": "0",
            "use_qty1": "0",
            "trad_psbl_qty2": "0",
            "rght_type_cd": "13",
            "bass_dt": "20170706",
            "psbl_yn": "Y"
        },
        {
            "pdno": "021960",
            "prdt_name": "KB캐피탈",
            "papr": "5000",
            "bfdy_clpr": "0",
            "sbst_prvs": "0",
            "tr_stop_dvsn_name": "거래정지",
            "psbl_yn_name": "가능",
            "lmt_qty1": "0",
            "use_qty1": "0",
            "trad_psbl_qty2": "0",
            "rght_type_cd": "13",
            "bass_dt": "20170706",
            "psbl_yn": "Y"
        },
        {
            "pdno": "105270",
            "prdt_name": "KINDEX 성장대형F15",
            "papr": "0",
            "bfdy_clpr": "0",
            "sbst_prvs": "0",
            "tr_stop_dvsn_name": "거래정지",
            "psbl_yn_name": "가능",
            "lmt_qty1": "0",
            "use_qty1": "0",
            "trad_psbl_qty2": "0",
            "rght_type_cd": "32",
            "bass_dt": "20140430",
            "psbl_yn": "Y"
        },...
        {
            "pdno": "003450",
            "prdt_name": "현대증권",
            "papr": "5000",
            "bfdy_clpr": "0",
            "sbst_prvs": "0",
            "tr_stop_dvsn_name": "거래정지",
            "psbl_yn_name": "가능",
            "lmt_qty1": "0",
            "use_qty1": "0",
            "trad_psbl_qty2": "0",
            "rght_type_cd": "13",
            "bass_dt": "20161018",
            "psbl_yn": "Y"
        }
    ],
    "output2": {
        "tot_stup_lmt_qty": "6441070",
        "brch_lmt_qty": "-1228",
        "rqst_psbl_qty": "6442095"
    },
    "rt_cd": "0",
    "msg_cd": "KIOK0460",
    "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
