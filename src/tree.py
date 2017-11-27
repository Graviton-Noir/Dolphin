#!/usr/bin/env python

import copy
from data_manager import DataManager
from evaluation import Evaluation

CORRELATION_THRESHOLD = 0.5
MAX_MONEY = 10000000
EVALUATE_QUANTITIES_FROM_SHARPE = False
dm = DataManager()
evaluation = Evaluation()


class Tree:

    def __init__(self):
        self.root = Node(None)
        self.assets_dict = []

    def build(self, assets, n_assets):
        self.root.init_children(assets, n_assets, [])

    def __str__(self):
        return str(self.root)


class Node:

    def __init__(self, asset):
        self.asset = asset
        self.children = []

    def init_children(self, assets, depth, ids_combination):
        print('init_children - depth: {}'.format(depth))
        if depth > 0:
            for i in range(len(assets)):
                sub_assets, asset = self.get_sub_assets(assets, i)
                n = Node(asset)
                n_ids_combination = copy.copy(ids_combination)
                n_ids_combination.append(n.asset.id)  # add node n in combination
                if n.init_children(sub_assets, depth - 1, n_ids_combination):
                    self.children.append(n)
            return len(self.children) > 0
        elif EVALUATE_QUANTITIES_FROM_SHARPE:  # Leaf : Evaluation
            evaluation.evaluate_with_sharpe_quantities(ids_combination)
        else:
            evaluation.evaluate(ids_combination)
        return True

    # return a sub assets without the current node (the order doesn't matter)
    # the children whose correlation is under the CORRELATION_THRESHOLD are ignored
    def get_sub_assets(self, assets, index):
        # we_ need to move the current asset to save memory: working in place
        current_asset = assets[index]
        assets[index] = assets[-1]

        # filter children (correlation must be more than CORRELATION_THRESHOLD)
        new_assets = []
        for a in assets[:-1]:
            # check correlation
            # TODO: TEST if DataFileManager().get_correlation_dict()[str(current_asset.id)][str(a.id)] > CORRELATION_THRESHOLD:
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
