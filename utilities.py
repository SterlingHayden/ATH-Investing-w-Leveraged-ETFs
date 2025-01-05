import yfinance as yf
import pandas as pd

#########################################################################################################################################################
def process_leveraged_data(tickers, leverage_scalars, portfolio_weights):
    """
    Download historical data for given tickers, simulate leveraged ETF data, 
    and calculate their weighted contributions to the portfolio.

    Parameters:
        tickers (list of str): List of ticker symbols (e.g., ["QQQ", "SPY"]).
        leverage_scalars (list of float): List of scalars for leveraged equity returns (e.g., [3, 1]).
        portfolio_weights (list of float): List of portfolio weights for each ticker; must sum to 1 (e.g., [.2, .8]).

    Returns:
        pd.DataFrame: DataFrame with formatted columns for each ticker and weighted portfolio returns.
    """
    if len(tickers) != len(leverage_scalars) or len(tickers) != len(portfolio_weights): # Check if there is a leverage_scalars & portfolio_weight for each ticker
        raise ValueError("The number of tickers, leverage scalars, and portfolio weights must match.")
    
    if not abs(sum(portfolio_weights) - 1.0) < 1e-6: # Check if portfolio_weights sums to 1
        raise ValueError("Portfolio weights must sum to 1.")

    # Find the latest first date across all tickers
    start_date = None
    for ticker in tickers:
        ticker_data = yf.download(ticker, progress=False)
        earliest_date = ticker_data.index.min()
        if start_date is None or earliest_date > start_date:
            start_date = earliest_date

    result_df = pd.DataFrame()  # Initialize an empty DataFrame for results

    for ticker, scalar, weight in zip(tickers, leverage_scalars, portfolio_weights):
        print(f"Downloading data for {ticker}...")

        # Download the baseline data
        baseline_data = yf.download(ticker, progress=False)

        # Drop rows before the latest start date
        baseline_data = baseline_data[baseline_data.index >= start_date]
        baseline_data = baseline_data.copy() # Make copy to stop slicing issues

        # Calculate daily returns
        baseline_data['Daily Return'] = baseline_data['Adj Close'].pct_change()

        # Simulate leveraged returns based on the scalar
        baseline_data['Leveraged Return'] = baseline_data['Daily Return'] * scalar
        baseline_data.loc[baseline_data.index[0], 'Leveraged Return'] = 0  # Ensure the first leveraged return is 0

        # Weighted leveraged return
        baseline_data['Weighted Leveraged Return'] = baseline_data['Leveraged Return'] * weight

        # Calculate simulated leveraged price
        baseline_data['Simulated Leveraged Price'] = (1 + baseline_data['Weighted Leveraged Return']).cumprod()
        baseline_data['Simulated Leveraged Price'] *= baseline_data['Adj Close'].iloc[0]  # Normalize to starting price

        # Rename columns to include the ticker symbol
        baseline_data = baseline_data.rename(
            columns={
                'Daily Return': f'DailyReturn_{ticker}',
                'Adj Close': f'AdjClose_{ticker}',
                'Leveraged Return': f'LeveragedReturn_{ticker}_{scalar}X',
                'Simulated Leveraged Price': f'SimulatedLeveragedPrice_{ticker}_{scalar}X',
                'Weighted Leveraged Return': f'WeightedLeveragedReturn_{ticker}_{scalar}X'
            }
        )

        # Keep only relevant columns and reset index
        baseline_data = baseline_data[[f'DailyReturn_{ticker}', f'AdjClose_{ticker}', 
                                       f'LeveragedReturn_{ticker}_{scalar}X', f'SimulatedLeveragedPrice_{ticker}_{scalar}X', 
                                       f'WeightedLeveragedReturn_{ticker}_{scalar}X']]
        
        baseline_data.reset_index(inplace=True)

        # Merge with the result DataFrame
        if result_df.empty:
            result_df = baseline_data
        else:
            result_df = pd.merge(result_df, baseline_data, on='Date', how='outer')

    # Calculate total portfolio returns
    weighted_columns_1 = [col for col in result_df.columns if col.startswith('LeveragedReturn')]
    result_df['TotalPortfolioReturn'] = result_df[weighted_columns_1].sum(axis=1)
    # Calculate total portfolio price
    weighted_columns_2 = [col for col in result_df.columns if col.startswith('SimulatedLeveragedPrice')]
    result_df['TotalPortfolioPrice'] = result_df[weighted_columns_2].sum(axis=1)


    return result_df.dropna().reset_index(drop=True)


#########################################################################################################################################################
def find_ath_indices(data, column, window=0):
    """
    Find indices where the column reaches a new all-time high and optionally expand indices by window of days.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        column (str): The column name to evaluate for all-time highs.
        Similarly, as mentioned above, we can examine the spread across multiple windows. (int): Number of days to expand the indices by (± window). Default is 0.
    
    Returns:
        list: List of indices where a new all-time high is set, optionally expanded.
    """
    ath_indices = []
    current_ath = -9999
    
    # Find new all-time highs
    for idx, value in data[column].items():
        if value > current_ath:
            current_ath = value
            ath_indices.append(idx)
    
    # Expand indices if window > 0
    if window > 0:
        expanded_indices = set()
        for idx in ath_indices:
            for offset in range(-window, window + 1):  # ±window range
                new_idx = idx + offset
                if 0 <= new_idx < len(data):  # Ensure within bounds
                    expanded_indices.add(new_idx)
        ath_indices = sorted(expanded_indices)
    
    return ath_indices

#########################################################################################################################################################
def calculate_ath_returns_all_periods(data, ath_indices):
    holding_periods = {
        'Return_3M': 91,  # 3 months
        'Return_6M': 182, # 6 months
        'Return_12M': 365, # 12 months
        'Return_24M': 730, # 2 Years
        'Return_48M': 1460, # 4 Years
    }
    
    results = []
    for idx in ath_indices:
        row = {'ATH_Index': idx, 'Date': data.loc[idx, 'Date']}
        for period_name, holding_period in holding_periods.items():
            if idx + holding_period < len(data):
                entry_price = data['TotalPortfolioPrice'].iloc[idx]
                exit_price = data['TotalPortfolioPrice'].iloc[idx + holding_period]
                return_pct = (exit_price - entry_price) / entry_price
                row[period_name] = return_pct
            else:
                row[period_name] = None  # Handle cases where holding period exceeds data length

        results.append(row)
    return pd.DataFrame(results)




def calculate_non_ath_returns_all_periods(data, ath_indices):
    holding_periods = {
        'Return_3M': 91,  # 3 months
        'Return_6M': 182, # 6 months
        'Return_12M': 365, # 12 months
        'Return_24M': 730, # 2 Years
        'Return_48M': 1460, # 4 Years
    }
    
    results = []

    for idx in data.index:
        if idx not in ath_indices:  # Exclude ATH indices
            row = {'Index': idx, 'Date': data.loc[idx, 'Date']}
            for period_name, holding_period in holding_periods.items():
                if idx + holding_period < len(data):  # Ensure holding period is valid
                    entry_price = data['TotalPortfolioPrice'].iloc[idx]
                    exit_price = data['TotalPortfolioPrice'].iloc[idx + holding_period]
                    return_pct = (exit_price - entry_price) / entry_price
                    row[period_name] = return_pct
                else:
                    row[period_name] = None  # Handle cases where holding period exceeds data length
            
            results.append(row)
    return pd.DataFrame(results)
