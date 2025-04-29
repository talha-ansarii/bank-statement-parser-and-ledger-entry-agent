from pydantic import BaseModel, Field
from typing import List

class BankTransaction(BaseModel):
    date: str = Field(description="The date of the transaction in DD-MM-YYYY format")
    particulars: str = Field(description="The transaction description")
    description: str = Field(description="A concise human-readable summary including date.")
    deposits: float = Field(description="Amount deposited")
    withdrawals: float = Field(description="Amount withdrawn")
    balance: float = Field(description="Balance after transaction")
    category: str = Field(default="Uncategorized", description="Auto-categorized type")
    is_transfer: bool = Field(default=False, description="Transfer detection")

class BankTransactionList(BaseModel):
    transactions: List[BankTransaction]
