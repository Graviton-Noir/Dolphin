#!/usr/bin/env python

from json import load
from client import Client

# Contains functions related to the data management

class DataManager:
    class __Singleton:
        def __init__(self):
            self.correlation_dict_path = 'output_correlation_dict_4.json'
            self.file = open(self.correlation_dict_path, 'r')
            self.correlation_dict = None
            self.client = Client()
            self.assets = None
            self.assets_dict = None

    instance = None

    def __init__(self):
        if not DataManager.instance:
            DataManager.instance = DataManager.__Singleton()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_correlation_dict(self):
        if self.instance.correlation_dict is None:
            self.instance.correlation_dict = load(self.file)
            self.file.close()
        return self.correlation_dict

    def get_assets_dict(self):
        if self.instance.assets_dict is None:
            self.instance.assets, self.instance.assets_dict = self.client.fill_all_assets_split()
        return self.instance.assets_dict

    def get_assets(self):
        if self.instance.assets is None:
            self.instance.assets, self.instance.assets_dict = self.client.fill_all_assets_split()
        return self.instance.assets

if __name__ == '__main__':
    dfm = DataManager()
    d = dfm.get_correlation_dict()
    print(d)
