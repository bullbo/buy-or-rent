import numpy as np

def _intrest(arr, rate):
  for i in range(1,len(arr)):
    arr[i] = arr[i-1]*rate
  return arr


def calcs(years, rent, rent_increase, loan, intrest, amort, fee, fee_increase):
    ones = np.ones(years)
    years = np.arange(1, years+1)
    rent = rent*12
    fee = fee*12
    rent_increase /= 100
    amort /= 100
    intrest /= 100
    fee_increase /= 100

    amort_left = _intrest(loan*ones, 1-amort)

    yearly_rent = _intrest(rent*ones, 1+rent_increase)
    yearly_fee = _intrest(fee*ones, 1+fee_increase)
    yearly_intrest = amort_left*intrest
    yearly_buy = yearly_fee+yearly_intrest

    cost_rent = np.cumsum(yearly_rent)
    cost_fee = np.cumsum(yearly_fee)
    cost_intrest = np.cumsum(yearly_intrest)
    cost_buy = np.cumsum(yearly_buy)

    return {"yearly-rent"   : yearly_rent,
            "yearly-fee"    : yearly_fee,
            "yearly-intrest": yearly_intrest,
            "yearly-buy"    : yearly_buy,
            "cost-rent"     : cost_rent, 
            "cost-fee"      : cost_fee,
            "cost-intrest"  : cost_intrest,
            "cost-buy"      :cost_buy,
            "amort-left"    : amort_left}