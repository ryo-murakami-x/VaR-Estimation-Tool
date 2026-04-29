"""
Stock Data Reader Module
Reads Stooq CSV files for TSE stock data and prepares data for VaR analysis
"""

import os
import pandas as pd
from pathlib import Path
from typing import Optional, Tuple


class StooqDataReader:
    """
    A class to read and parse Stooq CSV files containing TSE stock data.
    """
    
    def __init__(self, data_base_path: str = "/Users/ryo_murakami/CodingProject/AIProject/AI_VaRsystem_dev_test/data/daily/jp/tse stocks"):
        """
        Initialize the data reader with the base path to stock data.
        
        Args:
            data_base_path (str): Base path to the data directory
        """
        self.data_base_path = data_base_path
        self.df = None
        self.ticker = None
        self.file_path = None
        
    def _find_stock_file(self, ticker: str) -> Optional[str]:
        """
        Find the stock data file for a given ticker.
        
        Args:
            ticker (str): Stock ticker code (e.g., "1305", "130a", "2989")
        
        Returns:
            Optional[str]: Full path to the file if found, None otherwise
        """
        # First, try directory structure (stocks/1/, stocks/2/, etc.)
        for subdir in ['1', '2']:  # Based on the directory structure
            possible_path = os.path.join(self.data_base_path, subdir, f"{ticker}.jp.txt")
            if os.path.exists(possible_path):
                return possible_path
        
        # If not found in numbered directories, search in the main directory
        possible_path = os.path.join(self.data_base_path, f"{ticker}.jp.txt")
        if os.path.exists(possible_path):
            return possible_path
        
        return None
    
    def load_stock_data(self, ticker: str) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Load stock data for a given ticker.
        
        Args:
            ticker (str): Stock ticker code (without .jp extension)
        
        Returns:
            Tuple[bool, str, Optional[pd.DataFrame]]: 
                - Success flag (True/False)
                - Message (status/error message)
                - DataFrame with the data (None if failed)
        """
        # Validate input
        if not ticker or not isinstance(ticker, str):
            return False, "Invalid ticker: must be a non-empty string", None
        
        ticker = ticker.strip().upper()
        
        # Find the file
        file_path = self._find_stock_file(ticker)
        if not file_path:
            return False, f"Stock data file not found for ticker: {ticker}", None
        
        try:
            # Read the CSV file
            # The first line contains column definitions like <TICKER>, <DATE>, etc.
            df = pd.read_csv(file_path)
            
            # Rename columns to remove angle brackets
            df.columns = [col.strip('<>') for col in df.columns]
            
            # Convert DATE to datetime format
            df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
            
            # Convert numeric columns to appropriate data types
            numeric_cols = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL', 'OPENINT']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Sort by date in ascending order
            df = df.sort_values('DATE').reset_index(drop=True)
            
            self.df = df
            self.ticker = ticker
            self.file_path = file_path
            
            return True, f"Successfully loaded {len(df)} records for ticker {ticker}", df
        
        except Exception as e:
            return False, f"Error reading file {file_path}: {str(e)}", None
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Get the currently loaded data.
        
        Returns:
            Optional[pd.DataFrame]: The loaded DataFrame or None if no data is loaded
        """
        return self.df
    
    def get_ticker(self) -> Optional[str]:
        """
        Get the ticker of the currently loaded stock.
        
        Returns:
            Optional[str]: The ticker code or None if no data is loaded
        """
        return self.ticker
    
    def get_file_path(self) -> Optional[str]:
        """
        Get the file path of the currently loaded data.
        
        Returns:
            Optional[str]: The file path or None if no data is loaded
        """
        return self.file_path
    
    def get_summary_info(self) -> dict:
        """
        Get summary information about the loaded data.
        
        Returns:
            dict: Summary statistics including date range, records count, etc.
        """
        if self.df is None:
            return {"error": "No data loaded"}
        
        info = {
            "ticker": self.ticker,
            "records": len(self.df),
            "start_date": self.df['DATE'].min().strftime('%Y-%m-%d') if 'DATE' in self.df.columns else None,
            "end_date": self.df['DATE'].max().strftime('%Y-%m-%d') if 'DATE' in self.df.columns else None,
            "columns": list(self.df.columns),
            "file_path": self.file_path
        }
        
        if 'CLOSE' in self.df.columns:
            info["close_price_min"] = float(self.df['CLOSE'].min())
            info["close_price_max"] = float(self.df['CLOSE'].max())
            info["close_price_mean"] = float(self.df['CLOSE'].mean())
        
        return info
    
    def get_daily_returns(self) -> Optional[pd.Series]:
        """
        Calculate daily returns (percentage change) from close prices.
        
        Returns:
            Optional[pd.Series]: Series of daily returns or None if data not loaded
        """
        if self.df is None or 'CLOSE' not in self.df.columns:
            return None
        
        returns = self.df['CLOSE'].pct_change() * 100  # Convert to percentage
        return returns
    
    def validate_data(self) -> Tuple[bool, list]:
        """
        Validate the loaded data for quality issues.
        
        Returns:
            Tuple[bool, list]: (is_valid, list_of_issues)
        """
        issues = []
        
        if self.df is None:
            return False, ["No data loaded"]
        
        # Check for missing values in critical columns
        critical_cols = ['DATE', 'CLOSE', 'OPEN', 'HIGH', 'LOW']
        for col in critical_cols:
            if col in self.df.columns:
                missing = self.df[col].isna().sum()
                if missing > 0:
                    issues.append(f"Column '{col}' has {missing} missing values")
        
        # Check for data consistency (High >= Low, etc.)
        if 'HIGH' in self.df.columns and 'LOW' in self.df.columns:
            invalid = (self.df['HIGH'] < self.df['LOW']).sum()
            if invalid > 0:
                issues.append(f"{invalid} records have HIGH < LOW (data inconsistency)")
        
        return len(issues) == 0, issues


def interactive_stock_selector() -> Optional[str]:
    """
    Interactive function to prompt user for stock ticker selection.
    
    Returns:
        Optional[str]: Selected ticker or None if user cancels
    """
    print("\n" + "="*60)
    print("TSE Stock Data Reader - Interactive Mode")
    print("="*60)
    print("\nEnter a stock ticker code (e.g., 1305, 1306, 2989, etc.)")
    print("Or type 'list' to see available stocks")
    print("Type 'quit' to exit\n")
    
    while True:
        ticker = input("Enter stock ticker: ").strip()
        
        if ticker.lower() == 'quit':
            return None
        
        if ticker.lower() == 'list':
            print("\nSearching for available stocks...")
            data_base_path = "/Users/ryo_murakami/CodingProject/AIProject/AI_VaRsystem_dev_test/data/daily/jp/tse stocks"
            
            stocks = []
            for subdir in ['1', '2']:
                subdir_path = os.path.join(data_base_path, subdir)
                if os.path.exists(subdir_path):
                    files = os.listdir(subdir_path)
                    stocks.extend([f.replace('.jp.txt', '') for f in files if f.endswith('.jp.txt')])
            
            stocks.sort()
            print(f"\nFound {len(stocks)} stocks:")
            print(", ".join(stocks[:20]) + ("..." if len(stocks) > 20 else ""))
            print("\n")
            continue
        
        if ticker:
            return ticker
        else:
            print("Please enter a valid ticker code.\n")


def main():
    """
    Main function to demonstrate the data reader.
    """
    # Create reader instance
    reader = StooqDataReader()
    
    # Interactive mode - ask user for ticker
    ticker = interactive_stock_selector()
    if ticker is None:
        print("\nExiting...")
        return
    
    # Load the data
    print(f"\nLoading data for ticker: {ticker}...")
    success, message, df = reader.load_stock_data(ticker)
    
    print(message)
    
    if success:
        # Display summary
        print("\n" + "="*60)
        print("Data Summary")
        print("="*60)
        summary = reader.get_summary_info()
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # Validate data
        print("\n" + "="*60)
        print("Data Validation")
        print("="*60)
        is_valid, issues = reader.validate_data()
        if is_valid:
            print("✓ Data validation passed!")
        else:
            print("✗ Data validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
        
        # Display first and last few records
        print("\n" + "="*60)
        print("Data Preview (First 5 rows)")
        print("="*60)
        print(df.head())
        
        print("\n" + "="*60)
        print("Data Preview (Last 5 rows)")
        print("="*60)
        print(df.tail())
        
        # Calculate and display daily returns
        returns = reader.get_daily_returns()
        if returns is not None:
            print("\n" + "="*60)
            print("Daily Returns Statistics")
            print("="*60)
            print(f"Mean return: {returns.mean():.4f}%")
            print(f"Std deviation: {returns.std():.4f}%")
            print(f"Min return: {returns.min():.4f}%")
            print(f"Max return: {returns.max():.4f}%")
    else:
        print(f"Failed to load data.")


if __name__ == "__main__":
    main()
