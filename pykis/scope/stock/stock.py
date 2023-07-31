from typing import TYPE_CHECKING, Literal

from ...rtclient import KisRTSysResponse, RT_CODE_TYPE

from ..base import KisScopeBase
from .._import import *

if TYPE_CHECKING:
    from ...kis import PyKis
    from ...market import KisKStockItem


class KisStockScope(KisScopeBase):
    kis: "PyKis"
    """KIS API"""
    code: str
    """단축코드"""
    name: str
    """한글종목명"""
    info: "KisKStockItem"
    """종목 정보"""

    def __init__(self, kis: "PyKis", info: "KisKStockItem"):
        self.kis = kis
        self.info = info
        self.code = info.mksc_shrn_iscd
        self.name = info.hts_kor_isnm

    @property
    def etf(self) -> bool:
        """ETF 여부"""
        return self.info.scrt_grp_cls_code == "EF" or self.info.scrt_grp_cls_code == "FE"

    @property
    def elw(self) -> bool:
        """ELW 여부"""
        return self.info.scrt_grp_cls_code == "EW"

    @property
    def etn(self) -> bool:
        """ETN 여부"""
        return self.info.etp_prod_cls_code == "3" or self.info.etp_prod_cls_code == "4"

    @property
    def stock(self) -> bool:
        """주식 여부"""
        return not self.etf and not self.etn and not self.elw

    from .api import (
        price,
        price_daily,
        period_price,
        overtime_price_daily,
        asking_price,
        conclude,
        day_conclude,
        overtime_conclude,
        elw_price,
        investor,
        member,
    )

    def rt_add(self, id: RT_CODE_TYPE, timeout: int = 10) -> KisRTSysResponse | None:
        """실시간 응답을 등록합니다.

        Args:
            id (Literal['체결가', '호가', '체결']): 등록할 실시간 코드
        Raises:
            KeyError: 등록할 실시간 코드가 잘못되었습니다.
            Exception: 이미 등록된 코드입니다.
        """
        return self.rtclient.add(id, self.code, timeout=timeout)

    def rt_remove(self, id: RT_CODE_TYPE, timeout: int = 10) -> KisRTSysResponse | None:
        """실시간 응답을 해제합니다.

        Args:
            id (Literal['체결가', '호가', '체결']): 해제할 실시간 코드
            tr_key (str): 실시간 키
            timeout (int, optional): 응답 대기 시간. Defaults to 10.

        Returns:
            KisRTSysResponse: 등록 해제 응답.
            None: 이미 등록 해제 되어 있습니다
        """
        return self.rtclient.remove(id, self.code, timeout=timeout)
