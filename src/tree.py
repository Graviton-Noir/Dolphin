#!/usr/bin/env python

import numpy as np
import random
import copy
from asset_2 import Assett
from data_file_manager import DataFileManager
CORRELATION_THRESHOLD = 0.5


class Tree:

    def __init__(self):
        self.root = Node(None)

    def build(self, assets, n_assets):
        self.root.init_children(assets, n_assets)

    def __str__(self):
        return str(self.root)


class Node:

    def __init__(self, asset):
        self.asset = asset
        self.children = []

    def init_children(self, assets, depth):
        print('init_children - depth: {}'.format(depth))
        if depth > 0:
            for i in range(len(assets)):
                sub_assets, asset = self.get_sub_assets(assets, i)
                n = Node(asset)
                if n.init_children(sub_assets, depth - 1):
                    self.children.append(n)
            return len(self.children) > 0
        return True

    # return a sub assets without the current node (the order doesn't matter)
    # the children whose correlation is under the CORRELATION_THRESHOLD are ignored
    def get_sub_assets(self, assets, index):
        # we need to move the current asset to save memory: working in place
        current_asset = assets[index]
        assets[index] = assets[-1]

        # filter children (correlation must be more than CORRELATION_THRESHOLD)
        new_assets = []
        for a in assets[:-1]:
            # check correlation
            correlation = DataFileManager().get_correlation_dict()[str(current_asset.id)][str(a.id)]
            print("{}-{}: {}".format(current_asset.id, a.id, correlation))
            if correlation > CORRELATION_THRESHOLD:
                # add in list only if correlation > THRESHOLD
                new_assets.append(a)

        # set last and current assets in their initial places
        assets[-1] = assets[index]
        assets[index] = current_asset
        return new_assets, current_asset

    def __str__(self):
        # return '( asset: {}, weight: {}, children: [{}] )'.format(self.asset, self.weight,
        #                                                           self.nodes_to_str(self.children))
        if len(self.children) > 0:
            return '{{{} : [{}]}}'.format(self.asset, self.nodes_to_str(self.children))
        else:
            return '{{{}}}'.format(self.asset)

    @staticmethod
    def nodes_to_str(nodes):
        s = ''
        for n in nodes[:-1]:
            s += '{}, '.format(n)
        s += '{}'.format(nodes[-1])
        return s


if __name__ == '__main__':

    n_assets = 2
    assets = [Assett(16, 1.409424248688, 1.409424248688),
              Assett(31, 0.751849284981, 0.751849284981),
              Assett(61, 0.507142575734, 0.507142575734)]
              #Assett(67, 0.972497555641, 0.972497555641,
              #Assett(70, 1.07826992451, 1.07826992451),
              #Assett(109, 0.409811278998, 0.409811278998)]

    tree = Tree()
    tree.build(assets, n_assets)
    print(tree)

