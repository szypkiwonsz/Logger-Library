import pytest


@pytest.mark.log_entry
class TestLogEntry:

    def test_json_log_entry(self, log_entry):
        assert log_entry.json_log_entry() == {'date': '2021-01-01 00:00:00', 'level': 'ERROR', 'msg': 'test_message'}
