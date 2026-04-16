"""Utility functions for code execution and memory."""
import json
import os
import subprocess
import logging
from typing import Dict, Any, Tuple
from pathlib import Path

from .config import CANDIDATE_FILE, MEMORY_FILE, TEST_TIMEOUT

logger = logging.getLogger(__name__)

def safe_exec_code(code_snippet: str, cwd: str = ".") -> Tuple[str, str]:
    """Safely execute code snippet via subprocess for testing."""
    temp_file = Path(TEMP_FILE)
    try:
        temp_file.write_text(code_snippet)
        cmd = [
            "python", "-c",
            f"from {TEMP_FILE.replace('.py', '')} import f; "
            f"from {TESTS_MODULE} import run_tests; print(run_tests(f))"
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT,
            cwd=cwd
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        logger.warning("Test timeout")
        return "", "Timeout"
    except Exception as e:
        logger.error(f"Exec error: {e}")
        return "", str(e)
    finally:
        if temp_file.exists():
            temp_file.unlink(missing_ok=True)

def load_memory() -> Dict[str, Any]:
    """Load optimization history from memory.json."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"iterations": [], "best_score": 0}

def save_memory(memory: Dict[str, Any]) -> None:
    """Save optimization history."""
    os.makedirs(os.path.dirname(MEMORY_FILE) if MEMORY_FILE else "", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

