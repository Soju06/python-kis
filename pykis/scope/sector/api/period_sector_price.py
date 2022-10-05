# import requests
# from datetime import datetime
# from typing import TYPE_CHECKING, Literal
# from ...responses import KisDynamicAPIResponse, KisDynamic

# if TYPE_CHECKING:
#     from ....kis import PyKis

# def period_sector_price(
#     self: 'PyKis',
#     div: str,
#     code: str,
#     start_date: datetime,
#     end_date: datetime,
#     period: Literal['day', 'week', 'month', 'year'] = 'day',
# ) -> 'KisStockSectorPrices':
#     '''업종별 주식기간봉을 조회합니다.
#     업종구분과 업종코드는 https://new.real.download.dws.co.kr/common/master/idxcode.mst.zip 에서 확인할 수 있습니다. (KIS Developers > 포럼 > 종목정보 다운로드 > 업종코드)

#     Examples:
#         업종코드 구분 예시:
#             19101 (앞 5자리) -> div: 1 (앞 1자리), code: 9101 (div 다음 4자리)
#         >>> kis.period_sector_price('1', '9101', datetime(2022, 1, 1), datetime.now())

#     Args:
#         div: 업종구분
#         code: 업종코드
#         start_date: 시작일
#         end_date: 종료일
#         period: 기간. 기본값은 일봉.
#     '''
#     if len(div) != 1:
#         raise ValueError('업종구분은 1자리입니다.')
#     if len(code) != 4:
#         raise ValueError('업종코드는 4자리입니다.')

#     return self.client.request(
#         'get',
#         '/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice',
#         headers={
#             'tr_id': 'FHKUP03500100'
#         },
#         params={
#             'FID_COND_MRKT_DIV_CODE': 'U',
#             "fid_input_iscd": code,
#             "fid_period_div_code": div,
#             'FID_INPUT_DATE_1': start_date.strftime('%Y%m%d'),
#             'FID_INPUT_DATE_2': end_date.strftime('%Y%m%d'),
#             'FID_PERIOD_DIV_CODE': 'D' if period == 'day' else 'W' if period == 'week' else 'M' if period == 'month' else 'Y',
#         },
#         response=KisStockSectorPrices
#     )
    
# class KisStockSectorPrice(KisDynamic):
# # -STCK_BSOP_DATE	영업 일자	String	Y	8	영업 일자
# # -BSTP_NMIX_PRPR	업종 지수 현재가	String	Y	10	업종 지수 현재가
# # -BSTP_NMIX_OPRC	업종 지수 시가	String	Y	10	업종 지수 시가
# # -BSTP_NMIX_HGPR	업종 지수 최고가	String	Y	10	업종 지수 최고가
# # -BSTP_NMIX_LWPR	업종 지수 최저가	String	Y	10	업종 지수 최저가
# # -ACML_VOL	누적 거래량	String	Y	18	누적 거래량
# # -ACML_TR_PBMN	누적 거래 대금	String	Y	18	누적 거래 대금
# # -MOD_YN	변경 여부	String	Y	1	변경 여부
#     stck_bsop_date: datetime
#     '''영업 일자'''
#     bstp_nmix_prpr: float
#     '''업종 지수 현재가'''
#     bstp_nmix_oprc: float
#     '''업종 지수 시가'''
#     bstp_nmix_hgpr: float
#     '''업종 지수 최고가'''
#     bstp_nmix_lwpr: float
#     '''업종 지수 최저가'''
#     acml_vol: int
#     '''누적 거래량'''
#     acml_tr_pbmn: int
#     '''누적 거래 대금'''
#     mod_yn: bool
#     '''변경 여부'''

#     def __init__(self, data: dict):
#         super().__init__(data)

    
# class KisStockSectorPrices(KisDynamicAPIResponse):
# # BSTP_NMIX_PRDY_VRSS	업종 지수 전일 대비	String	Y	14	업종 지수 전일 대비
# # PRDY_VRSS_SIGN	전일 대비 부호	String	Y	1	전일 대비 부호
# # BSTP_NMIX_PRDY_CTRT	업종 지수 전일 대비율	String	Y	11	업종 지수 전일 대비율
# # PRDY_NMIX	전일 지수	String	Y	14	전일 지수
# # ACML_VOL	누적 거래량	String	Y	18	누적 거래량
# # ACML_TR_PBMN	누적 거래 대금	String	Y	18	누적 거래 대금
# # HTS_KOR_ISNM	HTS 한글 종목명	String	Y	40	HTS 한글 종목명
# # BSTP_NMIX_PRPR	업종 지수 현재가	String	Y	10	업종 지수 현재가
# # BSTP_CLS_CODE	업종 구분 코드	String	Y	9	업종 구분 코드
# # PRDY_VOL	전일 거래량	String	Y	18	전일 거래량
# # BSTP_NMIX_OPRC	업종 지수 시가	String	Y	14	업종 지수 시가
# # BSTP_NMIX_HGPR	업종 지수 최고가	String	Y	14	업종 지수 최고가
# # BSTP_NMIX_LWPR	업종 지수 최저가	String	Y	14	업종 지수 최저가
# # FUTS_PRDY_OPRC	업종 전일 시가	String	Y	14	업종 전일 시가
# # FUTS_PRDY_HGPR	업종 전일 최고가	String	Y	14	업종 전일 최고가
# # FUTS_PRDY_LWPR	업종 전일 최저가	String	Y	14	업종 전일 최저가
#     bstp_nmix_prdy_vrss: float
#     '''업종 지수 전일 대비'''
#     prdy_vrss_sign: str
#     '''전일 대비 부호'''
#     bstp_nmix_prdy_ctr: float
#     '''업종 지수 전일 대비율'''
#     prdy_nmix: float
#     '''전일 지수'''
#     acml_vol: int
#     '''누적 거래량'''
#     acml_tr_pbmn: int
#     '''누적 거래 대금'''
#     hts_kor_isnm: str
#     '''HTS 한글 종목명'''
#     bstp_nmix_prpr: float
#     '''업종 지수 현재가'''
#     bstp_cls_code: str
#     '''업종 구분 코드'''
#     prdy_vol: int
#     '''전일 거래량'''
#     bstp_nmix_oprc: float
#     '''업종 지수 시가'''
#     bstp_nmix_hgpr: float
#     '''업종 지수 최고가'''
#     bstp_nmix_lwpr: float
#     '''업종 지수 최저가'''
#     futs_prdy_oprc: float
#     '''업종 전일 시가'''
#     futs_prdy_hgpr: float
#     '''업종 전일 최고가'''
#     futs_prdy_lwpr: float
#     '''업종 전일 최저가'''
#     prices: list[KisStockSectorPrice]

#     def __init__(self, data: dict, response: requests.Response):
#         super().__init__(data, response)
#         self.prices = [KisStockSectorPrice(price) for price in data['output2']]
