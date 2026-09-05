import os
import unittest
from typing import Literal

import dotenv

import vmkis.logging
from vmkis import VmKis

# 이 import 와 호출은 `try/except ImportError: pass` 로 감싸여 있었습니다.
# #72 에서 지웠습니다.
#
# python-dotenv 는 이제 `[dependency-groups] test` 의 선언된 의존성이고,
# **pytest 자신이 같은 그룹에 있습니다.** 즉 이 파일을 실행할 수 있는 환경이면
# dotenv 도 반드시 있습니다 — 폴백이 걸릴 수 있는 경우가 없었습니다.
#
# 걸렸다면 더 나빴습니다. 아래 `require_credentials` 가 "저장소 루트에 .env 를
# 만들어 채우세요" 라고 안내하는데, dotenv 가 없으면 .env 를 만들어도 아무 일도
# 일어나지 않습니다. 사용자는 영원히 같은 자리를 돕니다.
dotenv.load_dotenv()

#: 도메인별로 반드시 있어야 하는 환경변수.
#: 저장소 루트에 `.env` 를 두면 python-dotenv 가 자동으로 읽습니다.
REQUIRED_ENV: dict[str, tuple[str, ...]] = {
    "live": (
        "VMKIS_HTS_ID",
        "VMKIS_ACCOUNT_NUMBER",
        "VMKIS_APPKEY",
        "VMKIS_SECRETKEY",
    ),
    "paper": (
        "VMKIS_HTS_ID",
        "VMKIS_APPKEY",
        "VMKIS_SECRETKEY",
        "VMKIS_PAPER_ACCOUNT_NUMBER",
        "VMKIS_PAPER_HTS_ID",
        "VMKIS_PAPER_APPKEY",
        "VMKIS_PAPER_SECRETKEY",
    ),
}


def require_credentials(domain: Literal["live", "paper"] = "live") -> None:
    """자격증명이 없으면 테스트를 **건너뜁니다**.

    이 함수가 없으면 자격증명 없는 환경에서 `VmKis` 생성자가 `ValueError` 를
    내고, 그것이 `setUpClass` 에서 터지므로 pytest 가 **error** 로 보고합니다.
    새로 클론한 사람이 `uv run pytest` 를 처음 돌리면 17개가 빨갛게 뜹니다.

    코드는 멀쩡하고 환경이 없을 뿐입니다. 그건 error 가 아니라 skip 입니다.
    (`tests/performance/test_perf_dummy.py` 가 `RUN_PERF` 로 같은 방식을 씁니다.)

    `unittest.SkipTest` 를 쓰는 이유: 이 함수의 호출자가 전부
    `unittest.TestCase.setUpClass` 인데, unittest 는 여기서 발생한 `SkipTest` 를
    받아 **클래스 전체를 건너뜁니다.** pytest 도 그대로 skip 으로 보고합니다.
    """
    missing = [name for name in REQUIRED_ENV[domain] if not os.getenv(name)]

    if missing:
        raise unittest.SkipTest(
            f"{domain} 도메인 자격증명이 없어 건너뜁니다. "
            f"누락: {', '.join(missing)} — 저장소 루트에 .env 를 만들어 채우세요."
        )


def load_vmkis(
    domain: Literal["live", "paper"] = "live",
    use_websocket: bool = True,
) -> VmKis:
    # 자격증명이 없으면 여기서 skip 으로 빠집니다. 호출자마다 검사할 필요가 없습니다.
    require_credentials(domain)

    vmkis.logging.setLevel("DEBUG")

    if domain == "live":
        kis = VmKis(
            id=os.getenv("VMKIS_HTS_ID"),
            account=os.getenv("VMKIS_ACCOUNT_NUMBER"),
            appkey=os.getenv("VMKIS_APPKEY"),
            secretkey=os.getenv("VMKIS_SECRETKEY"),
            use_websocket=use_websocket,
            keep_token=os.getenv("VMKIS_KEEP_TOKEN", "false").lower() == "true",
        )
    else:
        kis = VmKis(
            id=os.getenv("VMKIS_HTS_ID"),
            account=os.getenv("VMKIS_PAPER_ACCOUNT_NUMBER"),
            appkey=os.getenv("VMKIS_APPKEY"),
            secretkey=os.getenv("VMKIS_SECRETKEY"),
            paper_id=os.getenv("VMKIS_PAPER_HTS_ID"),
            paper_appkey=os.getenv("VMKIS_PAPER_APPKEY"),
            paper_secretkey=os.getenv("VMKIS_PAPER_SECRETKEY"),
            use_websocket=use_websocket,
            keep_token=os.getenv("VMKIS_KEEP_TOKEN", "false").lower() == "true",
        )

    return kis
