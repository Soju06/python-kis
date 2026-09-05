# 예제

현물 표면은 `01_basic/` 하나입니다. 초·중·고 학습 경로는 없습니다.

```text
examples/
├── 01_basic/    # 시세 · 잔고 · 주문 · 실시간
└── README.md
```

설정은 [01_basic/README.md](01_basic/README.md) 를 보세요. 템플릿을 복사해 채웁니다.

```bash
cp configs/template_account_profiles.yaml configs/account_profiles.yaml
python examples/01_basic/hello_world.py
python examples/01_basic/get_quote.py
```

없는 TR 은 [EXTENDING_API](../docs/user/EXTENDING_API.md) 의 `fetch()` 입니다.
