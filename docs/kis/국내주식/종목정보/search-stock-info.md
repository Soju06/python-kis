# 주식기본조회[v1_국내주식-067]

> [국내주식] 종목정보

주식기본조회 API입니다.
국내주식 종목의 종목상세정보를 확인할 수 있습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `da0485b5-31f1-4c62-a3d4-294a4311ad39` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/search-stock-info` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTPF1002R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-16
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
| `tr_id` | 거래ID | String | 13 | Y | CTPF1002R |
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
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | 300: 주식, ETF, ETN, ELW  301 : 선물옵션  302 : 채권  306 : ELS' |
| `PDNO` | 상품번호 | String | 12 | Y | 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001) |

### 요청 예시

```json
{
  "PDNO": "000660",
  "PRDT_TYPE_CD": "300"
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
| `output` | 응답상세1 | String |   | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `mket_id_cd` | 시장ID코드 | String | 3 | Y | AGR.농축산물파생 BON.채권파생 CMD.일반상품시장 CUR.통화파생 ENG.에너지파생 EQU.주식파생 ETF.ETF파생 IRT.금리파생 KNX.코넥스 KSQ.코스닥 MTL... |
| `scty_grp_id_cd` | 증권그룹ID코드 | String | 2 | Y | BC.수익증권 DR.주식예탁증서 EF.ETF EN.ETN EW.ELW FE.해외ETF FO.선물옵션 FS.외국주권 FU.선물 FX.플렉스 선물 GD.금현물 IC.투자계약증권 ... |
| `excg_dvsn_cd` | 거래소구분코드 | String | 2 | Y | 01.한국증권 02.증권거래소 03.코스닥 04.K-OTC 05.선물거래소 06.CME 07.EUREX 21.금현물 50.미국주간 51.홍콩 52.상해B 53.심천 54.홍콩... |
| `setl_mmdd` | 결산월일 | String | 4 | Y |  |
| `lstg_stqt` | 상장주수 | String | 19 | Y |  |
| `lstg_cptl_amt` | 상장자본금액 | String | 19 | Y |  |
| `cpta` | 자본금 | String | 19 | Y |  |
| `papr` | 액면가 | String | 19 | Y |  |
| `issu_pric` | 발행가격 | String | 19 | Y |  |
| `kospi200_item_yn` | 코스피200종목여부 | String | 1 | Y |  |
| `scts_mket_lstg_dt` | 유가증권시장상장일자 | String | 8 | Y |  |
| `scts_mket_lstg_abol_dt` | 유가증권시장상장폐지일자 | String | 8 | Y |  |
| `kosdaq_mket_lstg_dt` | 코스닥시장상장일자 | String | 8 | Y |  |
| `kosdaq_mket_lstg_abol_dt` | 코스닥시장상장폐지일자 | String | 8 | Y |  |
| `frbd_mket_lstg_dt` | 프리보드시장상장일자 | String | 8 | Y |  |
| `frbd_mket_lstg_abol_dt` | 프리보드시장상장폐지일자 | String | 8 | Y |  |
| `reits_kind_cd` | 리츠종류코드 | String | 1 | Y |  |
| `etf_dvsn_cd` | ETF구분코드 | String | 2 | Y |  |
| `oilf_fund_yn` | 유전펀드여부 | String | 1 | Y |  |
| `idx_bztp_lcls_cd` | 지수업종대분류코드 | String | 3 | Y |  |
| `idx_bztp_mcls_cd` | 지수업종중분류코드 | String | 3 | Y |  |
| `idx_bztp_scls_cd` | 지수업종소분류코드 | String | 3 | Y |  |
| `stck_kind_cd` | 주식종류코드 | String | 3 | Y | 000.해당사항없음 101.보통주 201.우선주 202.2우선주 203.3우선주 204.4우선주 205.5우선주 206.6우선주 207.7우선주 208.8우선주 209.9우선... |
| `mfnd_opng_dt` | 뮤추얼펀드개시일자 | String | 8 | Y |  |
| `mfnd_end_dt` | 뮤추얼펀드종료일자 | String | 8 | Y |  |
| `dpsi_erlm_cncl_dt` | 예탁등록취소일자 | String | 8 | Y |  |
| `etf_cu_qty` | ETFCU수량 | String | 10 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `prdt_name120` | 상품명120 | String | 120 | Y |  |
| `prdt_abrv_name` | 상품약어명 | String | 60 | Y |  |
| `std_pdno` | 표준상품번호 | String | 12 | Y |  |
| `prdt_eng_name` | 상품영문명 | String | 60 | Y |  |
| `prdt_eng_name120` | 상품영문명120 | String | 120 | Y |  |
| `prdt_eng_abrv_name` | 상품영문약어명 | String | 60 | Y |  |
| `dpsi_aptm_erlm_yn` | 예탁지정등록여부 | String | 1 | Y |  |
| `etf_txtn_type_cd` | ETF과세유형코드 | String | 2 | Y |  |
| `etf_type_cd` | ETF유형코드 | String | 2 | Y |  |
| `lstg_abol_dt` | 상장폐지일자 | String | 8 | Y |  |
| `nwst_odst_dvsn_cd` | 신주구주구분코드 | String | 2 | Y |  |
| `sbst_pric` | 대용가격 | String | 19 | Y |  |
| `thco_sbst_pric` | 당사대용가격 | String | 19 | Y |  |
| `thco_sbst_pric_chng_dt` | 당사대용가격변경일자 | String | 8 | Y |  |
| `tr_stop_yn` | 거래정지여부 | String | 1 | Y |  |
| `admn_item_yn` | 관리종목여부 | String | 1 | Y |  |
| `thdt_clpr` | 당일종가 | String | 19 | Y |  |
| `bfdy_clpr` | 전일종가 | String | 19 | Y |  |
| `clpr_chng_dt` | 종가변경일자 | String | 8 | Y |  |
| `std_idst_clsf_cd` | 표준산업분류코드 | String | 6 | Y |  |
| `std_idst_clsf_cd_name` | 표준산업분류코드명 | String | 130 | Y | 표준산업소분류코드 000000	해당사항없음                                      010101	작물 재배업                       ... |
| `idx_bztp_lcls_cd_name` | 지수업종대분류코드명 | String | 60 | Y | 표준산업대분류코드 00	해당사항없음                                                             01	농업, 임업 및 어업   ... |
| `idx_bztp_mcls_cd_name` | 지수업종중분류코드명 | String | 60 | Y | 표준산업중분류코드                                                    0000	해당사항없음                         ... |
| `idx_bztp_scls_cd_name` | 지수업종소분류코드명 | String | 60 | Y | 표준산업소분류코드 참조 |
| `ocr_no` | OCR번호 | String | 4 | Y |  |
| `crfd_item_yn` | 크라우드펀딩종목여부 | String | 1 | Y |  |
| `elec_scty_yn` | 전자증권여부 | String | 1 | Y |  |
| `issu_istt_cd` | 발행기관코드 | String | 5 | Y |  |
| `etf_chas_erng_rt_dbnb` | ETF추적수익율배수 | String | 19 | Y |  |
| `etf_etn_ivst_heed_item_yn` | ETFETN투자유의종목여부 | String | 1 | Y |  |
| `stln_int_rt_dvsn_cd` | 대주이자율구분코드 | String | 2 | Y |  |
| `frnr_psnl_lmt_rt` | 외국인개인한도비율 | String | 24 | Y |  |
| `lstg_rqsr_issu_istt_cd` | 상장신청인발행기관코드 | String | 5 | Y |  |
| `lstg_rqsr_item_cd` | 상장신청인종목코드 | String | 12 | Y |  |
| `trst_istt_issu_istt_cd` | 신탁기관발행기관코드 | String | 5 | Y |  |
| `cptt_trad_tr_psbl_yn` | NXT 거래종목여부 | String | 1 | Y | NXT 거래가능한 종목은 Y, 그 외 종목은 N |
| `nxt_tr_stop_yn` | NXT 거래정지여부 | String | 1 | Y | NXT 거래종목 중 거래정지가 된 종목은 Y, 그 외 모든 종목은 N |

### 응답 예시

```json
{
  "output": {
    "pdno": "00000A000660",
    "prdt_type_cd": "300",
    "mket_id_cd": "STK",
    "scty_grp_id_cd": "ST",
    "excg_dvsn_cd": "02",
    "setl_mmdd": "12",
    "lstg_stqt": "728002365",
    "lstg_cptl_amt": "0",
    "cpta": "3657652050000",
    "papr": "5000",
    "issu_pric": "5000",
    "kospi200_item_yn": "Y",
    "scts_mket_lstg_dt": "19961226",
    "scts_mket_lstg_abol_dt": "",
    "kosdaq_mket_lstg_dt": "",
    "kosdaq_mket_lstg_abol_dt": "",
    "frbd_mket_lstg_dt": "19961226",
    "frbd_mket_lstg_abol_dt": "",
    "reits_kind_cd": "",
    "etf_dvsn_cd": "0",
    "oilf_fund_yn": "N",
    "idx_bztp_lcls_cd": "002",
    "idx_bztp_mcls_cd": "013",
    "idx_bztp_scls_cd": "013",
    "stck_kind_cd": "101",
    "mfnd_opng_dt": "",
    "mfnd_end_dt": "",
    "dpsi_erlm_cncl_dt": "",
    "etf_cu_qty": "0",
    "prdt_name": "에스케이하이닉스보통주",
    "prdt_name120": "에스케이하이닉스보통주",
    "prdt_abrv_name": "SK하이닉스",
    "std_pdno": "KR7000660001",
    "prdt_eng_name": "SK hynix",
    "prdt_eng_name120": "SK hynix",
    "prdt_eng_abrv_name": "SK hynix",
    "dpsi_aptm_erlm_yn": "Y",
    "etf_txtn_type_cd": "00",
    "etf_type_cd": "",
    "lstg_abol_dt": "",
    "nwst_odst_dvsn_cd": "1",
    "sbst_pric": "115980",
    "thco_sbst_pric": "115980",
    "thco_sbst_pric_chng_dt": "20240215",
    "tr_stop_yn": "N",
    "admn_item_yn": "N",
    "thdt_clpr": "146800",
    "bfdy_clpr": "148700",
    "clpr_chng_dt": "20240216",
    "std_idst_clsf_cd": "032601",
    "std_idst_clsf_cd_name": "반도체 제조업",
    "idx_bztp_lcls_cd_name": "시가총액규모대",
    "idx_bztp_mcls_cd_name": "전기,전자",
    "idx_bztp_scls_cd_name": "전기,전자",
    "ocr_no": "1147",
    "crfd_item_yn": "N",
    "elec_scty_yn": "Y"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0530",
  "msg1": "조회되었습니다                                                                  "
}
```
