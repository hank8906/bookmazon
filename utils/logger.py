import logging

def setup_logger(level=logging.DEBUG):
    logger = logging.getLogger(__file__)
    logger.setLevel(level)

    # rm_file(log_file)
    fileHandler = logging.FileHandler("./log/app.log", mode='w')
    fileHandler.setLevel(level)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(level)

    # set formatter
    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # add
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    return logger
