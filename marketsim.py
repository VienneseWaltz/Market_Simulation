""""""  		  	   		   	 			  		 			 	 	 		 		 	
"""MC2-P1: Market simulator.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 			  		 			 	 	 		 		 	
Atlanta, Georgia 30332  		  	   		   	 			  		 			 	 	 		 		 	
All Rights Reserved  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Template code for CS 4646/7646  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 			  		 			 	 	 		 		 	
works, including solutions to the projects assigned in this course. Students  		  	   		   	 			  		 			 	 	 		 		 	
and other users of this template code are advised not to share it with others  		  	   		   	 			  		 			 	 	 		 		 	
or to make it available on publicly viewable websites including repositories  		  	   		   	 			  		 			 	 	 		 		 	
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 			  		 			 	 	 		 		 	
or edited.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
We do grant permission to share solutions privately with non-students such  		  	   		   	 			  		 			 	 	 		 		 	
as potential employers. However, sharing with other current or future  		  	   		   	 			  		 			 	 	 		 		 	
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 			  		 			 	 	 		 		 	
GT honor code violation.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
-----do not edit anything above this line---  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Student Name: Stella Soh (replace with your name)  		  	   		   	 			  		 			 	 	 		 		 	
GT User ID: lsoh3 (replace with your User ID)  		  	   		   	 			  		 			 	 	 		 		 	
GT ID: 903641298 (replace with your GT ID)  		  	   		   	 			  		 			 	 	 		 		 	
"""
import math
import pandas as pd  		  	   		   	 			  		 			 	 	 		 		 	
from util import get_data, plot_data


def compute_portvals(  		  	   		   	 			  		 			 	 	 		 		 	
    orders_file="./orders/orders-01.csv",
    start_val=1000000,  		  	   		   	 			  		 			 	 	 		 		 	
    commission=9.95,
    impact=0.005
):  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Computes the portfolio values.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    :param orders_file: Path of the order file or the file object  		  	   		   	 			  		 			 	 	 		 		 	
    :type orders_file: str or file object  		  	   		   	 			  		 			 	 	 		 		 	
    :param start_val: The starting value of the portfolio  		  	   		   	 			  		 			 	 	 		 		 	
    :type start_val: int  		  	   		   	 			  		 			 	 	 		 		 	
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 			  		 			 	 	 		 		 	
    :type commission: float  		  	   		   	 			  		 			 	 	 		 		 	
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 			  		 			 	 	 		 		 	
    :type impact: float  		  	   		   	 			  		 			 	 	 		 		 	
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 			  		 			 	 	 		 		 	
    :rtype: pandas.DataFrame  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    # this is the function the autograder will call to test your code  		  	   		   	 			  		 			 	 	 		 		 	
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		   	 			  		 			 	 	 		 		 	
    # code should work correctly with either input  		  	   		   	 			  		 			 	 	 		 		 	
    # TODO: Your code here

    ##########################################################
    # 1. Build the first dataframe, df_prices
    ##########################################################

    # Create an empty dataframe, df_orders that uses the above dates as indices
    # df_orders = pd.DataFrame(index = dates)

    df_orders = pd.read_csv(orders_file, index_col = 'Date', parse_dates = True, na_values = ['nan'])

    # Sort by index labels in ascending order
    df_orders.sort_index(axis = 0, inplace = True)

    # Obtain the list of unique symbols
    symbols = list(df_orders.Symbol.unique())

    # Start date to track
    start_date = min(df_orders.index)

    # End date to track
    end_date = max(df_orders.index)

    # Obtain a DatetimeIndex with the specified start_date and end_date
    dates = pd.date_range(start_date, end_date)

    # SPY is automatically added when get_data() is used. prices_all spans from start_date and
    # end_date, and has 245 rows by 5 columns
    prices_all = get_data(symbols, dates)

    # From Lesson 1: to work around gaps in a DataFrame, fill forward, then fill backward
    prices_all.fillna(method = 'ffill')
    prices_all.fillna(method = 'bfill')

    # Remove SPY, get prices only for portfolio symbols in symbols. DataFrame df_prices holds the
    # adjusted closing prices for each symbol, and is now 245 rows by 4 columns
    df_prices = prices_all[symbols]

    # Add in a 'Cash' column at the end of df_prices and populate with 1.0's all the way
    # down to end_date
    df_prices.insert(len(symbols), 'Cash', [1.0]*df_prices.shape[0], True)


    ######################################################################
    # 2. Build and populate the second dataframe, df_trades
    ######################################################################

    # Make a copy of df_prices created above. This DataFrame represents the changes in the number of shares
    df_trades = df_prices.copy()

    # Initialize all rows and columns of df_trades to zero
    df_trades.iloc[:, :] = 0

    for date, row in df_orders.iterrows():
        symbol = row['Symbol']
        order = row['Order']
        shares = row['Shares']
        stock_price = df_prices.at[date, symbol]

        if order  == 'BUY':
            # Add appropriate number of shares to the count for that stock and subtract the
            # appropriate cost of the shares from the cash account
            df_trades.at[date, symbol] += shares
            df_trades.at[date,  'Cash'] -= stock_price * shares
        else:
            # It is a SELL order, and the accounting of the number of shares and cash reverse.
            df_trades.at[date, symbol] -= shares
            df_trades.at[date, 'Cash'] += stock_price * shares
        # Part 2: Factoring in the transaction costs
        df_trades.at[date, 'Cash'] -= commission + (impact * stock_price * shares)


    #####################################################################
    # 3. Build and populate the third dataframe, df_holdings
    #####################################################################

    # Make a copy of df_trades created above
    df_holdings = df_trades.copy()

    # Handling the 'Cash' column on the first row
    df_holdings.iloc[0]['Cash'] += start_val

    # Iterate over the rows to find the cumulative sum in each equity column of df_holdings
    df_holdings = df_holdings.cumsum()


    ###############################################################
    # 4. Build and populate the fourth dataframe, df_values
    ################################################################

    # DataFrame df_values is a product of df_prices and df_holdings
    df_values = df_prices * df_holdings


    ##################################################################
    # 5. Build and populate the fifth dataframe, df_port_values
    ###################################################################

    # df_port_values = pd.DataFrame(index=df_holdings.index)
    df_port_values = df_values.sum(axis=1)

    portvals = df_port_values
    print(f' The portfolio values = {portvals}')
  		  	   		   	 			  		 			 	 	 		 		 	

    return portvals


def author():
    return 'lsoh3'


def cal_port_stats(portvals):

    # Cumulative returns
    cr = (portvals[-1]/portvals[0]) - 1

    # Daily returns
    dr = (portvals/portvals.shift(1)) - 1

    # Remove the top row
    dr = dr[1:]

    # Mean or average daily returns
    adr = dr.mean()

    # Standard deviation of daily returns
    sddr = dr.std()

    # Risk-free rate
    rfr = 0.0

    # Sharpe ratio
    sr = math.sqrt(252) * ((dr - rfr).mean() / sddr)

    return cr, adr, sddr, sr


  		  	   		   	 			  		 			 	 	 		 		 	
def test_code():  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Helper function to test code  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    # this is a helper function you can use to test your code  		  	   		   	 			  		 			 	 	 		 		 	
    # note that during autograding his function will not be called.  		  	   		   	 			  		 			 	 	 		 		 	
    # Define input parameters  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    of = "./orders/orders-01.csv"
    sv = 1000000  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    # Process orders  		  	   		   	 			  		 			 	 	 		 		 	
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):  		  	   		   	 			  		 			 	 	 		 		 	
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		   	 			  		 			 	 	 		 		 	
    else:  		  	   		   	 			  		 			 	 	 		 		 	
        "warning, code did not return a DataFrame"  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    # Get portfolio stats  		  	   		   	 			  		 			 	 	 		 		 	
    # Here we just fake the data. you should use your code from previous assignments.

    start_date = portvals.index.min()
    end_date = portvals.index.max()
    dates = pd.date_range(start_date, end_date)

    # Obtain cumulative returns, average daily returns, standard deviation for daily returns
    # and Sharpe ratio of the portfolio
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = cal_port_stats(portvals)


    # Portfolio values of SPY
    portvals_SPY = get_data(['SPY'], dates)

    # Remove the 'SPY' heading in portvals_SPY and save into k
    k = portvals_SPY.sum(axis=1)

    # Obtain cumulative returns, average daily returns, standard deviation for daily returns
    # and Sharpe ratio of S&P 500
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = cal_port_stats(k)

  		  	   		   	 			  		 			 	 	 		 		 	
    # Compare portfolio against $SPX  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Date Range: {start_date} to {end_date}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
if __name__ == "__main__":  		  	   		   	 			  		 			 	 	 		 		 	
    test_code()  		  	   		   	 			  		 			 	 	 		 		 	
