from src.schemas.accounts_schema import AccountSchema, AccountDepositSchema
from src.core.exceptions import OwnerAlreadyExistsError, AccountNotFoundError

async def create_account_service(pool, data: AccountSchema):
  owner_exists = await pool.fetchrow('SELECT * FROM accounts WHERE owner = $1;', data.owner)

  if owner_exists is not None:
    raise OwnerAlreadyExistsError('Já existe uma conta com esse dono.')
  
  account = await pool.fetchrow('INSERT INTO accounts(owner, age, balance_cents) VALUES($1, $2, $3) RETURNING *;', data.owner, data.age, 0)

  return dict(account)


async def get_account_by_id_service(pool, id: int):
  account = await pool.fetchrow('SELECT * FROM accounts WHERE id = $1;', id)

  if account is None:
    raise AccountNotFoundError('Conta não encontrada.')

  return dict(account)


async def account_deposit_service(pool, id, data: AccountDepositSchema):
  account = await pool.fetchrow('SELECT * FROM accounts WHERE id = $1;', id)

  if account is None:
    raise AccountNotFoundError('Conta não encontrada.')
  
  updated_account = await pool.fetchrow('UPDATE accounts SET balance_cents = balance_cents + $1, updated_at = now() WHERE id = $2 RETURNING *;', data.value, id)

  return dict(updated_account)