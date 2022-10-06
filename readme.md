
![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=260&section=header&text=%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%ED%95%9C%EA%B5%AD%ED%88%AC%EC%9E%90%EC%A6%9D%EA%B6%8C%20API&fontSize=50&animation=fadeIn&fontAlignY=38&desc=KIS%20Open%20Trading%20API%20Client&descAlignY=51&descAlign=62&customColorList=24)

## ✨ 1. 파이썬용 한국투자증권 API 소개

한국투자증권의 트레이딩 OPEN API 서비스를 파이썬 환경에서 사용할 수 있도록 만든 강력한 운용 라이브러리입니다.

### 1.1. 라이브러리 특징

#### <b>🖋️ 모든 형식에 Typing</b>
이 라이브러리는 모든 함수와 클래스에 Typing을 적용하여, 파이썬의 동적 타이핑을 보완합니다.
IDE의 자동완성 기능을 통해, 공식 문서 없이 더욱 빠르고 정확한 개발이 가능합니다.

#### <b>🔗 복구 가능한 실시간 클라이언트</b>
이 라이브러리는 실시간 데이터를 받아오는 클라이언트를 네트워크 문제 등으로 인해 중단했을 때, 다시 시작할 수 있도록 만들어졌습니다.
또한, 이전에 등록된 조회도 자동으로 재등록합니다.

#### <b>🔍 시장 종목 자동 파싱</b>
이 라이브러리는 텍스트 파일인 시장별 종목 정보를 자동으로 파싱하여, SQLite 데이터베이스에 저장합니다.
빠른 조회와 검색을 사용할 수 있으며, 매일 자동으로 업데이트됩니다.

## ⚙️ 2. 사용 설명

### 2.1. 서비스 신청

1. KIS 트레이딩 서비스는 [KIS Developers 서비스](https://apiportal.koreainvestment.com/)를 통해 신청 할 수 있습니다.
   한국투자증권 계좌와 아이디가 필요합니다.
![image](https://user-images.githubusercontent.com/34199905/193738291-c9c663fd-8ab4-43da-acb6-6a2f7846a79d.png)
1. 서비스를 신청이 완료되면, 아래와 같이 앱 키를 발급 받을 수 있습니다.
![image](https://user-images.githubusercontent.com/34199905/193740291-53f282ee-c40c-40b9-874e-2df39543cb66.png)

### 2.2. 라이브러리 설치

라이브러리는 파이썬 3.10을 기준으로 작성되었습니다.

```zsh
pip install python-kis
```

사용 모듈은 다음과 같다.

```
requests>=2.28.1
SQLAlchemy>=1.4.39
websocket-client>=1.4.1
pycryptodome>=3.15.0
colorlog>=6.7.0
```

### 2.3. 라이브러리 사용

#### 2.3.1. 라이브러리 설치

라이브러리는 파이썬 3.10을 기준으로 작성되었다.

```zsh
pip install python-kis
```

#### 2.3.2. 임포트

하도 클래스가 많아서 암 걸리기 싫으면 `from pykis import *`로 임포트 하자.

클래스 네이밍 규칙은 Kis + 기능명 이니까 충돌 할 일 없다.

```py
from pykis import *
```

#### 2.3.2. PyKis 객체 생성

모든 KIS API는 PyKis 객체를 통해 사용할 수 있다.
하나의 파이썬 프로세스에서 여러 PyKis 객체 생성을 권장하지 않는다.
다 잘 되게 해놨다. 하나만 쓰자.

```py
kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True,
)
```

#### 2.3.3. 라이브러리 사용

- <b>[1. 라이브러리 설치](https://github.com/Soju06/python-kis/wiki/Tutorial#1-라이브러리-설치)</b>
- <b>[2. 임포트](https://github.com/Soju06/python-kis/wiki/Tutorial#2-임포트)</b>
- <b>[3. 시장 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#3-시장-조회)</b>
- [3.1. 시장 전종목 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#31-시장-전종목-조회)
- [3.2. 시장 종목 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#32-시장-종목-조회)
- [3.3. 시장 검색](https://github.com/Soju06/python-kis/wiki/Tutorial#33-시장-검색)
- <b>[4. 종목 상세](https://github.com/Soju06/python-kis/wiki/Tutorial#4-종목-상세)</b>
- [4.1. 현재가 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#41-현재가-조회)
- [4.2. 호가 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#42-호가-조회)
- [4.3. 기간봉 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#43-기간봉-조회)
- [4.4. 이 외 기능](https://github.com/Soju06/python-kis/wiki/Tutorial#44-이-외-기능)
- <b>[5. 실시간 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#5-실시간-조회)</b>
- [5.1. 실시간 체결가](https://github.com/Soju06/python-kis/wiki/Tutorial#51-실시간-체결가)
- [5.2. 실시간 호가](https://github.com/Soju06/python-kis/wiki/Tutorial#52-실시간-호가)
- [5.3. 실시간 체결](https://github.com/Soju06/python-kis/wiki/Tutorial#53-실시간-체결)
- [5.4. 리스너 해제](https://github.com/Soju06/python-kis/wiki/Tutorial#54-리스너-해제)
- [5.5. 실시간 해제](https://github.com/Soju06/python-kis/wiki/Tutorial#55-실시간-해제)
- [5.6. 모든 이벤트 수신](https://github.com/Soju06/python-kis/wiki/Tutorial#56-모든-이벤트-수신)
- <b>[6. 계좌](https://github.com/Soju06/python-kis/wiki/Tutorial#6-계좌)</b>
- [6.1. 잔고 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#61-잔고-조회)
- [6.2. 주문가능 금액 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#62-주문가능-금액-조회)
- [6.3. 매수 주문](https://github.com/Soju06/python-kis/wiki/Tutorial#63-매수-주문)
- [6.4. 매도 주문](https://github.com/Soju06/python-kis/wiki/Tutorial#64-매도-주문)
- [6.5. 주문 취소](https://github.com/Soju06/python-kis/wiki/Tutorial#65-주문-취소)
- [6.6. 주문 정정](https://github.com/Soju06/python-kis/wiki/Tutorial#66-주문-정정)
- [6.7. 이 외의 기능](https://github.com/Soju06/python-kis/wiki/Tutorial#67-이-외의-기능)
- <b>[7. 유틸리티](https://github.com/Soju06/python-kis/wiki/Tutorial#7-유틸리티)</b>
- [7.1. 상한가하한가 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#71-상한가하한가-조회)
- [7.2. 등락율 순위 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#72-등락율-순위-조회)
- [7.3. 시장오픈여부 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#73-시장오픈여부-조회)

#### 📚 예제 목록

- [계좌 조회](https://github.com/Soju06/python-kis/wiki/Examples#1-계좌-조회)
- [계좌 주문](https://github.com/Soju06/python-kis/wiki/Examples#2-계좌-주문)
- [종목 시세](https://github.com/Soju06/python-kis/wiki/Examples#3-종목-시세)
- [실시간 체결가체결 조회](https://github.com/Soju06/python-kis/wiki/Examples#4-실시간-체결가체결-조회)
- [상한가/하한가/상승/하락/거래상위 종목 조회](https://github.com/Soju06/python-kis/wiki/Examples#5-상한가하한가상승하락거래상위-종목-조회)
- [시장 오픈 여부](https://github.com/Soju06/python-kis/wiki/Examples#6-시장-오픈-여부)


## 📦 지원하는 API

국내 주식 시장에서 사용할 수 있는 API를 지원합니다.
해외, 선물, 옵션 등과 신용은 지원하지 않습니다.


| API | 기능 | 지원 여부 |
| :--- | :--- | :--- |
| OAuth인증 | Hashkey | ✅ |
| OAuth인증 | 접근토큰발급(P) | ✅ |
| OAuth인증 | 접근토큰폐기(P) | ✅ |
| 국내주식주문 | 주식주문(현금) | ✅ |
| 국내주식주문 | 주식주문(신용) | ❌ |
| 국내주식주문 | 주식주문(정정취소) | ✅ |
| 국내주식주문 | 주식정정취소가능주문조회 | ✅ |
| 국내주식주문 | 주식일별주문체결조회 | ✅ |
| 국내주식주문 | 주식잔고조회 | ✅ |
| 국내주식주문 | 매수가능조회 | ✅ |
| 국내주식주문 | 주식예약주문 | ❌ |
| 국내주식주문 | 주식예약주문정정취소 | ❌ |
| 국내주식주문 | 주식예약주문조회 | ❌ |
| 국내주식주문 | 퇴직연금종합주문 | ❌ |
| 국내주식시세 | 주식현재가 시세 | ✅ |
| 국내주식시세 | 주식현재가 체결 | ✅ |
| 국내주식시세 | 주식현재가 일자별 | ✅ |
| 국내주식시세 | 주식현재가 호가 예상체결 | ✅ |
| 국내주식시세 | 주식현재가 투자자 | ✅ |
| 국내주식시세 | 주식현재가 회원사 | ✅ |
| 국내주식시세 | ELW현재가 시세 | ✅ |
| 국내주식시세 | 국내주식기간별시세(일/주/월/년) | ✅ |
| 국내주식시세 | 국내주식업종기간별시세(일/주/월/년) | ✅ |
| 국내주식시세 | 주식현재가 당일시간대별체결 | ✅ |
| 국내주식시세 | 주식현재가 시간외시간별체결 | ✅ |
| 국내주식시세 | 주식현재가 시간외일자별주가 | ✅ |
| 국내주식시세 | 주식당일분봉조회 | ✅ |
| 실시간시세 | 주식현재가 실시간주식체결가 | ✅ |
| 실시간시세 | 주식현재가 실시간주식호가 | ✅ |
| 실시간시세 | 주식현재가 실시간주식체결통보 | ✅ |
| 실시간시세 | 해외주식 실시간지연체결가 | ✅ |
| 실시간시세 | 해외주식 실시간지연호가 | ❌ |
| 실시간시세 | 해외주식 실시간체결통보 | ❌ |
| 국내선물옵션주문 | * | ❌ |
| 국내선물옵션시세 | * | ❌ |
| 해외주식주문 | * | ❌ |
| 해외주식현재가 | * | ❌ |
| 해외선물옵션주문 | * | ❌ |
| 해외선물옵션시세 | * | ❌ |

### License

[MIT](https://github.com/Soju06/python-kis/blob/main/LICENCE)
