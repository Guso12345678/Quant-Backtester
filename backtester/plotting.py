import matplotlib.pyplot as plt 
import numpy as np 

def plot_equity_curve(results, benchmark_curve=None, title="Equity curve"): 
    dates = [point["date"] for point in results.equity_curve]
    equity = [point["equity"] for point in results.equity_curve]
    fig,ax = plt.subplots(figsize=(10,5))
    ax.plot(dates,equity,label="Estrategia",color="tab:blue")

    if benchmark_curve is not None: 
        bench_dates = [p["date"] for p in benchmark_curve]
        bench_equity = [p["equity"] for p in benchmark_curve]
        ax.plot(bench_dates,bench_equity,label="Buy & Hold", color="tab:gray",linestyle="--")

    for trade in results.trades: 
        color = "green" if trade["size"] > 0 else "red"
        marker = "^" if trade["size"] > 0 else "v"
        equity_at_trade = next(p["equity"] for p in results.equity_curve if p["date"] == trade["date"])
        ax.scatter(trade["date"], equity_at_trade, color=color, marker=marker, zorder=5, s=20)

    ax.set_title(title)
    ax.set_ylabel("Valor de la cartera")
    ax.legend()
    fig.tight_layout()
    return fig

def plot_drawdown(results,title="Drawdown"): 
    equity = np.array([point["equity"] for point in results.equity_curve])
    dates = [point["date"] for point in results.equity_curve]

    running_max = np.maximum.accumulate(equity)
    drawdowns = (equity - running_max)/running_max

    fig,ax = plt.subplots(figsize=(10,3))
    ax.fill_between(dates,drawdowns,0,color="tab:red",alpha=0.3)
    ax.plot(dates,drawdowns, color="tab:red", linewidth=1)

    ax.set_title(title)
    ax.set_ylabel("Drawdown")
    fig.tight_layout()
    return fig
 
