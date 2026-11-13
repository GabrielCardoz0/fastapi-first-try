from pydantic import BaseModel, Field

class AccountSchema(BaseModel):
  owner: str = Field(..., min_length=3, max_length=50)
  age: int = Field(..., gt=18)

class AccountDepositSchema(BaseModel):
  value: int = Field(..., gt=0)