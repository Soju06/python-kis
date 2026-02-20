from __future__ import annotations

from codegen.core.enums import parse_enum_entries, parse_enum_values


def test_parse_enum_entries_builds_bitwise_combinations_for_market_phase_code() -> None:
    description = """' '00' : 장전 예상체결가와 장마감 동시호가
'49' : 장후 예상체결가

(1) 첫 번째 비트
1 : 장개시전
2 : 장중
3 : 장종료후
4 : 시간외단일가
7 : 일반Buy-in
8 : 당일Buy-in
(2) 두 번째 비트
0 : 보통
1 : 종가
2 : 대량
3 : 바스켓
7 : 정리매매
8 : Buy-in'"""

    values = parse_enum_values(description)

    assert "00" in values
    assert "49" in values
    assert "20" in values
    assert "31" in values
    assert "78" in values
    assert "1" not in values
    assert "0" not in values
    assert "Buy" not in values
    assert "in" not in values


def test_parse_enum_entries_keeps_non_bitwise_pairs() -> None:
    description = "1:0:종합 1:FGHIN:공시 2:F:거래소"

    entries = parse_enum_entries(description)
    values = [entry.code for entry in entries]

    assert "FGHIN" in values
    assert "F" in values


def test_parse_enum_entries_builds_prefixed_subcodes() -> None:
    description = """1:S:컨슈머타임스
3:01:종합
3:02:파이낸셜컨슈머
1:d:NSP통신
3:11:IT/과학"""

    values = parse_enum_values(description)

    assert "S01" in values
    assert "S02" in values
    assert "d11" in values
