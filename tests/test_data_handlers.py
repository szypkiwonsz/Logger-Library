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
