from typing import TYPE_CHECKING

from pykis.api.stock.market import MARKET_TYPE, KisTradingHours
from pykis.responses.exceptions import KisNotFoundError

if TYPE_CHECKING:
    from pykis import PyKis

MARKET_SAMPLE_STOCK_MAP: dict[MARKET_TYPE, list[str] | MARKET_TYPE] = {
    # 2024/07/29 기준 시총 상위 3개 종목
    "KRX": ["005930", "000660", "373220"],  # 삼성전자, SK하이닉스, LG에너지솔루션
    "NASD": ["MSFT", "AAPL", "NVDA"],  # 마이크로소프트, 애플, 엔비디아
    "NYSE": ["TSM", "BRK-A", "LLY"],  # TSMC, 버크셔해서웨이, 일라이릴리
    "AMEX": ["IMO", "SIM", "BTG"],  # 임페리얼오일, 그루포시멕, B2골드
    "TKSE": ["7203", "8306", "6758"],  # 도요타, 미쓰비시, 소니
    "SEHK": ["04338", "00700", "00941"],  # 마이크로소프트, 텐센트, 차이나모바일
    "HASE": "VNSE",
    "VNSE": ["VCB", "BID", "FPT"],  # 베트남무역은행, 베트남개발은행, FPT
    "SHAA": ["600519", "601398", "601288"],  # 귀주모태주, 공상은행, 농업은행
    "SZAA": "SHAA",
}


def trading_hours(self: "PyKis", market: MARKET_TYPE) -> KisTradingHours:
    """
    한국투자증권 해외 장운영 시간 조회

    해외 당일 봉 차트 조회의 파생 API입니다.

    해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]
    (업데이트 날짜: 2024/07/29)

    Args:
        market (MARKET_TYPE): 시장 종류

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    from pykis.api.stock.day_chart import foreign_day_chart

    while isinstance(samples := MARKET_SAMPLE_STOCK_MAP[market], MARKET_TYPE):
        market = samples

    for symbol in samples:
        try:
            chart = foreign_day_chart(
                self,
                market=market,
                symbol=symbol,
                once=True,
            )

            return chart.trading_hours
        except KisNotFoundError:
            pass

    raise ValueError("해외 주식 시장 정보를 찾을 수 없습니다.")
