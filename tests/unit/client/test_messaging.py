import copy
from typing import Any

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from vmkis.client.messaging import (
    TR_SUBSCRIBE_TYPE,
    TR_UNSUBSCRIBE_TYPE,
    KisWebsocketEncryptionKey,
    KisWebsocketRequest,
    KisWebsocketTR,
)


def test_tr_build_and_str_and_equality_and_hash_and_copy():
    tr = KisWebsocketTR("TR.ID", "K")
    data = tr.build()
    assert data["tr_id"] == "TR.ID"
    assert data["tr_key"] == "K"

    assert str(tr) == "TR.ID.K"

    tr2 = KisWebsocketTR("TR.ID", "K")
    assert tr == tr2
    assert hash(tr) == hash(tr2)

    tr_copy = copy.copy(tr)
    assert isinstance(tr_copy, KisWebsocketTR)
    assert tr_copy == tr

    tr_deep = copy.deepcopy(tr)
    assert tr_deep == tr

    # empty key yields id only
    tr_empty = KisWebsocketTR("X", "")
    assert str(tr_empty) == "X"


def test_tr_equality_with_other_types():
    tr = KisWebsocketTR("A", "B")
    assert not (tr == "A.B")
    assert not (tr == object())


def test_tr_constants():
    assert TR_SUBSCRIBE_TYPE == "1"
    assert TR_UNSUBSCRIBE_TYPE == "2"


def test_websocket_request_build_includes_header_and_body(monkeypatch):
    class DummyKis:
        pass

    # fake approval key function
    class FakeApproval:
        def __init__(self, key: str):
            self.approval_key = key

    def fake_websocket_approval_key(kis_obj: Any, domain=None):
        assert isinstance(kis_obj, DummyKis)
        return FakeApproval("APPKEY-123")

    # patch the function that is imported inside build()
    monkeypatch.setattr("vmkis.api.auth.websocket.websocket_approval_key", fake_websocket_approval_key)

    # body that implements build()
    class SimpleBody:
        def build(self, dict=None):
            return {"x": 1}

    kis = DummyKis()
    req = KisWebsocketRequest(kis=kis, type="T1", body=SimpleBody(), domain="live")
    built = req.build()

    assert "header" in built
    hdr = built["header"]
    assert hdr["approval_key"] == "APPKEY-123"
    assert hdr["custtype"] == "P"
    assert hdr["tr_type"] == "T1"
    assert hdr["content-type"] == "utf-8"

    assert "body" in built and "input" in built["body"]
    assert built["body"]["input"] == {"x": 1}


def test_websocket_request_build_without_body(monkeypatch):
    class DummyKis:
        pass

    def fake_websocket_approval_key(kis_obj: Any, domain=None):
        return type("A", (), {"approval_key": "K"})()

    monkeypatch.setattr("vmkis.api.auth.websocket.websocket_approval_key", fake_websocket_approval_key)

    kis = DummyKis()
    req = KisWebsocketRequest(kis=kis, type="T2", body=None, domain=None)
    built = req.build()
    assert "header" in built
    assert "body" not in built


def test_encryption_key_decrypt_and_text_roundtrip():
    # create 32-byte key and 16-byte iv
    key = b"k" * 32
    iv = b"i" * 16

    ek = KisWebsocketEncryptionKey(iv=iv, key=key)

    # plaintext
    plaintext = b"hello websocket"  # bytes

    # pad
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded = padder.update(plaintext) + padder.finalize()

    # encrypt using same cipher params
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    # decrypt via class
    dec = ek.decrypt(ciphertext)
    assert dec == plaintext
    assert ek.text(ciphertext) == plaintext.decode("utf-8")
