# 🛠️ PR Summary

## 🌟 요약
어떤 것이 변경되었나요? 간략히 설명해주세요.

인증 토큰을 자동으로 관리하는 기능을 추가했습니다.

## 📊 주요 변경 사항
주요 변경 사항을 적어주세요.

- `utils.workspace.py` 파일을 추가했습니다.
  PyKis 라이브러리의 개인 작업 공간을 관리하는 기능을 추가했습니다.
- `kis.py`에서 `PyKis` 메인 클래스 생성자에 keep_token 인자를 추가했습니다.
  keep_token이 True이면 인증 토큰을 개인 작업 공간에서 자동으로 관리합니다.
- 웹소켓 Ping을 로깅하는 코드를 제거했습니다.


## 🎯 목적 및 영향

- 목적: 왜 이 PR이 필요한가요?
  인증 토큰을 자동으로 관리하는 기능을 추가하여 라이브러리를 손쉽게 사용할 수 있도록 합니다.

- 영향: 이 변경 사항이 어떤 영향을 미치나요?
  토큰 로드 및 저장을 자동으로 처리하므로 비전문 사용자가 토큰을 관리하는 부담이 줄어듭니다.
