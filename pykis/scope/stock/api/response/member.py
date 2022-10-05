from ...._import import *

class KisStockMember:
    seln_mbcr_no: str
    '''매도 회원사 번호'''
    seln_mbcr_name: str
    '''매도 회원사 명'''
    total_seln_qty: int
    '''총 매도 수량'''
    seln_mbcr_rlim: float
    '''매도 회원사 비중'''
    seln_qty_icdc: int
    '''매도 수량 증감'''
    shnu_mbcr_no: str
    '''매수2 회원사 번호'''
    shnu_mbcr_name: str
    '''매수2 회원사 명'''
    total_shnu_qty: int
    '''총 매수2 수량'''
    shnu_mbcr_rlim: float
    '''매수2 회원사 비중'''
    shnu_qty_icdc: int
    '''매수2 수량 증감'''
    seln_mbcr_glob_yn: bool
    '''매도 회원사 외국계 여부'''
    shnu_mbcr_glob_yn: bool
    '''매수2 회원사 외국계 여부'''

    def __init__(self, data: dict, number: int):
        self.seln_mbcr_no = data[f'seln_mbcr_no{number}']
        self.seln_mbcr_name = data[f'seln_mbcr_name{number}']
        self.total_seln_qty = int(data[f'total_seln_qty{number}'])
        self.seln_mbcr_rlim = float(data[f'seln_mbcr_rlim{number}'])
        self.seln_qty_icdc = int(data[f'seln_qty_icdc{number}'])
        self.shnu_mbcr_no = data[f'shnu_mbcr_no{number}']
        self.shnu_mbcr_name = data[f'shnu_mbcr_name{number}']
        self.total_shnu_qty = int(data[f'total_shnu_qty{number}'])
        self.shnu_mbcr_rlim = float(data[f'shnu_mbcr_rlim{number}'])
        self.shnu_qty_icdc = int(data[f'shnu_qty_icdc{number}'])
        self.seln_mbcr_glob_yn = data[f'seln_mbcr_glob_yn_{number}'] == 'Y'
        self.shnu_mbcr_glob_yn = data[f'shnu_mbcr_glob_yn_{number}'] == 'Y'


class KisStockMembers(KisDynamicAPIResponse):
    glob_total_seln_qty: int
    '''외국계 총 매도 수량'''
    glob_seln_rlim: float
    '''외국계 매도 비중'''
    glob_ntby_qty: int
    '''외국계 순매수 수량'''
    glob_total_shnu_qty: int
    '''외국계 총 매수2 수량'''
    glob_shnu_rlim: float
    '''외국계 매수2 비중'''
    glob_total_seln_qty_icdc: int
    '''외국계 총 매도 수량 증감'''
    glob_total_shnu_qty_icdc: int
    '''외국계 총 매수2 수량 증감'''
    acml_vol: int
    '''누적 거래량'''
    members: list[KisStockMember]
    '''회원사별 매매 현황'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        data = data['output']
        self.members = [KisStockMember(data, i) for i in range(1, 6)]
