#!/usr/bin/env python3
"""추출된 스펙에서 vmkis 스타일 엔드포인트 모듈을 생성합니다. (이슈 #21 파일럿)

## 무엇을 생성하는가

- `KisEndpoint` 상수 (경로 + TR ID)
- 응답 항목 클래스 (`KisDynamic` 상속, 필드 + 한글 라벨 docstring)
- 응답 래퍼 클래스 (`KisAPIResponse`, `output` 을 리스트/단건으로)

## 무엇을 생성하지 **않는가** — 손이 필요한 부분

| | 왜 |
|---|---|
| `output` 이 리스트인지 단건인지 (일부) | 샘플의 `pd.DataFrame` 인자로 판정합니다. **원본이 `isinstance` 로 방어한 곳은 원본도 모릅니다** — `unknown` 으로 표시하고 사람에게 넘깁니다 |
| 파라미터 검증 규칙 | 샘플의 `raise ValueError(...)` 는 **원문 로직**입니다. 옮기지 않습니다 |
| scope 바인딩 (`kis.stock().xxx()`) | Protocol 필요 여부 판정이 필요합니다 (ARCHITECTURE.md 판정표) |
| 필드 이름의 한국어→영어 번역 | 기계가 정하면 공개 API 이름이 흔들립니다 |

## 원문 복사 금지

원본(`koreainvestment/open-trading-api`)에는 LICENSE 가 없습니다. 이 생성기는
**사실만** 씁니다 — 경로, TR ID, 필드명, 한글 라벨. 원문 docstring 설명문은
스펙에 들어 있지도 않습니다(`extract_kis_specs.py` 가 추출하지 않습니다).

`tests/unit/test_codegen_pilot.py` 가 생성물에 원문 문장이 섞이지 않았는지
기계적으로 검사합니다. **사람이 눈으로 지키는 규칙은 300개 규모에서 지켜지지
않습니다.**

## 사용법

    python scripts/generate_endpoint.py specs.json volume_rank -o out/
"""

from __future__ import annotations

import argparse
import json
import keyword
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from extract_kis_specs import DOMAIN_AXIS, DOMAIN_VALUES, guess_type  # noqa: E402

#: 생성 헤더. 손으로 고치면 다음 생성 때 날아간다는 것을 파일 자신이 말해야 합니다.
HEADER = '''"""{title}

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/{category}/{name}` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""
'''


def _pascal(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[_\-]", name) if part)


def _safe_ident(name: str) -> str:
    ident = re.sub(r"\W", "_", name)
    if not ident or ident[0].isdigit():
        ident = f"f_{ident}"
    if keyword.iskeyword(ident):
        ident = f"{ident}_"
    return ident


#: KisType 이름 -> 파이썬 주석 타입.
PY_TYPE = {
    "KisString": "str",
    "KisInt": "int",
    "KisDecimal": "Decimal",
    "KisBool": "bool",
    "KisDate": "date",
    "KisTime": "time",
}


def _endpoint_args(spec: dict, tr_live: str, tr_paper: str | None, indent: str) -> list[str]:
    lines = [f'{indent}path="{spec["path"]}",', f'{indent}tr_live="{tr_live}",']
    if tr_paper:
        lines.append(f'{indent}tr_paper="{tr_paper}",')
    if spec["method"] == "POST":
        lines.append(f'{indent}method="POST",')
    # `is not None` 입니다. **`0` 은 falsy 인데 유효한 값입니다** —
    # 접미사 없는 `CTX_AREA_FK` 를 뜻하는 `NO_SUFFIX`(#16). `if page_size:` 로
    # 적었다가 국내휴장일조회가 페이징 없는 엔드포인트로 생성됐습니다.
    if spec.get("page_size") is not None:
        size = spec["page_size"]
        if size == 0:
            lines.append(f"{indent}page_size=NO_SUFFIX,  # 접미사 없는 CTX_AREA_FK")
        else:
            lines.append(f"{indent}page_size={size},")
    return lines


def _render_endpoints(spec: dict, const: str) -> list[str]:
    """TR ID 분기를 `KisEndpoint` 하나 또는 `dict[key, KisEndpoint]` 로.

    KIS 는 같은 기능이라도 **실전/모의**와 **업무 구분**(주문 종류, 거래소,
    기간 등) 두 축으로 TR ID 를 가릅니다. `client/endpoint.py` 가 정한 방식이
    이것입니다 — 실전/모의 축은 `KisEndpoint` 가 `tr_live`/`tr_paper` 로
    흡수하고, **나머지 축만 dict 로 남깁니다.**

    실측: TR ID 가 2개 이상인 23개 중 11개는 실전/모의 축만이라 상수 하나로
    끝나고, 12개는 업무 축이 있어 dict 가 필요합니다.
    """
    branches = spec.get("tr_branches") or [{"tr_id": t, "conditions": {}} for t in spec["tr_ids"]]
    if not branches:
        return []

    # 업무 축 키로 묶습니다. 실전/모의 축은 KisEndpoint 안으로 들어갑니다.
    groups: dict[tuple, dict[str, str]] = {}
    for b in branches:
        conditions = dict(b["conditions"])
        domain = conditions.pop(DOMAIN_AXIS, None)
        key = tuple(sorted((k, v) for k, v in conditions.items()))
        slot = DOMAIN_VALUES.get(domain or "", "live")
        groups.setdefault(key, {}).setdefault(slot, b["tr_id"])

    out: list[str] = []

    if len(groups) == 1:
        ((key, trs),) = groups.items()
        live = trs.get("live") or next(iter(trs.values()))
        out.append(f"{const} = KisEndpoint(")
        out.extend(_endpoint_args(spec, live, trs.get("paper"), "    "))
        out.append(")")
        out.append("")
        if key:
            out.append(f"# 조건 {dict(key)} 에서만 유효합니다 — 원본이 그 분기에서만 이 TR 을 씁니다.")
            out.append("")
        return out

    axes = sorted({k for key in groups for k, _ in key})
    out.append(f"#: {' × '.join(axes)} -> 엔드포인트.")
    out.append("#: 실전/모의 축은 KisEndpoint 가 tr_live/tr_paper 로 흡수합니다.")
    out.append(f"{const}_ENDPOINTS: dict[str, KisEndpoint] = {{")
    for key, trs in sorted(groups.items(), key=lambda kv: str(kv[0])):
        values = [v for _, v in key]
        label = repr(values[0]) if len(values) == 1 else repr(tuple(values))
        if any(v is None for v in values):
            out.append("    # ⚠️ 키에 None 이 있습니다 — 원본의 else 가지라 조건을 특정할 수 없습니다.")
        live = trs.get("live") or next(iter(trs.values()))
        out.append(f"    {label}: KisEndpoint(")
        out.extend(_endpoint_args(spec, live, trs.get("paper"), "        "))
        out.append("    ),")
    out.append("}")
    out.append("")
    return out


def render(spec: dict, as_list: bool | None = None) -> str:
    """스펙 하나를 vmkis 스타일 모듈로 렌더링합니다.

    `as_list` 는 스펙이 판정을 못 한 블록에만 쓰이는 수동 지정입니다.
    스펙이 `list`/`single` 을 알고 있으면 그것을 따릅니다.
    """
    name = spec["name"]
    cls = f"Kis{_pascal(name)}"
    const = name.upper()
    title = f"[{spec['category']}] {name}" + (f"  {spec['doc_code']}" if spec["doc_code"] else "")

    fields = spec["fields"]
    kis_types = {f: (guess_type(f) or "KisString") for f in fields}
    used = sorted(set(kis_types.values()) | {"KisString"})
    py_imports = sorted({PY_TYPE[t] for t in used if PY_TYPE[t] in ("Decimal", "date", "time")})

    blocks = spec.get("output_blocks") or {"output": "unknown"}

    out: list[str] = [HEADER.format(title=title, category=spec["category"], name=name)]

    if py_imports:
        std = [i for i in py_imports if i in ("date", "time")]
        if std:
            out.append(f"from datetime import {', '.join(std)}")
        if "Decimal" in py_imports:
            out.append("from decimal import Decimal")
        out.append("")

    if spec.get("page_size") == 0:
        out.append("from vmkis.client.endpoint import KisEndpoint")
        out.append("from vmkis.client.page import NO_SUFFIX")
    else:
        out.append("from vmkis.client.endpoint import KisEndpoint")
    out.append("from vmkis.responses.dynamic import KisDynamic, KisList, KisObject")
    out.append("from vmkis.responses.response import KisAPIResponse")
    out.append(f"from vmkis.responses.types import {', '.join(used)}")
    out.append("")
    out.append("")

    # ── 엔드포인트 상수 ──────────────────────────────────────────────────────
    out.extend(_render_endpoints(spec, const))
    if spec["method"] == "POST":
        out.append("# ⚠️ 주문 계열입니다. 오생성 시 금전 사고로 이어지므로 수동 리뷰 없이")
        out.append("#    패키지에 넣지 마세요. (#21 의 '주의' 항목)")
        out.append("")
    out.append("")

    # ── 블록별 항목 클래스 ──────────────────────────────────────────────────
    #
    # KIS 는 한 응답에 output / output1 / output2 를 함께 담기도 합니다
    # (272개 중 94개가 블록 2개 이상). 예전 생성기는 `output` 하나만
    # 가정해서 나머지를 통째로 잃었습니다.
    #
    # **필드 라벨은 블록별로 나뉘어 있지 않습니다.** `COLUMN_MAPPING` 이
    # 응답 전체를 한 표로 담기 때문입니다. 그래서 블록이 여럿이면 같은 필드
    # 집합을 각 블록에 붙이고 사람이 갈라야 합니다 — 아래 주석으로 표시합니다.
    multi = len(blocks) > 1
    item_names: dict[str, str] = {}

    for block in sorted(blocks):
        item_cls = f"{cls}{_pascal(block)}Item" if multi else f"{cls}Item"
        item_names[block] = item_cls
        out.append(f"class {item_cls}(KisDynamic):")
        out.append(f'    """{name} 응답 항목 — `{block}` ({len(fields)}개 필드)"""')
        out.append("")
        for raw, label in fields.items():
            kt = kis_types[raw]
            out.append(f'    {_safe_ident(raw)}: {PY_TYPE[kt]} = {kt}["{raw}"]')
            out.append(f'    """{label}"""')
        out.append("")
        out.append("")

    # ── 응답 래퍼 ───────────────────────────────────────────────────────────
    out.append(f"class {cls}(KisAPIResponse):")
    out.append(f'    """{name} 응답"""')
    out.append("")
    out.append("    __path__ = None")
    out.append("")

    for block in sorted(blocks):
        kind = blocks[block]
        if kind == "unknown" and as_list is not None:
            kind = "list" if as_list else "single"

        attr = _safe_ident(block)
        item_cls = item_names[block]

        if kind == "single":
            out.append(f'    {attr}: {item_cls} = KisObject({item_cls})["{block}"]')
            out.append(f'    """{block} (단건)"""')
        else:
            if kind == "unknown":
                # 추측하지 않습니다. 원본이 `isinstance` 로 방어했다는 것은
                # **원본 생성기도 몰랐다**는 뜻입니다. KisList 는 dict 를 받으면
                # TypeError 를 내므로, 틀리면 런타임에 터집니다.
                out.append(f"    # ⚠️ `{block}` 이 리스트인지 단건인지 원본이 알려주지 않습니다")
                out.append("    #    (샘플이 `isinstance(x, list)` 로 방어하고 있습니다).")
                out.append("    #    실제 응답을 보고 KisList / KisObject 중 하나로 확정하세요.")
            out.append(f'    {attr}: list[{item_cls}] = KisList({item_cls})["{block}"]')
            out.append(f'    """{block} 목록"""')
        out.append("")

    untyped = [f for f, t in kis_types.items() if guess_type(f) is None]
    if untyped:
        out.append("")
        out.append(f"# 타입을 추정하지 못해 KisString 으로 둔 필드 {len(untyped)}개:")
        for chunk in [untyped[i : i + 6] for i in range(0, len(untyped), 6)]:
            out.append(f"#   {', '.join(chunk)}")
        out.append("# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.")
        out.append("# 실제 응답을 보고 승격하세요.")

    if multi:
        out.append("")
        out.append(f"# ⚠️ 이 응답은 블록이 {len(blocks)}개입니다: {', '.join(sorted(blocks))}")
        out.append("#    원본의 COLUMN_MAPPING 은 블록을 나누지 않으므로 위 항목 클래스들이")
        out.append("#    같은 필드 집합을 공유합니다. 실제 응답을 보고 갈라내세요.")

    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("specs", type=pathlib.Path)
    ap.add_argument(
        "names",
        nargs="+",
        help="생성할 엔드포인트. `category/name` 또는 `name`. "
        "이름은 카테고리 간에 유일하지 않습니다 — 332개 중 30개가 겹칩니다",
    )
    ap.add_argument("-o", "--out", type=pathlib.Path, required=True)
    ap.add_argument("--single", nargs="*", default=[], help="output 이 단건인 엔드포인트")
    args = ap.parse_args()

    raw = json.loads(args.specs.read_text(encoding="utf-8"))
    # **이름만으로 키를 잡으면 안 됩니다.** `inquire_price` 는 카테고리 5곳에
    # 있고, 뒤엣것이 앞엣것을 덮어 조용히 다른 엔드포인트를 생성합니다.
    specs = {f"{s['category']}/{s['name']}": s for s in raw}
    args.out.mkdir(parents=True, exist_ok=True)

    for name in args.names:
        if name in specs:
            spec = specs[name]
        else:
            matches = [k for k in specs if k.rsplit("/", 1)[1] == name]
            if not matches:
                print(f"스펙에 없습니다: {name}", file=sys.stderr)
                return 1
            if len(matches) > 1:
                print(
                    f"이름이 모호합니다: {name} — {', '.join(matches)}\n`category/name` 형태로 지정하세요.",
                    file=sys.stderr,
                )
                return 1
            spec = specs[matches[0]]
        if not spec["complete"] if "complete" in spec else spec["problems"]:
            print(f"완전 파싱되지 않은 스펙입니다: {name} — {spec['problems']}", file=sys.stderr)
            return 1
        forced = None
        if name in args.single or spec["name"] in args.single:
            forced = False
        code = render(spec, as_list=forced)
        # 파일명에도 카테고리를 넣습니다. 이름이 겹치면 생성물끼리 덮어씁니다.
        path = args.out / f"{spec['category']}__{spec['name']}.py"
        path.write_text(code, encoding="utf-8")
        print(f"{len(code.splitlines()):4d}줄  {path}")

    _format(args.out)
    return 0


def _format(out: pathlib.Path) -> None:
    """생성물을 저장소의 ruff 설정으로 다듬습니다.

    생성기가 빈 줄까지 완벽하게 맞추게 만들면 템플릿이 읽기 어려워집니다.
    포매팅은 포매터에게 맡기고, 생성기는 **내용**만 책임집니다.

    ruff 가 없으면 조용히 건너뜁니다 — 생성 자체는 성공했기 때문입니다.
    """
    ruff = shutil.which("ruff")
    if ruff is None:
        print("ruff 를 찾지 못해 포매팅을 건너뜁니다.", file=sys.stderr)
        return
    subprocess.run([ruff, "check", "--fix", "--quiet", str(out)], check=False)
    subprocess.run([ruff, "format", "--quiet", str(out)], check=False)


if __name__ == "__main__":
    raise SystemExit(main())
