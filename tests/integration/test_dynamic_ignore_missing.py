"""Integration tests for KisObject.transform_ ignore_missing behaviors."""

from vmkis.responses.dynamic import KisDynamic, KisObject, KisTransform, KisType


class PassThrough(KisType):
    def transform(self, data):
        return data


class WithIgnoreParam(KisDynamic):
    a = PassThrough()("a")
    b = PassThrough()("b")


def test_transform_ignore_missing_param():
    """Instance-level ignore_missing skips missing fields without raising."""
    obj = KisObject.transform_({"a": 10}, WithIgnoreParam, ignore_missing=True)
    assert hasattr(obj, "a") and obj.a == 10
    # Skipped field should not be set on the instance
    assert "b" not in obj.__dict__


class WithIgnoreClass(KisDynamic):
    __ignore_missing__ = True
    a = PassThrough()("a")
    b = PassThrough()("b")


def test_transform_ignore_missing_class():
    """Class-level __ignore_missing__ skips missing fields without raising."""
    obj = KisObject.transform_({"a": 10}, WithIgnoreClass)
    assert hasattr(obj, "a") and obj.a == 10
    # Skipped field should not be set on the instance
    assert "b" not in obj.__dict__


class VerboseMissing(KisDynamic):
    __verbose_missing__ = True
    a = KisTransform(lambda d: d["a"])("a")


def test_transform_ignore_missing_fields_suppresses_verbose():
    """ignore_missing_fields prevents warnings for extra keys (behavioral no-op)."""
    obj = KisObject.transform_({"a": 1, "extra": 2}, VerboseMissing, ignore_missing_fields={"extra"})
    assert obj.a == 1
