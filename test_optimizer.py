"""Pytest suite for AI Optimizer MCP."""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai_optimizer_mcp.utils import safe_exec_code
from ai_optimizer_mcp.config import CANDIDATE_FILE

@pytest.fixture
def sample_code():
    return '''def f(x):
    return x * 2
'''

def test_safe_exec_code(sample_code):
    stdout, stderr = safe_exec_code(sample_code)
    assert "4,4" in stdout or "(4, 4)" in stdout  # Full pass

def test_sample_candidate():
    # Test initial candidate would fail
    with open(CANDIDATE_FILE, "w") as f:
        f.write('def f(x): return x + 1')
    stdout, _ = safe_exec_code(open(CANDIDATE_FILE).read())
    assert "0,4" in stdout  # Initial fails all

