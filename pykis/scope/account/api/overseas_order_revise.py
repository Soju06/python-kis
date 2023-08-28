from ._import import *


TR_ID_CODE_MAP: list[dict[str, str]] = [
    # [실전투자]
    {
        "NASD": "TTTT1004U",  # 미국
        "NYSE": "JTTT1004U",  # 미국
        "AMEX": "JTTT1004U",  # 미국
        "SEHK": "TTTS1003U",  # 홍콩
        "SHAA": "TTTS0302U",  # 상해
        "SZAA": "TTTS0306U",  # 심천
        "TKSE": "TTTS0309U",  # 일본
        "HASE": "TTTS0312U",  # 베트남 하노이
        "VNSE": "TTTS0312U",  # 베트남 호치민
    },
    # [모의투자]
    {
        "NASD": "VTTT1004U",  # 미국
        "NYSE": "VTTT1004U",  # 미국
        "AMEX": "VTTT1004U",  # 미국
        "SEHK": "VTTS1003U",  # 홍콩
        "SHAA": "VTTS0302U",  # 상해
        "SZAA": "VTTS0306U",  # 심천
        "TKSE": "VTTS0309U",  # 일본
        "HASE": "VTTS0312U",  # 베트남 하노이
        "VNSE": "VTTS0312U",  # 베트남 호치민
    },
]


def overseas_order_revise(
    self: "KisAccountScope",
    market: OVERSEAS_OVRS_EXCG_CD,
    order: KisStockOrderBase,
    type: Literal["01", "02", "정정", "취소"],
    code: str,
    qty: int | None,
    unpr: float,
) -> "KisStockOrder":
    """주식 주문 정정/취소

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        order (KisStockOrder): 정정할 주식 주문
        type (Literal['01', '02', '취소', '정정']): 정정/취소 구분
        code (str): 종목코드
        qty (int | None): 주문 수량 (None일 경우 전량 정정)
        unpr (float, optional): 주문 단가. 주문 취소시 0

    Returns:
        KisStockOrder: 주식 주문 응답
    """
    if len(code) > 12:
        raise ValueError("종목코드는 12자리 이하입니다.")

    if market not in OVERSEAS_OVRS_EXCGS:
        market = OVERSEAS_R_OVRS_EXCGS.get(market, None)  # type: ignore
        if market is None:
            raise ValueError(
                f'해외 시장 구분은 ({", ".join(f"{k}, {v}" for k, v in OVERSEAS_R_OVRS_EXCGS.items())}) 중 하나여야 합니다.'
            )

    if type[0] != "0":
        type = "01" if type == "정정" else "02"

    return self.client.request(
        "post",
        "/uapi/overseas-stock/v1/trading/order-rvsecncl",
        headers={
            "tr_id": TR_ID_CODE_MAP[1 if self.key.virtual_account else 0][market],
        },
        body=self.account.build_body(
            {
                "ORGN_ODNO": order.odno,
                "PDNO": code,
                "RVSE_CNCL_DVSN_CD": type,
                "ORD_QTY": qty or 0,
                "OVRS_ORD_UNPR": str(unpr),
                "OVRS_EXCG_CD": market,
                "ORD_SVR_DVSN_CD": "0",
            }
        ),
        response=KisStockOrder,
    )


def overseas_cancel(
    self: "KisAccountScope",
    market: OVERSEAS_OVRS_EXCG_CD,
    code: str,
    order: KisStockOrderBase,
    qty: int | None = None,
) -> "KisStockOrder":
    """
    주식 주문 취소

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        code (str): 종목코드
        order (KisStockOrderBase): 주문
        qty (int): 취소 수량
    """
    return self.overseas_order_revise(
        market,
        order,
        "취소",
        code,
        qty,
        0,
    )


def overseas_revise(
    self: "KisAccountScope",
    market: OVERSEAS_OVRS_EXCG_CD,
    code: str,
    order: KisStockOrderBase,
    qty: int | None,
    unpr: float,
) -> "KisStockOrder":
    """
    주식 주문 정정

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        code (str): 종목코드
        order (KisStockOrderBase): 주문
        qty (int): 정정 수량
        unpr (float): 정정 단가
    """
    return self.overseas_order_revise(
        market,
        order,
        "정정",
        code,
        qty,
        unpr,
    )
