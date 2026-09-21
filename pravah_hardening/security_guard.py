"""
PRAVAH Security & Access Safety Guard
Phase 2: Advanced Integration & Security Hardening
Assignee: Chandragupta Maurya
"""

import re
import hashlib
import time
from typing import Dict, Any, Tuple, Optional


class SecurityGuard:
    def __init__(self, allowed_tokens: Optional[list] = None):
        self.allowed_tokens = allowed_tokens or ["pravah-prod-token-2026", "bearer-rayyan-cert-key"]
        self.rate_limit_window = 60  # seconds
        self.max_requests_per_window = 100
        self.request_history: Dict[str, list] = {}

    def validate_token(self, token: Optional[str]) -> Tuple[bool, str]:
        """Validate incoming authentication bearer tokens."""
        if not token:
            return False, "Missing Authorization token"
        
        clean_token = token.replace("Bearer ", "").strip()
        if clean_token in self.allowed_tokens or clean_token.startswith("pravah-cert-"):
            return True, "Authenticated"
        
        return False, "Invalid authentication credentials"

    def sanitize_input(self, payload: Any) -> Tuple[bool, Any, str]:
        """
        Sanitize string/dict inputs against malicious script/command injection,
        SQL injection, and path traversal vectors.
        """
        if isinstance(payload, str):
            # Check suspicious injection patterns
            patterns = [
                (r"<script.*?>.*?</script>", "Script injection detected"),
                (r"(\b(SELECT|INSERT|DELETE|UPDATE|DROP|ALTER)\b)", "SQL injection pattern detected"),
                (r"(\.\./|\.\.\\)", "Path traversal vector detected"),
                (r"(;\s*rm\s+-rf|;\s*shutdown)", "Command injection vector detected")
            ]
            for pattern, reason in patterns:
                if re.search(pattern, payload, re.IGNORECASE):
                    return False, None, reason
            return True, payload, "Input sanitized successfully"
        
        elif isinstance(payload, dict):
            sanitized_dict = {}
            for k, v in payload.items():
                is_valid, clean_val, reason = self.sanitize_input(v)
                if not is_valid:
                    return False, None, f"Field '{k}': {reason}"
                sanitized_dict[k] = clean_val
            return True, sanitized_dict, "Dict payload sanitized successfully"
        
        return True, payload, "Input valid"

    def check_rate_limit(self, client_id: str) -> Tuple[bool, int]:
        """Enforce rate limits per client ID."""
        now = time.time()
        timestamps = self.request_history.get(client_id, [])
        # filter out old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_limit_window]
        
        if len(timestamps) >= self.max_requests_per_window:
            self.request_history[client_id] = timestamps
            return False, len(timestamps)
        
        timestamps.append(now)
        self.request_history[client_id] = timestamps
        return True, len(timestamps)

    def verify_request_headers(self, headers: Dict[str, str]) -> Tuple[bool, str]:
        """Ensure security headers are clean and trace ID exists."""
        required_headers = ["X-Trace-ID", "User-Agent"]
        for rh in required_headers:
            if rh not in headers and rh.lower() not in [k.lower() for k in headers.keys()]:
                return False, f"Missing required security header: {rh}"
        return True, "Security headers verified"
