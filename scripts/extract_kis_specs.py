#!/usr/bin/env python3
"""`examples_llm/` 에서 엔드포인트 **사실**을 추출합니다. (이슈 #21)

## 왜 이 파일이 여기 있는가

[#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 은 "AST 파서 400줄은
프로토타입 완성 상태"라고 적고 파싱률 98.9% 등의 수치를 근거로 삼았습니다.
**그 파서가 저장소에 없었습니다.** 숫자를 검증할 방법도 재현할 방법도 없어서
다시 만들었습니다. 중단 조건("파싱률 급락")을 판정하려면 잴 수 있어야 합니다.

## 무엇을 추출하는가 — 사실만

원본(`koreainvestment/open-trading-api`)에는 **LICENSE 파일이 없습니다.**
README 는 "참고용으로 제공"이라고만 적습니다. 그래서 이 스크립트는 **사실**만
꺼냅니다 — 경로, TR ID, 파라미터 이름, 응답 필드명과 한글 라벨.

**원문 docstring 설명문은 추출하지 않습니다.** 생성기는 라벨과 메타데이터로부터
자체 문장을 조립해야 합니다. `--dump-prose` 로 원문을 뽑는 기능은 **의도적으로
넣지 않았습니다.**

## 사용법

    python scripts/extract_kis_specs.py <examples_llm 경로> -o specs.json
    python scripts/extract_kis_specs.py <examples_llm 경로> --report
"""

from __future__ import annotations

import argparse
import ast
import json
import pathlib
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any

#: 엔드포인트가 아닌 폴더. auth 는 이 라이브러리가 자체 구현을 갖고 있습니다.
SKIP_DIRS = {"__pycache__", "auth"}

#: 헤더 주석의 `[v1_국내주식-047]` 같은 문서 코드.
_DOC_CODE = re.compile(r"\[([A-Za-z0-9_가-힣]+-\d+)\]")


#: `COLUMN_MAPPING` 이 실제 필드가 아니라 **껍데기 키**만 담은 경우.
#: `news_title` 이 `{'output1': '응답상세'}` 하나뿐입니다 — 파싱은 되지만
#: 필드를 하나도 주지 않으므로 성공으로 세면 안 됩니다.
WRAPPER_KEYS = {"output", "output1", "output2", "outblock1", "outblock2", "res"}


@dataclass
class EndpointSpec:
    category: str
    name: str
    #: "rest" | "websocket". 웹소켓은 `API_URL` 이 없는 것이 정상입니다.
    kind: str = "rest"
    path: str | None = None
    tr_ids: list[str] = field(default_factory=list)
    #: TR ID 마다 그것이 선택되는 조건. `{"env_dv": "real", "pd_dv": "before"}`.
    #: 조건 없이 하나뿐이면 빈 dict 하나입니다.
    tr_branches: list[dict[str, Any]] = field(default_factory=list)
    method: str = "GET"
    params: dict[str, str] = field(default_factory=dict)  # KIS 이름 -> 파이썬 인자
    required: list[str] = field(default_factory=list)
    optional: list[str] = field(default_factory=list)
    fields: dict[str, str] = field(default_factory=dict)  # 필드명 -> 한글 라벨
    numeric_fields: list[str] = field(default_factory=list)
    #: 응답 블록 이름 -> "list" | "single" | "unknown".
    #: KIS 는 한 응답에 output / output1 / output2 를 함께 담기도 합니다.
    #: 332개 중 32개가 블록 2개, 4개가 3개 이상입니다.
    output_blocks: dict[str, str] = field(default_factory=dict)
    #: 연속조회 커서 폭. `ctx_area_fk200` 이면 200. 없으면 페이징이 없습니다.
    page_size: int | None = None
    doc_code: str | None = None
    #: 완전 파싱 실패 사유. 비어 있으면 성공입니다.
    problems: list[str] = field(default_factory=list)
    #: 실패는 아니지만 생성기가 알아야 하는 것. 예: 껍데기 키를 걷어냄.
    warnings: list[str] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return not self.problems


def _module(path: pathlib.Path) -> ast.Module | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return None


def _str_assign(tree: ast.Module, name: str) -> str | None:
    """모듈 최상위 `NAME = "..."` 를 찾습니다."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        return node.value.value
    return None


def _dict_assign(tree: ast.Module, name: str) -> dict[str, str]:
    """모듈 최상위 `NAME = {...}` 을 문자열 쌍으로 읽습니다."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name and isinstance(node.value, ast.Dict):
                    out = {}
                    for k, v in zip(node.value.keys, node.value.values, strict=False):
                        if (
                            isinstance(k, ast.Constant)
                            and isinstance(k.value, str)
                            and isinstance(v, ast.Constant)
                            and isinstance(v.value, str)
                        ):
                            out[k.value] = v.value
                    return out
    return {}


def _list_assign(tree: ast.Module, name: str) -> list[str]:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name and isinstance(node.value, ast.List):
                    return [
                        e.value for e in node.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)
                    ]
    return []


def _main_function(tree: ast.Module, name: str) -> ast.FunctionDef | None:
    """엔드포인트 함수. 파일명과 같은 이름을 우선하고, 없으면 첫 함수를 씁니다."""
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    for f in funcs:
        if f.name == name:
            return f
    return funcs[0] if funcs else None


def _collect_tr_ids(func: ast.FunctionDef) -> list[str]:
    """`tr_id = "..."` 를 **전부** 모읍니다.

    `inquire_daily_ccld` 처럼 실전/모의 × 기간 4-way 분기가 있습니다.
    한 개만 집으면 그 분기를 통째로 잃습니다.
    """
    found: list[str] = []
    for node in ast.walk(func):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id == "tr_id"
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    found.append(node.value.value)
    # 순서를 지키면서 중복만 제거합니다.
    return list(dict.fromkeys(found))


#: 실전/모의를 가르는 축. 값이 `"real"`/`"demo"` 입니다.
#: 분기 조건에 쓰인 변수를 전수로 세면 `env_dv` 가 94회로 압도적입니다.
DOMAIN_AXIS = "env_dv"

#: `env_dv` 값 -> vmkis 도메인.
DOMAIN_VALUES = {"real": "live", "demo": "paper"}


def _predicate(test: ast.expr) -> tuple[str, str] | None:
    """`x == "y"` 를 `("x", "y")` 로. 그 밖의 형태는 `None`."""
    if (
        isinstance(test, ast.Compare)
        and len(test.ops) == 1
        and isinstance(test.ops[0], ast.Eq)
        and isinstance(test.left, ast.Name)
        and isinstance(test.comparators[0], ast.Constant)
        and isinstance(test.comparators[0].value, str)
    ):
        return test.left.id, test.comparators[0].value
    return None


def _collect_tr_branches(func: ast.FunctionDef) -> list[dict[str, Any]]:
    """TR ID 와 **그것이 선택되는 조건**을 함께 모읍니다.

    `inquire_daily_ccld` 가 이렇게 생겼습니다.

        if env_dv == "real":
            if pd_dv == "before":   tr_id = "CTSC9215R"
            elif pd_dv == "inner":  tr_id = "TTTC0081R"
        elif env_dv == "demo":
            if pd_dv == "before":   tr_id = "VTSC9215R"
            elif pd_dv == "inner":  tr_id = "VTTC0081R"

    조건을 버리고 TR ID 만 모으면 **4개 중 어느 것이 언제 쓰이는지 알 수
    없습니다.** 첫 판이 그랬고, 생성물은 첫 번째만 쓰고 나머지를 주석으로
    흘렸습니다.

    `ast` 에는 부모 링크가 없으므로 조건 스택을 들고 하향식으로 걷습니다.
    `else` 가지는 **조건을 특정할 수 없으므로** 그 사실을 그대로 남깁니다
    (`{...: None}`) — 추측해서 반대값을 넣으면 3분기 이상에서 틀립니다.
    """
    found: list[dict[str, Any]] = []

    def walk(nodes: list[ast.stmt], conditions: dict[str, Any]) -> None:
        for node in nodes:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                if any(isinstance(t, ast.Name) and t.id == "tr_id" for t in node.targets):
                    if isinstance(node.value.value, str):
                        found.append({"tr_id": node.value.value, "conditions": dict(conditions)})
                continue

            if isinstance(node, ast.If):
                pred = _predicate(node.test)
                taken = dict(conditions)
                if pred:
                    taken[pred[0]] = pred[1]
                walk(node.body, taken)

                # `else` / `elif`. elif 는 `orelse` 안의 If 로 표현됩니다.
                fallthrough = dict(conditions)
                if pred and not (len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If)):
                    # 순수 else 입니다. "pred 가 아니다"를 값으로 적을 수 없습니다.
                    fallthrough[pred[0]] = None
                walk(node.orelse, fallthrough)
                continue

            for attr in ("body", "orelse", "finalbody"):
                inner = getattr(node, attr, None)
                if isinstance(inner, list):
                    walk(inner, conditions)

    walk(func.body, {})

    # 같은 TR ID 가 여러 경로로 나오면 첫 경로만 남깁니다.
    seen: set[str] = set()
    unique = []
    for entry in found:
        if entry["tr_id"] not in seen:
            seen.add(entry["tr_id"])
            unique.append(entry)
    return unique


def _collect_params(func: ast.FunctionDef) -> dict[str, str]:
    """`params = {"KIS_NAME": python_arg, ...}` 을 읽습니다."""
    for node in ast.walk(func):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "params" and isinstance(node.value, ast.Dict):
                    out: dict[str, str] = {}
                    for k, v in zip(node.value.keys, node.value.values, strict=False):
                        if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
                            continue
                        out[k.value] = v.id if isinstance(v, ast.Name) else ast.unparse(v)
                    return out
    return {}


def _split_args(func: ast.FunctionDef) -> tuple[list[str], list[str]]:
    """필수(기본값 없음) / 선택(기본값 있음)."""
    args = [a.arg for a in func.args.args]
    n_default = len(func.args.defaults)
    required = args[: len(args) - n_default] if n_default else args
    optional = args[len(args) - n_default :] if n_default else []
    # 호출 배관용 인자는 KIS 파라미터가 아닙니다.
    plumbing = {"tr_cont", "dataframe", "self", "env_dv", "depth", "max_depth"}
    return (
        [a for a in required if a not in plumbing],
        [a for a in optional if a not in plumbing],
    )


#: 연속조회 커서. **폭 숫자가 없는 변형이 있습니다** — `CTX_AREA_FK` 처럼.
#: 처음에 `(\d+)` 로 적었다가 국내휴장일조회(`CTCA0903R`)를 통째로 놓쳤습니다.
#: #21 이 파일럿 항목으로 지목한 바로 그 엔드포인트입니다.
_CURSOR = re.compile(r"(?i)ctx_area_[fn]k(\d*)\b")

#: 접미사 없는 커서. `vmkis.client.page.NO_SUFFIX` 와 같은 값이어야 합니다
#: (#16 이 `KisPage` 에 도입했습니다). 여기서 다시 import 하지 않는 이유는
#: 이 스크립트가 패키지 없이도 돌아야 하기 때문입니다.
NO_SUFFIX = 0


def _collect_page_size(source: str) -> int | None:
    r"""연속조회 커서 폭을 읽습니다.

    `KisEndpoint.page_size` 가 받는 값입니다. KIS 의 커서에는 **네 가지
    변형**이 있습니다 (#16 이 `KisPage` 에서 정리한 것과 같은 목록).

        ctx_area_fk200  ctx_area_fk100  ctx_area_fk50  ctx_area_fk

    마지막이 함정입니다. 폭 숫자가 없어서 `\d+` 로 찾으면 **조용히 빠집니다.**
    그 API 는 `KisPaginationAPIResponse` 를 상속하는 순간 파싱에서 죽습니다.

    폭을 모르는 평문 커서는 `NO_SUFFIX`(0) 로 둡니다 — 라이브러리가 쓰는
    바로 그 표현입니다. `None`(페이징 없음)과 구분되어야 합니다.
    """
    found = _CURSOR.findall(source)
    if not found:
        return None

    widths = {int(m) for m in found if m}
    if widths:
        # 한 엔드포인트가 폭을 섞어 쓰지는 않습니다. 섞였다면 큰 쪽이 실제 커서입니다.
        return max(widths)

    return NO_SUFFIX


def _body_attr(node: ast.AST) -> str | None:
    """`res.getBody().output1` 에서 `output1` 을 꺼냅니다."""
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and node.value.func.attr == "getBody"
    ):
        return node.attr
    return None


def _collect_output_blocks(func: ast.FunctionDef) -> dict[str, str]:
    """응답 블록 이름과 리스트/단건 여부를 읽습니다.

    판별 신호는 **샘플이 DataFrame 을 만드는 방식**입니다.

        pd.DataFrame(res.getBody().output)     -> list    (그대로 넘김)
        pd.DataFrame([res.getBody().output])   -> single  (감싸는 이유는 dict 라서)

    중간 변수를 거치는 경우가 많아(`output_data = res.getBody().output`)
    변수→블록 매핑을 먼저 만든 뒤 `pd.DataFrame` 인자를 봅니다.

    `if not isinstance(x, list): x = [x]` 로 방어한 곳은 **원본도 확신이
    없다는 뜻**이므로 `unknown` 으로 둡니다. 추측해서 채우면 생성물이 조용히
    틀립니다 — 사람이 보게 남깁니다.
    """
    var_to_block: dict[str, str] = {}
    blocks: dict[str, str] = {}
    defensive: set[str] = set()

    for node in ast.walk(func):
        # ① 블록 이름 수집 + 변수 매핑
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = _body_attr(node.value)
            if name and name.startswith("output") and isinstance(node.targets[0], ast.Name):
                var_to_block[node.targets[0].id] = name
                blocks.setdefault(name, "unknown")

        if (name := _body_attr(node)) and name.startswith("output"):
            blocks.setdefault(name, "unknown")

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "hasattr":
            continue

        # ② `isinstance(x, list)` 방어가 있으면 그 변수는 확신할 수 없습니다
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "isinstance"
            and len(node.args) == 2
            and isinstance(node.args[0], ast.Name)
        ):
            defensive.add(node.args[0].id)

    # ③ `pd.DataFrame(...)` 인자로 리스트/단건 판정
    for node in ast.walk(func):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "DataFrame"
            and node.args
        ):
            continue

        arg = node.args[0]
        wrapped = isinstance(arg, ast.List) and len(arg.elts) == 1
        inner = arg.elts[0] if wrapped else arg

        block = _body_attr(inner)
        if block is None and isinstance(inner, ast.Name):
            if inner.id in defensive:
                continue  # 원본이 방어했습니다 — 확신할 수 없습니다
            block = var_to_block.get(inner.id)

        if block and block.startswith("output"):
            blocks[block] = "single" if wrapped else "list"

    return blocks


def _is_post(func: ast.FunctionDef) -> bool:
    for node in ast.walk(func):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg == "postFlag" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    return True
    return False


def _doc_code(source: str) -> str | None:
    m = _DOC_CODE.search(source)
    return m.group(1) if m else None


def extract_one(folder: pathlib.Path, category: str) -> EndpointSpec:
    spec = EndpointSpec(category=category, name=folder.name)

    main_path = folder / f"{folder.name}.py"
    if not main_path.exists():
        candidates = [p for p in folder.glob("*.py") if not p.name.startswith("chk_")]
        if not candidates:
            spec.problems.append("주 파일 없음")
            return spec
        main_path = candidates[0]

    tree = _module(main_path)
    if tree is None:
        spec.problems.append(f"{main_path.name} 파싱 불가")
        return spec

    source = main_path.read_text(encoding="utf-8")
    spec.doc_code = _doc_code(source)
    spec.path = _str_assign(tree, "API_URL")

    func = _main_function(tree, folder.name)

    # 웹소켓 구독 함수는 `API_URL` 이 없는 것이 **정상**입니다. 시그니처가
    # `(tr_type, tr_key, ...)` 이고 문서 코드가 `[실시간-nnn]` 입니다.
    # 이것을 실패로 세면 파싱률이 82% 로 보입니다 — 실제로는 REST 100% 입니다.
    ws_args = func is not None and {"tr_type", "tr_key"} <= {a.arg for a in func.args.args}
    if ws_args or (spec.path is None and spec.doc_code and "실시간" in spec.doc_code):
        spec.kind = "websocket"

    if spec.kind == "rest" and spec.path is None:
        spec.problems.append("API_URL 없음")
    if func is None:
        spec.problems.append("엔드포인트 함수 없음")
    else:
        spec.tr_branches = _collect_tr_branches(func)
        spec.tr_ids = [b["tr_id"] for b in spec.tr_branches]
        if not spec.tr_ids:
            spec.problems.append("tr_id 없음")
        spec.params = _collect_params(func)
        spec.required, spec.optional = _split_args(func)
        spec.method = "POST" if _is_post(func) else "GET"
        spec.output_blocks = _collect_output_blocks(func)
        spec.page_size = _collect_page_size(source)

    chk_path = folder / f"chk_{folder.name}.py"
    if chk_path.exists():
        chk_tree = _module(chk_path)
        if chk_tree is None:
            spec.problems.append(f"{chk_path.name} 파싱 불가")
        else:
            spec.fields = _dict_assign(chk_tree, "COLUMN_MAPPING")
            spec.numeric_fields = _list_assign(chk_tree, "NUMERIC_COLUMNS")
            if not spec.fields:
                spec.problems.append("COLUMN_MAPPING 비어 있음")
            elif not (set(spec.fields) - WRAPPER_KEYS):
                # 파싱은 됐지만 필드가 하나도 없습니다. 성공으로 세면 생성기가
                # 필드 0개짜리 응답 클래스를 만들어 냅니다.
                spec.problems.append("COLUMN_MAPPING 이 껍데기 키뿐")
            else:
                stray = sorted(set(spec.fields) & WRAPPER_KEYS)
                if stray:
                    # `news_title` 이 이 경우입니다 — 실제 필드 사이에 `output1`
                    # 이 섞여 있습니다. **조용히 지우지 않고 기록합니다.**
                    # 진짜 필드가 이 이름을 쓰는 날이 오면 여기서 보입니다.
                    for k in stray:
                        del spec.fields[k]
                    spec.warnings.append(f"껍데기 키 제거: {', '.join(stray)}")
    elif spec.kind == "rest":
        spec.problems.append("chk_ 파일 없음")

    return spec


def extract_all(root: pathlib.Path) -> list[EndpointSpec]:
    specs: list[EndpointSpec] = []
    for category_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        if category_dir.name in SKIP_DIRS:
            continue
        for folder in sorted(p for p in category_dir.iterdir() if p.is_dir()):
            if folder.name in SKIP_DIRS:
                continue
            specs.append(extract_one(folder, category_dir.name))
    return specs


#: 필드명 접미사 -> vmkis 타입.
#:
#: #21 은 4개(`_amt` `_qty` `_dt` `_yn`)만 예로 들고 커버리지 54% 를 주장했습니다.
#: 아래는 **유니크 필드 2,499개의 접미사 분포를 실측해** 상위부터 채운 것입니다.
#: 각 줄 끝 숫자가 그 접미사를 가진 유니크 필드 수입니다(2026-08-30 기준).
#:
#: 미확정 필드는 `KisString` 으로 둡니다. `KisString` 은 어떤 문자열도 받으므로
#: **런타임 파싱 에러가 나지 않습니다.** 커버리지는 편의의 문제이지 정확성의
#: 문제가 아닙니다 — 타입 승격은 나중에 해도 됩니다.
SUFFIX_TYPES: dict[str, str] = {
    # 금액·가격 계열
    "_amt": "KisDecimal",  # 356  금액
    "_pbmn": "KisDecimal",  #  78  대금
    "_smtl": "KisDecimal",  #  44  합계
    "_unpr": "KisDecimal",  #  25  단가
    "_pric": "KisDecimal",  #  24
    "_vrss": "KisDecimal",  #  22  대비
    "_prpr": "KisDecimal",  #  20  현재가
    "_hgpr": "KisDecimal",  #  19  최고가
    "_lwpr": "KisDecimal",  #  19  최저가
    "_prc": "KisDecimal",  #  15
    "_price": "KisDecimal",  #  14
    "_oprc": "KisDecimal",  #  13  시가
    "_mgna": "KisDecimal",  #  13  증거금
    # 비율 계열
    "_rate": "KisDecimal",  #  81
    "_rt": "KisDecimal",  #  31
    "_ctrt": "KisDecimal",  #  18  대비율
    # 수량 계열
    "_qty": "KisInt",  # 127
    "_vol": "KisInt",  #  63  거래량
    "_cnt": "KisInt",  #  18
    "_rsqn": "KisInt",  #  16  잔수량
    "_rank": "KisInt",  #       순위
    # 날짜·시간
    "_dt": "KisDate",  #  89
    "_date": "KisDate",  #  35
    "_tm": "KisTime",  #
    "_time": "KisTime",  #
    # 불리언
    "_yn": "KisBool",  #  75  여부
    # 문자열(명시적으로 두어 "추정 못 함"과 구분합니다)
    "_cd": "KisString",  # 127  코드
    "_code": "KisString",  #  35
    "_name": "KisString",  #  81
    "_nm": "KisString",  #       명
    "_sign": "KisString",  #  16  부호
    "_no": "KisString",  #       번호
}


def guess_type(field_name: str) -> str | None:
    for suffix, kis_type in SUFFIX_TYPES.items():
        if field_name.endswith(suffix):
            return kis_type
    return None


def report(specs: list[EndpointSpec]) -> None:
    rest = [s for s in specs if s.kind == "rest"]
    ws = [s for s in specs if s.kind == "websocket"]
    ok = [s for s in rest if s.complete]
    post = [s for s in rest if s.method == "POST"]

    all_fields = [f for s in rest for f in s.fields if f not in WRAPPER_KEYS]
    unique = sorted(set(all_fields))
    typed = [f for f in unique if guess_type(f)]

    print(f"엔드포인트 폴더        {len(specs)}  (auth 제외)")
    print(f"  REST                 {len(rest)}")
    print(f"  웹소켓               {len(ws)}   ← API_URL 이 없는 것이 정상")
    print(f"REST 완전 파싱         {len(ok)} / {len(rest)} = {len(ok) / len(rest):.1%}")
    print(f"POST(주문 계열)        {len(post)}   ← 수동 리뷰 게이트 대상")
    print(f"응답 필드 총           {len(all_fields)}  (유니크 {len(unique)})")
    print(f"접미사로 타입 추정     {len(typed)} / {len(unique)} = {len(typed) / len(unique):.1%}")

    # 이름은 카테고리 간에 **유일하지 않습니다.** 이름으로 키를 잡는 도구는
    # 여기 걸리는 만큼을 조용히 잃습니다.
    dup = {n for n, c in Counter(s.name for s in specs).items() if c > 1}
    print(f"이름 충돌              {len(dup)}종  ← category/name 으로 키를 잡아야 합니다")

    warned = [s for s in rest if s.warnings]
    if warned:
        print(f"\n경고 {len(warned)}건:")
        for s in warned:
            print(f"  {s.category}/{s.name}: {'; '.join(s.warnings)}")

    print("\n실패 사유:")
    for reason, n in Counter(p for s in rest for p in s.problems).most_common():
        print(f"  {n:4d}  {reason}")

    print("\n실패한 엔드포인트:")
    for s in rest:
        if not s.complete:
            print(f"  {s.category}/{s.name}: {', '.join(s.problems)}")

    print("\n카테고리별 (REST):")
    for cat, n in Counter(s.category for s in rest).most_common():
        good = sum(1 for s in rest if s.category == cat and s.complete)
        print(f"  {good:3d}/{n:3d}  {cat}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=pathlib.Path, help="examples_llm 디렉터리")
    ap.add_argument("-o", "--output", type=pathlib.Path, help="스펙 JSON 출력 경로")
    ap.add_argument("--report", action="store_true", help="수치 요약을 표준출력으로")
    args = ap.parse_args()

    if not args.root.is_dir():
        print(f"경로가 없습니다: {args.root}", file=sys.stderr)
        return 2

    specs = extract_all(args.root)

    if args.output:
        args.output.write_text(
            json.dumps([asdict(s) for s in specs], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"{len(specs)}건 -> {args.output}")

    if args.report or not args.output:
        report(specs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
