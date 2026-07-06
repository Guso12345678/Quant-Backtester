#This python script acts to prepare every single part of the temporal loop, it does not know how the portfolio is updated. 
#It just ensure problems like the look-ahead bias. 
from dataclasses import dataclass, field 
from typing import List

@dataclass
class BacktestResults: 
    equity_curve: list = field(default_factory=list)
    trades: list = field(default_factory=list)

class Backtester: 
    def __init__(self,data, strategy, portfolio, execution_model): 
        self.data = data #Any dataframe, from any source and any coin
        self.strategy = strategy #The strategy that is going to decide the target_postion
        self.portfolio = portfolio #The portfolio that we are going to actualize
        self.execution_model = execution_model 

        self.results = BacktestResults()

    def run(self) -> BacktestResults: 
        for i in range(len(self.data)): 

            old_data = self.data.iloc[: i+1] #Include the actual one, we avoid the look-ahead bias. 
            current_price = self.data.iloc[i]["Close"]
            direction = self.strategy.generate_signal(old_data)#Generate the position based on the strategy

            current_position = self.portfolio.current_position()

            target_shares = self._target_to_shares(direction,current_price)
            order = self.position_to_order(target_shares,current_position) 

            #Only execute when the order is != 0:
            if order != 0: 
                if i + 1 < len(self.data):#To avoid IndexError.
                    #This part is to represent in a real way the difference between when we decide and we execute. 
                    next_bar_price = self.data.iloc[i+1]["Open"]
                    fill_price = self.execution_model.execute(order_size=order,reference_price=next_bar_price)
                    self.portfolio.update_position(order, fill_price)
                    self.results.trades.append({
                        "date": self.data.index[i+1], 
                        "size": order, 
                        "price": fill_price
                    })
            
            total_value = self.portfolio.total_value(current_price)
            self.results.equity_curve.append({
                "date": self.data.index[i],
                "equity":total_value
            })
        return self.results
    def _target_to_shares(self,direction:int,current_price:float,allocation:float=0.95): 
        if direction == 0: 
            return 0 
        total_equity = self.portfolio.total_value(current_price)
        capital_to_invest = total_equity*allocation
        shares = int(capital_to_invest / current_price)
        return shares * direction
    @staticmethod
    def position_to_order(target_position: int, current_position: int) -> int: 
        return target_position - current_position 
    
    
            


    
