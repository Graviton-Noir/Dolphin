#!/usr/bin/env python

from client import Client
from asset_2 import Assett
import random
from portfolio import PortfolioItem, Portfolio
from evaluate import check_portfolio
from client import Client
from tree import Tree, Node
from util import list_to_str
from copy import deepcopy
from json import dumps
from data_file_manager import DataFileManager

CORRELATION_THRESHOLD = 0.9
MAX_MONEY = 10000000

# model where the assets with best sharpes are selected
# the weights are according sharpes
class IntermediateModel:

    def __init__(self):
        self.client = Client()
        self.combinaisons = []
        self.n_assets = n_assets
        self.best_assets = []
        self.best_sharpe = 0
        self.correlation_dict = {}
        self.file = open('output_portfolio', 'w')

    # get sorted assets (sharpe) and remove those with sharpe <= 0
    @staticmethod
    def select_assets(assets):
        print('select_assets: length before: {}'.format(len(assets)))
        # remove assets with negative sharpes
        assets = (a for a in assets if a.sharpe > 0)
        # Sort assets (reverse)
        return sorted(assets, key=lambda a: a.sharpe, reverse=True)

    # evaluate assets combinaison (when reaching a leaf) and write result in file.
    def evaluate_combinaison(self, assets_combinaison, ids_combinaison):
        print('evaluate_combinaison')
        # Generate portfolio from given assets_combinaison
        portfolio = self.generate_portfolio(assets_combinaison)
        #self.client.put_portfolio_from_assets(str(portfolio))
        sharpe = self.client.get_portfolio_sharpe()
        if sharpe > self.best_sharpe:
            self.best_sharpe = sharpe
            self.best_assets = assets
        s = '{{"combinaison": {}, "ids": {}, "sharpe": {}}}'.format(list_to_str(assets_combinaison),
                                                                    ids_combinaison, sharpe)
        print(s)
        self.file.write(s)

    @staticmethod
    def is_in_list(int_list, int_list_list):
        for l in int_list_list:
            if int_list != l:
                return False
        return True

    # Evaluate node
    #   If it's leaf, evaluate combinaison
    #   If not:
    #       If the correlation between current node and child is more than CORRELATION_THRESHOLD, evaluate node.
    #       If not, cut the branch
    def evaluate_node(self, node, combinaison):

        # Leaf
        if len(node.children) == 0:
            ids_combinaison = sorted(combinaison, key=lambda a: a.id)
            if self.is_in_list(ids_combinaison, self.combinaisons):
                # evaluate combinaison
                self.evaluate_combinaison(combinaison, ids_combinaison)
                # add in combinaisons list after evaluation
                self.combinaisons.append(ids_combinaison)

        for n in node.children:
            if self.correlation_dict.get(node.asset.id) is not None:
                if self.correlation_dict[node.asset.id].get(str(n.asset.id)) is not None:
                    if self.correlation_dict[node.asset.id][str(n.asset.id)] > CORRELATION_THRESHOLD:
                        # Add asset in combinaison (to be used in child nodes until reaching leaf)
                        cpy = deepcopy(combinaison)
                        cpy.append(n.asset)
                        self.evaluate_node(n, cpy)
                    else:
                        print('Node with correlation <= THRESHOLD found: {}-{}'.format(node.asset.id, n.asset.id))

    # Evaluate tree
    def evaluate_tree(self, tree):
        print('evaluate_tree')
        # Call evaluation on every root children
        for node in tree.root.children:
            # Add asset in combinaison (to be used in child nodes until reaching leaf)
            self.evaluate_node(node, [node.asset])

    # Generate portfolio (quantities) for a given assets combinaison
    def generate_portfolio(self, assets_combinaison):
        print('generate_portfolio')
        portfolio = Portfolio()
        for a in assets_combinaison:
            quantity = 1  # TODO
            portfolio.items.append(PortfolioItem(a, quantity))
        return portfolio

    # Run algorithm to get the best portfolio.
    def run(self, assets, n_assets):
        # Set True if you want to regenerate corr dict.
        regenerate_corr_dict = False

        print('run')
        # select assets with sharpe > 0
        assets = self.select_assets(assets)

        asset_ids = [a.id for a in assets]
        # compute correlation dictionary
        print('[START] correlation_dict')
        if regenerate_corr_dict:
            correlation_dict_file = open('output_correlation_dict.json', 'w')
            self.correlation_dict = self.client.get_correlation_dict(asset_ids)
            correlation_dict_file.write(dumps(self.correlation_dict))
            correlation_dict_file.close()
        else:  # get correlation dictionary from file
            dfm = DataFileManager()
            self.correlation_dict = dfm.get_correlation_dict()
        print('[END] correlation_dict')

        # browse list of combinaisons and build tree with assets whose correlation ratio > THRESHOLD
        for a in assets:
            print(a.id)
            ast_ids = []
            correlations = self.correlation_dict[a.id]
            # browse correlations for this asset and append k whose v > THRESHOLD
            for k, v in correlations.iteritems():
                if v > CORRELATION_THRESHOLD:
                    ast_ids.append(k)

            # Build portfolio from ids directly if length = 20
            if len(ast_ids) == 20:
                portfolio = Portfolio(MAX_MONEY)
                portfolio.build_from_asset_ids(assets, ast_ids)
                portfolio_sharpe = self.submit_portfolio(portfolio)
                self.file.write('{}\n{}'.format(portfolio, portfolio_sharpe))
                print('{}\n{}'.format(portfolio_sharpe, portfolio))


                # get correlation dictionary
        # correlation_dict = self.client.get_correlation_dict()
        # build tree
        # evaluation
            # Cut if:
                # composition with sharpe > 0 only
                # composition with correlation == 1

    # Submit portfolio : PUT the given portfolio on the server and return information about it (sharpe)
    def submit_portfolio(self, portfolio):
        self.client.put_portfolio_from_assets(str(portfolio))
        return self.client.get_portfolio_sharpe()


if __name__ == '__main__':
    n_assets = 20
    max_money = 10000000
    c = Client()
    print('fill_all_assets')
    assets = c.fill_all_assets()
    #assets = [Assett(16, 1.409424248688, 1.409424248688),
    #          Assett(31, 0.751849284981, 0.751849284981),
    #          Assett(61, -0.507142575734, 0.507142575734),
    #          Assett(70, -1.07826992451, 1.07826992451),
    #          Assett(109, 0.092134124, 0.0002134124)]
    print('intermediateModel')
    model = IntermediateModel()
    model.run(assets, n_assets)
    model.file.close()
