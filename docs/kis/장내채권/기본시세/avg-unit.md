# 장내채권 평균단가조회 [국내주식-158]

> [장내채권] 기본시세

장내채권 평균단가조회 API입니다. 
한국투자 HTS(eFriend Plus) > [7216] 채권 발행정보 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `aacab59c-7559-414b-bf73-b0d15f3d62f1` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/quotations/avg-unit` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTPF2005R` |

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
| `tr_id` | 거래ID | String | 13 | Y | CTPF2005R |
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
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y | 일자 ~ |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y | ~ 일자 |
| `PDNO` | 상품번호 | String | 12 | Y | 공백: 전체,  특정종목 조회시 : 종목코드 |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | Unique key(302) |
| `VRFC_KIND_CD` | 검증종류코드 | String | 2 | Y | Unique key(00) |
| `CTX_AREA_NK30` | 연속조회키30 | String | 30 | Y | 공백 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y | 공백 |

### 요청 예시

```json
INQR_STRT_DT:20240101
INQR_END_DT:20240425
PDNO:KR2033022D33
PRDT_TYPE_CD:302
VRFC_KIND_CD:00
CTX_AREA_NK30:
CTX_AREA_FK100:
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
| `evlu_dt` | 평가일자 | String | 245 | Y |  |
| `pdno` | 상품번호 | String | 202 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 238 | Y |  |
| `prdt_name` | 상품명 | String | 1 | Y |  |
| `kis_unpr` | 한국신용평가단가 | String | 8 | Y |  |
| `kbp_unpr` | 한국채권평가단가 | String | 500 | Y |  |
| `nice_evlu_unpr` | 한국신용정보평가단가 | String | 238 | Y |  |
| `fnp_unpr` | 에프앤자산평가단가 | String | 202 | Y |  |
| `avg_evlu_unpr` | 평균평가단가 | String | 500 | Y |  |
| `kis_crdt_grad_text` | 한국신용평가신용등급내용 | String | 238 | Y |  |
| `kbp_crdt_grad_text` | 한국채권평가신용등급내용 | String | 202 | Y |  |
| `nice_crdt_grad_text` | 한국신용정보신용등급내용 | String | 238 | Y |  |
| `fnp_crdt_grad_text` | 에프앤자산평가신용등급내용 | String | 500 | Y |  |
| `chng_yn` | 변경여부 | String | 238 | Y |  |
| `kis_erng_rt` | 한국신용평가수익율 | String | 202 | Y |  |
| `kbp_erng_rt` | 한국채권평가수익율 | String | 238 | Y |  |
| `nice_evlu_erng_rt` | 한국신용정보평가수익율 | String | 500 | Y |  |
| `fnp_erng_rt` | 에프앤자산평가수익율 | String | 179 | Y |  |
| `avg_evlu_erng_rt` | 평균평가수익율 | String | 202 | Y |  |
| `kis_rf_unpr` | 한국신용평가RF단가 | String | 238 | Y |  |
| `kbp_rf_unpr` | 한국채권평가RF단가 | String | 12 | Y |  |
| `nice_evlu_rf_unpr` | 한국신용정보평가RF단가 | String | 60 | Y |  |
| `avg_evlu_rf_unpr` | 평균평가RF단가 | String | 3 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `evlu_dt` | 평가일자 | String | 19 | Y |  |
| `pdno` | 상품번호 | String | 1 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 8 | Y |  |
| `prdt_name` | 상품명 | String | 19 | Y |  |
| `kis_evlu_amt` | 한국신용평가평가금액 | String | 19 | Y |  |
| `kbp_evlu_amt` | 한국채권평가평가금액 | String | 19 | Y |  |
| `nice_evlu_amt` | 한국신용정보평가금액 | String | 19 | Y |  |
| `fnp_evlu_amt` | 에프앤자산평가평가금액 | String | 12 | Y |  |
| `avg_evlu_amt` | 평균평가금액 | String | 60 | Y |  |
| `chng_yn` | 변경여부 | String | 3 | Y |  |
| `output3` | 응답상세 | Object |   | Y | array |
| `evlu_dt` | 평가일자 | String | 236 | Y |  |
| `pdno` | 상품번호 | String | 19 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 1 | Y |  |
| `prdt_name` | 상품명 | String | 8 | Y |  |
| `kis_crcy_cd` | 한국신용평가통화코드 | String | 3 | Y |  |
| `kis_evlu_unit_pric` | 한국신용평가평가단위가격 | String | 236 | Y |  |
| `kis_evlu_pric` | 한국신용평가평가가격 | String | 19 | Y |  |
| `kbp_crcy_cd` | 한국채권평가통화코드 | String | 3 | Y |  |
| `kbp_evlu_unit_pric` | 한국채권평가평가단위가격 | String | 236 | Y |  |
| `kbp_evlu_pric` | 한국채권평가평가가격 | String | 19 | Y |  |
| `nice_crcy_cd` | 한국신용정보통화코드 | String | 3 | Y |  |
| `nice_evlu_unit_pric` | 한국신용정보평가단위가격 | String | 236 | Y |  |
| `nice_evlu_pric` | 한국신용정보평가가격 | String | 19 | Y |  |
| `avg_evlu_unit_pric` | 평균평가단위가격 | String | 12 | Y |  |
| `avg_evlu_pric` | 평균평가가격 | String | 60 | Y |  |
| `chng_yn` | 변경여부 | String | 3 | Y |  |

### 응답 예시

```json
{
  "ctx_area_nk30": "20240406!^KR2033022D33!^302   ",
  "ctx_area_fk100": "20240101!^20240425!^KR2033022D33!^302!^00                                                           ",
  "output1": [
    {
      "evlu_dt": "20240425",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9745.69000000",
      "kbp_unpr": "9760.39000000",
      "nice_evlu_unpr": "9767.78000000",
      "fnp_unpr": "9760.76",
      "avg_evlu_unpr": "9758.65000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.87000000",
      "kbp_erng_rt": "3.83000000",
      "nice_evlu_erng_rt": "3.810000000",
      "fnp_erng_rt": "3.82900000",
      "avg_evlu_erng_rt": "3.83480",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240424",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9757.62000000",
      "kbp_unpr": "9771.98000000",
      "nice_evlu_unpr": "9780.14000000",
      "fnp_unpr": "9773.46",
      "avg_evlu_unpr": "9770.80000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.83500000",
      "kbp_erng_rt": "3.79600000",
      "nice_evlu_erng_rt": "3.774000000",
      "fnp_erng_rt": "3.79200000",
      "avg_evlu_erng_rt": "3.79930",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240423",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9764.04000000",
      "kbp_unpr": "9778.42000000",
      "nice_evlu_unpr": "9785.84000000",
      "fnp_unpr": "9779.90",
      "avg_evlu_unpr": "9777.05000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.81500000",
      "kbp_erng_rt": "3.77600000",
      "nice_evlu_erng_rt": "3.756000000",
      "fnp_erng_rt": "3.77200000",
      "avg_evlu_erng_rt": "3.77980",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240422",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9753.79000000",
      "kbp_unpr": "9768.17000000",
      "nice_evlu_unpr": "9777.44000000",
      "fnp_unpr": "9769.65",
      "avg_evlu_unpr": "9767.26000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.84000000",
      "kbp_erng_rt": "3.80100000",
      "nice_evlu_erng_rt": "3.776000000",
      "fnp_erng_rt": "3.79700000",
      "avg_evlu_erng_rt": "3.80350",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240421",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9765.77000000",
      "kbp_unpr": "9780.18000000",
      "nice_evlu_unpr": "9789.47000000",
      "fnp_unpr": "9781.66",
      "avg_evlu_unpr": "9779.27000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.80500000",
      "kbp_erng_rt": "3.76600000",
      "nice_evlu_erng_rt": "3.741000000",
      "fnp_erng_rt": "3.76200000",
      "avg_evlu_erng_rt": "3.76850",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240420",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9764.79000000",
      "kbp_unpr": "9779.20000000",
      "nice_evlu_unpr": "9788.50000000",
      "fnp_unpr": "9780.69",
      "avg_evlu_unpr": "9778.29000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.80500000",
      "kbp_erng_rt": "3.76600000",
      "nice_evlu_erng_rt": "3.741000000",
      "fnp_erng_rt": "3.76200000",
      "avg_evlu_erng_rt": "3.76850",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240419",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9763.81000000",
      "kbp_unpr": "9778.23000000",
      "nice_evlu_unpr": "9787.53000000",
      "fnp_unpr": "9779.72",
      "avg_evlu_unpr": "9777.32000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.80500000",
      "kbp_erng_rt": "3.76600000",
      "nice_evlu_erng_rt": "3.741000000",
      "fnp_erng_rt": "3.76200000",
      "avg_evlu_erng_rt": "3.76850",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240418",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9782.54000000",
      "kbp_unpr": "9793.65000000",
      "nice_evlu_unpr": "9805.22000000",
      "fnp_unpr": "9798.50",
      "avg_evlu_unpr": "9794.97000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.75200000",
      "kbp_erng_rt": "3.72200000",
      "nice_evlu_erng_rt": "3.691000000",
      "fnp_erng_rt": "3.70900000",
      "avg_evlu_erng_rt": "3.71850",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240417",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9770.02000000",
      "kbp_unpr": "9777.77000000",
      "nice_evlu_unpr": "9791.94000000",
      "fnp_unpr": "9784.10",
      "avg_evlu_unpr": "9780.95000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.78300000",
      "kbp_erng_rt": "3.76200000",
      "nice_evlu_erng_rt": "3.724000000",
      "fnp_erng_rt": "3.74500000",
      "avg_evlu_erng_rt": "3.75350",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240416",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9767.18000000",
      "kbp_unpr": "9774.93000000",
      "nice_evlu_unpr": "9788.73000000",
      "fnp_unpr": "9782.02",
      "avg_evlu_unpr": "9778.21000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.78800000",
      "kbp_erng_rt": "3.76700000",
      "nice_evlu_erng_rt": "3.730000000",
      "fnp_erng_rt": "3.74800000",
      "avg_evlu_erng_rt": "3.75830",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240415",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9778.13000000",
      "kbp_unpr": "9787.02000000",
      "nice_evlu_unpr": "9798.98000000",
      "fnp_unpr": "9794.12",
      "avg_evlu_unpr": "9789.56000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.75600000",
      "kbp_erng_rt": "3.73200000",
      "nice_evlu_erng_rt": "3.700000000",
      "fnp_erng_rt": "3.71300000",
      "avg_evlu_erng_rt": "3.72530",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240414",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9795.10000000",
      "kbp_unpr": "9802.13000000",
      "nice_evlu_unpr": "9812.25000000",
      "fnp_unpr": "9808.13",
      "avg_evlu_unpr": "9804.40000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.70800000",
      "kbp_erng_rt": "3.68900000",
      "nice_evlu_erng_rt": "3.662000000",
      "fnp_erng_rt": "3.67300000",
      "avg_evlu_erng_rt": "3.68300",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240413",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9794.13000000",
      "kbp_unpr": "9801.18000000",
      "nice_evlu_unpr": "9811.30000000",
      "fnp_unpr": "9807.17",
      "avg_evlu_unpr": "9803.44000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.70800000",
      "kbp_erng_rt": "3.68900000",
      "nice_evlu_erng_rt": "3.662000000",
      "fnp_erng_rt": "3.67300000",
      "avg_evlu_erng_rt": "3.68300",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240412",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9793.17000000",
      "kbp_unpr": "9800.22000000",
      "nice_evlu_unpr": "9810.35000000",
      "fnp_unpr": "9806.22",
      "avg_evlu_unpr": "9802.49000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.70800000",
      "kbp_erng_rt": "3.68900000",
      "nice_evlu_erng_rt": "3.662000000",
      "fnp_erng_rt": "3.67300000",
      "avg_evlu_erng_rt": "3.68300",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240411",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9764.91000000",
      "kbp_unpr": "9773.80000000",
      "nice_evlu_unpr": "9783.16000000",
      "fnp_unpr": "9778.67",
      "avg_evlu_unpr": "9775.13000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.78100000",
      "kbp_erng_rt": "3.75700000",
      "nice_evlu_erng_rt": "3.732000000",
      "fnp_erng_rt": "3.74400000",
      "avg_evlu_erng_rt": "3.75350",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240410",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9793.13000000",
      "kbp_unpr": "9799.81000000",
      "nice_evlu_unpr": "9809.20000000",
      "fnp_unpr": "9804.69",
      "avg_evlu_unpr": "9801.70000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.70300000",
      "kbp_erng_rt": "3.68500000",
      "nice_evlu_erng_rt": "3.660000000",
      "fnp_erng_rt": "3.67200000",
      "avg_evlu_erng_rt": "3.68000",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240409",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9792.17000000",
      "kbp_unpr": "9798.85000000",
      "nice_evlu_unpr": "9808.25000000",
      "fnp_unpr": "9803.74",
      "avg_evlu_unpr": "9800.75000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.70300000",
      "kbp_erng_rt": "3.68500000",
      "nice_evlu_erng_rt": "3.660000000",
      "fnp_erng_rt": "3.67200000",
      "avg_evlu_erng_rt": "3.68000",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240408",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9796.84000000",
      "kbp_unpr": "9802.41000000",
      "nice_evlu_unpr": "9812.94000000",
      "fnp_unpr": "9806.92",
      "avg_evlu_unpr": "9804.77000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.68800000",
      "kbp_erng_rt": "3.67300000",
      "nice_evlu_erng_rt": "3.645000000",
      "fnp_erng_rt": "3.66100000",
      "avg_evlu_erng_rt": "3.66680",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240407",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9814.71000000",
      "kbp_unpr": "9818.40000000",
      "nice_evlu_unpr": "9830.10000000",
      "fnp_unpr": "9822.93",
      "avg_evlu_unpr": "9821.53000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.63800000",
      "kbp_erng_rt": "3.62800000",
      "nice_evlu_erng_rt": "3.597000000",
      "fnp_erng_rt": "3.61600000",
      "avg_evlu_erng_rt": "3.61980",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    },
    {
      "evlu_dt": "20240406",
      "pdno": "KR2033022D33",
      "prdt_type_cd": "302",
      "prdt_name": "충북지역개발채권23-03",
      "kis_unpr": "9813.76000000",
      "kbp_unpr": "9817.46000000",
      "nice_evlu_unpr": "9829.16000000",
      "fnp_unpr": "9821.99",
      "avg_evlu_unpr": "9820.59000000",
      "kis_crdt_grad_text": "",
      "kbp_crdt_grad_text": "",
      "nice_crdt_grad_text": "",
      "fnp_crdt_grad_text": "",
      "chng_yn": "N",
      "kis_erng_rt": "3.63800000",
      "kbp_erng_rt": "3.62800000",
      "nice_evlu_erng_rt": "3.597000000",
      "fnp_erng_rt": "3.61600000",
      "avg_evlu_erng_rt": "3.61980",
      "kis_rf_unpr": "0.00",
      "kbp_rf_unpr": "0.00",
      "nice_evlu_rf_unpr": "0.00",
      "avg_evlu_rf_unpr": "0.00"
    }
  ],
  "output2": [],
  "output3": [],
  "rt_cd": "0",
  "msg_cd": "KIOK0500",
  "msg1": "조회가 계속됩니다..다음버튼을 Click 하십시오.                                   "
}
```
