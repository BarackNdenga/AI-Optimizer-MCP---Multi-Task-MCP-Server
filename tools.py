"""MCP Tools for AI Optimizer."""
import logging
from typing import Dict, Any
from mcp.types import Tool, tool
from openai import OpenAI

from .config import OPENAI_API_KEY, OBJECTIVE, MODEL
from .utils import safe_exec_code, load_memory

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

@tool()
async def run_tests(code_snippet: str) -> str:
    """Run test suite on f(x) function. Provide the full candidate.py code (def f(x): ...)."""
    stdout, stderr = safe_exec_code(code_snippet)
    result = stdout or stderr or "Unknown error"
    logger.info(f"Tests run: {result}")
    return result

@tool()
async def generate_improvement(code: str, test_result: str) -> str:
    """Generate improved code from current code and test results."""
    memory = load_memory()
    
    prompt = f"""Objective: {OBJECTIVE}

Current code:
```{python}
{code}
```

Test result:
{test_result}

History (best score: {memory.get('best_score', 0)}):
{memory.get('iterations', [])[-3:]}

Improve the f(x) function to pass all tests and maximize score.
Return ONLY the complete Python code (def f(x): ...). No explanations."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        new_code = response.choices[0].message.content.strip()
        # Clean markdown
        if "```python" in new_code:
            new_code = new_code.split("```python")[-1].split("```")[0].strip()
        logger.info("Generated improvement")
        return new_code
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return code  # Fallback

@tool()
async def get_objective() -> str:
    """Get the optimization objective."""
    return OBJECTIVE

