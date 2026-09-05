from types import SimpleNamespace

from requests import Response

from vmkis.responses.exceptions import KisMarketNotOpenedError, KisNotFoundError


def make_response_with_request(
    method="GET", url="https://api.example/test?x=1", headers=None, body: bytes | None = None
):
    r = Response()
    r.status_code = 400
    r.reason = "Bad Request"
    r._content = b'{"ok": false}'
    r.encoding = "utf-8"
    # attach a minimal request-like object used by safe_request_data
    req = SimpleNamespace()
    req.method = method
    req.url = url
    req.headers = headers or {}
    req.body = body
    r.request = req
    # allow headers on response (used by KisAPIError)
    r.headers = {}
    return r


def test_kis_not_found_error_defaults_and_fields():
    resp = make_response_with_request()
    data = {"a": 1}
    fields = {"id": 123, "name": "x"}

    err = KisNotFoundError(data=data, response=resp, fields=fields)

    # data preserved and response/status_code set
    assert err.data is data
    assert err.response is resp
    assert err.status_code == resp.status_code

    # message contains the default text and the formatted fields
    msg = str(err)
    assert "KIS API 요청한 자료가 존재하지 않습니다." in msg
    assert "id=123" in msg and "name='x'" in msg


def test_kis_not_found_error_custom_message():
    resp = make_response_with_request()
    data = {"k": "v"}
    err = KisNotFoundError(data=data, response=resp, message="custom", fields={})

    assert err.data is data
    assert "custom" in str(err)


def test_kis_market_not_opened_error_and_api_error_properties():
    # prepare response with headers and a request containing sensitive headers/body
    headers = {"appkey": "SECRET", "Authorization": "Bearer TOKEN"}
    body = b"param=1&secretkey=zzz"
    resp = make_response_with_request(method="POST", url="https://api.example/do?y=2", headers=headers, body=body)
    # set response-level headers used by KisAPIError
    resp.headers = {"tr_id": "TRX", "gt_uid": "GID"}

    data = {"rt_cd": "200", "msg_cd": "MKTCL", "msg1": " market not open "}

    err = KisMarketNotOpenedError(data=data, response=resp)

    # underlying data and parsed numeric rt_cd
    assert err.data == data
    assert err.rt_cd == 200
    assert err.msg_cd == "MKTCL"
    # msg1 is stripped in constructor
    assert err.msg1 == "market not open"

    # properties
    assert err.message == "market not open"
    assert err.code == 200
    assert err.error_code == "MKTCL"
    assert err.transaction_id == "TRX"
    assert err.transaction_unique_id == "GID"

    # string representation contains RT_CD and request details
    s = str(err)
    assert "RT_CD: 200" in s or "RT_CD: 200" in s
    assert "[  Request  ]: POST" in s

    # safe_request_data should have masked the appkey and Authorization in headers shown in message
    assert "***" in s
