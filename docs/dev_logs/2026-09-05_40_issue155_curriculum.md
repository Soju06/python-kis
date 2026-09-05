# 2026-09-05 - 초·중·고 커리큘럼 접기 일지

## 작업 내용

이슈 [#155](https://github.com/visualmoney/vm-stock-kis/issues/155).
`examples/02_intermediate/` · `examples/03_advanced/` 를 지웠습니다.
`01_basic` 은 그대로입니다. 펼치거나 합치거나 archive 하지 않았습니다.

살아 있는 문서에서 그 경로와 SIMPLEKIS 「예정」을 뺐습니다.
`test_examples_layout.py` 가 폴더가 돌아오면 실패합니다.
결함 재현: `02_intermediate` 를 다시 두면 `test_curriculum_folders_are_gone` 이 실패했습니다.
예제 README 개수 검사는 4에서 2로 맞췄습니다 (`examples/` · `01_basic/`).

`#30` 은 이미 닫혀 있습니다. `#33`–`#36` 은 열지 않았습니다.
`v1.0.0` 은 찍지 않았습니다.

## 변경 파일

- `examples/02_intermediate/` · `examples/03_advanced/` (삭제)
- `examples/README.md`
- `README.md`
- `docs/SIMPLEKIS_GUIDE.md`
- `tests/unit/test_examples_layout.py`
- `CHANGELOG.md`
- `docs/prompts/2026-09-05_40_issue155_curriculum.md`
- `docs/dev_logs/2026-09-05_40_issue155_curriculum.md`
