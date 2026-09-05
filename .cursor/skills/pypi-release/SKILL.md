---
name: pypi-release
description: Follows this repo's PyPI/tag release procedure. Use when releasing to PyPI, cutting a version tag, or updating CHANGELOG for a release.
---

# PyPI release

Follow @docs/guidelines/PYPI_RELEASE.md. Do not paste that guide into the skill.

Checklist:

- [ ] `CHANGELOG.md` for this version
- [ ] Architecture doc drift check (`docs/architecture/ARCHITECTURE.md`)
- [ ] Version comes from the git tag (`hatch-vcs`). Do not hand-edit a version in `pyproject.toml`
- [ ] Tag is `v*.*.*` on the commit you intend to publish
- [ ] Analysis reports only if this is an analysis; status is the issue list

Trusted Publishing and tag rules are in the guide. If anything in the guide and this checklist conflict, the guide wins.
