
import logging
import time


def retry_operation(operation, max_attempts=3, delay=1):
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()

        except (TimeoutError, ConnectionError):
            if attempt == max_attempts:
                logging.exception(
                    "Operation failed after %s attempts",
                    max_attempts
                )
                raise

            wait_time = delay * (2 ** (attempt - 1))

            logging.warning(
                "Attempt %s failed. Retrying in %s seconds",
                attempt,
                wait_time
            )

            time.sleep(wait_time)
