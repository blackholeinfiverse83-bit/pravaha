"""
PRAVAH Error Boundary Safety & Circuit Breaker Engine
Phase 2: Advanced Integration & Security Hardening
Assignee: Chandragupta Maurya
"""

import time
import logging
from typing import Callable, Any, Dict, Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pravah.error_boundary")


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, name: str, failure_threshold: int = 3, recovery_time: float = 30.0):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_state_change = time.time()

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        now = time.time()
        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_time:
                logger.info(f"[CircuitBreaker:{self.name}] Transitioning OPEN -> HALF-OPEN")
                self.state = "HALF-OPEN"
            else:
                raise CircuitBreakerOpenException(f"Circuit '{self.name}' is OPEN. Requests blocked.")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                logger.info(f"[CircuitBreaker:{self.name}] Service recovered. Transitioning HALF-OPEN -> CLOSED")
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            logger.warning(f"[CircuitBreaker:{self.name}] Exec failure ({self.failure_count}/{self.failure_threshold}): {e}")
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = time.time()
                logger.error(f"[CircuitBreaker:{self.name}] Failure threshold reached. Transitioning -> OPEN")
            raise e


class ErrorBoundary:
    """Error Boundary wrapper to trap runtime exceptions and provide safe fallbacks."""
    
    @staticmethod
    def safe_execute(
        func: Callable,
        fallback_value: Any = None,
        circuit_breaker: Optional[CircuitBreaker] = None,
        *args,
        **kwargs
    ) -> Tuple[bool, Any, Optional[str]]:
        """
        Executes func safely.
        Returns: (success: bool, result_or_fallback: Any, error_message: Optional[str])
        """
        try:
            if circuit_breaker:
                res = circuit_breaker.execute(func, *args, **kwargs)
            else:
                res = func(*args, **kwargs)
            return True, res, None
        except CircuitBreakerOpenException as cbe:
            logger.warning(f"[ErrorBoundary] Circuit breaker triggered: {cbe}")
            return False, fallback_value, f"Circuit Breaker Triggered: {str(cbe)}"
        except Exception as ex:
            logger.error(f"[ErrorBoundary] Caught unhandled exception: {ex}")
            return False, fallback_value, f"Exception Caught: {str(ex)}"
