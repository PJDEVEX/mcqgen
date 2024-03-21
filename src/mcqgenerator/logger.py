import logging
import os
from datetime import datetime

# Custom logger
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# loging path
log_path = os.path.join(os.getcwd(),"logs")

# create logs directory if not exists
os.makedirs(log_path, exist_ok=True)

# create dot log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# logging configuration
logging.basicConfig(level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)