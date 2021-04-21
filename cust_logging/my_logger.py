import logging


class MyLog:
    logging.basicConfig(level=logging.INFO, filename='bank_main.log', filemode='a',
                        format='%(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # Log Levels: Info, Warning, Error, Critical, Debug, etc...
    # Handlers are used to better manage where a logger will log to.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(console_handler)

    @staticmethod
    def info_log(message=None):
        if message is not None:
            MyLog.logger.info(message)
        else:
            MyLog.logger.info("We went to the next step in the program")

    @staticmethod
    def warning_log(message=None):
        if message is not None:
            MyLog.logger.warning(message)
        else:
            MyLog.logger.info("Warning! Must have valid values!")

    @staticmethod
    def error_log(message=None):
        if message is not None:
            MyLog.logger.error(message)
        else:
            MyLog.logger.info("Warning! An error has occurred!")


def _test():
    MyLog().info_log("The test log was successful!")


if __name__ == '__main__':
    _test()
