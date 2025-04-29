from models.transaction import BankTransactionList, BankTransaction
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]


#using langchain with structured output to get accurate results
def get_transaction_data(table_input: str) -> List[BankTransaction]:
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17")

    prompt = PromptTemplate(
        input_variables=["table_data"],
        template="""
You are given a bank statement table. Extract transactions.

Strictly follow this:
- Summarize 'particulars' into a clean 'description' with date included.
- Avoid technical IDs or codes in the description.
- category: Assign a clear and specific categorized label based on the transaction description. Use the following as examples:

    - "Salary" → "Income - Salary"
    - "Uber" → "Expense - Travel"
    - "Zomato", "Swiggy" → "Expense - Food"
    - "Amazon" → "Expense - Software"
    - "ATM Withdrawal" → "Expense - ATM"
    - "Netflix", "Spotify" → "Expense - Entertainment"
    - "Finance Charge" → "Expense - Finance Charge"
    - "EMI" → "Expense - EMI"

- If the transaction does not match these examples, **intelligently infer** the category using the words in the description.
- Do not put transfer as a category.

- If no clear inference can be made, mark as "Uncategorized".

- is_transfer: Detect transfers (e.g., UPI, NEFT, IMPS, RTGS,transfer via check). If the transaction appears to involve sending or receiving money directly between accounts, mark True.


Table:
{table_data}

Return the list of BankTransaction.
"""
    )

    format_prompt = prompt.format(table_data=table_input)
    structured_model = model.with_structured_output(BankTransactionList)
    result = structured_model.invoke(format_prompt)

    print("✅ Transactions parsed", result)
    return result.transactions
