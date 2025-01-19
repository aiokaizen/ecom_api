from typing import ClassVar, Optional, Type
from pydantic import BaseModel, ConfigDict


class BaseSerializer(BaseModel):
    _model: ClassVar = None

    def get_model_instance(self):
        if not self._model:
            raise Exception(
                f"`_model` is not set on serializer {self.__class__.__name__}."
            )

        return self._model(**self.model_dump())


class BaseORMSerializer(BaseSerializer):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class BaseCreateUpdateSerializer(BaseSerializer):
    model_config = ConfigDict(extra="forbid")
