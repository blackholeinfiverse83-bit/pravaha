"""
PRAVAH Automated Metadata Extraction Engine
Phase 2: Advanced Integration & Security Hardening
Assignee: Chandragupta Maurya
"""

import hashlib
import json
import os
import time
from typing import Dict, Any, Optional


class MetadataExtractor:
    """Extracts deterministic metadata, cryptographic hashes, and schema validation."""
    
    @staticmethod
    def calculate_sha256(content: bytes) -> str:
        """Calculate deterministic sha256 checksum."""
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def extract_file_metadata(file_path: str) -> Dict[str, Any]:
        """Extract multi-format metadata from file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = os.stat(file_path)
        with open(file_path, "rb") as f:
            content = f.read()
            
        sha256_hash = hashlib.sha256(content).hexdigest()
        ext = os.path.splitext(file_path)[1].lower()
        
        format_type = "unknown"
        if ext in [".json"]:
            format_type = "application/json"
        elif ext in [".md", ".txt"]:
            format_type = "text/markdown"
        elif ext in [".py"]:
            format_type = "text/x-python"
        elif ext in [".log"]:
            format_type = "text/plain"

        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": stat.st_size,
            "mime_type": format_type,
            "sha256": sha256_hash,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(stat.st_ctime)),
            "modified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(stat.st_mtime))
        }

    @staticmethod
    def extract_payload_metadata(payload: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        """Extract deterministic metadata for JSON payload."""
        serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
        payload_hash = hashlib.sha256(serialized).hexdigest()
        
        return {
            "trace_id": trace_id,
            "field_count": len(payload.keys()),
            "keys": list(payload.keys()),
            "payload_sha256": payload_hash,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    @staticmethod
    def validate_schema(data: Dict[str, Any], required_keys: list) -> Tuple[bool, list]:
        """Validate presence of required schema keys."""
        missing = [key for key in required_keys if key not in data]
        if missing:
            return False, missing
        return True, []
