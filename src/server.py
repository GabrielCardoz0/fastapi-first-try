from fastapi import FastAPI
from src.routers.health_router import health_router
from src.routers.accounts_router import accounts_router
from src.routers.transfers_router import transfers_router
from src.core.database import create_pool
from contextlib import asynccontextmanager
import asyncio
from src.workers.transfer_worker import transfer_worker

@asynccontextmanager
async def lifespan(app: FastAPI):
  app.state.pool = await create_pool()
  app.state.queue = asyncio.Queue()

  pending_transfers = await app.state.pool.fetch("SELECT id FROM transfers WHERE status = 'PENDING' ORDER BY id;")

  for transfer in pending_transfers:
    app.state.queue.put_nowait(transfer['id'])

  worker = asyncio.create_task(transfer_worker(app.state.pool, app.state.queue))

  yield

  worker.cancel()
  await app.state.pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(accounts_router)
app.include_router(transfers_router)