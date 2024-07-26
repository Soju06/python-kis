import os
from typing import Literal

import dotenv

import pykis.logging
from pykis import PyKis

dotenv.load_dotenv()


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
            token=token_path if os.path.exists(token_path := os.getenv("PYKIS_TOKEN_PATH", "")) else None,
            use_websocket=use_websocket,
        )
        kis.token.save(token_path)
    else:
        kis = PyKis(
            id=os.getenv("PYKIS_VIRTUAL_ID"),
            account=os.getenv("PYKIS_VIRTUAL_ACCOUNT_NUMBER"),
            appkey=os.getenv("PYKIS_APPKEY"),
            secretkey=os.getenv("PYKIS_SECRETKEY"),
            token=token_path if os.path.exists(token_path := os.getenv("PYKIS_TOKEN_PATH", "")) else None,
            virtual_id=os.getenv("PYKIS_VIRTUAL_ID"),
            virtual_appkey=os.getenv("PYKIS_VIRTUAL_APPKEY"),
            virtual_secretkey=os.getenv("PYKIS_VIRTUAL_SECRETKEY"),
            virtual_token=(
                virtual_token_path
                if os.path.exists(virtual_token_path := os.getenv("PYKIS_VIRTUAL_TOKEN_PATH", ""))
                else None
            ),
            use_websocket=use_websocket,
        )
        kis.token.save(token_path)
        kis.primary_token.save(virtual_token_path)

    return kis
