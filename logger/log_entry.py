class LogEntry:
    """Class representing log entry."""

    def __init__(self, date, level, msg):
        self.date = date
        self.level = level
        self.msg = msg

    def json_log_entry(self):
        """
        Returns log entry in json format.
        :return: <dict> -> log entry in json format
        """
        return {'date': self.date.strftime("%Y-%m-%d %H:%M:%S"), 'level': self.level, 'msg': self.msg}
