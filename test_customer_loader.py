
from customer_loader import target, upsert_customers


def test_reloading_customers_does_not_duplicate_them():
    target.clear()

    customers = [
        {"customer_id": 101, "name": "Aman"},
        {"customer_id": 102, "name": "Simran"},
    ]

    upsert_customers(customers)
    upsert_customers(customers)

    assert len(target) == 2
    assert target[101]["name"] == "Aman"
