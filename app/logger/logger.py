import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

#later we can use it .
'''
from app.logger import logger

logger.info("User registered")
logger.error("Login failed")

'''