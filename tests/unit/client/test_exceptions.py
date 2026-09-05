from types import SimpleNamespace

from requests import Response

from vmkis.client import exceptions
from vmkis.client.exceptions import KisAPIError, KisHTTPError, safe_request_data


def make_response_with_request(
    method: str = "GET", url: str = "https://api.test/path?foo=bar", headers: dict | None = None, body=None
) -> Response:
    r = Response()
    r.status_code = 400
    r.reason = "Bad Request"
    # set raw content so Response.text property works
    r._content = b"error"
    r.encoding = "utf-8"
    if headers is None:
        headers = {}
    # attach a simple request-like object
    req = SimpleNamespace()
    req.method = method
    req.url = url
    req.headers = headers
    req.body = body
    r.request = req
    return r


def test_safe_request_data_masks_sensitive_headers_and_body(monkeypatch):
    # ensure TRACE_DETAIL_ERROR is False to trigger body masking
    monkeypatch.setattr(exceptions, "TRACE_DETAIL_ERROR", False)

    headers = {
        "appkey": "MYAPP",
        "appsecret": "MYSECRET",
        "Authorization": "Bearer tok",
        "X": "y",
    }

    body = b"a=1&appkey=MYAPP&secretkey=SECRETS"
    resp = make_response_with_request(method="POST", url="https://api.test/path?x=1&y=2", headers=headers, body=body)

    s = safe_request_data(resp)

    # headers masked
    assert s.header["appkey"] == "***"
    assert s.header["appsecret"] == "***"
    assert s.header["Authorization"] == "Bearer ***"

    # body masked because it contains sensitive keys and TRACE_DETAIL_ERROR is False
    assert s.body == "[PROTECTED BODY]"

    # params should show parsed query string (as string form)
    assert "x" in s.params and "y" in s.params

    # url should have query removed
    assert s.url.geturl().endswith("/path")


def test_safe_request_data_decodes_memoryview_body():
    body = memoryview(b"hello=1")
    resp = make_response_with_request(body=body)
    s = safe_request_data(resp)
    assert s.body == "hello=1"


def test_kis_http_error_contains_redacted_request_info():
    headers = {"appkey": "A", "Authorization": "Bearer tok"}
    resp = make_response_with_request(method="DELETE", url="https://host/api?z=9", headers=headers, body=b"payload")
    resp.status_code = 500
    resp.reason = "Server Error"
    resp._content = b"server failed"
    resp.encoding = "utf-8"

    err = KisHTTPError(resp)
    # status and reason captured
    assert err.status_code == 500
    assert err.reason == "Server Error"

    msg = str(err)
    # should include masked headers and not reveal raw appkey value in headers
    assert "***" in msg
    assert "'appkey': 'A'" not in msg
    assert "Request" in msg


def test_kis_api_error_properties_and_defaults():
    data = {"rt_cd": "123", "msg_cd": "E100", "msg1": " problem occurred "}
    resp = make_response_with_request(headers={})
    resp.headers = {"tr_id": "TRX1", "gt_uid": "GID1"}

    e = KisAPIError(data, resp)
    assert e.data == data
    assert e.code == 123
    assert e.error_code == "E100"
    assert e.message == "problem occurred"
    assert e.transaction_id == "TRX1"
    assert e.transaction_unique_id == "GID1"

    # missing fields -> defaults
    resp2 = make_response_with_request()
    resp2.headers = {}
    e2 = KisAPIError({}, resp2)
    assert e2.code == 0
    assert e2.error_code == "UNKNOWN"
    assert e2.transaction_id == "UNKNOWN"
    assert e2.transaction_unique_id == "UNKNOWN"
