import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

load_dotenv()

ENDPOINT = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
KEY = os.getenv("DOCUMENT_INTELLIGENCE_KEY")

def parse_invoice(file_bytes: bytes) -> dict:
    client = DocumentIntelligenceClient(
        endpoint=ENDPOINT, 
        credential=AzureKeyCredential(KEY)
    )
    
    # Analyze invoice bytes using the prebuilt invoice model
    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        body=file_bytes
    )
    result = poller.result()
    
    extracted = {
        "vendor_name": None,
        "invoice_id": None,
        "invoice_date": None,
        "subtotal": 0.0,
        "total_tax": 0.0,
        "invoice_total": 0.0,
        "items": []
    }
    
    for document in result.documents:
        fields = document.fields
        
        if "VendorName" in fields:
            extracted["vendor_name"] = fields["VendorName"].get("valueString")
        if "InvoiceId" in fields:
            extracted["invoice_id"] = fields["InvoiceId"].get("valueString")
        if "InvoiceDate" in fields:
            extracted["invoice_date"] = str(fields["InvoiceDate"].get("valueDate"))
        if "SubTotal" in fields:
            extracted["subtotal"] = fields["SubTotal"].get("valueCurrency", {}).get("amount", 0.0)
        if "TotalTax" in fields:
            extracted["total_tax"] = fields["TotalTax"].get("valueCurrency", {}).get("amount", 0.0)
        if "InvoiceTotal" in fields:
            extracted["invoice_total"] = fields["InvoiceTotal"].get("valueCurrency", {}).get("amount", 0.0)
            
        # Parse Line Items
        if "Items" in fields:
            for item in fields["Items"].get("valueArray", []):
                item_obj = item.get("valueObject", {})
                extracted["items"].append({
                    "description": item_obj.get("Description", {}).get("valueString", "N/A"),
                    "quantity": item_obj.get("Quantity", {}).get("valueNumber", 1),
                    "unit_price": item_obj.get("UnitPrice", {}).get("valueCurrency", {}).get("amount", 0.0),
                    "amount": item_obj.get("Amount", {}).get("valueCurrency", {}).get("amount", 0.0),
                })
                
    return extracted