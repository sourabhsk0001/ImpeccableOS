import time
import logging
import json
from typing import Dict, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s", "level":"%(levelname)s", "module":"%(name)s", "message": %(message)s}'
)

logger = logging.getLogger("impeccable.telemetry")


class ExecutionTracer:
    """Records execution latency, token accounting, and retrieval steps for observability."""

    def __init__(self, trace_id: str, operation_name: str):
        self.trace_id = trace_id
        self.operation_name = operation_name
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.metadata: Dict[str, Any] = {}
        self.metrics: Dict[str, Any] = {}

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        duration_ms = (self.end_time - self.start_time) * 1000
        self.metrics["duration_ms"] = round(duration_ms, 2)
        if exc_type is not None:
            self.metadata["error"] = str(exc_val)
        self.flush()

    def record_tokens(self, prompt_tokens: int, completion_tokens: int):
        self.metrics["prompt_tokens"] = prompt_tokens
        self.metrics["completion_tokens"] = completion_tokens
        self.metrics["total_tokens"] = prompt_tokens + completion_tokens

    def set_attribute(self, key: str, value: Any):
        self.metadata[key] = value

    def flush(self):
        log_payload = {
            "trace_id": self.trace_id,
            "operation": self.operation_name,
            "metrics": self.metrics,
            "attributes": self.metadata
        }
        logger.info(json.dumps(log_payload))
