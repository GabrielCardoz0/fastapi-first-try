from pydantic import BaseModel, Field

class TransferSchema(BaseModel):
  from_id: int = Field(..., gte=0)
  to_id: int = Field(..., gte=0)
  amount_cents: int = Field(..., gt=0)
  idempotency_key: str