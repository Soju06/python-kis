from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Protocol

from pykis.streaming.raw.parser import PayloadDecryptor


class KeyStore(Protocol):
    def get_key(self) -> bytes | None: ...
    def get_iv(self) -> bytes | None: ...


@dataclass(slots=True)
class SyncStreamingKeyStore:
    key: bytes | None = None
    iv: bytes | None = None

    def update(self, key: str, iv: str) -> None:
        self.key = _decode_secret(key)
        self.iv = _decode_secret(iv)

    def clear(self) -> None:
        self.key = None
        self.iv = None

    def get_key(self) -> bytes | None:
        return self.key

    def get_iv(self) -> bytes | None:
        return self.iv


@dataclass(slots=True)
class SyncAesCbcDecryptor(PayloadDecryptor):
    key_store: KeyStore

    def decrypt(self, tr_id: str, payload: str) -> str:
        key = self.key_store.get_key()
        iv = self.key_store.get_iv()
        if not key or not iv:
            raise ValueError("Missing AES key/iv")
        data = _decode_payload(payload)
        cipher = _load_cipher(key, iv)
        decryptor = cipher.decryptor()
        padded = decryptor.update(data) + decryptor.finalize()
        text = _unpad(padded)
        return text.decode("utf-8", errors="replace")


def _decode_payload(payload: str) -> bytes:
    text = payload.strip()
    try:
        return base64.b64decode(text, validate=True)
    except Exception:
        return text.encode("utf-8")


def _decode_secret(value: str) -> bytes:
    text = value.strip()
    if not text:
        return b""
    if _looks_like_hex(text):
        try:
            return bytes.fromhex(text)
        except ValueError:
            pass
    try:
        return base64.b64decode(text, validate=True)
    except Exception:
        return text.encode("utf-8")


def _looks_like_hex(text: str) -> bool:
    return len(text) % 2 == 0 and all(ch in "0123456789abcdefABCDEF" for ch in text)


def _load_cipher(key: bytes, iv: bytes):
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    except Exception as exc:
        raise RuntimeError("cryptography is required for AES decryption") from exc

    return Cipher(algorithms.AES(key), modes.CBC(iv))


def _unpad(data: bytes) -> bytes:
    if not data:
        return data
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        return data
    return data[:-pad_len]
