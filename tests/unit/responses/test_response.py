from types import SimpleNamespace

import pytest

from vmkis.client.exceptions import KisAPIError
from vmkis.responses.response import (
    KisPaginationAPIResponse,
    KisResponse,
    raise_not_found,
)


def test_raise_not_found_raises_with_response():
    resp = SimpleNamespace(status_code=404)
    data = {"__response__": resp}

    with pytest.raises(Exception) as excinfo:
        raise_not_found(data, message="not here", foo=1)

    err = excinfo.value
    # KisNotFoundError is subclass of Exception and stores response via exception
    assert hasattr(err, "response") and err.response is resp


def test_kis_response_raw_and_none():
    r = object.__new__(KisResponse)
    # when __data__ is None, raw() returns None
    r.__data__ = None
    assert r.raw() is None

    # when __data__ present, raw returns a copy without __response__
    resp = SimpleNamespace(status_code=200)
    r.__data__ = {"a": 1, "__response__": resp}
    out = r.raw()
    assert out == {"a": 1}


def test_kisresponse_pre_init_raises_on_nonzero_rtcd():
    r = object.__new__(KisResponse)
    # call __pre_init__ with rt_cd != 0 should raise KisAPIError
    req = SimpleNamespace(headers={}, method="GET", url="https://api/test?x=1", body=None)
    data = {"rt_cd": "1", "__response__": SimpleNamespace(status_code=500, headers={}, request=req)}
    with pytest.raises(KisAPIError):
        KisResponse.__pre_init__(r, data)

    # rt_cd == 0 should not raise
    req2 = SimpleNamespace(headers={}, method="GET", url="https://api/test?x=1", body=None)
    data2 = {"rt_cd": "0", "__response__": SimpleNamespace(status_code=200, headers={}, request=req2)}
    KisResponse.__pre_init__(r, data2)


def test_pagination_api_response_properties_and_has_next():
    p = object.__new__(KisPaginationAPIResponse)
    # is_last when page_status == 'end'
    p.page_status = "end"
    p.next_page = SimpleNamespace(is_empty=False)
    assert p.is_last is True
    # has_next false when page_status == 'end'
    assert p.has_next is False

    # other status and next_page empty
    p.page_status = "cont"
    p.next_page = SimpleNamespace(is_empty=True)
    assert p.is_last is False
    assert p.has_next is False

    # other status and next_page not empty -> True
    p.next_page = SimpleNamespace(is_empty=False)
    assert p.has_next is True
