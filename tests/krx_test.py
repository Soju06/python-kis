from prettytable import PrettyTable
from pykis.utlis import *

table = PrettyTable(field_names=[
        '순위',
        '종목코드',
        '종목명',
        '등락율',
        '거래량',
        '거래대금(만)'
    ],
    align='r',
)

def add_split(name: str):
    table.add_row([
        '- - - -' if e != 0 else name for e in range(len(table.field_names))
    ])

def add_rank(rank: list, p: bool = False):
    for i, item in enumerate(rank):
        item: KRXRank

        table.add_row([
            i+1,
            item.isu_cd,
            item.isu_abbrv,
            item.fluc_rt,
            item.acc_trdvol,
            item.acc_trdval / 10000 if p else item.acc_trdval // 10000
        ])


rank = KRXLimitRank.fetch(table='상한가')[:8]
add_split('상한가')
add_rank(rank)

rank = KRXLimitRank.fetch(table='하한가')[:8]
add_split('하한가')
add_rank(rank)

rank = KRXFluctRank.fetch(table='상승')[:8]
add_split('상승순위')
add_rank(rank)

rank = KRXFluctRank.fetch(table='하락')[:8]
add_split('하락순위')
add_rank(rank, p=True)

add_split('거래상위')
rank = KRXFluctRank.fetch(table='거래상위')[:8]
add_rank(rank)


print(table)
