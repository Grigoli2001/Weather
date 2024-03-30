import logging
import sys
# TODO: Make it a function that takes level as an argument
logger = logging.getLogger()

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')

# stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [file_handler]

logger.setLevel(logging.INFO)