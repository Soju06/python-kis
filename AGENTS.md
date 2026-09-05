# VM-Stock-KIS agent instructions

This file is the live source of agent invariants for Cursor.
Do not copy these sentences into To-Do markdown, reports, or extra always-on rules.

Living docs start at [docs/INDEX.md](docs/INDEX.md).
Architecture invariants: [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) §1.1.
Coding/commit habits: [docs/guidelines/AGENT_WORKFLOW_RULES.md](docs/guidelines/AGENT_WORKFLOW_RULES.md).
Scoped rules: `.cursor/rules/`. Session close and PyPI: `.cursor/skills/`.

## Work state

The issue tracker is the only work list. Do not create markdown To-Do lists.

| What | Where |
|---|---|
| Closable work | GitHub issues |
| Next to pick | label `next-up` — **at most 3** |
| Has a predecessor | label `blocked` + first line of the body `선행: #NN` |
| Direction unset | label `needs-decision` — do not start |
| Parent/child | native sub-issues |
| Traps, how to verify | frozen `docs/dev_logs/` + an issue comment that links them |
| Counts (tests, coverage, PyPI version, closed-issue totals) | never write them down; query when needed |

Do not use Discussions, milestones, or Phase 1–4. Phase work finished in 2025-12.

A decision-only issue is valid. Closing condition can be “we decided”, not only “we patched”.

## Session start

```bash
gh issue list --label next-up
gh issue list --label blocked
```

On Windows PowerShell do not pass `--jq` with escaped quotes; the commands above are enough.

If `next-up` is empty, **re-queuing is the first job of the session**.

Before starting an issue, read **all** of its comments.

## When a unit of work starts

One prompt file per work request (not per chat message):
`docs/prompts/YYYY-MM-DD_nn_주제.md`
(`nn` is that day's sequence, two digits, from 2026-08-28 onward).
Do not rename older files.

## When a unit of work ends

- Write `docs/dev_logs/YYYY-MM-DD_nn_주제.md` — traps more than a changelog.
- If you added a regression test, **re-introduce the defect and confirm the test fails**; record that in the log.
- PR body: `Closes #NN`.
- If the issue stays half-done, comment: done-vs-criteria table, remaining `file:line`, traps, log link.
- Drop `blocked` when the predecessor is gone.

## Release

Follow [docs/guidelines/PYPI_RELEASE.md](docs/guidelines/PYPI_RELEASE.md). Update `CHANGELOG.md`. Check architecture docs for drift. Status reports belong in issues, not new reports.

## Document tree (must exist)

Do not invent paths. If you add a doc, update this tree and `docs/INDEX.md` after `ls`.

```text
docs/
├── INDEX.md
├── guidelines/          # API_STABILITY_POLICY, PYPI_RELEASE, DEVELOPER_SETUP,
│                        # GUIDELINES_001_TEST_WRITING, AGENT_WORKFLOW_RULES, …
├── architecture/       # ARCHITECTURE.md
├── dev_logs/            # frozen YYYY-MM-DD_nn_*.md
├── reports/             # frozen; archive/
├── prompts/             # frozen YYYY-MM-DD_nn_*.md
├── generated/           # API_REFERENCE.md only — regenerate, don't hand-edit
└── user/                # USER_GUIDE.md, EXTENDING_API.md, en/

archive/                 # retired docs; see archive/README.md
```
