# main.py

import os
import pandas as pd
from indicators.sma import calculate_sma
from indicators.rsi import calculate_rsi
from indicators.ema import calculate_ema
from indicators.bollinger_bands import calculate_bollinger_bands
from indicators.macd import calculate_macd
from indicators.atr import calculate_atr

# Define the path to the price history folder
PRICE_HISTORY_FOLDER = "price_history"

# Variable to point to the specific price history file (update this variable with the filename to use)
price_file = "BNBUSDT.csv"  # Replace with your desired file


# Function to load price data from the specified CSV file
def load_price_data(filename):
    """
    Load the price data from a CSV file located in the 'price_history' folder.

    The CSV should contain the following columns in order:
    - Date
    - Open
    - High
    - Low
    - Close
    - Volume

    Any columns beyond the 6th will be ignored during extraction.

    :param filename: The name of the CSV file to load.
    :return: A Pandas DataFrame with the first 6 columns (Date, Open, High, Low, Close, Volume).
    """
    # Construct the full path to the CSV file
    file_path = os.path.join(PRICE_HISTORY_FOLDER, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {filename} not found in {PRICE_HISTORY_FOLDER} folder.")

    # Load the CSV file into a DataFrame
    try:
        # Load only the first 6 columns from the CSV file (headers will be auto-detected)
        df = pd.read_csv(file_path, usecols=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        return df
    except Exception as e:
        raise ValueError(f"Error loading file {filename}: {e}")


# Main function to execute the script
def main():
    """
    Main execution flow of the script.
    Loads the price data from the CSV file and processes it.
    """
    # Step 1: Load the price data from the specified CSV file
    try:
        price_data = load_price_data(price_file)
        print(f"Successfully loaded price data from {price_file}.")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    # Step 2: Display the first few rows of the data to verify it's loaded correctly
    print("First 6 rows of the price data:")
    print(price_data.head())

    # Step 3: Example usage of the indicators
    price_data['SMA_20'] = calculate_sma(price_data, period=20)  # Simple Moving Average
    price_data['RSI_14'] = calculate_rsi(price_data, period=14)  # Relative Strength Index
    price_data['EMA_20'] = calculate_ema(price_data, period=20)  # Exponential Moving Average

    bollinger_bands = calculate_bollinger_bands(price_data, period=20)  # Bollinger Bands
    macd = calculate_macd(price_data)  # MACD
    price_data['ATR_14'] = calculate_atr(price_data, period=14)  # ATR

    # Display the calculated Bollinger Bands, MACD, and ATR (optional)
    print("\nBollinger Bands:")
    print(bollinger_bands.tail(10))

    print("\nMACD:")
    print(macd.tail(10))

    print("\nATR:")
    print(price_data[['Date', 'ATR_14']].tail(10))


# Entry point of the script
if __name__ == "__main__":
    main()
