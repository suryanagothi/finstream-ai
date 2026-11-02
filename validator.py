def validate_invoice(data: dict) -> dict:
    alerts = []
    
    # 1. Sum up line items
    calculated_subtotal = sum(item["amount"] for item in data["items"])
    
    # 2. Check math consistency
    if data["subtotal"] and abs(calculated_subtotal - data["subtotal"]) > 0.5:
        alerts.append(f"Discrepancy: Line items sum ({calculated_subtotal}) does not match subtotal ({data['subtotal']}).")
        
    expected_total = (data["subtotal"] or calculated_subtotal) + data["total_tax"]
    if data["invoice_total"] and abs(expected_total - data["invoice_total"]) > 0.5:
        alerts.append(f"Discrepancy: Total ({data['invoice_total']}) does not equal Subtotal + Tax ({expected_total}).")
        
    return {
        "status": "FLAGGED" if alerts else "VERIFIED",
        "alerts": alerts
    }