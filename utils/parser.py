from langchain_docling import DoclingLoader

def extract_tables_from_pdf(file_path: str):
    loader = DoclingLoader(file_path=file_path, export_type="markdown")
    docs = loader.load()

    all_tables = []
    current_table = []
    inside_table = False

    for doc in docs:
        lines = doc.page_content.splitlines()

        for line in lines:
            if line.strip().startswith("|") and line.strip().endswith("|"):
                inside_table = True
                current_table.append(line)
            else:
                if inside_table:
                    if current_table:
                        all_tables.append(current_table)
                        current_table = []
                    inside_table = False

    if current_table:
        all_tables.append(current_table)

    print(f"✅ Found {len(all_tables)} tables in PDF")
    return all_tables
