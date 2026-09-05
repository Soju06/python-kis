> **동결 — 2025-12 시점의 스냅샷입니다.** 원래 자리는
> `docs/generated/prompts_rules.md` 였습니다.
>
> 생성기가 만들지 않는 일회성 산출물입니다. 생성기가 만드는 것은
> `docs/generated/API_REFERENCE.md` 하나입니다.
>
> 지금 무엇을 볼 것인가 — `docs/generated/API_REFERENCE.md`, `gh issue list`.

---

**규칙 (Rules)**

- **테스트 실행:** `poetry run pytest` 또는 `.venv\Scripts\python.exe -m pytest`
- **커버리지 HTML 위치:** `--cov-report=html:reports/coverage_html`로 출력 폴더 지정
- **인증 객체:** `KisAuth`는 `virtual` 필드를 명시적으로 전달해야 함 (현재 구현)
- **PyKis 초기화:** 실전/모의 도메인 구분은 생성자 인자(`auth`, `virtual_auth` 또는 위치 인자)로 결정됨
- **호출 제한:** `RateLimiter(rate, period)` 사용, 레거시 kwargs(`max_requests`, `per_seconds`)도 지원 가능
- **응답 변환:** `KisObject.transform_()`를 사용하여 응답 dict → 동적 객체 변환

(이 규칙은 현재 코드베이스 상태에 맞춰 정리된 간단한 요약입니다.)
