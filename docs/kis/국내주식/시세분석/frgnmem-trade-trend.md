# 회원사 실시간 매매동향(틱) [국내주식-163]

> [국내주식] 시세분석

회원사 실시간 매매동향(틱) API입니다.
한국투자 HTS(eFriend Plus) > [0432] 회원사 실시간 매매동향 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

최근 100건까지 데이터 조회 가능합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ce9f2a8f-e3cb-4bd3-83ba-7b6034eafae9` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/frgnmem-trade-trend` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHPST04320000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17
- **최종 수정일**: 2025-05-15

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST04320000 |
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
| `FID_COND_SCR_DIV_CODE` | 화면분류코드 | String | 5 | Y | 20432(primary key) |
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | J 고정 입력 |
| `FID_INPUT_ISCD` | 종목코드 | String | 12 | Y | ex. 005930(삼성전자)   ※ FID_INPUT_ISCD(종목코드) 혹은 FID_MRKT_CLS_CODE(시장구분코드) 둘 중 하나만 입력 |
| `FID_INPUT_ISCD_2` | 회원사코드 | String | 10 | Y | ex. 99999(전체)  ※ 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) 참조) |
| `FID_MRKT_CLS_CODE` | 시장구분코드 | String | 2 | Y | A(전체),K(코스피), Q(코스닥), K2(코스피200), W(ELW)  ※ FID_INPUT_ISCD(종목코드) 혹은 FID_MRKT_CLS_CODE(시장구분코드) 둘 중... |
| `FID_VOL_CNT` | 거래량 | String | 12 | Y | 거래량 ~ |

### 요청 예시

```json
FID_COND_SCR_DIV_CODE:20432
FID_INPUT_ISCD:005930
FID_INPUT_ISCD2:99999
FID_MRKT_CLS_CODE:
FID_VOL_CNT:
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
| `output1` | 응답상세 | String |   | Y | array |
| `total_seln_qty` | 총매도수량 | String | 18 | Y |  |
| `total_shnu_qty` | 총매수2수량 | String | 18 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `bsop_hour` | 영업시간 | String | 6 | Y |  |
| `mbcr_name` | 회원사명 | String | 50 | Y |  |
| `hts_kor_isnm` | HTS한글종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `cntg_vol` | 체결거래량 | String | 18 | Y |  |
| `acml_ntby_qty` | 누적순매수수량 | String | 18 | Y |  |
| `glob_ntby_qty` | 외국계순매수수량 | String | 12 | Y |  |
| `frgn_ntby_qty_icdc` | 외국인순매수수량증감 | String | 10 | Y |  |

### 응답 예시

```json
{
    "output1": [
        {
            "total_seln_qty": "3403046",
            "total_shnu_qty": "1539165"
        }
    ],
    "output2": [
        {
            "bsop_hour": "153025",
            "mbcr_name": "JP모간",
            "hts_kor_isnm": "삼성전자",
            "stck_prpr": "75200",
            "prdy_vrss": "-500",
            "prdy_vrss_sign": "5",
            "cntg_vol": "168484",
            "acml_ntby_qty": "1473742",
            "glob_ntby_qty": "-1863881",
            "frgn_ntby_qty_icdc": "168484"
        },
        {
            "bsop_hour": "153025",
            "mbcr_name": "메릴린치",
            "hts_kor_isnm": "삼성전자",
            "stck_prpr": "75200",
            "prdy_vrss": "-500",
            "prdy_vrss_sign": "5",
            "cntg_vol": "-188645",
            "acml_ntby_qty": "-938293",
            "glob_ntby_qty": "-2032365",
            "frgn_ntby_qty_icdc": "-188645"
        },
        {
            "bsop_hour": "153025",
            "mbcr_name": "씨티그룹",
            "hts_kor_isnm": "삼성전자",
            "stck_prpr": "75200",
            "prdy_vrss": "-500",
            "prdy_vrss_sign": "5",
            "cntg_vol": "-135506",
            "acml_ntby_qty": "-2308688",
            "glob_ntby_qty": "-1843720",
            "frgn_ntby_qty_icdc": "-135506"
        },
        {
            "bsop_hour": "152020",
            "mbcr_name": "JP모간",
            "hts_kor_isnm": "삼성전자",
            "stck_prpr": "75500",
            "prdy_vrss": "-200",
            "prdy_vrss_sign": "5",
            "cntg_vol": "139",
            "acml_ntby_qty": "1305258",
            "glob_ntby_qty": "-1708214",
            "frgn_ntby_qty_icdc": "139"
        },
        {
            "bsop_hour": "151904",
            "mbcr_name": "JP모간",
            "hts_kor_isnm": "삼성전자",
            "stck_prpr": "75400",
            "prdy_vrss": "-300",
            "prdy_vrss_sign": "5",
            "cntg_vol": "2271",
            "acml_ntby_qty": "1305119",
            "glob_ntby_qty": "-1708353",
            "frgn_ntby_qty_icdc": "2271"
        },
        {
            "bsop_hour": "151749",
            "mbcr_name": "JP모간",
            "hts_kor_isnm": "삼성전자",
            "stck_prpr": "75300",
            "prdy_vrss": "-400",
            "prdy_vrss_sign": "5",
            "cntg_vol": "23867",
            "acml_ntby_qty": "1302848",
            "glob_ntby_qty": "-1710624",
            "frgn_ntby_qty_icdc": "23867"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
