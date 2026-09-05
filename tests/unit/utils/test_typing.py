from typing import Protocol

import pytest

from vmkis.utils.typing import Checkable


def test_instantiation_with_builtin_types_and_no_storage():
    # instantiate with common builtin types
    c_int = Checkable(int)
    c_str = Checkable(str)
    c_list = Checkable(list)

    assert isinstance(c_int, Checkable)
    assert isinstance(c_str, Checkable)
    assert isinstance(c_list, Checkable)

    # class defines empty __slots__ -> instances should not have __dict__
    assert not hasattr(c_int, "__dict__")
    assert getattr(c_int, "__slots__", []) == []

    # attempting to set arbitrary attributes on instance raises AttributeError
    with pytest.raises(AttributeError):
        c_int.new_attr = 123


def test_generic_subscription_and_protocol_argument():
    # Using subscription syntax for generic should allow instantiation
    CInt = Checkable[int]
    inst = CInt(int)
    assert isinstance(inst, Checkable)

    # Define a runtime Protocol and use it as the type parameter / argument
    class P(Protocol):
        def foo(self) -> int: ...

    cp = Checkable[P](P)  # runtime accepts Protocol type objects
    assert isinstance(cp, Checkable)


def test_constructor_accepts_non_type_values_without_error():
    # The constructor does not enforce the argument to be a 'type' at runtime.
    # Passing non-type values should not raise; instance is still created.
    c_none = Checkable(None)
    c_number = Checkable(123)
    c_string = Checkable("not-a-type")

    assert isinstance(c_none, Checkable)
    assert isinstance(c_number, Checkable)
    assert isinstance(c_string, Checkable)


def test_multiple_instances_are_independent():
    a = Checkable(int)
    b = Checkable(int)

    # both are instances but independent objects
    assert a is not b
    assert isinstance(a, Checkable) and isinstance(b, Checkable)
