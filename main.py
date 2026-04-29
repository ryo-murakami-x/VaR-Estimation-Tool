#!/usr/bin/env python3
"""
Main Entry Point for VaR Estimation Tool
Launches the GUI application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from var_gui import main

if __name__ == "__main__":
    print("Starting VaR Estimation Tool...")
    print("This tool estimates Value at Risk using Monte Carlo simulation")
    print("based on Stooq TSE stock data.\n")
    main()
