from prettytable import PrettyTable
from pykis import PyKis

with open('B:\\ack.txt', 'r') as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

with open('B:\\acco.txt', 'r') as f:
    ACCOUNT_NO = f.readline().strip()

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=False,
    # 실시간 조회 비활성화
    realtime=False
)

# 잔고
account = kis.account(ACCOUNT_NO) # 계좌번호 ex) 50071022-01 또는 5007102201

table = PrettyTable(field_names=[
        '상품번호',
        '상품명',
        '보유수량',
        '매입금액',
        '현재가',
        '평가손익율',
        '평가손익',
    ],
    align='r',
)

balance = account.balance_all()

print(f'예수금: {balance.dnca_tot_amt:,}원 평가금: {balance.tot_evlu_amt:,} 손익: {balance.evlu_pfls_smtl_amt:,}원')

for stock in balance.stocks:
    table.add_row([
        stock.pdno,
        stock.prdt_name,
        f'{stock.hldg_qty:,}주',
        f'{stock.pchs_amt:,}원',
        f'{stock.prpr:,}원',
        f'{stock.evlu_pfls_rt:.2f}%',
        f'{stock.evlu_pfls_amt:,}원',
    ])

print(table)

profit = account.profit()

# FM 대로 사용 다한 임시 토큰은 삭제함.
if kis.client.token:
    kis.client.token.discard()
