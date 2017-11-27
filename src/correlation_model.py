#!/usr/bin/env python

from portfolio import PortfolioItem, Portfolio
from client import Client
from json import dumps
from data_manager import DataManager

CORRELATION_THRESHOLD_MIN = -0.2
CORRELATION_THRESHOLD_MAX = 0.2
MAX_MONEY = 10000000
SAVE_PORTFOLIOS = False  # If true, the results will be saved in file
GENERATE_CORRELATION_DICT = True


# model based on correlation between assets
# we aim to find an uncorrelated assets portfolio
# the weights are according sharpes
class CorrelationModel:

    def __init__(self):
        self.client = Client()
        self.combinations = []
        self.n_assets = n_assets
        self.best_assets = []
        self.best_sharpe = 0
        self.correlation_dict = {}
        self.file = open('../out/correlations/1', 'w')
        self.correlation_dict_filepath = '../assets/output_correlation_dict.json'

    # get sorted assets (sharpe) and remove those with sharpe <= 0
    @staticmethod
    def select_assets(assets):
        # remove assets with negative sharpes
        assets = (a for a in assets if a.sharpe > 0)
        # Sort assets (reverse)
        return sorted(assets, key=lambda a: a.sharpe, reverse=True)

    # Set correlation dictionary, from file or compute
    #   regenerate_corr_dict: Set True if you want to generate correlation dictionary and write in file
    def set_correlation_dict(self, regenerate_corr_dict):
        asset_ids = [a.id for a in assets]
        # compute correlation dictionary
        if regenerate_corr_dict:
            correlation_dict_file = open(self.correlation_dict_filepath, 'w')
            self.correlation_dict = self.client.get_correlation_dict(asset_ids)
            correlation_dict_file.write(dumps(self.correlation_dict))
            correlation_dict_file.close()
        else:  # get correlation dictionary from file
            dm = DataManager()
            self.correlation_dict = dm.get_correlation_dict()

    # Evaluate assets and get best portfolio, taking into account correlation
    def generate_portfolio(self, assets):
        # browse list of combinations and build tree with assets whose correlation ratio < THRESHOLD
        for a in assets:
            print(a.id)
            ast_ids = []
            correlations = self.correlation_dict[a.id]

            # browse correlations for this asset and append k whose MIN < v < MAX thresholds.
            # we aim to get un-correlated assets
            for k, v in correlations.iteritems():
                if CORRELATION_THRESHOLD_MIN < v < CORRELATION_THRESHOLD_MAX:
                    ast_ids.append(k)

            # Compute mean value of correlation between chosen assets
            sum_correlations = 0
            for id1 in ast_ids:
                for id2 in ast_ids:
                    if id1 != id2:
                        sum_correlations += self.correlation_dict[id1][id2]
            mean_correlation = sum_correlations / (len(ast_ids) ^ 2) - len(ast_ids)
            # if not uncorrelated, break
            if CORRELATION_THRESHOLD_MIN < mean_correlation < CORRELATION_THRESHOLD_MAX:
                break

            # Build portfolio from ids directly if length = 20
            if len(ast_ids) == 20:
                portfolio = Portfolio(MAX_MONEY)
                portfolio.build_from_asset_ids(assets, ast_ids)
                portfolio_sharpe = portfolio.submit()
                if SAVE_PORTFOLIOS:
                    self.file.write('{}\n{}'.format(portfolio, portfolio_sharpe))
            # Get 20 assets with best sharpes
            elif len(ast_ids) > 20:
                assets_from_ids = sorted(self.ids_to_assets_array(assets_dict, ast_ids),
                                         key=lambda a: a.sharpe,
                                         reverse=True)
                portfolio = Portfolio(MAX_MONEY)
                portfolio.build(assets_from_ids[:n_assets])
                portfolio_sharpe = portfolio.submit()
                if SAVE_PORTFOLIOS:
                    self.file.write('{} {}\n'.format(portfolio_sharpe, portfolio))

    # Run algorithm to get the best portfolio.
    def run(self, assets):
        # select assets with sharpe > 0
        assets = self.select_assets(assets)
        # Set correlation dictionary
        self.set_correlation_dict(GENERATE_CORRELATION_DICT)
        self.generate_portfolio(assets)

    # Get assets array from ids array
    def ids_to_assets_array(self, assets_dict, assets_ids):
        assets_from_ids = []
        # build assets array from ids
        for id in assets_ids:
            assets_from_ids.append(assets_dict[id])
        return assets_from_ids


if __name__ == '__main__':
    n_assets = 20
    max_money = 10000000
    c = Client()
    assets, assets_dict = c.fill_all_assets_split()
    model = CorrelationModel()
    model.run(assets)
    model.file.close()
