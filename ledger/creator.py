# bank/ledger/creator.py

import pandas as pd
import io

def create_ledger(df, output_csv_path: str):
    # Load existing parsed transactions
  

    # Create new columns for the ledger
    ledger_df = pd.DataFrame({
        "Date": df["date"],
        "Description": df.get("description", df["particulars"]),  # fallback to particulars if description missing
        "Debit": df["withdrawals"].fillna(0),
        "Credit": df["deposits"].fillna(0),
        "Transaction Type": df["category"],
        "Ledger Entry": df["date"]
    })

    # Save the new ledger file

    print(f"✅ Ledger created at {output_csv_path}")
    ledger_csv_buffer = io.StringIO()
    ledger_df.to_csv(ledger_csv_buffer, index=False)
    
    return ledger_csv_buffer
