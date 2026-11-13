from fastapi import APIRouter, HTTPException, Request
from src.schemas.accounts_schema import AccountSchema,AccountDepositSchema
from src.services.accounts_service import create_account_service,get_account_by_id_service,account_deposit_service
from src.core.exceptions import OwnerAlreadyExistsError,AccountNotFoundError

accounts_router = APIRouter(tags=['Contas'])

@accounts_router.post('/accounts', status_code=201)
async def create_account(body: AccountSchema, request: Request):
  try:
    account = await create_account_service(request.app.state.pool, body)

    return { 'account': account }

  except OwnerAlreadyExistsError as erro:
    raise HTTPException(status_code=409, detail=str(erro))


@accounts_router.get('/accounts/{id}', status_code=200)
async def get_account_by_id(id: int, request: Request):
  try:
    account = await get_account_by_id_service(request.app.state.pool, id)

    return { 'account': account }
  except AccountNotFoundError as erro:
    raise AccountNotFoundError(status_code=404, detail=str(erro))
  

@accounts_router.post('/accounts/{id}/deposit', status_code=201)
async def account_deposit(id: int, body: AccountDepositSchema, request: Request):
  try:
    account = await account_deposit_service(request.app.state.pool, id, body)

    return { 'account': account }

  except AccountNotFoundError as erro:
    raise HTTPException(status_code=404, detail=str(erro))