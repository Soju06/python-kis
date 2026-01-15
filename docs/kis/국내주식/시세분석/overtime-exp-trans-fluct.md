# 국내주식 시간외예상체결등락률 [국내주식-140]

> [국내주식] 시세분석

국내주식 시간외예상체결등락률 API입니다. 
한국투자 HTS(eFriend Plus) > [0236] 시간외 예상체결등락률 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fc52daa5-9919-4f80-b926-ee35ef298c54` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/overtime-exp-trans-fluct` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHKST11860000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST11860000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J: 주식) |
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(11186) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 0000(전체), 0001(코스피), 1001(코스닥) |
| `FID_RANK_SORT_CLS_CODE` | 순위 정렬 구분 코드 | String | 2 | Y | 0(상승률), 1(상승폭), 2(보합), 3(하락률), 4(하락폭) |
| `FID_DIV_CLS_CODE` | 분류 구분 코드 | String | 2 | Y | '0(전체), 1(관리종목), 2(투자주의), 3(투자경고),  4(투자위험예고), 5(투자위험), 6(보통주), 7(우선주)' |
| `FID_INPUT_PRICE_1` | 입력 가격1 | String | 12 | Y | 가격 ~ |
| `FID_INPUT_PRICE_2` | 입력 가격2 | String | 12 | Y | 공백 |
| `FID_INPUT_VOL_1` | 입력 거래량 | String | 18 | Y | 거래량 ~ |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_COND_SCR_DIV_CODE:11186
FID_INPUT_ISCD:0000
FID_RANK_SORT_CLS_CODE:0
FID_DIV_CLS_CODE:0
FID_INPUT_PRICE_1:
FID_INPUT_PRICE_2:
FID_INPUT_VOL_1:
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
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `iscd_stat_cls_code` | 종목 상태 구분 코드 | String | 3 | Y |  |
| `stck_shrn_iscd` | 주식 단축 종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `ovtm_untp_antc_cnpr` | 시간외 단일가 예상 체결가 | String | 10 | Y |  |
| `ovtm_untp_antc_cntg_vrss` |  시간외 단일가 예상 체결 대비 | String | 10 | Y |  |
| `ovtm_untp_antc_cntg_vrsssign` | 시간외 단일가 예상 체결 대비 | String | 1 | Y |  |
| `ovtm_untp_antc_cntg_ctrt` | 시간외 단일가 예상 체결 대비율 | String | 82 | Y |  |
| `ovtm_untp_askp_rsqn1` | 시간외 단일가 매도호가 잔량1 | String | 12 | Y |  |
| `ovtm_untp_bidp_rsqn1` | 시간외 단일가 매수호가 잔량1 | String | 12 | Y |  |
| `ovtm_untp_antc_cnqn` | 시간외 단일가 예상 체결량 | String | 18 | Y |  |
| `itmt_vol` | 장중 거래량 | String | 18 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "data_rank": "1",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "025820",
      "hts_kor_isnm": "이구산업",
      "ovtm_untp_antc_cnpr": "6270",
      "ovtm_untp_antc_cntg_vrss": "570",
      "ovtm_untp_antc_cntg_vrss_sign": "1",
      "ovtm_untp_antc_cntg_ctrt": "10.00",
      "ovtm_untp_askp_rsqn1": "231200",
      "ovtm_untp_bidp_rsqn1": "394",
      "ovtm_untp_antc_cnqn": "253267",
      "itmt_vol": "14355442",
      "stck_prpr": "5700"
    },
    {
      "data_rank": "2",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "024840",
      "hts_kor_isnm": "KBI메탈",
      "ovtm_untp_antc_cnpr": "1805",
      "ovtm_untp_antc_cntg_vrss": "164",
      "ovtm_untp_antc_cntg_vrss_sign": "1",
      "ovtm_untp_antc_cntg_ctrt": "9.99",
      "ovtm_untp_askp_rsqn1": "0",
      "ovtm_untp_bidp_rsqn1": "1512765",
      "ovtm_untp_antc_cnqn": "25869",
      "itmt_vol": "13518874",
      "stck_prpr": "1641"
    },
    {
      "data_rank": "3",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "097800",
      "hts_kor_isnm": "윈팩",
      "ovtm_untp_antc_cnpr": "1334",
      "ovtm_untp_antc_cntg_vrss": "121",
      "ovtm_untp_antc_cntg_vrss_sign": "1",
      "ovtm_untp_antc_cntg_ctrt": "9.98",
      "ovtm_untp_askp_rsqn1": "150248",
      "ovtm_untp_bidp_rsqn1": "300",
      "ovtm_untp_antc_cnqn": "40546",
      "itmt_vol": "1020359",
      "stck_prpr": "1213"
    },
    {
      "data_rank": "4",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "060280",
      "hts_kor_isnm": "큐렉소",
      "ovtm_untp_antc_cnpr": "13460",
      "ovtm_untp_antc_cntg_vrss": "1220",
      "ovtm_untp_antc_cntg_vrss_sign": "1",
      "ovtm_untp_antc_cntg_ctrt": "9.97",
      "ovtm_untp_askp_rsqn1": "0",
      "ovtm_untp_bidp_rsqn1": "5409",
      "ovtm_untp_antc_cnqn": "4769",
      "itmt_vol": "233482",
      "stck_prpr": "12240"
    },
    {
      "data_rank": "5",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "206650",
      "hts_kor_isnm": "유바이오로직스",
      "ovtm_untp_antc_cnpr": "13270",
      "ovtm_untp_antc_cntg_vrss": "1200",
      "ovtm_untp_antc_cntg_vrss_sign": "1",
      "ovtm_untp_antc_cntg_ctrt": "9.94",
      "ovtm_untp_askp_rsqn1": "23618",
      "ovtm_untp_bidp_rsqn1": "8",
      "ovtm_untp_antc_cnqn": "20021",
      "itmt_vol": "182132",
      "stck_prpr": "12070"
    },
    {
      "data_rank": "6",
      "iscd_stat_cls_code": "51",
      "stck_shrn_iscd": "008110",
      "hts_kor_isnm": "대동전자",
      "ovtm_untp_antc_cnpr": "7680",
      "ovtm_untp_antc_cntg_vrss": "690",
      "ovtm_untp_antc_cntg_vrss_sign": "1",
      "ovtm_untp_antc_cntg_ctrt": "9.87",
      "ovtm_untp_askp_rsqn1": "0",
      "ovtm_untp_bidp_rsqn1": "16106",
      "ovtm_untp_antc_cnqn": "238",
      "itmt_vol": "3577",
      "stck_prpr": "6990"
    },
    {
      "data_rank": "7",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "058450",
      "hts_kor_isnm": "엔터파트너즈",
      "ovtm_untp_antc_cnpr": "5910",
      "ovtm_untp_antc_cntg_vrss": "510",
      "ovtm_untp_antc_cntg_vrss_sign": "1",
      "ovtm_untp_antc_cntg_ctrt": "9.44",
      "ovtm_untp_askp_rsqn1": "607",
      "ovtm_untp_bidp_rsqn1": "10000",
      "ovtm_untp_antc_cnqn": "20026",
      "itmt_vol": "3168350",
      "stck_prpr": "5400"
    },
    {
      "data_rank": "8",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "336060",
      "hts_kor_isnm": "웨이버스",
      "ovtm_untp_antc_cnpr": "1589",
      "ovtm_untp_antc_cntg_vrss": "129",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "8.84",
      "ovtm_untp_askp_rsqn1": "3539",
      "ovtm_untp_bidp_rsqn1": "2739",
      "ovtm_untp_antc_cnqn": "3970",
      "itmt_vol": "195703",
      "stck_prpr": "1460"
    },
    {
      "data_rank": "9",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "047560",
      "hts_kor_isnm": "이스트소프트",
      "ovtm_untp_antc_cnpr": "26900",
      "ovtm_untp_antc_cntg_vrss": "2000",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "8.03",
      "ovtm_untp_askp_rsqn1": "826",
      "ovtm_untp_bidp_rsqn1": "30",
      "ovtm_untp_antc_cnqn": "9827",
      "itmt_vol": "399313",
      "stck_prpr": "24900"
    },
    {
      "data_rank": "10",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "018470",
      "hts_kor_isnm": "조일알미늄",
      "ovtm_untp_antc_cnpr": "2380",
      "ovtm_untp_antc_cntg_vrss": "155",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "6.97",
      "ovtm_untp_askp_rsqn1": "33239",
      "ovtm_untp_bidp_rsqn1": "8263",
      "ovtm_untp_antc_cnqn": "133388",
      "itmt_vol": "8895974",
      "stck_prpr": "2225"
    },
    {
      "data_rank": "11",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "012800",
      "hts_kor_isnm": "대창",
      "ovtm_untp_antc_cnpr": "1630",
      "ovtm_untp_antc_cntg_vrss": "87",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "5.64",
      "ovtm_untp_askp_rsqn1": "3999",
      "ovtm_untp_bidp_rsqn1": "5309",
      "ovtm_untp_antc_cnqn": "109013",
      "itmt_vol": "9386217",
      "stck_prpr": "1543"
    },
    {
      "data_rank": "12",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "279600",
      "hts_kor_isnm": "미디어젠",
      "ovtm_untp_antc_cnpr": "14300",
      "ovtm_untp_antc_cntg_vrss": "660",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "4.84",
      "ovtm_untp_askp_rsqn1": "1957",
      "ovtm_untp_bidp_rsqn1": "50",
      "ovtm_untp_antc_cnqn": "7",
      "itmt_vol": "8603",
      "stck_prpr": "13640"
    },
    {
      "data_rank": "13",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "102120",
      "hts_kor_isnm": "어보브반도체",
      "ovtm_untp_antc_cnpr": "17220",
      "ovtm_untp_antc_cntg_vrss": "770",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "4.68",
      "ovtm_untp_askp_rsqn1": "126",
      "ovtm_untp_bidp_rsqn1": "38",
      "ovtm_untp_antc_cnqn": "7594",
      "itmt_vol": "1243555",
      "stck_prpr": "16450"
    },
    {
      "data_rank": "14",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "217330",
      "hts_kor_isnm": "싸이토젠",
      "ovtm_untp_antc_cnpr": "13670",
      "ovtm_untp_antc_cntg_vrss": "570",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "4.35",
      "ovtm_untp_askp_rsqn1": "86",
      "ovtm_untp_bidp_rsqn1": "86",
      "ovtm_untp_antc_cnqn": "114",
      "itmt_vol": "41089",
      "stck_prpr": "13100"
    },
    {
      "data_rank": "15",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "204270",
      "hts_kor_isnm": "제이앤티씨",
      "ovtm_untp_antc_cnpr": "20300",
      "ovtm_untp_antc_cntg_vrss": "840",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "4.32",
      "ovtm_untp_askp_rsqn1": "31630",
      "ovtm_untp_bidp_rsqn1": "68",
      "ovtm_untp_antc_cnqn": "17659",
      "itmt_vol": "6038040",
      "stck_prpr": "19460"
    },
    {
      "data_rank": "16",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "049630",
      "hts_kor_isnm": "재영솔루텍",
      "ovtm_untp_antc_cnpr": "717",
      "ovtm_untp_antc_cntg_vrss": "27",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "3.91",
      "ovtm_untp_askp_rsqn1": "5419",
      "ovtm_untp_bidp_rsqn1": "1018",
      "ovtm_untp_antc_cnqn": "581",
      "itmt_vol": "356136",
      "stck_prpr": "690"
    },
    {
      "data_rank": "17",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "011300",
      "hts_kor_isnm": "성안",
      "ovtm_untp_antc_cnpr": "1295",
      "ovtm_untp_antc_cntg_vrss": "39",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "3.11",
      "ovtm_untp_askp_rsqn1": "974",
      "ovtm_untp_bidp_rsqn1": "1126",
      "ovtm_untp_antc_cnqn": "30",
      "itmt_vol": "469466",
      "stck_prpr": "1256"
    },
    {
      "data_rank": "18",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "164060",
      "hts_kor_isnm": "이루다",
      "ovtm_untp_antc_cnpr": "6390",
      "ovtm_untp_antc_cntg_vrss": "190",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "3.06",
      "ovtm_untp_askp_rsqn1": "223",
      "ovtm_untp_bidp_rsqn1": "812",
      "ovtm_untp_antc_cnqn": "146",
      "itmt_vol": "86988",
      "stck_prpr": "6200"
    },
    {
      "data_rank": "19",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "008500",
      "hts_kor_isnm": "일정실업",
      "ovtm_untp_antc_cnpr": "16300",
      "ovtm_untp_antc_cntg_vrss": "460",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.90",
      "ovtm_untp_askp_rsqn1": "11",
      "ovtm_untp_bidp_rsqn1": "825",
      "ovtm_untp_antc_cnqn": "352",
      "itmt_vol": "450888",
      "stck_prpr": "15840"
    },
    {
      "data_rank": "20",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "226330",
      "hts_kor_isnm": "신테카바이오",
      "ovtm_untp_antc_cnpr": "11350",
      "ovtm_untp_antc_cntg_vrss": "310",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.81",
      "ovtm_untp_askp_rsqn1": "116",
      "ovtm_untp_bidp_rsqn1": "100",
      "ovtm_untp_antc_cnqn": "1568",
      "itmt_vol": "150421",
      "stck_prpr": "11040"
    },
    {
      "data_rank": "21",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "313760",
      "hts_kor_isnm": "윌링스",
      "ovtm_untp_antc_cnpr": "6980",
      "ovtm_untp_antc_cntg_vrss": "180",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.65",
      "ovtm_untp_askp_rsqn1": "40",
      "ovtm_untp_bidp_rsqn1": "65",
      "ovtm_untp_antc_cnqn": "8",
      "itmt_vol": "436483",
      "stck_prpr": "6800"
    },
    {
      "data_rank": "22",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "196300",
      "hts_kor_isnm": "애니젠",
      "ovtm_untp_antc_cnpr": "15500",
      "ovtm_untp_antc_cntg_vrss": "370",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.45",
      "ovtm_untp_askp_rsqn1": "21",
      "ovtm_untp_bidp_rsqn1": "20",
      "ovtm_untp_antc_cnqn": "35",
      "itmt_vol": "66884",
      "stck_prpr": "15130"
    },
    {
      "data_rank": "23",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "003160",
      "hts_kor_isnm": "디아이",
      "ovtm_untp_antc_cnpr": "19400",
      "ovtm_untp_antc_cntg_vrss": "460",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.43",
      "ovtm_untp_askp_rsqn1": "129",
      "ovtm_untp_bidp_rsqn1": "36",
      "ovtm_untp_antc_cnqn": "10214",
      "itmt_vol": "12266019",
      "stck_prpr": "18940"
    },
    {
      "data_rank": "24",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "014910",
      "hts_kor_isnm": "성문전자",
      "ovtm_untp_antc_cnpr": "1485",
      "ovtm_untp_antc_cntg_vrss": "33",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.27",
      "ovtm_untp_askp_rsqn1": "200",
      "ovtm_untp_bidp_rsqn1": "33",
      "ovtm_untp_antc_cnqn": "1",
      "itmt_vol": "58133",
      "stck_prpr": "1452"
    },
    {
      "data_rank": "25",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "291650",
      "hts_kor_isnm": "압타머사이언스",
      "ovtm_untp_antc_cnpr": "2655",
      "ovtm_untp_antc_cntg_vrss": "55",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.12",
      "ovtm_untp_askp_rsqn1": "99",
      "ovtm_untp_bidp_rsqn1": "1",
      "ovtm_untp_antc_cnqn": "1",
      "itmt_vol": "184868",
      "stck_prpr": "2600"
    },
    {
      "data_rank": "26",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "017510",
      "hts_kor_isnm": "세명전기",
      "ovtm_untp_antc_cnpr": "3790",
      "ovtm_untp_antc_cntg_vrss": "75",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.02",
      "ovtm_untp_askp_rsqn1": "3652",
      "ovtm_untp_bidp_rsqn1": "20",
      "ovtm_untp_antc_cnqn": "7126",
      "itmt_vol": "15284327",
      "stck_prpr": "3715"
    },
    {
      "data_rank": "27",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "072770",
      "hts_kor_isnm": "율호",
      "ovtm_untp_antc_cnpr": "2530",
      "ovtm_untp_antc_cntg_vrss": "50",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "2.02",
      "ovtm_untp_askp_rsqn1": "135",
      "ovtm_untp_bidp_rsqn1": "14",
      "ovtm_untp_antc_cnqn": "800",
      "itmt_vol": "538402",
      "stck_prpr": "2480"
    },
    {
      "data_rank": "28",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "001780",
      "hts_kor_isnm": "알루코",
      "ovtm_untp_antc_cnpr": "3345",
      "ovtm_untp_antc_cntg_vrss": "65",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "1.98",
      "ovtm_untp_askp_rsqn1": "15679",
      "ovtm_untp_bidp_rsqn1": "567",
      "ovtm_untp_antc_cnqn": "3419",
      "itmt_vol": "1403435",
      "stck_prpr": "3280"
    },
    {
      "data_rank": "29",
      "iscd_stat_cls_code": "55",
      "stck_shrn_iscd": "017370",
      "hts_kor_isnm": "우신시스템",
      "ovtm_untp_antc_cnpr": "8300",
      "ovtm_untp_antc_cntg_vrss": "160",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "1.97",
      "ovtm_untp_askp_rsqn1": "160",
      "ovtm_untp_bidp_rsqn1": "6",
      "ovtm_untp_antc_cnqn": "34",
      "itmt_vol": "59584",
      "stck_prpr": "8140"
    },
    {
      "data_rank": "30",
      "iscd_stat_cls_code": "57",
      "stck_shrn_iscd": "203400",
      "hts_kor_isnm": "에이비온",
      "ovtm_untp_antc_cnpr": "5980",
      "ovtm_untp_antc_cntg_vrss": "110",
      "ovtm_untp_antc_cntg_vrss_sign": "2",
      "ovtm_untp_antc_cntg_ctrt": "1.87",
      "ovtm_untp_askp_rsqn1": "289",
      "ovtm_untp_bidp_rsqn1": "230",
      "ovtm_untp_antc_cnqn": "1",
      "itmt_vol": "128021",
      "stck_prpr": "5870"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
