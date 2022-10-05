
![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=260&section=header&text=%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%ED%95%9C%EA%B5%AD%ED%88%AC%EC%9E%90%EC%A6%9D%EA%B6%8C%20API&fontSize=50&animation=fadeIn&fontAlignY=38&desc=KIS%20Open%20Trading%20API%20Client&descAlignY=51&descAlign=62)

## ✨ 1. 파이썬용 한국투자증권 API 소개

한국투자증권의 트레이딩 OPEN API 서비스를 파이썬 환경에서 사용할 수 있도록 만든 강력한 운용 라이브러리입니다.



## ⚙️ 2. 사용 설명

### 2.1. 서비스 신청

1. KIS 트레이딩 서비스는 [KIS Developers 서비스](https://apiportal.koreainvestment.com/)를 통해 신청 할 수 있습니다.
   한국투자증권 계좌와 아이디가 필요합니다.
![image](https://user-images.githubusercontent.com/34199905/193738291-c9c663fd-8ab4-43da-acb6-6a2f7846a79d.png)
2. 서비스를 신청이 완료되면, 아래와 같이 앱 키를 발급 받을 수 있습니다.
   만약 앱 키가 유출되었을 경우, 즉각 홈페이지에서 해지해야 합니다.
![image](https://user-images.githubusercontent.com/34199905/193740291-53f282ee-c40c-40b9-874e-2df39543cb66.png)

### 2.2. 라이브러리 설치

라이브러리는 파이썬 3.10을 기준으로 작성되었다.
하위버전으로 했다가 오류나서 뭐라 하지 말라.

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

#### 2.3.1. 임포트

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
```log
[10/04 15:53:30] INFO MARKET: sync kospi, download https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip
[10/04 15:53:30] INFO RTC websocket connected
[10/04 15:53:31] INFO MARKET: parseing kospi data... 1967 lines
[10/04 15:53:32] INFO MARKET: sync kosdaq, download https://new.real.download.dws.co.kr/common/master/kosdaq_code.mst.zip
[10/04 15:53:33] INFO MARKET: parseing kosdaq data... 1587 lines
[10/04 15:53:34] INFO MARKET: sync sector, download https://new.real.download.dws.co.kr/common/master/idxcode.mst.zip
[10/04 15:53:35] INFO MARKET: parseing sector data... 483 lines
```

초기 생성시 시장정보를 동기화 한다. 시장 정보는 `$temp/.pykis-cache_market.{version}.db` 에 저장된다.
시장 정보는 마지막 동기화 시간을 기준으로 24시간마다 자동으로 갱신된다.

#### 2.3.3. 간단한 예제

백번 설명하는 것보다 한번 코드를 보는게 이해하기 쉬울 것이다.

#### 시작하기 전에...

초보 이용자를 위해 수명 10분 아끼는 방법 몇 가지를 소개한다.

1. **사용할줄 모르면 기본값으로 두자.**

2. 이 라이브러리는 다른 라이브러리와 다르게 모든 데이터가 타이핑이 되어있다.
그렇기에 문서 없이 IDE의 자동완성 기능만으로도 사용이 가능하다.
예를 들어 VSCode에서 `price = kis.stock('000660').price()` 이후 `price.`을 입력하면 다음과 같은 자동완성이 나온다.
나오지 않는 경우 `Ctrl + Space`를 눌러 자동완성을 활성화 시키자.
![image](https://user-images.githubusercontent.com/34199905/193761942-55bf37ed-b50c-48ec-8a31-effc9126c899.png)
해당 화면에서 찾기 어려운 경우 함수 부분에 커서를 두고 `F12`를 눌러 해당 함수의 정의로 이동한다.
![image](https://user-images.githubusercontent.com/34199905/193762382-2210cb75-3a78-44de-ae9e-02e02794f01d.png)
그 후 함수의 리턴 타입 `->` 다음 부분에 커서를 두고 `F12`를 누르면 해당 타입의 정의로 이동 할 수 있다.
![image](https://user-images.githubusercontent.com/34199905/193763078-dcca18ce-f15a-4619-bf87-615370e91378.png)
다음과 같이 해당 클래스의 필드들을 한번에 확인 할 수 있다.
![image](https://user-images.githubusercontent.com/34199905/193764039-b651720a-e1e2-4f4b-bbf5-6735dd83a32f.png)
이 방법을 이용하여 수명을 늘릴 수 있다.


TODO: WIKI PAGE


