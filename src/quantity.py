# coding: utf-8
#
#   Quantity
#
#
#   Compute the quantity for every asset in a portfolio 
#

def compute_quantity_by_return(asset):
       
    # Let's set a quantity to get 500k€, which is 1/20 of 10M€
    return 500000 / asset.priceValue


#def improve_quantity_with_sharpe(portfolio):
#
#    asset_sharpe_sum += [asset.sharpe for asset in portfolio.items]
#
#    for asset in portfolio.items:
#	sharpe_pourcentage = asset.sharpe / asset_sharpe_sum
#
#	portfolio.items.quantity * (-sharpe_pourcentage * 100 + 200)

