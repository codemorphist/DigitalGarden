import logging
import sys


logging.basicConfig(
    level=logging.DEBUG,
    filename="digital_garden.log",
    format='[%(asctime)s] <%(levelname)-8s> %(filename)s:'
            '%(lineno)d (%(name)s) : %(message)s',
    encoding="utf-8",
    filemode="a"
)

logger = logging.getLogger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


from root import RootWindow


if __name__ == "__main__":
    logger.info("Starting window...")
    app = RootWindow()
    app.mainloop()
    logger.info("Window closed!")
    
