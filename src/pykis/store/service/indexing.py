from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pykis.store.raw.spec import RecordSpec


@dataclass(frozen=True, slots=True)
class IndexFields:
    symbol: str | None = None
    standard: str | None = None
    isin: str | None = None


_EXPLICIT: dict[str, IndexFields] = {
    "IDX_CODE": IndexFields(symbol="idx_code"),
    "ST_FO_COM_CODE": IndexFields(symbol="shrn_iscd", standard="stnd_iscd"),
    "ST_FO_STK_CODE": IndexFields(symbol="shrn_iscd", standard="stnd_iscd"),
    "ST_FO_IDX_CODE": IndexFields(symbol="shrn_iscd", standard="stnd_iscd"),
    "ST_BOND_CODE": IndexFields(symbol="stnd_iscd", standard="stnd_iscd"),
    "ST_KNX_CODE": IndexFields(symbol="mksc_shrn_iscd", standard="stnd_iscd"),
    "ST_KSQ_CODE": IndexFields(symbol="mksc_shrn_iscd", standard="stnd_iscd"),
    "ST_KSP_CODE": IndexFields(symbol="mksc_shrn_iscd", standard="stnd_iscd"),
    "ST_ELW_CODE": IndexFields(symbol="mksc_shrn_iscd", standard="stnd_iscd"),
    "ST_MEM_CODE": IndexFields(symbol="mbcr_no"),
    "THEME_CODE": IndexFields(symbol="shrn_iscd"),
    "FFCODE_TBL": IndexFields(symbol="sSrsCd"),
    "FOCODE_TBL": IndexFields(symbol="sSrsCd"),
    "mastcode": IndexFields(symbol="symb"),
    "ST_FRGN_CODE": IndexFields(symbol="symb"),
}


def detect_index_fields(struct_name: str, record_spec: RecordSpec) -> IndexFields:
    explicit = _EXPLICIT.get(struct_name)
    if explicit is not None:
        return explicit

    names = [field.name for field in record_spec.fields]
    lower = {name.lower(): name for name in names}

    def pick(candidates: tuple[str, ...]) -> str | None:
        for cand in candidates:
            if cand in lower:
                return lower[cand]
        return None

    symbol = pick(("symbol", "symb", "shrn_iscd", "mksc_shrn_iscd", "srs_cd", "pdno", "code"))
    standard = pick(("stnd_iscd", "std_pdno", "std_iscd"))
    isin = None
    for name in names:
        if "isin" in name.lower():
            isin = name
            break
    return IndexFields(symbol=symbol, standard=standard, isin=isin)


def build_index_row(
    *,
    fields: Mapping[str, str],
    index_fields: IndexFields,
    source_id: str,
    line_no: int,
    table_name: str,
) -> dict[str, object] | None:
    symbol = fields.get(index_fields.symbol) if index_fields.symbol else None
    standard = fields.get(index_fields.standard) if index_fields.standard else None
    isin = fields.get(index_fields.isin) if index_fields.isin else None

    symbol = symbol.strip().upper() if isinstance(symbol, str) else None
    standard = standard.strip().upper() if isinstance(standard, str) else None
    isin = isin.strip().upper() if isinstance(isin, str) else None

    if not symbol and not standard and not isin:
        return None

    return {
        "symbol": symbol or None,
        "standard_code": standard or None,
        "isin": isin or None,
        "source_id": source_id,
        "line_no": line_no,
        "table_name": table_name,
    }
