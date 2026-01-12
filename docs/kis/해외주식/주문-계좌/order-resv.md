# 해외주식 예약주문접수[v1_해외주식-002]

> [해외주식] 주문/계좌

미국거래소 운영시간 외 미국주식을 예약 매매하기 위한 API입니다.

* 해외주식 서비스 신청 후 이용 가능합니다. (아래 링크 3번 해외증권 거래신청 참고)
https://securities.koreainvestment.com/main/bond/research/_static/TF03ca010001.jsp

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

* 아래 각 국가의 시장별 예약주문 접수 가능 시간을 확인하시길 바랍니다.

미국 예약주문 접수시간
1) 10:00 ~ 23:20 / 10:00 ~ 22:20 (서머타임 시)
2) 주문제한 : 16:30 ~ 16:45 경까지 (사유 : 시스템 정산작업시간)
3) 23:30 정규장으로 주문 전송 (서머타임 시 22:30 정규장 주문 전송)
4) 미국 거래소 운영시간(한국시간 기준) : 23:30 ~ 06:00 (썸머타임 적용 시 22:30 ~ 05:00)

홍콩 예약주문 접수시간
1) 09:00 ~ 10:20 접수, 10:30 주문전송
2) 10:40 ~ 13:50 접수, 14:00 주문전송

중국 예약주문 접수시간
1) 09:00 ~ 10:20 접수, 10:30 주문전송
2) 10:40 ~ 13:50 접수, 14:00 주문전송

일본 예약주문 접수시간
1) 09:10 ~ 12:20 까지 접수, 12:30 주문전송

베트남 예약주문 접수시간
1) 09:00 ~ 11:00 까지 접수, 11:15 주문전송
2) 11:20 ~ 14:50 까지 접수, 15:00 주문전송

* 예약주문 유의사항
1) 예약주문 유효기간 : 당일
 - 미국장 마감 후, 미체결주문은 자동취소
 - 미국휴장 시, 익 영업일로 이전
   (미국예약주문화면에서 취소 가능)
2) 증거금 및 잔고보유 : 체크 안함
3) 주문전송 불가사유
 - 매수증거금 부족: 수수료 포함 매수금액부족, 환전, 시세이용료 출금, 인출에 의한 증거금 부족
 - 기타 매수증거금 부족, 매도가능수량 부족, 주권변경 등 권리발생으로 인한 주문불가사유 발생
4) 지정가주문만 가능
* 단 미국 예약매도주문(TTTT3016U)의 경우, MOO(장개시시장가)로 주문 접수 가능

[해외주식-002 v1] 해외주식 예약주문접수

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `55095c42-8c7d-47fc-a34b-947e12481678` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/overseas-stock/v1/trading/order-resv` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `(미국예약매수) VTTT3014U  (미국예약매도) VTTT3016U   (중국/홍콩/일본/베트남 예약주문) VTTS3013U`, `(미국예약매수) TTTT3014U  (미국예약매도) TTTT3016U   (중국/홍콩/일본/베트남 예약주문) TTTS3013U` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTT3016U : 미국 매도 예약 주문 TTTT3014U : 미국 매수 예약 주문 TTTS3013U : 중국/홍콩/일본/베트남 예약 매수/매도/취소 주문  [... |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인 P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호 ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | N | tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 01 : 매도 02 : 매수 |
| `RVSE_CNCL_DVSN_CD` | 정정취소구분코드 | String | 2 | Y | tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 00 : "매도/매수 주문"시 필수 항목 02 : 취소 |
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 515 : 일본 501 : 홍콩 / 543 : 홍콩CNY / 558 : 홍콩USD 507 : ... |
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | NASD : 나스닥 NYSE : 뉴욕 AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE :... |
| `FT_ORD_QTY` | FT주문수량 | String | 10 | Y |  |
| `FT_ORD_UNPR3` | FT주문단가3 | String | 27 | Y |  |
| `ORD_SVR_DVSN_CD` | 주문서버구분코드 | String | 1 | N | "0"(Default) |
| `RSVN_ORD_RCIT_DT` | 예약주문접수일자 | String | 8 | N | tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 |
| `ORD_DVSN` | 주문구분 | String | 20 | N | tr_id가 TTTT3014U(미국 예약 매수 주문)인 경우만 사용 00 : 지정가 35 : TWAP 36 : VWAP  tr_id가 TTTT3016U(미국 예약 매도 주문)... |
| `OVRS_RSVN_ODNO` | 해외예약주문번호 | String | 10 | N | tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용 |
| `ALGO_ORD_TMD_DVSN_CD` | 알고리즘주문시간구분코드 | String | 2 | N | ※ TWAP, VWAP 주문에서만 사용. 예약주문은 시간입력 불가하여 02로 값 고정 ※ 정규장 종료 10분전까지 가능 |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "AAPL",
  "PDNO": "AAPL",
  "OVRS_EXCG_CD": "NASD",
  "FT_ORD_QTY": "1",
  "FT_ORD_UNPR3": "148.00"
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
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공  0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output` | 응답상세 | String |  | Y |  |
| `ODNO` | 한국거래소전송주문조직번호 | String | 10 | Y | tr_id가 TTTT3016U(미국 예약 매도 주문) / TTTT3014U(미국 예약 매수 주문)인 경우만 출력 |
| `RSVN_ORD_RCIT_DT` | 예약주문접수일자 | String | 8 | Y | tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력 |
| `OVRS_RSVN_ODNO` | 해외예약주문번호 | String | 10 | Y | tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력 |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0013",
  "msg1": "주문 전송 완료 되었습니다.",
  "output": {
    "ODNO": "0030138295"
  }
}
```
