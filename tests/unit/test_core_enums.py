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
    description = "1:0:종합 2:F:거래소 2:G:코스닥"

    entries = parse_enum_entries(description)
    values = [entry.code for entry in entries]

    assert "F" in values
    assert "G" in values


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


def test_parse_enum_entries_parses_label_code_pairs() -> None:
    description = "KRX : J , NXT : NX, 통합 : UN"

    values = parse_enum_values(description)

    assert "J" in values
    assert "NX" in values
    assert "UN" in values


def test_parse_enum_entries_does_not_reverse_code_label_pairs() -> None:
    description = "J: KRX, NX: NXT, UN: 통합"

    values = parse_enum_values(description)

    assert "J" in values
    assert "NX" in values
    assert "UN" in values
    assert "KRX" not in values


def test_parse_enum_entries_skips_long_label_value_after_korean_label() -> None:
    description = "공백: KOSPI200\nMKI: 미니KOSPI200\nWKM: KOSPI200위클리(월)"

    values = parse_enum_values(description)

    assert "MKI" in values
    assert "WKM" in values
    assert "KOSPI200" not in values


def test_parse_enum_entries_ignores_example_label_pairs() -> None:
    description = "Ticker 코드 ex: NAS, NYS, AMS"

    values = parse_enum_values(description)

    assert values == []


def test_parse_enum_entries_filters_metadata_key_tokens() -> None:
    description = "prdt_dvsn(상품구분) : 직원용 데이터(Type: String, Length:2)"

    values = parse_enum_values(description)

    assert "Type" not in values
    assert "Length" not in values
    assert values == []


def test_parse_enum_entries_ignores_instruction_sentence_tokens() -> None:
    description = "TTS6058R 조회 시 해당 주문번호(odno)의 ord_gno_brno 입력"

    values = parse_enum_values(description)

    assert values == []


def test_parse_enum_entries_ignores_collapsed_keyword_code() -> None:
    description = "1:FGHIN:공시 2:F:거래소 2:G:코스닥"

    values = parse_enum_values(description)

    assert "FGHIN" not in values
    assert "F" in values
    assert "G" in values
