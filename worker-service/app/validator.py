def validate_record(record: dict):
    errors = []

    store_id = str(record.get("store_id", "")).strip()
    sku = str(record.get("sku", "")).strip()

    try:
        price = float(record.get("price", 0))
    except Exception:
        price = None

    try:
        offer_price = float(record.get("offer_price", 0))
    except Exception:
        offer_price = None

    try:
        stock = int(record.get("stock", 0))
    except Exception:
        stock = None

    if not store_id:
        errors.append("store_id is required")

    if not sku:
        errors.append("sku is required")

    if price is None or price <= 0:
        errors.append("price must be greater than 0")

    if offer_price is not None and price is not None and offer_price > price:
        errors.append("offer_price must be less than or equal to price")

    if stock is None or stock < 0:
        errors.append("stock must be greater than or equal to 0")

    return errors