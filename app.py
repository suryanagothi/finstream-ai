import streamlit as st
import pandas as pd
from extractor import parse_invoice
from validator import validate_invoice

st.set_page_config(page_title="FinStream AI", layout="wide")
st.title("📄 FinStream AI - Smart Document Intelligence")

uploaded_file = st.file_uploader("Upload an Invoice (PDF or JPG/PNG)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    with st.spinner("Extracting invoice entities with Azure Document Intelligence..."):
        file_bytes = uploaded_file.read()
        data = parse_invoice(file_bytes)
        validation = validate_invoice(data)
        
    st.subheader("Invoice Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Vendor", data["vendor_name"] or "N/A")
    col2.metric("Invoice #", data["invoice_id"] or "N/A")
    col3.metric("Date", data["invoice_date"] or "N/A")
    col4.metric("Total", f"${data['invoice_total']:.2f}")
    
    if validation["status"] == "FLAGGED":
        for alert in validation["alerts"]:
            st.error(f"⚠️ {alert}")
    else:
        st.success("✅ Financial Verification Passed: Math & line items match.")
        
    st.subheader("Line Items")
    if data["items"]:
        df = pd.DataFrame(data["items"])
        st.dataframe(df, use_container_width=True)
        st.download_button("Export as CSV", df.to_csv(index=False), "invoice_items.csv")