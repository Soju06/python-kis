# VM-Stock-KIS 뉴스레터 템플릿

이 파일은 **빈 서식**입니다. 발행할 때는 이 파일을 직접 고치지 말고 복사하세요.

```bash
cp docs/NEWSLETTER_TEMPLATE.md archive/docs/YYYY-MM_NEWSLETTER.md
```

발행이 끝난 호는 저장소 루트의 [archive/docs/](../archive/README.md) 에 그대로
둡니다. `archive/` 는 린트와 이름 스윕에서 제외돼 있어 당시 서술과 링크를 손대지
않고 보존할 수 있습니다. 지난 호는
[2025-12_NEWSLETTER.md](../archive/docs/2025-12_NEWSLETTER.md) 를 참고하세요.

> 이 템플릿의 코드 예제는 **0.0.1 이후 이름**(`vmkis` / `VmKis`)을 씁니다.
> 예제를 새로 쓸 때는 `docs/MIGRATION_GUIDE.md` 의 대조표를 확인하세요.

작성 규칙:

- `{{ }}` 로 감싼 부분을 전부 채우고, 해당 호에 해당 없는 절은 **삭제**합니다.
  빈 절을 남기면 다음 호에서 그대로 복사돼 유령 항목이 됩니다.
- 통계·버전·일정은 추측하지 말고 실제 값을 넣습니다. 출처는
  `CHANGELOG.md`, `uv run pytest`, `uv run coverage report`, GitHub Releases 입니다.
- 코드 예제는 붙여넣기 전에 실제로 실행해 봅니다.

---

## 📰 VM-Stock-KIS Monthly Newsletter

### {{YYYY년 M월호}}

---

## 🎯 이번 달의 주요 소식

### 1️⃣ {{제목}}

**변경 사항:**

- {{항목}}
- {{항목}}

**영향:**

- {{사용자에게 무엇이 달라지는가}}

**예제:**

```python
from vmkis import create_client

kis = create_client("configs/account_profiles.yaml")
quote = kis.stock("005930").quote()
```

---

### 2️⃣ {{제목}}

{{내용. 필요한 만큼 절을 늘리고, 남는 절은 지웁니다.}}

---

## 📊 통계

| 항목 | 현황 | 변화 |
|------|------|------|
| **테스트** | {{N}}개 | {{+N}} |
| **커버리지** | {{N}}% | {{+N}} |
| **공개 API** | {{N}}개 | {{±N}} |
| **미해결 이슈** | {{N}}개 | {{±N}} |

---

## 🆕 새로운 기능

### {{기능명}}

```python
from vmkis.logging import enable_json_logging

enable_json_logging()
```

---

## 🐛 버그 수정

| 버그 | 해결 |
|------|------|
| {{증상}} | {{수정 내용}} ([#{{N}}](https://github.com/visualmoney/vm-stock-kis/issues/{{N}})) |

---

## ⚠️ Breaking Change

{{없으면 이 절을 통째로 지웁니다.}}

| 대상 | v{{이전}} | v{{이후}} |
|------|-----------|-----------|
| {{항목}} | `{{옛 표기}}` | `{{새 표기}}` |

마이그레이션 절차는 [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) 를 따르세요.

---

## 📚 문서 업데이트

- {{추가/개정된 문서와 한 줄 설명}}

---

## 🚀 다음 릴리스 (v{{X.Y.Z}})

- **예정 시기**: {{YYYY-MM}}
- **주요 내용**: {{요약}}
- **하위 호환성**: {{유지 / Breaking — 근거}}

릴리스 절차는 [PYPI_RELEASE.md](./guidelines/PYPI_RELEASE.md),
버전 규칙은 [VERSIONING.md](./developer/VERSIONING.md) 를 참고하세요.

---

## 👥 커뮤니티

| 주제 | 수 | 상태 |
|------|-----|------|
| 질문 | {{N}} | {{상태}} |
| 기능 제안 | {{N}} | {{상태}} |
| 버그 리포트 | {{N}} | {{상태}} |

### 기여자

{{이번 호에 기여해 주신 분들. 없으면 절을 지웁니다.}}

---

## 💡 팁 & 트릭

### {{팁 제목}}

```python
from vmkis.utils.retry import with_retry


@with_retry(max_retries=5, initial_delay=2.0)
def reliable_fetch(kis, symbol):
    return kis.stock(symbol).quote()
```

---

## 🔗 유용한 링크

- 📖 [저장소](https://github.com/visualmoney/vm-stock-kis)
- 🐛 [Issues](https://github.com/visualmoney/vm-stock-kis/issues)
- 📦 [PyPI](https://pypi.org/project/vm-stock-kis/)
- 📚 [FAQ](./FAQ.md)
- 🚀 [QUICKSTART](../QUICKSTART.md)
- 📋 [CHANGELOG](../CHANGELOG.md)

원본 프로젝트: [Soju06/python-kis](https://github.com/Soju06/python-kis)

---

## 📝 피드백

- 제안·질문: [Issues](https://github.com/visualmoney/vm-stock-kis/issues)

---

**VM-Stock-KIS**
**발행일**: {{YYYY-MM-DD}}
**다음 호**: {{YYYY-MM-DD}}
