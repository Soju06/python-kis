
![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=260&section=header&text=%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%ED%95%9C%EA%B5%AD%ED%88%AC%EC%9E%90%EC%A6%9D%EA%B6%8C%20API&fontSize=50&animation=fadeIn&fontAlignY=38&desc=KIS%20Open%20Trading%20API%20Client&descAlignY=51&descAlign=62&customColorList=24)

## ✨ 1. 파이썬용 한국투자증권 API 소개

한국투자증권의 트레이딩 OPEN API 서비스를 파이썬 환경에서 사용할 수 있도록 만든 강력한 운용 라이브러리입니다.

### 1.1. 라이브러리 특징

<details>
  <summary><h4><b>🖋️ 모든 형식에 Typing</b></h4></summary>

  이 라이브러리는 모든 함수와 클래스에 Typing을 적용하여, 파이썬의 동적 타이핑을 보완합니다.
  IDE의 자동완성 기능을 통해, 공식 문서 없이 더욱 빠르고 정확한 개발이 가능합니다.
</details>


<details>
  <summary><h4><b>🔗 복구 가능한 실시간 클라이언트</b></h4></summary>

  이 라이브러리는 실시간 데이터를 받아오는 클라이언트를 네트워크 문제 등으로 인해 중단했을 때, 다시 시작할 수 있도록 만들어졌습니다.
  또한, 이전에 등록된 조회도 자동으로 재등록합니다.
</details>

<details>
  <summary><h4><b>🔍 시장 종목 자동 파싱</b></h4></summary>

  이 라이브러리는 텍스트 파일인 시장별 종목 정보를 자동으로 파싱하여, SQLite 데이터베이스에 저장합니다.
  빠른 조회와 검색을 사용할 수 있으며, 매일 자동으로 업데이트됩니다.
</details>

<hr>

## ⚙️ 2. 사용 설명


<details>
  <summary><h3>2.1. 서비스 신청</h3></summary>

  1. 한국투자증권 계좌와 아이디가 필요합니다. KIS 트레이딩 서비스는 [KIS Developers 서비스](https://apiportal.koreainvestment.com/)를 통해 신청 할 수 있습니다.

  ![image](https://user-images.githubusercontent.com/34199905/193738291-c9c663fd-8ab4-43da-acb6-6a2f7846a79d.png)

  2. 서비스를 신청이 완료되면, 아래와 같이 앱 키를 발급 받을 수 있습니다.

  ![image](https://user-images.githubusercontent.com/34199905/193740291-53f282ee-c40c-40b9-874e-2df39543cb66.png)
</details>

### 2.2. 📦 라이브러리 설치

라이브러리는 파이썬 3.10을 기준으로 작성되었습니다.

```zsh
pip install python-kis
```

<details>
  <summary>사용된 모듈 보기</summary>

  ```
  requests>=2.28.1
  SQLAlchemy>=1.4.39
  websocket-client>=1.4.1
  pycryptodome>=3.15.0
  colorlog>=6.7.0
  ```
</details>

<hr>

### 2.3. 라이브러리 사용

#### 2.3.1. 임포트

하도 클래스가 많아 `from pykis import *`로 임포트 하자.

클래스 네이밍 규칙은 Kis + 기능명 이니까 충돌 할 일 없다.

```py
from pykis import *
```

<hr>


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

시각화를 위해 PrettyTable를 사용했다.

다음의 명령어로 PrettyTable을 설치할 수 있다.
```sh
pip install prettytable
```

잔고를 조회해보자.

```py
from pykis import *
from prettytable import PrettyTable

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True,
)

# 먼저 계좌 스코프를 생성한다.
account = kis.account('50071022-01') # 계좌번호 ex) 50071022-01 또는 5007102201
# 이제 잔고를 조회한다.
balance = account.balance_all()

# 결과를 출력한다.
print(f'예수금: {balance.dnca_tot_amt:,}원 평가금: {balance.tot_evlu_amt:,} 손익: {balance.evlu_pfls_smtl_amt:,}원')

# 테이블을 시각화 하기 위해 PrettyTable을 사용한다.

table = PrettyTable(field_names=[
        '상품번호', '상품명', '보유수량', '매입금액',
        '현재가', '평가손익율', '평가손익',
    ], align='r',
)

# 잔고를 테이블에 추가한다.
for stock in balance.stocks:
    table.add_row([
        stock.pdno,
        stock.prdt_name,
        f'{stock.hldg_qty:,}주',
        f'{stock.pchs_amt:,}원',
        f'{stock.prpr:,}원',
        f'{stock.evlu_pfls_rt:.2f}%',
        f'{stock.evlu_pfls_amt:,}원',
    ])

print(table)
```

결과는 다음과 같다.

```log
예수금: 7,799,675원 평가금: 10,071,255 손익: 70,165원
+----------+----------------+----------+-----------+-----------+------------+-----------+
| 상품번호 |         상품명 | 보유수량 |  매입금액 |    현재가 | 평가손익율 |  평가손익 |
+----------+----------------+----------+-----------+-----------+------------+-----------+
|   004370 |           농심 |      3주 | 910,500원 | 298,000원 |     -1.81% | -16,500원 |
|   005305 |     롯데칠성우 |      4주 | 274,900원 |  68,200원 |     -0.76% |  -2,100원 |
|   005935 |     삼성전자우 |      4주 | 190,000원 |  51,000원 |      7.37% |  14,000원 |
|   034220 |   LG디스플레이 |     20주 | 241,000원 |  13,550원 |     12.45% |  30,000원 |
|   053260 |       금강철강 |     20주 | 145,800원 |   7,550원 |      3.57% |   5,200원 |
|   073240 |     금호타이어 |      3주 |  10,215원 |   3,260원 |     -4.26% |    -435원 |
|   373220 | LG에너지솔루션 |      1주 | 429,000원 | 469,000원 |      9.32% |  40,000원 |
+----------+----------------+----------+-----------+-----------+------------+-----------+
```

~~투자 결과가 나쁘지 않은걸?~~

<hr>

#### 2.3.4. 라이브러리 사용

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


## 3. 📦 지원하는 API

국내 주식 시장에서 사용할 수 있는 API를 지원합니다.
선물, 옵션 등과 신용은 지원하지 않습니다.


| API              | 기능                                | 지원 여부 |
| :--------------- | :---------------------------------- | :-------- |
| OAuth인증        | Hashkey                             | ✅         |
| OAuth인증        | 접근토큰발급(P)                     | ✅         |
| OAuth인증        | 접근토큰폐기(P)                     | ✅         |
| 국내주식주문     | 주식주문(현금)                      | ✅         |
| 국내주식주문     | 주식주문(신용)                      | ❌         |
| 국내주식주문     | 주식주문(정정취소)                  | ✅         |
| 국내주식주문     | 주식정정취소가능주문조회            | ✅         |
| 국내주식주문     | 주식일별주문체결조회                | ✅         |
| 국내주식주문     | 주식잔고조회                        | ✅         |
| 국내주식주문     | 매수가능조회                        | ✅         |
| 국내주식주문     | 주식예약주문                        | ❌         |
| 국내주식주문     | 주식예약주문정정취소                | ❌         |
| 국내주식주문     | 주식예약주문조회                    | ❌         |
| 국내주식주문     | 퇴직연금종합주문                    | ❌         |
| 국내주식주문     | 주식잔고조회_실현손익               | ✅         |
| 국내주식시세     | 주식현재가 시세                     | ✅         |
| 국내주식시세     | 주식현재가 체결                     | ✅         |
| 국내주식시세     | 주식현재가 일자별                   | ✅         |
| 국내주식시세     | 주식현재가 호가 예상체결            | ✅         |
| 국내주식시세     | 주식현재가 투자자                   | ✅         |
| 국내주식시세     | 주식현재가 회원사                   | ✅         |
| 국내주식시세     | ELW현재가 시세                      | ✅         |
| 국내주식시세     | 국내주식기간별시세(일/주/월/년)     | ✅         |
| 국내주식시세     | 국내주식업종기간별시세(일/주/월/년) | ✅         |
| 국내주식시세     | 주식현재가 당일시간대별체결         | ✅         |
| 국내주식시세     | 주식현재가 시간외시간별체결         | ✅         |
| 국내주식시세     | 주식현재가 시간외일자별주가         | ✅         |
| 국내주식시세     | 주식당일분봉조회                    | ✅         |
| 국내주식시세     | 상품기본조회                        | ✅         |
| 실시간시세       | 주식현재가 실시간주식체결가         | ✅         |
| 실시간시세       | 주식현재가 실시간주식호가           | ✅         |
| 실시간시세       | 주식현재가 실시간주식체결통보       | ✅         |
| 실시간시세       | 해외주식 실시간지연체결가           | ❌         |
| 실시간시세       | 해외주식 실시간지연호가             | ❌         |
| 실시간시세       | 해외주식 실시간체결통보             | ❌         |
| 국내선물옵션주문 | *                                   | ❌         |
| 국내선물옵션시세 | *                                   | ❌         |
| 해외주식주문     | *                                   | ✅         |
| 해외주식현재가   | *                                   | ❌         |
| 해외선물옵션주문 | *                                   | ❌         |
| 해외선물옵션시세 | *                                   | ❌         |

## 4. ✨ Changelog

### 1.0.6

- 상품기본조회가 추가되었습니다.

- 환경 변수를 분리하였습니다.
  각각의 파일에 나뉘어있던 Version, 접속 URL, API Rate Limit 등의 상수 데이터를 `__env__.py`로 옮겼습니다.

- 예외구조 변경
  기존 HTTP Error, RT_CD Error를 모두 `ValueError`로 처리하던 구조에서 각각의 `KisHTTPError`, `KisAPIError` 예외 객체로 나누었고, `rt_cd`, `msg_cd` 등의 변수를 예외 객체에서 참조할 수 있도록 변경하였습니다.

- 엑세스토큰 발급 Thread Safe
  엑세스 토큰이 발급되어있지 않은 상태에서 멀티스레드로 `KisAccessToken.ensure()` 함수를 호출하면 Thread Lock 되지 않고 다수가 `KisAccessToken.issue()`를 호출하는 문제를 해결하였습니다.

### 1.0.5

- `RTClient`에서 웹소켓 연결이 끊어졌을 때, 이벤트 처리가 잘못되는 버그를 수정하였습니다.

- `RTClient`에서 재연결시 실시간 조회가 복구되지 않는 버그를 수정하였습니다.

- 휴장일 조회가 추가되었습니다.

- 해외 주식 주문이 추가되었습니다.

- 해외 미체결 조회가 추가되었습니다.

### 1.0.4

- 주식잔고조회_실현손익 조회가 추가되었습니다.

- [실시간 해제요청이 정상적으로 되지 않습니다](https://github.com/Soju06/python-kis/issues/1) 버그를 수정하였습니다.

### 1.0.3

- `RTClient` [웹소켓 보안강화를 위한 개선 안내](https://apiportal.koreainvestment.com/community/10000000-0000-0011-0000-000000000001)의 내용에 따라, 앱키 대신 웹소켓 접속키를 발급하여 사용하도록 변경되었습니다.

### 1.0.2

- API 초당 요청 제한을 넘어버리는 버그를 수정하였습니다.
- `period_price` 응답 데이터의 `stck_fcam`값 `float`으로 변경하였습니다.
- `utils.KRXMarketOpen` 공휴일 데이터가 1개인 경우 오류 발생하는 버그 수정하였습니다.


### License

[MIT](https://github.com/Soju06/python-kis/blob/main/LICENCE)
