# 주식현재가 시세2[v1_국내주식-054]

> [국내주식] 기본시세

주식현재가 시세2 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `995f745a-aa8a-491b-85ef-0d4697094b58` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-price-2` |
| **Content-Type** | `` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHPST01010000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-01-26
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01010000 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 000660 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930"
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
| `output` | 응답상세 | String |   | Y |  |
| `rprs_mrkt_kor_name` | 대표 시장 한글 명 | String | 40 | Y |  |
| `new_hgpr_lwpr_cls_code` | 신 고가 저가 구분 코드 | String | 10 | Y | 특정 경우에만 데이터 출력 |
| `mxpr_llam_cls_code` | 상하한가 구분 코드 | String | 10 | Y | 특정 경우에만 데이터 출력 |
| `crdt_able_yn` | 신용 가능 여부 | String | 1 | Y |  |
| `stck_mxpr` | 주식 상한가 | String | 10 | Y |  |
| `elw_pblc_yn` | ELW 발행 여부 | String | 1 | Y |  |
| `prdy_clpr_vrss_oprc_rate` | 전일 종가 대비 시가2 비율 | String | 84 | Y |  |
| `crdt_rate` | 신용 비율 | String | 84 | Y |  |
| `marg_rate` | 증거금 비율 | String | 84 | Y |  |
| `lwpr_vrss_prpr` | 최저가 대비 현재가 | String | 10 | Y |  |
| `lwpr_vrss_prpr_sign` | 최저가 대비 현재가 부호 | String | 1 | Y |  |
| `prdy_clpr_vrss_lwpr_rate` | 전일 종가 대비 최저가 비율 | String | 84 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `hgpr_vrss_prpr` | 최고가 대비 현재가 | String | 10 | Y |  |
| `hgpr_vrss_prpr_sign` | 최고가 대비 현재가 부호 | String | 1 | Y |  |
| `prdy_clpr_vrss_hgpr_rate` | 전일 종가 대비 최고가 비율 | String | 84 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `oprc_vrss_prpr` | 시가2 대비 현재가 | String | 10 | Y |  |
| `oprc_vrss_prpr_sign` | 시가2 대비 현재가 부호 | String | 1 | Y |  |
| `mang_issu_yn` | 관리 종목 여부 | String | 1 | Y |  |
| `divi_app_cls_code` | 동시호가배분처리코드 | String | 2 | Y | 11:매수상한배분 12:매수하한배분 13: 매도상한배분 14:매도하한배분 |
| `short_over_yn` | 단기과열여부 | String | 1 | Y |  |
| `mrkt_warn_cls_code` | 시장경고코드 | String | 2 | Y | 00: 없음 01: 투자주의 02:투자경고 03:투자위험 |
| `invt_caful_yn` | 투자유의여부 | String | 1 | Y |  |
| `stange_runup_yn` | 이상급등여부 | String | 1 | Y |  |
| `ssts_hot_yn` | 공매도과열 여부 | String | 1 | Y |  |
| `low_current_yn` | 저유동성 종목 여부 | String | 1 | Y |  |
| `vi_cls_code` | VI적용구분코드 | String | 1 | Y |  |
| `short_over_cls_code` | 단기과열구분코드 | String | 10 | Y |  |
| `stck_llam` | 주식 하한가 | String | 10 | Y |  |
| `new_lstn_cls_name` | 신규 상장 구분 명 | String | 40 | Y |  |
| `vlnt_deal_cls_name` | 임의 매매 구분 명 | String | 16 | Y |  |
| `flng_cls_name` | 락 구분 이름 | String | 40 | Y | 특정 경우에만 데이터 출력 |
| `revl_issu_reas_name` | 재평가 종목 사유 명 | String | 40 | Y | 특정 경우에만 데이터 출력 |
| `mrkt_warn_cls_name` | 시장 경고 구분 명 | String | 40 | Y | 특정 경우에만 데이터 출력 "투자환기" / "투자경고" |
| `stck_sdpr` | 주식 기준가 | String | 10 | Y |  |
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y |  |
| `stck_prdy_clpr` | 주식 전일 종가 | String | 10 | Y |  |
| `insn_pbnt_yn` | 불성실 공시 여부 | String | 1 | Y |  |
| `fcam_mod_cls_name` | 액면가 변경 구분 명 | String | 10 | Y | 특정 경우에만 데이터 출력 |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vrss_vol_rate` | 전일 대비 거래량 비율 | String | 84 | Y |  |
| `bstp_kor_isnm` | 업종 한글 종목명 | String | 40 | Y | ※ 거래소 정보로 특정 종목은 업종구분이 없어 데이터 미회신 |
| `sltr_yn` | 정리매매 여부 | String | 1 | Y |  |
| `trht_yn` | 거래정지 여부 | String | 1 | Y |  |
| `oprc_rang_cont_yn` | 시가 범위 연장 여부 | String | 1 | Y |  |
| `vlnt_fin_cls_code` | 임의 종료 구분 코드 | String | 1 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": {
    "rprs_mrkt_kor_name": "KOSPI200",
    "insn_pbnt_yn": "N",
    "stck_prpr": "74400",
    "prdy_vrss": "1000",
    "prdy_vrss_sign": "2",
    "prdy_ctrt": "1.36",
    "acml_tr_pbmn": "276161183000",
    "acml_vol": "3733708",
    "prdy_vol": "11160062",
    "prdy_vrss_vol_rate": "33.46",
    "bstp_kor_isnm": "전기.전자",
    "sltr_yn": "N",
    "mang_issu_yn": "N",
    "trht_yn": "N",
    "oprc_rang_cont_yn": "N",
    "vlnt_fin_cls_code": "N",
    "stck_prdy_clpr": "73400",
    "stck_oprc": "73800",
    "prdy_clpr_vrss_oprc_rate": "0.54",
    "oprc_vrss_prpr_sign": "2",
    "oprc_vrss_prpr": "600",
    "stck_hgpr": "74500",
    "prdy_clpr_vrss_hgpr_rate": "1.50",
    "hgpr_vrss_prpr_sign": "5",
    "hgpr_vrss_prpr": "-100",
    "stck_lwpr": "73500",
    "prdy_clpr_vrss_lwpr_rate": "0.14",
    "lwpr_vrss_prpr_sign": "2",
    "lwpr_vrss_prpr": "900",
    "marg_rate": "20.00",
    "crdt_rate": "20.00",
    "crdt_able_yn": "Y",
    "elw_pblc_yn": "Y",
    "stck_mxpr": "95400",
    "stck_llam": "51400",
    "bstp_cls_code": "005930",
    "stck_sdpr": "73400",
    "vlnt_deal_cls_name": " ",
    "new_lstn_cls_name": "        ",
    "divi_app_cls_code": "  ",
    "short_over_cls_code": "          ",
    "vi_cls_code": "N",
    "low_current_yn": "N",
    "ssts_hot_yn": " ",
    "stange_runup_yn": "N",
    "invt_caful_yn": "N",
    "mrkt_warn_cls_code": "00",
    "short_over_yn": "N"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
