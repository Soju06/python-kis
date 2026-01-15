from __future__ import annotations

from docsgen.parsers.master_sources import normalize_header_url, parse_master_contents_body


SAMPLE_HTML = """
<div class="conts-area-item">
  <h2 class="cont-tit">국내</h2>
  <table class="data-table">
    <tbody>
      <tr>
        <th rowspan="2" scope="row">국내주식</th>
        <td class="align-center"><a href="https://example.com/kospi_code.mst.zip">코스피</a></td>
        <td class="align-center">
          <a href="https://github.com/org/repo/blob/main/stocks_info/kospi.h">헤더정보</a>
        </td>
      </tr>
      <tr>
        <td class="align-center"><a href="https://example.com/kosdaq_code.mst.zip">코스닥</a></td>
        <td class="align-center">
          <a href="https://github.com/org/repo/blob/main/stocks_info/kosdaq.h">헤더정보</a>
        </td>
      </tr>
    </tbody>
  </table>
</div>
"""


def test_parse_master_contents_body() -> None:
    sources = parse_master_contents_body(SAMPLE_HTML)
    assert len(sources) == 2
    assert sources[0].group == "국내주식"
    assert sources[0].label == "코스피"
    assert sources[0].download_url == "https://example.com/kospi_code.mst.zip"
    assert sources[0].header_url == "https://raw.githubusercontent.com/org/repo/main/stocks_info/kospi.h"
    assert sources[1].group == "국내주식"


def test_normalize_header_url() -> None:
    url = "https://github.com/org/repo/blob/main/stocks_info/sample.h"
    assert normalize_header_url(url) == "https://raw.githubusercontent.com/org/repo/main/stocks_info/sample.h"
