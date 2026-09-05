# 2026-08-28 - Issue #27 core metadata 고정 검토 개발 일지

**대상 이슈**: [#27](https://github.com/visualmoney/vm-stock-kis/issues/27)
**범위**: `core-metadata-version = "2.4"` 고정 해제 여부 판단 + 근거 갱신 + 게시 전 검사 추가

---

## 요약

이슈 [#2](https://github.com/visualmoney/vm-stock-kis/issues/2)가 "TestPyPI에서 2.5가
통과하면 이 두 줄을 삭제하세요"라고 남긴 항목을 검토했다.

**결론: 고정을 유지한다. 다만 그 이유가 바뀌었다.**

원래 근거("PyPI가 2.5를 받는지 모른다")는 해소됐다. 그런데 그것이 고정을 풀 이유가
되지는 않는다.

---

## 실측

### 1. 고정을 빼면 hatchling 1.32.0은 2.5를 낸다

```console
$ sed -i '/^core-metadata-version = "2.4"$/d' pyproject.toml && uv build
휠  Metadata-Version: 2.5
sdist Metadata-Version: 2.5
```

### 2. PyPI는 2.5를 받는다

`warehouse/forklift/metadata.py`:

```python
SUPPORTED_METADATA_VERSIONS = {"1.0", "1.1", "1.2", "2.1", "2.2", "2.3", "2.4", "2.5"}
...
if metadata.metadata_version not in SUPPORTED_METADATA_VERSIONS:
```

`twine check --strict`도 2.5 아티팩트에서 통과한다(whl, tar.gz).

### 3. 그런데 올려도 얻는 것이 없다

[PEP 794](https://peps.python.org/pep-0794/)가 2.5에서 추가한 필드는 `Import-Name`과
`Import-Namespace` 둘뿐인데 **hatchling이 이 둘을 쓰지 않는다.**

```console
$ # 2.5로 빌드한 휠의 METADATA
Import-Name 필드 : False
```

우리에게 2.4와 2.5는 **내용이 완전히 같고 버전 숫자만 다르다.**

### 4. 정작 위험은 다음 버전이다

core metadata **2.6이 2026-05에 승인**됐지만 위 목록에 2.6은 없다. PyPI가 아직 받지
않는다. hatchling은 1.32.0에서 기본값을 2.4 → 2.5로 **이미 한 번 올렸다.**

즉 고정의 목적은 "PyPI 수용 여부를 몰라서"가 아니라 **"빌드 백엔드 기본값이 우리
모르게 바뀌는 것을 막는 것"** 이다. 남는 두 줄은 같지만 이유가 다르므로 주석을
바꿔야 한다 — 특히 "삭제하세요"라는 지시는 위험하다.

---

## 변경

### 1. `pyproject.toml` 주석 교체

사실이 아니게 된 서술("PyPI 수용 여부가 확인되지 않았습니다")과 삭제 지시를 지우고,
실제 근거(백엔드 기본값 고정 / 2.6 미지원 / 2.5는 얻는 것 없음)를 적었다.

### 2. `publish.yml`의 `Wheel contents` 스텝에 검사 추가

`twine check`는 **형식만** 본다. PyPI가 그 버전을 받는지는 모른다. 고정이 실수로
지워지거나 백엔드가 기본값을 올려도 게시 시도 전에 잡히도록, 휠 METADATA와 sdist
PKG-INFO의 `Metadata-Version`을 `SUPPORTED_METADATA_VERSIONS`에 대조한다.

---

## 검증 — 스텝 스크립트를 워크플로에서 뽑아 직접 실행

| 케이스 | 입력 | 기대 | 결과 |
|---|---|---|---|
| A | 현행 2.4 아티팩트 | 통과 | ✅ `exit=0`, `{'휠': '2.4', 'sdist': '2.4'}` |
| B | 고정 삭제 → 2.5 | 통과 | ✅ `exit=0`, `{'휠': '2.5', 'sdist': '2.5'}` |
| C | `core-metadata-version = "2.6"` | — | hatchling이 **빌드 단계에서 거부**. 아티팩트가 생기지 않음 |
| D | 2.6으로 다시 포장한 휠 | 실패 | ✅ `exit=1` |

케이스 C가 통과/실패 어느 쪽도 아닌 이유는 hatchling 1.32.0이 아직 2.6을 낼 수
없기 때문이다. **그래서 실제 위험 시나리오(미래 백엔드가 2.6을 기본으로 내는
경우)를 재현하려고 METADATA만 고쳐 다시 포장한 휠로 D를 만들었다.**

```text
::error::휠의 Metadata-Version 이 '2.6' 입니다.
PyPI가 받는 값: ['1.0','1.1','1.2','2.1','2.2','2.3','2.4','2.5'].
pyproject.toml 의 core-metadata-version 고정을 확인하세요.
```

메시지가 원인과 조치 위치를 함께 준다.

---

## 변경 파일

- `pyproject.toml` — `[tool.hatch.build.targets.{wheel,sdist}]` 주석 교체
  (고정 값 `2.4`는 그대로)
- `.github/workflows/publish.yml` — `Wheel contents` 스텝에 `Metadata-Version` 검사

---

## 다음 할 일

- [ ] PyPI가 2.6을 받기 시작하면 `SUPPORTED_METADATA_VERSIONS` 상수를 함께 갱신.
      그때도 판단 기준은 **우리가 실제로 쓰는 필드가 늘어나는지**다.
- [ ] `docs/guidelines/PYPI_RELEASE.md` 에는 관련 서술이 없어 손대지 않았다.
