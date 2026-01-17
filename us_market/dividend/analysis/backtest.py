"""
Backtest Engine for Dividend Portfolios
Historical simulation with dividend reinvestment
"""
import yfinance as yf
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class BacktestEngine:
    def __init__(self, benchmark: str = 'SPY'):
        self.benchmark = benchmark
    
    def run_backtest(
        self,
        portfolio: List[Tuple[str, float]],
        start_date: str,
        end_date: Optional[str] = None,
        initial_capital: float = 100000
    ) -> Dict:
        """Run backtest on portfolio."""
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        tickers = [t for t, _ in portfolio]
        # Normalize weights
        raw_weights = np.array([w for _, w in portfolio])
        if raw_weights.sum() == 0:
             return {"error": "Total weight cannot be zero"}
        weights = raw_weights / raw_weights.sum()
        
        # Fetch price data
        price_data = {}
        dividend_data = {}
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(start=start_date, end=end_date)
                if not hist.empty:
                    price_data[ticker] = hist['Close']
                    divs = stock.dividends
                    if divs is not None and len(divs) > 0:
                        # Ensure timezone naive
                        divs.index = divs.index.tz_localize(None)
                        # Filter range
                        start_dt = pd.Timestamp(start_date)
                        end_dt = pd.Timestamp(end_date)
                        mask = (divs.index >= start_dt) & (divs.index <= end_dt)
                        dividend_data[ticker] = divs[mask]
            except Exception as e:
                logger.error(f"Error fetching {ticker}: {e}")
        
        if len(price_data) == 0:
            return {"error": "No valid price data"}
        
        prices_df = pd.DataFrame(price_data).dropna()
        if len(prices_df) < 10:
            return {"error": "Insufficient data (less than 10 days)"}
        
        returns_df = prices_df.pct_change().dropna()
        
        # Align weights to available tickers
        available = list(prices_df.columns)
        aligned_weights = []
        for t in available:
            # Find weight for ticker t
            found = False
            for i, p_ticker in enumerate(tickers):
                if p_ticker == t:
                    aligned_weights.append(weights[i])
                    found = True
                    break
            if not found:
                aligned_weights.append(0)
        
        aligned_weights = np.array(aligned_weights)
        if aligned_weights.sum() > 0:
            aligned_weights = aligned_weights / aligned_weights.sum()
        
        # Portfolio returns
        portfolio_returns = (returns_df * aligned_weights).sum(axis=1)
        price_cumulative = (1 + portfolio_returns).cumprod()
        
        # Calculate dividends
        total_dividends = 0
        for i, ticker in enumerate(available):
            w = aligned_weights[i]
            divs = dividend_data.get(ticker, pd.Series(dtype=float))
            if len(divs) > 0:
                init_price = prices_df[ticker].iloc[0]
                if init_price > 0:
                    shares = (initial_capital * w) / init_price
                    total_dividends += divs.sum() * shares
        
        # Results
        final_price = initial_capital * price_cumulative.iloc[-1]
        final_total = final_price + total_dividends
        
        price_return = price_cumulative.iloc[-1] - 1
        total_return = (final_total - initial_capital) / initial_capital
        
        # CAGR
        start_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_obj = datetime.strptime(end_date, '%Y-%m-%d')
        years = (end_obj - start_obj).days / 365.25
        cagr = (final_total / initial_capital) ** (1 / years) - 1 if years > 0.5 else total_return
        
        # Max drawdown
        rolling_max = price_cumulative.expanding().max()
        drawdowns = (price_cumulative - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()
        
        # Volatility and Sharpe
        annual_vol = portfolio_returns.std() * np.sqrt(252)
        annual_ret = portfolio_returns.mean() * 252
        sharpe = (annual_ret - 0.05) / annual_vol if annual_vol > 0 else 0
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "final_value": round(final_total, 2),
            "total_return": round(float(total_return), 4),
            "price_return": round(float(price_return), 4),
            "dividend_return": round(total_dividends / initial_capital, 4),
            "cagr": round(float(cagr), 4),
            "max_drawdown": round(float(max_drawdown), 4),
            "volatility": round(float(annual_vol), 4),
            "sharpe_ratio": round(float(sharpe), 2)
        }
