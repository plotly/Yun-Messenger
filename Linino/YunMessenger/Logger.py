import logging
import logging.handlers

class Logger:
    file_name = '/root/YunMessenger.log'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=524288, backupCount=0)

    formatter = logging.Formatter()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", '%Y-%m-%d %H:%M:%S')

    handler.setFormatter(formatter)

    logger.addHandler(handler)