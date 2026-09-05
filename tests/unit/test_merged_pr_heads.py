"""머지된 PR 헤드가 origin 에 남으면 실패합니다. (#125)

#119 는 그때 보이던 브랜치를 지우고 끝났습니다. 로컬 추적 목록은
스쿼시 머지 잔여와 prune 안 한 참조를 구분하지 못합니다.

판정은 머지된 PR 의 head 이름과 `git ls-remote --heads` 의 교집합입니다.

`draft/config-schema-v2` 는 머지된 PR 이 없으므로 교집합에 안 들어옵니다.
"""

from __future__ import annotations

import inspect
import json
import os
import pathlib
import re
import subprocess
import urllib.error
import urllib.request

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
KEEP = frozenset({"main"})


class _Unreachable(Exception):
    """origin 또는 GitHub API 에 닿지 못했습니다."""


def leftover_merged_heads(origin_heads: set[str], merged_heads: set[str]) -> set[str]:
    """origin 에 아직 있는 머지된 PR 헤드."""
    return (origin_heads & merged_heads) - KEEP


def _github_repo(url: str) -> tuple[str, str] | None:
    url = url.strip().removesuffix(".git")
    for prefix in ("git@github.com:", "https://github.com/", "ssh://git@github.com/"):
        if url.startswith(prefix):
            parts = url[len(prefix) :].split("/")
            if len(parts) >= 2 and parts[0] and parts[1]:
                return parts[0], parts[1]
    return None


def _parse_ls_remote_heads(text: str) -> set[str]:
    heads: set[str] = set()
    for line in text.splitlines():
        if "\t" not in line:
            continue
        _, ref = line.split("\t", 1)
        prefix = "refs/heads/"
        if ref.startswith(prefix):
            heads.add(ref[len(prefix) :])
    return heads


def _next_link(link: str) -> str | None:
    for part in link.split(","):
        if 'rel="next"' in part:
            match = re.search(r"<([^>]+)>", part)
            if match:
                return match.group(1)
    return None


def _origin_url() -> str:
    try:
        return subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise _Unreachable("origin 원격이 없습니다") from exc


def _origin_heads(url: str) -> set[str]:
    try:
        text = subprocess.check_output(
            ["git", "ls-remote", "--heads", url],
            cwd=REPO_ROOT,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise _Unreachable("git ls-remote --heads 에 실패했습니다") from exc
    return _parse_ls_remote_heads(text)


def _merged_heads(owner: str, repo: str) -> set[str]:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "vm-stock-kis-tests",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    heads: set[str] = set()
    url: str | None = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=100"
    while url:
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                page = json.loads(response.read().decode())
                link = response.headers.get("Link") or ""
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise _Unreachable("GitHub pulls API 에 닿지 못했습니다") from exc
        if not isinstance(page, list):
            raise _Unreachable("GitHub pulls API 응답이 목록이 아닙니다")
        for pull in page:
            if pull.get("merged_at") and (name := (pull.get("head") or {}).get("ref")):
                heads.add(name)
        url = _next_link(link)
    return heads


def _live_leftovers() -> set[str]:
    remote = _origin_url()
    parsed = _github_repo(remote)
    if parsed is None:
        raise _Unreachable(f"origin 이 GitHub 가 아닙니다: {remote}")
    owner, repo = parsed
    return leftover_merged_heads(_origin_heads(remote), _merged_heads(owner, repo))


def test_leftover_checker_catches_the_original_defect() -> None:
    """#125 를 연 날 보이던 5개를 그대로 먹여 봅니다."""
    leftover = {
        "docs/issue94-generated",
        "docs/issue112-96-living-docs",
        "chore/sync-tokens-from-server",
        "docs/issue-111-tutorial-schema",
        "cursor/setup-cloud-agent-env-a721",
    }
    origin = {"main", "draft/config-schema-v2"} | leftover

    found = leftover_merged_heads(origin, leftover)

    assert found == leftover, f"검사기가 스쿼시 잔여를 못 잡습니다: {found}"


def test_draft_branch_without_a_merged_pr_is_kept() -> None:
    found = leftover_merged_heads(
        {"main", "draft/config-schema-v2"},
        {"docs/issue94-generated"},
    )

    assert found == set()


def test_main_is_never_reported() -> None:
    found = leftover_merged_heads({"main"}, {"main"})

    assert found == set()


def test_origin_heads_come_from_ls_remote() -> None:
    """#119 함정: 로컬 추적 목록은 쓰지 않습니다."""
    source = inspect.getsource(_origin_heads)

    assert "ls-remote" in source
    assert "branch" not in source


def test_no_merged_pr_head_lingers_on_origin() -> None:
    try:
        leftovers = _live_leftovers()
    except _Unreachable as exc:
        if os.environ.get("GITHUB_ACTIONS"):
            raise
        pytest.skip(str(exc))

    assert not leftovers, (
        "머지된 PR 헤드가 origin 에 남아 있습니다. "
        "delete_branch_on_merge 가 켜져 있어도 스쿼시 잔여가 생깁니다. "
        f"지우세요: {sorted(leftovers)}"
    )
