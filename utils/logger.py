import logging
import os

def setup_logger(level=logging.DEBUG):
    logger = logging.getLogger(__file__)
    logger.setLevel(level)

    # 取得專案根目錄的絕對路徑
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(project_root, "log/app.log")

    # 檢查文件是否存在，如果不存在則創建一個新的文件
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w'):
            pass

    # 使用 FileHandler 的 delay 參數，延遲文件的創建
    fileHandler = logging.FileHandler(log_file_path, mode='a', delay=True)
    fileHandler.setLevel(level)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(level)

    # 設置格式化器
    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 添加處理器
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger
