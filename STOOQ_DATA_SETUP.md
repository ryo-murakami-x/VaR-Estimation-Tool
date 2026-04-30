# Stooq Data Setup Guide

Complete guide for downloading CSV files from Stooq and setting them up for the VaR Estimation Tool.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Detailed Instructions](#detailed-instructions)
3. [Data Requirements](#data-requirements)
4. [File Format Requirements](#file-format-requirements)
5. [Troubleshooting](#troubleshooting)
6. [Batch Download](#batch-download)

---

## Quick Start

**TL;DR**: Download CSV files from [Stooq Historical Data](https://stooq.com/db/h/) and use them directly in the tool (no manual directory organization steps required).

---

## Detailed Instructions

### Step 1: Visit Stooq Website

1. Open your web browser
2. Go to: **https://stooq.com/db/h/**
3. You'll see the Stooq historical data download page

### Step 2: Select Tokyo Stock Exchange (TSE) Data

1. On the Stooq website, look for filter options or category selection
2. Select: **Japan** → **Tokyo Stock Exchange (TSE)**
3. Or filter by stock list containing TSE stocks

### Step 3: Find Your Stock

**Option A: Search for a Specific Stock**
- Use the search box on Stooq
- Enter ticker code (e.g., `1301` for Toyota)
- Click on the stock result

**Option B: Browse Stock List**
- Go to: **https://stooq.com/db/h/?d=1** (for TSE stocks)
- Scroll through the available stocks
- Click on a stock to open its page

### Step 4: Download CSV File

1. **On the stock's page** (e.g., https://stooq.com/q/?s=1301.JP for Toyota):
   - Look for the **"Download"** button or link
   - Usually located near the top of the data table

2. **Alternative method** (Direct Stooq database):
   - Go to: **https://stooq.com/db/h/?d=1** 
   - Find the stock in the list
   - Click on the download icon (often a down arrow 📥)

3. **On Stooq Quotes Page**:
   - Go to: **https://stooq.com/q/?s=TICKER.JP** (replace TICKER with stock code)
   - Example: **https://stooq.com/q/?s=1301.JP**
   - Look for the download/export button
   - Select CSV format
   - Click "Download"

### Step 5: Verify Downloaded File Format

After downloading, **verify the file contains**:

```
<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>
1301,d,20220101,000000,1234.5,1245.3,1230.2,1240.5,12345600,0
1301,d,20220104,000000,1241.0,1255.0,1235.5,1250.3,9876500,0
...
```

**Key columns to verify**:
- `<TICKER>`: Stock ticker (e.g., 1301)
- `<DATE>`: Date in YYYYMMDD format (e.g., 20220101)
- `<CLOSE>`: Closing price (this is used for VaR calculation)
- `<VOL>`: Trading volume

---

## Data Requirements

No manual folder creation, file moving, or renaming workflow is required in this guide.
Focus on downloading valid CSV data and confirming its format.

---

## File Format Requirements

### CSV Format

The application expects **Stooq CSV format** with these columns:

```
<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>
```

| Column | Format | Example | Required |
|--------|--------|---------|----------|
| `<TICKER>` | Text | 1301 | ✅ Yes |
| `<PER>` | Text ('d' for daily) | d | ✅ Yes |
| `<DATE>` | YYYYMMDD | 20220101 | ✅ Yes |
| `<TIME>` | HHMMSS | 000000 | ⚠️ Usually 000000 for daily |
| `<OPEN>` | Number | 1234.5 | ✅ Yes |
| `<HIGH>` | Number | 1245.3 | ✅ Yes |
| `<LOW>` | Number | 1230.2 | ✅ Yes |
| `<CLOSE>` | Number | 1240.5 | ✅ **Critical** |
| `<VOL>` | Integer | 12345600 | ⚠️ Optional |
| `<OPENINT>` | Integer | 0 | ⚠️ Optional |

**Note**: The CLOSE column is **critical** as it's used for VaR calculations.

### Data Quality Requirements

For accurate VaR calculations, ensure:
- ✅ Minimum 500+ trading days of historical data (for reliability)
- ✅ Continuous daily data (no missing trading days is ideal)
- ✅ Valid numerical values for CLOSE prices
- ✅ Dates in correct YYYYMMDD format
- ✅ Data sorted chronologically (oldest to newest)

---

## Batch Download

### Downloading Multiple Stocks Efficiently

**Method 1: Manual Batch Download**

1. On Stooq TSE Stock List (https://stooq.com/db/h/?d=1)
2. Select multiple stocks (if checkbox available)
3. Choose "Download All" or similar option
4. Download will be a ZIP file
5. Extract files and use the data directly

**Method 2: Using Browser Extensions**

- Use "Download Manager" or "Batch Download" browser extensions
- Create a list of URLs from Stooq
- Let the extension download all files

**Method 3: Automated Script (Optional)**

For advanced users, create a Python script to download from Stooq:

```python
import requests
import os

# Example: Download multiple stocks
stocks = ['1301', '1305', '1306', '2001', '2002']

for ticker in stocks:
    url = f"https://stooq.com/q/d/?s={ticker}.JP&c=d&barscount=500000&i=d"
    filename = f"{ticker}.jp.txt"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {ticker}")
```

---

## Troubleshooting

### Problem 1: "Stock data file not found for ticker: 1301"

**Cause**: The downloaded file is unavailable to the tool.

**Solution**:
1. Confirm the CSV file was downloaded successfully.
2. Verify the file can be opened locally.
3. Re-download the file from Stooq if needed.

### Problem 2: "Failed to parse CSV file"

**Cause**: CSV format is incorrect or file encoding is wrong

**Solution**:
1. Open the downloaded file in a text editor
2. Verify it matches the Stooq format with columns: `<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>`
3. Check file encoding is UTF-8 (not Unicode or other encoding)
4. Ensure no extra spaces or quotes around column headers

### Problem 3: Data Not Loading in Application

**Cause**: Data format issue or unreadable file

**Solution**:
1. Run command-line test:
   ```bash
   python3 data_reader.py
   ```
   - Enter ticker: `1301`
   - This will show if file is found and readable

2. Ensure the downloaded CSV is readable and not locked by another app.

### Problem 4: "Invalid Date Format"

**Cause**: Dates in CSV are not in YYYYMMDD format

**Solution**:
1. Download fresh data from Stooq (ensure "daily" data is selected)
2. Stooq might have other date formats available
3. Request only daily data (period = 'd')

### Problem 5: GUI Says "No Data Available"

**Cause**: No valid downloaded stock data is currently available.

**Solution**:
1. Download at least one stock CSV from Stooq.
2. Verify it includes required Stooq columns.
3. Restart the application.

---

## Alternative Data Sources

If you have issues with Stooq, consider these alternatives:

### 1. **Yahoo Finance** (via yfinance library)
```python
import yfinance as yf

# Download TSE stock data
df = yf.download('1301.T', start='2020-01-01', end='2024-01-01')
df.to_csv('1301_yahoo.csv')
```

### 2. **Google Finance**
- Visit: https://www.google.com/finance/quote/1301:TYO
- Look for download/export options

### 3. **Japanese Exchange Group (JPX)**
- Official TSE data: https://www.jpx.co.jp/

### 4. **Other CSV providers**
- Ensure CSV has at least: Date, Open, High, Low, Close, Volume columns

---

## Verification Checklist

Before using data in the VaR tool:

- [ ] Downloaded CSV files from https://stooq.com/db/h/
- [ ] Verified file format contains `<CLOSE>` column
- [ ] Verified date format is YYYYMMDD
- [ ] Files are readable (no permission issues)
- [ ] CSV is valid (can open in text editor)
- [ ] Have at least 500+ trading days of data

---

## Common Stock Tickers for Testing

| Ticker | Company | Exchange | Category |
|--------|---------|----------|----------|
| 1301 | Toyota | TSE | Stock |
| 1305 | MAXIS TSE 1xx | TSE | ETF |
| 1332 | Nippon Life | TSE | Stock |
| 2001 | Nippon Steel | TSE | Stock |
| 2002 | Sumitomo Metal | TSE | Stock |
| 9984 | SoftBank | TSE | Stock |
| 9997 | Telekom | TSE | Stock |

---

## Support

If you encounter issues:

1. **Check this guide** for your specific problem
2. **Review the Troubleshooting section**
3. **Check file format** in a text editor
4. **Run test command**: `python3 data_reader.py`
5. **Review INSTALLATION.md** for general setup issues
6. **See CONTRIBUTING.md** for reporting issues

---

## Summary

**To use the VaR Tool with Stooq data**:

1. Visit: **https://stooq.com/db/h/**
2. Download CSV files for TSE stocks
3. Verify CSV format includes required Stooq columns
4. Run: `python3 main.py`
5. Select ticker and click "Load Data"

That's it! Your data is ready for VaR analysis.

---

**Last Updated**: April 29, 2026  
**Version**: 1.0.0
