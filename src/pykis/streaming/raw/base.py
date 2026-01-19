from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StreamingRawModel(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True, populate_by_name=True)
