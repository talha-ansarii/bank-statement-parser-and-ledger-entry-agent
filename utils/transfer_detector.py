from typing import List
from models.transaction import BankTransaction

class TransferDetector:
    def __init__(self):
        self.transfer_keywords = ["UPI", "NEFT", "IMPS", "RTGS", "CHEQUE"]

    def detect_transfer(self, particulars: str) -> bool:
        return any(keyword in particulars.upper() for keyword in self.transfer_keywords)

    def tag_transactions(self, transactions: List[BankTransaction]) -> List[BankTransaction]:
        for txn in transactions:
            txn.is_transfer = self.detect_transfer(txn.particulars)
        return transactions
