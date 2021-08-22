from datetime import datetime
from unittest import mock

import pytest


@pytest.mark.logger_reader
class TestLoggerReader:

    def test_find_by_text_with_msg(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_msg = json_logger_reader.find_by_text('test_msg')
        assert data_with_msg == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_find_by_text_without_msg(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_without_msg = json_logger_reader.find_by_text('non_existing_msg')
        assert data_without_msg == []

    def test_find_by_text_with_s_date_true(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_s_date_true = json_logger_reader.find_by_text('test_msg', start_date=datetime(2020, 7, 31))
        assert data_with_s_date_true == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_find_by_text_with_s_date_false(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_s_date_false = json_logger_reader.find_by_text('test_msg', start_date=datetime(2022, 7, 31))
        assert data_with_s_date_false == []

    def test_find_by_text_with_e_date_true(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_e_date_true = json_logger_reader.find_by_text('test_msg', end_date=datetime(2022, 7, 31))
        assert data_with_e_date_true == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_find_by_text_with_e_date_false(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_e_date_false = json_logger_reader.find_by_text('test_msg', end_date=datetime(2020, 7, 31))
        assert data_with_e_date_false == []

    def test_find_by_text_with_s_date_and_e_date_true(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_s_date_and_e_date_true = json_logger_reader.find_by_text(
                'test_msg', start_date=datetime(2020, 7, 31), end_date=datetime(2022, 7, 31))
        assert data_with_s_date_and_e_date_true == [
            {"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_find_by_text_with_s_date_and_e_date_false(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_s_date_and_e_date_false = json_logger_reader.find_by_text(
                'test_msg', start_date=datetime(2022, 7, 31), end_date=datetime(2020, 7, 31))
        assert data_with_s_date_and_e_date_false == []
