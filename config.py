"""Configuration management for AI Optimizer MCP."""
import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required.")

OBJECTIVE = os.getenv("OBJECTIVE", "Create a function f(x) that doubles a number")
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))

MODEL = "gpt-4o-mini"
TEST_TIMEOUT = 5  # seconds

# Paths
CANDIDATE_FILE = "candidate.py"
MEMORY_FILE = "memory.json"
TEMP_FILE = "temp_candidate.py"

