from retry_utils import retry_operation


def test_retry_succeeds_after_temporary_failure():
    attempts = {"count": 0}

    def unreliable_operation():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise TimeoutError("Simulated network timeout")

        return "Data loaded successfully"

    result = retry_operation(
        unreliable_operation,
        max_attempts=3,
        delay=0
    )

    assert result == "Data loaded successfully"
    assert attempts["count"] == 3