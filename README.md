# 📄 Bank Statement PDF Processor

A Streamlit-based application that processes bank statement PDFs, extracts transaction tables, categorizes them intelligently using LLMs, and exports the cleaned data to CSV format.

---

## 🚀 Features

- 🔍 **PDF Table Extraction:** Automatically splits multi-page PDFs and extracts tables using a parser.
- 🧠 **LLM-Powered Categorization:** Uses intelligent language models to summarize and classify transactions.
- 🔁 **Transfer Detection:** Identifies UPI, IMPS, NEFT, and RTGS transactions automatically.
- 📤 **Export to CSV:** Download all parsed transactions as a CSV file.
- 🖥️ **User-Friendly UI:** Built using Streamlit for a clean and interactive experience.

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/talha-ansarii/bank-statement-parser-and-ledger-entry-agent
   cd bank-statement-parser-and-ledger-entry-agent
   ```

2. **Set up a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠️ Usage

Run the Streamlit app:

```bash
streamlit run main.py
```

Then open your browser to [http://localhost:8501](http://localhost:8501) to interact with the app.

---

## 🧠 Transaction Categorization Rules

- **Description Generation:** Technical fields like `UPI/CR/...` are cleaned into human-readable summaries.
- **Categorization Examples:**
  - "Uber" → `Expense - Travel`
  - "Swiggy" → `Expense - Food`
  - "Bata Footwear" → `Expense - Shopping`
  - Unmatched patterns are set to `Uncategorized`
- **Transfer Detection:** Flags `is_transfer = True` if transaction is a direct money transfer (UPI/NEFT/etc).

---

## 📂 Output

- **Table:** Displays all parsed transactions.
- **CSV:** Downloadable version of the cleaned and structured data.



## 🧪 Example Output

| Date       | Description                            | Deposits | Withdrawals | Balance  | Category              | Is Transfer |
|------------|----------------------------------------|----------|-------------|----------|------------------------|-------------|
| 02-12-2024 | UPI transfer from Rimsha RI on 02-12   | 5000.00  | 0.00        | 13587.96 | Expense - Transfer     | True        |
| 03-12-2024 | Salary from Company XYZ on 03-12       | 45000.00 | 0.00        | 58587.96 | Income - Salary        | False       |
| 03-12-2024 | Purchase from Bata Footwear on 03-12   | 0.00     | 1200.00     | 57387.96 | Expense - Shopping     | False       |

---


