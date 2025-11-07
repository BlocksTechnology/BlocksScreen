import os
import pytest
from lib.logger_manager import get_logger, set_correlation_id

LOG_PATH = "test_logs/test_app.log"

@pytest.fixture
def setup_logger():
    # Remove ficheiro antigo
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    logger = get_logger(
        name="TestLogger",
        env="dev",  # deve ativar DEBUG
        log_file=LOG_PATH,
        json_console=False,
        service="test-service"
    )
    return logger

def test_debug_logging_in_dev(setup_logger):
    set_correlation_id("test-corr-id")
    setup_logger.debug("Debug message for test", extra={"test_key": "value"})

    # wait for queuelistener
    import time
    time.sleep(0.1)

    assert os.path.exists(LOG_PATH), "Log file was not created"

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        logs = f.readlines()

    assert any("debug message for test" in line.lower() for line in logs), "DEBUG message not found in log"
    assert any('"correlation_id": "test-corr-id"' in line for line in logs), "Correlation ID not found"