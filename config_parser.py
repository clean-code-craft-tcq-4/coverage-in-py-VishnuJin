from configparser import ConfigParser

class ConfigProvider:
    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser()
        self.config.read(self.filename)

    def get_categories(self):
        return tuple(self.config.keys())[1:]  # excluding default

    def get_value(self, field_name, field_type, category):
        try:
            value = self.config.get(category, field_name)
            return field_type(value)
        except Exception as e:
            raise ValueError(f"Error parsing the config..\n{e}")

