from vmkis.scope.base import KisScopeBase


class DummyKis:
    pass


# KisScopeBase의 생성자 동작(주입한 kis가 인스턴스에 저장되는지)은 간단한 스모크 테스트로 검증목적
def test_kisscopebase_sets_kis_attribute():
    kis = DummyKis()
    scope = KisScopeBase(kis)
    assert hasattr(scope, "kis")
    assert scope.kis is kis


def test_kisscopebase_accepts_different_objects_as_kis():
    # ensure any object can be passed and is preserved
    for val in (None, 123, "x", DummyKis()):
        s = KisScopeBase(val)
        assert s.kis is val
