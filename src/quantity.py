# coding: utf-8
#
#   Quantity
#
#
#   Compute the quantity for every asset in a portfolio 
#

#from portfolio import Portfolio


def compute_quantity_by_return(asset):

    # Let's set a quantity to get 500k€, which is 1/20 of 10M€
    quantity = 500000 / asset.priceValue

    print "id : " + str(asset.id)
    print "Quantity   = " + str(quantity)
    print "Qtt * " + str(asset.priceValue) + " = " + str(quantity * asset.priceValue)
    return quantity

#def improve_quantity_with_sharpe(portfolio):
#
#    asset_sharpe_sum += [asset.sharpe for asset in portfolio.items]
#
#    for asset in portfolio.items:
#	sharpe_pourcentage = asset.sharpe / asset_sharpe_sum
#
#	portfolio.items.quantity * (-sharpe_pourcentage * 100 + 200)

