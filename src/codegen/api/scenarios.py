from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from codegen.core.types import JsonValue


class AugmentScenario(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    description: str | None = None
    request_template: str | None = None
    expected: str | None = None
    store_as: str | None = None
    conditions: dict[str, JsonValue] | None = None

    def output_filename(self) -> str:
        return self.store_as or f"{self.id}.json"


class ScenarioConfig(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    scenarios: list[AugmentScenario] = Field(default_factory=list)
    request_templates: dict[str, dict[str, dict[str, JsonValue]]] = Field(default_factory=dict)

    def ensure_default(self) -> ScenarioConfig:
        if self.scenarios:
            return self
        return ScenarioConfig(
            scenarios=[
                AugmentScenario(
                    id="success",
                    description="Valid request with expected parameters",
                    request_template="default",
                    expected="valid_response",
                    store_as="success.json",
                )
            ],
            request_templates=self.request_templates,
        )


def load_scenarios(path: Path) -> ScenarioConfig:
    if not path.exists():
        return ScenarioConfig().ensure_default()
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid scenario config root: {path}")
    config = ScenarioConfig.model_validate(data)
    return config.ensure_default()


__all__ = ["AugmentScenario", "ScenarioConfig", "load_scenarios"]
