from src.schemas.transfers_schema import TransferSchema
from src.core.exceptions import AccountNotFoundError, TransferDontHaveValueError, TransferNotFoundError

async def create_transfer_service(pool, data: TransferSchema):
  
  transfer_exist = await pool.fetchrow('SELECT * FROM transfers WHERE idempotency_key = $1', data.idempotency_key)

  if transfer_exist is not None:
    return dict(transfer_exist)

  from_account = await pool.fetchrow('SELECT * FROM accounts WHERE id = $1;', data.from_id)

  if from_account is None:
    raise AccountNotFoundError('Conta para envio não encontrada.')
  
  to_account = await pool.fetchrow('SELECT * FROM accounts WHERE id = $1;', data.to_id)

  if to_account is None:
    raise AccountNotFoundError('Conta de destino não encontrada.')
  
  if from_account['balance_cents'] < data.amount_cents:
    raise TransferDontHaveValueError('A conta não tem saldo suficiente para tranferência.')
  
  transfer = await pool.fetchrow('INSERT INTO transfers(from_id, to_id, amount_cents,idempotency_key) VALUES($1,$2,$3,$4) ON CONFLICT(idempotency_key) DO NOTHING RETURNING *;', data.from_id, data.to_id, data.amount_cents, data.idempotency_key)
  
  if transfer is None:
    existing = await pool.fetchrow('SELECT * FROM transfers WHERE idempotency_key = $1', data.idempotency_key)
    return dict(existing)
  
  return dict(transfer)


async def get_transfer_by_id_service(pool, id: int):
  transfer = await pool.fetchrow('SELECT * FROM transfers WHERE id = $1', id)

  if transfer is None:
    raise TransferNotFoundError('Transferência não encontrada.')
  
  return dict(transfer)