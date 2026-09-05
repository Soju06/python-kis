# 프롬프트 로그: 예제/설정 멀티프로파일 지원

## 프롬프트

- config.example.yaml을 멀티프로파일로 분리하고, virtual/real 단일 프로파일 예제를 추가하며, 예제 스크립트에 `--config`/`--profile`을 도입하라.

## 조치

- `config.example.yaml`: `default` + `configs`(virtual/real) 형태로 재작성
- `config.example.virtual.yaml`, `config.example.real.yaml` 생성
- `pykis/helpers.py`: `load_config(path, profile)` / `create_client(..., profile)` 구현
- `examples/*`: 주요 스크립트에 `--config`/`--profile` 파라미터 추가 및 헬퍼 사용으로 통합
- README들 업데이트

## 결과

- 예제 실행 시 프로파일 선택 가능 (CLI 또는 `PYKIS_PROFILE`)
- 단일/다중 프로파일 파일 모두 지원
- YAML 탭→공백 치환으로 에디터 문법 오류 제거
