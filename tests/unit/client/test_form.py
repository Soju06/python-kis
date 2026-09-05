import pytest

from vmkis.client.form import KisForm


def test_kisform_is_abstract_cannot_instantiate():
    """`KisForm`은 추상 클래스이므로 직접 인스턴스화하면 TypeError가 발생해야 합니다."""
    with pytest.raises(TypeError):
        KisForm()


def test_concrete_subclass_must_implement_build():
    """최소 구현만으로도 인스턴스화되고 `build`가 동작해야 합니다."""

    class MyForm(KisForm):
        def build(self, dict=None):
            # 간단히 받은 dict를 포함한 결과를 반환
            return {"ok": True, "data": dict or {}}

    f = MyForm()
    assert isinstance(f, KisForm)
    res = f.build()
    assert isinstance(res, dict)
    assert res == {"ok": True, "data": {}}

    res2 = f.build({"a": 1})
    assert res2 == {"ok": True, "data": {"a": 1}}


def test_incomplete_subclass_without_build_is_still_abstract():
    """`build`를 구현하지 않으면 서브클래스도 추상 클래스 취급됩니다."""

    class Incomplete(KisForm):
        pass

    with pytest.raises(TypeError):
        Incomplete()
