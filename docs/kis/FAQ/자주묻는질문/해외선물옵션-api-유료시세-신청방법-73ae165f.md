<!-- generated: kis-docs-fetch -->
# 해외선물옵션 API 유료시세 신청방법(CME, SGX 거래소)

- 출처: [https://apiportal.koreainvestment.com/community/10000000-0000-0011-0000-000000000002/post/73ae165f-7554-43a0-8615-e77460d61c4a](https://apiportal.koreainvestment.com/community/10000000-0000-0011-0000-000000000002/post/73ae165f-7554-43a0-8615-e77460d61c4a)
- 작성일: `2024-05-28T04:31:36.000+0000`

## 내용

해외선물옵션 API 유료시세(CME, SGX 거래소) 신청방법 안내드립니다.

1. (HTS) eFriend Force 다운로드

한국투자증권 홈페이지 > [HTS/MTS 다운로드](https://securities.koreainvestment.com/main/customer/systemdown/_static/TF04ea000000.jsp) 접속

![](https://apiportal.koreainvestment.com/files/download/public/image/f0ce1767-b08d-4b46-9187-f00ff4359296)

2. eFriend Force [7936] 해외선물옵션 실시간 시세신청/조회 접속 > 상단 우측의 "유의사항" 확인

![](https://apiportal.koreainvestment.com/files/download/public/image/cacf6f3c-c3d1-4997-b06f-564dce4c0433)

3.  우측 상단의 'HTS+MTS(무료)' 조회 후 CME 거래소 4개 항목 및 SGX 거래소 1개 항목 클릭 후 '신청하기' 클릭

![](https://apiportal.koreainvestment.com/files/download/public/image/e8832524-ec2c-46fb-90fb-6657168fd817)

4. 우측 상단의 'API(유료)' 조회 후 CME 거래소 4개 항목 및 SGX 거래소 1개 항목 클릭 후 '신청하기' 클릭

![](https://apiportal.koreainvestment.com/files/download/public/image/96342615-02b4-4adb-ac2a-3a3d0dcc149e)

5. 공동인증서 로그인 후 신청 완료 확인

→ API 신청정보(appkey, appsecret)을 이용하여 접근토큰발급 후 유료시세 정상 조회되는지 확인

6. 접근토큰발급 API(/oauth2/tokenP)를 호출하여 해외선물 유료시세 신청정보 동기화

유료시세 서비스 가입 후 반드시 "접근토큰발급 API"를 호출하여 해외선물 유료시세 신청정보를 동기화해주셔야 합니다.

**"접근토큰발급 API 호출 후" 최대 2시간 이후**실시간 유료 시세 수신이 가능합니다

▶ HTS/MTS 다운로드 링크 : https://securities.koreainvestment.com/main/customer/systemdown/_static/TF04ea000000.jsp

▶ 유료시세 신청 관련 문의 : 해외선물/FX마진 문의 1577-1282

**[FAQ]**

Q1. CME, SGX API유료시세 신청하지 않고 시세 조회 시 어떻게 응답되나요?

REST API의 경우, 아래 오류메시지가 확인됩니다.

{

"rt_cd": "1",

"msg_cd": "EGW00550",

"msg1": "CME SUB거래소 신청 계좌가 아닙니다."

}

Websocket의 경우 실시간데이터가 수신되지 않습니다.

**Q2. CME, SGX 시세를 HTS, MTS에서 조회 시에도 유료인가요?**

그렇지 않습니다. HTS, MTS에서는 CME, SGX 시세 조회 시, 무료입니다.

API로의 CME, SGX 시세 조회 시 위에 기술된 순서대로 유료시세신청 후 시세 수신 가능합니다.

**Q3. HTS 설치가 불가하여 유료시세 신청이 어려울 경우 어떻게 유료시세 신청이 가능할까요?**

HTS 설치가 불가하여 유료시세 신청이 어려우실 경우 한국투자증권 해외선물/FX마진 고객센터(1577-1282)로 문의 부탁드립니다.

**Q4. CME, SGX 외의 거래소 무료시세에 대해서도 위 신청 과정이 필요할까요?**

CME, SGX 외의 거래소 시세는 위와 같은 신청과정이 필요하지 않으며, API로의 무료시세 수신이 가능합니다.

위에 기술된 신청과정은 CME, SGX 유료시세 신청시에만 필수적입니다.

Q5. CME, SGX 유료시세 신청했는데도**"CME/SGX SUB거래소 신청 계좌가 아닙니다." 오류가 발생합니다.**

유료시세 신청 후 접근토큰발급API (/oauth2/tokenP) 발급하셨는지 확인 부탁드립니다.

유료시세 서비스 가입 후 반드시 "접근토큰발급API"를 호출하여 해외선물유료시세 신청정보를 동기화해 주셔야 합니다.

"접근토큰발급 API 호출 후" 최대 2시간 이후 실시간 유료 시세 수신이 가능합니다

[해외선물옵션 가이드]

1. 한국투자증권 해외선물옵션 가이드(거래절차, 손익계산, 기타)

https://securities.koreainvestment.com/main/bond/foreign/_static/TF10da000000.jsp

2. 한국투자증권 해외선물옵션 개요(해외선물이란, 거래상품, 거래시간, 해외거래소 소개간 안내, 결제일 정보, 환전안내)

https://securities.koreainvestment.com/main/bond/foreign/_static/TF03df010100.jsp

3. 한국투자증권 해외옵션 상세안내(옵션의 분류, 증거금제도, 권리행사 및 배정, 만기결제, 주문유의사항, 정산가산점)

https://securities.koreainvestment.com/main/bond/foreign/_static/TF03df110100.jsp

