"""
Monte Carlo VaR Estimation Module
Calculates Value at Risk using Monte Carlo simulation for stock prices
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import warnings

warnings.filterwarnings('ignore')


@dataclass
class VaRResults:
    """Data class to store VaR calculation results"""
    var_95: float
    var_99: float
    expected_shortfall_95: float
    expected_shortfall_99: float
    mean_return: float
    volatility: float
    simulations_count: int
    time_horizon_days: int
    confidence_levels: Dict[float, float]
    simulated_returns: np.ndarray
    simulated_prices: np.ndarray


class MonteCarloVaR:
    """
    Monte Carlo simulation for Value at Risk estimation
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the Monte Carlo VaR calculator.
        
        Args:
            seed (Optional[int]): Random seed for reproducibility
        """
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
        
        self.daily_returns = None
        self.mean_return = None
        self.volatility = None
        self.current_price = None
        
    def set_data(self, daily_returns: pd.Series, current_price: float):
        """
        Set the data for VaR calculation.
        
        Args:
            daily_returns (pd.Series): Series of daily returns (in decimal, not percentage)
            current_price (float): Current stock price
        """
        # Remove NaN values
        self.daily_returns = daily_returns.dropna()
        
        # Calculate statistics
        self.mean_return = self.daily_returns.mean()
        self.volatility = self.daily_returns.std()
        self.current_price = current_price
        
    def simulate_price_paths(self, 
                            num_simulations: int = 10000,
                            time_horizon: int = 10,
                            dt: float = 1/252) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate stock price paths using geometric Brownian motion.
        
        dS = μ * S * dt + σ * S * sqrt(dt) * Z
        
        Args:
            num_simulations (int): Number of Monte Carlo simulations
            time_horizon (int): Time horizon in trading days
            dt (float): Time step (default: 1/252 for daily)
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: (simulated_prices, simulated_returns)
                - simulated_prices: shape (num_simulations, time_horizon)
                - simulated_returns: shape (num_simulations,) - final returns
        """
        if self.mean_return is None or self.volatility is None:
            raise ValueError("Data not set. Call set_data() first.")
        
        # Initialize arrays
        simulated_prices = np.zeros((num_simulations, time_horizon + 1))
        simulated_prices[:, 0] = self.current_price
        
        # Generate random numbers
        Z = np.random.standard_normal((num_simulations, time_horizon))
        
        # Simulate price paths
        for t in range(1, time_horizon + 1):
            simulated_prices[:, t] = simulated_prices[:, t-1] * np.exp(
                (self.mean_return - 0.5 * self.volatility**2) * dt + 
                self.volatility * np.sqrt(dt) * Z[:, t-1]
            )
        
        # Calculate returns
        final_prices = simulated_prices[:, -1]
        simulated_returns = (final_prices - self.current_price) / self.current_price * 100
        
        return simulated_prices, simulated_returns
    
    def calculate_var(self, 
                     confidence_level: float = 0.95,
                     num_simulations: int = 10000,
                     time_horizon: int = 10) -> Tuple[float, float]:
        """
        Calculate Value at Risk (VaR) and Conditional Value at Risk (CVaR/Expected Shortfall).
        
        Args:
            confidence_level (float): Confidence level (e.g., 0.95 for 95%)
            num_simulations (int): Number of simulations
            time_horizon (int): Time horizon in trading days
        
        Returns:
            Tuple[float, float]: (VaR, CVaR) - both as percentage losses
        """
        _, simulated_returns = self.simulate_price_paths(num_simulations, time_horizon)
        
        # VaR: percentile of returns distribution
        var = np.percentile(simulated_returns, (1 - confidence_level) * 100)
        
        # CVaR (Expected Shortfall): average of worst returns beyond VaR
        cvar = simulated_returns[simulated_returns <= var].mean()
        
        return var, cvar
    
    def calculate_var_comprehensive(self,
                                   num_simulations: int = 10000,
                                   time_horizon: int = 10,
                                   confidence_levels: Optional[List[float]] = None) -> VaRResults:
        """
        Comprehensive VaR calculation with multiple confidence levels.
        
        Args:
            num_simulations (int): Number of simulations
            time_horizon (int): Time horizon in trading days
            confidence_levels (Optional[List[float]]): List of confidence levels (e.g., [0.90, 0.95, 0.99])
        
        Returns:
            VaRResults: Object containing all VaR calculations
        """
        if self.mean_return is None or self.volatility is None:
            raise ValueError("Data not set. Call set_data() first.")
        
        if confidence_levels is None:
            confidence_levels = [0.90, 0.95, 0.99]
        
        # Simulate price paths
        simulated_prices, simulated_returns = self.simulate_price_paths(
            num_simulations, time_horizon
        )
        
        # Calculate VaR and CVaR for all confidence levels
        var_dict = {}
        cvar_dict = {}
        
        for conf_level in confidence_levels:
            var = np.percentile(simulated_returns, (1 - conf_level) * 100)
            cvar = simulated_returns[simulated_returns <= var].mean()
            var_dict[conf_level] = var
            cvar_dict[conf_level] = cvar
        
        # Get 95% and 99% VaR
        var_95 = var_dict.get(0.95, np.percentile(simulated_returns, 5))
        var_99 = var_dict.get(0.99, np.percentile(simulated_returns, 1))
        cvar_95 = cvar_dict.get(0.95, simulated_returns[simulated_returns <= var_95].mean())
        cvar_99 = cvar_dict.get(0.99, simulated_returns[simulated_returns <= var_99].mean())
        
        return VaRResults(
            var_95=var_95,
            var_99=var_99,
            expected_shortfall_95=cvar_95,
            expected_shortfall_99=cvar_99,
            mean_return=float(self.mean_return),
            volatility=float(self.volatility),
            simulations_count=num_simulations,
            time_horizon_days=time_horizon,
            confidence_levels=var_dict,
            simulated_returns=simulated_returns,
            simulated_prices=simulated_prices
        )
    
    def calculate_var_dollar_terms(self, var_percent: float, 
                                  portfolio_value: float) -> float:
        """
        Convert VaR from percentage to dollar terms.
        
        Args:
            var_percent (float): VaR as percentage
            portfolio_value (float): Portfolio value in dollars
        
        Returns:
            float: VaR in dollar terms
        """
        return abs(var_percent / 100 * portfolio_value)
    
    def get_risk_metrics(self, simulated_returns: np.ndarray) -> Dict[str, float]:
        """
        Calculate additional risk metrics from simulated returns.
        
        Args:
            simulated_returns (np.ndarray): Array of simulated returns
        
        Returns:
            Dict[str, float]: Dictionary with risk metrics
        """
        metrics = {
            "mean": np.mean(simulated_returns),
            "std": np.std(simulated_returns),
            "min": np.min(simulated_returns),
            "max": np.max(simulated_returns),
            "skewness": self._calculate_skewness(simulated_returns),
            "kurtosis": self._calculate_kurtosis(simulated_returns),
            "percentile_1": np.percentile(simulated_returns, 1),
            "percentile_5": np.percentile(simulated_returns, 5),
            "percentile_95": np.percentile(simulated_returns, 95),
            "percentile_99": np.percentile(simulated_returns, 99),
        }
        return metrics
    
    @staticmethod
    def _calculate_skewness(data: np.ndarray) -> float:
        """Calculate skewness of data"""
        mean = np.mean(data)
        std = np.std(data)
        skewness = np.mean(((data - mean) / std) ** 3)
        return skewness
    
    @staticmethod
    def _calculate_kurtosis(data: np.ndarray) -> float:
        """Calculate excess kurtosis of data"""
        mean = np.mean(data)
        std = np.std(data)
        kurtosis = np.mean(((data - mean) / std) ** 4) - 3
        return kurtosis


def demonstrate_var_calculation():
    """
    Demonstration function for VaR calculation.
    """
    # Example: Create sample daily returns
    np.random.seed(42)
    daily_returns = np.random.normal(0.0005, 0.015, 1000)  # Mean 0.05%, Std 1.5%
    daily_returns_series = pd.Series(daily_returns)
    
    # Current stock price
    current_price = 3000.0
    
    # Initialize VaR calculator
    var_calc = MonteCarloVaR(seed=42)
    var_calc.set_data(daily_returns_series, current_price)
    
    print("="*70)
    print("Monte Carlo VaR Calculation - Demonstration")
    print("="*70)
    print(f"\nInput Parameters:")
    print(f"  Current Price: ¥{current_price:.2f}")
    print(f"  Mean Daily Return: {var_calc.mean_return*100:.4f}%")
    print(f"  Volatility (Std Dev): {var_calc.volatility*100:.4f}%")
    print(f"  Historical Returns: {len(daily_returns_series)} days")
    
    # Calculate comprehensive VaR
    print(f"\nRunning Monte Carlo simulation with 10,000 simulations for 10 trading days...")
    results = var_calc.calculate_var_comprehensive(
        num_simulations=10000,
        time_horizon=10,
        confidence_levels=[0.90, 0.95, 0.99]
    )
    
    print("\n" + "="*70)
    print("VaR Results (10-Day Horizon, in percentage terms)")
    print("="*70)
    print(f"\n95% Confidence Level:")
    print(f"  Value at Risk (VaR): {results.var_95:.4f}%")
    print(f"  Expected Shortfall (ES/CVaR): {results.expected_shortfall_95:.4f}%")
    print(f"  Dollar Value at Risk: ¥{abs(var_calc.calculate_var_dollar_terms(results.var_95, current_price)):.2f}")
    
    print(f"\n99% Confidence Level:")
    print(f"  Value at Risk (VaR): {results.var_99:.4f}%")
    print(f"  Expected Shortfall (ES/CVaR): {results.expected_shortfall_99:.4f}%")
    print(f"  Dollar Value at Risk: ¥{abs(var_calc.calculate_var_dollar_terms(results.var_99, current_price)):.2f}")
    
    print(f"\nAll Confidence Levels:")
    for conf_level, var_val in sorted(results.confidence_levels.items()):
        print(f"  {conf_level*100:.0f}%: {var_val:.4f}%")
    
    # Additional risk metrics
    print("\n" + "="*70)
    print("Risk Metrics from Simulated Returns")
    print("="*70)
    metrics = var_calc.get_risk_metrics(results.simulated_returns)
    for metric_name, metric_value in metrics.items():
        print(f"  {metric_name}: {metric_value:.4f}%")
    
    print(f"\nSimulation Statistics:")
    print(f"  Total Simulations: {results.simulations_count:,}")
    print(f"  Time Horizon: {results.time_horizon_days} trading days")


if __name__ == "__main__":
    demonstrate_var_calculation()
