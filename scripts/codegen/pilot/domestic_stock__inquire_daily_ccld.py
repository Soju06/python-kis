"""[domestic_stock] inquire_daily_ccld  v1_국내주식-005

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/inquire_daily_ccld` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from datetime import date
from decimal import Decimal

from vmkis.client.endpoint import KisEndpoint
from vmkis.responses.dynamic import KisDynamic, KisList, KisObject
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisBool, KisDate, KisDecimal, KisInt, KisString

#: pd_dv -> 엔드포인트.
#: 실전/모의 축은 KisEndpoint 가 tr_live/tr_paper 로 흡수합니다.
INQUIRE_DAILY_CCLD_ENDPOINTS: dict[str, KisEndpoint] = {
    "before": KisEndpoint(
        path="/uapi/domestic-stock/v1/trading/inquire-daily-ccld",
        tr_live="CTSC9215R",
        tr_paper="VTSC9215R",
        page_size=100,
    ),
    "inner": KisEndpoint(
        path="/uapi/domestic-stock/v1/trading/inquire-daily-ccld",
        tr_live="TTTC0081R",
        tr_paper="VTTC0081R",
        page_size=100,
    ),
}


class KisInquireDailyCcldOutput1Item(KisDynamic):
    """inquire_daily_ccld 응답 항목 — `output1` (39개 필드)"""

    ord_dt: date = KisDate["ord_dt"]
    """주문일자"""
    ord_gno_brno: str = KisString["ord_gno_brno"]
    """주문채번지점번호"""
    odno: str = KisString["odno"]
    """주문번호"""
    orgn_odno: str = KisString["orgn_odno"]
    """원주문번호"""
    ord_dvsn_name: str = KisString["ord_dvsn_name"]
    """주문구분명"""
    sll_buy_dvsn_cd: str = KisString["sll_buy_dvsn_cd"]
    """매도매수구분코드"""
    sll_buy_dvsn_cd_name: str = KisString["sll_buy_dvsn_cd_name"]
    """매도매수구분코드명"""
    pdno: str = KisString["pdno"]
    """상품번호"""
    prdt_name: str = KisString["prdt_name"]
    """상품명"""
    ord_qty: int = KisInt["ord_qty"]
    """주문수량"""
    ord_unpr: Decimal = KisDecimal["ord_unpr"]
    """주문단가"""
    ord_tmd: str = KisString["ord_tmd"]
    """주문시각"""
    tot_ccld_qty: int = KisInt["tot_ccld_qty"]
    """총체결수량"""
    avg_prvs: str = KisString["avg_prvs"]
    """평균가"""
    cncl_yn: bool = KisBool["cncl_yn"]
    """취소여부"""
    tot_ccld_amt: Decimal = KisDecimal["tot_ccld_amt"]
    """매입평균가격"""
    loan_dt: date = KisDate["loan_dt"]
    """대출일자"""
    ordr_empno: str = KisString["ordr_empno"]
    """주문자사번"""
    ord_dvsn_cd: str = KisString["ord_dvsn_cd"]
    """주문구분코드"""
    cnc_cfrm_qty: int = KisInt["cnc_cfrm_qty"]
    """취소확인수량"""
    rmn_qty: int = KisInt["rmn_qty"]
    """잔여수량"""
    rjct_qty: int = KisInt["rjct_qty"]
    """거부수량"""
    ccld_cndt_name: str = KisString["ccld_cndt_name"]
    """체결조건명"""
    inqr_ip_addr: str = KisString["inqr_ip_addr"]
    """조회IP주소"""
    cpbc_ordp_ord_rcit_dvsn_cd: str = KisString["cpbc_ordp_ord_rcit_dvsn_cd"]
    """전산주문표주문접수구분코드"""
    cpbc_ordp_infm_mthd_dvsn_cd: str = KisString["cpbc_ordp_infm_mthd_dvsn_cd"]
    """전산주문표통보방법구분코드"""
    infm_tmd: str = KisString["infm_tmd"]
    """통보시각"""
    ctac_tlno: str = KisString["ctac_tlno"]
    """연락전화번호"""
    prdt_type_cd: str = KisString["prdt_type_cd"]
    """상품유형코드"""
    excg_dvsn_cd: str = KisString["excg_dvsn_cd"]
    """거래소구분코드"""
    cpbc_ordp_mtrl_dvsn_cd: str = KisString["cpbc_ordp_mtrl_dvsn_cd"]
    """전산주문표자료구분코드"""
    ord_orgno: str = KisString["ord_orgno"]
    """주문조직번호"""
    rsvn_ord_end_dt: date = KisDate["rsvn_ord_end_dt"]
    """예약주문종료일자"""
    excg_id_dvsn_Cd: str = KisString["excg_id_dvsn_Cd"]
    """거래소ID구분코드"""
    stpm_cndt_pric: Decimal = KisDecimal["stpm_cndt_pric"]
    """스톱지정가조건가격"""
    stpm_efct_occr_dtmd: str = KisString["stpm_efct_occr_dtmd"]
    """스톱지정가효력발생상세시각"""
    tot_ord_qty: int = KisInt["tot_ord_qty"]
    """총주문수량"""
    prsm_tlex_smtl: Decimal = KisDecimal["prsm_tlex_smtl"]
    """총체결금액"""
    pchs_avg_pric: Decimal = KisDecimal["pchs_avg_pric"]
    """추정제비용합계"""


class KisInquireDailyCcldOutput2Item(KisDynamic):
    """inquire_daily_ccld 응답 항목 — `output2` (39개 필드)"""

    ord_dt: date = KisDate["ord_dt"]
    """주문일자"""
    ord_gno_brno: str = KisString["ord_gno_brno"]
    """주문채번지점번호"""
    odno: str = KisString["odno"]
    """주문번호"""
    orgn_odno: str = KisString["orgn_odno"]
    """원주문번호"""
    ord_dvsn_name: str = KisString["ord_dvsn_name"]
    """주문구분명"""
    sll_buy_dvsn_cd: str = KisString["sll_buy_dvsn_cd"]
    """매도매수구분코드"""
    sll_buy_dvsn_cd_name: str = KisString["sll_buy_dvsn_cd_name"]
    """매도매수구분코드명"""
    pdno: str = KisString["pdno"]
    """상품번호"""
    prdt_name: str = KisString["prdt_name"]
    """상품명"""
    ord_qty: int = KisInt["ord_qty"]
    """주문수량"""
    ord_unpr: Decimal = KisDecimal["ord_unpr"]
    """주문단가"""
    ord_tmd: str = KisString["ord_tmd"]
    """주문시각"""
    tot_ccld_qty: int = KisInt["tot_ccld_qty"]
    """총체결수량"""
    avg_prvs: str = KisString["avg_prvs"]
    """평균가"""
    cncl_yn: bool = KisBool["cncl_yn"]
    """취소여부"""
    tot_ccld_amt: Decimal = KisDecimal["tot_ccld_amt"]
    """매입평균가격"""
    loan_dt: date = KisDate["loan_dt"]
    """대출일자"""
    ordr_empno: str = KisString["ordr_empno"]
    """주문자사번"""
    ord_dvsn_cd: str = KisString["ord_dvsn_cd"]
    """주문구분코드"""
    cnc_cfrm_qty: int = KisInt["cnc_cfrm_qty"]
    """취소확인수량"""
    rmn_qty: int = KisInt["rmn_qty"]
    """잔여수량"""
    rjct_qty: int = KisInt["rjct_qty"]
    """거부수량"""
    ccld_cndt_name: str = KisString["ccld_cndt_name"]
    """체결조건명"""
    inqr_ip_addr: str = KisString["inqr_ip_addr"]
    """조회IP주소"""
    cpbc_ordp_ord_rcit_dvsn_cd: str = KisString["cpbc_ordp_ord_rcit_dvsn_cd"]
    """전산주문표주문접수구분코드"""
    cpbc_ordp_infm_mthd_dvsn_cd: str = KisString["cpbc_ordp_infm_mthd_dvsn_cd"]
    """전산주문표통보방법구분코드"""
    infm_tmd: str = KisString["infm_tmd"]
    """통보시각"""
    ctac_tlno: str = KisString["ctac_tlno"]
    """연락전화번호"""
    prdt_type_cd: str = KisString["prdt_type_cd"]
    """상품유형코드"""
    excg_dvsn_cd: str = KisString["excg_dvsn_cd"]
    """거래소구분코드"""
    cpbc_ordp_mtrl_dvsn_cd: str = KisString["cpbc_ordp_mtrl_dvsn_cd"]
    """전산주문표자료구분코드"""
    ord_orgno: str = KisString["ord_orgno"]
    """주문조직번호"""
    rsvn_ord_end_dt: date = KisDate["rsvn_ord_end_dt"]
    """예약주문종료일자"""
    excg_id_dvsn_Cd: str = KisString["excg_id_dvsn_Cd"]
    """거래소ID구분코드"""
    stpm_cndt_pric: Decimal = KisDecimal["stpm_cndt_pric"]
    """스톱지정가조건가격"""
    stpm_efct_occr_dtmd: str = KisString["stpm_efct_occr_dtmd"]
    """스톱지정가효력발생상세시각"""
    tot_ord_qty: int = KisInt["tot_ord_qty"]
    """총주문수량"""
    prsm_tlex_smtl: Decimal = KisDecimal["prsm_tlex_smtl"]
    """총체결금액"""
    pchs_avg_pric: Decimal = KisDecimal["pchs_avg_pric"]
    """추정제비용합계"""


class KisInquireDailyCcld(KisAPIResponse):
    """inquire_daily_ccld 응답"""

    __path__ = None

    output1: list[KisInquireDailyCcldOutput1Item] = KisList(KisInquireDailyCcldOutput1Item)["output1"]
    """output1 목록"""

    output2: KisInquireDailyCcldOutput2Item = KisObject(KisInquireDailyCcldOutput2Item)["output2"]
    """output2 (단건)"""


# 타입을 추정하지 못해 KisString 으로 둔 필드 13개:
#   ord_gno_brno, odno, orgn_odno, pdno, ord_tmd, avg_prvs
#   ordr_empno, inqr_ip_addr, infm_tmd, ctac_tlno, ord_orgno, excg_id_dvsn_Cd
#   stpm_efct_occr_dtmd
# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.
# 실제 응답을 보고 승격하세요.

# ⚠️ 이 응답은 블록이 2개입니다: output1, output2
#    원본의 COLUMN_MAPPING 은 블록을 나누지 않으므로 위 항목 클래스들이
#    같은 필드 집합을 공유합니다. 실제 응답을 보고 갈라내세요.
