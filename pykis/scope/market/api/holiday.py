from datetime import date
from ._import import *


def holiday(
    self: "KisMarketClient",
    date: date | datetime | str | None = None,
    page: KisZeroPage = KisZeroPage.first(),
    format: str = "%Y%m%d",
) -> "KisMarketHolidays":
    """국내 휴장일 조회

    Args:
        date (date | datetime | str, optional): 조회 일자. 생략 시 오늘 날짜가 사용됩니다.
        format (str, optional): 날짜 포맷. Defaults to '%Y%m%d'.
        page (KisZeroPage, optional): 페이지. Defaults to KisZeroPage.first().
    """
    if isinstance(date, datetime):
        date = date.date()
    elif isinstance(date, str):
        date = datetime.strptime(date, format).date()
    elif date is None:
        date = datetime.now().date()

    return self.client.request(
        "get",
        "/uapi/domestic-stock/v1/quotations/chk-holiday",
        headers={"tr_id": "CTCA0903R"},
        params=page.build_body(
            {
                "BASS_DT": date.strftime("%Y%m%d"),
            }
        ),
        response=KisMarketHolidays,
        domain_type="real",
    )


# def holidays(
#     self: 'KisMarketClient',
#     date: date | datetime | str | None = None,
#     format: str = '%Y%m%d',
#     page: KisZeroPage = KisZeroPage.first(),
#     count: int | None = 5
# ) -> Iterable['KisMarketHolidays']:
#     '''국내 휴장일 조회

#     Args:
#         date (date | datetime | str, optional): 조회 일자. 생략 시 오늘 날짜가 사용됩니다.
#         format (str, optional): 날짜 포맷. Defaults to '%Y%m%d'.
#         page (KisZeroPage, optional): 페이지. Defaults to KisZeroPage.first().
#         count (int, optional): 조회할 개수. Defaults to None.
#     '''

#     return KisMarketHolidays.iterable(
#         holiday,
#         args=(self,),
#         kwargs={
#             'date': date,
#             'format': format,
#         },
#         page=page,
#         count=count
#     )

# def holiday_all(
#     self: 'KisMarketClient',
#     date: date | datetime | str | None = None,
#     format: str = '%Y%m%d',
#     page: KisZeroPage = KisZeroPage.first(),
#     count: int | None = 5
# ) -> 'KisMarketHolidays':
#     '''국내 휴장일 조회

#     Args:
#         date (date | datetime | str, optional): 조회 일자. 생략 시 오늘 날짜가 사용됩니다.
#         format (str, optional): 날짜 포맷. Defaults to '%Y%m%d'.
#         page (KisZeroPage, optional): 페이지. Defaults to KisZeroPage.first().
#         count (int, optional): 조회할 개수. Defaults to None.
#     '''

#     return KisMarketHolidays.join(holidays(
#         self,
#         date=date,
#         format=format,
#         page=page,
#         count=count
#     ))
