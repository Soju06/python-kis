from ._import import *


def info(
    self: "KisMarketClient",
    pdno: str,
    prdt_type_cd: PRDT_TYPE_CD = "주식",
) -> "KisMarketSearchInfo":
    """상품기본정보 조회

    Args:
        pdno (str): 상품번호
        prdt_type_cd (PRDT_TYPE_CD, optional): 상품유형코드. Defaults to "주식".
    """

    if not pdno:
        raise ValueError("상품번호가 없습니다.")

    return self.client.request(
        "get",
        "/uapi/domestic-stock/v1/quotations/chk-holiday",
        headers={
            "tr_id": "CTPF1604R",
        },
        params={
            "PDNO": pdno,
            "PRDT_TYPE_CD": prdt_type_cd,
        },
        response=KisMarketSearchInfo,
        domain_type="real",
    )
