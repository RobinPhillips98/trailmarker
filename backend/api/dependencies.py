"""Creates and imports dependencies used in the API"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import models  # noqa: F401
import schemas  # noqa: F401
from db import get_db  # noqa: F401
from simulation.core.simulation import run_simulation  # noqa: F401

db_dependency = Annotated[AsyncSession, Depends(get_db)]
