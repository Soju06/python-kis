# Hashkey

> OAuth인증

해쉬키(Hashkey)는 보안을 위한 요소로 사용자가 보낸 요청 값을 중간에 탈취하여 변조하지 못하도록 하는데 사용됩니다.
해쉬키를 사용하면 POST로 보내는 요청(주로 주문/정정/취소 API 해당)의 body 값을 사전에 암호화시킬 수 있습니다.
해쉬키는 비필수값으로 사용하지 않아도 POST API 호출은 가능합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `214b9e22-8f2e-4fba-9688-587279f1061a` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/hashkey` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | 미지원 |
| **TR ID (모의)** | 미지원 |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-04-11T10:10:35+09:00
- **최종 수정일**: 2023-09-19T08:55:17+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `JsonBody` | 요청값 | String |  | Y | POST로 보낼 body값  ex) datas = {     "CANO": '00000000',     "ACNT_PRDT_CD": "01",     "OVRS_EXCG_CD": "SHAA"  } |

### 요청 예시

```json
{
  "ORD_PRCS_DVSN_CD": "02",
  "CANO": "계좌번호",
  "ACNT_PRDT_CD": "03",
  "SLL_BUY_DVSN_CD": "02",
  "SHTN_PDNO": "101S06",
  "ORD_QTY": "1",
  "UNIT_PRICE": "370",
  "NMPR_TYPE_CD": "",
  "KRX_NMPR_CNDT_CD": "",
  "CTAC_TLNO": "",
  "FUOP_ITEM_DVSN_CD": "",
  "ORD_DVSN_CD": "02"
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `JsonBody` | 요청값 | String |  | Y | 요청한 JsonBody |
| `HASH` | 해쉬키 | String | 256 | Y | [POST API 대상] Client가 요청하는 Request Body를 hashkey api로 생성한 Hash값 * API문서 > hashkey 참조 |

### 응답 예시

```json
{
  "BODY": {
    "ORD_PRCS_DVSN_CD": "02",
    "CANO": "계좌번호",
    "ACNT_PRDT_CD": "03",
    "SLL_BUY_DVSN_CD": "02",
    "SHTN_PDNO": "101S06",
    "ORD_QTY": "1",
    "UNIT_PRICE": "370",
    "NMPR_TYPE_CD": "",
    "KRX_NMPR_CNDT_CD": "",
    "CTAC_TLNO": "",
    "FUOP_ITEM_DVSN_CD": "",
    "ORD_DVSN_CD": "02"
  },
  "HASH": "8b84068222a49302f7ef58226d90403f62e216828f8103465f900de0e7be2f0f"
}
```

