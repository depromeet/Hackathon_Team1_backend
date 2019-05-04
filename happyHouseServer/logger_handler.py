import logging


class LoggerHandler():
    server_logger = logging.getLogger('logging_example')
    server_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    server_logger.addHandler(stream_hander)

    server_logger.info("server start!!!")
