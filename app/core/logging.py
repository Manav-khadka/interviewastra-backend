from loguru import logger
import sys

# Configure logger
logger.remove()  # Remove default handler
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")
logger.add("logs/app.log", rotation="10 MB", retention="1 week", level="INFO")

# Export logger
__all__ = ["logger"]