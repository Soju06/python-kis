"""이슈 #15 — `KisNotFoundError` 이름 충돌.

같은 이름의 서로 다른 클래스가 두 곳에 있었다.

    vmkis/client/exceptions.py      KisHTTPError 상속.  HTTP 404
    vmkis/responses/exceptions.py   KisException 상속.  조회 결과 없음

문제는 이름이 겹친다는 것 자체가 아니라, **공개 모듈 `vmkis.exceptions` 가
한 번도 발생하지 않는 쪽(HTTP 404)을 내보내고 있었다**는 것이다. 공개 API 대로
잡은 사용자의 핸들러가 절대 실행되지 않았다.

`client.exceptions.KisNotFoundError` 별칭은 제거됐다 (#164).
"""

import pytest

import vmkis.exceptions as public
from vmkis.client.exceptions import KisHTTPNotFoundError
from vmkis.responses.exceptions import KisNotFoundError


class TestPublicExportPointsAtTheRaisedClass:
    def test_public_notfound_is_the_one_actually_raised(self):
        """`vmkis.exceptions.KisNotFoundError` 로 잡으면 실제 예외가 잡혀야 한다."""
        assert public.KisNotFoundError is KisNotFoundError

    def test_public_notfound_is_not_the_http_one(self):
        assert public.KisNotFoundError is not KisHTTPNotFoundError

    def test_http_variant_is_exported_under_its_own_name(self):
        assert public.KisHTTPNotFoundError is KisHTTPNotFoundError

    def test_both_names_are_in_all(self):
        assert "KisNotFoundError" in public.__all__
        assert "KisHTTPNotFoundError" in public.__all__


class TestTheTwoClassesAreDistinct:
    def test_different_classes(self):
        assert KisNotFoundError is not KisHTTPNotFoundError

    def test_neither_catches_the_other(self):
        """상속 계층이 달라 한쪽으로 다른 쪽을 잡을 수 없다.

        이것이 원래 버그의 본질이다 — 어느 것을 import 했는지에 따라
        `except` 가 조용히 다르게 동작했다.
        """
        assert not issubclass(KisNotFoundError, KisHTTPNotFoundError)
        assert not issubclass(KisHTTPNotFoundError, KisNotFoundError)


class TestClientPathHasNoNotFoundAlias:
    def test_old_client_path_raises(self):
        """`vmkis.client.exceptions.KisNotFoundError` 별칭은 제거됐다 (#164)."""
        from vmkis.client import exceptions as ce

        with pytest.raises(AttributeError):
            _ = ce.KisNotFoundError

    def test_http_name_remains(self):
        from vmkis.client import exceptions as ce

        assert "KisNotFoundError" not in ce.__all__
        assert "KisHTTPNotFoundError" in ce.__all__
        assert ce.KisHTTPNotFoundError is KisHTTPNotFoundError

    def test_unknown_attribute_still_raises(self):
        from vmkis.client import exceptions as ce

        with pytest.raises(AttributeError):
            _ = ce.NoSuchThing
