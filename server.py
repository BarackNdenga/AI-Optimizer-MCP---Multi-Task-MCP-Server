"""Main MCP Server for AI Optimizer."""
import asyncio
import logging
from mcp.server.stdio import stdio_server
from .tools import run_tests, generate_improvement, get_objective

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main() -> None:
    """Run the MCP stdio server."""
    tools = [run_tests, generate_improvement, get_objective]
    logger.info("Starting AI Optimizer MCP Server v0.1.0")
    
    async with stdio_server(tools=tools) as server:
        await server.run()

if __name__ == "__main__":
    asyncio.run(main())

