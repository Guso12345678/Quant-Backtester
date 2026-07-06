# Quant Backtester — Motor de backtesting construido desde cero
 
Motor de backtesting implementado en Python sin depender de librerías de alto nivel como `backtrader` o `zipline`. El objetivo del proyecto no es encontrar una estrategia ganadora, sino construir con rigor la herramienta que permite evaluar honestamente si una estrategia de trading habría funcionado en el pasado.
 
---
 
## ¿Por qué construir el motor desde cero?
 
Cualquiera puede conectar una librería de backtesting y obtener una curva de equity bonita. Este proyecto construye el motor a propósito, para poder razonar y defender cada decisión de diseño: cómo se evita el look-ahead bias, cómo se modelan los costes de transacción, y por qué una estrategia gana o pierde frente a un benchmark simple.
 
---
 
## Estructura del proyecto
 
```
quant-backtester/
├── backtester/               # Motor: agnóstico a la estrategia usada
│   ├── engine.py             # Bucle temporal, orquesta todo lo demás
│   ├── strategy.py           # Interfaz abstracta Strategy
│   ├── portfolio.py          # Contabilidad: cash, posición, valor total
│   ├── execution.py          # Simula comisión y slippage
│   ├── data.py               # Carga y limpieza de datos (yfinance / CSV)
│   ├── metrics.py            # Sharpe ratio, drawdown, retorno total
│   └── plotting.py           # Curva de equity y drawdown
│
├── strategies/               # Estrategias concretas, desacopladas del motor
│   ├── sma_crossover.py      # SMA Crossover (fast/slow configurable)
│   └── buy_and_hold.py       # Benchmark de referencia
│
├── examples/
│   └── run_sma_appl.py       # Script end-to-end sobre AAPL
│
└── tests/                    # Tests unitarios de cada módulo
```
 
---
 
## Cómo ejecutarlo
 
```bash
git clone https://github.com/Guso12345678/quant-backtester.git
cd quant-backtester
pip install -e .
python -m examples.run_sma_appl
```
 
---
 
## Uso básico
 
```python
from backtester.data import load_data
from backtester.engine import Backtester
from backtester.portfolio import Portfolio
from backtester.execution import ExecutionModel
from strategies.sma_crossover import SMACrossover
 
data = load_data("AAPL", "2015-01-01", "2025-01-01")
 
engine = Backtester(
    data=data,
    strategy=SMACrossover(fast=20, slow=50),
    portfolio=Portfolio(initial_cash=10_000),
    execution_model=ExecutionModel(commission_rate=0.001, slippage_rate=0.0005)
)
 
results = engine.run()
```
 
---
 
## Decisiones de diseño
 
**Prevención de look-ahead bias por construcción**
En cada barra `i`, la estrategia solo recibe `data.iloc[:i+1]` — nunca ve el dataset completo. Es estructuralmente imposible que una estrategia mire al futuro, no depende de que el programador "tenga cuidado".
 
**Ejecución en la barra siguiente, no en la actual**
Una decisión tomada con el cierre de la barra `i` se ejecuta contra el precio de apertura de la barra `i+1`. Decidir con el cierre de hoy y ejecutar al cierre de hoy sería otra forma de look-ahead bias, muy común en backtesters mal construidos.
 
```python
# engine.py — la decisión y la ejecución están separadas por una barra
direction = self.strategy.generate_signal(data.iloc[:i+1])
next_bar_price = self.data.iloc[i+1]["Open"]
fill_price = self.execution_model.execute(order_size=order, reference_price=next_bar_price)
```
 
**Slippage direccional, nunca a favor del trader**
El modelo de ejecución empeora el precio en la dirección que perjudica la operación: comprar siempre cuesta más de lo que se ve, vender siempre da menos. Un slippage simétrico o aleatorio sobreestimaría la rentabilidad real de cualquier estrategia.
 
```python
# execution.py
direction = 1 if order_size > 0 else -1
slipped_price = reference_price * (1 + direction * self.slippage_rate)
```
 
**Separación estricta de responsabilidades**
`engine.py` no sabe calcular señales ni conoce el signo de la comisión. `strategy.py` no sabe nada de ejecución. `portfolio.py` no decide nada, solo contabiliza. Esta separación permite testear cada pieza de forma aislada con valores calculados a mano.
 
**Position sizing basado en capital disponible, no en unidades fijas**
La estrategia solo devuelve una dirección (`+1 / 0 / -1`). El motor traduce esa dirección en un número de acciones invirtiendo el 95% del valor total de la cartera. El 5% de colchón evita quedarse sin cash por pequeños movimientos de precio entre la decisión y la ejecución.
 
```python
# engine.py
capital_to_invest = total_equity * 0.95
shares = int(capital_to_invest / current_price) * direction
```
 
**Buy & Hold como benchmark obligatorio, no opcional**
Se ejecuta a través del mismo motor, mismo modelo de ejecución y mismos costes que cualquier otra estrategia, para que la comparación sea honesta y no le dé ventaja artificial a ninguna de las dos.
 
---
 
## Métricas implementadas
 
```python
# metrics.py
total_return(equity_curve)      # Retorno total sobre el capital inicial
sharpe_ratio(equity_curve)      # Sharpe anualizado (252 periodos/año)
max_drawdown(equity_curve)      # Máxima caída desde el pico anterior
```
 
---
 
## Resultado principal: SMA Crossover vs. Buy & Hold
 
SMA Crossover (20/50) vs. Buy & Hold sobre AAPL, 2015-2025, capital inicial 10.000 €:
 
| | SMA Crossover | Buy & Hold |
|---|---|---|
| Retorno total | ~250% | ~860% |
| Nº de operaciones | Varias decenas | 1 |
 
**La estrategia no supera al benchmark.** Esta es la conclusión honesta del proyecto, no un fallo a esconder.
 
El SMA Crossover genera múltiples señales en fases de mercado lateral ("whipsaw"): la media rápida y la lenta se cruzan repetidamente sin que haya un movimiento sostenido detrás, y cada cruce genera un coste de operación sin beneficio real. Este resultado es consistente con la dificultad conocida en la literatura de superar a buy-and-hold usando señales técnicas simples sobre un único activo en tendencia alcista de largo plazo.
 
---
 
## Tecnologías
 
- Python 3.13
- `yfinance` — descarga de datos históricos de mercado
- `pandas` / `numpy` — manipulación de series temporales y cálculo de métricas
- `matplotlib` — visualización de curvas de equity y drawdown
- `pyproject.toml` — packaging moderno
---
 
## Próximos pasos
 
- Walk-forward analysis con ventanas de entrenamiento y test separadas, para evitar overfitting sobre los parámetros `fast`/`slow`
- Estrategia de pairs trading / reversión a la media como alternativa al seguimiento de tendencia
- Soporte para múltiples activos simultáneos en el mismo portfolio
- Desglose del PnL entre spread capturado y coste de slippage por operación
---
 
## Autor
 
**Guzman Ignacio Perez Ibarz**
 
Proyecto personal orientado a quantitative finance y desarrollo de herramientas de análisis de estrategias de trading.
