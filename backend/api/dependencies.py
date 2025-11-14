from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

import models  # noqa: F401
import schemas
from db import get_db  # noqa: F401

db_dependency = Annotated[Session, Depends(get_db)]