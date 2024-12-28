
from typing import ClassVar
from pydantic import BaseModel


class BaseSerializer(BaseModel):

    _model: ClassVar = None
    
    def get_model_instance(self):
        if not self._model:
            raise Exception(f"`_model` is not set on serializer {self.__class__.__name__}.")

        return self._model(**self.model_dump())
