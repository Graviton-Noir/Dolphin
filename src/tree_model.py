#!/usr/bin/env python

from portfolio import PortfolioItem, Portfolio
from client import Client
from tree import Tree, Node
from json import dumps
from data_manager import DataManager

MAX_MONEY = 10000000
SAVE_PORTFOLIOS = True  # If true, the results will be saved in file
GENERATE_CORRELATION_DICT = False

# model where the assets with best sharpes are selected
# a tree is built
# the weights are according sharpes
class TreeModel:

    def __init__(self):
        self.client = Client()
        self.combinations = []
        self.n_assets = n_assets
        self.best_assets = []
        self.best_sharpe = 0
        self.correlation_dict = {}
        self.output_file = open('../out/trees/1', 'w')
        self.correlation_dict_infile = '../assets/correlation_dict.json'

    # get sorted assets (sharpe) and remove those with sharpe <= 0
    @staticmethod
    def select_assets(assets):
        # Sort assets (reverse)
        return sorted(assets, key=lambda a: a.sharpe, reverse=True)[:25]

    # Set correlation dictionary, from file or compute
    #   regenerate_corr_dict: Set True if you want to generate correlation dictionary and write in file
    def set_correlation_dict(self, regenerate_corr_dict):
        asset_ids = [a.id for a in assets]
        # compute correlation dictionary
        if regenerate_corr_dict:
            correlation_dict_file = open(self.correlation_dict_infile, 'w')
            self.correlation_dict = self.client.get_correlation_dict(asset_ids)
            correlation_dict_file.write(dumps(self.correlation_dict))
            correlation_dict_file.close()
        else:  # get correlation dictionary from file
            dm = DataManager()
            self.correlation_dict = dm.get_correlation_dict()

    # Evaluate assets and get best portfolio
    def generate_portfolio(self, assets):

        # Build portfolio from ids directly if length = 20
        if len(assets) == 20:
            portfolio = Portfolio(MAX_MONEY)
            portfolio.build(assets)
            portfolio_sharpe = portfolio.submit()
            if SAVE_PORTFOLIOS:
                self.output_file.write('{{ "sharpe": {}, "portfolio": {} }}'.format(portfolio_sharpe, str(portfolio)))
            print('{{ "sharpe": {}, "portfolio": {} }}'.format(portfolio_sharpe, str(portfolio)))
        # Build tree and evaluate it at the same time
        elif len(assets) > 20:
            tree = Tree()
            tree.build(assets, n_assets)

    # Run algorithm to get the best portfolio.
    def run(self, assets):
        # select assets with sharpe > 0
        assets = self.select_assets(assets)

        # Set correlation dictionary
        self.set_correlation_dict(GENERATE_CORRELATION_DICT)
        self.generate_portfolio(assets)


if __name__ == '__main__':
    n_assets = 20
    max_money = 10000000
    c = Client()
    assets, assets_dict = c.fill_all_assets_split()
    model = TreeModel()
    model.run(assets)
    model.output_file.close()
