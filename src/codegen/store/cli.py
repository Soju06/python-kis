from __future__ import annotations

from codegen.store.pipeline import run_pipeline
from pykis.logging import configure_logging


def main() -> None:
    configure_logging()
    run_pipeline(infer=True, refresh=True)


if __name__ == "__main__":
    main()
