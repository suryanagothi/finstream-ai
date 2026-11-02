# 📄 FinStream AI

> **Intelligent Financial Document Parsing, Line-Item Verification & Discrepancy Detection Engine**  
> *Built for Microsoft Imagine Cup 2027*

---

## 📌 Executive Summary

Manual verification of financial documents costs small and medium-sized enterprises (SMEs) dozens of hours every week and exposes organizations to billing errors, duplicate charges, and invoice tampering. 

**FinStream AI** automates document-to-ledger ingestion. By pairing **Azure AI Document Intelligence** with rule-based reconciliation logic, it parses semi-structured invoices and receipts, extracts key transactional fields and line items, verifies mathematical consistency, and exports structured data directly for downstream accounting.

---

## 🚀 Key Features

* **Multimodal Extraction:** Ingests invoices, receipts, and billing statements in PDF, PNG, and JPG formats.
* **Prebuilt Financial Document AI:** Uses Azure's `prebuilt-invoice` model to accurately extract key metadata (Vendor, Invoice ID, Invoice Date, Subtotal, Tax, and Grand Total).
* **Deep Line-Item Parsing:** Pulls structured arrays of individual line items (Description, Quantity, Unit Price, Amount) directly into clean tabular dataframes.
* **Automated Reconciliation Engine:** Computes independent mathematical checksums to flag mismatches between line-item aggregates and stated invoice subtotals or taxes.
* **Accounting Export:** One-click export of verified line-item data to CSV/JSON format for integration into enterprise systems.

---

## 🏛 Architecture Overview


┌─────────────────┐        ┌──────────────────────┐       ┌─────────────────────────────────┐
│                 │        │                      │       │                                 │
│   Client UI     │──────▶│   FastAPI / Python   │──────▶│  Azure AI Document Intelligence │
│  (Streamlit)    │        │   Processing Engine  │       │       (prebuilt-invoice)        │
│                 │◀──────│                      │◀──────│                                 │
└─────────────────┘        └──────────┬───────────┘       └─────────────────────────────────┘
                                      │
                                      ▼
                          ┌──────────────────────┐
                          │  Mathematical Audit  │
                          │   & Rule Engine      │
                          │ (Discrepancy Checks) │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │   Structured Data    │
                          │     (CSV / JSON)     │
                          └──────────────────────┘


                          ---

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **AI & Document Intelligence:** Azure AI Document Intelligence SDK (`azure-ai-documentintelligence`)
* **Interface:** Streamlit
* **Data Manipulation:** Pandas
* **Environment & Security:** `python-dotenv`

---

## 📁 Repository Structure

finstream-ai/
│
├── app.py                  # Streamlit application UI
├── extractor.py            # Azure AI Document Intelligence client & parser
├── validator.py            # Audit & line-item reconciliation logic
├── test_connection.py      # Standalone API health check & verification script
├── requirements.txt        # Python package dependencies
├── .env.example            # Sample environment variables file
├── .gitignore              # Git ignore rules for venv and credentials
└── README.md               # Project documentation


---

## ⚡ Quickstart & Setup Guide

### 1. Prerequisites
* Python 3.10 or higher installed
* An active Microsoft Azure subscription (or [Azure for Students](https://azure.microsoft.com/free/students/))
* Azure Document Intelligence resource endpoint and API key

### 2. Clone the Repository
```bash
git clone [https://github.com/suryanagothi/finstream-ai.git](https://github.com/suryanagothi/finstream-ai.git)
cd finstream-ai
