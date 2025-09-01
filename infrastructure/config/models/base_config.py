from pathlib import Path

from pydantic import BaseModel, model_validator

from ....core.exceptions.error_codes import ErrorCode
from ..exceptions import MissingConfigValueError


class BaseConfig(BaseModel):
    """ """

    name: str
    path: Path

    @model_validator(mode="after")
    def require_name_and_path(self) -> "BaseConfig":
        if (not self.name) or (not self.path):
            raise MissingConfigValueError(
                message="The config is missing name and/or path",
                err_code=ErrorCode.INF_CFGB_LOOK_521,
            )

        return self
