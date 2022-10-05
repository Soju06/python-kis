# 여기는 테스트 코드가 아닙니다.

from pykis import *




kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey='Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX',
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret='V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvYXXXXXXXXXXXX',
    # 가상 계좌 여부
    virtual_account=True,
    # 시장 데이터베이스 경로 (기본값: os temp 경로)
    market_database_path=None,
    # 시장 자동 동기화 여부 (기본값: True)
    market_auto_sync=True,
    # 실시간 API 사용 여부 (기본값: True)
    realtime=True,
    # 클라이언트 로거 (기본값: Logger(name='pykis', level=INFO))
    logger=None,
    # 나중에 초기화할지 여부 [WS 연결, 시장 동기화 등등..]  (기본값: False)
    late_init=False
)