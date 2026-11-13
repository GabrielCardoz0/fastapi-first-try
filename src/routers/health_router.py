from fastapi import APIRouter
from src.core.database import test_pool

health_router = APIRouter()

@health_router.get("/health")
async def get_health():
  await test_pool()
  return {
    "status": "ok"
  }