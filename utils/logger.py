# Import modules
import logging
import platform
import getpass
from datetime import datetime

# Define log file name (creates in the same directory as the script)
LOG_FILE = "it_support_toolkit.log"


logger = logging.getLogger("toolkit_logs") # Creates a logger instance
logger.setLevel(logging.INFO) # Sets the minimum level of messages to log


# Create a file handler
handler = logging.FileHandler(LOG_FILE)


    