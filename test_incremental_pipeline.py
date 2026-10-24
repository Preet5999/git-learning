
from datetime import datetime
from pathlib import Path

import pytest

from incremental_pipeline import run_pipeline


def test_watermark_does_not_advance_when_load_fails(tmp_path):
    source_file = tmp_path / "customers.csv"
    watermark_file = tmp_path / "watermark.txt"

    source_file.write_text(
        "customer_id,name,city,updated_at\n"
        "201,Aman,Delhi,2026-10-22 10:00:00\n"
    )
    original_watermark = "2026-10-21 09:00:00"
    watermark_file.write_text(original_watermark)

    def failing_loader(records):
        raise ConnectionError("Simulated load failure")

    with pytest.raises(ConnectionError):
        run_pipeline(
            file_path=source_file,
            watermark_file=watermark_file,
            loader=failing_loader
        )

    assert watermark_file.read_text() == original_watermark

def test_successful_load_advances_watermark(tmp_path):
    source_file = tmp_path / "customers.csv"
    watermark_file = tmp_path / "watermark.txt"

    source_file.write_text(
        "customer_id,name,city,updated_at\n"
        "201,Aman,Delhi,2026-10-22 10:00:00\n"
    )
    watermark_file.write_text("2026-10-21 09:00:00")

    loaded_records = []

    def successful_loader(records):
        loaded_records.extend(records)

    valid_records, rejected_records = run_pipeline(
        file_path=source_file,
        watermark_file=watermark_file,
        loader=successful_loader
    )

    assert len(loaded_records) == 1
    assert len(valid_records) == 1
    assert rejected_records == []
    assert watermark_file.read_text().strip() == "2026-10-22 10:00:00"
