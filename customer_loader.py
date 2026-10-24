
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# Simulated target table, keyed by customer_id
target = {}


def upsert_customers(customers):
    for customer in customers:
        customer_id = customer["customer_id"]
        target[customer_id] = customer

    logging.info(
        "Load complete. Unique customers in target: %s",
        len(target)
    )
