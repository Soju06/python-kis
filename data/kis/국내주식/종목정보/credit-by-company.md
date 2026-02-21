# 국내주식 당사 신용가능종목[국내주식-111]

> [국내주식] 종목정보

국내주식 당사 신용가능종목 API입니다.
한국투자 HTS(eFriend Plus) > [0477] 당사 신용가능 종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 100건 확인 가능하며, 다음 조회가 불가합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `43c17205-d112-4f9f-83f9-1704af8e4f79` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/credit-by-company` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST04770000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15T09:33:22+09:00
- **최종 수정일**: 2025-05-14T13:20:07+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST04770000 |
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
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0:코드순, 1:이름순 |
| `fid_slct_yn` | 선택 여부 | String | 1 | Y | 0:신용주문가능, 1: 신용주문불가 |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100 |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20477) |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20477",
  "fid_input_iscd": "0000",
  "fid_slct_yn": "0",
  "fid_rank_sort_cls_code": "1"
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
| `output` | 응답상세 | Object |   | Y | array |
| `stck_shrn_iscd` | 주식 단축 종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `crdt_rate` | 신용 비율 | String | 84 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_shrn_iscd": "473440",
      "hts_kor_isnm": "ACE 11월만기자동연장회사채AA-이상액티브",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "105190",
      "hts_kor_isnm": "ACE 200",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "332500",
      "hts_kor_isnm": "ACE 200TR",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "448880",
      "hts_kor_isnm": "ACE 24-12 회사채(AA-이상)액티브",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "461270",
      "hts_kor_isnm": "ACE 26-06 회사채(AA-이상)액티브",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "414270",
      "hts_kor_isnm": "ACE G2전기차&자율주행액티브",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "365780",
      "hts_kor_isnm": "ACE 국고채10년",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "446770",
      "hts_kor_isnm": "ACE 글로벌반도체TOP4 Plus SOLACTIVE",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "190620",
      "hts_kor_isnm": "ACE 단기통안채",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "453850",
      "hts_kor_isnm": "ACE 미국30년국채액티브(H)",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "360200",
      "hts_kor_isnm": "ACE 미국S&P500",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "438080",
      "hts_kor_isnm": "ACE 미국S&P500채권혼합액티브",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "309230",
      "hts_kor_isnm": "ACE 미국WideMoat가치주",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "367380",
      "hts_kor_isnm": "ACE 미국나스닥100",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "456880",
      "hts_kor_isnm": "ACE 미국달러SOFR금리(합성)",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "402970",
      "hts_kor_isnm": "ACE 미국배당다우존스",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "465580",
      "hts_kor_isnm": "ACE 미국빅테크TOP7 Plus",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "245710",
      "hts_kor_isnm": "ACE 베트남VN30(합성)",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "448540",
      "hts_kor_isnm": "ACE 엔비디아채권혼합블룸버그",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "238720",
      "hts_kor_isnm": "ACE 일본Nikkei225(H)",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "356540",
      "hts_kor_isnm": "ACE 종합채권(AA-이상)KIS액티브",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "457480",
      "hts_kor_isnm": "ACE 테슬라밸류체인액티브",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "469170",
      "hts_kor_isnm": "ACE 포스코그룹포커스",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "265520",
      "hts_kor_isnm": "AP시스템",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "152100",
      "hts_kor_isnm": "ARIRANG 200",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "453010",
      "hts_kor_isnm": "ARIRANG KOFR금리",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "449450",
      "hts_kor_isnm": "ARIRANG K방산Fn",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "161510",
      "hts_kor_isnm": "ARIRANG 고배당주",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "464470",
      "hts_kor_isnm": "ARIRANG 미국채30년액티브",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "195980",
      "hts_kor_isnm": "ARIRANG 신흥국MSCI(합성 H)",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "421320",
      "hts_kor_isnm": "ARIRANG 우주항공&UAM iSelect",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "328370",
      "hts_kor_isnm": "ARIRANG 코스피TR",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "027410",
      "hts_kor_isnm": "BGF",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "282330",
      "hts_kor_isnm": "BGF리테일",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "126600",
      "hts_kor_isnm": "BGF에코머티리얼즈",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "138930",
      "hts_kor_isnm": "BNK금융지주",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "001040",
      "hts_kor_isnm": "CJ",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "000120",
      "hts_kor_isnm": "CJ대한통운",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "011150",
      "hts_kor_isnm": "CJ씨푸드",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "097950",
      "hts_kor_isnm": "CJ제일제당",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "097955",
      "hts_kor_isnm": "CJ제일제당 우",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "051500",
      "hts_kor_isnm": "CJ프레시웨이",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "058820",
      "hts_kor_isnm": "CMG제약",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "012030",
      "hts_kor_isnm": "DB",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "005830",
      "hts_kor_isnm": "DB손해보험",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "000990",
      "hts_kor_isnm": "DB하이텍",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "139130",
      "hts_kor_isnm": "DGB금융지주",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "001530",
      "hts_kor_isnm": "DI동일",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "375500",
      "hts_kor_isnm": "DL이앤씨",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "068790",
      "hts_kor_isnm": "DMS",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "007340",
      "hts_kor_isnm": "DN오토모티브",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "241520",
      "hts_kor_isnm": "DSC인베스트먼트",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "017940",
      "hts_kor_isnm": "E1",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "007700",
      "hts_kor_isnm": "F&F홀딩스",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "078930",
      "hts_kor_isnm": "GS",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "001250",
      "hts_kor_isnm": "GS글로벌",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "007070",
      "hts_kor_isnm": "GS리테일",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "293180",
      "hts_kor_isnm": "HANARO 200",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "454320",
      "hts_kor_isnm": "HANARO CAPEX설비투자iSelect",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "395290",
      "hts_kor_isnm": "HANARO Fn K-POP&미디어",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "395270",
      "hts_kor_isnm": "HANARO Fn K-반도체",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "441540",
      "hts_kor_isnm": "HANARO Fn조선해운",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "434730",
      "hts_kor_isnm": "HANARO 원자력iSelect",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "078150",
      "hts_kor_isnm": "HB테크놀러지",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "089470",
      "hts_kor_isnm": "HDC현대EP",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "009540",
      "hts_kor_isnm": "HD한국조선해양",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "267250",
      "hts_kor_isnm": "HD현대",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "267270",
      "hts_kor_isnm": "HD현대건설기계",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "322000",
      "hts_kor_isnm": "HD현대에너지솔루션",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "042670",
      "hts_kor_isnm": "HD현대인프라코어",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "329180",
      "hts_kor_isnm": "HD현대중공업",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "195940",
      "hts_kor_isnm": "HK이노엔",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "204320",
      "hts_kor_isnm": "HL만도",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "060980",
      "hts_kor_isnm": "HL홀딩스",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "011200",
      "hts_kor_isnm": "HMM",
      "crdt_rate": "20.00"
    },
    {
      "stck_shrn_iscd": "036640",
      "hts_kor_isnm": "HRS",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "095340",
      "hts_kor_isnm": "ISC",
      "crdt_rate": "60.00"
    },
    {
      "stck_shrn_iscd": "175330",
      "hts_kor_isnm": "JB금융지주",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "234080",
      "hts_kor_isnm": "JW생명과학",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "035900",
      "hts_kor_isnm": "JYP Ent.",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "148020",
      "hts_kor_isnm": "KBSTAR 200",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "448600",
      "hts_kor_isnm": "KBSTAR 25-11 회사채(AA-이상)액티브",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "465330",
      "hts_kor_isnm": "KBSTAR 2차전지TOP10",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "422420",
      "hts_kor_isnm": "KBSTAR 2차전지액티브",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "469070",
      "hts_kor_isnm": "KBSTAR AI&로봇",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "290130",
      "hts_kor_isnm": "KBSTAR ESG사회책임투자",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "367760",
      "hts_kor_isnm": "KBSTAR Fn5G테크",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "367770",
      "hts_kor_isnm": "KBSTAR Fn수소경제테마",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "326240",
      "hts_kor_isnm": "KBSTAR IT플러스",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "385560",
      "hts_kor_isnm": "KBSTAR KIS국고채30년Enhanced",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "401170",
      "hts_kor_isnm": "KBSTAR iSelect메타버스",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "266160",
      "hts_kor_isnm": "KBSTAR 고배당",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "385550",
      "hts_kor_isnm": "KBSTAR 단기종합채권(AA-이상)액티브",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "196230",
      "hts_kor_isnm": "KBSTAR 단기통안채",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "315960",
      "hts_kor_isnm": "KBSTAR 대형고배당10TR",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "455890",
      "hts_kor_isnm": "KBSTAR 머니마켓액티브",
      "crdt_rate": "30.00"
    },
    {
      "stck_shrn_iscd": "379780",
      "hts_kor_isnm": "KBSTAR 미국S&P500",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "453330",
      "hts_kor_isnm": "KBSTAR 미국S&P500(H)",
      "crdt_rate": "50.00"
    },
    {
      "stck_shrn_iscd": "368590",
      "hts_kor_isnm": "KBSTAR 미국나스닥100",
      "crdt_rate": "40.00"
    },
    {
      "stck_shrn_iscd": "437350",
      "hts_kor_isnm": "KBSTAR 미국단기투자등급회사채액티브",
      "crdt_rate": "40.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

