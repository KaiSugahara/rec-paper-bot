from datetime import datetime
from typing import Any

from airflow.sdk import task


@task
def get_now(flag: Any) -> str:
    """Get the current time

    Args:
        flag (Any): A flag parameter (not used in the function)

    Returns:
        str: The current time in ISO 8601 format
    """

    return datetime.now().isoformat(timespec="seconds")
