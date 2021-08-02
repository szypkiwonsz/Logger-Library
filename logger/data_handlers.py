import json


class Handler:
    """A class with a constructor for handler classes."""

    def __init__(self, file_name):
        self.file_name = file_name


class JsonHandler(Handler):
    """Inheriting class storing methods to handle json files."""

    def get_data_from_file(self):
        """
        Gets data from json file.
        :return: <list> -> list of json log entries
        """
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def load_data_into_file(self, data):
        """
        Loads data into json file.
        :param data: <list> -> data to load
        """
        with open(self.file_name, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    def load_log_entry_data_into_file(self, log_entry):
        """
        Loads log entry into json file.
        :param log_entry: <logger.log_entry.LogEntry> -> class representing log entry
        """
        data_to_save = log_entry.json_log_entry()
        data_from_file = self.get_data_from_file()
        data_from_file.append(data_to_save)
        self.load_data_into_file(data_from_file)
