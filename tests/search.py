import logging
from typing import get_args
from pykis import PyKis, KisAPIError
from pykis.scope.market.api.response import PRDT_TYPES, PRDT_TYPE_CD

with open("B:\\vack.txt", "r") as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True,
)

kis.logger.setLevel(logging.WARN)

print("[ 상품 정보 조회 ]\n")

while True:
    for i, prdt_type in enumerate(PRDT_TYPES.values()):
        print(f"{i + 1}. {prdt_type}".ljust(15), end="\t" if not i or i % 5 else "\n")

    prdt_type = get_args(PRDT_TYPE_CD)[int(input("\n상품 유형 번호를 선택하세요: ")) - 1]
    pdno = input("상품번호를 입력하세요 ex) 000660: ")

    if not pdno:
        break

    try:
        info = kis.market.info(pdno=pdno, prdt_type_cd=prdt_type)
    except KisAPIError as e:
        if e.rt_cd == 7:
            print("상품 정보가 없습니다.")
        else:
            print(e)
        print()
        continue

    print(f"\n--- {info.prdt_abrv_name} 상품 정보 ---")
    print(f"상품명: {info.prdt_name} / {info.prdt_eng_name}")
    print(f"분류: {info.prdt_clsf_name} / {info.ivst_prdt_type_cd_name}")
    print(f"등록일: {info.frst_erlm_dt}")
    print(f"--- {info.prdt_abrv_name} 상품 정보 ---\n")
