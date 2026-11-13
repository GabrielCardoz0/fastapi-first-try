async def transfer_worker(pool, queue):
  while True:
    transfer_id = await queue.get()
    try:
      async with pool.acquire() as connection, connection.transaction():
        transfer = await connection.fetchrow("SELECT * FROM transfers WHERE id = $1 AND status = 'PENDING' FOR UPDATE;", transfer_id)

        if transfer is None:
          continue

        from_account = await connection.fetchrow("UPDATE accounts SET balance_cents = balance_cents - $1 WHERE id = $2 AND balance_cents >= $1 RETURNING *;", transfer["amount_cents"], transfer["from_id"])

        if from_account is None:
          await connection.fetchrow("UPDATE transfers SET status = 'FAILED' WHERE id = $1;", transfer_id)
          continue

        await connection.fetchrow("UPDATE accounts SET balance_cents = balance_cents + $1 WHERE id = $2 RETURNING *;", transfer["amount_cents"], transfer["to_id"])

        await connection.fetchrow("UPDATE transfers SET status = 'COMPLETED' WHERE id = $1;", transfer_id)

    except Exception as erro:
      print("Erro ao processar transferência", transfer_id, erro)
    finally:
      queue.task_done()
