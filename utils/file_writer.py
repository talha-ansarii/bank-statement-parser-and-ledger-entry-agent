import csv
from typing import List
from models.transaction import BankTransaction

def write_to_csv(transactions: List[BankTransaction], file_name: str):
    fieldnames = ["date", "particulars", "description", "deposits", "withdrawals", "balance", "category", "is_transfer"]
    dict_list = [tx.model_dump() for tx in transactions]

    try:
        with open(file_name, mode="x", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dict_list)
    except FileExistsError:
        with open(file_name, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(dict_list)

    print(f"✅ Transactions written to {file_name}")
