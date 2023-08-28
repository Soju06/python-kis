from ...._import import *

OVERSEAS_ORD_DVSNS = {
    '00': '지정가',
    '31': '장개시시장가',
    '32': '장개시지정가',
    '33': '장마감시장가',
    '34': '장마감지정가',
    '05': '단주지정가'
}

OVERSEAS_R_ORD_DVSNS = {
    '지정가': '00',
    '장개시시장가': '31',
    '장개시지정가': '32',
    '장마감시장가': '33',
    '장마감지정가': '34',
    '단주지정가': '05'
}

OVERSEAS_ORD_DVSN_TYPE = Literal[
    '00', '31', '32', '33', '34',
    '지정가', '장개시시장가', '장개시지정가', '장마감시장가', '장마감지정가',
    '05', '단주지정가'
] | None

# [Header tr_id TTTT1002U(미국 매수 주문)]
# 00 : 지정가
# 32 : LOO(장개시지정가)
# 34 : LOC(장마감지정가)
# * 모의투자 VTTT1002U(미국 매수 주문)로는 00:지정가만 가능

# [Header tr_id TTTT1006U(미국 매도 주문)]
# 00 : 지정가
# 31 : MOO(장개시시장가)
# 32 : LOO(장개시지정가)
# 33 : MOC(장마감시장가)
# 34 : LOC(장마감지정가)
# * 모의투자 VTTT1006U(미국 매도 주문)로는 00:지정가만 가능

# [Header tr_id TTTS1001U(홍콩 매도 주문)]
# 00 : 지정가
# 50 : 단주지정가
# * 모의투자 VTTS1001U(홍콩 매도 주문)로는 00:지정가만 가능

# [그외 tr_id]
# 제거

OVERSEAS_ORD_DVSN_MAP: dict[str | None, set[str | None]] = {
    # 미국 매수 주문
    'TTTT1002U': {'00', '32', '34', '지정가', '장개시지정가', '장마감지정가'},
    'VTTT1002U': {'00', '지정가'},
    # 미국 매도 주문
    'TTTT1006U': {'00', '31', '32', '33', '34', '지정가', '장개시시장가', '장개시지정가', '장마감시장가', '장마감지정가'},
    # Issue #15: 미국 모의투자 매도 주문 Id는 VTTT1006U이 아닌 VTTT1001U
    # Docs도 매우 난해하다.
    'VTTT1001U': {'00', '지정가'},
    # 홍콩 매도 주문
    'TTTS1001U': {'00', '50', '지정가', '단주지정가'},
    'VTTS1001U': {'00', '지정가'},
    None: {None}
}

OVERSEAS_OVRS_EXCGS = {
    'NASD': '나스닥',
    'NYSE': '뉴욕',
    'AMEX': '아멕스',
    'SEHK': '홍콩',
    'SHAA': '상해',
    'SZAA': '심천',
    'TKSE': '일본',
    'HASE': '하노이',
    'VNSE': '호치민',
}

OVERSEAS_R_OVRS_EXCGS = {
    '나스닥': 'NASD',
    '뉴욕': 'NYSE',
    '아멕스': 'AMEX',
    '홍콩': 'SEHK',
    '상해': 'SHAA',
    '심천': 'SZAA',
    '일본': 'TKSE',
    '하노이': 'HASE',
    '호치민': 'VNSE',
}

OVERSEAS_OVRS_EXCG_CD = Literal[
    'NASD', '나스닥',
    'NYSE', '뉴욕',
    'AMEX', '아멕스',
    'SEHK', '홍콩',
    'SHAA', '상해',
    'SZAA', '심천',
    'TKSE', '일본',
    'HASE', '하노이',
    'VNSE', '호치민',
]
