import logging
import sys
from colorlog import ColoredFormatter

logging.addLevelName(logging.DEBUG, 'DEBG')
logging.addLevelName(logging.INFO, 'INFO')
logging.addLevelName(logging.WARNING, 'WARN')
logging.addLevelName(logging.ERROR, 'EROR')
logging.addLevelName(logging.CRITICAL, 'CRIT')

def _create_logger(name: str, level) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(ColoredFormatter(
        "%(log_color)s[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%m/%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG':    'white',
            'INFO':     'white,bold',
            'INFOV':    'white,bold',
            'WARNING':  'yellow',
            'ERROR':    'red,bold',
            'CRITICAL': 'red,bold',
        },
        secondary_log_colors={},
        style='%'
    ))
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

default_logger = _create_logger('pykis', logging.INFO)

class KisLoggable:
    logger: logging.Logger
    '''로거'''

    def _logger_ready(self, logger: logging.Logger):
        pass

    def _emit_logger(self, logger: logging.Logger | None = None):
        if logger:
            n = logger != getattr(self, 'logger', None)
            self.logger = logger
        else:
            self.logger = default_logger
            n = True

        for obj in self.__dict__.values():
            if isinstance(obj, KisLoggable):
                obj._emit_logger(self.logger)
        
        if n:
            self._logger_ready(logger)  # type: ignore
