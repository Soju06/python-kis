# 국내주식 시간외현재가[국내주식-076]

> [국내주식] 기본시세

국내주식 시간외현재가 API입니다. 
한국투자 HTS(eFriend Plus) > [0230] 시간외 현재가 화면의 좌측 상단기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1e375270-7d8d-4e4b-bcac-d11cb41542cb` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-overtime-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST02300000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05T10:46:37+09:00
- **최종 수정일**: 2025-04-30T10:16:47+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST02300000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 |

### 요청 예시

```json
fid_cond_mrkt_div_code:J
fid_input_iscd:005930
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
| `output` | 응답상세 | String |   | Y |  |
| `bstp_kor_isnm` | 업종 한글 종목명 | String | 40 | Y | ※ 거래소 정보로 특정 종목은 업종구분이 없어 데이터 미회신 |
| `mang_issu_cls_name` | 관리 종목 구분 명 | String | 40 | Y |  |
| `ovtm_untp_prpr` | 시간외 단일가 현재가 | String | 10 | Y |  |
| `ovtm_untp_prdy_vrss` | 시간외 단일가 전일 대비 | String | 10 | Y |  |
| `ovtm_untp_prdy_vrss_sign` | 시간외 단일가 전일 대비 부호 | String | 1 | Y |  |
| `ovtm_untp_prdy_ctrt` | 시간외 단일가 전일 대비율 | String | 82 | Y |  |
| `ovtm_untp_vol` | 시간외 단일가 거래량 | String | 18 | Y |  |
| `ovtm_untp_tr_pbmn` | 시간외 단일가 거래 대금 | String | 18 | Y |  |
| `ovtm_untp_mxpr` | 시간외 단일가 상한가 | String | 18 | Y |  |
| `ovtm_untp_llam` | 시간외 단일가 하한가 | String | 18 | Y |  |
| `ovtm_untp_oprc` | 시간외 단일가 시가2 | String | 10 | Y |  |
| `ovtm_untp_hgpr` | 시간외 단일가 최고가 | String | 10 | Y |  |
| `ovtm_untp_lwpr` | 시간외 단일가 최저가 | String | 10 | Y |  |
| `marg_rate` | 증거금 비율 | String | 84 | Y |  |
| `ovtm_untp_antc_cnpr` | 시간외 단일가 예상 체결가 | String | 10 | Y |  |
| `ovtm_untp_antc_cntg_vrss` | 시간외 단일가 예상 체결 대비 | String | 10 | Y |  |
| `ovtm_untp_antc_cntg_vrss_sign` | 시간외 단일가 예상 체결 대비 | String | 1 | Y |  |
| `ovtm_untp_antc_cntg_ctrt` | 시간외 단일가 예상 체결 대비율 | String | 82 | Y |  |
| `ovtm_untp_antc_cnqn` | 시간외 단일가 예상 체결량 | String | 18 | Y |  |
| `crdt_able_yn` | 신용 가능 여부 | String | 1 | Y |  |
| `new_lstn_cls_name` | 신규 상장 구분 명 | String | 40 | Y |  |
| `sltr_yn` | 정리매매 여부 | String | 1 | Y |  |
| `mang_issu_yn` | 관리 종목 여부 | String | 1 | Y |  |
| `mrkt_warn_cls_code` | 시장 경고 구분 코드 | String | 2 | Y |  |
| `trht_yn` | 거래정지 여부 | String | 1 | Y |  |
| `vlnt_deal_cls_name` | 임의 매매 구분 명 | String | 16 | Y |  |
| `ovtm_untp_sdpr` | 시간외 단일가 기준가 | String | 10 | Y |  |
| `mrkt_warn_cls_name` | 시장 경구 구분 명 | String | 40 | Y |  |
| `revl_issu_reas_name` | 재평가 종목 사유 명 | String | 40 | Y |  |
| `insn_pbnt_yn` | 불성실 공시 여부 | String | 1 | Y |  |
| `flng_cls_name` | 락 구분 이름 | String | 40 | Y |  |
| `rprs_mrkt_kor_name` | 대표 시장 한글 명 | String | 40 | Y |  |
| `ovtm_vi_cls_code` | 시간외단일가VI적용구분코드 | String | 1 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": {
    "bstp_kor_isnm": "전기.전자",
    "ovtm_untp_prpr": "83600",
    "ovtm_untp_prdy_vrss": "-100",
    "ovtm_untp_prdy_vrss_sign": "5",
    "ovtm_untp_prdy_ctrt": "-0.12",
    "ovtm_untp_vol": "3500",
    "ovtm_untp_tr_pbmn": "292600000",
    "ovtm_untp_mxpr": "92000",
    "ovtm_untp_llam": "75400",
    "ovtm_untp_oprc": "83600",
    "ovtm_untp_hgpr": "83600",
    "ovtm_untp_lwpr": "83600",
    "marg_rate": "20.00",
    "ovtm_untp_antc_cnpr": "83500",
    "ovtm_untp_antc_cntg_vrss": "-200",
    "ovtm_untp_antc_cntg_vrss_sign": "5",
    "ovtm_untp_antc_cntg_ctrt": "-0.24",
    "ovtm_untp_antc_cnqn": "4442",
    "crdt_able_yn": "Y",
    "new_lstn_cls_name": "        ",
    "sltr_yn": "N",
    "mang_issu_yn": "N",
    "mrkt_warn_cls_code": "00",
    "trht_yn": "N",
    "vlnt_deal_cls_name": " ",
    "ovtm_untp_sdpr": "83700",
    "insn_pbnt_yn": "N",
    "rprs_mrkt_kor_name": "KOSPI200",
    "ovtm_vi_cls_code": "N",
    "bidp": "83600",
    "askp": "83700"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

