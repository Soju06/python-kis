from __future__ import annotations

from docsgen.parsers.error_codes import parse_error_code_contents_body


def test_parse_error_code_contents_body_pairs() -> None:
    html = """
    <div class="conts-area-item">
      <h2 class="cont-tit">EGW서버</h2>
      <table class="data-table">
        <tbody>
          <tr>
            <th scope="row">EGW00001</th><td>일시적 오류</td>
            <th scope="row">EGW00002</th><td>서버 에러</td>
          </tr>
          <tr>
            <th scope="row">EGW00003</th><td>접근 거부</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="conts-area-item">
      <h2 class="cont-tit">OPSQ서버</h2>
      <table class="data-table">
        <tbody>
          <tr>
            <th>OPSQ0001</th><td>호출 전처리 오류</td>
            <th>OPSQ0002</th><td>없는 서비스 코드</td>
          </tr>
        </tbody>
      </table>
    </div>
    """

    entries = parse_error_code_contents_body(html)
    assert [(e.category, e.code, e.message) for e in entries] == [
        ("EGW서버", "EGW00001", "일시적 오류"),
        ("EGW서버", "EGW00002", "서버 에러"),
        ("EGW서버", "EGW00003", "접근 거부"),
        ("OPSQ서버", "OPSQ0001", "호출 전처리 오류"),
        ("OPSQ서버", "OPSQ0002", "없는 서비스 코드"),
    ]


