def process_leveraged_data(ticker, leverage_scalar=None):
    """
    Download historical data for a given ticker and simulate leveraged ETF data.

    Parameters:
        ticker (str): Ticker symbol of the baseline index (e.g., "QQQ").
        leverage_scalar (float, optional): Scalar for leveraged equity returns. 
            If None, prompts the user for input.

    Returns:
        pd.DataFrame: DataFrame containing the simulated leveraged ETF data.
    """
    # Download the baseline data
    print(f"Downloading data for {ticker}...")
    baseline_data = yf.download(ticker, progress=False)

    # Get leverage scalar from user if not provided
    if leverage_scalar is None:
        while True:
            try:
                leverage_scalar = float(input("Enter the scalar for the leveraged equity returns (e.g., 3): "))
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
                
    # Calculate daily returns (pct_change introduces NaN in the first row)
    baseline_data['Daily Return'] = baseline_data['Adj Close'].pct_change()

    # Simulate leveraged returns (remove NaN for first row calculation)
    baseline_data['Leveraged Return'] = baseline_data['Daily Return'] * leverage_scalar
    baseline_data['Leveraged Return'].iloc[0] = 0  # Ensure the first leveraged return is 0

    # Initialize the simulated leveraged price column
    baseline_data['Simulated Leveraged Price'] = baseline_data['Adj Close'].iloc[0]  # Starting price
    
    # Calculate cumulative price using Leveraged Return
    for i in range(1, len(baseline_data)):
        baseline_data['Simulated Leveraged Price'].iloc[i] = (
            baseline_data['Simulated Leveraged Price'].iloc[i-1] *
            (1 + baseline_data['Leveraged Return'].iloc[i])
        )

    return baseline_data