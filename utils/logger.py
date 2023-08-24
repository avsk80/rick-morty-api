import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

class Logger:
    def __init__(self, log_file, maxBytes = 10*1024*1024, backup = 5, log_level=logging.INFO, console='ON', file='ON') -> None:
        self.log_file = log_file
        self.log_level = log_level
        self.maxBytes = maxBytes
        self.backup = backup
        self.console = console
        self.file = file
        self.create_log_path()
        self.logger = self.setup_logger()
        
    def create_log_path(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        Path(self.log_file).touch()
        
        
    def setup_logger(self):
        logger = logging.getLogger(name=__name__)
        logger.setLevel(level=self.log_level)
        
        formatter = logging.Formatter(
            fmt= "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        if self.console == 'ON':           
            logger = self.log2console(formatter, logger)
        if self.file == 'ON':
            logger = self.log2file(formatter, logger, self.log_file, self.maxBytes, self.backup)
        return logger
    
    
    def log2console(self, formatter, logger):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger
    
    def log2file(self, formatter, logger, log_file, maxBytes, backup):
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=maxBytes,
            backupCount=backup
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
    
    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def exception(self, msg):
        self.logger.exception(msg)

if __name__ == "__main__":
    # dir = os.path.join("D:\\", "MS", "projects", "utube", "Rick_Morty", "logs")
    # print(dir)
    # os.makedirs(name=dir, exist_ok=True)
    # os.makedirs(name="../logs2")
    # log_path = os.path.join(dir, "test.log")
    # Path(log_path).touch()
    dir = os.path.join("D:\\", "MS", "projects", "utube", "Rick_Morty", "config", "config.ini")
    print(os.path.exists(dir))
    print(dir)
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(dir)
    log_path = config.get("Logs", "log_file_path")
    
    logger = Logger(log_file=log_path)
    logger.info("Testing logger!!!")
    try:
        a = 1/0
    except Exception as e:
        logger.exception(e)