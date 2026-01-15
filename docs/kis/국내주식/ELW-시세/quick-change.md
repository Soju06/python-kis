# ELW 당일급변종목[국내주식-171]

> [국내주식] ELW 시세

ELW 당일급변종목 API입니다. 
한국투자 HTS(eFriend Plus) > [0287] ELW 당일급변종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4769336b-3280-419e-b69d-7531195b2221` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/ranking/quick-change` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPEW02870000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
- **최종 수정일**: 2025-05-07

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02870000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | 시장구분코드 (W) |
| `FID_COND_SCR_DIV_CODE` | 조건화면분류코드 | String | 5 | Y | Unique key(20287) |
| `FID_UNAS_INPUT_ISCD` | 기초자산입력종목코드 | String | 12 | Y | '000000(전체), 2001(코스피200) , 3003(코스닥150), 005930(삼성전자) ' |
| `FID_INPUT_ISCD` | 발행사 | String | 12 | Y | '00000(전체), 00003(한국투자증권) , 00017(KB증권), 00005(미래에셋주식회사)' |
| `FID_MRKT_CLS_CODE` | 시장구분코드 | String | 2 | Y | Unique key(A) |
| `FID_INPUT_PRICE_1` | 가격(이상) | String | 12 | Y |  |
| `FID_INPUT_PRICE_2` | 가격(이하) | String | 12 | Y |  |
| `FID_INPUT_VOL_1` | 거래량(이상) | String | 18 | Y |  |
| `FID_INPUT_VOL_2` | 거래량(이하) | String | 18 | Y |  |
| `FID_HOUR_CLS_CODE` | 시간구분코드 | String | 5 | Y | 1(분), 2(일) |
| `FID_INPUT_HOUR_1` | 입력 일 또는 분 | String | 10 | Y |  |
| `FID_INPUT_HOUR_2` | 기준시간(분 선택 시) | String | 10 | Y |  |
| `FID_RANK_SORT_CLS_CODE` | 순위정렬구분코드 | String | 2 | Y | '1(가격급등), 2(가격급락), 3(거래량급증) , 4(매수잔량급증), 5(매도잔량급증)' |
| `FID_BLNG_CLS_CODE` | 결재방법 | String | 2 | Y | 0(전체), 1(일반), 2(조기종료) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_COND_SCR_DIV_CODE:20287
FID_UNAS_INPUT_ISCD:000000
FID_INPUT_ISCD:00000
FID_MRKT_CLS_CODE:A
FID_INPUT_PRICE_1:
FID_INPUT_PRICE_2:
FID_INPUT_VOL_1:
FID_INPUT_VOL_2:
FID_HOUR_CLS_CODE:2
FID_INPUT_HOUR_1:1
FID_INPUT_HOUR_2:
FID_RANK_SORT_CLS_CODE:1
FID_BLNG_CLS_CODE:0
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
| `output` | 응답상세 | Object |   | Y | array |
| `elw_shrn_iscd` | ELW단축종목코드 | String | 9 | Y |  |
| `elw_kor_isnm` | ELW한글종목명 | String | 40 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `total_askp_rsqn` | 총매도호가잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총매수호가잔량 | String | 12 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `stnd_val` | 기준값 | String | 10 | Y |  |
| `stnd_val_vrss` | 기준값대비 | String | 11 | Y |  |
| `stnd_val_ctrt` | 기준값대비율 | String | 162 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "elw_shrn_iscd": "57JAKW",
            "elw_kor_isnm": "한국JAKWLS일렉콜",
            "elw_prpr": "460",
            "prdy_vrss_sign": "2",
            "prdy_vrss": "350",
            "prdy_ctrt": "318.18",
            "askp": "0",
            "bidp": "145",
            "total_askp_rsqn": "0",
            "total_bidp_rsqn": "49060",
            "acml_vol": "3320",
            "stnd_val": "110",
            "stnd_val_vrss": "350",
            "stnd_val_ctrt": "318.18"
        },
        {
            "elw_shrn_iscd": "58JF27",
            "elw_kor_isnm": "KBJF27KOSPI200콜",
            "elw_prpr": "2395",
            "prdy_vrss_sign": "2",
            "prdy_vrss": "1745",
            "prdy_ctrt": "268.46",
            "askp": "0",
            "bidp": "15",
            "total_askp_rsqn": "0",
            "total_bidp_rsqn": "29000",
            "acml_vol": "100",
            "stnd_val": "650",
            "stnd_val_vrss": "1745",
            "stnd_val_ctrt": "268.46"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

