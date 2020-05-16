from logging import Filter
from orb.middleware.default import DefaultHandler


class GUIDLogger(Filter):
    def filter(self, record):
        """
        Determines that the specified record is to be logged.
        From the docs:
                Is the specified record to be logged? Returns 0 for no, nonzero for
                yes. If deemed appropriate, the record may be modified in-place.
        :param record: Log record
        :return: True
        """
        record.request_id = DefaultHandler.get_request_id()
        return True
