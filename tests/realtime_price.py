from logging import DEBUG
from pykis import PyKis, KisRTPrice, KisRTClient, KisRTConclude

with open('B:\\vack.txt', 'r') as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True
)

kis.logger.setLevel(DEBUG)

stock = kis.market.stock_search_one('하이닉스')

if not stock:
    print('주식 정보를 찾을 수 없습니다.')
    exit(1)

stock = kis.stock(stock)
info = stock.info

print(f'{info.mksc_shrn_iscd} \t{info.hts_kor_isnm} \t시총: {info.prdy_avls_scal:,}억 구분: {info.avls_scal_cls_name} \t영업이익: {info.bsop_prfi:,}억')

def on_cntg(cli: KisRTClient, res: KisRTPrice):
    print(f'시간: {res.stck_cntg_hour.strftime("%H:%M:%S")}', end=' ')
    print(f'현재가: {res.stck_prpr:,}', end=' ')
    print(f'전일대비: {res.prdy_vrss:,}', end=' ')
    print(f'전일대비율: {res.prdy_ctrt:.2f}%', end=' ')
    print(f'거래량: {res.acml_vol:,}', end=' ')
    print(f'거래대금: {res.acml_tr_pbmn:,}')

def on_oder(cli: KisRTClient, res: KisRTConclude):
    print(f'{res.acnt_no} {res.acpt_yn_name} {res.cntg_isnm} {res.cntg_yn_name} {res.order_kind_name}', end=' ')
    print(f'수량: {res.oder_qty:,}', end=' ')
    print(f'가격: {res.cntg_unpr:,}')


kis.rtclient.event.cntg.add(on_cntg)
kis.rtclient.event.oder.add(on_oder)

stock.rt_add('체결가')

# kis.rtclient.add('체결', 'kth****') # 한국투자증권 로그인 ID (HTS ID)

# 체결가: KisRTPrice
# 호가: KisRTAskingPrice
# 체결: KisRTConclude


# import threading, time

# def disconnect():
#     time.sleep(10)
#     kis.rtclient.ws.close()
#     time.sleep(10)
#     kis.rtclient.ws.sock.close()


# threading.Thread(target=disconnect).start()


input('[ENTER]를 누르면 종료합니다.\n')

