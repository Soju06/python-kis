from ._import import *

TR_ID_CODE_MAP: list[dict[str, tuple[str, str]]] = [
    # [실전투자]
    {
        # '거래소명': ('매수 TR_ID', '매도 TR_ID')
        "NASD": ("TTTT1002U", "TTTT1006U"),  # 미국
        "NYSE": ("TTTT1002U", "TTTT1006U"),  # 미국
        "AMEX": ("TTTT1002U", "TTTT1006U"),  # 미국
        "TKSE": ("TTTS0308U", "TTTS0307U"),  # 일본
        "SHAA": ("TTTS0202U", "TTTS1005U"),  # 상해
        "SEHK": ("TTTS1002U", "TTTS1001U"),  # 홍콩
        "SZAA": ("TTTS0305U", "TTTS0304U"),  # 심천
        "HASE": ("TTTS0311U", "TTTS0310U"),  # 베트남 하노이
        "VNSE": ("TTTS0311U", "TTTS0310U"),  # 베트남 호치민
    },
    # [모의투자]
    {
        "NASD": ("VTTT1002U", "VTTT1001U"),  # 미국
        "NYSE": ("VTTT1002U", "VTTT1001U"),  # 미국
        "AMEX": ("VTTT1002U", "VTTT1001U"),  # 미국
        "TKSE": ("VTTS0308U", "VTTS0307U"),  # 일본
        "SHAA": ("VTTS0202U", "VTTS1005U"),  # 상해
        "SEHK": ("VTTS1002U", "VTTS1001U"),  # 홍콩
        "SZAA": ("VTTS0305U", "VTTS0304U"),  # 심천
        "HASE": ("VTTS0311U", "VTTS0310U"),  # 베트남 하노이
        "VNSE": ("VTTS0311U", "VTTS0310U"),  # 베트남 호치민
    },
]

# * 해외 거래소 운영시간 외 API 호출 시 애러가 발생하오니 운영시간을 확인해주세요.
# * 해외 거래소 운영시간(한국시간 기준)
# 1) 미국 : 23:30 ~ 06:00 (썸머타임 적용 시 22:30 ~ 05:00)
# 2) 일본 : (오전) 09:00 ~ 11:30, (오후) 12:30 ~ 15:00
# 3) 상해 : 10:30 ~ 16:00
# 4) 홍콩 : (오전) 10:30 ~ 13:00, (오후) 14:00 ~ 17:00


def overseas_order(
    self: "KisAccountScope",
    market: OVERSEAS_OVRS_EXCG_CD,
    code: str,
    qty: int,
    unpr: float,
    type: Literal["매도", "매수"],
    dvsn: OVERSEAS_ORD_DVSN_TYPE = "지정가",
) -> "KisStockOrder":
    """해외주식 주문

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (int): 주문 단가
        type (Literal['매도', '매수']): 주문 타입
        dvsn (US_ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
            미국 홍콩 외 일부 시장에서는 주문 구분을 None으로 설정해야 합니다.
    """
    if len(code) > 12:
        raise ValueError("종목코드는 12자리 이하입니다.")

    if market not in OVERSEAS_OVRS_EXCGS:
        market = OVERSEAS_R_OVRS_EXCGS.get(market, None)  # type: ignore
        if market is None:
            raise ValueError(
                f'해외 시장 구분은 ({", ".join(f"{k}, {v}" for k, v in OVERSEAS_R_OVRS_EXCGS.items())}) 중 하나여야 합니다.'
            )

    tr_id = TR_ID_CODE_MAP[1 if self.key.virtual_account else 0][market][0 if type == "매수" else 1]
    supported_dvsn = OVERSEAS_ORD_DVSN_MAP.get(tr_id, OVERSEAS_ORD_DVSN_MAP[None])
    if dvsn not in supported_dvsn:
        raise ValueError(f'주문 구분은 ({", ".join(i if i else "None" for i in supported_dvsn)}) 중 하나여야 합니다.')

    dvsn = OVERSEAS_R_ORD_DVSNS.get(dvsn, dvsn)  # type: ignore

    return self.client.request(
        "post",
        "/uapi/overseas-stock/v1/trading/order",
        headers={
            "tr_id": tr_id,
        },
        body=self.account.build_body(
            {
                "OVRS_EXCG_CD": market,
                "PDNO": code,
                "ORD_QTY": qty,
                "ORD_DVSN": dvsn,
                "OVRS_ORD_UNPR": str(unpr),
                "ORD_SVR_DVSN_CD": "0",
            }
        ),
        response=KisStockOrder,
    )


def overseas_buy(
    self: "KisAccountScope",
    market: OVERSEAS_OVRS_EXCG_CD,
    code: str,
    qty: int,
    unpr: float,
    dvsn: OVERSEAS_ORD_DVSN_TYPE = "지정가",
) -> "KisStockOrder":
    """해외주식 매수

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (float): 주문 단가
        dvsn (US_ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
            미국 홍콩 외 일부 시장에서는 주문 구분을 None으로 설정해야 합니다.
    """
    return self.overseas_order(market, code, qty, unpr, "매수", dvsn)


def overseas_sell(
    self: "KisAccountScope",
    market: OVERSEAS_OVRS_EXCG_CD,
    code: str,
    qty: int,
    unpr: float,
    dvsn: OVERSEAS_ORD_DVSN_TYPE = "지정가",
) -> "KisStockOrder":
    """해외주식 매도

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (float): 주문 단가
        dvsn (US_ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
            미국 홍콩 외 일부 시장에서는 주문 구분을 None으로 설정해야 합니다.
    """
    return self.overseas_order(market, code, qty, unpr, "매도", dvsn)
