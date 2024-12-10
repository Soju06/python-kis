import os
from typing import Literal

import pykis.logging
from pykis import PyKis

try:
    import dotenv

    dotenv.load_dotenv()
except ImportError:
    pass


def load_pykis(
    domain: Literal["real", "virtual"] = "real",
    use_websocket: bool = True,
) -> PyKis:
    pykis.logging.setLevel("DEBUG")

    if domain == "real":
        kis = PyKis(
            id=os.getenv("PYKIS_HTS_ID"),
            account=os.getenv("PYKIS_ACCOUNT_NUMBER"),
            appkey=os.getenv("PYKIS_APPKEY"),
            secretkey=os.getenv("PYKIS_SECRETKEY"),
            use_websocket=use_websocket,
            keep_token=os.getenv("PYKIS_KEEP_TOKEN", "false").lower() == "true",
        )
    else:
        kis = PyKis(
            id=os.getenv("PYKIS_HTS_ID"),
            account=os.getenv("PYKIS_VIRTUAL_ACCOUNT_NUMBER"),
            appkey=os.getenv("PYKIS_APPKEY"),
            secretkey=os.getenv("PYKIS_SECRETKEY"),
            virtual_id=os.getenv("PYKIS_VIRTUAL_HTS_ID"),
            virtual_appkey=os.getenv("PYKIS_VIRTUAL_APPKEY"),
            virtual_secretkey=os.getenv("PYKIS_VIRTUAL_SECRETKEY"),
            use_websocket=use_websocket,
            keep_token=os.getenv("PYKIS_KEEP_TOKEN", "false").lower() == "true",
        )

    return kis
