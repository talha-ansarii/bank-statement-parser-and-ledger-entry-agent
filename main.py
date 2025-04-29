import streamlit as st
from utils.parser import extract_tables_from_pdf
from utils.transfer_detector import TransferDetector
from utils.file_writer import write_to_csv
from utils.extractor import get_transaction_data
from ledger.creator import create_ledger
from concurrent.futures import ThreadPoolExecutor, as_completed
from tempfile import NamedTemporaryFile

import os
import PyPDF2
import pandas as pd
import io
from typing import List

# Function to split uploaded PDF into 2-page chunks
def split_pdf_stream(uploaded_pdf):
    reader = PyPDF2.PdfReader(uploaded_pdf)
    temp_files = []

    num_pages = len(reader.pages)
    for i in range(0, num_pages, 2):
        writer = PyPDF2.PdfWriter()
        writer.add_page(reader.pages[i])
        if i + 1 < num_pages:
            writer.add_page(reader.pages[i + 1])

        temp_file = NamedTemporaryFile(delete=False, suffix=f'_pages_{i + 1}-{min(i + 2, num_pages)}.pdf')
        with open(temp_file.name, 'wb') as f_out:
            writer.write(f_out)

        temp_files.append(temp_file.name)

    return temp_files

# Function to delete temporary files
def delete_temp_files(temp_files):
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except Exception as e:
            st.error(f"Error deleting file {temp_file}: {e}")

def process_table(index, table):
    table_str = "\n".join(table)
    transactions = get_transaction_data(table_str)
    return index, transactions

# Streamlit App
st.title("📄 Bank Statement PDF Processor")
uploaded_pdf = st.file_uploader("Upload your bank statement PDF", type=["pdf"])

if uploaded_pdf:
    output_buffer = io.StringIO()
    with st.spinner("Splitting PDF..."):
        temp_pdfs = split_pdf_stream(uploaded_pdf)
        st.success(f"Split into {len(temp_pdfs)} files")

    all_flat_transactions = []

    for i, temp_pdf in enumerate(temp_pdfs):
        st.header(f"🔍 Processing file {i+1}/{len(temp_pdfs)}")

        tables = extract_tables_from_pdf(temp_pdf)
        if not tables:
            st.warning(f"No tables found in {os.path.basename(temp_pdf)}")
            continue

        st.subheader("📋 Extracted Tables:")
        for idx, table in enumerate(tables):
            table_text = "\n".join(table)
            st.text_area(f"Table {idx+1}", table_text, height=200)
            
            

        all_transactions = [None] * len(tables)

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(process_table, idx, table) for idx, table in enumerate(tables)]
            for future in as_completed(futures):
                index, transactions = future.result()
                all_transactions[index] = transactions

        flat_transactions = [txn for txns in all_transactions if txns for txn in txns]
        all_flat_transactions.extend(flat_transactions)
        data_dicts: List[dict] = [txn.dict() for txn in flat_transactions]

        # Convert to DataFrame
        df = pd.DataFrame(data_dicts)

        # Display as a Streamlit table
        st.header("📊 Transaction Table")
        st.dataframe(df)
        # st.text_area(f"Table {idx+1}", all_flat_transactions, height=200)
        st.success(f"✅ Done processing pdf {i+1} with {len(flat_transactions)} transactions.")

    # Clean up
    delete_temp_files(temp_pdfs)

    if all_flat_transactions:
        st.header("📈 All Transactions")
        data_dicts: List[dict] = [txn.dict() for txn in all_flat_transactions]
        df = pd.DataFrame(data_dicts)
        st.dataframe(df)

        csv_buffer = io.StringIO()
        ledger_csv_buffer = create_ledger(df, output_csv_path=csv_buffer)
        df.to_csv(csv_buffer, index=False)
        
        st.download_button(
            label="📥 Download bank statement",
            data=csv_buffer.getvalue(),
            file_name="transactions.csv",
            mime="text/csv"
        )
        st.download_button(
            label="📥 Download Ledger",
            data=ledger_csv_buffer.getvalue(),
            file_name="ledger.csv",
            mime="text/csv"
        )
    else:
        st.warning("No transactions found in the PDF.")
