"""
Integration Test Script
Demonstrates all components of the VaR Estimation Tool working together
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_reader import StooqDataReader
from var_calculator import MonteCarloVaR
import pandas as pd


def test_data_reader():
    """Test data reading functionality"""
    print("\n" + "="*70)
    print("TEST 1: Data Reader Component")
    print("="*70)
    
    reader = StooqDataReader()
    
    # Test loading stock data - using tickers that exist in the data
    tickers_to_test = ["1301", "1332", "2001"]
    
    for ticker in tickers_to_test:
        print(f"\nLoading ticker: {ticker}")
        success, message, df = reader.load_stock_data(ticker)
        
        if success:
            print(f"  ✓ {message}")
            
            # Validate data
            is_valid, issues = reader.validate_data()
            if is_valid:
                print(f"  ✓ Data validation passed")
            else:
                print(f"  ✗ Validation issues: {issues}")
            
            # Get summary
            summary = reader.get_summary_info()
            print(f"  - Records: {summary['records']}")
            print(f"  - Date range: {summary['start_date']} to {summary['end_date']}")
            print(f"  - Current price: ¥{df['CLOSE'].iloc[-1]:.2f}")
        else:
            print(f"  ✗ Failed: {message}")
            return False
    
    return True


def test_var_calculator():
    """Test VaR calculation functionality"""
    print("\n" + "="*70)
    print("TEST 2: VaR Calculator Component")
    print("="*70)
    
    # Load real stock data
    print("\nLoading stock data for calculation...")
    reader = StooqDataReader()
    success, message, df = reader.load_stock_data("1301")
    
    if not success:
        print(f"  ✗ Failed to load data: {message}")
        return False
    
    print(f"  ✓ Loaded {len(df)} records")
    
    # Get daily returns
    daily_returns = reader.get_daily_returns()
    current_price = df['CLOSE'].iloc[-1]
    
    print(f"  - Current price: ¥{current_price:.2f}")
    print(f"  - Mean daily return: {daily_returns.mean():.4f}%")
    print(f"  - Daily volatility: {daily_returns.std():.4f}%")
    
    # Initialize VaR calculator
    var_calc = MonteCarloVaR(seed=42)
    var_calc.set_data(daily_returns / 100, current_price)  # Convert to decimal
    
    # Test different scenarios
    scenarios = [
        {"sims": 5000, "horizon": 5, "desc": "5-day, 5K simulations"},
        {"sims": 10000, "horizon": 10, "desc": "10-day, 10K simulations"},
        {"sims": 10000, "horizon": 21, "desc": "1-month, 10K simulations"},
    ]
    
    for scenario in scenarios:
        print(f"\n  Scenario: {scenario['desc']}")
        results = var_calc.calculate_var_comprehensive(
            num_simulations=scenario['sims'],
            time_horizon=scenario['horizon']
        )
        
        print(f"    95% VaR: {results.var_95:.4f}%")
        print(f"    99% VaR: {results.var_99:.4f}%")
        
        # Dollar VaR for 1M portfolio
        portfolio = 1000000
        var_dollar = abs(var_calc.calculate_var_dollar_terms(results.var_95, portfolio))
        print(f"    Dollar VaR (1M ¥): ¥{var_dollar:,.2f}")
    
    return True


def test_integration():
    """Test full integration of all components"""
    print("\n" + "="*70)
    print("TEST 3: Full Integration Test")
    print("="*70)
    
    # Select ticker
    ticker = "1301"
    print(f"\nTesting with ticker: {ticker}")
    
    # Load data
    print("\n1. Loading data...")
    reader = StooqDataReader()
    success, message, df = reader.load_stock_data(ticker)
    if not success:
        print(f"   ✗ Failed: {message}")
        return False
    print(f"   ✓ Loaded {len(df)} records")
    
    # Prepare data
    print("\n2. Preparing data...")
    daily_returns = reader.get_daily_returns()
    current_price = df['CLOSE'].iloc[-1]
    print(f"   ✓ Current price: ¥{current_price:.2f}")
    print(f"   ✓ Historical volatility: {daily_returns.std():.4f}%")
    
    # Calculate VaR
    print("\n3. Calculating VaR...")
    var_calc = MonteCarloVaR(seed=42)
    var_calc.set_data(daily_returns / 100, current_price)
    
    results = var_calc.calculate_var_comprehensive(
        num_simulations=10000,
        time_horizon=10
    )
    print(f"   ✓ Completed 10,000 simulations")
    
    # Display comprehensive results
    print("\n4. VaR Results (10-day horizon):")
    print(f"\n   95% Confidence Level:")
    print(f"     - VaR: {results.var_95:.4f}%")
    print(f"     - Expected Shortfall: {results.expected_shortfall_95:.4f}%")
    
    print(f"\n   99% Confidence Level:")
    print(f"     - VaR: {results.var_99:.4f}%")
    print(f"     - Expected Shortfall: {results.expected_shortfall_99:.4f}%")
    
    # Risk metrics
    print(f"\n5. Distribution Metrics:")
    metrics = var_calc.get_risk_metrics(results.simulated_returns)
    print(f"   - Mean return: {metrics['mean']:.4f}%")
    print(f"   - Std deviation: {metrics['std']:.4f}%")
    print(f"   - Min: {metrics['min']:.4f}%")
    print(f"   - Max: {metrics['max']:.4f}%")
    print(f"   - Skewness: {metrics['skewness']:.6f}")
    print(f"   - Kurtosis: {metrics['kurtosis']:.6f}")
    
    # Interpretation
    print(f"\n6. Risk Interpretation (¥1,000,000 portfolio):")
    portfolio = 1000000
    var_dollar_95 = abs(var_calc.calculate_var_dollar_terms(results.var_95, portfolio))
    var_dollar_99 = abs(var_calc.calculate_var_dollar_terms(results.var_99, portfolio))
    
    print(f"   95% confidence: Maximum loss ¥{var_dollar_95:,.2f} in 10 days")
    print(f"   99% confidence: Maximum loss ¥{var_dollar_99:,.2f} in 10 days")
    
    return True


def main():
    """Run all integration tests"""
    print("\n" + "#"*70)
    print("# VaR ESTIMATION TOOL - INTEGRATION TESTS")
    print("#"*70)
    
    tests = [
        ("Data Reader", test_data_reader),
        ("VaR Calculator", test_var_calculator),
        ("Full Integration", test_integration)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = "PASS" if result else "FAIL"
        except Exception as e:
            print(f"\n  ✗ Exception: {str(e)}")
            results[test_name] = "ERROR"
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, result in results.items():
        status_symbol = "✓" if result == "PASS" else "✗"
        print(f"{status_symbol} {test_name}: {result}")
    
    all_passed = all(r == "PASS" for r in results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✓ All tests passed successfully!")
        print("\nThe VaR Estimation Tool is ready to use.")
        print("Run 'python3 main.py' to launch the GUI application.")
    else:
        print("✗ Some tests failed. Please review the output above.")
    print("="*70 + "\n")
    
    return all_passed


if __name__ == "__main__":
    import time
    start_time = time.time()
    
    success = main()
    
    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds\n")
    
    sys.exit(0 if success else 1)
