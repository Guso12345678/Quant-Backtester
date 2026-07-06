import numpy as np 

def compute_returns(equity_curve: list) -> np.ndarray: 
    values = np.array([point["equity"] for point in equity_curve])
    returns = values[1:] / values[:-1] -1 
    return returns

def total_return(equity_curve: list) -> float: 
    start = equity_curve[0]["equity"]
    end = equity_curve[-1]["equity"]
    return (end - start) / start 

def sharpe_ratio(equity_curve,periods_per_year:int = 252): 
    returns = compute_returns(equity_curve)

    if returns.std() == 0: 
        return 0.0 #No desviation with respect to the mean, so no volatility in the price. 
    
    mean_return = returns.mean()
    volatility = returns.std()

    return (mean_return / volatility) * np.sqrt(periods_per_year)

def max_drawdown(equity_curve): 
    values = np.array([point["equity"] for point in equity_curve]) 
    running_max = np.maximum.accumulate(values)
    drawdowns = (values - running_max) / running_max 
    return drawdowns.min()
