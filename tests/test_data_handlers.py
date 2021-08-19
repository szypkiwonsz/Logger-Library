import json
from unittest import mock

import pytest


@pytest.mark.json_handler
class TestJsonHandler:

    def test_get_data_from_file(self, json_handler, log_entries_json_data):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            data = json_handler.get_data_from_file()
        assert data == json.loads(log_entries_json_data)

    def test_load_data_into_file(self, json_handler, log_entries_json_data):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_json_data), create=True):
            json_handler.load_data_into_file(log_entries_json_data)
            data = json_handler.get_data_from_file()
        assert data == json.loads(log_entries_json_data)

    def test_load_log_entry_data_into_file(self, json_handler, log_entry):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps([log_entry.json_log_entry()])),
                        create=True):
            json_handler.load_log_entry_data_into_file(log_entry)
            data = json_handler.get_data_from_file()
        assert data == [log_entry.json_log_entry()]


@pytest.mark.csv_handler
class TestCSVHandler:

    def test_get_data_from_file(self, csv_handler, log_entries_csv_data):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_csv_data), create=True):
            data = csv_handler.get_data_from_file()
        assert data == [{'date': '2021-01-01 00:00:00', 'level': 'ERROR', 'msg': 'test_message'}]

    def test_load_data_into_file(self, csv_handler, log_entries_csv_data, log_entry):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_csv_data), create=True):
            csv_handler.load_data_into_file(log_entry.json_log_entry())
            data = csv_handler.get_data_from_file()
        assert data == [{'date': '2021-01-01 00:00:00', 'level': 'ERROR', 'msg': 'test_message'}]

    def test_load_log_entry_data_into_file(self, csv_handler, log_entry, log_entries_csv_data):
        with mock.patch("builtins.open", mock.mock_open(read_data=log_entries_csv_data),
                        create=True):
            csv_handler.load_log_entry_data_into_file(log_entry)
            data = csv_handler.get_data_from_file()
        assert data == [log_entry.json_log_entry()]
