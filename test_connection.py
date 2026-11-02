import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError

# Load credentials from .env
load_dotenv()

ENDPOINT = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
KEY = os.getenv("DOCUMENT_INTELLIGENCE_KEY")

print("Checking configuration...")
if not ENDPOINT or not KEY:
    print("❌ Error: DOCUMENT_INTELLIGENCE_ENDPOINT or DOCUMENT_INTELLIGENCE_KEY missing from .env file.")
    exit(1)

print(f"Target Endpoint: {ENDPOINT}")

try:
    client = DocumentIntelligenceClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(KEY)
    )

    print("Connecting to Azure and testing 'prebuilt-invoice' model with sample invoice...")

    # Public Microsoft sample invoice URL for testing
    sample_invoice_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-invoice.pdf"

    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        AnalyzeDocumentRequest(url_source=sample_invoice_url)
    )
    result = poller.result()

    print("\n✅ Connection Successful! Azure Document Intelligence is working.\n")

    for idx, document in enumerate(result.documents):
        print(f"--- Document #{idx + 1} Extracted Details ---")
        vendor = document.fields.get("VendorName", {}).get("valueString")
        invoice_id = document.fields.get("InvoiceId", {}).get("valueString")
        total = document.fields.get("InvoiceTotal", {}).get("valueCurrency", {}).get("amount")

        print(f"Vendor Name : {vendor}")
        print(f"Invoice ID  : {invoice_id}")
        print(f"Total Amount: {total}")

except ClientAuthenticationError:
    print("\n❌ Authentication Failed: The API key is invalid for this resource.")
except HttpResponseError as e:
    print(f"\n❌ Request Error: {e.message}")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")