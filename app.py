import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

logging.info("Hello Git")
print('Learning Git - Main Version')
print('Sales pipeline')
print("Testing CI through Pull Request")

def add(a, b):
    return a + b

import os

target_database = os.getenv("TARGET_DATABASE", "dev_db")
print(f"Target database: {target_database}")

def divide(a, b):
    try:
        result = a / b
        logging.info("Division successful: %s", result)
        return result
    except ZeroDivisionError:
        logging.exception("Cannot divide by zero")
        return None

print(divide(10, 2))
print(divide(10, 0))

def run_pipeline():
    logging.info("Pipeline started")

    try:
        # Simulate the main pipeline operation
        logging.info("Reading source data")
        logging.info("Transforming customer data")
        logging.info("Loading target table")

        logging.info("Pipeline completed successfully")

    except Exception:
        logging.exception("Pipeline failed")
        raise


run_pipeline()