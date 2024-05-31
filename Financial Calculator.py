import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#get baseline data
benchmark = yf.Ticker("^GSPC") #SP500
bond = yf.Ticker("^TNX")

#get stock data
#activate THESE 2 LATER
ticker = input("Enter the stock symbol: ")
interval = input("Enter the interval ( Options: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'): ")
stock = yf.Ticker(ticker)

# overall historical prices for calculations
stock_data = yf.download(ticker, start='2020-01-01', end='2021-01-01')
index_data = yf.download('^GSPC', start='2020-01-01', end='2021-01-01')

# get financials
financials = stock.financials.T


# we transpose by using object.T
# we transpose because it will treat it like a dataframe (ie rows and columns)
# transpose income statement
income_statement = stock.income_stmt
income_statement_transposed = income_statement.T

# transpose the balance sheet
balance_sheet = stock.balance_sheet
balance_sheet_transposed = balance_sheet.T

# transpose the cash flow

cash_flow = stock.cash_flow.T

# stock history
hist = stock.history(period=interval)
bhist = benchmark.history(period=interval)
bdhist = bond.history(period=interval)
wantHist = input("Would you like to see the historical data? (y/n): ")
wantHist = "n"
if wantHist == "y":
    print(hist)

# Ensure datetime index consistency
if hist.index.tz is None:
    hist.index = hist.index.tz_localize('UTC')
else:
    hist.index = hist.index.tz_convert('UTC')

# This plotting the points stock prices
chart = input("Do you want a chart? (y/n): ")
if chart == 'y':
    x = hist['Open']
    y = hist['Close']
    plt.plot(x, y)
    plt.title(f"Historical Prices of {ticker} (w/interval {interval})")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()


# WACC calculations for DCF
DCF_activate = input("Do you want to perform a DCF (y/n): ")
if DCF_activate == "y":
    # all the information needed for cost of debt__________
    interest_expense = financials['Interest Expense'].iloc[0]

    # get total debt
    total_debt = balance_sheet_transposed['Total Debt'].iloc[0]

    cost_debt = interest_expense/total_debt

    inc_tax_expense = income_statement_transposed['Tax Provision'].iloc[0]

    inc_bef_tax = income_statement_transposed['Pretax Income'].iloc[0]
    effective_taxRATE = inc_tax_expense/inc_tax_expense
    cost_debt_AFTax = cost_debt * (1-effective_taxRATE)
    # Cost of Equity calculations_________
    # get returns
    # Calculate daily returns for the stock and the index
    stock_returns = stock_data['Adj Close'].pct_change()
    market_returns = index_data['Adj Close'].pct_change()
    # Create a DataFrame with both stock and index returns
    returns_df = pd.DataFrame({'Stock': stock_returns, 'Index': market_returns})

    # Drop missing values
    returns_df.dropna(inplace=True)

    # Calculate covariance matrix
    cov_matrix = np.cov(returns_df['Stock'], returns_df['Index'])

    # Calculate beta
    # calculating beta was difficult due to the fact that the dates were not aligning hence the need to drop a value
    beta = cov_matrix[0, 1] / cov_matrix[1, 1]

    # rfr from 10 year US Bond Rate
    rfr = bond.history(interval)['Close'].iloc[-1] / 100  # Dividing by 100 to convert to a decimal
    cost_equity = rfr + beta * (.09 - rfr)

    # Weight of Debt and Equity__________________________
    market_cap = stock.info['marketCap']
    total_DebtEquity = total_debt + market_cap

    weight_debt = total_debt / total_DebtEquity
    weight_equity = market_cap / total_DebtEquity

    # final WACC Calc
    WACC = (cost_debt * weight_debt) + (cost_equity * weight_equity)
# DCF Calculations
fcf = cash_flow["Free Cash Flow"]

# Initialize variables for calculating average growth rate
avg_growth = 0

# Calculate growth rates and accumulate for average
for x in range(1, 5):  # Start from 1 to avoid division by zero and go up to 4 for the last 4 periods
    growth_rate = (fcf.iloc[x] / fcf.iloc[x-1]) - 1
    avg_growth += growth_rate

# Calculate the average growth rate
avg_growth /= 4

for period in range(5):
    future_fcf = fcf.iloc[0] * (avg_growth + 1)
    discount = future_fcf / ((1 + WACC) ** period)

terminal_fcf = future_fcf * ((1+0.025) / (WACC - 0.025))

sum_fcf = terminal_fcf + discount

cash = balance_sheet_transposed["Cash And Cash Equivalents"].iloc[0]

equityValue = sum_fcf - total_debt + cash
shares_outstanding = stock.info['sharesOutstanding']

price_per_share = equityValue / shares_outstanding

currentPrice = stock.history(period="1d")['Close'].iloc[-1]

if price_per_share > currentPrice:
    print("BUY")
else:
    print("SELL")
