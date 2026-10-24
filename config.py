
import os

PIPELINE_ENV = os.getenv("PIPELINE_ENV", "dev").lower()

ALLOWED_ENVIRONMENTS = {"dev", "uat", "prod"}

if PIPELINE_ENV not in ALLOWED_ENVIRONMENTS:
    raise ValueError(
        f"Invalid PIPELINE_ENV: {PIPELINE_ENV}. "
        f"Allowed values: {sorted(ALLOWED_ENVIRONMENTS)}"
    )

SOURCE_FILE = os.getenv("SOURCE_FILE", "customers.csv")
WATERMARK_FILE = os.getenv("WATERMARK_FILE", "watermark.txt")
