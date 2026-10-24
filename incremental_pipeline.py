
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path
from config import SOURCE_FILE, WATERMARK_FILE

from customer_transform import transform_customers
from customer_loader import upsert_customers
from retry_utils import retry_operation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def read_watermark(watermark_file):
    return datetime.strptime(
        Path(watermark_file).read_text().strip(),
        TIMESTAMP_FORMAT
    )


def load_incremental_data(file_path, watermark):
    records = []
    lookback_start = watermark - timedelta(days=2)

    with open(file_path, "r", newline="") as file:
        for row in csv.DictReader(file):
            updated_at = datetime.strptime(
                row["updated_at"], TIMESTAMP_FORMAT
            )
            if updated_at > lookback_start:
                records.append(row)

    return records


def save_watermark(watermark_file, new_watermark):
    Path(watermark_file).write_text(
        new_watermark.strftime(TIMESTAMP_FORMAT) + "\n"
    )


def run_pipeline(
    file_path=SOURCE_FILE,
    watermark_file=WATERMARK_FILE,
    loader=upsert_customers
):
    watermark = read_watermark(watermark_file)
    records = load_incremental_data(file_path, watermark)

    valid_records, rejected_records = transform_customers(records)

    logging.info("Extracted: %s", len(records))
    logging.info(
        "Valid: %s | Rejected: %s",
        len(valid_records),
        len(rejected_records)
    )

    # Do not advance the watermark if loading fails.
    if valid_records:
        retry_operation(
            lambda: loader(valid_records),
            max_attempts=3,
            delay=0
        )

    if records:
        latest_timestamp = max(
            datetime.strptime(r["updated_at"], TIMESTAMP_FORMAT)
            for r in records
        )
        new_watermark = max(watermark, latest_timestamp)
        save_watermark(watermark_file, new_watermark)
        logging.info("Watermark advanced to %s", new_watermark)

    logging.info("Pipeline completed successfully")
    return valid_records, rejected_records


if __name__ == "__main__":
    run_pipeline()
