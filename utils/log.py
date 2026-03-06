import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.getLogger("telethon").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)
