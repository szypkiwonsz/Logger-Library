import re
from datetime import datetime

from logger.log_entry import LogEntry


class LoggerSaver:
    """Class storing methods to save log into selected type of files."""

    def __init__(self, handlers):
        self.handlers = handlers
        self.log_level = 3

    def save_log_into_handlers(self, log_entry):
        """
        Saves log into all handlers.
        :param log_entry: <logger.log_entry.LogEntry> -> class representing log entry
        """
        for handler in self.handlers:
            handler.load_log_entry_data_into_file(log_entry)

    def info(self, message):
        """
        Saves info log into file.
        :param message: <str> -> log message to save
        """
        if self.log_level <= 2:
            log_entry = LogEntry(datetime.now(), 'INFO', message)
            self.save_log_into_handlers(log_entry)

    def warning(self, message):
        """
        Saves warning log into file.
        :param message: <str> -> log message to save
        """
        if self.log_level <= 3:
            log_entry = LogEntry(datetime.now(), 'WARNING', message)
            self.save_log_into_handlers(log_entry)

    def debug(self, message):
        """
        Saves debug log into file.
        :param message: <str> -> log message to save
        """
        if self.log_level <= 1:
            log_entry = LogEntry(datetime.now(), 'DEBUG', message)
            self.save_log_into_handlers(log_entry)

    def critical(self, message):
        """
        Saves critical log into file.
        :param message: <str> -> log message to save
        """
        if self.log_level <= 5:
            log_entry = LogEntry(datetime.now(), 'CRITICAL', message)
            self.save_log_into_handlers(log_entry)

    def error(self, message):
        """
        Saves error log into file.
        :param message: <str> -> log message to save
        """
        if self.log_level <= 4:
            log_entry = LogEntry(datetime.now(), 'ERROR', message)
            self.save_log_into_handlers(log_entry)

    def set_log_level(self, log_level):
        """
        Sets minimal log level to be saved into files.
        :param log_level: <str> -> selected log level
        """
        log_priority = {'DEBUG': 1, 'INFO': 2, 'WARNING': 3, 'ERROR': 4, 'CRITICAL': 5}
        self.log_level = log_priority[log_level]


class LoggerReader:
    """Class storing methods which are responsible for reading log entries from selected file."""

    def __init__(self, handler):
        self.handler = handler

    @staticmethod
    def filter_by_date(start_date, end_date, data):
        """
        Filters data by provided dates.
        :param start_date: <datetime> -> start date
        :param end_date: <datetime> -> end date
        :param data: <list> -> list of log entries
        :return: <list> -> list of filtered log entries
        """
        if start_date and end_date:
            return list(filter(lambda x: start_date < datetime.fromisoformat(x['date']) < end_date, data))
        elif start_date and not end_date:
            return list(filter(lambda x: start_date < datetime.fromisoformat(x['date']), data))
        else:
            return list(filter(lambda x: datetime.fromisoformat(x['date']) < end_date, data))

    def find_by_text(self, text, start_date=None, end_date=None):
        """
        Finds log entries with selected text.
        :param text: <str> -> text to find
        :param start_date: <datetime> -> start date
        :param end_date: <datetime> -> end date
        :return: <list> -> list of log entries with selected text
        """
        data = list(filter(lambda x: text in x['msg'], self.handler.get_data_from_file()))
        if start_date or end_date:  # if any datetime is given, filter according to that datetime
            data = self.filter_by_date(start_date, end_date, data)
        return data

    def find_by_regex(self, regex, start_date=None, end_date=None):
        """
        Finds log entries with selected regex.
        :param regex: <str> -> regex to find
        :param start_date: <datetime> -> start date
        :param end_date: <datetime> -> end date
        :return: <list> -> list of log entries with selected regex
        """
        data = list(filter(lambda x: re.search(regex, x['msg']), self.handler.get_data_from_file()))
        if start_date or end_date:  # if any datetime is given, filter according to that datetime
            data = self.filter_by_date(start_date, end_date, data)
        return data
