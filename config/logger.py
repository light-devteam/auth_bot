import logging

from config.settings import settings


class LoggerFilter(logging.Filter):
    COLOR = {
        'DEBUG': 'GREEN',
        'INFO': 'GREEN',
        'WARNING': 'YELLOW',
        'ERROR': 'RED',
        'CRITICAL': 'RED',
    }

    def filter(self, record):
        record.color = LoggerFilter.COLOR[record.levelname]
        return True


class Logger:
    _LOG_FORMAT = '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

    def __init__(self, name: str) -> logging.Logger:
        log_level = self.__get_logger_level(logging.INFO)
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(log_level)
        self.__logger.addFilter(LoggerFilter())
        self.__logger.addHandler(self.file_handler)
        self.__logger.addHandler(self.stream_handler)

    @property
    def file_handler(self) -> logging.FileHandler:
        log_level = self.__get_logger_level(logging.WARNING)
        file_handler = logging.FileHandler(settings.LOGS_FILE)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(self._LOG_FORMAT))
        return file_handler

    @property
    def stream_handler(self) -> logging.StreamHandler:
        log_level = self.__get_logger_level(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(logging.Formatter(self._LOG_FORMAT))
        return stream_handler

    def __get_logger_level(self, default_level: int) -> int:
        if settings.DEV_MODE:
            return logging.DEBUG
        return default_level

    @property
    def logger(self) -> logging.Logger:
        return self.__logger


logger = Logger(__name__).logger
