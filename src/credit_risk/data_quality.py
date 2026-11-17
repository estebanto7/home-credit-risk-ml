"""Reusable, read-only data quality audits for pandas DataFrames.

Quickstart
----------
>>> result = audit_dataframe(df)
>>> paths = result.export('reports/data_quality')

Requires pandas and numpy only. The report HTML is self-contained; no server,
plotting library, internet connection or JavaScript build tool is required.

The auditor detects *signals*, not business-rule violations by implication.
No imputation, dtype conversion or modification is ever performed on ``df``.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd

__all__ = ["AuditConfig", "AuditResult", "audit_dataframe"]


@dataclass(frozen=True)
class AuditConfig:
    """Optional limits and detection settings; defaults suit laptop-size data."""

    high_missing_pct: float = 50.0
    missing_pair_threshold: float = 0.95
    missing_pair_sample_rows: int = 10_000
    missing_pair_max_columns: int = 140
    identical_columns_max_columns: int = 400
    duplicate_rows_max_cells: int = 60_000_000
    string_scan_max_unique: int = 5_000
    run_duplicate_rows: bool = True
    run_identical_columns: bool = True
    run_related_missingness: bool = True
    run_string_checks: bool = True
    run_numeric_sentinels: bool = True


@dataclass
class AuditResult:
    """In-memory audit results with an HTML/JSON exporter."""

    overview: dict[str, Any]
    variables: list[dict[str, Any]]
    findings: list[dict[str, Any]]
    coverage: list[dict[str, Any]]
    missing_groups: list[dict[str, Any]]
    related_missingness: list[dict[str, Any]]
    row_missing_distribution: list[dict[str, Any]]
    config: AuditConfig

    def as_dict(self) -> dict[str, Any]:
        """JSON-ready representation: diagnostics and evidence, no treatments."""
        return {
            "schema_version": "1.0",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "overview": self.overview,
            "variables": self.variables,
            "findings": self.findings,
            "missing_groups": self.missing_groups,
            "related_missingness": self.related_missingness,
            "row_missing_distribution": self.row_missing_distribution,
            "audit_coverage": self.coverage,
            "config": vars(self.config).copy(),
            "interpretation_notice": (
                "Flags are quality signals, not evidence that a value is invalid. "
                "No corrections have been applied."
            ),
        }

    def export(self, directory: str | Path) -> dict[str, Path]:
        """Write audit_report.html and audit_findings.json to ``directory``."""
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        files = {
            "html": directory / "audit_report.html",
            "json": directory / "audit_findings.json",
        }
        content = self.as_dict()
        files["json"].write_text(
            json.dumps(content, indent=2, ensure_ascii=False, allow_nan=False),
            encoding="utf-8",
        )
        files["html"].write_text(_render_html(content), encoding="utf-8")
        return files

    def findings_table(self) -> pd.DataFrame:
        """Every detected issue in a convenient tabular format."""
        return pd.DataFrame(self.findings, columns=["id", "code", "message", "category", "level", "columns", "evidence", "method"])

    def variable_table(self) -> pd.DataFrame:
        """One row per dataset column, including columns with no findings."""
        return pd.DataFrame(self.variables)


def _as_number(value: Any) -> int | float | None:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (int, np.integer)):
        return int(value)
    return float(value)


def _small_string(value: Any, limit: int = 180) -> str:
    string = str(value)
    return string[:limit] + ("…" if len(string) > limit else "")


def _metadata_map(metadata: pd.DataFrame | Mapping[str, Any] | None) -> dict[str, dict[str, Any]]:
    """Accept a DataFrame with Row/column, Description, Statistical Type, etc."""
    if metadata is None:
        return {}
    if isinstance(metadata, pd.DataFrame):
        columns = {str(c).strip().casefold().replace(" ", "_"): c for c in metadata.columns}
        key_col = next((columns[k] for k in ("column", "row", "variable", "name") if k in columns), None)
        if key_col is None:
            raise ValueError("metadata DataFrame needs a 'column' or 'Row' field")
        output = {}
        for _, record in metadata.iterrows():
            if pd.isna(record[key_col]):
                continue
            name = str(record[key_col])
            description = next((record[columns[k]] for k in ("description",) if k in columns), None)
            role = next((record[columns[k]] for k in ("statistical_type", "statistical_role") if k in columns), None)
            output[name] = {
                "description": None if description is None or pd.isna(description) else str(description),
                "statistical_type": None if role is None or pd.isna(role) else str(role),
            }
        return output
    if isinstance(metadata, Mapping):
        result = {}
        for key, value in metadata.items():
            if isinstance(value, Mapping):
                result[str(key)] = {
                    "description": value.get("description") or value.get("Description"),
                    "statistical_type": value.get("statistical_type") or value.get("Statistical Type"),
                }
            else:
                result[str(key)] = {"description": None, "statistical_type": str(value)}
        return result
    raise TypeError("metadata must be a pandas DataFrame, mapping, or None")


def _is_identifier(role: str | None) -> bool:
    return bool(role and "identifier" in role.casefold())


def _text_null_codes(s: pd.Series) -> list[dict[str, Any]]:
    markers = {
        "unknown", "not known", "not available", "missing", "n/a",
        "na", "none", "null", "nan", "not applicable", "?", "-", "--", "",
    }
    normalized = s.dropna().astype(str).str.strip().str.casefold()
    subset = normalized[normalized.isin(markers)]
    if subset.empty:
        return []
    counts = subset.value_counts()
    return [{"value": k if k else "<empty/whitespace>", "count": int(v)} for k, v in counts.items()]


def _numeric_sentinels(s: pd.Series) -> list[dict[str, Any]]:
    """Flag conventional repeated-9 placeholders only, never generic outliers."""
    candidates = [-9999999, -999999, -99999, -9999, -999, 999, 9999, 99999, 999999, 9999999]
    counts = s[s.isin(candidates)].value_counts()
    return [{"value": _as_number(k), "count": int(v)} for k, v in counts.items()]


def _mixed_types(s: pd.Series) -> dict[str, int]:
    counts = s.dropna().map(lambda x: type(x).__name__).value_counts()
    return {str(k): int(v) for k, v in counts.items()}


def _normalized_label_collisions(s: pd.Series, limit: int) -> list[list[str]]:
    try:
        unique = s.dropna().unique()
    except TypeError:
        return []  # Nested, non-hashable objects cannot be normalized safely.
    if len(unique) > limit:
        return []
    groups: defaultdict[str, set[str]] = defaultdict(set)
    for value in unique:
        if not isinstance(value, str):
            continue
        groups[value.strip().casefold()].add(value)
    collisions = [sorted(values) for values in groups.values() if len(values) > 1]
    return sorted(collisions, key=lambda x: -len(x))[:8]


def _text_looks_numeric_or_date(s: pd.Series) -> tuple[bool, bool]:
    values = s.dropna().astype(str).str.strip()
    if values.empty:
        return False, False
    if len(values) > 3_000:
        values = values.sample(n=3_000, random_state=42)
    # Don't classify codes with leading zeros as numeric-like.
    leading_zero_codes = values.str.fullmatch(r"[+-]?0\d+").mean() > 0.05
    parsed = pd.to_numeric(values, errors="coerce")
    looks_numeric = bool(parsed.notna().mean() >= 0.98 and not leading_zero_codes)
    iso = values.str.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?")
    looks_date = bool(iso.mean() >= 0.98)
    return looks_numeric, looks_date


def _fingerprint(s: pd.Series) -> tuple[Any, ...]:
    """Cheap candidate key. Full equality is always checked afterwards."""
    n = len(s)
    if n:
        sample_indices = np.unique(np.linspace(0, n - 1, min(n, 128), dtype=int))
        sampled = s.iloc[sample_indices]
        signature = tuple(_small_string(x, limit=48) for x in sampled.tolist())
    else:
        signature = ()
    return str(s.dtype), int(s.isna().sum()), signature


def audit_dataframe(
    df: pd.DataFrame,
    *,
    metadata: pd.DataFrame | Mapping[str, Any] | None = None,
    special_values: Mapping[str, list[Any] | tuple[Any, ...]] | None = None,
    config: AuditConfig | None = None,
) -> AuditResult:
    """Audit one DataFrame without changing it.

    Parameters
    ----------
    df: pandas.DataFrame
        Any tabular dataset. No target or schema is required.
    metadata: optional
        DataFrame with 'Row', 'Description', 'Statistical Type' (or column,
        description, statistical_type), or a mapping keyed by column name.
    special_values: optional
        Known/suspected special codes by variable, *only flagged*, never replaced.
        Example: {'DAYS_EMPLOYED': [365243]}.
    config: optional
        Configurable thresholds and expensive checks.

    Returns
    -------
    AuditResult
        .overview, .variables, .findings, .coverage and .export(folder).
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("audit_dataframe expects a pandas DataFrame")
    cfg = config or AuditConfig()
    if not 0 <= cfg.high_missing_pct <= 100 or not 0 <= cfg.missing_pair_threshold <= 1:
        raise ValueError("Invalid thresholds in AuditConfig")
    meta = _metadata_map(metadata)
    special_values = special_values or {}
    n_rows, n_cols = df.shape
    missing = df.isna()
    column_labels = [str(x) for x in df.columns]
    findings: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    variables: list[dict[str, Any]] = []

    def add(code: str, message: str, category: str, level: str = "review", *,
            columns: list[str] | None = None, evidence: dict[str, Any] | None = None,
            method: str = "exact") -> None:
        findings.append({
            "id": f"F{len(findings)+1:04}",
            "code": code,
            "message": message,
            "category": category,
            "level": level,
            "columns": columns or [],
            "evidence": evidence or {},
            "method": method,
        })

    def mark(check: str, status: str = "completed", method: str = "exact", detail: str = "") -> None:
        coverage.append({"check": check, "status": status, "method": method, "detail": detail})

    # 01. Dataset structure and value counts.
    dup_names = sorted([name for name, ct in Counter(column_labels).items() if ct > 1])
    if dup_names:
        add("duplicate_column_names", "Duplicate column names detected", "integrity", columns=dup_names,
            evidence={"names": dup_names})
    mark("Column names")

    name_missing_counts = []
    string_format_sampled = False
    label_normalization_skipped = 0
    complete_unique_identifier = False
    grouped: defaultdict[bytes, list[str]] = defaultdict(list)
    for i, label in enumerate(column_labels):
        s = df.iloc[:, i]
        is_missing = missing.iloc[:, i]
        if n_rows:
            try:
                unique_count = int(s.nunique(dropna=True))
            except TypeError:
                # Nested list/dict cells are not hashable. Report a fallback and
                # preserve the original dtype; this does not validate semantics.
                unique_count = int(s.dropna().map(repr).nunique())
                add("nonhashable_values", "Non-hashable nested values detected", "data_types", "review",
                    columns=[label], evidence={"distinct_repr_count": unique_count})
        else:
            unique_count = 0
        miss_count = int(is_missing.sum())
        missing_pct = 100 * miss_count / n_rows if n_rows else 0.0
        role = meta.get(label, {}).get("statistical_type")
        numerical = pd.api.types.is_numeric_dtype(s.dtype) and not pd.api.types.is_bool_dtype(s.dtype)
        zero_count = int(s.eq(0).sum()) if numerical else None
        item = {
            "position": i,
            "column": label,
            "dtype": str(s.dtype),
            "statistical_type": role,
            "description": meta.get(label, {}).get("description"),
            "rows": n_rows,
            "missing_count": miss_count,
            "missing_pct": round(missing_pct, 5),
            "unique_values": unique_count,
            "unique_ratio_pct": round(unique_count / max(n_rows - miss_count, 1) * 100, 5),
            "zero_count": zero_count,
            "zero_pct_of_all_rows": round(zero_count / n_rows * 100, 5) if zero_count is not None and n_rows else None,
            "all_missing": bool(miss_count == n_rows and n_rows > 0),
            "constant_observed": bool(unique_count == 1),
        }
        variables.append(item)
        name_missing_counts.append(miss_count)
        if miss_count:
            # A bit-packed pattern gives an *exact* group key, not a sample.
            pattern = np.packbits(is_missing.to_numpy(dtype=bool)).tobytes()
            grouped[pattern].append(label)
            add("missing_values", "Missing values detected" if missing_pct < cfg.high_missing_pct else "High missingness detected",
                "missingness", "review" if missing_pct >= cfg.high_missing_pct else "info",
                columns=[label], evidence={"count": miss_count, "pct": round(missing_pct, 4)})
        if item["all_missing"]:
            add("all_missing", "Entire column is missing", "integrity", columns=[label], evidence={"rows": n_rows})
        elif item["constant_observed"]:
            add("constant_observed", "Constant observed values detected", "integrity", "info",
                columns=[label], evidence={"observed_count": n_rows - miss_count})
        if _is_identifier(role):
            if miss_count == 0 and unique_count == n_rows:
                complete_unique_identifier = True
            if miss_count:
                add("identifier_missing", "Missing identifier values detected", "integrity", columns=[label],
                    evidence={"count": miss_count})
            if unique_count < n_rows - miss_count:
                add("identifier_duplicates", "Non-unique identifier values detected", "integrity", columns=[label],
                    evidence={"duplicates_among_observed": n_rows - miss_count - unique_count})
        if numerical:
            nonfinite = int(np.isinf(s.to_numpy(dtype=float, na_value=np.nan)).sum())
            if nonfinite:
                add("infinite_values", "Infinite numeric values detected", "integrity", columns=[label],
                    evidence={"count": nonfinite})
            if cfg.run_numeric_sentinels:
                sentinels = _numeric_sentinels(s)
                if sentinels:
                    add("numeric_sentinel_like", "Potential numeric codes detected", "unusual", "review",
                        columns=[label], evidence={"codes": sentinels})
        if cfg.run_string_checks and (pd.api.types.is_object_dtype(s.dtype) or pd.api.types.is_string_dtype(s.dtype) or isinstance(s.dtype, pd.CategoricalDtype)):
            types = _mixed_types(s) if pd.api.types.is_object_dtype(s.dtype) else {}
            if len(types) > 1:
                add("mixed_runtime_types", "Mixed value types detected", "data_types", columns=[label], evidence={"types": types})
            codes = _text_null_codes(s)
            if codes:
                add("null_like_strings", "Potential missing-value codes detected", "missingness", "review",
                    columns=[label], evidence={"codes": codes})
            if (pd.api.types.is_object_dtype(s.dtype) or pd.api.types.is_string_dtype(s.dtype)) and (not types or set(types).issubset({"str"})):
                nonmissing_count = n_rows - miss_count
                if nonmissing_count > 3_000:
                    string_format_sampled = True
                looks_numeric, looks_date = _text_looks_numeric_or_date(s)
                text_hint_method = "sampled" if nonmissing_count > 3_000 else "exact"
                if looks_numeric:
                    add("numeric_like_text", "Numeric-like text detected", "data_types", "review",
                        columns=[label], method=text_hint_method)
                elif looks_date:
                    add("date_like_text", "Date-like text detected", "data_types", "review",
                        columns=[label], method=text_hint_method)
            if unique_count > cfg.string_scan_max_unique:
                label_normalization_skipped += 1
            collisions = _normalized_label_collisions(s, cfg.string_scan_max_unique)
            if collisions:
                add("inconsistent_labels", "Potential inconsistent category labels detected", "integrity", "review",
                    columns=[label], evidence={"variants": collisions})
        if label in special_values:
            vals = special_values[label]
            if not isinstance(vals, (list, tuple)):
                raise TypeError(f"special_values[{label!r}] must be a list/tuple")
            for value in vals:
                try:
                    cnt = int(s.eq(value).fillna(False).sum())
                except (TypeError, ValueError):
                    cnt = 0
                if cnt:
                    add("declared_special_code", "Specified special values detected", "unusual", "review",
                        columns=[label], evidence={"value": _small_string(value), "count": cnt, "pct": round(100 * cnt / max(n_rows, 1), 4)})
    mark("Basic per-column profiling")
    mark("Missing values")
    mark("Type and string checks", "completed" if cfg.run_string_checks else "disabled",
         detail="Mixed runtime types and null-like tokens checked on all non-missing string values" if cfg.run_string_checks else "Disabled in configuration")
    mark("Text numeric/date format hints", "completed" if cfg.run_string_checks else "disabled",
         method="sampled" if string_format_sampled and cfg.run_string_checks else "exact",
         detail="Random sample of up to 3,000 non-missing values per text column")
    mark("Category label normalization", "partially_skipped" if label_normalization_skipped and cfg.run_string_checks else ("completed" if cfg.run_string_checks else "disabled"),
         detail=f"Skipped {label_normalization_skipped} high-cardinality text columns (> {cfg.string_scan_max_unique:,} distinct values)")
    mark("Numeric placeholder codes", "completed" if cfg.run_numeric_sentinels else "disabled")
    mark("Declared special values", "completed" if special_values else "not_configured",
         detail="Extra user-provided codes; not interpreted as missing automatically")
    mark("Identifier consistency", "completed" if any(_is_identifier(m.get('statistical_type')) for m in meta.values()) else "not_configured",
         detail="Requires optional identifier metadata")

    # 03. Missingness patterns, full-data exact matches.
    missing_groups = []
    for member_cols in grouped.values():
        if len(member_cols) > 1:
            missing_groups.append({"columns": member_cols, "column_count": len(member_cols),
                                   "missing_count": int(missing[member_cols[0]].sum()) if not dup_names else None,
                                   "missing_pct": round(100 * int(missing[member_cols[0]].sum()) / max(n_rows, 1), 4) if not dup_names else None})
            add("shared_missing_pattern", "Identical missingness patterns detected", "missingness", "info",
                columns=member_cols, evidence={"column_count": len(member_cols),
                                                "missing_pct": missing_groups[-1]["missing_pct"]})
    missing_groups.sort(key=lambda x: (-x["column_count"], -(x["missing_pct"] or 0)))
    mark("Identical missingness patterns")

    # Related, not identical, absence: Jaccard similarity of missing masks.
    related: list[dict[str, Any]] = []
    eligible_positions = [i for i, count in enumerate(name_missing_counts) if count > 0]
    if not cfg.run_related_missingness:
        mark("Related missingness", "disabled", detail="Disabled in configuration")
    elif n_rows < 1 or len(eligible_positions) < 2:
        mark("Related missingness", "completed", detail="Not enough nonempty patterns")
    elif len(eligible_positions) > cfg.missing_pair_max_columns:
        mark("Related missingness", "skipped", detail=f"More than {cfg.missing_pair_max_columns} columns with missing data")
    else:
        n_sample = min(n_rows, cfg.missing_pair_sample_rows)
        rng = np.random.default_rng(42)
        row_idx = np.sort(rng.choice(n_rows, size=n_sample, replace=False)) if n_sample < n_rows else np.arange(n_rows)
        mask = missing.iloc[row_idx, eligible_positions].to_numpy(dtype=np.float32)
        overlap = mask.T @ mask
        sums = mask.sum(axis=0)
        for a in range(len(eligible_positions)):
            for b in range(a + 1, len(eligible_positions)):
                union = float(sums[a] + sums[b] - overlap[a, b])
                if union <= 0:
                    continue
                sim = float(overlap[a, b] / union)
                if cfg.missing_pair_threshold <= sim < 1.0 - 1e-8:
                    related.append({"columns": [column_labels[eligible_positions[a]], column_labels[eligible_positions[b]]],
                                    "jaccard": round(sim, 5), "rows_sampled": int(n_sample)})
        related.sort(key=lambda x: -x["jaccard"])
        related = related[:35]
        if related:
            add("related_missingness", "Related missingness patterns detected", "missingness", "info",
                columns=sorted(set(c for item in related for c in item["columns"])),
                evidence={"pairs_reported": len(related), "threshold": cfg.missing_pair_threshold,
                          "rows_sampled": n_sample}, method="sampled" if n_sample < n_rows else "exact")
        mark("Related missingness", method="sampled" if n_sample < n_rows else "exact",
             detail=f"Jaccard similarity; {n_sample:,} rows; up to 35 strongest pairs reported")

    # Row completeness distribution (exact, non-disclosive aggregation).
    if n_cols and n_rows:
        fraction = missing.sum(axis=1).to_numpy() / n_cols
        bins = [
            ("0%", fraction == 0), (">0–10%", (fraction > 0) & (fraction <= .10)),
            (">10–25%", (fraction > .10) & (fraction <= .25)),
            (">25–50%", (fraction > .25) & (fraction <= .50)),
            (">50–75%", (fraction > .50) & (fraction <= .75)),
            (">75%", fraction > .75),
        ]
        row_dist = [{"label": label, "count": int(mask.sum()), "pct": round(100 * int(mask.sum()) / n_rows, 4)} for label, mask in bins]
        incomplete_rows = int((fraction > 0).sum())
    else:
        row_dist, incomplete_rows = [], 0
    mark("Row-level missingness")

    # 04. Duplicate rows, full dataset when feasible.
    duplicates = None
    if not cfg.run_duplicate_rows:
        mark("Duplicate rows", "disabled", detail="Disabled in configuration")
    elif complete_unique_identifier:
        duplicates = 0
        mark("Duplicate rows", detail="Proven by a complete unique identifier; no expensive full-row comparison needed")
    elif n_rows * n_cols > cfg.duplicate_rows_max_cells:
        mark("Duplicate rows", "skipped", detail="Above configured cell limit")
    else:
        try:
            duplicates = int(df.duplicated().sum())
            if duplicates:
                add("duplicate_rows", "Duplicate rows detected", "integrity", columns=[], evidence={"count": duplicates})
            mark("Duplicate rows")
        except (TypeError, ValueError) as exc:
            mark("Duplicate rows", "failed", detail=f"Cannot hash some values: {_small_string(exc)}")

    # 04. Identical columns, cheaply shortlisted then fully verified.
    identical_groups: list[list[str]] = []
    if not cfg.run_identical_columns:
        mark("Identical columns", "disabled")
    elif n_cols > cfg.identical_columns_max_columns:
        mark("Identical columns", "skipped", detail="Above configured column limit")
    else:
        try:
            candidates: defaultdict[tuple, list[int]] = defaultdict(list)
            for i in range(n_cols):
                candidates[_fingerprint(df.iloc[:, i])].append(i)
            for members in candidates.values():
                unused = list(members)
                while unused:
                    head = unused.pop(0)
                    equal = [head]
                    remaining = []
                    for j in unused:
                        if df.iloc[:, head].equals(df.iloc[:, j]):
                            equal.append(j)
                        else:
                            remaining.append(j)
                    if len(equal) > 1:
                        identical_groups.append([column_labels[i] for i in equal])
                    unused = remaining
            for group in identical_groups:
                add("identical_columns", "Identical columns detected", "integrity", "review",
                    columns=group, evidence={"column_count": len(group)})
            mark("Identical columns")
        except (TypeError, ValueError) as exc:
            mark("Identical columns", "failed", detail=_small_string(exc))

    # Complete overview and per-column issue counts; all reports stay consistent.
    counts = Counter(c for finding in findings for c in set(finding["columns"]))
    levels = {"review": 2, "info": 1}
    importance = defaultdict(int)
    for finding in findings:
        for col in set(finding["columns"]):
            importance[col] = max(importance[col], levels.get(finding["level"], 0))
    for item in variables:
        item["findings_count"] = counts[item["column"]]
        item["attention"] = "review" if importance[item["column"]] >= 2 else ("info" if importance[item["column"]] else "none")
    variables.sort(key=lambda item: (-int(item["attention"] == "review"), -item["findings_count"], -item["missing_pct"], item["column"]))
    overview = {
        "rows": n_rows,
        "columns": n_cols,
        "memory_bytes": int(df.memory_usage(index=True, deep=True).sum()),
        "dtype_counts": dict(Counter(str(dt) for dt in df.dtypes)),
        "missing_cells": int(missing.to_numpy(dtype=bool).sum()),
        "missing_pct": round(100 * int(missing.to_numpy(dtype=bool).sum()) / max(n_rows * n_cols, 1), 5),
        "columns_with_missing": int(sum(1 for x in name_missing_counts if x)),
        "columns_over_50pct_missing": int(sum(100 * x / n_rows > 50 for x in name_missing_counts)) if n_rows else 0,
        "incomplete_rows": incomplete_rows,
        "incomplete_rows_pct": round(100 * incomplete_rows / max(n_rows, 1), 5),
        "duplicate_rows": duplicates,
        "duplicate_column_names": dup_names,
        "identical_column_groups": identical_groups,
        "shared_missingness_groups": len(missing_groups),
        "variables_in_shared_missingness_groups": sum(g["column_count"] for g in missing_groups),
        "findings_count": len(findings),
        "review_findings_count": sum(x["level"] == "review" for x in findings),
        "info_findings_count": sum(x["level"] == "info" for x in findings),
    }
    return AuditResult(overview, variables, findings, coverage, missing_groups, related, row_dist, cfg)


def _render_html(audit: dict[str, Any]) -> str:
    """Generate offline self-contained HTML with compact charts and filters."""
    overview = audit["overview"]
    variables = audit["variables"]
    findings = audit["findings"]
    groups = audit["missing_groups"]
    related = audit["related_missingness"]
    coverage = audit["audit_coverage"]

    def fmt(x: Any) -> str:
        return f"{x:,}" if isinstance(x, int) else str(x)

    def percent(x: float) -> str:
        return f"{x:.2f}%"

    def pill(label: str, class_name: str = "muted") -> str:
        return f'<span class="pill {class_name}">{escape(label)}</span>'

    def item_header(section: str, title: str, body: str) -> str:
        return f'<section id="{section}" class="section"><header class="section-head"><span class="eyebrow">DATA QUALITY AUDIT</span><h2>{title}</h2><p>{body}</p></header>'

    def metric(title: str, value: Any, subtitle: str = "") -> str:
        return f'<div class="metric"><div class="metric-label">{escape(title)}</div><div class="metric-value">{escape(str(value))}</div><div class="metric-sub">{escape(subtitle)}</div></div>'

    top_missing = sorted((v for v in variables if v["missing_count"] > 0), key=lambda v: -v["missing_pct"])
    missing_bars = "".join(
        f'<div class="bar-row"><div class="bar-name" title="{escape(v["column"], quote=True)}">{escape(v["column"])}</div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{min(100, v["missing_pct"]):.4f}%"></div></div>'
        f'<span class="bar-figure">{percent(v["missing_pct"])}</span></div>'
        for v in top_missing[:30]
    ) or '<p class="muted">No recognized missing values.</p>'

    dtype_colors = ["#416f91", "#9db9a6", "#dcb67a", "#a8a6c4", "#bb8d82", "#789eab"]
    dtype_bars = "".join(
        f'<div class="dtype-block" title="{escape(str(dtype))}: {count}" style="flex:{count};background:{dtype_colors[i % len(dtype_colors)]}"></div>'
        for i, (dtype, count) in enumerate(overview["dtype_counts"].items())
    )
    dtype_legend = "".join(
        f'<span class="legend"><span class="legend-dot" style="background:{dtype_colors[i % len(dtype_colors)]}"></span>{escape(str(dtype))} · {count}</span>'
        for i, (dtype, count) in enumerate(overview["dtype_counts"].items())
    )

    group_rows = "".join(
        f'<tr><td class="wrap">{escape(", ".join(g["columns"]))}</td><td>{g["column_count"]}</td><td>{percent(g["missing_pct"] or 0)}</td></tr>'
        for g in groups
    ) or '<tr><td colspan="3">No identical nonempty missingness patterns.</td></tr>'
    related_rows = "".join(
        f'<tr><td>{escape(" · ".join(g["columns"]))}</td><td>{g["jaccard"]:.3f}</td><td>{g["rows_sampled"]:,}</td></tr>'
        for g in related[:20]
    ) or '<tr><td colspan="3">No related patterns above the configured threshold (or check not run).</td></tr>'
    row_bars = "".join(
        f'<div class="bar-row"><div class="bar-name">{escape(str(g["label"]))} missing</div><div class="bar-track"><div class="bar-fill slate" style="width:{g["pct"]:.4f}%"></div></div><span class="bar-figure">{g["pct"]:.1f}%</span></div>'
        for g in audit["row_missing_distribution"]
    )
    categories = [
        ("data_types", "Data types"), ("missingness", "Missingness"),
        ("integrity", "Integrity"), ("unusual", "Unusual values"),
    ]
    count_by_cat = Counter(f["category"] for f in findings)
    category_metrics = "".join(metric(label, count_by_cat.get(cat, 0), "flagged findings") for cat, label in categories)

    by_col: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    dataset_findings = []
    for finding in findings:
        if not finding["columns"]:
            dataset_findings.append(finding)
        else:
            for column in set(finding["columns"]):
                by_col[column].append(finding)

    def finding_box(finding: dict[str, Any]) -> str:
        evi = escape(json.dumps(finding.get("evidence", {}), ensure_ascii=False))
        return (
            '<div class="finding">'
            f'<div class="finding-row">{pill(finding["level"].upper(), "amber" if finding["level"] == "review" else "muted")}'
            f'<strong>{escape(finding["message"])}</strong></div>'
            f'<div class="finding-evidence">Code: <code>{escape(finding["code"])}</code> · Method: {escape(finding["method"])}</div>'
            f'<div class="finding-evidence"><strong>Evidence:</strong> {evi}</div></div>'
        )

    # Note: build each card on demand in Python; browser only filters and sorts it.
    cards = []
    for v in variables:
        vf = by_col.get(v["column"], [])
        role = v["statistical_type"] or "Not provided"
        description = f'<p class="muted">{escape(v["description"])}</p>' if v["description"] else ""
        inner = "".join(finding_box(f) for f in vf) if vf else '<p class="muted">No findings flagged for this variable.</p>'
        inner += (f'<div class="facts"><span>Missing: <b>{percent(v["missing_pct"])}</b></span>'
                  f'<span>Distinct: <b>{v["unique_values"]:,}</b></span>'
                  f'<span>Zero count: <b>{fmt(v["zero_count"]) if v["zero_count"] is not None else "n/a"}</b></span></div>')
        data = (f'<details class="variable" data-name="{escape(v["column"].casefold(), quote=True)}" '
                f'data-attention="{v["attention"]}" data-findings="{v["findings_count"]}" '
                f'data-missing="{v["missing_pct"]}" data-position="{v["position"]}">'
                f'<summary><span><strong>{escape(v["column"])}</strong>'
                f'<small>{escape(v["dtype"])} · {escape(role)} · {v["findings_count"]} findings</small></span>'
                f'{pill(v["attention"].upper(), "amber" if v["attention"] == "review" else "muted")}'
                '</summary><div class="detail">' + description + inner + '</div></details>')
        cards.append(data)

    audit_lines = "".join(
        f'<tr><td>{escape(c["check"])}</td><td>{pill(c["status"].replace("_", " ").title(), "green" if c["status"] == "completed" else "muted")}</td>'
        f'<td>{escape(c["method"])}</td><td class="wrap">{escape(c["detail"])}</td></tr>'
        for c in coverage
    )
    no_col_findings = "".join(finding_box(f) for f in dataset_findings) or '<p class="muted">No dataset-level findings.</p>'
    # A standalone HTML report; no data is fetched externally.
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Data Quality Audit</title><style>
:root{--ink:#243548;--muted:#6d7d8d;--bg:#f5f7f9;--card:#fff;--border:#dce3e8;--blue:#416f91;--orange:#c38f55}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,Segoe UI,Arial,sans-serif;font-size:14px;line-height:1.55}
a{color:inherit;text-decoration:none}.layout{display:grid;grid-template-columns:240px 1fr;min-height:100vh}
nav{background:#1d344a;color:#edf4f7;padding:30px 18px;position:sticky;top:0;height:100vh;overflow-y:auto}nav .brand{font-weight:780;letter-spacing:.02em;font-size:20px;margin-bottom:6px}nav .sub{font-size:11px;color:#aabeca;margin-bottom:28px}nav a{display:block;padding:11px 12px;border-radius:9px;margin-bottom:4px;color:#d8e5ee;font-size:13px}nav a:hover,nav a:focus{background:#35536b}nav .footer{border-top:1px solid #456078;margin-top:24px;padding:16px 8px;font-size:11px;color:#b1c6d4}
main{padding:34px clamp(18px,4vw,66px);max-width:1550px;width:100%}h1{font-size:29px;letter-spacing:-.045em;margin:5px 0}h2{font-size:22px;letter-spacing:-.03em;margin:0}h3{margin:16px 0 10px;font-size:16px}p{margin:7px 0 12px}.eyebrow{color:#68849a;font-size:10px;font-weight:800;letter-spacing:.13em}
.section{margin-top:38px;scroll-margin-top:22px}.section-head{margin-bottom:19px}.section-head p{color:var(--muted);max-width:760px}.metric-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px}.metric-label{font-size:12px;color:var(--muted)}.metric-value{font-size:25px;font-weight:760;line-height:1.5;letter-spacing:-.03em}.metric-sub{color:var(--muted);font-size:11px;min-height:14px}
.panel{border:1px solid var(--border);border-radius:14px;background:var(--card);padding:20px;margin:15px 0}.panel-note{font-size:12px;color:var(--muted)}.mini-heading{font-size:13px;font-weight:750;margin:0 0 13px}.dtype-bar{height:18px;display:flex;gap:2px;overflow:hidden;border-radius:6px;background:#e9edef}.dtype-block{min-width:2px}.legend-grid{display:flex;gap:12px;flex-wrap:wrap;margin-top:14px}.legend{font-size:12px;color:var(--muted);display:flex;gap:6px;align-items:center}.legend-dot{width:10px;height:10px;border-radius:3px;display:inline-block}
.bar-row{display:grid;grid-template-columns:minmax(130px,260px) 1fr 70px;gap:12px;align-items:center;margin:9px 0}.bar-name{font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bar-track{height:11px;border-radius:5px;background:#edf0f3;overflow:hidden}.bar-fill{background:#c5936b;height:100%;border-radius:4px}.bar-fill.slate{background:#7194aa}.bar-figure{text-align:right;font-size:12px;font-variant-numeric:tabular-nums}
.table-wrap{overflow:auto;max-height:390px}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px 8px;border-bottom:1px solid #e8edf0;font-size:12px;vertical-align:top}th{background:#f3f6f8;position:sticky;top:0;font-weight:700}.wrap{max-width:630px;overflow-wrap:anywhere}
.pill{display:inline-flex;border-radius:20px;font-size:10px;font-weight:700;letter-spacing:.02em;padding:3px 8px;text-transform:uppercase;background:#e9edf1;color:#54697b;white-space:nowrap}.pill.amber{background:#fff0dc;color:#945c25}.pill.green{background:#e4f2e9;color:#357551}
.controls{display:flex;gap:10px;align-items:center;margin:14px 0;flex-wrap:wrap}input,select{border:1px solid var(--border);padding:10px 12px;font:inherit;border-radius:9px;background:white;color:var(--ink)}input{min-width:230px;flex:1}select{min-width:190px}small,.muted{color:var(--muted)}.variable{border:1px solid var(--border);background:white;border-radius:10px;margin:8px 0;overflow:hidden}.variable summary{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:13px 16px;cursor:pointer;list-style:none}.variable summary::-webkit-details-marker{display:none}.variable summary:hover{background:#f8fafb}.variable summary strong{display:block;font-size:13px}.variable summary small{display:block;font-size:11px}.detail{border-top:1px solid var(--border);padding:15px}.finding{border-left:3px solid #b7c9d4;background:#f7f9fa;padding:10px 12px;margin:8px 0;border-radius:4px}.finding-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.finding strong{font-size:12px}.finding-evidence{font-size:11px;color:#607083;margin-top:5px;overflow-wrap:anywhere}.facts{display:flex;flex-wrap:wrap;gap:20px;font-size:12px;margin-top:13px}.empty{padding:18px;color:var(--muted)}.foot-note{font-size:12px;color:var(--muted);margin-top:25px}
@media(max-width:850px){.layout{display:block}nav{position:relative;height:auto;padding:16px}nav a{display:inline-block;padding:6px}nav .footer{display:none}main{padding:20px}.metric-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.bar-row{grid-template-columns:120px 1fr 65px}}
</style></head><body><div class="layout"><nav><div class="brand">Data Quality Audit</div><div class="sub">ONE DATAFRAME · READ ONLY</div>
<a href="#overview">01 · Dataset Overview</a><a href="#types">02 · Data Types</a><a href="#missing">03 · Missing Values</a><a href="#validity">04 · Data Validity</a><a href="#unusual">05 · Unusual Values</a><a href="#summary">06 · Audit Summary</a><a href="#coverage">Audit Coverage</a>
<div class="footer">Signals are not corrections.<br>No data was modified.</div></nav><main>
<div class="eyebrow">AUTOMATED DATA QUALITY REPORT</div><h1>Dataset Quality Overview</h1><p class="muted">A navigable, read-only diagnosis. Expand details for evidence. This report does not perform data cleaning or statistical EDA.</p>
''' + item_header("overview", "01 · Dataset Overview", "Size, structure and overall data completeness.") + '''<div class="metric-grid">''' + (
        metric("Rows", fmt(overview["rows"])) + metric("Columns", fmt(overview["columns"])) +
        metric("Memory", f'{overview["memory_bytes"] / (1024**2):,.1f} MB', "Deep pandas estimate") +
        metric("Flagged findings", fmt(overview["findings_count"]), "Not necessarily errors")
    ) + '''</div><div class="panel"><div class="mini-heading">Stored dtypes</div><div class="dtype-bar">''' + dtype_bars + '''</div><div class="legend-grid">''' + dtype_legend + '''</div></div></section>''' + (
        item_header("types", "02 · Data Types", "Stored pandas dtypes and optional statistical metadata. Statistical types are not inferred without context.") +
        '<div class="panel"><div class="mini-heading">Dtype distribution</div><div class="dtype-bar">' + dtype_bars + '</div><div class="legend-grid">' + dtype_legend + '</div><p class="panel-note">See each variable below for its storage dtype, statistical type and detected representation issues.</p></div></section>'
    ) + (
        item_header("missing", "03 · Missing Values", "Recognized missing values first; related patterns second. Potential codes remain separate from missingness percentages.") +
        '<div class="metric-grid">' + metric("Missing cells", percent(overview["missing_pct"])) +
        metric("Variables affected", f'{overview["columns_with_missing"]:,} / {overview["columns"]:,}') +
        metric("Incomplete rows", percent(overview["incomplete_rows_pct"])) +
        metric("Exact pattern groups", fmt(overview["shared_missingness_groups"])) + '</div>' +
        '<div class="panel"><div class="mini-heading">Missingness by variable · top 30</div>' + missing_bars + '<p class="panel-note">All variables and exact values are available in Variable Diagnostics and audit_findings.json.</p></div>' +
        '<div class="panel"><div class="mini-heading">Share of rows by proportion of missing columns</div>' + row_bars + '</div>' +
        '<div class="panel"><div class="mini-heading">Identical missingness patterns · exact</div><div class="table-wrap"><table><thead><tr><th>Variables</th><th>Count</th><th>Missing</th></tr></thead><tbody>' + group_rows + '</tbody></table></div></div>' +
        '<div class="panel"><div class="mini-heading">Related missingness · Jaccard similarity</div><p class="panel-note">May be calculated from a sample; check Audit Coverage.</p><div class="table-wrap"><table><thead><tr><th>Variables</th><th>Similarity</th><th>Rows checked</th></tr></thead><tbody>' + related_rows + '</tbody></table></div></div></section>'
    ) + (
        item_header("validity", "04 · Data Validity & Consistency", "Structural problems, duplicate rows, duplicate column names and identical columns.") +
        '<div class="metric-grid">' +
        metric("Duplicate rows", "Not checked" if overview["duplicate_rows"] is None else fmt(overview["duplicate_rows"])) +
        metric("Duplicate names", fmt(len(overview["duplicate_column_names"]))) +
        metric("Identical column groups", fmt(len(overview["identical_column_groups"]))) +
        metric("Review findings", fmt(count_by_cat.get("integrity", 0))) + '</div>' +
        '<div class="panel"><div class="mini-heading">Dataset-level issues</div>' + no_col_findings + '<p class="panel-note">Column-level validity findings are listed under Variable Diagnostics.</p></div></section>'
    ) + (
        item_header("unusual", "05 · Unusual Values", "Potential special codes and inconsistent representations. No statistical outlier detection is performed.") +
        '<div class="metric-grid">' + category_metrics +
        '</div><div class="panel"><div class="mini-heading">What is flagged</div><p>Possible null-like strings, conventional numeric placeholder patterns, declared special codes and inconsistent categorical labels.</p><p class="panel-note">These are review signals, not verified invalid values. See Variable Diagnostics for counts and evidence.</p></div></section>'
    ) + (
        item_header("summary", "06 · Audit Summary", "All variables, with those requiring attention shown first. Filter and expand a variable to inspect exact evidence.") +
        '<div class="controls"><input id="variable-search" type="search" placeholder="Search variables..." aria-label="Search variables">' +
        '<select id="variable-filter" aria-label="Filter variables"><option value="all">All variables</option><option value="review">Needs review</option><option value="info">Informational</option><option value="none">No findings</option></select>' +
        '<select id="variable-sort" aria-label="Sort variables"><option value="attention">Most findings</option><option value="missing">Highest missingness</option><option value="name">Alphabetical</option><option value="original">Original column order</option></select></div>' +
        '<div id="variable-list">' + "".join(cards) + '</div><p class="empty" id="empty-results" hidden>No variables match these filters.</p></section>'
    ) + (
        item_header("coverage", "Audit Coverage", "Checks performed, disabled, skipped or failed. Exact and sampled results are marked explicitly.") +
        '<div class="panel table-wrap"><table><thead><tr><th>Check</th><th>Status</th><th>Method</th><th>Detail</th></tr></thead><tbody>' + audit_lines + '</tbody></table></div>' +
        '<p class="foot-note">The report covers one DataFrame and does not infer business semantics. Approximate or unexecuted checks are never presented as exact. Its companion JSON is intended for systematic review.</p></section>'
    ) + '''</main></div><script>
(function(){const list=document.getElementById('variable-list');const search=document.getElementById('variable-search');const filter=document.getElementById('variable-filter');const sorter=document.getElementById('variable-sort');
function update(){const cards=Array.from(list.querySelectorAll('.variable'));const query=search.value.trim().toLowerCase();const rule=filter.value;const order=sorter.value;
cards.sort((a,b)=>{if(order==='missing')return Number(b.dataset.missing)-Number(a.dataset.missing);if(order==='name')return a.dataset.name.localeCompare(b.dataset.name);if(order==='original')return Number(a.dataset.position)-Number(b.dataset.position);const pa={review:2,info:1,none:0};return (pa[b.dataset.attention]-pa[a.dataset.attention])||(Number(b.dataset.findings)-Number(a.dataset.findings))||(Number(b.dataset.missing)-Number(a.dataset.missing));});
let shown=0;cards.forEach(card=>{list.appendChild(card);const ok=card.dataset.name.includes(query)&&(rule==='all'||card.dataset.attention===rule);card.hidden=!ok;if(ok)shown++;});document.getElementById('empty-results').hidden=shown!==0;}
[search,filter,sorter].forEach(x=>x.addEventListener('input',update));update();
})();
</script></body></html>'''
