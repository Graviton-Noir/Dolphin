#!/usr/bin/env python

from json import load

# Contains functions related to the data management (get data from file)


class DataFileManager:

    def __init__(self):
        self.correlation_dict_path = 'output_correlation_dict_2.json'
        self.file = open(self.correlation_dict_path, 'r')
        self.correlation_dict = None

    def get_correlation_dict(self):
        if self.correlation_dict is None:
            self.correlation_dict = load(self.file)
            self.file.close()
        return self.correlation_dict


if __name__ == '__main__':
    dfm = DataFileManager()
    d = dfm.get_correlation_dict()
    print(d)
