from __future__ import annotations

from collections import Counter

from codegen.core.issues import IssueLevel, SpecIssue
from codegen.streaming.models import StreamingSpecRoot, TrSpec

ALLOWED_MARKETS = {"domestic", "overseas"}
ALLOWED_TIMEZONES = {"Asia/Seoul", "market"}
ALLOWED_FIELD_TYPES = {"decimal", "str", "int", "datetime"}
ALLOWED_DATETIME_KINDS = {"date_only", "time_only"}
ALLOWED_DATETIME_FORMATS = {"YYYYMMDD", "YYMMDD", "HHMMSS"}
ALLOWED_DECIMAL_SCALES = {"zdiv"}
ALLOWED_YEAR_POLICIES = {None, "century_from_local"}


def validate_spec(spec: StreamingSpecRoot) -> list[SpecIssue]:
    issues: list[SpecIssue] = []
    for tr_id, tr_spec in spec.tr_specs.items():
        issues.extend(_validate_tr_spec(tr_spec))
        if tr_spec.tr_id != tr_id:
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "tr.id.mismatch",
                    f"TR key {tr_id} does not match tr_id {tr_spec.tr_id}",
                    tr_spec.endpoint_uuid,
                    tr_id,
                )
            )
    return issues


def _validate_tr_spec(tr_spec: TrSpec) -> list[SpecIssue]:
    issues: list[SpecIssue] = []
    if not tr_spec.endpoint_uuid:
        issues.append(
            SpecIssue(
                IssueLevel.ERROR,
                "tr.missing_endpoint_uuid",
                "endpoint_uuid is required",
                tr_spec.tr_id,
                tr_spec.tr_id,
            )
        )

    if tr_spec.market not in ALLOWED_MARKETS:
        issues.append(
            SpecIssue(
                IssueLevel.ERROR,
                "tr.market.invalid",
                f"market must be one of {sorted(ALLOWED_MARKETS)}",
                tr_spec.tr_id,
                tr_spec.tr_id,
            )
        )

    if tr_spec.timezone not in ALLOWED_TIMEZONES and not tr_spec.timezone:
        issues.append(
            SpecIssue(
                IssueLevel.WARN,
                "tr.timezone.unexpected",
                f"timezone {tr_spec.timezone} is not in {sorted(ALLOWED_TIMEZONES)}",
                tr_spec.tr_id,
                tr_spec.tr_id,
            )
        )

    field_order = tr_spec.field_order
    counts = Counter(field_order)
    duplicates = [code for code, count in counts.items() if count > 1]
    if duplicates and not tr_spec.field_aliases:
        issues.append(
            SpecIssue(
                IssueLevel.ERROR,
                "tr.duplicate_fields",
                f"duplicate field codes require aliases: {', '.join(sorted(duplicates))}",
                tr_spec.tr_id,
                tr_spec.tr_id,
            )
        )

    if tr_spec.field_order_normalized is not None:
        if len(tr_spec.field_order_normalized) != len(tr_spec.field_order):
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "tr.field_order_normalized.length",
                    "field_order_normalized length must match field_order",
                    tr_spec.tr_id,
                    tr_spec.tr_id,
                )
            )

        normalized_set = set(tr_spec.field_order_normalized)
        if len(normalized_set) != len(tr_spec.field_order_normalized):
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "tr.field_order_normalized.unique",
                    "field_order_normalized must have unique names",
                    tr_spec.tr_id,
                    tr_spec.tr_id,
                )
            )

    expected_names = tr_spec.field_order_normalized or tr_spec.field_order
    for name in expected_names:
        if name not in tr_spec.field_specs:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "tr.field_specs.missing",
                    f"Missing field_specs for {name}",
                    tr_spec.tr_id,
                    tr_spec.tr_id,
                )
            )

    for name, field_spec in tr_spec.field_specs.items():
        if field_spec.field_type not in ALLOWED_FIELD_TYPES:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "field.type.invalid",
                    f"Invalid field type {field_spec.field_type} for {name}",
                    tr_spec.tr_id,
                    tr_spec.tr_id,
                )
            )

        if field_spec.field_type == "datetime":
            if field_spec.datetime_rule is None:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "field.datetime.missing_rule",
                        f"datetime rule missing for {name}",
                        tr_spec.tr_id,
                        tr_spec.tr_id,
                    )
                )
                continue
            rule = field_spec.datetime_rule
            if rule.kind not in ALLOWED_DATETIME_KINDS:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "field.datetime.kind",
                        f"Invalid datetime kind {rule.kind} for {name}",
                        tr_spec.tr_id,
                        tr_spec.tr_id,
                    )
                )
            if rule.format not in ALLOWED_DATETIME_FORMATS:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "field.datetime.format",
                        f"Invalid datetime format {rule.format} for {name}",
                        tr_spec.tr_id,
                        tr_spec.tr_id,
                    )
                )
            if rule.kind == "time_only" and not rule.date_field:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "field.datetime.date_field",
                        f"time_only datetime requires date_field for {name}",
                        tr_spec.tr_id,
                        tr_spec.tr_id,
                    )
                )
            if rule.year_policy not in ALLOWED_YEAR_POLICIES:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "field.datetime.year_policy",
                        f"Invalid year_policy {rule.year_policy} for {name}",
                        tr_spec.tr_id,
                        tr_spec.tr_id,
                    )
                )
        elif field_spec.datetime_rule is not None:
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "field.datetime.unused",
                    f"datetime rule provided for non-datetime field {name}",
                    tr_spec.tr_id,
                    tr_spec.tr_id,
                )
            )

        if field_spec.decimal_rule is not None:
            rule = field_spec.decimal_rule
            if rule.scale not in ALLOWED_DECIMAL_SCALES:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "field.decimal.scale",
                        f"Invalid decimal scale {rule.scale} for {name}",
                        tr_spec.tr_id,
                        tr_spec.tr_id,
                    )
                )
            if rule.zdiv_field not in tr_spec.field_order:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "field.decimal.zdiv_field",
                        f"zdiv_field {rule.zdiv_field} missing in field_order",
                        tr_spec.tr_id,
                        tr_spec.tr_id,
                    )
                )
        if field_spec.field_type in {"str", "int"} and field_spec.decimal_rule is not None:
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "field.decimal.unused",
                    f"decimal rule provided for non-decimal field {name}",
                    tr_spec.tr_id,
                    tr_spec.tr_id,
                )
            )

    return issues
