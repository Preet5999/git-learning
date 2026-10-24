def transform_customers(records):
    valid_records = []
    rejected_records = []

    for record in records:
        customer_id = record.get("customer_id", "").strip()
        name = record.get("name", "").strip()
        city = record.get("city", "").strip()
        updated_at = record.get("updated_at", "").strip()

        if not customer_id or not name or not city or not updated_at:
            rejected_records.append({
                "record": record,
                "reason": "Missing required field"
            })
            continue

        try:
            customer_id = int(customer_id)
        except ValueError:
            rejected_records.append({
                "record": record,
                "reason": "Invalid customer_id"
            })
            continue

        valid_records.append({
            "customer_id": customer_id,
            "name": name,
            "city": city,
            "updated_at": updated_at
        })

    return valid_records, rejected_records