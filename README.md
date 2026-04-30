# VaR Estimation Tool for Stooq TSE Stock Data

A comprehensive Value at Risk (VaR) estimation tool using Monte Carlo simulation for Tokyo Stock Exchange (TSE) stocks based on Stooq data.

## Features

### 1. **Data Reader Component** (`data_reader.py`)
- Reads Stooq CSV format stock data files
- Supports interactive ticker selection
- Data validation and quality checks
- Calculates historical daily returns
- Provides summary statistics

### 2. **Monte Carlo VaR Calculator** (`var_calculator.py`)
- Simulates stock price paths using Geometric Brownian Motion
- Calculates Value at Risk (VaR) at multiple confidence levels
- Computes Expected Shortfall (Conditional Value at Risk)
- Additional risk metrics (skewness, kurtosis, percentiles)
- Converts VaR to dollar terms

### 3. **GUI Application** (`var_gui.py`)
- User-friendly interface built with tkinter
- Real-time data loading and validation
- Interactive VaR parameter configuration
- Distribution visualization with matplotlib
- Results display with detailed statistics
- Data preview of loaded stock data

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Steps

1. **Clone/Navigate to the project directory:**
```bash
cd /path/to/VaR-Estimation-Tool
```

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

## 📥 Downloading Stock Data from Stooq

Before using the application, you need to download CSV files from Stooq.

### Quick Steps

1. **Visit Stooq Historical Data**: https://stooq.com/db/h/
2. **Select TSE (Tokyo Stock Exchange)** stocks
3. **Download CSV files** for desired stock tickers (e.g., 1301, 1332, 2001)
4. **Use downloaded files directly** (no manual directory organization steps required)

### Expected File Format

CSV files must contain:
- `<TICKER>`: Stock ticker
- `<DATE>`: Date in YYYYMMDD format
- `<CLOSE>`: Closing price (used for VaR calculation)
- `<OPEN>`, `<HIGH>`, `<LOW>`, `<VOL>`: Additional data

**For detailed data setup instructions**, see: **[STOOQ_DATA_SETUP.md](STOOQ_DATA_SETUP.md)**

## Usage

### Running the GUI Application

```bash
python3 main.py
```

or directly:

```bash
python3 var_gui.py
```

### Using Command-Line Data Reader

```bash
python3 data_reader.py
```

This launches an interactive mode where you can:
- Enter stock ticker (e.g., 1301, 1305, 2989)
- View data summary
- See first/last rows
- Check daily returns statistics
- Type 'list' to see available stocks
- Type 'quit' to exit

## GUI Components

### Left Panel - Controls
- **Stock Selection**: Enter ticker code and load data
- **Data Information**: Displays loaded data statistics
- **VaR Parameters**: Configure calculation parameters
  - Number of Simulations (1,000 - 100,000)
  - Time Horizon (1 - 252 days)
  - Confidence Level (90%, 95%, 99%)
  - Portfolio Value (in ¥)

### Right Panel - Results
Three tabs:
1. **VaR Results**: Displays comprehensive VaR statistics
2. **Distribution Chart**: Histogram of simulated returns with VaR lines
3. **Data Preview**: Shows last 20 records of loaded data

## Data Structure

Stock data files are located at:
```
data/daily/jp/tse stocks/
├── 1/
│   ├── 1301.jp.txt
│   ├── 1305.jp.txt
│   └── ...
└── 2/
    ├── 2301.jp.txt
    ├── 2302.jp.txt
    └── ...
```

### File Format (CSV)
```
<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>
1301.JP,D,20050322,000000,2100.74,2135.41,2083.4,2109.41,276592,0
```

## VaR Calculation Details

### Methodology
The tool uses **Monte Carlo Simulation** with **Geometric Brownian Motion** (GBM):

$$dS = \mu \cdot S \cdot dt + \sigma \cdot S \cdot dW$$

Where:
- S: Stock price
- μ: Mean daily return
- σ: Daily volatility
- dt: Time step
- dW: Random normal variable

### Confidence Levels
- **95% VaR**: Maximum expected loss with 95% probability
- **99% VaR**: Maximum expected loss with 99% probability

### Risk Metrics
- **Expected Shortfall (CVaR)**: Average loss beyond VaR
- **Skewness**: Distribution asymmetry
- **Kurtosis**: Distribution tail behavior

## Example Workflow

1. **Launch the application:**
   ```bash
   python3 main.py
   ```

2. **Load stock data:**
   - Enter ticker (e.g., "1301")
   - Click "Load Data"
   - Review data information and preview

3. **Configure VaR parameters:**
   - Simulations: 10,000 (default)
   - Time Horizon: 10 days (default)
   - Confidence Level: 95% (default)
   - Portfolio Value: 1,000,000 ¥ (default)

4. **Calculate VaR:**
   - Click "Calculate VaR"
   - View results in "VaR Results" tab
   - Check distribution chart in "Distribution Chart" tab

5. **Interpret Results:**
   - For 95% confidence: Maximum expected loss over 10 days
   - For 99% confidence: More conservative estimate
   - Dollar amount: Actual loss in yen (¥)

## Example Output

```
==================================================
VaR ESTIMATION RESULTS
==================================================

PARAMETERS:
  Time Horizon: 10 trading days
  Simulations: 10,000
  Portfolio Value: ¥1,000,000
  Current Stock Price: ¥4,640.00

HISTORICAL STATISTICS:
  Mean Daily Return: 0.0276%
  Daily Volatility: 1.5809%

VaR RESULTS:
  
  95% Confidence Level:
    VaR (percentage): -1.2345%
    VaR (dollar): ¥12,345.00
    Expected Shortfall: -1.5678%
    
  99% Confidence Level:
    VaR (percentage): -1.8901%
    VaR (dollar): ¥18,901.00
    Expected Shortfall: -2.1234%
```

## Performance Considerations

- **Simulations**: More simulations = more accurate but slower
  - 1,000: Fast (~1 sec)
  - 10,000: Balanced (default, ~5 sec)
  - 100,000: Accurate but slower (~30 sec)

- **Time Horizon**: Longer horizons increase computational time

## Modules

### `data_reader.py`
**Classes:**
- `StooqDataReader`: Main data reading class

**Key Methods:**
- `load_stock_data(ticker)`: Load data for specific ticker
- `get_daily_returns()`: Calculate daily returns
- `get_summary_info()`: Get data statistics
- `validate_data()`: Check data quality

### `var_calculator.py`
**Classes:**
- `MonteCarloVaR`: VaR calculation engine
- `VaRResults`: Data class for results

**Key Methods:**
- `simulate_price_paths()`: Generate price scenarios
- `calculate_var()`: Single confidence level VaR
- `calculate_var_comprehensive()`: Multi-level VaR
- `get_risk_metrics()`: Additional risk statistics

### `var_gui.py`
**Classes:**
- `VaREstimationGUI`: Main GUI application

### `main.py`
Entry point for launching the GUI application

## Requirements

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Data visualization
- **tkinter**: GUI framework (comes with Python)

## Limitations

1. Historical data-based analysis (assumes past = future)
2. Assumes normal distribution (may underestimate tail risk)
3. Single stock analysis (not portfolio-based)
4. No real-time data updates

## Troubleshooting

### Issue: Stock data file not found
- Verify ticker code is correct
- Verify downloaded CSV data is available and readable
- Use 'list' command in data_reader.py to see available stocks

### Issue: GUI doesn't appear
- Ensure tkinter is installed: `python3 -m tkinter`
- On macOS: May need to use `python3` instead of `python`

### Issue: Slow calculation
- Reduce number of simulations
- Reduce time horizon
- Check system resources

## Future Enhancements

- [ ] Portfolio VaR (multiple stocks)
- [ ] Real-time data integration
- [ ] GARCH volatility modeling
- [ ] Historical VaR comparison
- [ ] Export results to Excel/PDF
- [ ] Additional distribution models (Student-t, etc.)
- [ ] Backtesting framework
- [ ] Performance benchmarking

## References

- Hull, J. C. (2021). Risk Management and Financial Institutions
- Dowd, K. (2007). Measuring Market Risk
- Stooq: https://stooq.com/

## License

This project is provided as-is for educational purposes.

## Author

Created for AI-based VaR System Development

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the data format requirements
3. Verify all dependencies are installed
