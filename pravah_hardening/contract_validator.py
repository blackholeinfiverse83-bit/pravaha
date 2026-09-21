"""
PRAVAH System Contract Boundary Validator
Phase 2: Advanced Integration & Security Hardening
Assignee: Chandragupta Maurya
"""

import json
import ssl
import urllib.request
from typing import Dict, Any, Tuple


class ContractValidator:
    """Validates contract compliance for Pravah microservices."""
    
    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def validate_masterdb_contract(self, url: str) -> Tuple[bool, Dict[str, Any]]:
        """Validate MASTERDB Core OpenAPI schema and contract boundaries."""
        try:
            req = urllib.request.Request(f"{url}/openapi.json", headers={"User-Agent": "Pravah-ContractValidator/2.0"})
            with urllib.request.urlopen(req, timeout=5, context=self.ctx) as resp:
                if resp.status == 200:
                    spec = json.loads(resp.read().decode("utf-8"))
                    paths = spec.get("paths", {})
                    has_validate = "/validate" in paths
                    has_certify = "/certify" in paths
                    if has_validate and has_certify:
                        return True, {
                            "status": "VALIDATED",
                            "title": spec.get("info", {}).get("title"),
                            "version": spec.get("info", {}).get("version"),
                            "endpoints": ["/validate", "/certify"]
                        }
                    return False, {"error": "Missing required paths /validate or /certify"}
                return False, {"error": f"HTTP {resp.status}"}
        except Exception as e:
            return False, {"error": str(e)}

    def validate_sarathi_contract(self, url: str) -> Tuple[bool, Dict[str, Any]]:
        """Validate Sarathi Execution Engine contract response."""
        try:
            req = urllib.request.Request(f"{url}/health", headers={"User-Agent": "Pravah-ContractValidator/2.0"})
            with urllib.request.urlopen(req, timeout=5, context=self.ctx) as resp:
                if resp.status == 200:
                    payload = json.loads(resp.read().decode("utf-8"))
                    is_valid = payload.get("status") == "healthy" and payload.get("bridge_active") is True
                    return is_valid, payload
                return False, {"error": f"HTTP {resp.status}"}
        except Exception as e:
            return False, {"error": str(e)}

    def validate_control_plane_contract(self, url: str) -> Tuple[bool, Dict[str, Any]]:
        """Validate Control Plane & Decision Brain health contract."""
        try:
            req = urllib.request.Request(f"{url}/health", headers={"User-Agent": "Pravah-ContractValidator/2.0"})
            with urllib.request.urlopen(req, timeout=5, context=self.ctx) as resp:
                if resp.status == 200:
                    payload = json.loads(resp.read().decode("utf-8"))
                    is_valid = payload.get("status") == "healthy"
                    return is_valid, payload
                return False, {"error": f"HTTP {resp.status}"}
        except Exception as e:
            return False, {"error": str(e)}

    def validate_observer_contract(self, url: str) -> Tuple[bool, Dict[str, Any]]:
        """Validate Observer health contract."""
        try:
            req = urllib.request.Request(f"{url}/health", headers={"User-Agent": "Pravah-ContractValidator/2.0"})
            with urllib.request.urlopen(req, timeout=5, context=self.ctx) as resp:
                if resp.status == 200:
                    payload = json.loads(resp.read().decode("utf-8"))
                    is_valid = payload.get("status") == "ok"
                    return is_valid, payload
                return False, {"error": f"HTTP {resp.status}"}
        except Exception as e:
            return False, {"error": str(e)}
