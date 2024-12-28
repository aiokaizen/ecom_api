from typing import Any
from sqlalchemy import or_, and_
from collections.abc import Iterable

class Filter:
    
    def __init__(self, filters: dict) -> None:
        self.filters = filters


    def build_filters(self):
        """
        Uses the dictionary provided in the init method to create
        sqlalchemy valid filter that can be passed to the select(Model).where() function.
        """

        filters = []
        # This will not work, come back later and redo this method.
        for k, v in self.filters:
            filters.append(k == v)
            if not isinstance(v, Iterable):
                continue

            # @TODO: Support multiple levels
            # for sub_k, sub_v in v:
            #     filters.append(k == v)

        return and_(*filters)
