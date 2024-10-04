from fastapi import APIRouter,Depends,status
from typing import  Union
from repository import task, user
router = APIRouter()
# ------------------------------------ tasks-----------------------------------------------------------------------
router.include_router(task.router)
#------------------------------------ user-----------------------------------------------------------------------
router.include_router(user.router)
