# 국내주식 손익계산서[v1_국내주식-079]

> [국내주식] 종목정보

국내주식 손익계산서 API입니다.
한국투자 HTS(eFriend Plus) > [0635] 재무분석종합 화면의 하단 '2. 손익계산서' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `c5933de1-4016-485a-a9ff-729818881d28` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/finance/income-statement` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `` |
| **TR ID** | `FHKST66430200`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-29
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST66430200 |
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
| `FID_DIV_CLS_CODE` | 분류 구분 코드 | String | 2 | Y | 0: 년, 1: 분기  ※ 분기데이터는 연단위 누적합산 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | J |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 000660 : 종목코드 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_div_cls_code": "1"
}
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
| `output` | 응답상세 | Object |   | Y | array |
| `stac_yymm` | 결산 년월 | String | 6 | Y |  |
| `sale_account` | 매출액 | String | 18 | Y |  |
| `sale_cost` | 매출 원가 | String | 182 | Y |  |
| `sale_totl_prfi` | 매출 총 이익 | String | 182 | Y |  |
| `depr_cost` | 감가상각비 | String | 182 | Y | 출력되지 않는 데이터(99.99 로 표시) |
| `sell_mang` | 판매 및 관리비 | String | 182 | Y | 출력되지 않는 데이터(99.99 로 표시) |
| `bsop_prti` | 영업 이익 | String | 182 | Y |  |
| `bsop_non_ernn` | 영업 외 수익 | String | 182 | Y | 출력되지 않는 데이터(99.99 로 표시) |
| `bsop_non_expn` | 영업 외 비용 | String | 182 | Y | 출력되지 않는 데이터(99.99 로 표시) |
| `op_prfi` | 경상 이익 | String | 182 | Y |  |
| `spec_prfi` | 특별 이익 | String | 182 | Y |  |
| `spec_loss` | 특별 손실 | String | 182 | Y |  |
| `thtr_ntin` | 당기순이익 | String | 102 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stac_yymm": "202312",
      "sale_account": "2589355.00",
      "sale_cost": "1803886.00",
      "sale_totl_prfi": "785469",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "65670.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "110063.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "154871.00"
    },
    {
      "stac_yymm": "202309",
      "sale_account": "1911556.00",
      "sale_cost": "1342731.00",
      "sale_totl_prfi": "568825",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "37423.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "74820.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "91423.00"
    },
    {
      "stac_yymm": "202306",
      "sale_account": "1237509.00",
      "sale_cost": "876543.00",
      "sale_totl_prfi": "360966",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "13087.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "35394.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "32982.00"
    },
    {
      "stac_yymm": "202303",
      "sale_account": "637454.00",
      "sale_cost": "460071.00",
      "sale_totl_prfi": "177383",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "6402.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "18264.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "15746.00"
    },
    {
      "stac_yymm": "202212",
      "sale_account": "3022314.00",
      "sale_cost": "1900418.00",
      "sale_totl_prfi": "1121896",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "433766.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "464405.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "556541.00"
    },
    {
      "stac_yymm": "202209",
      "sale_account": "2317668.00",
      "sale_cost": "1414141.00",
      "sale_totl_prfi": "903527",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "390705.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "413856.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "318126.00"
    },
    {
      "stac_yymm": "202206",
      "sale_account": "1549851.00",
      "sale_cost": "933418.00",
      "sale_totl_prfi": "616433",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "282185.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "295306.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "224234.00"
    },
    {
      "stac_yymm": "202203",
      "sale_account": "777815.00",
      "sale_cost": "470721.00",
      "sale_totl_prfi": "307094",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "141214.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "150698.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "113246.00"
    },
    {
      "stac_yymm": "202112",
      "sale_account": "2796048.00",
      "sale_cost": "1664113.00",
      "sale_totl_prfi": "1131935",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "516339.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "533518.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "399075.00"
    },
    {
      "stac_yymm": "202109",
      "sale_account": "2030393.00",
      "sale_cost": "1214648.00",
      "sale_totl_prfi": "815745",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "377671.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "389889.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "290695.00"
    },
    {
      "stac_yymm": "202106",
      "sale_account": "1290601.00",
      "sale_cost": "785659.00",
      "sale_totl_prfi": "504942",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "219496.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "226331.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "167762.00"
    },
    {
      "stac_yymm": "202103",
      "sale_account": "653885.00",
      "sale_cost": "415000.00",
      "sale_totl_prfi": "238885",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "93829.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "97506.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "71417.00"
    },
    {
      "stac_yymm": "202012",
      "sale_account": "2368070.00",
      "sale_cost": "1444883.00",
      "sale_totl_prfi": "923187",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "359939.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "363451.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "264078.00"
    },
    {
      "stac_yymm": "202009",
      "sale_account": "1752555.00",
      "sale_cost": "1066834.00",
      "sale_totl_prfi": "685721",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "269469.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "273707.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "198007.00"
    },
    {
      "stac_yymm": "202006",
      "sale_account": "1082913.00",
      "sale_cost": "667129.00",
      "sale_totl_prfi": "415784",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "145936.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "145265.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "104400.00"
    },
    {
      "stac_yymm": "202003",
      "sale_account": "553252.00",
      "sale_cost": "348067.00",
      "sale_totl_prfi": "205185",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "64473.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "67569.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "48849.00"
    },
    {
      "stac_yymm": "201912",
      "sale_account": "2304009.00",
      "sale_cost": "1472396.00",
      "sale_totl_prfi": "831613",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "277685.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "304322.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "217389.00"
    },
    {
      "stac_yymm": "201909",
      "sale_account": "1705161.00",
      "sale_cost": "1086850.00",
      "sale_totl_prfi": "618311",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "206082.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "227131.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "165118.00"
    },
    {
      "stac_yymm": "201906",
      "sale_account": "1085127.00",
      "sale_cost": "686912.00",
      "sale_totl_prfi": "398215",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "128303.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "140923.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "102242.00"
    },
    {
      "stac_yymm": "201903",
      "sale_account": "523855.00",
      "sale_cost": "327464.00",
      "sale_totl_prfi": "196391",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "62333.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "69130.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "50436.00"
    },
    {
      "stac_yymm": "201812",
      "sale_account": "2437714.00",
      "sale_cost": "1323944.00",
      "sale_totl_prfi": "1113770",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "588867.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "611600.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "443449.00"
    },
    {
      "stac_yymm": "201809",
      "sale_account": "1845064.00",
      "sale_cost": "983785.00",
      "sale_totl_prfi": "861279",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "480861.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "495521.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "358827.00"
    },
    {
      "stac_yymm": "201806",
      "sale_account": "1190464.00",
      "sale_cost": "631841.00",
      "sale_totl_prfi": "558623",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "305112.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "315827.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "227320.00"
    },
    {
      "stac_yymm": "201803",
      "sale_account": "605637.00",
      "sale_cost": "319095.00",
      "sale_totl_prfi": "286542",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "156422.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "161759.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "116885.00"
    },
    {
      "stac_yymm": "201712",
      "sale_account": "2395754.00",
      "sale_cost": "1292907.00",
      "sale_totl_prfi": "1102847",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "536450.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "561960.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "421867.00"
    },
    {
      "stac_yymm": "201709",
      "sale_account": "1735970.00",
      "sale_cost": "935596.00",
      "sale_totl_prfi": "800374",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "384981.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "394916.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "299316.00"
    },
    {
      "stac_yymm": "201706",
      "sale_account": "1115481.00",
      "sale_cost": "605555.00",
      "sale_totl_prfi": "509926",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "239649.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "245768.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "187382.00"
    },
    {
      "stac_yymm": "201703",
      "sale_account": "505475.00",
      "sale_cost": "281556.00",
      "sale_totl_prfi": "223919",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "98984.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "101646.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "76844.00"
    },
    {
      "stac_yymm": "201612",
      "sale_account": "2018667.00",
      "sale_cost": "1202777.00",
      "sale_totl_prfi": "815890",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "292407.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "307137.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "227261.00"
    },
    {
      "stac_yymm": "201609",
      "sale_account": "1485350.00",
      "sale_cost": "893942.00",
      "sale_totl_prfi": "591408",
      "depr_cost": "99.99",
      "sell_mang": "99.99",
      "bsop_prti": "200199.00",
      "bsop_non_ernn": "99.99",
      "bsop_non_expn": "99.99",
      "op_prfi": "211651.00",
      "spec_prfi": "99.99",
      "spec_loss": "99.99",
      "thtr_ntin": "156381.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
