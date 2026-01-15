from __future__ import annotations

from docsgen.parsers.master_headers import parse_header_structs


HEADER_TEXT = """
/* header */
#define IGNORED 1

typedef struct
{
    char    code[SZ_SHRNCODE]; /* 단축코드 */
    char    name[4+1]; // 이름
    char    desc[2]; /* main */
                            /* extra1 */
                            /* extra2 */
} ST_TEST;

struct sample {
    char foo[3]; /* foo */
    char bar[2+1]; /* bar */
};
"""

HEADER_MULTILINE = """
typedef struct {
    char a[1]; /* a */
    /* a1 */

    /* a2 */
    char b[1]; /* b */
    // b2
    char c[2]; /* c */
} ST_MULTI;
"""


def test_parse_header_structs() -> None:
    structs = parse_header_structs(HEADER_TEXT, "https://example.com/header.h")
    assert {struct.name for struct in structs} == {"ST_TEST", "sample"}

    test_struct = next(item for item in structs if item.name == "ST_TEST")
    assert test_struct.record_length == 9 + 5 + 2

    code_field = test_struct.fields[0]
    assert code_field.length == 9
    assert code_field.length_source == "SZ_SHRNCODE"
    assert code_field.description == "단축코드"

    name_field = test_struct.fields[1]
    assert name_field.length == 5
    assert name_field.length_source == "4+1"
    assert name_field.description == "이름"

    desc_field = test_struct.fields[2]
    assert desc_field.description == "main\nextra1\nextra2"


def test_multiline_comments_do_not_leak() -> None:
    structs = parse_header_structs(HEADER_MULTILINE, "https://example.com/header2.h")
    multi = next(item for item in structs if item.name == "ST_MULTI")

    a_field = multi.fields[0]
    b_field = multi.fields[1]
    c_field = multi.fields[2]

    assert a_field.description == "a\na1\na2"
    assert b_field.description == "b\nb2"
    assert c_field.description == "c"
