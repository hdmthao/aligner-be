from typing import Optional

from pydantic import BaseModel


class DBModelMixin(BaseModel):
    id: Optional[int] = None
