# Data Directory

This directory is for storing stock data downloaded from Stooq.

## Important Notice

CSV data files are **NOT included** in this repository and should **NOT be committed** to GitHub.

## Setup Instructions

1. **Download data from Stooq**: https://stooq.com/db/h/
2. **Follow setup guide**: See [STOOQ_DATA_SETUP.md](../STOOQ_DATA_SETUP.md)
3. **Place files** in the appropriate subdirectories:
   - `daily/jp/tse stocks/1/` - For ticker codes starting with 1 (1001-1999)
   - `daily/jp/tse stocks/2/` - For ticker codes starting with 2 (2000-2999)

## Expected Structure

```
data/
└── daily/
    └── jp/
        └── tse stocks/
            ├── 1/
            │   ├── 1301.jp.txt
            │   ├── 1332.jp.txt
            │   └── ...
            └── 2/
                ├── 2001.jp.txt
                ├── 2002.jp.txt
                └── ...
```

## File Format

Files should be named: `{ticker}.jp.txt`

Example: `1301.jp.txt` for Toyota

## Why Data is Not Included

- **File Size**: Stooq data files can be large (several MB each)
- **Updates**: Data changes daily; static snapshots become outdated
- **User Choice**: Users may want different time periods or stocks
- **License Compliance**: Stooq data should be downloaded directly
- **Repository Size**: Keeping repo small for easier distribution

## Getting Started

1. Read: [STOOQ_DATA_SETUP.md](../STOOQ_DATA_SETUP.md)
2. Download: CSV files from Stooq
3. Extract: To the appropriate subdirectory
4. Run: Application to load and analyze data

For detailed instructions, see: [STOOQ_DATA_SETUP.md](../STOOQ_DATA_SETUP.md)
