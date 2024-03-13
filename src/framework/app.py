import structlog

class App:
    def __init__(self):
        self._logger: structlog.stdlib.BoundLogger  = structlog.get_logger()

    def Logger(self):
        return self._logger