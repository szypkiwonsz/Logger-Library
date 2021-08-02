from unittest import mock

import pytest


@pytest.mark.logger_reader
class TestLoggerReader:

    def test_find_by_text(self, log_entries_json_data, json_logger_reader):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data_with_msg = json_logger_reader.find_by_text('test_msg')
            data_without_msg = json_logger_reader.find_by_text('non_existing_msg')
        assert data_with_msg == [{"date": "2021-07-31 12:12:19", "level": "CRITICAL", "msg": "test_msg"}]
        assert data_without_msg == []
