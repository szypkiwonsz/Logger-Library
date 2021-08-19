from datetime import datetime

import pytest

from logger.data_handlers import JsonHandler, CSVHandler
from logger.log_entry import LogEntry
from logger.logger_handlers import LoggerReader


@pytest.fixture
def json_handler():
    temp_json_handler = JsonHandler('test_file.json')
    return temp_json_handler


@pytest.fixture
def log_entries_json_data():
    json_log_entries = '''[
        {
            "date": "2021-07-31 12:12:19",
            "level": "CRITICAL",
            "msg": "test_msg"
        }
    ]'''
    return json_log_entries


@pytest.fixture
def log_entry():
    temp_log_entry = LogEntry(datetime(2021, 1, 1), 'ERROR', 'test_message')
    return temp_log_entry


@pytest.fixture
def json_logger_reader(json_handler):
    temp_json_logger_reader = LoggerReader(json_handler)
    return temp_json_logger_reader


@pytest.fixture
def csv_handler():
    temp_csv_handler = CSVHandler('test_file.csv')
    return temp_csv_handler


@pytest.fixture
def log_entries_csv_data():
    csv_log_entries = '''date,level,msg
2021-01-01 00:00:00,ERROR,test_message'''
    return csv_log_entries
