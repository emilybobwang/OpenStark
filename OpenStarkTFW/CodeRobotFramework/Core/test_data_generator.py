# coding=utf8
import json


class TestDataGenerator(object):
    def load_test_data(self, json_string, replace=None):
        json_string = json.loads(json_string)
        for key in replace:
            if key in json_string.keys():
                json_string[key] = replace[key]
        return json_string
