"""
GUI for VaR Estimation Tool
Using tkinter for the interface and matplotlib for visualizations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from data_reader import StooqDataReader
from var_calculator import MonteCarloVaR


class VaREstimationGUI:
    """
    GUI Application for VaR Estimation
    """
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("VaR Estimation Tool - Stooq Data Analysis")
        self.root.geometry("1400x900")
        
        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Data and calculation objects
        self.data_reader = StooqDataReader()
        self.var_calculator = MonteCarloVaR(seed=42)
        self.current_data = None
        self.var_results = None
        self.calculation_thread = None
        
        # Create GUI components
        self._create_widgets()
        
    def _create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Right panel - Results and Visualization
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ===== LEFT PANEL =====
        # Title
        title_label = ttk.Label(left_panel, text="Stock Selection", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Ticker input
        ttk.Label(left_panel, text="Stock Ticker:").pack(anchor=tk.W)
        self.ticker_var = tk.StringVar()
        ticker_frame = ttk.Frame(left_panel)
        ticker_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.ticker_entry = ttk.Entry(ticker_frame, textvariable=self.ticker_var, width=15)
        self.ticker_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        self.load_button = ttk.Button(ticker_frame, text="Load Data", command=self._load_stock_data)
        self.load_button.pack(side=tk.LEFT)
        
        # Data info
        info_frame = ttk.LabelFrame(left_panel, text="Data Information", padding=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.info_text = tk.Text(info_frame, height=8, width=35, state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # VaR Parameters
        params_frame = ttk.LabelFrame(left_panel, text="VaR Parameters", padding=10)
        params_frame.pack(fill=tk.X, pady=10)
        
        # Number of simulations
        ttk.Label(params_frame, text="Simulations:").pack(anchor=tk.W)
        self.sims_var = tk.IntVar(value=10000)
        sims_spinbox = ttk.Spinbox(params_frame, from_=1000, to=100000, 
                                    textvariable=self.sims_var, increment=1000)
        sims_spinbox.pack(fill=tk.X, pady=(0, 10))
        
        # Time horizon
        ttk.Label(params_frame, text="Time Horizon (days):").pack(anchor=tk.W)
        self.horizon_var = tk.IntVar(value=10)
        horizon_spinbox = ttk.Spinbox(params_frame, from_=1, to=252, 
                                      textvariable=self.horizon_var, increment=1)
        horizon_spinbox.pack(fill=tk.X, pady=(0, 10))
        
        # Confidence level
        ttk.Label(params_frame, text="Confidence Level:").pack(anchor=tk.W)
        self.confidence_var = tk.StringVar(value="95")
        confidence_combo = ttk.Combobox(params_frame, textvariable=self.confidence_var,
                                        values=["90", "95", "99"], state="readonly")
        confidence_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Portfolio value
        ttk.Label(params_frame, text="Portfolio Value (¥):").pack(anchor=tk.W)
        self.portfolio_var = tk.DoubleVar(value=1000000)
        portfolio_entry = ttk.Entry(params_frame, textvariable=self.portfolio_var)
        portfolio_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Calculate button
        self.calc_button = ttk.Button(params_frame, text="Calculate VaR", 
                                      command=self._calculate_var)
        self.calc_button.pack(fill=tk.X)
        
        # Status
        status_frame = ttk.LabelFrame(left_panel, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="green")
        self.status_label.pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        # ===== RIGHT PANEL =====
        # Notebook for tabs
        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Results tab
        results_tab = ttk.Frame(notebook)
        notebook.add(results_tab, text="VaR Results")
        self._create_results_tab(results_tab)
        
        # Chart tab
        chart_tab = ttk.Frame(notebook)
        notebook.add(chart_tab, text="Distribution Chart")
        self.chart_frame = chart_tab
        
        # Data preview tab
        preview_tab = ttk.Frame(notebook)
        notebook.add(preview_tab, text="Data Preview")
        self._create_preview_tab(preview_tab)
        
    def _create_results_tab(self, parent):
        """Create the results display tab"""
        results_frame = ttk.Frame(parent)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results text area
        self.results_text = tk.Text(results_frame, height=25, width=50, 
                                     state=tk.DISABLED, font=("Courier", 10))
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                  command=self.results_text.yview)
        self.results_text['yscrollcommand'] = scrollbar.set
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_preview_tab(self, parent):
        """Create the data preview tab"""
        preview_frame = ttk.Frame(parent)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add treeview for data display
        columns = ("Date", "Open", "High", "Low", "Close", "Volume")
        tree = ttk.Treeview(preview_frame, columns=columns, height=25, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=tree.yview)
        tree['yscrollcommand'] = scrollbar.set
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.data_tree = tree
    
    def _load_stock_data(self):
        """Load stock data"""
        ticker = self.ticker_var.get().strip()
        
        if not ticker:
            messagebox.showerror("Error", "Please enter a stock ticker")
            return
        
        try:
            self.status_label.config(text="Loading data...", foreground="orange")
            self.root.update()
            
            success, message, df = self.data_reader.load_stock_data(ticker)
            
            if success:
                self.current_data = df
                self._update_info_display(df)
                self._update_data_preview(df)
                
                # Prepare data for VaR calculation
                daily_returns = self.data_reader.get_daily_returns()
                current_price = df['CLOSE'].iloc[-1]
                self.var_calculator.set_data(daily_returns / 100, current_price)  # Convert to decimal
                
                self.status_label.config(text="Data loaded successfully", foreground="green")
                messagebox.showinfo("Success", f"{message}")
            else:
                self.status_label.config(text="Failed to load data", foreground="red")
                messagebox.showerror("Error", message)
        
        except Exception as e:
            self.status_label.config(text="Error loading data", foreground="red")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _update_info_display(self, df):
        """Update the information display"""
        summary = self.data_reader.get_summary_info()
        
        info_text = f"""
Ticker: {summary['ticker']}
Records: {summary['records']:,}
Start Date: {summary['start_date']}
End Date: {summary['end_date']}

Price Statistics:
Min: ¥{summary['close_price_min']:.2f}
Max: ¥{summary['close_price_max']:.2f}
Mean: ¥{summary['close_price_mean']:.2f}

Current Price: ¥{df['CLOSE'].iloc[-1]:.2f}
"""
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", info_text)
        self.info_text.config(state=tk.DISABLED)
    
    def _update_data_preview(self, df):
        """Update the data preview treeview"""
        # Clear existing items
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Add last 20 rows
        for idx, row in df.tail(20).iterrows():
            date_str = row['DATE'].strftime('%Y-%m-%d')
            values = (
                date_str,
                f"{row['OPEN']:.2f}",
                f"{row['HIGH']:.2f}",
                f"{row['LOW']:.2f}",
                f"{row['CLOSE']:.2f}",
                f"{int(row['VOL']):,}"
            )
            self.data_tree.insert("", "end", values=values)
    
    def _calculate_var(self):
        """Calculate VaR (in a separate thread to prevent GUI freezing)"""
        if self.current_data is None:
            messagebox.showerror("Error", "Please load data first")
            return
        
        # Disable calculation while running
        self.calc_button.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Calculating VaR...", foreground="orange")
        
        # Run calculation in separate thread
        self.calculation_thread = threading.Thread(target=self._calculate_var_thread)
        self.calculation_thread.daemon = True
        self.calculation_thread.start()
    
    def _calculate_var_thread(self):
        """Thread function for VaR calculation"""
        try:
            num_sims = self.sims_var.get()
            time_horizon = self.horizon_var.get()
            
            # Calculate VaR
            self.var_results = self.var_calculator.calculate_var_comprehensive(
                num_simulations=num_sims,
                time_horizon=time_horizon,
                confidence_levels=[0.90, 0.95, 0.99]
            )
            
            # Update results display
            self.root.after(0, self._display_var_results)
            self.root.after(0, self._display_distribution_chart)
            
            self.root.after(0, lambda: self.calc_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.status_label.config(text="VaR calculation completed", foreground="green"))
        
        except Exception as e:
            self.root.after(0, lambda: self.calc_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.status_label.config(text="Calculation failed", foreground="red"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Calculation failed: {str(e)}"))
    
    def _display_var_results(self):
        """Display VaR results"""
        if self.var_results is None:
            return
        
        results = self.var_results
        portfolio_value = self.portfolio_var.get()
        confidence = float(self.confidence_var.get()) / 100
        
        # Calculate VaR in dollar terms
        var_95_dollar = abs(self.var_calculator.calculate_var_dollar_terms(
            results.var_95, portfolio_value))
        var_99_dollar = abs(self.var_calculator.calculate_var_dollar_terms(
            results.var_99, portfolio_value))
        
        results_text = f"""
{'='*50}
VaR ESTIMATION RESULTS
{'='*50}

PARAMETERS:
  Time Horizon: {results.time_horizon_days} trading days
  Simulations: {results.simulations_count:,}
  Portfolio Value: ¥{portfolio_value:,.0f}
  Current Stock Price: ¥{self.var_calculator.current_price:.2f}

HISTORICAL STATISTICS:
  Mean Daily Return: {results.mean_return*100:.4f}%
  Daily Volatility: {results.volatility*100:.4f}%

VaR RESULTS:
  
  95% Confidence Level:
    VaR (percentage): {results.var_95:.4f}%
    VaR (dollar): ¥{var_95_dollar:,.2f}
    Expected Shortfall: {results.expected_shortfall_95:.4f}%
    
  99% Confidence Level:
    VaR (percentage): {results.var_99:.4f}%
    VaR (dollar): ¥{var_99_dollar:,.2f}
    Expected Shortfall: {results.expected_shortfall_99:.4f}%

ALL CONFIDENCE LEVELS:
"""
        for conf_level, var_val in sorted(results.confidence_levels.items()):
            results_text += f"\n  {conf_level*100:.0f}%: {var_val:.4f}%"
        
        # Risk metrics
        metrics = self.var_calculator.get_risk_metrics(results.simulated_returns)
        results_text += f"""

DISTRIBUTION METRICS:
  Mean: {metrics['mean']:.4f}%
  Std Dev: {metrics['std']:.4f}%
  Min: {metrics['min']:.4f}%
  Max: {metrics['max']:.4f}%
  Skewness: {metrics['skewness']:.6f}
  Kurtosis: {metrics['kurtosis']:.6f}
  
  1st Percentile: {metrics['percentile_1']:.4f}%
  5th Percentile: {metrics['percentile_5']:.4f}%
  95th Percentile: {metrics['percentile_95']:.4f}%
  99th Percentile: {metrics['percentile_99']:.4f}%

{'='*50}
INTERPRETATION:
With {self.confidence_var.get()}% confidence, the maximum loss
over the next {results.time_horizon_days} trading days will be
no more than ¥{var_95_dollar:,.2f} ({results.var_95:.4f}%)
of the portfolio value.
{'='*50}
"""
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", results_text)
        self.results_text.config(state=tk.DISABLED)
    
    def _display_distribution_chart(self):
        """Display the return distribution chart"""
        if self.var_results is None:
            return
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create figure
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot histogram
        returns = self.var_results.simulated_returns
        ax.hist(returns, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Add VaR lines
        ax.axvline(self.var_results.var_95, color='orange', linestyle='--', 
                  linewidth=2, label=f"95% VaR: {self.var_results.var_95:.4f}%")
        ax.axvline(self.var_results.var_99, color='red', linestyle='--', 
                  linewidth=2, label=f"99% VaR: {self.var_results.var_99:.4f}%")
        ax.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
        
        ax.set_xlabel("Return (%)", fontsize=10)
        ax.set_ylabel("Frequency", fontsize=10)
        ax.set_title("Distribution of Simulated Returns", fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = VaREstimationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
