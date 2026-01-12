# 장내채권 매수주문 [국내주식-124]

> [장내채권] 주문/계좌

장내채권 매수주문 API입니다. 
한국투자 HTS(eFriend Plus) > [0978] 장내채권주문 '채권매수' 탭의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `51c1a249-5fde-412d-9c8f-be5ef2f8dc3b` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/domestic-bond/v1/trading/buy` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `TTTC0952U`, `모의투자 미지원` |

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
| `tr_id` | 거래ID | String | 13 | Y | TTTC0952U |
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
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y |  |
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `ORD_QTY2` | 주문수량2 | String | 19 | Y | SAMT_MKET_PTCI_YN(소액시장참여여부) : N(일반시장) 입력 시 10단위 입력 |
| `BOND_ORD_UNPR` | 채권주문단가 | String | 182 | Y |  |
| `SAMT_MKET_PTCI_YN` | 소액시장참여여부 | String | 1 | Y | N: 일반시장, Y: 소액시장 |
| `BOND_RTL_MKET_YN` | 채권소매시장여부 | String | 1 | Y | Y, N |
| `IDCR_STFNO` | 유치자직원번호 | String | 6 | Y | 공백 |
| `MGCO_APTM_ODNO` | 운용사지정주문번호 | String | 12 | Y | 공백 |
| `ORD_SVR_DVSN_CD` | 주문서버구분코드 | String | 1 | Y | Unique key(0) |
| `CTAC_TLNO` | 연락전화번호 | String | 20 | Y |  |

### 요청 예시

```json
{
  "CANO": "12345678",
  "ACNT_PRDT_CD": "01",
  "PDNO": "KR6095572D81",
  "ORD_QTY2": "1",
  "BOND_ORD_UNPR": "10000",
  "SAMT_MKET_PTCI_YN": "N",
  "BOND_RTL_MKET_YN": "N",
  "IDCR_STFNO": "",
  "MGCO_APTM_ODNO": "",
  "ORD_SVR_DVSN_CD": "0",
  "CTAC_TLNO": ""
}
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | String |   | Y |  |
| `krx_fwdg_ord_orgno` | 한국거래소전송주문조직번호 | String | 5 | Y |  |
| `odno` | 주문번호 | String | 10 | Y |  |
| `ord_tmd` | 주문시각 | String | 6 | Y |  |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "KRX_FWDG_ORD_ORGNO": "01790",
    "ODNO": "0000015401",
    "ORD_TMD": "104258"
  }
}
```
