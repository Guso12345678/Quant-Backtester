from backtester.data import load_data
from backtester.engine import Backtester
from backtester.portfolio import Portfolio
from backtester.execution import ExecutionModel
from strategies.sma_crossover import SMACrossover
from strategies.buy_and_hold import BuyAndHold
from backtester.metrics import total_return, sharpe_ratio, max_drawdown
from backtester.plotting import plot_equity_curve, plot_drawdown
data = load_data("AAPL","2015-01-01","2025-01-01")

engine = Backtester(
    data=data, 
    strategy=SMACrossover(fast=20,slow=50),
    portfolio=Portfolio(initial_cash=10000),
    execution_model=ExecutionModel(comission_rate=0.001,slippage_rate=0.0005)
)

results = engine.run()
benchmark_engine = Backtester(
    data=data,
    strategy=BuyAndHold(),
    portfolio=Portfolio(initial_cash=10_000),
    execution_model=ExecutionModel(comission_rate=0.001, slippage_rate=0.0005)
)
benchmark_results = benchmark_engine.run()

print(f"Retorno total SMA: {total_return(results.equity_curve)}")
print(f"Sharpe ratio SMA: {sharpe_ratio(results.equity_curve)}")
print(f"Max drawdown SMA: {max_drawdown(results.equity_curve)}")

print(f"Retorno total Buy and Hold: {total_return(benchmark_results.equity_curve)}")
print(f"Sharpe ratio Buy and Hold: {sharpe_ratio(benchmark_results.equity_curve)}")
print(f"Max drawdown Buy and Hold: {max_drawdown(benchmark_results.equity_curve)}")

fig1 = plot_equity_curve(results, benchmark_curve=benchmark_results.equity_curve,
                          title="SMA Crossover vs Buy & Hold — AAPL")
fig1.savefig("examples/equity_curve.png", dpi=150)

fig2 = plot_drawdown(results, title="Drawdown de la estrategia")
fig2.savefig("examples/drawdown.png", dpi=150)