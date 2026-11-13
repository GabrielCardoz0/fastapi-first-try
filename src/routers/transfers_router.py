from fastapi import APIRouter, HTTPException, Request
from src.schemas.transfers_schema import TransferSchema
from src.services.transfers_service import create_transfer_service, get_transfer_by_id_service
from src.core.exceptions import AccountNotFoundError,TransferNotFoundError,TransferDontHaveValueError

transfers_router = APIRouter(tags=['Transferências'])

@transfers_router.post('/transfers', status_code=202)
async def create_transfer(body: TransferSchema, request: Request):
  try:
    transfer = await create_transfer_service(request.app.state.pool, body)

    if transfer['status'] == 'PENDING':
      await request.app.state.queue.put(transfer['id'])

    return { 'transfer': transfer }

  except AccountNotFoundError as erro:
    raise HTTPException(status_code=404, detail=str(erro))
  except TransferDontHaveValueError as erro:
    raise HTTPException(status_code=400, detail=str(erro))
  

@transfers_router.get('/transfers/{id}', status_code=200)
async def get_transfer_by_id(id: int, request: Request):
  try:
    transfer = await get_transfer_by_id_service(request.app.state.pool, id)

    return { 'transfer': transfer }

  except TransferNotFoundError as erro:
    raise HTTPException(status_code=404, detail=str(erro))
