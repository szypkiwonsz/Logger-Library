from datetime import datetime
from unittest import mock

import pytest


@pytest.mark.logger_reader
class TestLoggerReader:

    def test_filter_by_date_s_date_and_e_date_true(self, list_of_log_entries, json_logger_reader):
        start_date = datetime(2021, 7, 31)
        end_date = datetime(2021, 8, 31)
        assert json_logger_reader.filter_by_date(start_date, end_date, list_of_log_entries) == list_of_log_entries

    def test_filter_by_date_s_date_and_e_date_false(self, list_of_log_entries, json_logger_reader):
        start_date = datetime(2021, 7, 31)
        end_date = datetime(2021, 7, 31)
        assert json_logger_reader.filter_by_date(start_date, end_date, list_of_log_entries) == []

    def test_filter_by_date_s_date_false(self, list_of_log_entries, json_logger_reader):
        start_date = datetime(2021, 8, 31)
        assert json_logger_reader.filter_by_date(start_date, None, list_of_log_entries) == []

    def test_filter_by_date_s_date_true(self, list_of_log_entries, json_logger_reader):
        start_date = datetime(2021, 7, 31)
        assert json_logger_reader.filter_by_date(start_date, None, list_of_log_entries) == list_of_log_entries

    def test_filter_by_date_e_date_false(self, list_of_log_entries, json_logger_reader):
        end_date = datetime(2021, 7, 31)
        assert json_logger_reader.filter_by_date(None, end_date, list_of_log_entries) == []

    def test_filter_by_date_e_date_true(self, list_of_log_entries, json_logger_reader):
        end_date = datetime(2021, 8, 31)
        assert json_logger_reader.filter_by_date(None, end_date, list_of_log_entries) == list_of_log_entries

    def test_filter_by_date_e_date_before_s_date(self, list_of_log_entries, json_logger_reader):
        start_date = datetime(2021, 7, 31)
        end_date = datetime(2021, 6, 30)
        with pytest.raises(ValueError):
            json_logger_reader.filter_by_date(start_date, end_date, list_of_log_entries)

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
            with pytest.raises(ValueError):
                json_logger_reader.find_by_text(
                    'test_msg', start_date=datetime(2022, 7, 31), end_date=datetime(2020, 7, 31))

    def test_find_by_regex_without_date(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            regex_data = json_logger_reader.find_by_regex('[a-g]')
        assert regex_data == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_find_by_regex_with_s_date(self, log_entries_json_data, json_logger_reader):
        start_date = datetime(2021, 7, 31)
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            regex_data = json_logger_reader.find_by_regex('[a-g]', start_date)
        assert regex_data == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_find_by_regex_with_e_date(self, log_entries_json_data, json_logger_reader):
        end_date = datetime(2021, 8, 31)
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            regex_data = json_logger_reader.find_by_regex('[a-g]', None, end_date)
        assert regex_data == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_find_by_regex_with_s_date_and_e_date(self, log_entries_json_data, json_logger_reader):
        start_date = datetime(2021, 7, 31)
        end_date = datetime(2021, 8, 31)
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            regex_data = json_logger_reader.find_by_regex('[a-g]', start_date, end_date)
        assert regex_data == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_validate_dates(self, json_logger_reader):
        with pytest.raises(ValueError):
            json_logger_reader.validate_dates(datetime(2021, 7, 31), datetime(2021, 6, 31))

    def test_group_by_month_without_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_month()
        assert grouped_data == [{"date": "2021-07-30 12:12:19", "level": "ERROR", "msg": "test_msg"},
                                {"date": "2021-06-30 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]

    def test_group_by_month_with_s_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_month(datetime(2021, 7, 31))
        assert grouped_data == []

    def test_group_by_month_with_e_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_month(None, datetime(2021, 6, 30))
        assert grouped_data == []

    def test_group_by_month_with_s_date_and_e_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_month(datetime(2021, 6, 25), datetime(2021, 6, 30))
        assert grouped_data == []

    def test_group_by_level_without_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_level()
        assert grouped_data == [{"date": "2021-06-30 12:12:19", "level": "CRITICAL", "msg": "test_msg"},
                                {"date": "2021-07-30 12:12:19", "level": "ERROR", "msg": "test_msg"}]

    def test_group_by_level_with_s_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_level(datetime(2021, 7, 31))
        assert grouped_data == []

    def test_group_by_level_with_e_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_level(None, datetime(2021, 6, 30))
        assert grouped_data == []

    def test_group_by_level_with_s_date_and_e_date(self, json_logger_reader, log_entries_json_data_to_group):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data_to_group), create=True):
            grouped_data = json_logger_reader.group_by_level(datetime(2021, 6, 25), datetime(2021, 6, 30))
        assert grouped_data == []
